==================
Verwandte Abfragen
==================

Übersicht
=========

Hier wird die Konfiguration verwandter Abfragen erläutert.
Sie können Suchergebnisse mit registrierten verwandten Abfragen verbessern.
Verwandte Abfragen können als Alternativbegriffe für Suchbegriffe verwendet werden.


Verwaltung
==========

Anzeige
-------

Um die Übersichtsseite für die Konfiguration verwandter Abfragen zu öffnen, klicken Sie im linken Menü auf [Crawler > Verwandte Abfrage].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Konfigurationsseite für verwandte Abfragen zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Begriff
:::::::

Geben Sie den Suchbegriff an, mit dem die Suchabfrage übereinstimmen soll.

Abfragen
::::::::

Geben Sie die Abfrage an.

Virtueller Host
:::::::::::::::

Geben Sie den Hostnamen des virtuellen Hosts an.
Weitere Details finden Sie unter :doc:`Virtueller Host im Konfigurationshandbuch <../config/security-virtual-host>`.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

Aus Suchprotokollen generieren
------------------------------

Klicken Sie auf der Listenseite auf [Aus Suchprotokollen generieren], um verwandte Abfragen aus den
letzten Suchprotokollen zu erstellen. Eine Suche, die dieselbe Benutzersitzung kurz nach einer
anderen Suche ausführt (ein Tippfehler gefolgt von seiner Korrektur oder ein allgemeiner Begriff
gefolgt von einem genaueren), gilt als Verfeinerung. Für häufig gesuchte Begriffe werden die
häufigsten Verfeinerungen zu den verwandten Abfragen des Begriffs.

Verwandte Abfragen gelten für alle Benutzer und erweitern jede Suche nach ihrem Begriff; die
Generierung ist daher zurückhaltend:

- Es werden nur Suchen verwendet, die ein Gast sehen kann. Ein Suchprotokoll wird nur gelesen, wenn
  alle seine Rollen ``suggest.search.log.permissions`` erfüllen (dieselbe Einstellung wie bei Suggest).
- Suchbegriffe mit einem Feldfilter wie ``label:"x"``, Operatoren, Platzhaltern, ``sort:`` oder
  einem führenden ``+`` / ``-`` werden nicht verwendet.
- Wörter, die unter [Vorschlagen > Schlechtes Wort] registriert sind, werden weder als Begriff noch als
  verwandte Abfrage verwendet.
- Ein Begriff und jede seiner verwandten Abfragen müssen aus mindestens
  ``related_query.generate.min.sessions`` Sitzungen stammen, und die Verfeinerungen müssen Treffer
  haben.
- Einträge werden für jeden virtuellen Host getrennt erzeugt. Suchprotokolle ohne virtuellen Host
  gelten als Standardhost.
- Begriffe, die bereits verwandte Abfragen haben, werden nicht verändert (das Ergebnis nennt die
  Anzahl der übersprungenen), und es werden nicht mehr Einträge erzeugt, als der Cache der
  verwandten Abfragen laden kann (``page.relatedquery.max.fetch.size``).

Erzeugte verwandte Abfragen lassen sich wie manuell registrierte bearbeiten oder löschen. Sie
können nicht erzeugt werden, solange „Suchprotokoll“ oder „Benutzerprotokoll“ unter
[System > Allgemein] deaktiviert ist, und ein zweiter Lauf kann nicht starten, während einer läuft.

Die folgenden Einstellungen in ``fess_config.properties`` steuern die Generierung.

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``related_query.generate.days``
     - Anzahl der Tage an Suchprotokollen, die gelesen werden
     - ``30``
   * - ``related_query.generate.term.size``
     - Höchstzahl an Begriffen je virtuellem Host
     - ``100``
   * - ``related_query.generate.query.size``
     - Höchstzahl an verwandten Abfragen je Begriff
     - ``5``
   * - ``related_query.generate.min.sessions``
     - Mindestzahl an Sitzungen, in denen ein Begriff und seine verwandte Abfrage vorkommen müssen
     - ``3``
   * - ``related_query.generate.session.interval``
     - Zeitraum, in dem eine Suche als Verfeinerung gilt (Minuten)
     - ``10``
   * - ``related_query.generate.seed.log.size``
     - Höchstzahl der je Begriff gelesenen Suchprotokolle
     - ``1000``
   * - ``related_query.generate.seed.session.size``
     - Höchstzahl der je Begriff gelesenen Sitzungen
     - ``200``
   * - ``related_query.generate.log.fetch.size``
     - Höchstzahl der je Begriff gelesenen Folgesuchen
     - ``2000``
   * - ``related_query.generate.query.min.length``
     - Mindestlänge eines Begriffs und einer verwandten Abfrage (Zeichen)
     - ``2``
   * - ``related_query.generate.query.max.length``
     - Höchstlänge eines Begriffs und einer verwandten Abfrage (Zeichen)
     - ``50``

.. |image0| image:: ../../../resources/images/en/15.9/admin/relatedquery-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/relatedquery-2.png
