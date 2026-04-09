============================================================
Part 3: Embedding Search into an Internal Portal -- Adding Search to Existing Websites
============================================================

Introduction
============

In the previous article, we launched Fess using Docker Compose and experienced its search capabilities.
However, in real-world scenarios, there is often a need not only to "use the Fess search screen as-is" but also to "add search functionality to an existing internal site or portal."

In this article, we introduce three approaches for integrating Fess search functionality into existing websites, and explain the characteristics and selection criteria for each.

Target Audience
===============

- Those who want to add search functionality to an internal portal or website
- Those with basic knowledge of front-end development
- Fess must already be up and running from the Part 2 procedures

Prerequisites
=============

- The Fess environment built in Part 2 (Docker Compose)
- A test web page (a local HTML file will work)

Three Integration Approaches
=============================

There are three main methods for integrating Fess search functionality into an existing site.

.. list-table:: Comparison of Integration Approaches
   :header-rows: 1
   :widths: 15 30 25 30

   * - Approach
     - Overview
     - Development Effort
     - Best Suited For
   * - FSS (Fess Site Search)
     - Simply embed a JavaScript tag
     - Minimal (a few lines of code)
     - Quickly adding search with minimal effort
   * - Search Form Integration
     - Navigate to Fess from an HTML form
     - Low (HTML changes only)
     - Using the Fess search screen as-is
   * - Search API Integration
     - Build a custom UI with the JSON API
     - Medium to High (front-end development)
     - Fully customizing design and behavior

Let us walk through each method with concrete scenarios.

Approach 1: Quick Addition with FSS (Fess Site Search)
=======================================================

Scenario
--------

You have an internal portal site, and while you have permission to edit the HTML, you want to avoid major modifications.
You want to enable searching of internal documents from the portal with minimal changes.

What is FSS?
------------

Fess Site Search (FSS) is a mechanism that adds search functionality simply by embedding a JavaScript tag into a web page.
Since the search box and search results are all handled by JavaScript, there is almost no need to change the existing page structure.

Implementation Steps
--------------------

1. Allow API access in the Fess administration screen.
   On the [System] > [General] page, enable JSON responses.

2. Embed the following code into the page where you want to add search functionality.

.. code-block:: html

    <script>
      (function() {
        var fess = document.createElement('script');
        fess.type = 'text/javascript';
        fess.async = true;
        fess.src = 'http://localhost:8080/js/fess-ss.min.js';
        fess.charset = 'utf-8';
        fess.setAttribute('id', 'fess-ss');
        fess.setAttribute('fess-url', 'http://localhost:8080/api/v1/documents');
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(fess, s);
      })();
    </script>

    <fess:search></fess:search>

A search box and search results will appear wherever the ``<fess:search>`` tag is placed.

Customization
-------------

The appearance of FSS can be customized with CSS.
By overriding the default styles provided by Fess, you can match the design of your existing site.

.. code-block:: css

    .fessWrapper {
      font-family: 'Noto Sans JP', sans-serif;
      max-width: 800px;
      margin: 0 auto;
    }
    .fessWrapper .searchButton {
      background-color: #1a73e8;
    }

Approach 2: Simple Integration with a Search Form
===================================================

Scenario
--------

Your internal portal already has a navigation bar in the header.
You want to add a search box there and have it navigate to the Fess search results screen when a search is performed.
You want to achieve this with HTML alone, without using JavaScript.

Implementation Steps
--------------------

Add the following HTML form to your existing navigation bar.

.. code-block:: html

    <form action="http://localhost:8080/search" method="get">
      <input type="text" name="q" placeholder="Internal search..." />
      <button type="submit">Search</button>
    </form>

That is all it takes. When a search is performed, the user is redirected to the Fess search results screen.
By customizing the design of the Fess search screen, you can provide a seamless experience.

Customizing the Fess Search Screen
------------------------------------

The Fess search screen is composed of JSP files and can also be edited from the administration screen.

