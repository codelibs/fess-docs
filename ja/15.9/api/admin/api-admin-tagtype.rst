===========
TagType API
===========

概要
====

TagType APIは、|Fess| のユーザーのタグ（ログインしたユーザーがドキュメントに付けるユーザーごとのタグ）を管理するためのAPIです（ :doc:`../../admin/tagtype-guide` を参照）。 ``user.tag.enabled`` の値に関係なく、すべてのユーザーのタグを管理できます。

認証方法やレスポンスの共通仕様（``status`` コード、``version`` フィールド、エラー形式、
HTTPステータスコードなど）については :doc:`api-admin-overview` を参照してください。
本APIにアクセスするには、管理API権限（``admin-api``）を持つアクセストークンを
``Authorization: Bearer <アクセストークン>`` ヘッダーで指定する必要があります。

本APIの JSON のフィールド名はスネークケース（ ``sort_order`` 、 ``virtual_host`` 、 ``seq_no`` 、 ``primary_term`` など）です。

ベースURL
=========

::

    /api/admin/tagtype

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET
     - /settings
     - タグ一覧取得
   * - GET
     - /setting/{id}
     - タグ取得
   * - POST
     - /setting
     - タグ作成
   * - PUT
     - /setting
     - タグ更新
   * - DELETE
     - /setting/{id}
     - タグ削除

タグ一覧取得
============

リクエスト
----------

::

    GET /api/admin/tagtype/settings

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``size``
     - Integer
     - いいえ
     - 1ページあたりの件数。デフォルトは ``paging.page.size`` の設定値（既定 ``25`` ）です。
   * - ``page``
     - Integer
     - いいえ
     - ページ番号（1から開始）。デフォルトは ``1`` です。
   * - ``name``
     - String
     - いいえ
     - タグ名で絞り込み（ワイルドカード検索。入力した文字列を含む名前に一致）。
   * - ``owner``
     - String
     - いいえ
     - 所有者で絞り込み（ワイルドカード検索。入力した文字列を含む所有者に一致）。

タグは表示順序、名前、所有者の順に並びます。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.9.0",
        "status": 0,
        "settings": [
          {
            "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
            "seq_no": 12,
            "primary_term": 1,
            "name": "to-review",
            "owner": "alice",
            "permissions": "{user}alice",
            "virtual_host": "",
            "sort_order": 0
          }
        ],
        "total": 5
      }
    }

.. note::

   一覧では、長くなりうるタグのパスを取得しないため、各要素には ``paths`` がありません。PUT はタグ全体を置き換えるため、タグを編集するときは、 ``paths`` を残せるよう先に ``GET /setting/{id}`` で取得してください。

タグ取得
========

リクエスト
----------

::

    GET /api/admin/tagtype/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
          "seq_no": 12,
          "primary_term": 1,
          "name": "to-review",
          "owner": "alice",
          "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
          "permissions": "{user}alice",
          "virtual_host": "",
          "sort_order": 0
        }
      }
    }

``seq_no`` と ``primary_term`` は、読み取ったタグのバージョンを表します。 ``paths`` と ``permissions`` は 1 行に 1 つの値を持ちます。

タグ作成
========

リクエスト
----------

::

    POST /api/admin/tagtype/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "specs",
      "owner": "bob",
      "paths": "https://www.example.com/spec.pdf",
      "permissions": "{user}bob\n{role}guest",
      "sort_order": 0
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - フィールド
     - 型
     - 必須
     - 説明
   * - ``name``
     - String
     - はい
     - タグ名。NFKC で正規化され、連続する空白は 1 つにまとめられ、前後の空白は取り除かれます。正規化後の長さは 1 〜 ``user.tag.name.max.length`` （デフォルト: ``50`` ）文字で、制御文字や書式文字は使えません。
   * - ``owner``
     - String
     - はい
     - タグを所有するユーザーのログインユーザー ID（最大1000文字）。
   * - ``paths``
     - String
     - いいえ
     - タグを付けるドキュメントの URL。複数指定する場合は改行（ ``\n`` ）で区切ります。それぞれドキュメントの ``url`` フィールドと完全に一致する必要があります。最大 ``user.tag.max.paths`` （デフォルト: ``10000`` ）個。
   * - ``permissions``
     - String
     - いいえ
     - タグを見られるユーザー・グループ・ロール（例: ``{role}guest`` ）。複数指定する場合は改行（ ``\n`` ）で区切ります。空の場合は所有者だけが見られます。 ``{role}guest`` （ ``role.search.guest.permissions`` の値）を含めると、ログインしたすべてのユーザーと共有されます。
   * - ``virtual_host``
     - String
     - いいえ
     - 仮想ホスト（最大1000文字）。
   * - ``sort_order``
     - Integer
     - いいえ
     - 表示順序（0以上の整数）。省略時は ``0`` です。

