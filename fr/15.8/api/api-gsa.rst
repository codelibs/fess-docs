===================================
API compatible Google Search Appliance
===================================

|Fess| fournit également une API qui retourne les résultats de recherche dans un format XML compatible avec Google Search Appliance (GSA).
Pour plus d'informations sur le format XML, veuillez consulter la `documentation officielle de GSA <https://www.google.com/support/enterprise/static/gsa/docs/admin/74/gsa_doc_set/xml_reference/results_format.html>`__\ .

Configuration
=============

Ajoutez ``web.api.gsa=true`` à system.properties pour activer l'API compatible Google Search Appliance.

Requête
=======

En envoyant à |Fess| une requête de type
``http://localhost:8080/gsa/?q=mot_recherche``,
vous pouvez recevoir les résultats de recherche au format XML compatible GSA.
Les valeurs pouvant être spécifiées comme paramètres de requête sont les mêmes que celles de l'`API de recherche avec réponse JSON <api-search.html>`__\ .
