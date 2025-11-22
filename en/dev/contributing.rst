========================
Contribution Guide
========================

We welcome contributions to the |Fess| project!
This page explains how to contribute to |Fess|, community guidelines,
and the process for creating pull requests.

.. contents:: Table of Contents
   :local:
   :depth: 2

Introduction
======

|Fess| is an open source project that grows through
community contributions.
Anyone can contribute regardless of programming experience level.

Ways to Contribute
========

There are various ways to contribute to |Fess|.

Code Contributions
----------

- Adding new features
- Bug fixes
- Performance improvements
- Refactoring
- Adding tests

Documentation Contributions
----------------

- Improving user manuals
- Adding/updating API documentation
- Creating tutorials
- Translations

Reporting Issues
-----------

- Bug reports
- Feature requests
- Questions and suggestions

Community Activities
--------------

- Discussions on GitHub Discussions
- Answering questions on forums
- Writing blog posts and tutorials
- Presenting at events

First Contribution
==========

If you are contributing to |Fess| for the first time, we recommend the following steps.

Step 1: Understand the Project
---------------------------

1. Check basic information on the `Fess Official Site <https://fess.codelibs.org/>`__
2. Understand the development overview in :doc:`getting-started`
3. Learn the code structure in :doc:`architecture`

Step 2: Find an Issue
-------------------

On the `GitHub Issues page <https://github.com/codelibs/fess/issues>`__,
look for issues labeled ``good first issue``.

These issues are relatively simple tasks suitable for first-time contributors.

Step 3: Set Up Development Environment
----------------------------

Follow :doc:`setup` to set up your development environment.

Step 4: Create a Branch and Work
----------------------------

Follow :doc:`workflow` to create a branch and start coding.

Step 5: Create Pull Request
--------------------------

Commit your changes and create a pull request.

Coding Conventions
==============

|Fess| follows these coding conventions to maintain
consistent code.

Java Coding Style
----------------------

Basic Style
~~~~~~~~~~

- **Indentation**: 4 spaces
- **Line endings**: LF (Unix style)
- **Encoding**: UTF-8
- **Line length**: 120 characters or less recommended

Naming Conventions
~~~~~~

- **Packages**: lowercase, dot-separated (e.g., ``org.codelibs.fess``)
- **Classes**: PascalCase (e.g., ``SearchService``)
- **Interfaces**: PascalCase (e.g., ``Crawler``)
- **Methods**: camelCase (e.g., ``executeSearch``)
- **Variables**: camelCase (e.g., ``searchResult``)
- **Constants**: UPPER_SNAKE_CASE (e.g., ``MAX_SEARCH_SIZE``)

Comments
~~~~~~

**Javadoc:**

Write Javadoc for public classes, methods, and fields.

.. code-block:: java

    /**
     * Executes a search.
     *
     * @param query search query
     * @return search results
     * @throws SearchException if search fails
     */
    public SearchResponse executeSearch(String query) throws SearchException {
        // implementation
    }

**Implementation comments:**

Add comments in Japanese or English for complex logic.

.. code-block:: java

    // Normalize query (convert full-width to half-width)
    String normalizedQuery = QueryNormalizer.normalize(query);

Class and Method Design
~~~~~~~~~~~~~~~~~~~~

- **Single Responsibility Principle**: One class has only one responsibility
- **Small methods**: One method does only one thing
- **Meaningful names**: Class and method names should clearly indicate intent

Exception Handling
~~~~~~

.. code-block:: java

    // Good example: Proper exception handling
    try {
        executeSearch(query);
    } catch (IOException e) {
        logger.error("Error occurred during search", e);
        throw new SearchException("Failed to execute search", e);
    }

    // Example to avoid: Empty catch block
    try {
        executeSearch(query);
    } catch (IOException e) {
        // Do nothing
    }

Handling null
~~~~~~~~~

- Avoid returning ``null`` when possible
- Recommend using ``Optional``
- Explicitly indicate null possibility with ``@Nullable`` annotation

.. code-block:: java

    // Good example
    public Optional<User> findUser(String id) {
        return Optional.ofNullable(userMap.get(id));
    }

    // Usage example
    findUser("123").ifPresent(user -> {
        // Process when user exists
    });

Writing Tests
~~~~~~~~~~

- Write tests for all public methods
- Test method names start with ``test``
- Use Given-When-Then pattern

.. code-block:: java

    @Test
    public void testSearch() {
        // Given: Test preconditions
        SearchService service = new SearchService();
        String query = "test";

        // When: Execute test target
        SearchResponse response = service.search(query);

        // Then: Verify results
        assertNotNull(response);
        assertEquals(10, response.getDocuments().size());
    }

Code Review Guidelines
========================

Pull Request Review Process
----------------------------

1. **Automated checks**: CI automatically runs builds and tests
2. **Code review**: Maintainers review the code
3. **Feedback**: Request modifications if necessary
4. **Approval**: Review is approved
5. **Merge**: Maintainers merge to main branch

Review Criteria
----------

Reviews check the following points:

**Functionality**

- Does it meet requirements
- Does it work as intended
- Are edge cases considered

**Code Quality**

- Follows coding conventions
- Readable and maintainable code
- Appropriate abstraction

**Tests**

- Sufficient tests written
- Tests pass
- Tests perform meaningful validation

**Performance**

- No negative performance impact
- Appropriate resource usage

**Security**

- No security issues
- Proper input validation

**Documentation**

- Necessary documentation updated
- Javadoc written appropriately

