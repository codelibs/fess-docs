================================================
Company-Wide Rollout: A Stage-by-Stage Checklist
================================================

Introduction
============

When a Fess trial goes well and you decide to roll it out across the company, the hard part is less the features themselves than the order in which to set them up.
Some settings are expensive to change if you leave them for a later stage.
For example, changing the encryption key after credentials have been registered makes the stored values impossible to decrypt, and changing document permissions afterwards requires a re-crawl.

This article lays out, stage by stage, the order in which to roll out Fess 15.9 company-wide.
For each stage, it lists what to configure, what to check, and the indicators that tell you whether you are ready to move on to the next stage.
As indicators, we use the analytics reports in [System Info] > [Search Log] of the admin console.
The procedures for individual features are not explained here; instead, we link to the articles that cover them.

Components and the Articles That Cover Them
===========================================

The components involved in a company-wide rollout, and the articles that cover each of them in detail, are as follows.

- Fess itself: provides the search page, the admin console, the API and the scheduler. For an overview, see :doc:`guide-01`; for memory and scaling out, see :doc:`guide-14`
- OpenSearch: stores not only the document index but also crawl configurations, users, job logs and search logs. For separating it out and clustering, see :doc:`guide-14`; for snapshots, see :doc:`guide-10`
- Child processes such as the crawler: crawling, suggest generation, thumbnail generation and chunk processing run per job in a JVM separate from Fess itself. For their heap settings, see :doc:`guide-14`
- Plugins: data stores (``fess-ds-*``), SSO (``fess-sso-*``), LLM and embeddings (``fess-llm-*``), MCP and multimodal search (``fess-webapp-*``), and so on. Install the same minor version as Fess (15.9.x), and restart Fess after installing or removing one. For how to write one, see :doc:`guide-17`
- LLM and embedding models (optional): external services, or servers such as Ollama, used by the AI search mode and semantic search. For configuration, see :doc:`guide-18` and :doc:`guide-19`

Anything that is not stored in OpenSearch is managed separately on each Fess server.
That means three things: the settings in [System] > [General] (``system.properties``), ``fess_config.properties`` (including the encryption key ``app.cipher.key``), and the plugins you have installed.
For how to keep copies of these, see :doc:`guide-10`; for managing them as code, see :doc:`guide-16`.

Overview of the Stages
======================

.. list-table::
   :header-rows: 1
   :widths: 22 40 38

   * - Stage
     - Goal
     - Ready to move on when
   * - 1. Trial
     - Let a small number of users search and learn what they look for
     - You have recorded the top queries and the zero-hit queries
   * - 2. Publish the first source
     - Publish the first source with permissions and put the basics of operation in place
     - You have recorded baseline values for users and click-through rate
   * - 3. SSO and login
     - Let users log in with their company ID and tailor results by group
     - IdP groups appear in "Searches by Role and Group"
   * - 4. Add more sources
     - Add SaaS, cloud storage and databases
     - Zero-hit queries caused by missing documents disappear
   * - 5. Quality improvement cycle
     - Find problem queries in the search log and fix them
     - The metrics you fixed are no worse than in the previous period
   * - 6. Scaling and automation
     - Prepare for growth in documents and users, and make the environment reproducible
     - Response times on the [Performance] tab are no worse than before scaling, even as users increase
   * - 7. AI features
     - Add the AI search mode, semantic search and MCP
     - Requests are recorded on the [AI Chat] tab, and the error rate is no higher than right after introduction

Every stage assumes the settings of the previous stages.
In particular, stages 2 and 3 include settings that require a re-crawl if changed later, so do not swap their order.

Stage 1: Trial
==============

Set up a Fess instance for evaluation and have some departments use it.
The goal of this stage is to collect, as search logs, what users are looking for.

**What to configure**

- Following :doc:`guide-02`, start Fess with the Compose files from the ``v15.9.0`` tag of docker-fess, and change the password at your first login
- Create a crawl configuration limited to a single site or a single folder
- Make sure that "Search Log" and "User Log" are enabled in [System] > [General] (both are enabled by default). If "User Log" is disabled, the number of users is not counted

**What to check**

- In [System Info] > [Job Log], the crawl job ends with "OK", and in [System Info] > [Crawling Info], the number of indexed documents is not 0
- If there are few documents, look at [System Info] > [Failure URL] (:doc:`guide-02`)

**Ready to move on when**

- On the [Overview] tab of [Search Log], the searches, users, top queries and zero-hit queries for the trial period are displayed
- Click each zero-hit query, check the actual searches on the [Logs] tab, and then, following the table in :doc:`guide-08`, sort the causes into "different wording", "steer to the official term" and "no documents"
- Treat the terms sorted into "no documents" as candidate sources to add in stages 2 and 4. Download the table as CSV and keep it

