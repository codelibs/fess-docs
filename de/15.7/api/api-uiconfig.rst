=====================
UI-Konfigurations-API
=====================

Übersicht
=========

Die UI-Konfigurations-API gibt die Anfangskonfiguration zurück, die eine Single-Page-Anwendung (SPA) benötigt (Theme, Feature-Flags, Paginierungslimits sowie, wenn CSRF erforderlich ist, ein neues CSRF-Token).
Dieser Endpunkt wird anonym vor der Anmeldung aufgerufen.

Informationen zum gemeinsamen Antwort-Envelope und zum Fehlermodell finden Sie unter :doc:`api-overview`.

UI-Konfiguration abrufen
========================

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/ui/config``
==================  ====================================================

Gibt die von der SPA benötigte Anfangskonfiguration zurück.

Antwort
-------

Bei Erfolg (HTTP 200, UiConfigResponse) wird eine Antwort im gemeinsamen Envelope-Format zurückgegeben (Auszug):

.. code-block:: json

    {
      "response": {
        "status": 0,
        "site_name": "Fess",
        "login_required": false,
        "locales": ["en", "ja"],
        "theme": {
          "name": "default",
          "display_name": "Default Theme",
          "version": "1.0.0",
          "supported_locales": ["en", "ja"]
        },
        "features": {
          "user_favorite": false,
          "popular_word": true,
          "suggest_search_log": true,
          "suggest_documents": true,
          "login_required": false,
          "eoled": false,
          "development_mode": false,
          "search_log_enabled": true,
          "thumbnail_enabled": true,
          "display_label_type": false,
          "clipboard_copy_icon": true,
          "eol_link": "",
          "installation_link": "https://fess.codelibs.org/15.7/install/",
          "login_link": true,
          "rag_chat_enabled": false
        },
        "page_size_default": 20,
        "page_size_max": 100,
        "sort_options": [
          {"value": "", "label_key": "labels.search_result_sort_score_desc"}
        ],
        "num_options": [10, 20, 30, 40, 50, 100],
        "lang_options": [
          {"value": "all", "label_key": "labels.searchoptions_all_langs"},
          {"value": "ja", "label_key": "labels.lang_ja"}
        ],
        "label_options": [],
        "notifications": {
          "search_top": "",
          "advance_search": "",
          "login": ""
        },
        "facet_views": [],
        "filetype_options": [
          {"value": "html", "label_key": "labels.facet_filetype_html"}
        ],
        "csrf_required": true,
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f"
      }
    }

Die einzelnen Elemente von ``response`` sind wie folgt beschrieben. Alle Felder sind Pflichtfelder.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Antwortinformationen
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Typ
     - Beschreibung
   * - ``site_name``
     - string
     - Seitenname.
   * - ``login_required``
     - boolean
     - Gibt an, ob eine Anmeldung erforderlich ist.
   * - ``locales``
     - string[]
     - Array der verfügbaren Gebietsschemas.
   * - ``theme``
     - object
     - Aktiver Theme-Deskriptor. Siehe nachfolgende Tabelle.
   * - ``features``
     - object
     - Feature-Flags. Siehe nachfolgende Tabelle.
   * - ``page_size_default``
     - integer
     - Standard-Seitengröße.
   * - ``page_size_max``
     - integer
     - Maximale Seitengröße.
   * - ``sort_options``
     - object[]
     - Sortieroptionen für die Suchoberfläche. Siehe nachfolgende Tabelle.
   * - ``num_options``
     - integer[]
     - Array der wählbaren Seitengrößen. Auf Werte begrenzt, die ``page_size_max`` nicht überschreiten.
   * - ``lang_options``
     - object[]
     - Optionen für den Sprachfilter. Siehe nachfolgende Tabelle.
   * - ``label_options``
     - object[]
     - Optionen für konfigurierte Labels. Siehe nachfolgende Tabelle.
   * - ``notifications``
     - object
     - HTML-Benachrichtigungsschnipsel, die oben in bestimmten Ansichten angezeigt werden. Siehe nachfolgende Tabelle.
   * - ``facet_views``
     - object[]
     - Konfigurierte Facettenabfrage-Ansichtsgruppen. Siehe nachfolgende Tabelle.
   * - ``filetype_options``
     - object[]
     - Dateitypfacetten-Optionen für das erweiterte Suchformular. Siehe nachfolgende Tabelle.
   * - ``csrf_required``
     - boolean
     - Gibt an, ob ein CSRF-Token erforderlich ist.
   * - ``csrf_token``
     - string
     - Leere Zeichenkette, wenn ``csrf_required`` ``false`` ist; andernfalls das neue, mit der aktuellen Sitzung verknüpfte Token.

theme
~~~~~

``theme`` ist stets vorhanden, aber ein leeres Objekt, wenn kein benutzerdefiniertes Theme mit der Anfrage verknüpft ist.
Aus dem Manifest abgeleitete Schlüssel (``display_name`` / ``version`` / ``supported_locales``) sind nur vorhanden, wenn das aktive Theme ein Manifest enthält.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: theme
   :header-rows: 1
   :widths: 28 15 57

   * - Feld
     - Typ
     - Beschreibung
   * - ``name``
     - string
     - Theme-Name.
   * - ``display_name``
     - string
     - Angezeigter Theme-Name.
   * - ``version``
     - string
     - Theme-Version.
   * - ``supported_locales``
     - string[]
     - Array der vom Theme unterstützten Gebietsschemas.

features
~~~~~~~~

