================================
サイト検索
================================

|Fess| は、検索APIを利用した検索ボックスをサイトに追加するスクリプトを提供しています。

設定
==================

以下のコードをHTML中の検索ボックスを表示したい位置に設置します。

::

    <script>
      (function() {
        var fess = document.createElement('script');
        fess.type = 'text/javascript';
        fess.async = true;
        fess.src = '//<Server Name>/js/ss/fess-ss.min.js';
        fess.charset = 'utf-8';
        fess.setAttribute('id', 'fess-ss');
        fess.setAttribute('fess-url', '//<Server Name>/json');
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(fess, s);
      })();
    </script>
    <fess:search></fess:search>

.. csv-table:: 表 利用可能なタグ
    :widths: 30, 60

    "<fess:search>", "検索フォームと検索結果を表示します。"
    "<fess:search-form-only>", "検索フォームを表示します。この検索フォームはsubmitすると、<script>中で``fess.setAttribute('fess-search-page-path', 'result.html');``で設定したページへ遷移します。"
    "<fess:search-result-only>", "検索結果を表示します。"


イメージ
==================

|image0|


.. |image0| image:: ../../../resources/images/ja/11.2/admin/fess-ss-1.png