Stage 2: Publish the First Source
=================================

Choose one source to be used by users across the company, and publish it with permissions.
At the same time, put in place the monitoring and backups needed for production operation.

**What to configure**

- Decide the encryption key ``app.cipher.key`` before registering credentials in web authentication, file authentication or data store parameters. If you change it after registering them, the stored values can no longer be decrypted (:doc:`guide-16`, :doc:`guide-10`)
- Create crawl configurations for websites and shared folders, file authentication, and labels (:doc:`guide-04`). To reflect a file server's ACLs in the search results, see :doc:`file-server-search`
- Decide on your permission design (:doc:`guide-05`). New crawl configurations and labels contain the permission ``{role}guest``, which as it stands makes them visible to users who have not logged in. For documents that should be visible only to certain departments, delete this value and then write ``{group}`` entries or similar
- Make the group names you write in ``{group}`` match the names that will arrive from the IdP in stage 3. Renaming them later requires rewriting the permissions and re-crawling
- If you have crawl configurations run by a job, for example once a week, make "Delete old documents" in [General] (default: 3 days) longer than the crawl interval (:doc:`guide-04`)
- Set up monitoring, notifications and backups (:doc:`guide-10`). Call ``/api/v2/health`` from an external monitoring tool, configure "Notification Mail" or "Slack Webhook URLs" in [General], and fetch the file from [System Info] > [Backup] through the admin API every day
- With Docker, the settings in [General] are stored in ``system.properties`` inside the ``fess01`` container, and they are lost when ``down`` recreates the container. Include them in your backups, or pass them through ``FESS_JAVA_OPTS`` (:doc:`guide-02`, :doc:`guide-16`)
- If needed, place a search box on the company portal (:doc:`guide-03`)

**What to check**

- Log in as users from different departments and confirm that the visible documents change. The permissions recorded on department-only documents no longer contain the default guest role (for how to check, see :doc:`guide-05`)
- ``/api/v2/health`` returns 200, and [Send Test Mail] in [General] delivers an email
- Run the backup script once by hand, and confirm that the file it fetches is not empty (:doc:`guide-10`)

**Ready to move on when**

[Search Log] does not tell you the state of the monitoring and backups set up in this stage.
Judge those with "What to check" above.
In the search log, record baseline values for usage after publication.

- On the [Overview] tab, check the searches, users, zero-hit rate and click-through rate for the period after publication, and keep them as CSV. In later stages, compare against these values using "Compare to previous period"
- The URLs of the published source appear in "Most clicked URLs" on the [Clicks] tab
- If you set a number of days in "Delete old search logs" in [General], logs older than that cannot be used for comparison (the default ``-1`` deletes nothing). Decide on a retention period

Stage 3: SSO and Login
======================

Have users log in through the company identity provider (IdP), and tailor search results by IdP group.

SSO here means the four methods provided as plugins in Fess 15.9.
Entra ID uses ``fess-sso-entraid``, OpenID Connect uses ``fess-sso-oidc`` ("SSO Type" is ``oic``), SAML uses ``fess-sso-saml``, and SPNEGO uses ``fess-sso-spnego``.
The Docker images include all four, but the ``-slim`` images do not.
With the ZIP, RPM and DEB packages, install them from [System] > [Plugin] or with ``bin/fess-setup``.

LDAP is not SSO.
The LDAP settings in [General] verify the ID and password entered on the Fess login page against Active Directory or a similar directory, and retrieve the user's groups (:doc:`guide-05`).
SPNEGO uses these LDAP settings to retrieve groups.

**What to configure**

- Install the plugin, restart Fess, and set "SSO Type" and the IdP details in [General]. The return URL to register with the IdP is ``https://<Fess host>/sso/`` (:doc:`guide-15`)
- When Fess sits behind a reverse proxy that terminates TLS, tell Fess the external scheme and port (:doc:`guide-15`)
- If users who have not logged in must not be able to search, enable "Login Required" in [General]

"Login Required" affects more than the search page.

- The search API under ``/api/v2/`` returns 401 to calls that have neither a login session nor a valid access token. Prepare tokens for calls from business systems (:doc:`guide-11`)
- With the default ``mcp.auth.mode=none``, ``/mcp`` rejects calls from AI agents with HTTP 403. If you use it, change the setting so that it authenticates with access tokens (:doc:`guide-20`)

**What to check**

- Opening ``/sso/`` lets you log in through the IdP, and the documents visible to each department change as designed in stage 2 (:doc:`guide-15`)
- If you run Fess on multiple servers, sticky sessions are enabled on the load balancer. In 15.9, login sessions are held in the memory of each Fess

**Ready to move on when**

