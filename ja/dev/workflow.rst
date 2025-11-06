==============
開発ワークフロー
==============

このページでは、|Fess| の開発における標準的なワークフローを説明します。
機能追加、バグ修正、テスト、コードレビューなど、
開発作業の進め方を学ぶことができます。

.. contents:: 目次
   :local:
   :depth: 2

開発の基本フロー
==============

|Fess| の開発は、以下のような流れで進めます：

.. code-block:: text

    1. Issue の確認・作成
       ↓
    2. ブランチの作成
       ↓
    3. コーディング
       ↓
    4. ローカルテストの実行
       ↓
    5. コミット
       ↓
    6. プッシュ
       ↓
    7. プルリクエストの作成
       ↓
    8. コードレビュー
       ↓
    9. レビューフィードバックへの対応
       ↓
    10. マージ

各ステップについて詳しく説明します。

Step 1: Issue の確認・作成
=========================

開発を始める前に、GitHub の Issue を確認します。

既存の Issue を確認
-----------------

1. `Fess の Issue ページ <https://github.com/codelibs/fess/issues>`__ にアクセス
2. 取り組みたい Issue を探す
3. Issue にコメントして、作業を開始する旨を伝える

.. tip::

   初めての貢献の場合は、``good first issue`` ラベルが付いた Issue から始めることをお勧めします。

新しい Issue の作成
-----------------

新しい機能やバグ修正の場合は、Issue を作成します。

1. `New Issue <https://github.com/codelibs/fess/issues/new>`__ をクリック
2. Issue のテンプレートを選択
3. 必要な情報を記入：

   - **タイトル**: 簡潔で分かりやすい説明
   - **説明**: 詳細な背景、期待される動作、現在の動作
   - **再現手順**: バグの場合
   - **環境情報**: OS、Java バージョン、Fess バージョンなど

4. ``Submit new issue`` をクリック

Issue のテンプレート
~~~~~~~~~~~~~~~~~~

**バグレポート:**

.. code-block:: markdown

    ## 問題の説明
    バグの簡潔な説明

    ## 再現手順
    1. ...
    2. ...
    3. ...

    ## 期待される動作
    本来どうあるべきか

    ## 実際の動作
    現在どうなっているか

    ## 環境
    - OS:
    - Java バージョン:
    - Fess バージョン:

**機能リクエスト:**

.. code-block:: markdown

    ## 機能の説明
    追加したい機能の説明

    ## 背景と動機
    なぜこの機能が必要か

    ## 提案する実装方法
    どのように実装するか（任意）

Step 2: ブランチの作成
====================

作業用のブランチを作成します。

ブランチ命名規則
--------------

ブランチ名は、以下の形式に従います：

.. code-block:: text

    <type>/<issue-number>-<short-description>

**type の種類:**

- ``feature``: 新機能の追加
- ``fix``: バグ修正
- ``refactor``: リファクタリング
- ``docs``: ドキュメントの更新
- ``test``: テストの追加・修正

**例:**

.. code-block:: bash

    # 新機能の追加
    git checkout -b feature/123-add-search-filter

    # バグ修正
    git checkout -b fix/456-fix-crawler-timeout

    # ドキュメント更新
    git checkout -b docs/789-update-api-docs

ブランチの作成手順
----------------

1. 最新の main ブランチを取得：

   .. code-block:: bash

       git checkout main
       git pull origin main

2. 新しいブランチを作成：

   .. code-block:: bash

       git checkout -b feature/123-add-search-filter

3. ブランチが作成されたことを確認：

   .. code-block:: bash

       git branch

Step 3: コーディング
==================

機能の実装やバグ修正を行います。

コーディング規約
--------------

|Fess| では、以下のコーディング規約に従います。

基本的なスタイル
~~~~~~~~~~~~~~

- **インデント**: スペース 4 つ
- **行の長さ**: 120 文字以内を推奨
- **エンコーディング**: UTF-8
- **改行コード**: LF（Unix スタイル）

命名規則
~~~~~~

- **クラス名**: PascalCase（例: ``SearchService``）
- **メソッド名**: camelCase（例: ``executeSearch``）
- **定数**: UPPER_SNAKE_CASE（例: ``MAX_SEARCH_SIZE``）
- **変数**: camelCase（例: ``searchResults``）

コメント
~~~~~~

- **Javadoc**: public なクラスとメソッドには必須
- **実装コメント**: 複雑なロジックには日本語または英語で説明を追加

