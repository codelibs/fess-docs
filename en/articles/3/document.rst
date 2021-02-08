===================================
Part 3: Web Scraping with Fess
===================================

Last time we showed you how to add site search to your existing site.
Fess has various functions, this time we would like to introduce the Web scraping function.

There is a lot of information on the Internet, and the technology to extract information from it is Web Scraping.
Fess has a powerful crawler, so you can extract specified parts from within a web page and save them in an index.
By using Fess, it is possible to collect and analyze necessary information using setting instead of writing your own web scraping algorithms.

In this and the next article, we will introduce how to collect information from news sites and create a model for classifying text.

Problem
=======

Let's consider creating a text classification model. Assuming there are categories such as "server / storage" in those articles, so which category does it belong to given an arbitrary sentence?
Fess can be used to create a classification model that can jdo that. By changing the settings, it is possible to build a system that involves natural language processing, such as judging spam documents and automatically sorting articles as used in this sample application.

Next, we will explain how to build a web scraping server using Fess for this problem.
Please install Fess by referring to the procedure of at https://fess.codelibs.org/setup.html

Crawling target analysis
========================

In order to do web scraping, you need to understand what is being crawled.
If your crawl a news site,

- Article list page: URL includes page number such as p=1 or page=1
- Article page: Same upper part like .../article/<article name>

You can crawl the two types of pages and save only the latter to collect the information you need.
The article page can be determined from the URL by clicking the pagination link in that list page.

Next, consider extracting the necessary parts from the article page.
Normally crawling with Fess will only index the text below the body tag as a search target. You can also specify the location you want to index with XPath and extract the value to save.
For example, if you want the title tag value, specify //TITLE to extract and save the value (in Fess, the XPath tag name must be specified in uppercase).

Creating a crawl configuration
==============================

Once the crawl target and extraction location are determined, create the crawl settings on the management screen.
The web crawl settings this time are as follows.

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
     - ``https://news.mynavi.jp/itsearch/article/.*/ [0-9] +``
   * - Configuration parameter
     - | field.xpath.article_category=//LI[@class='genre_tag sp-none']/SPAN
       | field.xpath.article_body=//DIV[@class='articleContent']/P
       | config.html.canonical.xpath=
   * - Depth
     - 1
   * - Interval
     - 3000 milliseconds

First, Fess check the "URL" to set to start crawl.
Fess then check the second page of the list page, since the URL is specified in the format including the page number like all \ _2, it adds it to the list to be crawled.
If there is a link from the article page to the article page, it will be crawled one after another until reach the maximum depth. By limiting the "Depth" to 1, it will be linked directly from the list page group specified by the URL.

By specifying the URL to be crawled, it is restricted to crawl only the list page and the article page.
Also, since it is not necessary to save the list page, it is specified to save only the article page with the URL to be searched.

In this setup, Fess will get the category information from the article page, save it in the article \ _category field, and save only the article body in the article \ _body field.
In Fess, by writing field.xpath. [Field name] = [XPath] in the configuration parameter, the value extracted by the specified field name can be saved in the index.

Depending on the site, the canonical URL may be specified on the list page, and Fess will process it with the canonical URL.
Therefore, canonical processing is disabled by leaving config.html.canonical.xpath empty in the configuration parameters.

Change of expiration date
=========================

Fess sets an expiration date for data indexed during crawl.
The default expiration is three days, so the collected data will be deleted after three days.
To prevent deletion, set the value of "Delete previous documents" to -1 days in the settings of the "General" crawler from the administration screen.

Check crawl
===========

Once you have configured the settings up to this point, start the Default Crawler job in the "scheduler" and perform a crawl.
After the crawl job finishes, check the saved values.
Fess can set additional fields which are not searched or displayed by default.
Change the following property values ​​in app / WEB-INF / classes / fess \ _config.properties to get the added article \ _category and article \ _body this time.

.. code-block:: properties

   # When writing by JSP
   query.additional.response.fields=article_category,article_body
   # To include in JSON response
   query.additional.api.response.fields=article_category,article_body


You need to restart Fess after changing fess \ _config.properties.
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
By using this function, it is possible to build an information gathering environment without writing code for scraping, and focus on the analysis and machine learning tasks that are the original objectives .

Next time, we will introduce how to create a classification model using data collected by Fess.