Responding to Review Comments
--------------------

Respond to review comments promptly and politely.

**When modifications are needed:**

.. code-block:: text

    Thank you for pointing that out. I've made the correction.
    [Brief description of the modification]

**When discussion is needed:**

.. code-block:: text

    Thank you for your feedback.
    I implemented it this way because of ○○,
    but would △△ implementation be better?

Pull Request Best Practices
================================

PR Size
---------

- Keep PRs small and easy to review
- Include one logical change per PR
- Split large changes into multiple PRs

PR Title
-----------

Use clear and descriptive titles:

.. code-block:: text

    feat: Add search result filtering feature
    fix: Fix crawler timeout issue
    docs: Update API documentation

PR Description
-------

Include the following information:

- **Changes**: What was changed
- **Reason**: Why this change is necessary
- **Testing method**: How it was tested
- **Screenshots**: For UI changes
- **Related Issue**: Issue number (e.g., Closes #123)

.. code-block:: markdown

    ## Changes
    Added a feature to filter search results by file type.

    ## Reason
    Many users requested the ability to "search only specific file types."

    ## Testing Method
    1. Select file type filter on search screen
    2. Execute search
    3. Verify that only results of selected file type are displayed

    ## Related Issue
    Closes #123

Commit Messages
----------------

Write clear and descriptive commit messages:

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**Example:**

.. code-block:: text

    feat: Add search filter feature

    Enabled users to filter search results by file type.

    - Added filter UI
    - Implemented backend filter processing
    - Added tests

    Closes #123

Using Draft PRs
--------------

Create work-in-progress PRs as Draft PRs,
then change to Ready for review when complete.

.. code-block:: text

    1. Select "Create draft pull request" when creating PR
    2. Click "Ready for review" when work is complete

Community Guidelines
======================

Code of Conduct
------

The |Fess| community follows these codes of conduct:

- **Be respectful**: Respect everyone
- **Be collaborative**: Provide constructive feedback
- **Be open**: Welcome different perspectives and experiences
- **Be polite**: Use courteous language

Communication
----------------

**Where to ask questions:**

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: General questions and discussions
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__: Bug reports and feature requests
- `Fess Forum <https://discuss.codelibs.org/c/FessEN>`__: Community forum

**How to ask questions:**

- Be specific
- Explain what you've tried
- Include error messages and logs
- Include environment information (OS, Java version, etc.)

**How to answer:**

- Be polite and kind
- Provide specific solutions
- Provide links to reference materials

Expressing Gratitude
--------

We express gratitude for contributions.
Even small contributions are valuable to the project.

Frequently Asked Questions
==========

Q: Can beginners contribute?
---------------------------

A: Yes, welcome! We recommend starting with issues labeled ``good first issue``.
Documentation improvements are also suitable contributions for beginners.

Q: How long does it take for pull requests to be reviewed?
-------------------------------------------------

A: Usually within a few days.
However, it may vary depending on maintainers' schedules.

Q: What if my pull request is rejected?
-----------------------------------

A: Check the reason for rejection and resubmit with modifications if needed.
Feel free to ask questions if you're unsure.

Q: What if I violate coding conventions?
---------------------------------------

A: It will be pointed out in the review, so you can fix it.
You can check in advance by running Checkstyle.

Q: What if I want to add a large feature?
-------------------------------

A: We recommend creating an Issue first to discuss the proposal.
Getting agreement in advance avoids wasted work.

Q: Can I ask questions in Japanese?
-------------------------------

A: Yes, both Japanese and English are fine.
Since Fess is a project from Japan, Japanese support is also comprehensive.

Type-Specific Contribution Guides
================

Documentation Improvements
----------------

1. Fork the documentation repository:

   .. code-block:: bash

       git clone https://github.com/codelibs/fess-docs.git

2. Make changes
3. Create pull request

Bug Reports
------

1. Search existing issues to check for duplicates
2. Create new issue
3. Include the following information:

   - Bug description
   - Reproduction steps
   - Expected behavior
   - Actual behavior
   - Environment information

Feature Requests
------------

1. Create issue
2. Explain:

   - Feature description
   - Background and motivation
   - Proposed implementation method (optional)

Code Reviews
------------

Reviewing other people's pull requests is also a contribution:

1. Find a PR you're interested in
2. Review the code
3. Provide constructive feedback

License
========

|Fess| is released under the Apache License 2.0.
Contributed code will also be subject to the same license.

By creating a pull request,
you are agreeing that your contribution will be released under this license.

Acknowledgments
====

Thank you for contributing to the |Fess| project!
Your contribution makes |Fess| better software.

Next Steps
==========

When you're ready to contribute:

1. Set up development environment with :doc:`setup`
2. Check development flow with :doc:`workflow`
3. Find issues on `GitHub <https://github.com/codelibs/fess>`__

References
======

- `GitHub Flow <https://docs.github.com/get-started/quickstart/github-flow>`__
- `How to Contribute to Open Source <https://opensource.guide/how-to-contribute/>`__
- `Writing Good Commit Messages <https://chris.beams.io/posts/git-commit/>`__

Community Resources
==================

- **GitHub**: `codelibs/fess <https://github.com/codelibs/fess>`__
- **Discussions**: `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- **Forum**: `Fess Forum <https://discuss.codelibs.org/c/FessEN>`__
- **Twitter**: `@codelibs <https://twitter.com/codelibs>`__
- **Website**: `fess.codelibs.org <https://fess.codelibs.org/>`__
