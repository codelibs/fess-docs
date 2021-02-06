===================================
Part 2: Migrate from GSS to FSS
===================================

Last time we introduced how to build and use the full text search server Fess.
This time, we will explain how to incorporate a search service into website using the Fess server that we have built.
There are several ways to incorporate Fess into your website as a search service. Let's talk about how to make a smooth transition from Google Site Search (GSS) to Fess.

If you want to incorporate GSS into your own website, you can use it simply by embedding the javascript tag on the page where you want to use the search service.
Fess provides the same function as Fess Site Search (FSS), you can use the search function of the built Fess server just by adding the FSS JavaScript to the page where you want to display the search results.
If you want to save the trouble of building and operating a Fess server, we provide an inexpensive Fess server as a commercial service. If you use it, you can enable search simply by placing our FSS JavaScript on your page.

We will explain the JavaScript of FSS (FSS JS) and the how to add it.

What is FSS JS?
===============

FSS JS is a JavaScript file that displays Fess search results.
By placing this JavaScript file on your company website, you will be able to display search results.
FSS JS can be generated and obtained from the site called FSS JS Generator at https://fss-generator.codelibs.org/

|image0|

There are many customization options, and the items that can be customized with FSS JS Generator will keep increase.

When "Generate" button is pressed, a preview of the search result is displayed with the generated JavaScript.

|image1|

If there is no problem in this preview display, press the "Download JS" button to download the JavaScript file.

Use FSS on Your Site
====================

This time, let's consider an example of introducing site search to www.n2sm.net made of static HTML.
Search results will be displayed in search.html within the site, and the Fess server will be built separately on nss833024.n2search.net.
The downloaded FSS JS JavaScript file is placed on the site as /js/fess-ss.min.js.

The above information is summarized as follows.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Subject name
     - URL
   * - Search target site
     - `https: // www.n2sm.net /`
   * - Search results page
     - `https://www.n2sm.net/search.html`
   * - FSS JS
     - `https://www.n2sm.net/js/fess-ss.min.js`
   * - Fess server
     - `https://nss833024.n2search.net/`

To embed the javascript tag, place the following tag in the place where you want to display search results in search.html.

.. code-block:: javascript

   <script>
     (function() {
       var fess = document.createElement('script');
       fess.type = 'text/javascript';
       fess.async = true;
       // Set the URL of FSS JS to src
       fess.src = 'https://www.n2sm.net/js/fess-ss.min.js';
       fess.charset = 'utf-8';
       fess.setAttribute ('id', 'fess-ss');
       // Set the URL of Fess search API to fess-url
       fess.setAttribute ('fess-url', 'https://nss833024.n2search.net/json');
       var s = document.getElementsByTagName ('script') [0];
       s.parentNode.insertBefore (fess, s);
     }) ();
   </script>
   <fess:search></fess:search>

When you access search.html, a search form will be displayed.
When you enter a search term, the search results can be displayed as follows.

|image2|

To display a search result by placing a search form on another page, place a search form as shown below on each page and pointing to https://www.n2sm.net/search.html?q=word


.. code-block:: html

   <form action="https://www.n2sm.net/search.html" method="get">
     <input type="text" name="q">
     <input type="submit" value="Search">
   </form>

Summary
=======

This time, we introduced how to embed Fess search results on the site just by placing JavaScript tags.
With FSS, migration from GSS can be achieved simply by replacing existing JavaScript tags.
FSS JS has other display methods and methods to link search logs with Google Analytics.
For other settings, refer to the FSS `Manual <https://fss-generator.codelibs.org/docs/manual>`__.

Next time, we will show you how to use Fess as a web scraping platform.

.. |image0| image:: ../../../resources/images/en/article/2/fss-top.png
.. |image1| image:: ../../../resources/images/en/article/2/fss-preview.png
.. |image2| image:: ../../../resources/images/en/article/2/fss-result.png

