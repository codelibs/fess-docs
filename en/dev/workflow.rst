==============
Development Workflow
==============

This page explains the standard workflow for |Fess| development.
You can learn how to proceed with development work, including
feature additions, bug fixes, testing, and code reviews.

.. contents:: Table of Contents
   :local:
   :depth: 2

Basic Development Flow
==============

|Fess| development follows this process:

.. code-block:: text

    1. Check/Create Issue
       ↓
    2. Create Branch
       ↓
    3. Coding
       ↓
    4. Run Local Tests
       ↓
    5. Commit
       ↓
    6. Push
       ↓
    7. Create Pull Request
       ↓
    8. Code Review
       ↓
    9. Address Review Feedback
       ↓
    10. Merge

Each step is explained in detail below.

Step 1: Check/Create Issue
=========================

Before starting development, check GitHub Issues.

Checking Existing Issues
-----------------

1. Visit the `Fess Issues page <https://github.com/codelibs/fess/issues>`__
2. Find an Issue you want to work on
3. Comment on the Issue to indicate you're starting work

.. tip::

   For first-time contributions, we recommend starting with Issues labeled ``good first issue``.

Creating a New Issue
-----------------

For new features or bug fixes, create an Issue.

1. Click `New Issue <https://github.com/codelibs/fess/issues/new>`__
2. Select an Issue template
3. Fill in the required information:

   - **Title**: Concise and clear description
   - **Description**: Detailed background, expected behavior, current behavior
   - **Reproduction steps**: For bugs
   - **Environment information**: OS, Java version, Fess version, etc.

4. Click ``Submit new issue``

Issue Templates
~~~~~~~~~~~~~~~~~~

**Bug Report:**

.. code-block:: markdown

    ## Problem Description
    Brief description of the bug

    ## Reproduction Steps
    1. ...
    2. ...
    3. ...

    ## Expected Behavior
    What should happen

    ## Actual Behavior
    What is currently happening

    ## Environment
    - OS:
    - Java version:
    - Fess version:

**Feature Request:**

.. code-block:: markdown

    ## Feature Description
    Description of the feature to add

    ## Background and Motivation
    Why this feature is needed

    ## Proposed Implementation
    How to implement it (optional)

Step 2: Create Branch
====================

Create a working branch.

Branch Naming Convention
--------------

Branch names follow this format:

.. code-block:: text

    <type>/<issue-number>-<short-description>

**Types:**

- ``feature``: Adding new features
- ``fix``: Bug fixes
- ``refactor``: Refactoring
- ``docs``: Documentation updates
- ``test``: Adding/modifying tests

**Examples:**

.. code-block:: bash

    # Adding a new feature
    git checkout -b feature/123-add-search-filter

    # Bug fix
    git checkout -b fix/456-fix-crawler-timeout

    # Documentation update
    git checkout -b docs/789-update-api-docs

Branch Creation Steps
----------------

1. Get the latest main branch:

   .. code-block:: bash

       git checkout main
       git pull origin main

2. Create a new branch:

   .. code-block:: bash

       git checkout -b feature/123-add-search-filter

3. Verify the branch was created:

   .. code-block:: bash

       git branch

Step 3: Coding
==================

Implement features or fix bugs.

Coding Conventions
--------------

|Fess| follows these coding conventions.

Basic Style
~~~~~~~~~~~~~~

- **Indentation**: 4 spaces
- **Line length**: 120 characters or less recommended
- **Encoding**: UTF-8
- **Line endings**: LF (Unix style)

Naming Conventions
~~~~~~

- **Class names**: PascalCase (e.g., ``SearchService``)
- **Method names**: camelCase (e.g., ``executeSearch``)
- **Constants**: UPPER_SNAKE_CASE (e.g., ``MAX_SEARCH_SIZE``)
- **Variables**: camelCase (e.g., ``searchResults``)

Comments
~~~~~~

