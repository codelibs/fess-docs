========
Tags-API
========

Dieses Dokument beschreibt die v2-Tags-API von |Fess|, mit der angemeldete Benutzer ihre eigenen
Tags verwalten und an Dokumente vergeben.
Informationen zum gemeinsamen Antwort-Envelope, zum Fehlermodell und zu CSRF finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

.. note::

   Tags sind standardmäßig deaktiviert. Um sie zu nutzen, setzen Sie ``user.tag.enabled=true`` in
   ``fess_config.properties``. ``features.user_tag`` von ``/api/v2/ui/config`` meldet den Zustand.
   Solange Tags deaktiviert sind, antworten die Tag-Endpunkte auf eine Anfrage, die die CSRF- und
   Origin-Prüfung besteht und eine unterstützte Methode verwendet, mit ``invalid_request`` (400).

Funktionsweise der Tags
=======================

- Tags werden pro Benutzer verwaltet. Wer ein Tag erstellt, ist sein Besitzer; der Besitzer ist die
  Benutzer-ID der Anmeldung. Zwei Benutzer können denselben Namen verwenden und haben trotzdem zwei
  getrennte Tags.
- Nur angemeldete Benutzer können Tags verwenden. Jeder Tag-Endpunkt handelt als Benutzer der
  Anmeldesitzung; ein Zugriffstoken ersetzt keine Anmeldung. Ein Aufrufer ohne Anmeldung erhält
  ``auth_required`` (401).
- Ein neues Tag ist privat: Nur sein Besitzer sieht es. Gibt der Besitzer das Tag frei, kann jeder
  angemeldete Benutzer es sehen und danach filtern. Ein nicht angemeldeter Benutzer sieht kein Tag,
  auch kein freigegebenes.
- Nur der Besitzer kann ein Tag ändern, löschen und an Dokumente vergeben oder davon entfernen. Ein
  freigegebenes Tag eines anderen Benutzers kann nur angezeigt und zum Filtern verwendet werden.
  Administratoren verwalten alle Tags im Verwaltungsbildschirm (siehe :doc:`../admin/tagtype-guide`).
- Ein Tag wird an die URL eines Dokuments vergeben, sodass jedes indexierte Dokument mit dieser URL
  es erhält.

Jedes Tag hat zwei Bezeichner.

``value``
    Der Tag-Wert, ``base64url(Name):base64url(Besitzer)`` (UTF-8, ohne Auffüllung), der im Feld
    ``tag`` des Index gespeichert wird. Behandeln Sie ihn als undurchsichtigen Wert zum Filtern von
    Suchergebnissen.

``id``
    Die Tag-ID, der SHA-256 von ``value`` in hexadezimalen Kleinbuchstaben (64 Zeichen). Sie wird in
    Pfaden wie ``/api/v2/tags/{tagId}`` angegeben. Eine Umbenennung ändert sowohl ``value`` als auch
    ``id``.

Ein Tag-Name wird NFKC-normalisiert, Leerzeichenfolgen werden zu einem Leerzeichen zusammengefasst,
und Anfang und Ende werden getrimmt. Das Ergebnis muss 1 bis ``user.tag.name.max.length``
(Standard: ``50``) Zeichen lang sein; Namen mit einem Steuer- oder Formatzeichen (etwa einem
Nullbreitenzeichen oder einer Bidi-Überschreibung) werden abgelehnt.

Tags in der Suche
=================

Solange ``user.tag.enabled`` den Wert ``true`` hat, behandelt die Such-API (``/api/v2/search``) Tags
wie folgt.

- Jeder Treffer enthält die für den Aufrufer sichtbaren Tags als ``tags``. Jeder Eintrag hat
  ``value``, ``name``, ``owner``, ``mine`` (``true``, wenn der Aufrufer das Tag besitzt) und
  ``shared`` (``true`` für ein freigegebenes Tag). Ohne Tags fehlt ``tags``. Das Indexfeld ``tag``
  selbst wird nie zurückgegeben.
- ``facet.field=tag`` liefert in ``facet_field`` eine Facette der für den Aufrufer sichtbaren Tags.
  Neben ``value`` und ``count`` hat jeder Bucket ``label`` (den Tag-Namen), ``owner``, ``mine`` und
  ``shared``.
- ``fields.tag=<Wert>`` grenzt die Ergebnisse auf Dokumente mit einem Tag ein. Übergeben Sie den
  ``value`` aus ``tags`` eines Treffers oder aus einem Facetten-Bucket unverändert.

