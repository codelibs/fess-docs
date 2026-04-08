============================================================
第16回 検索インフラの自動化 -- CI/CDパイプラインとInfrastructure as Codeでの管理
============================================================

はじめに
========

検索システムの設定を手動で管理していると、環境の再現が難しくなり、設定ミスのリスクも高まります。
モダンな DevOps の考え方を取り入れ、検索インフラもコードとして管理し、自動化しましょう。

本記事では、Fess の設定をコードとして管理し、デプロイを自動化するアプローチを紹介します。

対象読者
========

- 検索システムの運用を自動化したい方
- DevOps/IaC の手法を検索インフラに適用したい方
- Docker と CI/CD の基本知識がある方

Infrastructure as Code の適用
==============================

Fess 環境を「コード」として管理する対象は以下の通りです。

.. list-table:: IaC 管理対象
   :header-rows: 1
   :widths: 25 35 40

   * - 対象
     - 管理方法
     - バージョン管理
   * - Docker 構成
     - docker-compose.yml
     - Git
   * - Fess 設定
     - バックアップファイル / 管理 API
     - Git
   * - 辞書データ
     - 管理 API でエクスポート
     - Git
   * - OpenSearch 設定
     - 設定ファイル
     - Git

Docker Compose による環境定義
================================

本番環境用の Docker Compose ファイル
-------------------------------------

第2回で使用した基本構成を拡張し、本番環境に適した構成を定義します。

.. code-block:: yaml

    services:
      fess:
        image: ghcr.io/codelibs/fess:15.5.0
        environment:
          - FESS_DICTIONARY_PATH=/opt/fess/dictionary
          - JAVA_OPTS=-Xmx2g -Xms2g
        volumes:
          - fess-data:/opt/fess/data
          - ./dictionary:/opt/fess/dictionary:ro
        ports:
          - "8080:8080"
        depends_on:
          opensearch:
            condition: service_healthy
        restart: unless-stopped

      opensearch:
        image: opensearchproject/opensearch:2.19.1
        environment:
          - discovery.type=single-node
          - OPENSEARCH_JAVA_OPTS=-Xmx4g -Xms4g
          - DISABLE_SECURITY_PLUGIN=true
        volumes:
          - opensearch-data:/usr/share/opensearch/data
        healthcheck:
          test: ["CMD-SHELL", "curl -s http://localhost:9200/_cluster/health | grep -q '\"status\":\"green\"\\|\"status\":\"yellow\"'"]
          interval: 30s
          timeout: 10s
          retries: 5
        restart: unless-stopped

    volumes:
      fess-data:
      opensearch-data:

ポイントは以下の通りです。

- ヘルスチェックの定義: OpenSearch が準備できてから Fess を起動
- ボリュームの永続化: データの永続化
- 再起動ポリシー: 障害時の自動復旧
- JVM ヒープの明示的な設定

管理 API を使った設定の自動化
===============================

Fess の管理 API を使うことで、GUI を介さずにプログラムから設定を操作できます。

設定のエクスポート
------------------

現在の Fess 設定をエクスポートして、コードとして保存します。

管理画面の ［システム］ > ［バックアップ/リストア］ からエクスポートできます。
また、管理 API を使ってスクリプトからエクスポートすることも可能です。

設定のインポート
----------------

保存した設定ファイルを使って、新しい Fess 環境に設定を適用します。
これにより、環境の再構築や複製が容易になります。

fessctl CLI の活用
===================

fessctl は Fess のコマンドラインツールです。
管理画面で行う操作の多くを、コマンドラインから実行できます。

主な操作
--------

- クロール設定の作成・更新・削除
- スケジューラジョブの実行
- 辞書データの管理
- バックアップとリストア

CLI を使うことで、設定変更をスクリプト化し、CI/CD パイプラインに組み込むことができます。

CI/CD パイプラインの構築
==========================

設定変更のワークフロー
-----------------------

検索システムの設定変更を、以下のワークフローで管理します。

1. **変更**: 設定ファイルを修正し、Git ブランチで管理
2. **レビュー**: プルリクエストで変更内容をレビュー
3. **テスト**: ステージング環境で動作確認
4. **デプロイ**: 本番環境に設定を適用

GitHub Actions での自動化例
----------------------------

設定ファイルの変更がマージされたら、自動的に本番環境に反映する例です。

.. code-block:: yaml

    name: Deploy Fess Config
    on:
      push:
        branches: [main]
        paths:
          - 'fess-config/**'
          - 'dictionary/**'

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - name: Apply dictionary updates
            run: |
              # 辞書ファイルを Fess サーバーに転送
              scp dictionary/* fess-server:/opt/fess/dictionary/

          - name: Reload Fess configuration
            run: |
              # 管理 API で設定をリロード
              curl -X POST https://fess.example.com/api/admin/reload \
                -H "Authorization: Bearer ${{ secrets.FESS_ADMIN_TOKEN }}"

バックアップの自動化
=====================

定期的なバックアップも自動化しましょう。

バックアップスクリプト
----------------------

cron や CI/CD のスケジュール機能を使って、定期的にバックアップを取得します。

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    BACKUP_DIR="/backup/fess/$(date +%Y%m%d)"
    mkdir -p "${BACKUP_DIR}"

    # Fess 設定のバックアップ
    curl -s -o "${BACKUP_DIR}/fess-config.json" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup"

    # 古いバックアップの削除（30日以上前）
    find /backup/fess -type d -mtime +30 -exec rm -rf {} +

    echo "Backup completed: ${BACKUP_DIR}"

環境の再構築手順
=================

災害復旧やテスト環境の構築のために、環境を完全に再構築する手順を文書化しておきます。

1. Docker Compose でコンテナを起動
2. OpenSearch のヘルスチェックが green/yellow になるまで待機
3. Fess の設定をインポート（管理 API またはリストア機能）
4. 辞書ファイルを配置
5. クロールジョブを実行
6. 動作確認（検索テスト）

この手順をスクリプト化しておけば、環境の再構築を迅速に行えます。

まとめ
======

本記事では、Fess の検索インフラを DevOps の手法で管理するアプローチを紹介しました。

- Docker Compose による環境定義のコード化
- 管理 API と fessctl による設定の自動化
- CI/CD パイプラインによる設定変更のデプロイ自動化
- バックアップの自動化と環境再構築手順

「手順書を読んで手作業で設定」から「コードを実行して自動デプロイ」へ、検索インフラの運用を進化させましょう。

次回は、プラグイン開発による Fess の拡張について扱います。

参考資料
========

- `Fess 管理 API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__
