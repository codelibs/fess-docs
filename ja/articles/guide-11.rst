============================================================
第11回 検索APIで既存システムを拡張 -- CRM・社内システムとの連携パターン集
============================================================

はじめに
========

Fess は独立した検索システムとして利用するだけでなく、既存の業務システムに検索機能を提供する「検索マイクロサービス」としても活用できます。

本記事では、Fess の API を使って既存システムと連携する具体的なパターンを紹介します。
CRM への顧客情報検索の組み込み、FAQ 検索ウィジェット、ドキュメントポータルの構築など、実践的な連携シナリオを扱います。

対象読者
========

- 既存の業務システムに検索機能を追加したい方
- Fess の API を使ったシステム連携に興味がある方
- Web アプリケーション開発の基本知識がある方

Fess API の全体像
==================

Fess が提供する主要な API を整理します。

.. list-table:: Fess API 一覧
   :header-rows: 1
   :widths: 25 45 30

   * - API
     - 用途
     - エンドポイント
   * - 検索 API
     - ドキュメントの全文検索
     - ``/api/v1/documents``
   * - ラベル API
     - 利用可能なラベルの取得
     - ``/api/v1/labels``
   * - サジェスト API
     - 入力補完候補の取得
     - ``/api/v1/suggest-words``
   * - 人気ワード API
     - 人気の検索キーワードを取得
     - ``/api/v1/popular-words``
   * - ヘルス API
     - システムの稼働状態を確認
     - ``/api/v1/health``
   * - 管理 API
     - 設定の操作（CRUD）
     - ``/api/admin/*``

アクセストークン
----------------

API を利用する際は、アクセストークンによる認証が推奨されます。

1. 管理画面の ［システム］ > ［アクセストークン］ でアクセストークンを作成
2. API リクエストのヘッダーにトークンを含める

::

    Authorization: Bearer {アクセストークン}

トークンにはロールを割り当てることができ、API 経由の検索にもロールベースの検索結果制御が適用されます。

パターン1: CRM への検索組み込み
=================================

シナリオ
--------

営業チームが使う CRM システムに、顧客関連ドキュメントの検索機能を追加します。
CRM の顧客画面から、その顧客に関連する提案書、議事録、契約書などを横断検索できるようにします。

実装アプローチ
--------------

CRM の顧客画面に検索ウィジェットを埋め込みます。
顧客名を検索クエリとして Fess API に送信し、結果を CRM 画面内に表示します。

.. code-block:: javascript

    // CRM 画面内の検索ウィジェット
    async function searchCustomerDocs(customerName) {
      const params = new URLSearchParams({
        q: customerName,
        num: '5',
        'fields.label': 'sales-docs'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

ポイント
--------

- ``fields.label`` で営業関連ドキュメントに絞り込み
- ``num`` で表示件数を制限（CRM 画面内のスペースに合わせる）
- 顧客名だけでなく、案件名やプロジェクト番号でも検索できると便利

パターン2: FAQ 検索ウィジェット
=================================

シナリオ
--------

社内の問い合わせ対応システムに、FAQ 検索ウィジェットを追加します。
社員が問い合わせを起票する前に、関連する FAQ を検索して自己解決を促します。

実装アプローチ
--------------

サジェスト API と検索 API を組み合わせて、入力中にリアルタイムで候補を表示します。

.. code-block:: javascript

    // 入力中のサジェスト
    async function getSuggestions(query) {
      const params = new URLSearchParams({ q: query, num: '5' });
      const url = `https://fess.example.com/api/v1/suggest-words?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

サジェスト API は、利用者がキーワードを入力中に候補を表示するために使用します。
利用者がキーワードを確定して検索実行すると、検索 API で詳細な検索結果を取得します。

ポイント
--------

- サジェスト API はリアルタイム性が重要なため、レスポンス速度を確認
- FAQ カテゴリをラベルで管理し、カテゴリ別の絞り込みも提供
- 人気ワード API で「よく検索されるキーワード」を表示し、利用者の検索を支援

パターン3: ドキュメントポータル
=================================

シナリオ
--------

社内のドキュメント管理ポータルを構築します。
カテゴリ別のブラウジングと、全文検索を組み合わせたインタフェースを提供します。

実装アプローチ
--------------

ラベル API でカテゴリ一覧を取得し、検索 API でカテゴリ内のドキュメントを取得します。

.. code-block:: javascript

    // ラベル一覧の取得
    async function getLabels() {
      const url = 'https://fess.example.com/api/v1/labels';
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

    // ラベルでフィルタした検索
    async function searchByLabel(query, label) {
      const params = new URLSearchParams({
        q: query || '*',
        'fields.label': label,
        num: '20',
        sort: 'last_modified.desc'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

ポイント
--------

- ラベル API でカテゴリ一覧を動的に取得（ラベルの追加・削除が API 側に即反映）
- ``sort=last_modified.desc`` で最新のドキュメントを上位に表示
- ``q=*`` でキーワードなしのブラウジング（全件取得）も可能

パターン4: コンテンツインデクシング API
=========================================

シナリオ
--------

外部システムが生成するデータ（ログ、レポート、チャットボットの応答記録など）を Fess のインデックスに登録し、検索対象にしたい。

実装アプローチ
--------------

Fess の管理 API を使って、外部からドキュメントをインデックスに登録できます。

管理 API のドキュメントエンドポイントを使用して、タイトル、URL、本文などの情報を POST リクエストで送信します。

ポイント
--------

- クロールでは取得できないデータソースの統合に有効
- バッチ処理で複数ドキュメントを一括登録することも可能
- アクセストークンの権限を適切に設定し、書き込み権限を限定する

API 連携のベストプラクティス
=============================

エラーハンドリング
------------------

API 連携では、ネットワーク障害や Fess サーバーのメンテナンスに備えたエラーハンドリングが重要です。

- タイムアウトの設定: 検索 API の呼び出しに適切なタイムアウトを設定
- リトライロジック: 一時的なエラーに対するリトライ（最大3回程度）
- フォールバック: Fess が応答しない場合の代替表示（「検索サービスは現在利用できません」等）

パフォーマンスの考慮
--------------------

- レスポンスキャッシュ: 同じクエリの結果を短時間キャッシュ
- 検索結果件数の制限: 必要な件数のみ取得（``num`` パラメータ）
- フィールド指定: 必要なフィールドのみ取得してレスポンスサイズを削減

セキュリティ
------------

- HTTPS 通信の使用
- アクセストークンのローテーション
- トークンの権限を最小限に設定（読み取り専用など）
- CORS の適切な設定

まとめ
======

本記事では、Fess の API を使った既存システムとの連携パターンを紹介しました。

- **CRM 連携**: 顧客画面からの関連ドキュメント検索
- **FAQ ウィジェット**: サジェスト + 検索のリアルタイム候補表示
- **ドキュメントポータル**: ラベル API によるカテゴリブラウジング
- **コンテンツインデクシング**: 外部データの API 経由での登録

Fess の API は REST ベースでシンプルなため、様々なシステムとの連携が容易です。
既存のシステムに検索機能を「後付け」で追加できることが、Fess の大きな強みの一つです。

次回は、SaaS やデータベースのデータを検索可能にするシナリオを扱います。

参考資料
========

- `Fess 検索 API <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__

- `Fess 管理 API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__
