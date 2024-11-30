================================
Site Search
================================

|Fess| supports adding a search box to your website.

Settings
==================

Set the following code where you would like to place the search box of the website.

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


Screen Image
==================

|image0|

.. |image0| image:: ../../../resources/images/en/15.0/user/fess-ss-1.png