- **Javadoc**: Required for public classes and methods
- **Implementation comments**: Add explanations in Japanese or English for complex logic

**Example:**

.. code-block:: java

    /**
     * Executes a search.
     *
     * @param query search query
     * @return search results
     */
    public SearchResponse executeSearch(String query) {
        // Normalize query
        String normalizedQuery = normalizeQuery(query);

        // Execute search
        return searchEngine.search(normalizedQuery);
    }

Handling null
~~~~~~~~~

- Avoid returning ``null`` when possible
- Recommend using ``Optional``
- Explicitly check for ``null``

**Example:**

.. code-block:: java

    // Good example
    public Optional<User> findUser(String id) {
        return userRepository.findById(id);
    }

    // Example to avoid
    public User findUser(String id) {
        return userRepository.findById(id);  // Possibility of null
    }

Exception Handling
~~~~~~

- Properly catch and handle exceptions
- Output logs
- Provide user-friendly messages

**Example:**

.. code-block:: java

    try {
        // Processing
    } catch (IOException e) {
        logger.error("File read error", e);
        throw new FessSystemException("Failed to read file", e);
    }

Logging
~~~~~~

Use appropriate log levels:

- ``ERROR``: When errors occur
- ``WARN``: Situations that should be warned about
- ``INFO``: Important information
- ``DEBUG``: Debug information
- ``TRACE``: Detailed trace information

**Example:**

.. code-block:: java

    if (logger.isDebugEnabled()) {
        logger.debug("Search query: {}", query);
    }

Testing During Development
------------

During development, test using the following methods:

Local Execution
~~~~~~~~~~

Run Fess in IDE or command line to verify behavior:

.. code-block:: bash

    mvn compile exec:java

Debug Execution
~~~~~~~~~~

Use IDE debugger to trace code execution.

Running Unit Tests
~~~~~~~~~~~~~~

Run tests related to your changes:

.. code-block:: bash

    # Run specific test class
    mvn test -Dtest=SearchServiceTest

    # Run all tests
    mvn test

See :doc:`building` for details.

Step 4: Run Local Tests
=========================

Always run tests before committing.

Running Unit Tests
--------------

.. code-block:: bash

    mvn test

Running Integration Tests
--------------

.. code-block:: bash

    mvn verify

Code Style Checks
--------------------

.. code-block:: bash

    mvn checkstyle:check

Running All Checks
-------------------

.. code-block:: bash

    mvn clean verify

Step 5: Commit
==============

Commit your changes.

Commit Message Convention
--------------------

Commit messages follow this format:

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**Types:**

- ``feat``: New feature
- ``fix``: Bug fix
- ``docs``: Documentation only changes
- ``style``: Changes that don't affect code meaning (formatting, etc.)
- ``refactor``: Refactoring
- ``test``: Adding/modifying tests
- ``chore``: Changes to build process or tools

**Example:**

.. code-block:: text

    feat: Add search filter functionality

    Added ability for users to filter search results by file type.

    Fixes #123

Commit Steps
----------

1. Stage changes:

   .. code-block:: bash

       git add .

2. Commit:

   .. code-block:: bash

       git commit -m "feat: Add search filter functionality"

3. Verify commit history:

   .. code-block:: bash

       git log --oneline

Commit Granularity
------------

- Include one logical change per commit
- Split large changes into multiple commits
- Make commit messages clear and specific

Step 6: Push
==============

Push your branch to the remote repository.

.. code-block:: bash

    git push origin feature/123-add-search-filter

For initial push:

.. code-block:: bash

    git push -u origin feature/123-add-search-filter

Step 7: Create Pull Request
=========================

Create a Pull Request (PR) on GitHub.

PR Creation Steps
-----------

1. Visit the `Fess repository <https://github.com/codelibs/fess>`__
2. Click the ``Pull requests`` tab
3. Click ``New pull request``
4. Select base branch (``main``) and compare branch (your working branch)
5. Click ``Create pull request``
6. Fill in PR content (follow the template)
7. Click ``Create pull request``