タグの ID は、名前と所有者から作られるタグの値の SHA-256 で、サーバーが決めます。所有者と名前の組み合わせでタグが識別されるため、所有者が同じ名前のタグをすでに持っている場合は、バリデーションエラー（ ``status: 1`` 、「同じ名前と所有者のタグがすでに存在します。」）になります。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
        "created": true
      }
    }

作成に成功すると ``created`` は ``true`` になります。

タグ更新
========

リクエスト
----------

::

    PUT /api/admin/tagtype/setting
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
      "seq_no": 12,
      "primary_term": 1,
      "name": "reviewed",
      "owner": "alice",
      "paths": "https://www.example.com/a.html",
      "permissions": "{user}alice",
      "virtual_host": "",
      "sort_order": 0
    }

作成時のすべてのフィールドに加えて、以下のフィールドが必要です。タグは全体が置き換わるため、残したい ``paths`` も送ってください。

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - フィールド
     - 型
     - 必須
     - 説明
   * - ``id``
     - String
     - はい
     - 更新するタグの ID。
   * - ``seq_no``
     - Integer
     - はい
     - ``GET /setting/{id}`` が返したタグの ``seq_no`` 。
   * - ``primary_term``
     - Integer
     - はい
     - ``GET /setting/{id}`` が返したタグの ``primary_term`` 。

- 読み取った後にタグが変更され、 ``seq_no`` と ``primary_term`` が一致しなくなっている場合は、バリデーションエラー（ ``status: 1`` 、「タグが他のユーザーによって変更されました。再読み込みしてからやり直してください。」）になります。タグを取得し直してから再実行してください。
- ``name`` または ``owner`` を変更するとタグの ID が変わり、レスポンスの ``id`` は新しい ID になります。所有者が変更後の名前のタグをすでに持っている場合は、「同じ名前と所有者のタグがすでに存在します。」になります。
- 所有者を変更すると、 ``permissions`` に含まれる元の所有者のユーザーのパーミッションは、新しい所有者のものに置き換わります。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "c1fd8e024cbadfc79468e66fa52350e46cc31837aabf75b7ee6d929edaa20396",
        "created": false
      }
    }

更新時は ``created`` が ``false`` になります。

タグ削除
========

リクエスト
----------

::

    DELETE /api/admin/tagtype/setting/{id}

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

削除の途中でタグが変更された場合は、「タグが他のユーザーによって変更されました。再読み込みしてからやり直してください。」になります。

ドキュメントへの反映
====================

本APIによるタグの作成・更新・削除は、すぐにタグの情報に保存されます。 ``user.tag.enabled`` が ``true`` の間は、ドキュメントへの変更（追加・削除したパス、名前の変更、削除）がキューに入り、1 分ごとの「Log Aggregator」（ ``log_aggregator`` ）ジョブで反映されます。 ``false`` の間はキューに入らないため、タグ機能を有効にした後に「Tag Updater」（ ``tag_updater`` ）ジョブを実行してください。 :doc:`../../admin/tagtype-guide` を参照してください。

使用例
======

ログインしたすべてのユーザーとタグを共有
----------------------------------------

.. code-block:: bash

    # paths、seq_no、primary_term を含めてタグを取得
    curl "http://localhost:8080/api/admin/tagtype/setting/0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # パーミッションに {role}guest を加えて送り返す
    curl -X PUT "http://localhost:8080/api/admin/tagtype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
           "seq_no": 12,
           "primary_term": 1,
           "name": "to-review",
           "owner": "alice",
           "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
           "permissions": "{user}alice\n{role}guest",
           "sort_order": 0
         }'

ユーザーのタグ一覧取得
----------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/tagtype/settings?owner=alice&size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`api-admin-overview` - 管理API概要
- :doc:`../api-tag` - タグAPI
- :doc:`../../admin/tagtype-guide` - タグ管理ガイド
