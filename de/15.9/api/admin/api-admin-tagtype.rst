===========
TagType API
===========

Übersicht
=========

Die TagType API dient zur Verwaltung der Tags der Benutzer in |Fess|, also der benutzereigenen
Tags, die angemeldete Benutzer an Dokumente vergeben (siehe :doc:`../../admin/tagtype-guide`). Sie
verwaltet die Tags aller Benutzer, unabhängig davon, ob ``user.tag.enabled`` den Wert ``true`` hat.

Informationen zur Authentifizierung sowie zu den gemeinsamen Spezifikationen von Antworten
(``status``-Code, ``version``-Feld, Fehlerformat, HTTP-Statuscodes usw.) finden Sie unter
:doc:`api-admin-overview`.
Für den Zugriff auf diese API ist ein Access Token mit Admin-API-Berechtigung (``admin-api``)
im Header ``Authorization: Bearer <access_token>`` erforderlich.

Die JSON-Feldnamen dieser API sind in snake_case (``sort_order``, ``virtual_host``, ``seq_no``,
``primary_term`` usw.).

Basis-URL
=========

::

    /api/admin/tagtype

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /settings
     - Tags auflisten
   * - GET
     - /setting/{id}
     - Tag abrufen
   * - POST
     - /setting
     - Tag erstellen
   * - PUT
     - /setting
     - Tag aktualisieren
   * - DELETE
     - /setting/{id}
     - Tag löschen

Tags auflisten
==============

Anfrage
-------

::

    GET /api/admin/tagtype/settings

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``size``
     - Integer
     - Nein
     - Anzahl der Einträge pro Seite. Standard ist der Wert von ``paging.page.size`` (standardmäßig ``25``).
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1). Standard ist ``1``.
   * - ``name``
     - String
     - Nein
     - Nach Tag-Name filtern (Platzhaltersuche: trifft Namen, die den Text enthalten).
   * - ``owner``
     - String
     - Nein
     - Nach Besitzer filtern (Platzhaltersuche: trifft Besitzer, die den Text enthalten).

Die Tags sind nach Sortierreihenfolge, Name und Besitzer sortiert.

Antwort
-------

.. code-block:: json

    {
      "response": {
        "version": "15.9.0",
        "status": 0,
        "settings": [
          {
            "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
            "seq_no": 12,
            "primary_term": 1,
            "name": "to-review",
            "owner": "alice",
            "permissions": "{user}alice",
            "virtual_host": "",
            "sort_order": 0
          }
        ],
        "total": 5
      }
    }

.. note::

   Die Liste liest die möglicherweise langen Pfade der Tags nicht; die Einträge haben daher kein
   ``paths``. PUT ersetzt das Tag als Ganzes: Um ein Tag zu bearbeiten, rufen Sie es zuerst mit
   ``GET /setting/{id}`` ab, damit seine ``paths`` erhalten bleiben.

Tag abrufen
===========

Anfrage
-------

::

    GET /api/admin/tagtype/setting/{id}

Antwort
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
          "seq_no": 12,
          "primary_term": 1,
          "name": "to-review",
          "owner": "alice",
          "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
          "permissions": "{user}alice",
          "virtual_host": "",
          "sort_order": 0
        }
      }
    }

``seq_no`` und ``primary_term`` kennzeichnen die gelesene Version des Tags. ``paths`` und
``permissions`` enthalten einen Eintrag pro Zeile.

Tag erstellen
=============

Anfrage
-------

::

    POST /api/admin/tagtype/setting
    Content-Type: application/json

Anfragetext
~~~~~~~~~~~

.. code-block:: json

    {
      "name": "specs",
      "owner": "bob",
      "paths": "https://www.example.com/spec.pdf",
      "permissions": "{user}bob\n{role}guest",
      "sort_order": 0
    }

Feldbeschreibung
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Feld
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``name``
     - String
     - Ja
     - Tag-Name. Er wird NFKC-normalisiert, Leerzeichenfolgen werden zusammengefasst und Anfang und
       Ende getrimmt; das Ergebnis muss 1 bis ``user.tag.name.max.length`` (Standard: ``50``)
       Zeichen ohne Steuer- oder Formatzeichen umfassen.
   * - ``owner``
     - String
     - Ja
     - Benutzer-ID der Anmeldung des Besitzers (max. 1000 Zeichen).
   * - ``paths``
     - String
     - Nein
     - URLs der Dokumente, an die das Tag vergeben wird, getrennt durch einen Zeilenumbruch
       (``\n``). Jede muss dem Feld ``url`` eines Dokuments genau entsprechen. Höchstens
       ``user.tag.max.paths`` (Standard: ``10000``).
   * - ``permissions``
     - String
     - Nein
     - Benutzer/Gruppen/Rollen, die das Tag sehen können (z. B. ``{role}guest``), getrennt durch
       einen Zeilenumbruch (``\n``). Ist das Feld leer, sieht nur der Besitzer das Tag.
       ``{role}guest`` (der Wert von ``role.search.guest.permissions``) gibt das Tag für alle
       angemeldeten Benutzer frei.
   * - ``virtual_host``
     - String
     - Nein
     - Virtueller Host (max. 1000 Zeichen).
   * - ``sort_order``
     - Integer
     - Nein
     - Anzeigereihenfolge (nicht negative Ganzzahl). Ohne Angabe ``0``.

