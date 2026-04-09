===========================================================================
Teil 9: Suchinfrastruktur fuer mehrsprachige Organisationen -- Aufbau einer Umgebung zur korrekten Suche in japanischen, englischen und chinesischen Dokumenten
===========================================================================

Einfuehrung
============

In Unternehmen, die global taetig sind, oder in Organisationen mit Mitarbeitern verschiedener Nationalitaeten werden interne Dokumente in mehreren Sprachen erstellt.
Eine Suchinfrastruktur, die Dokumente in gemischten Sprachen -- wie japanische Sitzungsprotokolle, englische technische Spezifikationen und chinesische Marktberichte -- angemessen durchsuchen kann, ist unerlaeasslich.

In diesem Artikel gehen wir von einer Umgebung aus, in der Dokumente auf Japanisch, Englisch und Chinesisch nebeneinander existieren, und bauen eine Umgebung auf, in der Dokumente in jeder Sprache korrekt durchsucht werden koennen.

Zielgruppe
==========

- Administratoren von Organisationen, die mehrsprachige Dokumente verwalten
- Personen, die die Suchqualitaet fuer andere Sprachen als Japanisch verbessern moechten
- Personen, die die Grundlagen von Volltext-Analyzern erlernen moechten

Szenario
========

Wir gehen von einem Unternehmen mit Standorten in Japan, den USA und China aus.

- Standort Japan: Erstellung japanischer Dokumente (Spezifikationen, Sitzungsprotokolle, Berichte)
- Standort USA: Erstellung englischer Dokumente (technische Dokumente, Praesentationsmaterialien)
- Standort China: Erstellung chinesischer Dokumente (Marktforschung, Geschaeftspartnerinformationen)
- Gemeinsam: Globale Richtliniendokumente in englischer Sprache

Das Ziel ist es, eine Umgebung zu schaffen, in der Mitarbeiter an jedem Standort Dokumente unabhaengig von der Sprache durchsuchen koennen.

Grundlagen der mehrsprachigen Suche
=====================================

Sprachverarbeitung in der Volltextsuche
----------------------------------------

Damit eine Volltextsuchmaschine Dokumente durchsuchbar machen kann, muss sie Text in sogenannte ``Token`` (durchsuchbare Einheiten) aufteilen.
Dieser Vorgang wird als ``Tokenisierung`` bezeichnet.

Die Methode der Tokenisierung unterscheidet sich je nach Sprache erheblich.

**Englisch**: Durch Leerzeichen getrennte Woerter werden direkt zu Token.
Zusaetzlich werden Stemming (z. B. running -> run) und Kleinschreibung angewendet.

**Japanisch**: Da Woerter nicht durch Leerzeichen getrennt sind, wird ein morphologischer Analysator (wie Kuromoji) verwendet, um den Text in Woerter aufzuteilen.
Zum Beispiel wird ein Ausdruck wie folgt aufgeteilt: ``Volltextsuchserver`` -> ``Volltext`` ``Such`` ``Server``.

**Chinesisch**: Wie im Japanischen sind die Woerter nicht durch Leerzeichen getrennt, sodass ein spezieller Tokenizer erforderlich ist. Fess verwendet einen eigenen chinesischen Tokenizer fuer die Verarbeitung.

Mehrsprachige Unterstuetzung von Fess
---------------------------------------

Fess verwendet OpenSearch als Backend und kann die von OpenSearch bereitgestellten mehrsprachigen Analyzer nutzen.
In der Standardkonfiguration von Fess ist der japanische (Kuromoji) Analyzer aktiviert, es werden jedoch auch andere Sprachen unterstuetzt.

Fess verfuegt ueber Indexeinstellungen fuer ueber 20 Sprachen und bietet eine Funktion, die die Sprache eines Dokuments automatisch erkennt und den entsprechenden Analyzer anwendet.

Sprachspezifische Einstellungen
================================

Einstellungen fuer Japanisch
------------------------------

Japanische Dokumente werden mit dem Kuromoji Analyzer verarbeitet.
Da Japanisch durch die Standardeinstellungen von Fess angemessen verarbeitet wird, ist keine spezielle zusaetzliche Konfiguration erforderlich.

Die Suchqualitaet kann jedoch durch die folgenden Anpassungen verbessert werden.

**Benutzerlexikon**

Registrieren Sie branchenspezifische Begriffe und interne Terminologie im Woerterbuch.
Dies kann ueber die Administrationsoberflaeche unter [System] > [Woerterbuch] durch Auswahl des Kuromoji-Woerterbuchs konfiguriert werden.

Dies ist beispielsweise nuetzlich, wenn Sie moechten, dass ein zusammengesetzter Begriff als einzelnes Token behandelt wird, anstatt in separate Woerter aufgeteilt zu werden.

**Synonyme**

Behandlung von japanischspezifischen Schreibvarianten.

::

    サーバー,サーバ
    データベース,DB,ディービー
    ユーザー,ユーザ,利用者

Einstellungen fuer Englisch
-----------------------------

Englische Dokumente werden durch den mehrsprachigen Index von Fess automatisch mit dem entsprechenden Analyzer verarbeitet.

Englischspezifische Anpassungen umfassen Folgendes.

**Stoppwoerter**

Gaengige englische Stoppwoerter (the, a, an, is, are usw.) werden standardmaessig ausgeschlossen. Es koennen jedoch auch branchenspezifische Stoppwoerter hinzugefuegt werden.