PR Template
---------------

.. code-block:: markdown

    ## Changes
    What was changed in this PR

    ## Related Issue
    Closes #123

    ## Type of Change
    - [ ] New feature
    - [ ] Bug fix
    - [ ] Refactoring
    - [ ] Documentation update
    - [ ] Other

    ## Testing Method
    How this change was tested

    ## Checklist
    - [ ] Code works
    - [ ] Tests added
    - [ ] Documentation updated
    - [ ] Follows coding conventions

PR Description
-------

Include the following in the PR description:

- **Purpose of change**: Why this change is needed
- **Content of change**: What was changed
- **Testing method**: How it was tested
- **Screenshots**: For UI changes

Step 8: Code Review
====================

Maintainers will review the code.

Review Aspects
------------

The review checks the following:

- Code quality
- Compliance with coding conventions
- Test coverage
- Performance impact
- Security issues
- Documentation updates

Review Comment Examples
------------------

**Approval:**

.. code-block:: text

    LGTM (Looks Good To Me)

**Modification request:**

.. code-block:: text

    Doesn't this need a null check here?

**Suggestion:**

.. code-block:: text

    This process might be better moved to a Helper class.

Step 9: Address Review Feedback
===================================

Respond to review comments.

Feedback Response Steps
----------------------

1. Read review comments
2. Make necessary modifications
3. Commit changes:

   .. code-block:: bash

       git add .
       git commit -m "fix: Address review comments"

4. Push:

   .. code-block:: bash

       git push origin feature/123-add-search-filter

5. Reply to comments on PR page

Replying to Comments
--------------

Always reply to review comments:

.. code-block:: text

    Fixed. Please review.

Or:

.. code-block:: text

    Thank you for the feedback.
    I kept the current implementation for XX reason, how does that sound?

Step 10: Merge
=============

Once the review is approved, a maintainer will merge the PR.

Post-Merge Actions
------------

1. Update local main branch:

   .. code-block:: bash

       git checkout main
       git pull origin main

2. Delete working branch:

   .. code-block:: bash

       git branch -d feature/123-add-search-filter

3. Delete remote branch (if not auto-deleted on GitHub):

   .. code-block:: bash

       git push origin --delete feature/123-add-search-filter

Common Development Scenarios
==================

Adding Features
------

1. Create an Issue (or check existing Issue)
2. Create branch: ``feature/xxx-description``
3. Implement feature
4. Add tests
5. Update documentation
6. Create PR

Bug Fixes
------

1. Check bug report Issue
2. Create branch: ``fix/xxx-description``
3. Add test that reproduces the bug
4. Fix the bug
5. Verify tests pass
6. Create PR

Refactoring
--------------

1. Create an Issue (explain reason for refactoring)
2. Create branch: ``refactor/xxx-description``
3. Execute refactoring
4. Verify existing tests pass
5. Create PR

Documentation Updates
--------------

1. Create branch: ``docs/xxx-description``
2. Update documentation
3. Create PR

Development Tips
==========

Efficient Development
----------

- **Small commits**: Commit frequently
- **Early feedback**: Utilize Draft PRs
- **Test automation**: Leverage CI/CD
- **Code review**: Review others' code too

Problem Solving
--------

When stuck, use the following:

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__
- GitHub Issue comments

Next Steps
==========

After understanding the workflow, also refer to the following documents:

- :doc:`building` - Build and test details
- :doc:`contributing` - Contribution guidelines
- :doc:`architecture` - Understanding the codebase

References
======

- `GitHub Flow <https://docs.github.com/en/get-started/quickstart/github-flow>`__
- `Commit Message Guidelines <https://chris.beams.io/posts/git-commit/>`__
- `Code Review Best Practices <https://google.github.io/eng-practices/review/>`__
