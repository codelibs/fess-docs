====================================
Google Search Appliance-kompatible API
====================================

|Fess| bietet auch eine API, die Suchergebnisse im Google Search Appliance (GSA)-kompatiblen XML-Format zurückgibt.
Informationen zum XML-Format finden Sie in der \ `offiziellen GSA-Dokumentation <https://www.google.com/support/enterprise/static/gsa/docs/admin/74/gsa_doc_set/xml_reference/results_format.html>`__\ .

Konfiguration
=============

Fügen Sie ``web.api.gsa=true`` zu system.properties hinzu, um die Google Search Appliance-kompatible API zu aktivieren.

Anfrage
=======

Durch Senden einer Anfrage wie
``http://localhost:8080/gsa/?q=Suchbegriff``
an |Fess| können Sie Suchergebnisse im GSA-kompatiblen XML-Format erhalten.
Die als Anfrageparameter angebbaren Werte sind die gleichen wie bei der \ `Such-API mit JSON-Antwort <api-search.html>`__\ .
