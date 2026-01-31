==================================
Git Connector
==================================

Overview
========

The Git Connector provides functionality to retrieve files from Git repositories
and register them in the |Fess| index.

This feature requires the ``fess-ds-git`` plugin.

Supported Repositories
======================

- GitHub (public/private)
- GitLab (public/private)
- Bitbucket (public/private)
- Local Git repositories
- Other Git hosting services

Prerequisites
=============

1. Plugin installation is required
2. Authentication credentials are required for private repositories
3. Read access to the repository is required

Plugin Installation
-------------------

Install from "System" -> "Plugins" in the admin console.

Or refer to :doc:`../../admin/plugin-guide` for details.

Configuration
=============

Configure from admin console via "Crawler" -> "Data Store" -> "Create New".

Basic Settings
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Item
     - Example
   * - Name
     - Project Git Repository
   * - Handler Name
     - GitDataStore
   * - Enabled
     - On

Parameter Settings
------------------

Public repository example:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Private repository example (with authentication):

::

    uri=https://username:personal_access_token@github.com/company/private-repo.git
    base_url=https://github.com/company/private-repo/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``uri``
     - Yes
     - Git repository URI (for cloning)
   * - ``base_url``
     - Yes
     - Base URL for file viewing
   * - ``extractors``
     - No
     - Extractor settings by MIME type
   * - ``prev_commit_id``
     - No
     - Previous commit ID (for incremental crawl)
   * - ``delete_old_docs``
     - No
     - Delete removed files from index (default: ``false``)

Script Settings
---------------

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    cache=""
    digest=author.toExternalString()
    anchor=
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

Available Fields
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``url``
     - File URL
   * - ``path``
     - File path within repository
   * - ``name``
     - File name
   * - ``content``
     - File text content
   * - ``contentLength``
     - Content length
   * - ``timestamp``
     - Last modified date
   * - ``mimetype``
     - File MIME type
   * - ``author``
     - Last committer information

Git Repository Authentication
=============================

GitHub Personal Access Token
----------------------------

1. Generate Personal Access Token on GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access https://github.com/settings/tokens:

1. Click "Generate new token" -> "Generate new token (classic)"
2. Enter token name (e.g., Fess Crawler)
3. Check "repo" in scopes
4. Click "Generate token"
5. Copy the generated token

2. Include authentication in URI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:YOUR_GITHUB_TOKEN@github.com/company/repo.git

GitLab Private Token
--------------------

1. Generate Access Token on GitLab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GitLab User Settings -> Access Tokens:

1. Enter token name
2. Check "read_repository" in scopes
3. Click "Create personal access token"
4. Copy the generated token

2. Include authentication in URI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:YOUR_GITLAB_TOKEN@gitlab.com/company/repo.git

SSH Authentication
------------------

When using SSH key:

::

    uri=git@github.com:company/repo.git

.. note::
   When using SSH authentication, the SSH key must be configured for the user running |Fess|.

Extractor Settings
==================

Extractors by MIME Type
-----------------------

Specify extractors by file type using ``extractors`` parameter:

::

    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,application/json:textExtractor,

Format: ``<MIME type regex>:<extractor name>,``

Default Extractors
~~~~~~~~~~~~~~~~~~

- ``textExtractor`` - For text files
- ``tikaExtractor`` - For binary files (PDF, Word, etc.)

Crawl Text Files Only
~~~~~~~~~~~~~~~~~~~~~

::

    extractors=text/.*:textExtractor,

Crawl All Files
~~~~~~~~~~~~~~~

::

    extractors=.*:tikaExtractor,

Specific File Types Only
~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Markdown, YAML, JSON only
    extractors=text/markdown:textExtractor,text/yaml:textExtractor,application/json:textExtractor,

Incremental Crawl
=================

Crawl Only Changes Since Last Commit
------------------------------------

After initial crawl, set ``prev_commit_id`` to the previous commit ID:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    prev_commit_id=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
    delete_old_docs=true

