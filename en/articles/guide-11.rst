===========================================================================
Part 11: Extending Existing Systems with the Search API -- Integration Patterns for CRM and Internal Systems
===========================================================================

Introduction
============

Fess can be used not only as a standalone search system but also as a "search microservice" that provides search functionality to existing business systems.

This article introduces concrete patterns for integrating with existing systems using the Fess API.
It covers practical integration scenarios such as embedding customer document search into a CRM, building an FAQ search widget, and constructing a document portal.

Target Audience
===============

- Those who want to add search functionality to existing business systems
- Those interested in system integration using the Fess API
- Those with basic knowledge of web application development

Overview of the Fess API
========================

Here is a summary of the main APIs provided by Fess.

.. list-table:: Fess API List
   :header-rows: 1
   :widths: 25 45 30

   * - API
     - Purpose
     - Endpoint
   * - Search API
     - Full-text search of documents
     - ``/api/v1/documents``
   * - Label API
     - Retrieve available labels
     - ``/api/v1/labels``
   * - Suggest API
     - Retrieve auto-completion candidates
     - ``/api/v1/suggest-words``
   * - Popular Words API
     - Retrieve popular search keywords
     - ``/api/v1/popular-words``
   * - Health API
     - Check system operational status
     - ``/api/v1/health``
   * - Admin API
     - Configuration operations (CRUD)
     - ``/api/admin/*``

Access Tokens
----------------

When using the API, authentication via access tokens is recommended.

1. Create an access token under [System] > [Access Token] in the admin console
2. Include the token in the API request header

::

    Authorization: Bearer {access_token}

Roles can be assigned to tokens, and role-based search result control is also applied to searches performed via the API.

Pattern 1: Embedding Search in a CRM
=====================================

Scenario
--------

Add a document search function for customer-related documents to the CRM system used by the sales team.
Enable cross-document searching of proposals, meeting minutes, contracts, and more from the customer screen in the CRM.

Implementation Approach
-----------------------

Embed a search widget in the CRM customer screen.
Send the customer name as a search query to the Fess API and display the results within the CRM screen.

.. code-block:: javascript

    // Search widget within the CRM screen
    async function searchCustomerDocs(customerName) {
      const params = new URLSearchParams({
        q: customerName,
        num: '5',
        'fields.label': 'sales-docs'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

Key Points
----------

- Use ``fields.label`` to narrow results to sales-related documents
- Use ``num`` to limit the number of displayed results (adjusted to fit the CRM screen space)
- It is useful to allow searching not only by customer name but also by project name or project number

Pattern 2: FAQ Search Widget
===============================

Scenario
--------

Add an FAQ search widget to the internal inquiry handling system.
Before employees submit an inquiry, encourage self-resolution by searching for related FAQs.

Implementation Approach
-----------------------

Combine the Suggest API and the Search API to display candidates in real time during input.

.. code-block:: javascript

    // Suggestions during input
    async function getSuggestions(query) {
      const params = new URLSearchParams({ q: query, num: '5' });
      const url = `https://fess.example.com/api/v1/suggest-words?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

The Suggest API is used to display candidates while the user is typing keywords.
When the user finalizes a keyword and executes the search, the Search API retrieves detailed search results.

Key Points
----------

- Since real-time responsiveness is critical for the Suggest API, verify the response speed
- Manage FAQ categories with labels and provide category-based filtering
- Display "frequently searched keywords" using the Popular Words API to assist users in searching

Pattern 3: Document Portal
============================

Scenario
--------

Build an internal document management portal.
Provide an interface that combines category-based browsing with full-text search.

Implementation Approach
-----------------------

Use the Label API to retrieve the list of categories and the Search API to retrieve documents within each category.

.. code-block:: javascript

    // Retrieve label list
    async function getLabels() {
      const url = 'https://fess.example.com/api/v1/labels';
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

    // Search filtered by label
    async function searchByLabel(query, label) {
      const params = new URLSearchParams({
        q: query || '*',
        'fields.label': label,
        num: '20',
        sort: 'last_modified.desc'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

Key Points
----------

- The Label API dynamically retrieves the category list (additions and deletions of labels are immediately reflected on the API side)
- Use ``sort=last_modified.desc`` to display the most recent documents at the top
- Browsing without keywords (retrieving all items) is also possible with ``q=*``

Pattern 4: Content Indexing API
=================================

Scenario
--------

Register data generated by external systems (logs, reports, chatbot response records, etc.) into the Fess index to make it searchable.

Implementation Approach
-----------------------

Using the Fess Admin API, documents can be registered in the index from external sources.

Use the document endpoint of the Admin API to send information such as the title, URL, and body text via a POST request.

Key Points
----------

- Effective for integrating data sources that cannot be obtained through crawling
- Batch processing can also be used to register multiple documents at once
- Set access token permissions appropriately and restrict write permissions

Best Practices for API Integration
====================================

Error Handling
------------------

In API integration, error handling that accounts for network failures and Fess server maintenance is important.

- Timeout settings: Set appropriate timeouts for Search API calls
- Retry logic: Implement retries for transient errors (approximately 3 retries maximum)
- Fallback: Provide an alternative display when Fess is not responding (e.g., "The search service is currently unavailable")

Performance Considerations
-----------------------------

- Response caching: Cache results for the same query for a short period
- Limiting result count: Retrieve only the necessary number of results (``num`` parameter)
- Field specification: Retrieve only the necessary fields to reduce response size

Security
------------

- Use HTTPS communication
- Rotate access tokens
- Set token permissions to the minimum required (e.g., read-only)
- Configure CORS appropriately

Summary
========

This article introduced integration patterns with existing systems using the Fess API.

- **CRM integration**: Related document search from the customer screen
- **FAQ widget**: Real-time candidate display with Suggest + Search
- **Document portal**: Category browsing via the Label API
- **Content indexing**: Registration of external data via the API

The Fess API is REST-based and simple, making integration with various systems easy.
The ability to add search functionality to existing systems as an "aftermarket" addition is one of Fess's greatest strengths.

In the next article, we will cover scenarios for making SaaS and database data searchable.

References
==========

- `Fess Search API <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__

- `Fess Admin API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__
