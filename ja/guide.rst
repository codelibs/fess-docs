==========
実践ガイド
==========

Fess で実現するナレッジ活用
===========================

社内の情報を Fess で検索できるようにし、使われ続ける検索基盤に育てるための実践ガイドです。
各記事は Fess 15.9 を対象に、設定画面の項目や設定キー、うまくいったことの確かめ方まで具体的に説明します。
15.10 以降でのみ使える機能は、その旨を記事中に明記しています。

目的から選ぶ
============

- **まず試してみたい**: :doc:`articles/guide-01` → :doc:`articles/guide-02`
- **ファイルサーバーを検索したい**: :doc:`articles/file-server-search` → :doc:`articles/guide-04` → :doc:`articles/guide-05`
- **クラウドや SaaS のデータを検索したい**: :doc:`articles/datastore-basics` → :doc:`articles/guide-07` / :doc:`articles/guide-06` / :doc:`articles/guide-12`
- **既存のサイトやシステムに検索を組み込みたい**: :doc:`articles/guide-03` → :doc:`articles/guide-11`
- **部署や利用者ごとに見せる情報を分けたい**: :doc:`articles/guide-05` → :doc:`articles/guide-15` → :doc:`articles/guide-13`
- **AI で検索を強化したい**: :doc:`articles/guide-18` → :doc:`articles/guide-19` → :doc:`articles/guide-20`
- **本番運用を始める**: :doc:`articles/guide-10` → :doc:`articles/guide-16` → :doc:`articles/guide-14`

はじめる
========

- :doc:`articles/guide-01` - Fess の構成、本体とプラグインの役割分担、目的別の読み進め方
- :doc:`articles/guide-02` - Docker Compose で Fess を起動し、クロールから検索までを一通り試す

情報を集める
============

- :doc:`articles/guide-04` - Web サイトとファイルサーバーをクロールし、ラベルで絞り込めるようにする
- :doc:`articles/datastore-basics` - データストアプラグインの設定項目、権限、ラベル、スケジュール、結果の確かめ方
- :doc:`articles/guide-07` - Google Drive、SharePoint Online / OneDrive、Box のファイルを検索対象にする
- :doc:`articles/guide-06` - Git リポジトリ、Confluence、Jira、Slack の情報を検索対象にする
- :doc:`articles/guide-12` - データベース、CSV ファイル、Salesforce のデータを検索対象にする

検索を組み込む・見せ方を変える
==============================

- :doc:`articles/guide-03` - 既存サイトに検索窓を置き、テーマで検索画面の見た目を整える
- :doc:`articles/guide-11` - 検索 API とアクセストークンを使って業務システムから検索・登録する

アクセスを制御する
==================

- :doc:`articles/guide-05` - ロール・グループで検索結果を出し分け、LDAP / Active Directory と連携する
- :doc:`articles/guide-15` - SSO（OIDC / SAML / Entra ID / SPNEGO）を導入し、外部からのアクセスを保護する
- :doc:`articles/guide-13` - 仮想ホストとロールで、1 つの Fess を複数の組織で使い分ける

検索品質を高める
================

- :doc:`articles/guide-08` - 検索ログの分析画面から課題を見つけ、同義語やキーマッチで改善する
- :doc:`articles/guide-09` - 多言語の文書がどう索引・検索されるかを理解し、言語ごとに調整する
- :doc:`articles/guide-22` - OpenSearch Dashboards で検索ログを独自に集計・可視化する

運用する
========

- :doc:`articles/guide-10` - ヘルスチェック、ログ、通知、バックアップと復元、障害URL の扱い
- :doc:`articles/guide-16` - fessctl と管理 API で設定をコードとして管理し、環境を再現する
- :doc:`articles/guide-14` - メモリ設定、外部 OpenSearch クラスター、Fess の複数台構成
- :doc:`articles/guide-17` - データストアプラグインやインジェスターを自作して機能を追加する

AI で検索を強化する
===================

- :doc:`articles/guide-18` - ベクトル検索とランク融合で、言い回しが違っても見つかる検索にする
- :doc:`articles/guide-19` - LLM を接続し、社内文書を根拠に回答する AI 検索モードを使う
- :doc:`articles/guide-20` - MCP サーバープラグインで、AI エージェントから Fess を検索させる
- :doc:`articles/guide-21` - 画像とテキストをまとめて検索できるマルチモーダル検索を構築する

全社展開を計画する
==================

- :doc:`articles/guide-23` - 導入から全社展開までの段階ごとに、設定・確認すべき項目を整理する

ユースケース・比較
==================

- :doc:`articles/use-cases` - 業種別・規模別の活用事例と、それぞれに役立つ記事
- :doc:`articles/comparison` - Fess と他の検索ソリューション（OpenSearch 単体、Solr、商用製品など）の比較
- :doc:`articles/file-server-search` - ファイルサーバーの全文検索を導入する前に確認すべき点
- :doc:`articles/legacy-search-migration` - Namazu・Hyper Estraier などの全文検索から Fess へ移行する手順

.. toctree::
   :hidden:

   articles/guide-01
   articles/guide-02
   articles/guide-04
   articles/datastore-basics
   articles/guide-07
   articles/guide-06
   articles/guide-12
   articles/guide-03
   articles/guide-11
   articles/guide-05
   articles/guide-15
   articles/guide-13
   articles/guide-08
   articles/guide-09
   articles/guide-22
   articles/guide-10
   articles/guide-16
   articles/guide-14
   articles/guide-17
   articles/guide-18
   articles/guide-19
   articles/guide-20
   articles/guide-21
   articles/guide-23
   articles/use-cases
   articles/comparison
   articles/file-server-search
   articles/legacy-search-migration
