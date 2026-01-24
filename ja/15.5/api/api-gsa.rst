================================
Google Search Appliance 互換 API
================================

|Fess| は、検索結果をGoogle Search Appliance(GSA)互換のXMLフォーマットで返すAPIも提供しています。
XMLのフォーマットについては、\ `GSAの公式ドキュメント <https://www.google.com/support/enterprise/static/gsa/docs/admin/74/gsa_doc_set/xml_reference/results_format.html>`__\ をご覧ください。

設定
====

system.propertiesに ``web.api.gsa=true`` を追加して、Google Search Appliance互換APIを有効にしてください。

リクエスト
========

|Fess| に
``http://localhost:8080/gsa/?q=検索語``
のようなリクエストを送ることで、検索結果を GSA互換XML形式で受け取ることができます。
リクエストパラメーターとして指定できる値は、\ `JSON 応答の検索API <api-search.html>`__\ と同じです。
