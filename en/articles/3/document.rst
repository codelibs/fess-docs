==============================
Part 3: Web Scraping with Fess
==============================

In our previous article, we showed you how to add site search to your existing site.
This time, we would like to introduce the web scraping function of Fess.

Web scraping is a technology used to extract information from the vast amount of data available on the Internet.
Fess has a powerful crawler that allows you to extract specified parts from a web page and save them in an index.
By using Fess, you can collect and analyze necessary information through configuration settings instead of writing your own web scraping algorithms.

In this article and the next, we will demonstrate how to collect information from news sites and create a model for classifying text.

Problem
=======

Let's consider creating a text classification model.
Assuming there are categories such as "server/storage" in those articles, how can we determine which category an arbitrary sentence belongs to? Fess can be used to create a classification model for this purpose.
By adjusting the settings, it is possible to build a system involving natural language processing, such as detecting spam documents and automatically sorting articles, as shown in this sample application.

Next, we will explain how to build a web scraping server using Fess to address this problem.
Please install Fess by following the procedure outlined at https://fess.codelibs.org/setup.html.

Crawling Target Analysis
========================

To perform web scraping, you need to understand what will be crawled.
If you crawl a news site, the following types of pages may be included:

- Article list page: URL includes page number such as p=1 or page=1
- Article page: Similar upper part like .../article/<article name>

You can crawl both types of pages and save only the latter to collect the required information.
The article page can be determined from the URL by clicking the pagination link on the list page.

Next, consider extracting the necessary parts from the article page.
Normally, crawling with Fess will only index the text below the body tag as a search target.
However, you can specify the location you want to index with XPath and extract the value to save.
For example, if you want the title tag value, specify //TITLE to extract and save the value (in Fess, the XPath tag name must be specified in uppercase).

Creating a Crawl Configuration
==============================

Once the crawl target and extraction location are determined, create the crawl settings on the management screen.
The web crawl settings for this example are as follows:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Item
     - Value
   * - Name
     - IT Search + Explanations/Case Studies
   * - URL
     - | ``https://news.mynavi.jp/itsearch/article/push_list/all``
       | ``https://news.mynavi.jp/itsearch/article/push_list/all_2``
       | ``https://news.mynavi.jp/itsearch/article/push_list/all_3``
       | ``https://news.mynavi.jp/itsearch/article/push_list/all_4``
       | ``https://news.mynavi.jp/itsearch/article/push_list/all_5``
       | ``https://news.mynavi.jp/itsearch/article/push_list/all_6``
       | ``https://news.mynavi.jp/itsearch/article/push_list/all_7``
       | ``https://news.mynavi.jp/itsearch/article/push_list/all_8``
       | ``https://news.mynavi.jp/itsearch/article/push_list/all_9``
       | ``https://news.mynavi.jp/itsearch/article/push_list/all_10``
   * - URLs to be crawled
     - | ``https://news.mynavi.jp/itsearch/article/push_list/all.*``
       | ``https://news.mynavi.jp/itsearch/article/.*/[0-9]+``
   * - URL to search
     - ``https://news.mynavi.jp/itsearch/article/.*/[0-9]+``
   * - Configuration parameter
     - | field.xpath.article_category=//LI[@class='genre_tag sp-none']/SPAN
       | field.xpath.article_body=//DIV[@class='articleContent']/P
       | config.html.canonical.xpath=
   * - Depth
     - 1
   * - Interval
     - 3000 milliseconds

First, Fess checks the "URL" to start crawling.
Fess then checks the second page of the list page.
Since the URL is specified in the format including the page number like all_2, it adds it to the list to be crawled.
If there is a link from the article page to another article page, it will be crawled one after another until reaching the maximum depth.
By limiting the "Depth" to 1, it will be linked directly from the list page group specified by the URL.

By specifying the URL to be crawled, it restricts crawling to only the list page and the article page.
Also, since it is not necessary to save the list page, it is specified to save only the article page with the URL to be searched.

In this setup, Fess will get the category information from the article page, save it in the article_category field, and save only the article body in the article_body field.
In Fess, by writing field.xpath.[Field name] = [XPath] in the configuration parameter, the value extracted by the specified field name can be saved in the index.

Depending on the site, the canonical URL may be specified on the list page, and Fess will process it with the canonical URL.
Therefore, canonical processing is disabled by leaving config.html.canonical.xpath empty in the configuration parameters.

Change of Expiration Date
=========================

Fess sets an expiration date for data indexed during a crawl.
The default expiration is three days, so the collected data will be deleted after three days.
To prevent deletion, set the value of "Delete previous documents" to -1 days in the settings of the "General" crawler from the administration screen.

Check Crawl
===========

Once you have configured the settings up to this point, start the Default Crawler job in the "scheduler" and perform a crawl.
After the crawl job finishes, check the saved values.
Fess can set additional fields which are not searched or displayed by default.
Change the following property values in app/WEB-INF/classes/fess_config.properties to get the added article_category and article_body this time.

.. code-block:: properties

   # When writing by JSP
   query.additional.response.fields=article_category,article_body
   # To include in JSON response
   query.additional.api.response.fields=article_category,article_body

You need to restart Fess after changing fess_config.properties.
After restarting, you can confirm that the value has been obtained by calling the JSON API as shown below.

.. code-block:: bash

   curl -s "localhost:8080/json/?q=*" | \
     jq '.response.result[0] | {article_category: .article_category, article_body: .article_body[0:40]}'
   {
     "article_category": "sample category",
     "article_body": "my article body here"
   }

If you can't get it, check logs/fess-crawler.log to see if crawling is running as expected.

Summary
=======

This time, we introduced how to use Fess as a web scraping server.
By using this function, you can build an information-gathering environment without writing code for scraping, allowing you to focus on the analysis and machine learning tasks that are the primary objectives.

Next time, we will introduce how to create a classification model using data collected by Fess.