Eine Bedingung auf Tags (``fields.tag``, ``tag:``, ``ex_q``, ``facet.query``) trifft nur den exakten
Wert eines Tags, das der Aufrufer sehen kann. Der Wert eines für ihn unsichtbaren Tags sowie
Platzhalter-, Präfix-, unscharfe und Bereichsbedingungen treffen nichts. Ein Aufrufer ohne Anmeldung
erhält weder Tags noch eine Tag-Facette, und eine Tag-Bedingung trifft nichts.

Ein Benutzer sieht höchstens ``user.tag.visible.max.size`` (Standard: ``1000``) Tags, die eigenen
zuerst. Weitere Tags erscheinen weder in ``tags`` der Treffer noch in der Facette, lassen sich aber
weiterhin zum Filtern verwenden.

Wann Dokumente Änderungen übernehmen
====================================

Das Erstellen, Ändern und Löschen von Tags sowie das Vergeben und Entfernen an Dokumenten zeigen die
Tag-Endpunkte sofort. Das Feld ``tag`` der indexierten Dokumente wird dagegen über eine Warteschlange
im Speicher aktualisiert, die der Job „Log Aggregator“ (``log_aggregator``) jede Minute gesammelt
anwendet. Suchtreffer, Facette und Filter spiegeln eine Änderung daher erst nach bis zu etwa einer
Minute wider. Nach einer Umbenennung behalten die Dokumente den alten Wert, bis die Warteschlange das
nächste Mal verarbeitet wird, und das Tag wird in der Zwischenzeit nicht an ihnen angezeigt.

Zur Warteschlange und zu den Jobs siehe :doc:`../admin/tagtype-guide`.

Tags auflisten
==============

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v2/tags``
==================  ====================================================