Die ID eines Tags ist der SHA-256 seines aus Name und Besitzer gebildeten Werts und wird daher vom
Server bestimmt. Besitzer und Name kennzeichnen ein Tag gemeinsam: Hat der Besitzer bereits ein Tag
dieses Namens, schlägt das Erstellen mit einem Validierungsfehler fehl (``status: 1``, „A tag with
the same name and owner already exists.“).

Antwort
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
        "created": true
      }
    }

Bei erfolgreicher Erstellung ist ``created`` ``true``.

Tag aktualisieren
=================

Anfrage
-------

::

    PUT /api/admin/tagtype/setting
    Content-Type: application/json

Anfragetext
~~~~~~~~~~~

.. code-block:: json

    {
      "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
      "seq_no": 12,
      "primary_term": 1,
      "name": "reviewed",
      "owner": "alice",
      "paths": "https://www.example.com/a.html",
      "permissions": "{user}alice",
      "virtual_host": "",
      "sort_order": 0
    }

Der Text enthält alle Felder der Erstellung und zusätzlich die folgenden Felder. Das Tag wird als
Ganzes ersetzt; senden Sie also auch die ``paths``, die erhalten bleiben sollen.

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Feld
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``id``
     - String
     - Ja
     - Die ID des zu aktualisierenden Tags.
   * - ``seq_no``
     - Integer
     - Ja
     - Der von ``GET /setting/{id}`` zurückgegebene ``seq_no`` des Tags.
   * - ``primary_term``
     - Integer
     - Ja
     - Der von ``GET /setting/{id}`` zurückgegebene ``primary_term`` des Tags.

- Wurde das Tag nach dem Lesen geändert, sodass ``seq_no`` und ``primary_term`` nicht mehr passen,
  schlägt die Aktualisierung mit einem Validierungsfehler fehl (``status: 1``, „The tag was changed
  by someone else. Reload it and try again.“). Rufen Sie das Tag erneut ab und wiederholen Sie den
  Vorgang.
- Eine Änderung von ``name`` oder ``owner`` gibt dem Tag eine neue ID; die ``id`` der Antwort ist die
  neue. Hat der Besitzer bereits ein Tag des neuen Namens, schlägt die Aktualisierung mit „A tag
  with the same name and owner already exists.“ fehl.
- Ändert sich der Besitzer, wird die Benutzerberechtigung des alten Besitzers in ``permissions``
  durch die des neuen Besitzers ersetzt.

Antwort
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "c1fd8e024cbadfc79468e66fa52350e46cc31837aabf75b7ee6d929edaa20396",
        "created": false
      }
    }

Bei der Aktualisierung ist ``created`` ``false``.

Tag löschen
===========

Anfrage
-------

::

    DELETE /api/admin/tagtype/setting/{id}

Antwort
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Wird das Tag während des Löschens geändert, schlägt das Löschen mit „The tag was changed by someone
else. Reload it and try again.“ fehl.

Wie Änderungen die Dokumente erreichen
======================================

Das Erstellen, Aktualisieren und Löschen eines Tags über diese API wird sofort in den Tags
gespeichert. Solange ``user.tag.enabled`` den Wert ``true`` hat, wird die Änderung für die Dokumente
(hinzugefügte und entfernte Pfade, eine Umbenennung oder eine Löschung) in die Warteschlange
gestellt und vom minütlichen Job „Log Aggregator“ (``log_aggregator``) angewendet. Bei ``false``
wird nichts eingereiht; führen Sie nach dem Aktivieren der Tags den Job „Tag Updater“
(``tag_updater``) aus. Siehe :doc:`../../admin/tagtype-guide`.

Anwendungsbeispiele
===================

Ein Tag für alle angemeldeten Benutzer freigeben
------------------------------------------------

.. code-block:: bash

    # Das Tag mit paths, seq_no und primary_term lesen
    curl "http://localhost:8080/api/admin/tagtype/setting/0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Mit {role}guest in den Berechtigungen zurücksenden
    curl -X PUT "http://localhost:8080/api/admin/tagtype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
           "seq_no": 12,
           "primary_term": 1,
           "name": "to-review",
           "owner": "alice",
           "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
           "permissions": "{user}alice\n{role}guest",
           "sort_order": 0
         }'

Die Tags eines Benutzers auflisten
----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/tagtype/settings" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"owner": "alice", "size": 50, "page": 1}'

Siehe auch
==========

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../api-tag` - Tags-API
- :doc:`../../admin/tagtype-guide` - Tag-Verwaltungsanleitung