1. Select [System] > [Page Design] in the administration screen
2. Customize the header, footer, CSS, and more

For example, by matching the logo with your internal portal or unifying the color scheme, you can provide a search experience that feels natural to users.

Using Path Mapping
--------------------

You can convert the URLs displayed in search results to URLs that are more accessible to users.
For example, even if the URL at crawl time is ``http://internal-server:8888/docs/``, you can have search results display ``https://portal.example.com/docs/`` instead.

This can be configured from [Crawler] > [Path Mapping] in the administration screen.

Approach 3: Full Customization with the Search API
====================================================

Scenario
--------

You want to integrate search functionality into an internal business application.
You want full control over the design and how search results are displayed.
You have front-end development resources available.

Search API Basics
------------------

Fess provides a JSON-based search API.

::

    GET http://localhost:8080/api/v1/documents?q=search+keyword

The response is in JSON format as shown below.

.. code-block:: json

    {
      "record_count": 10,
      "page_count": 5,
      "data": [
        {
          "title": "Document Title",
          "url": "https://example.com/doc.html",
          "content_description": "...excerpt of body text containing the search keyword..."
        }
      ]
    }

Implementation Example in JavaScript
--------------------------------------

Below is a basic implementation example using the search API.

.. code-block:: javascript

    async function searchFess(query) {
      const url = new URL('http://localhost:8080/api/v1/documents');
      url.searchParams.set('q', query);
      const response = await fetch(url);
      const data = await response.json();

      const results = data.data;
      const container = document.getElementById('search-results');
      container.textContent = '';

      results.forEach(item => {
        const div = document.createElement('div');
        const heading = document.createElement('h3');
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        heading.appendChild(link);
        const desc = document.createElement('p');
        desc.textContent = item.content_description;
        div.appendChild(heading);
        div.appendChild(desc);
        container.appendChild(div);
      });
    }

Additional API Parameters
--------------------------

The search API supports various parameters to customize search behavior.

.. list-table:: Key API Parameters
   :header-rows: 1
   :widths: 20 50 30

   * - Parameter
     - Description
     - Example
   * - ``q``
     - Search keyword
     - ``q=Fess``
   * - ``num``
     - Number of results per page
     - ``num=20``
   * - ``start``
     - Starting position of search results
     - ``start=20``
   * - ``fields.label``
     - Filter by label
     - ``fields.label=intranet``
   * - ``sort``
     - Sort order
     - ``sort=last_modified.desc``

By leveraging the API, you can achieve fine-grained control over filtering, sorting, pagination, and more for search results.

Choosing the Right Approach
============================

Choose among the three approaches based on your situation.

**When to choose FSS**

- Development resources are limited
- You want to add search with minimal changes to existing pages
- A standard look and feel for search functionality is sufficient

**When to choose Search Form Integration**

- The Fess search screen design is sufficient
- You do not want to use JavaScript
- You only need to add a search box to the header or sidebar

**When to choose the Search API**

- You want full customization of how search results are displayed
- You want to integrate into a SPA (Single Page Application)
- You want to apply custom logic (filtering, highlighting, etc.) to search results
- You have front-end development resources available

Combining Approaches
---------------------

These approaches are not mutually exclusive.
For example, you could use FSS to quickly add search functionality to the top page, while providing a custom UI built with the API on a dedicated search page. Such combinations are also effective.

Summary
========

In this article, we introduced three approaches for integrating Fess search functionality into existing websites.

- **FSS**: Add search functionality simply by embedding a JavaScript tag
- **Search Form Integration**: Navigate to the Fess search screen from an HTML form
- **Search API**: Build a fully customized search experience with the JSON API

Regardless of which approach you choose, you can take full advantage of the search quality provided by the Fess backend.
Select the best method based on your requirements and available development resources.

In the next article, we will cover scenarios for unified search across multiple data sources such as file servers and cloud storage.

References
==========

- `Fess Site Search <https://github.com/codelibs/fess-site-search>`__

- `Fess Search API <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__
