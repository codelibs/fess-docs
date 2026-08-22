========================================
API compatible con Google Search Appliance
========================================

|Fess| también proporciona una API que devuelve los resultados de búsqueda en formato XML compatible con Google Search Appliance (GSA).
Para obtener información sobre el formato XML, consulte la \ `documentación oficial de GSA <https://www.google.com/support/enterprise/static/gsa/docs/admin/74/gsa_doc_set/xml_reference/results_format.html>`__\ .

Configuración
=============

Agregue ``web.api.gsa=true`` a system.properties para habilitar la API compatible con Google Search Appliance.

Solicitud
=========

Al enviar una solicitud como
``http://localhost:8080/gsa/?q=término de búsqueda``
a |Fess|, puede recibir los resultados de búsqueda en formato XML compatible con GSA.
Los valores que se pueden especificar como parámetros de solicitud son los mismos que en la \ `API de búsqueda de respuesta JSON <api-search.html>`__\ .
