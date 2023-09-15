=====================
Crawler Configuration
=====================

Setting Maximum Word Length
===========================

Words consisting solely of alphanumeric characters or consecutive symbols can lead to unnecessary index growth and reduced crawl performance. By default, |Fess| excludes words with more than 20 consecutive alphanumeric characters and words with more than 10 consecutive symbol characters during indexing. If you need to search for words longer than these limits, you can adjust the following settings in fess_config.properties:

::

    crawler.document.max.alphanumeric.term.size=20
    crawler.document.max.symbol.term.size=10

File Size Configuration
=======================

You have the option to specify the maximum file size for crawling, which includes:

* The maximum size for fetching files.
* The maximum file size for indexing based on file types.

Firstly, set the maximum file size for fetching using the client.maxContentLength parameter in the crawler configuration. To avoid fetching files larger than 10 megabytes, specify it as follows. There are no specific restrictions by default:

::

    client.maxContentLength=10485760

Next, regarding the limits for different file types, |Fess|, by default, processes HTML files up to 2.5 megabytes and other file types up to 10 megabytes. If you want to change these file size limits, edit app/WEB-INF/classes/crawler/contentlength.xml. The default contentlength.xml is structured as follows:

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
            "http://dbflute.org/meta/lastadi10.dtd">
    <components namespace="fessCrawler">
            <include path="crawler/container.xml" />

            <component name="contentLengthHelper"
                    class="org.codelibs.fess.crawler.helper.ContentLengthHelper" instance="singleton">
                    <property name="defaultMaxLength">10485760</property><!-- 10M -->
                    <postConstruct name="addMaxLength">
                            <arg>"text/html"</arg>
                            <arg>2621440</arg><!-- 2.5M -->
                    </postConstruct>
            </component>
    </components>

If you wish to modify the default values, you can change the defaultMaxLength value. You can specify the maximum file size for each content type. For HTML files, specify "text/html" along with the desired maximum file size limit.

When altering the maximum file size limits, please consider the amount of heap memory used.

Proxy Configuration
===================

If you need to crawl external sites from within an intranet, you may encounter issues with firewalls blocking the crawl. In such cases, configure a proxy for the crawler.

Configuration
-------------

In the administration panel's crawl settings, specify and save the following settings in the configuration parameters:

::

    client.proxyHost=ProxyServerName (e.g., 192.168.1.1)
    client.proxyPort=ProxyServerPort (e.g., 8080)

These revisions aim to provide a clearer and more concise explanation of the settings and procedures while maintaining accuracy in the technical details.