- Under "Searches by Role and Group" on the [Audience] tab of [Search Log], rows for the groups received from the IdP are listed in the form ``{group}<group name>``
- If no group rows appear, either users are searching without logging in (counted in the ``{role}guest`` row), or the groups are not reaching Fess
- The number of users on the [Overview] tab has not dropped significantly from the stage 2 baseline. Use the users column of "Searches by Role and Group" to check that no department has stopped using search because of the introduction of login

Stage 4: Add More Sources
=========================

Add sources other than websites and file servers through data store plugins.
The steps common to all sources (installing the plugin, parameters and scripts, permissions, jobs, and how to check the results) are collected in :doc:`datastore-basics`.
Read it first.

**What to configure**

- Install the plugin for each source and restart

  - Git, Confluence/Jira, Slack: ``fess-ds-git``, ``fess-ds-atlassian``, ``fess-ds-slack`` (:doc:`guide-06`)
  - Google Drive, SharePoint/OneDrive, Box: ``fess-ds-gsuite``, ``fess-ds-microsoft365``, ``fess-ds-box`` (:doc:`guide-07`)
  - Databases, CSV, Salesforce: ``fess-ds-db``, ``fess-ds-csv``, ``fess-ds-salesforce`` (:doc:`guide-12`)
  - For a source with no matching plugin, write your own plugin (:doc:`guide-17`)

- Data store configurations also contain ``{role}guest``. For each configuration, decide whether to inherit the source's permissions or to write them with the ``{group}`` entries from stage 2
- Use [Create New Job] to give each configuration its own job, so that API rate limits and credential expiry can be handled per source
- Give each source a label so that users can narrow results on the search page. Data store configurations have no label field, so assign labels with a script or with the label's "Included Paths" (:doc:`datastore-basics`)

**What to check**

- A data store job may end with "OK" even when an error occurs in the connector. Check "Index Size (Data Store)" in [Crawling Info], [Failure URL] and ``fess-crawler.log`` together (:doc:`datastore-basics`)
- For sources whose permissions are inherited, search as users with different permissions and confirm that the visible documents change

**Ready to move on when**

- The zero-hit queries sorted into "no documents" in stages 1 and 2 disappear from the zero-hit queries on the [Queries] tab for the period after the source was added
- Documents from the added sources appear in "Most clicked URLs" on the [Clicks] tab. A source that does not appear is either not being searched for, or not ranking near the top of the results. The latter is handled in stage 5

Stage 5: Quality Improvement Cycle
==================================

Once the sources are in place, review the search log regularly and fix problem queries.
How to choose a fix and the steps to apply it are covered in :doc:`guide-08`.

**What to configure**

- Use synonyms or related queries for zero-hit queries, and key match or document boost for documents buried low in the results (:doc:`guide-08`). After changing the synonym dictionary, reload the document index in [System Info] > [Maintenance]
- If documents that mix Japanese, English and Chinese are missed, check the per-language fields and dictionaries (:doc:`guide-09`)
- When you need aggregations that the built-in reports do not provide (URLs opened per search term, zero-hit queries per role, month-by-month trends over a long period, and so on), use OpenSearch Dashboards (:doc:`guide-22`)
- To manage dictionaries and key match settings as code, see :doc:`guide-16`

**What to check**

- Search for the fixed terms on the search page and confirm that the intended documents are found or ranked near the top
- For key match, the target documents are shown in the "URLs" field of the details page (:doc:`guide-08`)

**Ready to move on when**

This stage never ends; you repeat it.
Check the effect of each improvement as follows.

- Set the period to "Custom" starting from the day after the change, and enable "Compare to previous period"
- If you fixed zero-hit queries, look at the zero-hit rate on the [Overview] tab and the zero-hit queries on the [Queries] tab; if you fixed rankings, look at the average click position on the [Queries] tab and the click position distribution on the [Clicks] tab
- If the fixed terms have disappeared from the list and the overall metrics are no worse than in the previous period, keep the change

Stage 6: Scaling and Automation
===============================

As documents and users grow, find out what is running short before scaling.
At the same time, make it possible to rebuild the same environment.

**What to configure**

- Identify what is running short from the symptoms (:doc:`guide-14`). An OutOfMemoryError in ``fess-crawler.log`` is a shortage in the crawler's JVM (``jvm.crawler.options``), and increasing the heap of Fess itself (``FESS_HEAP_SIZE``) does not fix it
- Consider, in this order: moving OpenSearch to a separate server, making it a three-node cluster, and running multiple Fess servers (:doc:`guide-14`)
- When running multiple Fess servers, leave crawling to one of them. Set both ``scheduler.target.name`` and "Target" in [System] > [Scheduler] (:doc:`guide-14`)
- With multiple servers, keep ``app.cipher.key``, ``fess_config.properties``, the settings in [General] and the plugins identical on all servers
- Pin the Docker image tag and the plugin versions, and make the settings applicable with fessctl and the admin API (:doc:`guide-16`)
- To share one Fess among several organizations, combine virtual hosts with roles. Virtual hosts alone do not provide access control (:doc:`guide-13`)

