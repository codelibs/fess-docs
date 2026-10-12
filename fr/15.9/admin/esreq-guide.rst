======================
Requête à OpenSearch
======================

Présentation
============

Cette page envoie à OpenSearch une requête écrite dans un fichier JSON.

|image0|

Cette page ne figure pas dans le menu.
Pour l'afficher, connectez-vous en tant qu'administrateur et saisissez ``/admin/sereq/`` comme chemin d'URL.
Le rôle ``admin`` (administrateurs) ou le rôle ``admin-sereq`` est nécessaire pour envoyer une requête.

Méthode d'opération
===================

Envoi de requête
----------------

Créez sous forme de fichier JSON la requête que vous souhaitez envoyer à OpenSearch, sélectionnez ce fichier comme « Fichier de requête », puis cliquez sur le bouton « Envoyer » pour envoyer la requête à OpenSearch.
La réponse est téléchargée sous forme de fichier.

Paramètres de configuration
---------------------------

Fichier de requête
::::::::::::::::::

Spécifiez le fichier qui contient la requête.

Écrivez sur la première ligne ``<méthode> <chemin>``, séparés par un seul espace, puis le corps de la requête (par exemple un DSL de requête) sur les lignes suivantes.
La méthode peut être GET, POST, PUT ou DELETE. Le chemin est le chemin sur OpenSearch ; le ``/`` initial peut être omis.
Par exemple, le contenu du fichier serait comme suit.

::

    POST /_search
    {
      "query": {
        "match_all": {}
      }
    }

Les sauts de ligne du corps sont supprimés et les lignes sont concaténées avant l'envoi. Une requête dont le corps contient un document JSON par ligne, comme ``_bulk``, ne peut donc pas être envoyée.

.. warning::

   Une requête dont la méthode est PUT ou DELETE est également envoyée telle quelle à OpenSearch.
   Selon le contenu du fichier, elle peut modifier ou supprimer les index utilisés par |Fess| et entraîner une perte de données. Vérifiez soigneusement le contenu avant l'envoi.

.. |image0| image:: ../../../resources/images/en/15.9/admin/esreq-1.png