**Stemmer-Override**

Ueberschreiben Sie das Stemming bestimmter Woerter.
Dies kann ueber die Administrationsoberflaeche unter [System] > [Woerterbuch] durch Auswahl des Stemmer-Override-Woerterbuchs konfiguriert werden.

Dies wird beispielsweise verwendet, wenn Fachbegriffe unbeabsichtigte Transformationen erfahren.

Einstellungen fuer Chinesisch
-------------------------------

Fuer chinesische Dokumente wird der Fess-eigene chinesische Tokenizer verwendet.
Im mehrsprachigen Index von Fess werden sowohl vereinfachte als auch traditionelle chinesische Texte korrekt tokenisiert.

Chinesischspezifische Ueberlegungen umfassen Folgendes.

- Zuordnung zwischen vereinfachten und traditionellen chinesischen Zeichen
- Suchunterstuetzung ueber Pinyin-Eingabe
- Chinesischspezifische Synonymeinstellungen

Sucherlebnis in einer mehrsprachigen Umgebung
==============================================

Ueberlegungen zur Such-UI
---------------------------

In einer mehrsprachigen Umgebung muss auch die Such-UI an die Sprache des Benutzers angepasst werden.

Fess verfuegt ueber eine Funktion, die die UI-Sprache automatisch basierend auf den Spracheinstellungen des Browsers umschaltet.
Die Suchoberflaeche wird in mehreren Sprachen bereitgestellt, darunter Japanisch, Englisch und Chinesisch.

Ueberlegungen zur sprachuebergreifenden Suche
-----------------------------------------------

Es besteht auch der Bedarf an sprachuebergreifender Suche, z. B. ``englische Dokumente mit japanischen Suchbegriffen finden``.
Derzeit unterstuetzt Fess allein keine vollstaendig automatische uebersetzungsbasierte Suche, aber die folgenden Methoden koennen diesen Bedarf teilweise abdecken.

**Mehrsprachige Synonymeinstellungen**

Registrieren Sie Uebersetzungen zwischen Japanisch und Englisch als Synonyme.

::

    会議,meeting,ミーティング
    報告書,report,レポート
    仕様書,specification,スペック

Dadurch werden bei einer Suche nach dem japanischen Wort fuer ``Meeting`` auch englische Dokumente gefunden, die ``meeting`` enthalten.

**Sprachfilterung mit Labels**

Richten Sie Labels fuer jede Sprache ein, damit Benutzer den Sprachbereich ihrer Suche auswaehlen koennen.

- ``lang-ja``: Japanische Dokumente
- ``lang-en``: Englische Dokumente
- ``lang-zh``: Chinesische Dokumente

Best Practices fuer die Woerterbuchverwaltung
===============================================

In einer mehrsprachigen Umgebung hat die Woerterbuchverwaltung einen erheblichen Einfluss auf die Suchqualitaet.

Woerterbuchpflege nach Sprache
--------------------------------

.. list-table:: Punkte zur Woerterbuchpflege
   :header-rows: 1
   :widths: 20 40 40

   * - Woerterbuch
     - Japanisch
     - Englisch / Chinesisch
   * - Synonyme
     - Schreibvarianten, Abkuerzungen, Fachbegriffe
     - Abkuerzungserweiterung, Synonyme
   * - Stoppwoerter
     - Branchenspezifische ueberfluessige Woerter
     - Domaenenspezifische ueberfluessige Woerter
   * - Benutzerlexikon
     - Interne Begriffe, Produktnamen
     - (Kuromoji-spezifisch)
   * - Protwords (Geschuetzte Woerter)
     - Woerter, die nicht gestemmt werden sollen
     - Fachbegriffe, Eigennamen

Regelmaessige Woerterbuchpflege
---------------------------------

Woerterbuecher sind nicht etwas, das man einmal einrichtet und dann vergisst; sie muessen regelmaessig ueberprueft werden.

- Neue Produkt- und Projektnamen hinzufuegen
- Nicht mehr verwendete Begriffe bereinigen
- Neue Synonymkandidaten aus Suchprotokollen hinzufuegen

Kombinieren Sie dies mit dem in Teil 8 vorgestellten Zyklus zur Optimierung der Suchqualitaet, um Woerterbuecher kontinuierlich zu pflegen.

Zusammenfassung
================

In diesem Artikel haben wir den Aufbau einer Suchinfrastruktur in einer Umgebung erlaeutert, in der japanische, englische und chinesische Dokumente koexistieren.

- Verstaendnis der unterschiedlichen Tokenisierungsprozesse fuer jede Sprache
- Mehrsprachiger Index und Analyzer-Einstellungen von Fess
- Anpassungen fuer Japanisch (Kuromoji), Englisch und Chinesisch
- Unterstuetzung der sprachuebergreifenden Suche durch mehrsprachige Synonyme
- Best Practices fuer die Woerterbuchverwaltung

Mehrsprachige Unterstuetzung ist nicht etwas, das mit einer einmaligen Konfiguration abgeschlossen werden kann; eine kontinuierliche Verbesserung basierend auf den Nutzungsmustern ist wichtig.

Im naechsten Artikel behandeln wir den stabilen Betrieb von Suchsystemen.

Referenzen
==========

- `Fess Woerterbuchverwaltung <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__

- `OpenSearch Analyzer <https://opensearch.org/docs/latest/analyzers/>`__