**例:**

.. code-block:: java

    /**
     * 検索を実行します。
     *
     * @param query 検索クエリ
     * @return 検索結果
     */
    public SearchResponse executeSearch(String query) {
        // クエリの正規化
        String normalizedQuery = normalizeQuery(query);

        // 検索の実行
        return searchEngine.search(normalizedQuery);
    }

null の扱い
~~~~~~~~~

- 可能な限り ``null`` を返さない
- ``Optional`` の使用を推奨
- ``null`` チェックは明示的に行う

**例:**

.. code-block:: java

    // 良い例
    public Optional<User> findUser(String id) {
        return userRepository.findById(id);
    }

    // 避けるべき例
    public User findUser(String id) {
        return userRepository.findById(id);  // null の可能性
    }

例外処理
~~~~~~

- 例外は適切にキャッチして処理する
- ログ出力を行う
- ユーザーに分かりやすいメッセージを提供

**例:**

.. code-block:: java

    try {
        // 処理
    } catch (IOException e) {
        logger.error("ファイル読み込みエラー", e);
        throw new FessSystemException("ファイルの読み込みに失敗しました", e);
    }

ログ出力
~~~~~~

適切なログレベルを使用します：

- ``ERROR``: エラー発生時
- ``WARN``: 警告すべき状況
- ``INFO``: 重要な情報
- ``DEBUG``: デバッグ情報
- ``TRACE``: 詳細なトレース情報

**例:**

.. code-block:: java

    if (logger.isDebugEnabled()) {
        logger.debug("検索クエリ: {}", query);
    }

開発中のテスト
------------

開発中は、以下の方法でテストします：

ローカル実行
~~~~~~~~~~

IDE またはコマンドラインで Fess を実行し、動作を確認します：

.. code-block:: bash

    mvn compile exec:java

デバッグ実行
~~~~~~~~~~

IDE のデバッガーを使用して、コードの動作を追跡します。

単体テストの実行
~~~~~~~~~~~~~~

変更に関連するテストを実行します：

.. code-block:: bash

    # 特定のテストクラスを実行
    mvn test -Dtest=SearchServiceTest

    # すべてのテストを実行
    mvn test

詳細は :doc:`building` を参照してください。

Step 4: ローカルテストの実行
=========================

コミット前に、必ずテストを実行します。

単体テストの実行
--------------

.. code-block:: bash

    mvn test

統合テストの実行
--------------

.. code-block:: bash

    mvn verify

コードスタイルのチェック
--------------------

.. code-block:: bash

    mvn checkstyle:check

すべてのチェックを実行
-------------------

.. code-block:: bash

    mvn clean verify

Step 5: コミット
==============

変更をコミットします。

コミットメッセージの規約
--------------------

コミットメッセージは、以下の形式に従います：

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**type の種類:**

- ``feat``: 新機能
- ``fix``: バグ修正
- ``docs``: ドキュメントのみの変更
- ``style``: コードの意味に影響しない変更（フォーマットなど）
- ``refactor``: リファクタリング
- ``test``: テストの追加・修正
- ``chore``: ビルドプロセスやツールの変更

**例:**

.. code-block:: text

    feat: 検索フィルター機能を追加

    ユーザーが検索結果をファイルタイプでフィルタリングできるようにしました。

    Fixes #123

コミット手順
----------

1. 変更をステージング：

   .. code-block:: bash

       git add .

2. コミット：

   .. code-block:: bash

       git commit -m "feat: 検索フィルター機能を追加"

3. コミット履歴を確認：

   .. code-block:: bash

       git log --oneline

コミットの粒度
------------

- 1 つのコミットには 1 つの論理的な変更を含める
- 大きな変更は複数のコミットに分割する
- コミットメッセージは分かりやすく、具体的に

Step 6: プッシュ
==============

ブランチをリモートリポジトリにプッシュします。

.. code-block:: bash

    git push origin feature/123-add-search-filter

初回プッシュの場合：

.. code-block:: bash

    git push -u origin feature/123-add-search-filter

Step 7: プルリクエストの作成
=========================

GitHub でプルリクエスト（PR）を作成します。

PR の作成手順
-----------

1. `Fess リポジトリ <https://github.com/codelibs/fess>`__ にアクセス
2. ``Pull requests`` タブをクリック
3. ``New pull request`` をクリック
4. ベースブランチ（``main``）と比較ブランチ（作業ブランチ）を選択
5. ``Create pull request`` をクリック
6. PR の内容を記入（テンプレートに従う）
7. ``Create pull request`` をクリック