.. note::
   Set the commit ID to the one from the last crawl.
   This will only crawl changes since that commit.

Handling Deleted Files
----------------------

Setting ``delete_old_docs=true`` will remove files deleted from the Git repository
from the index as well.

Usage Examples
==============

GitHub Public Repository
------------------------

Parameters:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    delete_old_docs=false

Script:

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    last_modified=timestamp
    mimetype=mimetype

GitHub Private Repository
-------------------------

Parameters:

::

    uri=https://username:YOUR_GITHUB_TOKEN@github.com/company/repo.git
    base_url=https://github.com/company/repo/blob/main/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    delete_old_docs=false

Script:

::

    url=url
    title=name
    content=content
    digest=author.toExternalString()
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

GitLab (Self-Hosted)
--------------------

Parameters:

::

    uri=https://username:glpat-abc123@gitlab.company.com/team/project.git
    base_url=https://gitlab.company.com/team/project/-/blob/main/
    extractors=text/.*:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Script:

::

    url=url
    host="gitlab.company.com"
    site="gitlab.company.com/team/project/" + path
    title=name
    content=content
    last_modified=timestamp

Crawl Documentation Only (Markdown Files)
-----------------------------------------

Parameters:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/markdown:textExtractor,text/plain:textExtractor,
    delete_old_docs=false

Script:

::

    if (mimetype.startsWith("text/")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
    }

Crawl Specific Directory Only
-----------------------------

Filter in script:

::

    if (path.startsWith("docs/") || path.startsWith("README")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
        mimetype=mimetype
    }

Troubleshooting
===============

Authentication Error
--------------------

**Symptom**: ``Authentication failed`` or ``Not authorized``

**Check**:

1. Verify Personal Access Token is correct
2. Verify token has appropriate permissions (``repo`` scope)
3. Verify URI format is correct:

   ::

       # Correct
       uri=https://username:token@github.com/company/repo.git

       # Wrong
       uri=https://github.com/company/repo.git?token=...

4. Verify token has not expired

Repository Not Found
--------------------

**Symptom**: ``Repository not found``

**Check**:

1. Verify repository URL is correct
2. Verify repository exists and is not deleted
3. Verify authentication credentials are correct
4. Verify access permissions to repository

Files Not Retrieved
-------------------

**Symptom**: Crawl succeeds but 0 files

**Check**:

1. Verify ``extractors`` setting is appropriate
2. Verify repository contains files
3. Verify script settings are correct
4. Verify files exist on target branch

MIME Type Error
---------------

**Symptom**: Certain files are not crawled

**Solution**:

Adjust extractor settings:

::

    # Target all files
    extractors=.*:tikaExtractor,

    # Add specific MIME types
    extractors=text/.*:textExtractor,application/json:textExtractor,application/xml:textExtractor,

Large Repositories
------------------

**Symptom**: Crawl takes long time or runs out of memory

**Solution**:

1. Limit target files with ``extractors``
2. Filter specific directories in script
3. Use incremental crawl (``prev_commit_id`` setting)
4. Adjust crawl interval

Specifying Branch
-----------------

To crawl a branch other than default:

::

    uri=https://github.com/company/repo.git#develop
    base_url=https://github.com/company/repo/blob/develop/

Specify branch name after ``#``.

URL Generation
==============

base_url Setting Patterns
-------------------------

**GitHub**:

::

    base_url=https://github.com/user/repo/blob/master/

**GitLab**:

::

    base_url=https://gitlab.com/user/repo/-/blob/main/

**Bitbucket**:

::

    base_url=https://bitbucket.org/user/repo/src/master/

URLs are generated by combining ``base_url`` with the file path.

URL Generation in Script
------------------------

::

    url=base_url + path
    title=name
    content=content

Or custom URL:

::

    url="https://github.com/mycompany/repo/blob/main/" + path
    title=name
    content=content

Reference
=========

- :doc:`ds-overview` - DataStore Connector Overview
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `GitHub Personal Access Tokens <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_
- `GitLab Personal Access Tokens <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_