**What to check**

- Before and after scaling, compare the heap usage from ``/api/admin/stats`` and the crawl duration in [System Info] > [Job Log] (:doc:`guide-10`)
- With multiple servers, the search results are the same whichever server you open, and crawls run only on the assigned server. Clicking [Start Now] on another server does not run the crawl (:doc:`guide-14`)
- Settings can be restored from a backup into a rebuilt environment (:doc:`guide-10`)

**Ready to move on when**

- On the [Performance] tab of [Search Log], the median, p95 and p99 response times are lower than before scaling, or have not risen even as users increased
- Search for the terms listed in "Slowest queries" to tell whether only certain terms are slow or everything is slow

Note that the ability to store login sessions in OpenSearch and share them across multiple servers is available from 15.10.
In 15.9, operate with the sticky sessions mentioned earlier.

Stage 7: AI Features
====================

Each AI feature needs different preparation.
Add the ones that fit your goals first.

**AI search mode (RAG)**

- An LLM answers users' questions based on internal documents (:doc:`guide-19`)
- Vector search is not required. The supporting documents are gathered with an ordinary search, so the permissions from stages 2 and 3 apply as they are, and documents a user cannot see are not used in the answer
- Three things are required: ``rag.chat.enabled=true`` in ``fess_config.properties`` (the default is ``false``, and there is no item for it in the admin console), a ``fess-llm-*`` plugin, and "LLM Provider" in [General]
- You can restrict which users can use it with "Chat Permissions" in [General]

**Semantic search and multimodal search**

- Semantic search finds documents that are close in meaning even when the keywords do not match (:doc:`guide-18`). Choose the embedding provider with ``content_chunker.embedding.name``. The default ``opensearch`` uses a model in OpenSearch ML Commons, while ``ollama``, ``openai``, ``gemini`` and ``bedrock`` require the corresponding ``fess-llm-*`` plugin
- To enable it on an existing environment, recreate the index and then generate vectors for all documents. With pay-per-use models such as OpenAI, the initial processing incurs charges for every document
- Multimodal search uses the ``fess-webapp-multimodal`` plugin and a CLIP server to find images with text (:doc:`guide-21`)
- These two cannot be used at the same time on a single Fess. If you need both, build separate Fess instances

**MCP**

- Lets AI agents search Fess (:doc:`guide-20`). Installing the ``fess-webapp-mcp`` plugin makes ``/mcp`` available
- With the default ``mcp.auth.mode=none``, anyone who can reach ``/mcp`` can search as a guest. Before exposing it within the company, change the setting so that it authenticates with access tokens or similar

**What to check**

- AI search mode: ask a question with [AI Search] on the search page, and an answer and its sources are displayed. For users with different permissions, documents they cannot see do not appear among the sources (:doc:`guide-19`)
- Semantic search and multimodal search: vectors are written to the documents, and the search API response shows that vector search is used (:doc:`guide-18`, :doc:`guide-21`)
- MCP: after changing the authentication setting, calls without a token are rejected (:doc:`guide-20`)

**Ready to move on when**

- For the AI search mode, look at the requests, users, error rate and average response time on the [AI Chat] tab of [Search Log]. Token counts are recorded only when the LLM plugin reports them, and the content of questions and answers is not recorded
- For semantic search, enable "Compare to previous period" for a period starting the day after introduction, and compare the zero-hit rate, the click-through rate and the response times on the [Performance] tab
- MCP and multimodal search have no dedicated metrics in [Search Log]. Judge them by "What to check" above and by feedback from the departments using them

Further Reading
===============

- Start a trial: :doc:`guide-02`
- Publish the first source with permissions: :doc:`guide-04`, :doc:`guide-05`, :doc:`file-server-search`
- Monitoring and backups: :doc:`guide-10`
- SSO: :doc:`guide-15`
- Add more sources: :doc:`datastore-basics`
- Improve quality with the search log: :doc:`guide-08`
- Scaling and configuration as code: :doc:`guide-14`, :doc:`guide-16`
- AI features: :doc:`guide-19`, :doc:`guide-18`, :doc:`guide-20`

References
==========

- `Search Log <https://fess.codelibs.org/stable/admin/searchlog-guide.html>`__
- `General Settings <https://fess.codelibs.org/stable/admin/general-guide.html>`__
- `Plugin <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__
- `System Requirements <https://fess.codelibs.org/stable/install/prerequisites.html>`__
- `Fess Discussion Forum <https://discuss.codelibs.org/c/FessEN/>`__