PR のテンプレート
---------------

.. code-block:: markdown

    ## 変更内容
    この PR で何を変更したか

    ## 関連 Issue
    Closes #123

    ## 変更の種類
    - [ ] 新機能
    - [ ] バグ修正
    - [ ] リファクタリング
    - [ ] ドキュメント更新
    - [ ] その他

    ## テスト方法
    この変更をどのようにテストしたか

    ## チェックリスト
    - [ ] コードは動作する
    - [ ] テストを追加した
    - [ ] ドキュメントを更新した
    - [ ] コーディング規約に従っている

PR の説明
-------

PR の説明には、以下を含めます：

- **変更の目的**: なぜこの変更が必要か
- **変更内容**: 何を変更したか
- **テスト方法**: どのようにテストしたか
- **スクリーンショット**: UI の変更の場合

Step 8: コードレビュー
====================

メンテナーがコードをレビューします。

レビューの観点
------------

レビューでは、以下の点がチェックされます：

- コードの品質
- コーディング規約への準拠
- テストの充実度
- パフォーマンスへの影響
- セキュリティの問題
- ドキュメントの更新

レビューコメントの例
------------------

**承認:**

.. code-block:: text

    LGTM (Looks Good To Me)

**修正依頼:**

.. code-block:: text

    ここは null チェックが必要ではないでしょうか？

**提案:**

.. code-block:: text

    この処理は Helper クラスに移動した方が良いかもしれません。

Step 9: レビューフィードバックへの対応
===================================

レビューコメントに対応します。

フィードバックへの対応手順
----------------------

1. レビューコメントを読む
2. 必要な修正を行う
3. 変更をコミット：

   .. code-block:: bash

       git add .
       git commit -m "fix: レビューコメントに対応"

4. プッシュ：

   .. code-block:: bash

       git push origin feature/123-add-search-filter

5. PR ページでコメントに返信

コメントへの返信
--------------

レビューコメントには必ず返信します：

.. code-block:: text

    修正しました。ご確認ください。

または：

.. code-block:: text

    ご指摘ありがとうございます。
    ○○の理由で現在の実装としていますが、いかがでしょうか？

Step 10: マージ
=============

レビューが承認されたら、メンテナーが PR をマージします。

マージ後の対応
------------

1. ローカルの main ブランチを更新：

   .. code-block:: bash

       git checkout main
       git pull origin main

2. 作業ブランチを削除：

   .. code-block:: bash

       git branch -d feature/123-add-search-filter

3. リモートブランチを削除（GitHub で自動削除されない場合）：

   .. code-block:: bash

       git push origin --delete feature/123-add-search-filter

よくある開発シナリオ
==================

機能追加
------

1. Issue を作成（または既存の Issue を確認）
2. ブランチを作成：``feature/xxx-description``
3. 機能を実装
4. テストを追加
5. ドキュメントを更新
6. PR を作成

バグ修正
------

1. バグレポートの Issue を確認
2. ブランチを作成：``fix/xxx-description``
3. バグを再現するテストを追加
4. バグを修正
5. テストが通ることを確認
6. PR を作成

リファクタリング
--------------

1. Issue を作成（リファクタリングの理由を説明）
2. ブランチを作成：``refactor/xxx-description``
3. リファクタリングを実行
4. 既存のテストが通ることを確認
5. PR を作成

ドキュメント更新
--------------

1. ブランチを作成：``docs/xxx-description``
2. ドキュメントを更新
3. PR を作成

開発のヒント
==========

効率的な開発
----------

- **小さなコミット**: 頻繁にコミットする
- **早期のフィードバック**: Draft PR を活用する
- **テストの自動化**: CI/CD を活用する
- **コードレビュー**: 他の人のコードもレビューする

問題の解決
--------

困ったときは、以下を利用します：

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__
- GitHub の Issue コメント

次のステップ
==========

ワークフローを理解したら、以下のドキュメントも参照してください：

- :doc:`building` - ビルドとテストの詳細
- :doc:`contributing` - コントリビューションガイドライン
- :doc:`architecture` - コードベースの理解

参考資料
======

- `GitHub フロー <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `コミットメッセージのガイドライン <https://chris.beams.io/posts/git-commit/>`__
- `コードレビューのベストプラクティス <https://google.github.io/eng-practices/review/>`__
