=============================================
Part 4: Natural Language Processing with Fess
=============================================

Last time, we used Fess as a web scraping server to gather information from the site.
This time, we will introduce natural language processing using Python with the information collected by Fess.
A Python environment is required, so please prepare a Python 3 environment in advance.

Natural Language Processing
===========================

Natural language processing (NLP) is a set of technologies for processing languages spoken and written using computers.
It includes various fields such as parsing and machine translation.
This time, we will focus on word segmentation, including morphological analysis, and document classification.

Fess uses Elasticsearch as a search engine, and Elasticsearch includes a word splitter through the Analyzer provided by Apache Lucene.
The Analyzer can be customized in various settings.
By using this function, it is possible to realize morphological analysis and word segmentation for Japanese and other languages.
If you can use the Analyzer, you can leverage it for text analysis and machine learning.

Elasticsearch provides the `Analyze API <https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-analyze.html>`__ to access the Analyzer via an API.
Building an Elasticsearch environment just to use the Analyze API can be challenging.
Therefore, we will use the Python package `Esanpy <https://github.com/codelibs/esanpy>`__, which makes it easy to use.
Esanpy internally launches Elasticsearch with a minimal configuration and can be used without interfering with existing Elasticsearch instances that store data.

Esanpy
======

Esanpy is an Elasticsearch-based text analysis package.
With Esanpy, you can use the Analyzer function of Elasticsearch directly.
You can install it with the following command:

.. code-block:: bash

   $ pip install esanpy

To use it, import esanpy and pass the Analyzer name and text to esanpy.analyzer(), which will return an array of words.

.. code-block:: bash

   $ python
   >>> import esanpy
   >>> esanpy.start_server()
   >>> esanpy.analyzer("今日の天気は晴れです。", analyzer="kuromoji")
   ['今日', '天気', '晴れ']

esanpy.start_server() launches Elasticsearch for text analysis in the background, so you need to run it once before using esanpy.analyzer().
When the series of processes is completed and the word segmentation process is no longer needed, execute esanpy.stop_server() to stop it.

If you are running an Elasticsearch environment that stores search data, you can use that Elasticsearch for word segmentation with the Analyze API.
However, in my experience, it is easier to use it separately from Elasticsearch used for data storage, like Esanpy, when it is used as an API for text analysis.
We used to operate Elasticsearch for both data storage and text analysis, but we struggled with upgrades.
In that regard, Esanpy is easy to deploy and operate.

Document Classification
=======================

Let's create a text classification model using the IT Search + commentary/example articles obtained last time.
If you pass the body of the article (article_body) to this model, it will consider the content and predict the category information (article_category).
The flow of creating a model is as follows:

1. Get data stored in Fess.
2. Split the text of the acquired data into words.
3. Vectorize the string data.
4. Create a text classification model.
5. Predict any text with the text classification model.

This document does not discuss the evaluation of prediction results or parameter tuning, so please refer to the scikit-learn documentation if necessary.

First, install the required Python packages.

.. code-block:: bash

   $ pip install elasticsearch
   $ pip install numpy
   $ pip install scipy
   $ pip install scikit-learn

Put the following code in a .py file and execute it in order.
First, import the Python modules used this time.

.. code-block:: python

   from elasticsearch.client import Elasticsearch
   import esanpy
   from sklearn.feature_extraction.text import TfidfVectorizer
   from sklearn.preprocessing import LabelEncoder
   from sklearn.ensemble import RandomForestClassifier

First, use the Python Elasticsearch module to get the data stored in Fess.
Since this time the data is stored in article_category and article_body, only that data is extracted to generate a dictionary array.
If you want to use Fess data for another purpose, you can customize it by referring to this code.

.. code-block:: python

   def load_docs(doc_fields,
                 es_host='localhost:9201',
                 fess_index='fess.search',
                 search_query={"query": {"match_all": {}}}):
       es = Elasticsearch(es_host)
       response = None
       running = True
       docs = []
       # Fetch all items that match search_query by scroll search
       while running:
           if response is None:
               response = es.search(index=fess_index,
                                    scroll='5m',
                                    size=100,
                                    body=search_query)
           else:
               response = es.scroll(scroll_id=scroll_id,
                                    scroll='5m',
                                    params={"request_timeout": 60})
           if len(response['hits']['hits']) == 0:
               running = False
               break
           scroll_id = response['_scroll_id']
           for hit in response['hits']['hits']:
               if '_source' in hit:
                   docs.append({f: hit.get('_source').get(f) for f in doc_fields})
       return docs

   dataset = load_docs(['article_category', 'article_body'])
   # dataset = [{'article_category': '...', 'article_body': '...'}, ...]

Next, the text is split into words and vectorized to create a classification model.
Word segmentation of Japanese text is performed by morphological analysis with kuromoji using Esanpy.
In vectorization, scikit-learn's TfidfVectorizer converts the document group of article_body to a TFIDF matrix X, and the predicted category information article_category is digitized by LabelEncoder and converted to an integer array.
X is used as an explanatory variable and y as an objective variable when creating a classification model.

.. code-block:: python

   # Start Esanpy
   esanpy.start_server()
   
   # Make the Analyzer used in TfidfVectorizer a function
   def ja_analyzer(t):
       return esanpy.analyzer(t, analyzer='kuromoji')
   
   vectorizer = TfidfVectorizer(analyzer=ja_analyzer)
   corpus = [x.get('article_body') for x in dataset]
   X = vectorizer.fit_transform(corpus)  # Matrix of explanatory variables
   
   encoder = LabelEncoder()
   y = encoder.fit_transform([x.get('article_category') for x in dataset])  # Array of objective variables

Create a classification model using X and y.
This time, we use scikit-learn's random forest as a method to create a classification model.
scikit-learn has various implementation methods, and the interface is unified.
Fit to learn, predict to predict.
After learning with fit, you can predict the category of the text by passing any text to the random forest classifier clf.

.. code-block:: python

   clf = RandomForestClassifier()
   clf.fit(X, y)  # Learning

   text = 'マウスコンピューターは6月20日、AMDのハイエンドCPU「AMD Ryzen 7 1700X」を搭載したデスクトップPC「LM-AG350XN1-SH5」を発売した。'
   preds = clf.predict(vectorizer.transform([text]))  # Prediction
   print('category: %s' % encoder.inverse_transform(preds))

By executing the above code, you can predict the category of the document passed by text as follows:

.. code-block:: python

   category: ['ソリューション']

(Because the document to be learned changes depending on the crawling time, the prediction result may be other than "solution")

Summary
=======

This time, we introduced document classification as natural language processing using data collected by Fess.
Although not included in this document, if you use `gensim <https://radimrehurek.com/gensim/>`__, you can also generate Word2Vec, Doc2Vec, etc., from the data collected by Fess.
There are many packages in Python.
By combining them, you can use Fess for natural language processing and machine learning.

Next time, we will take a closer look at Analyzer, an important feature of the search system.

