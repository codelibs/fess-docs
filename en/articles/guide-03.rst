====================================
Adding Search to an Existing Website
====================================

Introduction
============

When you want to add search to an intranet portal or a product site, it is not realistic to ask users to remember the URL of Fess.
What is expected is a search box in the header of the pages they always open, and a results page that looks like part of that site.

In this article, we use Fess 15.9 to try, in order, the following three methods, all of which are completed on the browser side only.

- Place an HTML search form on an existing page and show the results on the Fess search page
- Use Fess Site Search (FSS) to show search results inside a page of the existing site
- Change the look of the Fess search page (the theme) to match the existing site

We also configure "path mapping", which changes the link targets of search results to URLs that users can access.

Building your own screens by calling the search API from the server of a business system is covered in :doc:`guide-11`.

Prerequisites
=============

- Following the steps in :doc:`guide-02`, Fess 15.9 is running with Docker Compose at ``http://localhost:8080/``, and at least one thing has been crawled
- A local HTML file to stand in for the existing site

An existing site is normally on a different origin (the combination of scheme, host, and port) from Fess.
To reproduce that condition in this article, run the following command in the directory that holds the HTML file, and open it at ``http://localhost:8000/``.

::

    $ python3 -m http.server 8000

Choosing a Method
=================

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - Method
     - Where search results are shown
     - What Fess needs
   * - Search form
     - Moves to the Fess search page (``/search``) and shows them there
     - Nothing
   * - Fess Site Search
     - Inside a page of the existing site
     - The ``fess-webapp-v1-api`` plugin
   * - Changing the theme
     - The Fess search page (with a different look)
     - A theme ZIP (or the [General] settings)

The search form and a theme change can be combined.
If the page users land on after leaving the existing site should look the same, configure both.

Sending Queries from a Search Form to the Fess Search Page
==========================================================

Placing the Form
----------------

Write the following form where you want the search box on the existing page.

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <button type="submit">Search</button>
    </form>

The search terms are sent to ``/search`` of Fess as the ``q`` parameter, and the results are shown on the Fess search page.
``maxlength`` matches the upper limit for the length of search terms on the Fess side, ``query.max.length`` (default ``1000``).
In production, change the ``action`` URL to the Fess URL that users access.

To have users search only documents with a particular label, send the label value as ``fields.label`` as well.

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <input type="hidden" name="fields.label" value="intranet">
      <button type="submit">Search</button>
    </form>

``intranet`` is the value of a label created in [Crawler] > [Label].
If you send a value that does not exist, there will be 0 results.
For how to create labels, see :doc:`guide-04`.

Checking the Result
-------------------

1. Open the HTML file from ``http://localhost:8000/`` and search for a word contained in a crawled document
2. If the browser moves to ``http://localhost:8080/search?q=...`` and the results are shown on the Fess search page, you are done

If there are 0 results, search for the same word in the search box at ``http://localhost:8080/`` and compare.
If that also returns 0 results, the problem is not the form but crawling or permissions.

About Suggestions
-----------------

The `Search Form Integration <https://fess.codelibs.org/stable/config/search-form-integration.html>`__ page includes an example that adds suggestions to the form.
However, ``/js/suggestor.js`` and ``/js/jquery-3.7.1.min.js``, which that example loads, are not included in Fess 15.9, so the example does not work as is in 15.9.
The form part (sending ``q`` to ``/search``) can be used as it is.

To show suggestions in the search box of an existing site, use one of the following.

- Enable suggestions in Fess Site Search, described in the next section
- Call ``/api/v2/suggest-words`` from your own script (for how to use the API, see :doc:`guide-11`)

Once users have moved to the Fess search page, the theme bundled with Fess shows suggestions.

Showing Results Inside a Page with Fess Site Search
===================================================

Fess Site Search (FSS) is JavaScript that shows a search form and search results on a page of the existing site.
Users can search without leaving the existing site.

