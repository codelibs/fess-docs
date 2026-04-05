==================================
Gitコネクタ
==================================

概要
====

Gitコネクタは、Gitリポジトリのファイルを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-git`` プラグインが必要です。

対応リポジトリ
==============

- GitHub（パブリック/プライベート）
- GitLab（パブリック/プライベート）
- Bitbucket（パブリック/プライベート）
- ローカルGitリポジトリ
- その他のGitホスティングサービス

前提条件
========

1. プラグインのインストールが必要です
2. プライベートリポジトリの場合は認証情報が必要です
3. リポジトリへの読み取りアクセス権が必要です

プラグインのインストール
------------------------

管理画面の「システム」→「プラグイン」からインストールします。

または、詳細は :doc:`../../admin/plugin-guide` を参照してください。

設定方法
========

管理画面から「クローラー」→「データストア」→「新規作成」で設定します。

基本設定
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 設定例
   * - 名前
     - Project Git Repository
   * - ハンドラ名
     - GitDataStore
   * - 有効
     - オン

パラメーター設定
----------------

パブリックリポジトリの例:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    prev_commit_id=

プライベートリポジトリの例（認証あり）:

::

    uri=https://username:personal_access_token@github.com/company/private-repo.git
    base_url=https://github.com/company/private-repo/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    prev_commit_id=

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``uri``
     - はい
     - GitリポジトリのURI（clone用）
   * - ``base_url``
     - いいえ
     - ファイル表示用のベースURL。設定しない場合、URLが空になり、削除ファイルの自動削除も無効になります
   * - ``username``
     - いいえ
     - Git認証のユーザー名。 ``password`` と組み合わせて使用します（URIに認証情報を含める代替手段）
   * - ``password``
     - いいえ
     - Git認証のパスワードまたはトークン。 ``username`` と組み合わせて使用します
   * - ``extractors``
     - いいえ
     - MIMEタイプ別の抽出器設定
   * - ``default_extractor``
     - いいえ
     - extractorsのパターンに一致しない場合のフォールバック抽出器（デフォルト: ``tikaExtractor``）
   * - ``prev_commit_id``
     - いいえ
     - 前回のコミットID（差分クロール用）。クロール成功後に自動更新されます
   * - ``commit_id``
     - いいえ
     - 対象コミットID（デフォルト: HEAD）。ブランチやタグを指定可能
   * - ``ref_specs``
     - いいえ
     - Gitのrefスペック（デフォルト: ``+refs/heads/*:refs/heads/*``）
   * - ``repository_path``
     - いいえ
     - ローカルリポジトリのパス。未設定の場合、一時ディレクトリが作成され、クロール後に削除されます
   * - ``include_pattern``
     - いいえ
     - ファイルパスのインクルードフィルター（正規表現）
   * - ``exclude_pattern``
     - いいえ
     - ファイルパスの除外フィルター（正規表現）
   * - ``max_size``
     - いいえ
     - インデックス対象の最大ファイルサイズ（バイト単位、デフォルト: ``10000000``）
   * - ``cache_threshold``
     - いいえ
     - メモリとディスクバッファリングの切り替え閾値（バイト単位、デフォルト: ``1000000``）

スクリプト設定
--------------

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    cache=""
    digest=author.toExternalString()
    anchor=
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``url``
     - ファイルのURL
   * - ``path``
     - リポジトリ内のファイルパス
   * - ``name``
     - ファイル名
   * - ``content``
     - ファイルのテキストコンテンツ
   * - ``contentLength``
     - コンテンツの長さ
   * - ``timestamp``
     - 最終更新日時
   * - ``mimetype``
     - ファイルのMIMEタイプ
   * - ``author``
     - 最終コミット者の情報（PersonIdent）
   * - ``committer``
     - コミッター情報（PersonIdent）。authorとは異なる場合があります
   * - ``uri``
     - GitリポジトリのURI

Gitリポジトリの認証
===================

GitHub Personal Access Token
-----------------------------

1. GitHubでPersonal Access Tokenを生成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

https://github.com/settings/tokens にアクセス:

1. 「Generate new token」→「Generate new token (classic)」をクリック
2. トークン名を入力（例: Fess Crawler）
3. スコープで「repo」にチェック
4. 「Generate token」をクリック
5. 生成されたトークンをコピー

2. URIに認証情報を含める
~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:YOUR_GITHUB_TOKEN@github.com/company/repo.git

GitLab Private Token
--------------------

1. GitLabでAccess Tokenを生成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GitLabのUser Settings → Access Tokens:

1. トークン名を入力
2. スコープで「read_repository」にチェック
3. 「Create personal access token」をクリック
4. 生成されたトークンをコピー

2. URIに認証情報を含める
~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:YOUR_GITLAB_TOKEN@gitlab.com/company/repo.git

SSH認証
-------

SSH鍵を使用する場合:

::

    uri=git@github.com:company/repo.git

.. note::
   SSH認証を使用する場合、|Fess| を実行しているユーザーのSSH鍵を設定する必要があります。

抽出器の設定
============

MIMEタイプ別の抽出器
--------------------

``extractors`` パラメーターでファイルタイプ別の抽出器を指定:

::

    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,application/json:textExtractor,

形式: ``<MIMEタイプ正規表現>:<抽出器名>,``

デフォルトの抽出器
~~~~~~~~~~~~~~~~~~

- ``textExtractor`` - テキストファイル用
- ``tikaExtractor`` - バイナリファイル用（PDF、Word等）

テキストファイルのみクロール
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    extractors=text/.*:textExtractor,

すべてのファイルをクロール
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    extractors=.*:tikaExtractor,

特定のファイルタイプのみ
~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Markdown、YAML、JSONのみ
    extractors=text/markdown:textExtractor,text/yaml:textExtractor,application/json:textExtractor,

差分クロール
============

前回のコミットからの変更のみクロール
------------------------------------

初回クロール後、``prev_commit_id`` に前回のコミットIDを設定:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    prev_commit_id=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0

.. note::
   ``prev_commit_id`` はクロール成功後に自動的に最新のコミットIDに更新されます。
   初回は空のまま設定すれば、全ファイルがクロールされ、以降は差分のみがクロールされます。

削除されたファイルの処理
------------------------

``base_url`` が設定されている場合、GitのDiffEntryで検出された削除ファイル（``ChangeType.DELETE``）は
自動的にインデックスから削除されます。

使用例
======

GitHubパブリックリポジトリ
--------------------------

パラメーター:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,

スクリプト:

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    last_modified=timestamp
    mimetype=mimetype

GitHubプライベートリポジトリ
----------------------------

パラメーター:

::

    uri=https://username:YOUR_GITHUB_TOKEN@github.com/company/repo.git
    base_url=https://github.com/company/repo/blob/main/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,

スクリプト:

::

    url=url
    title=name
    content=content
    digest=author.toExternalString()
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

GitLab（セルフホスト）
----------------------

パラメーター:

::

    uri=https://username:glpat-abc123@gitlab.company.com/team/project.git
    base_url=https://gitlab.company.com/team/project/-/blob/main/
    extractors=text/.*:textExtractor,
    prev_commit_id=

スクリプト:

::

    url=url
    host="gitlab.company.com"
    site="gitlab.company.com/team/project/" + path
    title=name
    content=content
    last_modified=timestamp

ドキュメントのみクロール（Markdownファイル）
--------------------------------------------

パラメーター:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/markdown:textExtractor,text/plain:textExtractor,

スクリプト:

::

    if (mimetype.startsWith("text/")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
    }

特定のディレクトリのみクロール
------------------------------

スクリプトでフィルタリング:

::

    if (path.startsWith("docs/") || path.startsWith("README")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
        mimetype=mimetype
    }

トラブルシューティング
======================

認証エラー
----------

**症状**: ``Authentication failed`` または ``Not authorized``

**確認事項**:

1. Personal Access Tokenが正しいか確認
2. トークンに適切な権限があるか確認（``repo`` スコープ）
3. URIのフォーマットが正しいか確認:

   ::

       # 正しい
       uri=https://username:token@github.com/company/repo.git

       # 間違い
       uri=https://github.com/company/repo.git?token=...

4. トークンの有効期限を確認

リポジトリが見つからない
------------------------

**症状**: ``Repository not found``

**確認事項**:

1. リポジトリのURLが正しいか確認
2. リポジトリが存在し、削除されていないか確認
3. 認証情報が正しいか確認
4. リポジトリへのアクセス権があるか確認

ファイルが取得できない
----------------------

**症状**: クロールは成功するがファイルが0件

**確認事項**:

1. ``extractors`` 設定が適切か確認
2. リポジトリにファイルが存在するか確認
3. スクリプト設定が正しいか確認
4. 対象ブランチにファイルが存在するか確認

MIMEタイプエラー
----------------

**症状**: 特定のファイルがクロールされない

**解決方法**:

抽出器設定を調整:

::

    # すべてのファイルを対象
    extractors=.*:tikaExtractor,

    # 特定のMIMEタイプを追加
    extractors=text/.*:textExtractor,application/json:textExtractor,application/xml:textExtractor,

大きなリポジトリ
----------------

**症状**: クロールに時間がかかる、またはメモリ不足

**解決方法**:

1. ``extractors`` で対象ファイルを限定
2. スクリプトで特定のディレクトリのみをフィルタリング
3. 差分クロールを使用（``prev_commit_id`` 設定）
4. クロール間隔を調整

ブランチの指定
--------------

デフォルトブランチ以外をクロールする場合、``commit_id`` パラメーターでブランチ名やタグを指定します:

::

    uri=https://github.com/company/repo.git
    base_url=https://github.com/company/repo/blob/develop/
    commit_id=develop

URLの生成
=========

base_urlの設定パターン
----------------------

**GitHub**:

::

    base_url=https://github.com/user/repo/blob/master/

**GitLab**:

::

    base_url=https://gitlab.com/user/repo/-/blob/main/

**Bitbucket**:

::

    base_url=https://bitbucket.org/user/repo/src/master/

``base_url`` とファイルパスが結合されてURLが生成されます。

スクリプトでのURL生成
---------------------

::

    url=url
    title=name
    content=content

または、カスタムURL:

::

    url="https://github.com/mycompany/repo/blob/main/" + path
    title=name
    content=content

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-database` - データベースコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `GitHub Personal Access Tokens <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_
- `GitLab Personal Access Tokens <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_
