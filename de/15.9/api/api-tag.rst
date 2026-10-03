========
Tags-API
========

Dieses Dokument beschreibt die v2-Tags-API von |Fess|, mit der Benutzer Dokumente taggen.
Informationen zum gemeinsamen Antwort-Envelope, zum Fehlermodell und zu CSRF finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

.. note::

   Tags sind standardmäßig deaktiviert. Um sie zu nutzen, setzen Sie ``user.tag.enabled=true`` in
   ``fess_config.properties``. ``features.user_tag`` von ``/api/v2/ui/config`` meldet den Zustand.

Ein Tag ist ein Label der Art „Tag“ (siehe :doc:`../admin/labeltype-guide`): Der Labelname ist der
Tag-Name, der Wert der SHA-256 des Namens in Hexadezimalform, die eingeschlossenen Pfade sind die
getaggten URLs, und die Berechtigungen bestimmen, wer das Tag sehen kann. Ein Tag ist nur sichtbar,
wenn sein Label für den Aufrufer sichtbar ist.

Die Such-API (``/api/v2/search``) gibt zu jedem Treffer die für den Aufrufer sichtbaren Tags als
``tags`` zurück. ``fields.tag=<Wert>`` grenzt die Ergebnisse auf Dokumente mit einem Tag ein, und
``facet.field=tag`` liefert eine Tag-Facette. Das Indexfeld ``tag`` selbst wird nicht zurückgegeben.

Tags abrufen
============

Anfrage
-------

==================  ====================================================
HTTP-Methode        GET
Endpunkt            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Gibt die für den Aufrufer sichtbaren Tags des Dokuments zurück. Kann der Aufrufer das Dokument nicht
durchsuchen, antwortet der Endpunkt mit ``not_found`` (404).

Antwort
-------

Bei Erfolg (200) werden die folgenden Felder direkt unter ``response`` des gemeinsamen Envelopes zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "addable": true,
        "tags": [
          { "value": "9f86d081884c7d65...", "name": "zu-pruefen", "mine": true }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortfelder

   * - ``doc_id``
     - Dokument-ID (str).
   * - ``addable``
     - ``true``, wenn der Aufrufer angemeldet ist und Tags hinzufügen kann (bool).
   * - ``added``
     - Nur POST. ``false``, wenn der Aufrufer das Dokument bereits getaggt hatte (bool).
   * - ``removed``
     - Nur DELETE (bool).
   * - ``tags``
     - Die für den Aufrufer sichtbaren Tags. Jedes hat ``value`` (den Labelwert für ``fields.tag``),
       ``name`` (den Tag-Namen) und ``mine`` (``true``, wenn der Aufrufer zu den Berechtigungen des
       Tags gehört).

Tabelle: Antwortfelder

Ein Tag hinzufügen
==================

Anfrage
-------

==================  ====================================================
HTTP-Methode        POST
Endpunkt            ``/api/v2/documents/{docId}/tags``
==================  ====================================================

Taggt die URL des Dokuments für den angemeldeten Benutzer; ein Zugriffstoken ersetzt keine Anmeldung.
Als zustandsändernde Anfrage erfordert sie den Header ``X-Fess-CSRF-Token``.

- Gibt es bereits ein Tag dieses Namens, wird die URL zu seinen eingeschlossenen Pfaden und der
  Benutzer zu seinen Berechtigungen hinzugefügt. Andernfalls wird ein Tag erstellt, das nur der
  Benutzer sehen kann. Tags gleichen Namens werden daher zu einem zusammengeführt, und Benutzer, die
  ein Tag gleichen Namens hinzugefügt haben, sehen gegenseitig, wo ihre Tags gesetzt sind.
- Erneutes Taggen desselben Dokuments ergibt ``added: false``.
- Ein Dokument kann höchstens ``user.tag.max.document.tags`` (Standard: ``100``) Tags haben.

Senden Sie ``Content-Type: application/json`` mit dem Tag-Namen in ``name``.

::

    {
      "name": "zu-pruefen"
    }

Der Name wird NFKC-normalisiert, Leerzeichenfolgen werden zusammengefasst und er wird getrimmt. Er
muss 1 bis ``user.tag.name.max.length`` (Standard: ``50``) Zeichen lang sein; Namen mit einem
Steuer- oder Formatzeichen (etwa einem Nullbreitenzeichen oder einer Bidi-Überschreibung) werden
abgelehnt.

Ein Tag entfernen
=================

Anfrage
-------

==================  ====================================================
HTTP-Methode        DELETE
Endpunkt            ``/api/v2/documents/{docId}/tags?value=<Tag-Wert>``
==================  ====================================================

Entfernt den angemeldeten Benutzer aus den Berechtigungen des mit ``value`` angegebenen Tags. Bleibt
keine Berechtigung eines Benutzers, einer Gruppe oder einer Rolle übrig, wird das Tag gelöscht und aus
den Dokumenten entfernt. Gehört der Benutzer nicht zu den Berechtigungen des Tags, antwortet der
Endpunkt mit ``forbidden`` (403). Der Header ``X-Fess-CSRF-Token`` ist erforderlich.

Fehlerantwort
=============

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Fehlerantwort

   * - Statuscode
     - Beschreibung
   * - 400 Bad Request
     - Wenn die Anfrage ungültig ist (auch wenn Tags deaktiviert sind, der Tag-Name ungültig ist oder
       ein Tag-Limit überschritten wird).
   * - 401 Unauthorized
     - POST oder DELETE ohne Anmeldung.
   * - 403 Forbidden
     - Ein fehlendes oder abgelaufenes CSRF-Token oder ein DELETE eines Tags, das der Benutzer nicht
       hinzugefügt hat.
   * - 404 Not Found
     - Wenn das Dokument nicht gefunden wird oder der Aufrufer es nicht durchsuchen kann.
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht zulässig ist.
   * - 413 Payload Too Large
     - Wenn der Anfrage-Body die Größenbegrenzung überschreitet.
   * - 415 Unsupported Media Type
     - Wenn der ``Content-Type`` nicht unterstützt wird.
   * - 500 Internal Server Error
     - Wenn ein interner Serverfehler auftritt.

Tabelle: Fehlerantwort