Gibt die Tags des Aufrufers nach Sortierreihenfolge und Name zurück. Freigegebene Tags anderer
Benutzer sind nicht enthalten.

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` des gemeinsamen Envelopes zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "tags": [
          {
            "id": "10cfcc876984e934930a5e4461088f738d748271320a8755344fd7f2edc8120a",
            "value": "enUtcHJ1ZWZlbg:YW5uYQ",
            "name": "zu-pruefen",
            "shared": false,
            "sort_order": 0,
            "path_count": 3
          }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder

   * - ``tags``
     - Die Tags des Aufrufers. Jedes hat ``id``, ``value``, ``name``, ``shared`` (``true`` für ein
       freigegebenes Tag), ``sort_order`` und ``path_count`` (die Anzahl der URLs mit dem Tag).

Tabelle: Antwortfelder

Ein Tag erstellen
=================

Anfrage
-------

==================  ====================================================
HTTP-Methode        POST
Endpunkt            ``/api/v2/tags``
==================  ====================================================

Erstellt ein Tag des Aufrufers. Als zustandsändernde Anfrage erfordert sie den Header
``X-Fess-CSRF-Token`` (siehe :doc:`api-overview`).

- Ein Benutzer kann höchstens ``user.tag.max.tags`` (Standard: ``1000``) Tags haben. Darüber hinaus
  antwortet der Endpunkt mit ``invalid_request`` (400).
- Hat der Aufrufer bereits ein Tag dieses Namens, antwortet der Endpunkt mit ``conflict`` (409). Ein
  gleichnamiges Tag eines anderen Benutzers spielt keine Rolle.

Senden Sie ``Content-Type: application/json``; der Body darf höchstens 1 KiB (1024 Byte) groß sein.

::

    {
      "name": "zu-pruefen",
      "shared": false
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Anfrage-Body

   * - ``name``
     - Tag-Name (str, erforderlich).
   * - ``shared``
     - ``true`` macht das Tag für jeden angemeldeten Benutzer sichtbar (bool, Standard: ``false``).

Tabelle: Anfrage-Body

Antwort
-------

Bei Erfolg (200) enthält ``tag`` direkt unter ``response`` das neue Tag in der Form eines Eintrags
von ``GET /api/v2/tags`` mit ``path_count`` ``0``.

Ein Tag ändern
==============

Anfrage
-------

==================  ====================================================
HTTP-Methode        PUT
Endpunkt            ``/api/v2/tags/{tagId}``
==================  ====================================================

Benennt ein Tag des Aufrufers um oder ändert, ob es freigegeben ist. Der Header
``X-Fess-CSRF-Token`` ist erforderlich.

- Der Body enthält ``name``, ``shared`` oder beides.
- Ein neuer ``name`` benennt das Tag um und gibt ihm eine neue ``id`` und einen neuen ``value``.
  Dokumente mit dem alten Wert erhalten den neuen, wenn die Warteschlange das nächste Mal verarbeitet
  wird. Eine Umbenennung auf einen Namen, den der Aufrufer bereits verwendet, ergibt ``conflict``
  (409) und lässt das Tag unverändert.
- ``shared`` ändert nur, wer das Tag sieht; kein Dokument wird aktualisiert. Wird ``shared`` auf
  ``false`` gesetzt, bleiben die Rollen und Gruppen, die ein Administrator zu den Berechtigungen
  hinzugefügt hat, erhalten.
- Ein freigegebenes Tag eines anderen Benutzers ergibt ``forbidden`` (403), ein für den Aufrufer
  unsichtbares Tag ``not_found`` (404).
- Ein Schreibvorgang, der wiederholt gegen eine andere Aktualisierung verliert, ergibt ebenfalls
  ``conflict`` (409).

::

    {
      "name": "geprueft",
      "shared": true
    }

Bei Erfolg (200) enthält ``response`` ``tag`` (das geänderte Tag) und ``renamed`` (``true``, wenn
das Tag umbenannt wurde; dann sind ``tag.id`` und ``tag.value`` neu).

Ein Tag löschen
===============

Anfrage
-------

==================  ====================================================
HTTP-Methode        DELETE
Endpunkt            ``/api/v2/tags/{tagId}``
==================  ====================================================

Löscht ein Tag des Aufrufers. Die Dokumente verlieren seinen Wert, wenn die Warteschlange das nächste
Mal verarbeitet wird. Der Header ``X-Fess-CSRF-Token`` ist erforderlich. Ein freigegebenes Tag eines
anderen Benutzers ergibt ``forbidden`` (403), ein für den Aufrufer unsichtbares Tag ``not_found``
(404).

Bei Erfolg (200) enthält ``response`` ``id`` (die ID des gelöschten Tags) und ``deleted`` (immer
``true``).

Die Tags eines Dokuments abrufen
================================

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Gibt die für den Aufrufer sichtbaren Tags an der URL des Dokuments zurück sowie die eigenen Tags des
Aufrufers, die dort noch nicht vergeben sind. Das Dokument wird mit den Rollen des Aufrufers
gesucht; ein Dokument, das der Aufrufer nicht durchsuchen kann, ergibt ``not_found`` (404).

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` des gemeinsamen Envelopes zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "tags": [
          {
            "id": "10cfcc876984e934930a5e4461088f738d748271320a8755344fd7f2edc8120a",
            "value": "enUtcHJ1ZWZlbg:YW5uYQ",
            "name": "zu-pruefen",
            "owner": "anna",
            "mine": true,
            "shared": false
          },
          {
            "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
            "value": "c3BlY3M:Ym9i",
            "name": "specs",
            "owner": "bob",
            "mine": false,
            "shared": true
          }
        ],
        "addable": []
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder

   * - ``doc_id``
     - Dokument-ID (str).
   * - ``tags``
     - Die für den Aufrufer sichtbaren Tags an der URL des Dokuments. Jedes hat ``id``, ``value``,
       ``name``, ``owner``, ``mine`` (``true``, wenn der Aufrufer das Tag besitzt) und ``shared``
       (``true`` für ein freigegebenes Tag).
   * - ``addable``
     - Die Tags des Aufrufers, die nicht an der URL des Dokuments vergeben sind, in derselben Form
       wie ``tags``.
   * - ``added``
     - Nur POST. ``false``, wenn das Tag bereits am Dokument war (bool).
   * - ``tag``
     - Nur POST. Das an das Dokument vergebene Tag, in derselben Form wie ``tags``.
   * - ``removed``
     - Nur DELETE. ``false``, wenn das Tag nicht am Dokument war (bool).

Tabelle: Antwortfelder

Ein Tag an ein Dokument vergeben
================================

Anfrage
-------

==================  ====================================================
HTTP-Methode        POST
Endpunkt            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Fügt die URL des Dokuments einem Tag des Aufrufers hinzu. Der Header ``X-Fess-CSRF-Token`` ist
erforderlich.

Der Body (``Content-Type: application/json``, höchstens 1 KiB) enthält entweder ``id``, ein
vorhandenes Tag, oder ``name``, einen Tag-Namen. Sind beide angegeben, gilt ``id``.

::

    {
      "name": "zu-pruefen"
    }

