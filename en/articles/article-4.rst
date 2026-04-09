==============================================================
Building an Elasticsearch-Based Search Server with Fess -- FSS
==============================================================

Introduction
============

This article explains how to integrate a search service into a website using a Fess server you have built.
By using the tags and JavaScript file provided by Fess Site Search (FSS), you can display a search box and search results on an existing website.


Target Audience
===============

- Those who want to add search functionality to an existing website

- Those who want to migrate from Google Site Search or Google Custom Search


What is Fess Site Search (FSS)?
================================

FSS is a feature for integrating the Fess search server into an existing website. It is provided by the CodeLibs project on the FSS site. Similar to site search services such as Google Site Search (GSS), you can use it simply by embedding a JavaScript tag on the page where you want to use the search service, making migration from GSS easy.

What is FSS JS?
================

FSS JS is a JavaScript file that displays search results from Fess. By placing this JavaScript file on your website, you can display search results.
FSS JS can be generated and obtained using the FSS JS Generator at "https://fss-generator.codelibs.org/".
FSS JS supports Fess version 11.3 and above, so please install Fess 11.3 or later when building your Fess server. For instructions on how to build Fess, please refer to the \ `Installation Guide <https://fess.codelibs.org/ja/articles/article-1.html>`__\ .


The FSS JS Generator allows you to specify the color scheme and font of the search form.
By clicking the "Generate" button, you can generate a JavaScript file with the specified settings.

|image0|

If the preview looks fine, click the "Download JS" button to download the JavaScript file.

|image1|

Integrating into Your Site
============================

In this example, we will consider adding site search to "`www.n2sm.net`", a site built with static HTML.

Search results will be displayed on search.html within the site, and the Fess server will be set up separately on "nss833024.n2search.net".

The downloaded FSS JS JavaScript file will be placed on the site as /js/fess-ss.min.js.

The information above is summarized as follows.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Item
     - URL
   * - Target Site
     - https://www.n2sm.net/
   * - Search Results Page
     - https://www.n2sm.net/search.html
   * - FSS JS
     - https://www.n2sm.net/js/fess-ss.min.js
   * - Fess Server
     - https://nss833024.n2search.net/

To embed the JavaScript tag, place the following tag at the location within search.html where you want to display the search results.

..
  <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      // Set the URL of FSS JS to src
      fess.src = 'https://www.n2sm.net/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      // Set the URL of the Fess search API to fess-url
      fess.setAttribute('fess-url', 'https://nss833024.n2search.net/json');
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(fess, s);
    })();
  </script>
  <fess:search></fess:search>

When you access search.html, the search form will be displayed.

Entering a search term will display the search results as shown below.

|image2|

To place a search form on other pages and display the search results, add a search form like the one below to each page, configured to redirect to "`https://www.n2sm.net/search.html?q=search+term`".

..
  <form action="https://www.n2sm.net/search.html" method="get">
    <input type="text" name="q">
    <input type="submit" value="Search">
  </form>


Summary
=======

We have shown how to embed Fess search results into a site simply by placing a JavaScript tag.
With FSS, migrating from GSS can also be achieved by simply replacing the existing JavaScript tag.
FSS JS also offers other display options and ways to integrate search logs with Google Analytics. For other configuration methods, please refer to the `FSS [Manual] <https://fss-generator.codelibs.org/ja/docs/manual>`__.

References
==========
- `Fess Site Search <https://fss-generator.codelibs.org/ja/>`__

.. |image0| image:: ../../resources/images/ja/article/5/FSS-JS-Generator1.png
.. |image1| image:: ../../resources/images/ja/article/5/FSS-JS-Generator2.png
.. |image2| image:: ../../resources/images/ja/article/5/N2Search-review.png
