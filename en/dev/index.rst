====================================
Open Source Full-Text Search Server - |Fess| Development Guide
====================================

This guide provides the information needed to participate in |Fess| development.
It is intended for a wide range of people, from those tackling |Fess| development for the first time to experienced developers.

.. contents:: Table of Contents
   :local:
   :depth: 2

Target Audience
========

This guide is intended for:

- Developers who want to contribute features and improvements to |Fess|
- Engineers who want to understand the |Fess| codebase
- Those who want to customize and use |Fess|
- Those interested in participating in open source projects

Required Prerequisites
============

To participate in |Fess| development, the following knowledge will be helpful:

**Required**

- Basic Java programming knowledge (Java 21 or later)
- Basic usage of Git and GitHub
- Basic usage of Maven

**Recommended**

- Knowledge of the LastaFlute framework
- Knowledge of DBFlute
- Knowledge of OpenSearch/Elasticsearch
- Experience with web application development

Development Guide Structure
==============

This guide consists of the following sections.

:doc:`getting-started`
    Explains the overview of |Fess| development and the first steps to start developing.
    You can understand the technology stack required for development and the overall project structure.

:doc:`setup`
    Provides detailed instructions on setting up the development environment.
    It covers everything from installing necessary tools like Java, IDE, and OpenSearch
    to obtaining and running the |Fess| source code, with step-by-step explanations.

:doc:`architecture`
    Explains the architecture and code structure of |Fess|.
    By understanding the main packages, modules, and design patterns,
    you can develop more efficiently.

:doc:`workflow`
    Explains the standard workflow for |Fess| development.
    You can learn how to proceed with development work such as feature additions,
    bug fixes, code reviews, and testing.

:doc:`building`
    Explains how to build and test |Fess|.
    It covers the usage of build tools, running unit tests,
    and creating distribution packages.

:doc:`contributing`
    Explains how to contribute to the |Fess| project.
    You can learn about creating pull requests, coding conventions,
    and how to communicate with the community.

Quick Start
==============

If you want to start developing |Fess| right away, follow these steps:

1. **Check System Requirements**

   The following tools are required for development:

   - Java 21 or later
   - Maven 3.x or later
   - Git
   - IDE (Eclipse, IntelliJ IDEA, etc.)

2. **Get Source Code**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

3. **Download OpenSearch Plugins**

   .. code-block:: bash

       mvn antrun:run

4. **Run**

   Run ``org.codelibs.fess.FessBoot`` from your IDE,
   or run it from Maven:

   .. code-block:: bash

       mvn compile exec:java

For details, see :doc:`setup`.

Development Environment Options
==============

|Fess| development can be done in any of the following environments:

Local Development Environment
--------------

This is the most common development environment. Install development tools on your machine
and develop using an IDE.

**Advantages:**

- Fast builds and execution
- Full use of IDE features
- Can work offline

**Disadvantages:**

- Initial setup takes time
- Problems may occur due to environment differences

Docker-Based Development Environment
------------------------

You can build a consistent development environment using Docker containers.

**Advantages:**

- Environment consistency is maintained
- Easy setup
- Easy to return to clean state

**Disadvantages:**

- Docker knowledge required
- Performance may be slightly degraded

For details, see :doc:`setup`.

Frequently Asked Questions
==========

Q: What are the minimum specifications required for development?
--------------------------------

A: We recommend the following:

- CPU: 4 cores or more
- Memory: 8GB or more
- Disk: 20GB or more of free space

Q: Which IDE should I use?
---------------------------------

A: You can use any IDE you prefer, such as Eclipse, IntelliJ IDEA, or VS Code.
This guide primarily uses Eclipse for examples,
but you can develop similarly with other IDEs.

Q: Is knowledge of LastaFlute and DBFlute required?
------------------------------------------

A: While not mandatory, having it will make development smoother.
Basic usage is explained in this guide,
but please refer to the official documentation of each framework for details.

Q: What should I start with for my first contribution?
------------------------------------------------------

A: We recommend starting with relatively simple tasks such as:

- Documentation improvements
- Adding tests
- Bug fixes
- Small improvements to existing features

For details, see :doc:`contributing`.

Related Resources
==========

Official Resources
----------

- `Fess Official Site <https://fess.codelibs.org/>`__
- `GitHub Repository <https://github.com/codelibs/fess>`__
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__

Technical Documentation
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

Community
----------

- `Fess Community Forum <https://discuss.codelibs.org/c/FessEN>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__

Next Steps
==========

To start developing, we recommend reading :doc:`getting-started` first.

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents:

   getting-started
   setup
   architecture
   workflow
   building
   contributing