- Mit ``name`` wird ein privates Tag dieses Namens erstellt und vergeben, wenn der Aufrufer noch
  keines hat. Das neue Tag zählt gegen ``user.tag.max.tags``.
- Ein Tag kann an höchstens ``user.tag.max.paths`` (Standard: ``10000``) URLs vergeben werden.
  Darüber hinaus antwortet der Endpunkt mit ``invalid_request`` (400).
- Die ``id`` eines Tags eines anderen Benutzers ergibt ``forbidden`` (403), wenn der Aufrufer das
  Tag sehen kann, sonst ``not_found`` (404).
- Bei Erfolg enthält die Antwort die Felder von „Die Tags eines Dokuments abrufen“ sowie ``added``
  und ``tag``. Die Tag-Endpunkte zeigen das Tag sofort; die Suchergebnisse der Dokumente mit der URL
  übernehmen es, wenn die Warteschlange das nächste Mal verarbeitet wird (etwa eine Minute später).

Ein Tag von einem Dokument entfernen
====================================

Anfrage
-------

==================  ====================================================
HTTP-Methode        DELETE
Endpunkt            ``/api/v2/documents/{docId}/tags/{tagId}``
==================  ====================================================

Entfernt die URL des Dokuments aus dem mit ``tagId`` angegebenen Tag des Aufrufers. Der Header
``X-Fess-CSRF-Token`` ist erforderlich. Ein Tag eines anderen Benutzers ergibt ``forbidden`` (403),
wenn der Aufrufer es sehen kann, sonst ``not_found`` (404). Bei Erfolg enthält die Antwort die
Felder von „Die Tags eines Dokuments abrufen“ sowie ``removed``.

Fehlerantwort
=============

Details zum Fehlermodell finden Sie unter :doc:`api-overview`. Die Tag-Endpunkte geben die folgenden
HTTP-Status zurück.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrage ungültig ist, auch wenn Tags deaktiviert sind, der Tag-Name ungültig ist, ein
       erforderliches Feld fehlt oder ``user.tag.max.tags`` bzw. ``user.tag.max.paths``
       überschritten würde.
   * - 401 Unauthorized
     - Ohne Anmeldung (ein Zugriffstoken ersetzt sie nicht).
   * - 403 Forbidden
     - Ein fehlendes oder abgelaufenes CSRF-Token oder eine Änderung am Tag eines anderen Benutzers.
       Die CSRF-Prüfung erfolgt vor der Anmeldeprüfung, daher erhält eine zustandsändernde Anfrage
       ohne Sitzung 403 statt 401.
   * - 404 Not Found
     - Wenn das Tag nicht existiert oder für den Aufrufer unsichtbar ist, oder wenn das Dokument nicht
       gefunden wird oder der Aufrufer es nicht durchsuchen kann.
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht zulässig ist.
   * - 409 Conflict
     - Wenn bereits ein Tag dieses Namens existiert oder ein Schreibvorgang gegen eine andere
       Aktualisierung verloren hat.
   * - 413 Payload Too Large
     - Wenn der Anfrage-Body die Größenbegrenzung (1 KiB) überschreitet.
   * - 415 Unsupported Media Type
     - Wenn der ``Content-Type`` nicht unterstützt wird.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort

Einstellungen
=============

Die folgenden Einstellungen in ``fess_config.properties`` passen die Tags an.

.. list-table::
   :header-rows: 1
   :widths: 35 50 15

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``user.tag.enabled``
     - Ob angemeldete Benutzer Tags verwenden können.
     - ``false``
   * - ``user.tag.name.max.length``
     - Maximale Länge eines Tag-Namens in Codepunkten.
     - ``50``
   * - ``user.tag.max.tags``
     - Maximale Anzahl Tags, die ein Benutzer besitzen kann.
     - ``1000``
   * - ``user.tag.max.paths``
     - Maximale Anzahl URLs, an die ein Tag vergeben werden kann.
     - ``10000``
   * - ``user.tag.queue.max.size``
     - Maximale Anzahl Änderungen, die im Speicher gehalten werden, bis sie die Dokumente erreichen.
       Eine Änderung darüber hinaus wird mit einem WARN-Log verworfen.
     - ``10000``
   * - ``user.tag.process.batch.size``
     - Anzahl der URLs pro Bulk-Anfrage, wenn Änderungen auf die Dokumente angewendet werden.
     - ``100``
   * - ``user.tag.visible.max.size``
     - Maximale Anzahl Tags, die ein Benutzer in einer Suche sieht.
     - ``1000``
