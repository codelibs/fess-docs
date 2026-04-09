============================================================
Part 21: Cross-Searching Images and Text -- Next-Generation Knowledge Management with Multimodal Search
============================================================

Introduction
============

In the previous articles, we have primarily focused on searching text-based documents.
However, enterprise knowledge includes a great deal of content beyond text.
Product photos, engineering drawings, presentation slide images, whiteboard photos -- if these "images" could also be searched, the possibilities for knowledge utilization would expand significantly.

In this article, we introduce how to build a multimodal search environment that enables cross-searching of text and images.

Target Audience
===============

- Those who face challenges in searching documents that contain images
- Those interested in applications of vector search
- Those who want to understand the concept of multimodal AI

What Is Multimodal Search?
============================

Multimodal search is a technology that enables cross-searching across different types of data (text, images, audio, etc.).

For example, when you search with the text "red sports car design," images that conceptually match are displayed in the search results.
It is a mechanism that allows searching for images from text, or text from images.

CLIP Model
-----------

The foundation of multimodal search is models such as CLIP (Contrastive Language-Image Pre-Training).
CLIP converts text and images into the same vector space, making it possible to calculate the similarity between text and images.

Multimodal Search in Fess
=============================

Fess can achieve cross-searching of text and images through its multimodal search plugin.

Components
----------

The components of multimodal search are as follows:

1. **CLIP Server**: Converts text and images into vectors
2. **OpenSearch**: Searches vectors using KNN (K-Nearest Neighbor)
3. **Fess**: Provides crawling, indexing, and search UI

Setup Procedure
----------------

**1. Preparing the CLIP Server**

Prepare a server to run the CLIP model.
An environment with GPU availability is recommended.

You can add a CLIP server using Docker Compose.

**2. Installing the Plugin**

Install the multimodal search plugin for Fess.

**3. Configuring the KNN Index**

Configure the KNN index settings to perform vector search in OpenSearch.
Set the vector dimensions to match the CLIP model you are using.

**4. Crawl Settings**

Configure directories and websites containing images as crawl targets.
Image files (PNG, JPEG, GIF, etc.) are also collected as crawl targets.

Search Experience
==================

Searching for Images with Text
--------------------------------

When you search with text such as "product exterior photo," "meeting whiteboard," or "engineering drawing," images that conceptually match are displayed in the search results.

Thumbnail images are shown in the search results, allowing you to visually find the desired images.

Mixed Results of Text and Images
----------------------------------

In multimodal search, search results containing a mix of text documents and images are returned.
Rank Fusion (see Part 18) is used to integrate the results of text search and image search.

Use Cases
==========

Manufacturing: Searching for Parts and Product Images
-------------------------------------------------------

In manufacturing, vast numbers of parts photos and product images are managed.
By searching with text such as "round metal part" or by searching for similar parts from a photo of a particular part, past design assets can be leveraged.

Design Teams: Managing Design Assets
---------------------------------------

Design teams manage large volumes of visual assets such as logos, icons, photo materials, and mockups.
Because you can search with natural language such as "blue gradient background," asset discovery becomes easier.

Research and Development: Searching Experimental Data
-------------------------------------------------------

R&D departments manage graphs of experimental results, microscope photos, and images of measurement data.
By making these images searchable, referencing past experimental data becomes easier.

Considerations for Deployment
===============================

Hardware Requirements
----------------------

Multimodal search requires computational resources to run the CLIP model.

- **Recommended**: GPU server (NVIDIA GPU)
- **Minimum**: Can run on CPU, but indexing speed will be reduced

Indexing time depends on model processing speed, so a GPU environment is strongly recommended when indexing a large number of images.

Supported Image Formats
------------------------

Common image formats (JPEG, PNG, GIF, BMP, TIFF, etc.) are supported.
Support for images within PDFs and embedded images within office documents depends on crawl settings.

Phased Deployment
------------------

Multimodal search can be deployed as an addition to an existing text search environment.

1. First, conduct a trial deployment targeting directories and sites with many images
2. Verify search quality and usage
3. Gradually expand the scope

Summary
========

In this article, we introduced cross-searching of images and text using multimodal search.

- The concept of multimodal search (unified vector space for text and images via CLIP)
- Components and configuration of multimodal search in Fess
- The experience of searching for images with text, and searching for similar images with images
- Use cases in manufacturing, design, and research and development
- GPU requirements and a phased deployment approach

In the next article, we will cover knowledge visualization in organizations through search data analysis.

References
==========

- `OpenSearch KNN Search <https://opensearch.org/docs/latest/search-plugins/knn/>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