The FSS JavaScript is not served by Fess.
Download the file generated with FSS JS Generator (https://fss-generator.codelibs.org/) and place it on the server of the existing site.

Installing the v1 API Plugin
----------------------------

FSS calls ``/api/v1`` of Fess.
Fess 15.9 itself provides only ``/api/v2``; ``/api/v1`` is provided by the ``fess-webapp-v1-api`` plugin.
This plugin is not bundled with the Docker image.

With Docker Compose, add the following line to ``environment`` of ``fess01`` in ``compose.yaml``.

.. code-block:: yaml

    - "FESS_PLUGINS=fess-webapp-v1-api:15.9.0"

If you already specify other plugins, list them in the same value, separated by spaces.
After saving, run ``up -d`` with both Compose files.
``fess01`` is recreated, and the plugin is installed at startup.
Because the container is recreated, settings you changed in [System] > [General] are reset, just as with ``down`` (see the section on stopping and restarting in :doc:`guide-02`).

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

You can also install it from [System] > [Plugin] > [Install] in the admin console (Fess must be restarted after the installation).
With Docker, however, the plugin is placed inside the container, so it disappears when the container is recreated with ``down``.
If you specify it in ``FESS_PLUGINS``, it is installed again every time the container is recreated.

When ``fess01`` is healthy, check that the API responds.

::

    $ curl 'http://localhost:8080/api/v1/documents?q=fess'

If JSON containing ``"record_count"`` is returned, you are ready.
If 404 is returned, the plugin is not installed.
In that case, a WARN starting with ``No plugin serves the legacy API`` is written to ``fess.log`` once.
If the plugin is installed but no JSON is returned, check whether "JSON Response" in [System] > [General] is turned off.
Turning off "JSON Response" stops not only ``/api/v1`` but also ``/api/v2`` from responding, which also makes the Fess search page itself unusable.

Generating and Placing the JavaScript
-------------------------------------

1. Open https://fss-generator.codelibs.org/, specify colors, fonts, and so on in the generator, and click [Generate]
2. Download the JavaScript file with [Download JS]
3. Rename the file to ``fess-ss.js`` and place it in the same directory as the HTML file

On the page that shows the search results (for example, ``result.html``), write the following code.

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form
        language="en"
        :enable-suggest="true"
        suggest-url="http://localhost:8080"
      ></fess-search-form>
      <fess-search-result
        fess-url="http://localhost:8080"
        language="en"
      ></fess-search-result>
    </div>

``fess-url`` is the Fess URL used for searching, and ``suggest-url`` is the Fess URL used for suggestions.
In production, use a Fess URL that users' browsers can access.

In the header of the other pages, place only the search form.

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form result-page="result.html"></fess-search-form>
    </div>

The form puts the search terms into the ``fss.query`` parameter and moves to ``result.html``, and FSS on ``result.html`` runs the search.
When sending from a page that does not load FSS, a form that moves to ``result.html?fss.query=keywords`` works in the same way.

For other attributes (the number of results per page ``:page-size``, narrowing by label ``:enable-label``, opening links in a new tab ``link-target="_blank"``, and so on), see the FSS JS Generator manual.

Checking the Result
-------------------

1. Open ``http://localhost:8000/result.html`` and search with the search form
2. If search results are shown inside the page, you are done
3. If they are not shown, check the request to ``/api/v1/documents`` in the Network tab of the browser's developer tools. If it is 404, check the plugin; if it is a CORS error, check the next section

Points to Note
--------------

From the browser's point of view, calling the API on ``localhost:8080`` from a page on ``localhost:8000`` is cross-origin communication.
By default, Fess sets ``api.cors.allow.origin=*`` and accepts calls from any origin.
How to restrict callers to the existing site is covered in :doc:`guide-11`.

Searches that FSS sends from a different origin are treated as searches by a user who is not logged in (a guest), even if the user is logged in to Fess.
This is because FSS calls the API without cookies, and the default ``api.cors.allow.origin=*`` does not allow cross-origin communication with credentials either.
As a result, only documents that have ``{role}guest`` in their permissions appear in the results.
To show different documents to each department, have users log in on the Fess search page (see :doc:`guide-05`).

Changing the Look of the Fess Search Page
=========================================

In 15.9, the search page is rendered by a "theme", which bundles HTML, CSS, and JavaScript.
The [Page Design] screen and JSP editing of earlier versions no longer exist.
If nothing is configured, the bundled ``bootstrap`` theme is used.

What You Can Change Without Building a ZIP
------------------------------------------

What you write in "Search Top Page" under "Notice" in [System] > [General] is shown on the search top page and the search results page of the bundled theme.
You can also write HTML, but elements such as ``<script>`` and ``<style>`` are removed.
If all you want is a one-line notice for internal users, there is no need to build a theme.

Using a Published Theme
-----------------------

The Fess project publishes themes such as ``docsearch``, which is designed for document search.

1. Open [System] > [Theme]
2. Under "Install Theme", choose a theme in "Name" and click [Select]
3. In "Version", choose the version for 15.9 (``15.9.x``) and click [Install]
4. In "Default Theme" above the list, choose the installed theme and click [Set]

When you reopen ``http://localhost:8080/``, the page is shown with the new theme.
Choosing "(no default)" and clicking [Set] returns to the bundled ``bootstrap`` theme.

Copying the Bundled Theme and Changing the Logo and Colors
----------------------------------------------------------

The bundled theme cannot be edited directly, and a theme named ``bootstrap`` cannot be replaced by uploading one either.
Copy it under a different name and change the copy.
Here we use ``mytheme``.

1. Copy the bundled theme out of the container

   ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml cp fess01:/usr/share/fess/app/themes/bootstrap ./mytheme

2. In ``mytheme/theme.yml``, change ``name`` to ``mytheme`` and ``displayName`` to something like ``My Theme``
3. Change the following files

   - Colors and layout: ``assets/styles.css``
   - Logo: ``assets/logo-head.png`` (header) and ``assets/logo.png`` (search top page)
   - Organization name in the footer: ``footer.copyright_org`` in ``i18n/messages.en.json`` (``messages.ja.json`` for the Japanese UI)

4. Package the files so that ``theme.yml`` is at the root of the ZIP

   ::

       $ cd mytheme && zip -r ../mytheme.zip . && cd ..

5. Upload ``mytheme.zip`` with [Upload] in [System] > [Theme]
6. In "Default Theme", choose ``mytheme`` and click [Set]

Do not change ``index.html``.
The bundled ``index.html`` refers to the files in the theme in the form ``{{themePath}}/assets/...``.
Because Fess replaces ``{{themePath}}`` with ``themes/mytheme`` when serving the page, renaming the theme is enough for the files of the copied theme to be loaded.

Checking the Result
-------------------

Reopen ``http://localhost:8080/`` and check that the logo and colors have changed.
If they have not, check in the Network tab of the developer tools whether the stylesheet is loaded from ``/themes/mytheme/assets/styles.css``.
If it is loaded from ``/themes/bootstrap/``, the default theme setting has not taken effect.

Things to Watch Out for with Themes
-----------------------------------

- The search page carries a ``Content-Security-Policy`` header that limits the sources of scripts, styles, and images to Fess itself. Fonts and scripts from external CDNs are not loaded, so include them in the theme ZIP
- The search page is not shown inside an ``iframe`` of another page (because the default of ``theme.index.frame.ancestors`` is ``'none'``). To show search results inside a portal, use FSS
- ``fess01`` in Docker has no volumes. Uploaded themes are placed inside the container and the default theme setting is saved in ``system.properties``, so both disappear when the container is recreated with ``down``. Normally use ``stop``/``start``, and after recreating the container, upload and configure the theme again
- The bundled theme is built for ``/api/v2`` of the same version of Fess. After upgrading Fess, copy the new bundled theme again and reapply your changes

For the structure of themes and the items in ``theme.yml``, see the `Theme Development Guide <https://fess.codelibs.org/stable/dev/theme-development.html>`__.

Pointing Search Result Links to User-Facing URLs
================================================

You may want to crawl using an internal host name while having users open documents through the portal URL.
For example, you crawl ``http://intranet-web01:8080/docs/`` and want search results to open ``https://portal.example.com/docs/``.
In this case, use path mapping to replace the URL only when it is displayed.

1. Open [Crawler] > [Path Mapping] and click [Create New]
2. Enter the following and click [Create]

   .. list-table::
      :header-rows: 1
      :widths: 25 75

      * - Field
        - Value
      * - Regex
        - ``^http://intranet-web01:8080/docs/``
      * - Replacement
        - ``https://portal.example.com/docs/``
      * - Process Type
        - Displaying
      * - Sort Order
        - ``0``

"Displaying" replaces only the URL shown in search results and the link target.
The URL stored in the index does not change, so no recrawl is needed, and the change is reflected in search results as soon as you save it.
If you choose "Crawling" or "Crawling/Displaying", the replaced URL is stored in the index.
Note that choosing one of these when you only want to change the display also changes the URLs of subsequent crawls.

To check, search for a word that brings up the target document, and confirm that the URL in the results and the link target are ``https://portal.example.com/docs/...``.
When you receive results through the API, the replaced URL is in ``url_link``, not ``url`` (see :doc:`guide-11`).

For an example that changes file server paths into web server URLs, see `Path Mapping <https://fess.codelibs.org/stable/admin/pathmap-guide.html>`__.

What to Read Next
=================

- To call the search API from the server of a business system: :doc:`guide-11`
- To change the documents shown in the portal for each department: :doc:`guide-05`
- To search websites and file servers together and separate them with labels: :doc:`guide-04`
- To show a different theme or search target to each organization: :doc:`guide-13`
- To require login for the search page: :doc:`guide-15`

References
==========

- `Search Form Integration <https://fess.codelibs.org/stable/config/search-form-integration.html>`__
- `Theme <https://fess.codelibs.org/stable/admin/theme-guide.html>`__
- `Theme Development Guide <https://fess.codelibs.org/stable/dev/theme-development.html>`__
- `Path Mapping <https://fess.codelibs.org/stable/admin/pathmap-guide.html>`__
- `Plugin <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__
- `FSS JS Generator <https://fss-generator.codelibs.org/>`__
- `fess-site-search (GitHub) <https://github.com/codelibs/fess-site-search>`__
- `fess-webapp-v1-api (GitHub) <https://github.com/codelibs/fess-webapp-v1-api>`__