Alle Felder sind Pflichtfelder.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: features
   :header-rows: 1
   :widths: 28 15 57

   * - Feld
     - Typ
     - Beschreibung
   * - ``user_favorite``
     - boolean
     - Gibt an, ob die Benutzerfavoriten-Funktion aktiviert ist.
   * - ``popular_word``
     - boolean
     - Gibt an, ob die Beliebte-Wörter-Funktion aktiviert ist.
   * - ``suggest_search_log``
     - boolean
     - Gibt an, ob Vorschläge aus dem Suchprotokoll aktiviert sind.
   * - ``suggest_documents``
     - boolean
     - Gibt an, ob Vorschläge aus Dokumenten aktiviert sind.
   * - ``login_required``
     - boolean
     - Gibt an, ob eine Anmeldung erforderlich ist.
   * - ``eoled``
     - boolean
     - Gibt an, ob dieser |Fess|-Build das End-of-Life-Datum erreicht hat.
   * - ``development_mode``
     - boolean
     - Wird ``true``, wenn die eingebettete (Entwicklungs-)Suchmaschine verwendet wird.
   * - ``search_log_enabled``
     - boolean
     - Gibt an, ob das Suchprotokoll aktiviert ist.
   * - ``thumbnail_enabled``
     - boolean
     - Gibt an, ob Vorschaubilder aktiviert sind.
   * - ``display_label_type``
     - boolean
     - Wird ``true``, wenn mindestens ein Label konfiguriert ist.
   * - ``clipboard_copy_icon``
     - boolean
     - Gibt an, ob das Zwischenablage-Kopiersymbol angezeigt wird.
   * - ``eol_link``
     - string
     - Aufgelöste EOL-Informations-URL. Leere Zeichenkette, wenn kein EOL vorliegt oder die URL nicht aufgelöst werden konnte.
   * - ``installation_link``
     - string
     - Aufgelöste Installationsanleitungs-URL. Leere Zeichenkette, wenn die URL nicht aufgelöst werden konnte.
   * - ``login_link``
     - boolean
     - Gibt an, ob der Anmelde-Link angezeigt werden soll.
   * - ``rag_chat_enabled``
     - boolean
     - Gibt an, ob die RAG-Chat-Funktion verfügbar ist.

sort_options
~~~~~~~~~~~~

Array der Sortieroptionen für die Suchoberfläche.
Jedes Element enthält ``value`` und ``label_key``.
Elemente mit ``click_count.*`` sind nur vorhanden, wenn das Suchprotokoll aktiviert ist; Elemente mit ``favorite_count.*`` sind nur vorhanden, wenn Benutzerfavoriten aktiviert sind.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elemente von sort_options
   :header-rows: 1
   :widths: 28 15 57

   * - Feld
     - Typ
     - Beschreibung
   * - ``value``
     - string
     - Sortierwert.
   * - ``label_key``
     - string
     - Label-Schlüssel.

num_options
~~~~~~~~~~~

Integer-Array der wählbaren Seitengrößen. Auf Werte begrenzt, die ``page_size_max`` nicht überschreiten.

lang_options
~~~~~~~~~~~~

Array der Sprachfilteroptionen.
Jedes Element enthält ``value`` und ``label_key``.
Das erste Element ist das ``all``-Sentinel, gefolgt von einem Element pro unterstütztem Sprachcode.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elemente von lang_options
   :header-rows: 1
   :widths: 28 15 57

   * - Feld
     - Typ
     - Beschreibung
   * - ``value``
     - string
     - Sprachwert.
   * - ``label_key``
     - string
     - Label-Schlüssel.

label_options
~~~~~~~~~~~~~

Array der Optionen für konfigurierte Labels. Leeres Array, wenn keine Labels definiert sind.
Jedes Element enthält ``value`` und ``name``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elemente von label_options
   :header-rows: 1
   :widths: 28 15 57

   * - Feld
     - Typ
     - Beschreibung
   * - ``value``
     - string
     - Label-Wert.
   * - ``name``
     - string
     - Label-Name.

notifications
~~~~~~~~~~~~~

HTML-Benachrichtigungsschnipsel, die oben in bestimmten Ansichten angezeigt werden. Eine leere Zeichenkette bedeutet, dass keine Benachrichtigung für diese Ansicht vorhanden ist.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: notifications
   :header-rows: 1
   :widths: 28 15 57

   * - Feld
     - Typ
     - Beschreibung
   * - ``search_top``
     - string
     - Benachrichtigung für die Such-Startseite.
   * - ``advance_search``
     - string
     - Benachrichtigung für die erweiterte Suche.
   * - ``login``
     - string
     - Benachrichtigung für die Anmeldeseite.

facet_views
~~~~~~~~~~~

Array der konfigurierten Facettenabfrage-Ansichtsgruppen. Leeres Array, wenn keine konfiguriert sind.
Jedes Element enthält ``group_name`` und ``queries``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elemente von facet_views
   :header-rows: 1
   :widths: 28 15 57

   * - Feld
     - Typ
     - Beschreibung
   * - ``group_name``
     - string
     - Gruppenname.
   * - ``queries``
     - object[]
     - Array der Facettenabfragen dieser Gruppe. Jedes Element enthält ``label_key`` (string) und ``value`` (string).

filetype_options
~~~~~~~~~~~~~~~~

Array der Dateitypfacetten-Optionen für das erweiterte Suchformular.
Jedes Element enthält ``value`` und ``label_key``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elemente von filetype_options
   :header-rows: 1
   :widths: 28 15 57

   * - Feld
     - Typ
     - Beschreibung
   * - ``value``
     - string
     - Dateityp-Wert.
   * - ``label_key``
     - string
     - Label-Schlüssel.

Fehlerantwort
~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort
   :header-rows: 1
   :widths: 25 75

   * - Statuscode
     - Beschreibung
   * - 405 Method Not Allowed
     - Wenn eine nicht unterstützte HTTP-Methode angegeben wurde.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.
