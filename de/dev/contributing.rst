========================
Leitfaden für Beiträge
========================

Wir begrüßen Beiträge zum |Fess|-Projekt!
Diese Seite erklärt, wie Sie zu |Fess| beitragen können, Community-Richtlinien,
Schritte zum Erstellen von Pull Requests usw.

.. contents:: Inhaltsverzeichnis
   :local:
   :depth: 2

Einführung
======

|Fess| ist ein Open-Source-Projekt und
wächst durch die Beiträge der Community.
Jeder kann beitragen, unabhängig vom Erfahrungsniveau in der Programmierung.

Möglichkeiten beizutragen
========

Sie können auf verschiedene Weise zu |Fess| beitragen.

Code-Beiträge
----------

- Hinzufügen neuer Funktionen
- Fehlerbehebungen
- Performance-Verbesserungen
- Refactoring
- Hinzufügen von Tests

Dokumentations-Beiträge
----------------

- Verbesserung der Benutzerhandbücher
- Hinzufügen/Aktualisieren von API-Dokumentation
- Erstellen von Tutorials
- Übersetzungen

Issue-Berichterstattung
-----------

- Fehlerberichte
- Feature-Anfragen
- Fragen oder Vorschläge

Community-Aktivitäten
--------------

- Diskussionen in GitHub Discussions
- Beantworten von Fragen in Foren
- Schreiben von Blogbeiträgen oder Tutorials
- Präsentationen bei Veranstaltungen

Erster Beitrag
==========

Wenn Sie zum ersten Mal zu |Fess| beitragen, empfehlen wir die folgenden Schritte.

Schritt 1: Das Projekt verstehen
---------------------------

1. Überprüfen Sie grundlegende Informationen auf der `offiziellen Fess-Website <https://fess.codelibs.org/ja/>`__
2. Verstehen Sie den Entwicklungsüberblick unter :doc:`getting-started`
3. Lernen Sie die Codestruktur unter :doc:`architecture`

Schritt 2: Nach Issues suchen
-------------------

Suchen Sie auf der `GitHub-Issue-Seite <https://github.com/codelibs/fess/issues>`__ nach
Issues mit dem Label ``good first issue``.

Diese Issues sind relativ einfache Aufgaben, die für Erstbeiträger geeignet sind.

Schritt 3: Entwicklungsumgebung einrichten
----------------------------

Richten Sie Ihre Entwicklungsumgebung gemäß :doc:`setup` ein.

Schritt 4: Branch erstellen und arbeiten
----------------------------

Erstellen Sie gemäß :doc:`workflow` einen Branch und beginnen Sie mit dem Codieren.

Schritt 5: Pull Request erstellen
--------------------------

Committen Sie Ihre Änderungen und erstellen Sie einen Pull Request.

Codierungskonventionen
==============

|Fess| folgt den folgenden Codierungskonventionen, um konsistenten Code zu pflegen.

Java-Codierungsstil
----------------------

Grundstil
~~~~~~~~~~

- **Einrückung**: 4 Leerzeichen
- **Zeilenumbruch**: LF (Unix-Stil)
- **Kodierung**: UTF-8
- **Zeilenlänge**: maximal 120 Zeichen empfohlen

Namenskonventionen
~~~~~~

- **Pakete**: Kleinbuchstaben, durch Punkte getrennt (z. B.: ``org.codelibs.fess``)
- **Klassen**: PascalCase (z. B.: ``SearchService``)
- **Schnittstellen**: PascalCase (z. B.: ``Crawler``)
- **Methoden**: camelCase (z. B.: ``executeSearch``)
- **Variablen**: camelCase (z. B.: ``searchResult``)
- **Konstanten**: UPPER_SNAKE_CASE (z. B.: ``MAX_SEARCH_SIZE``)

Kommentare
~~~~~~

**Javadoc:**

Schreiben Sie Javadoc für öffentliche Klassen, Methoden und Felder.

.. code-block:: java

    /**
     * Führt die Suche aus.
     *
     * @param query Suchanfrage
     * @return Suchergebnisse
     * @throws SearchException Wenn die Suche fehlschlägt
     */
    public SearchResponse executeSearch(String query) throws SearchException {
        // Implementierung
    }

**Implementierungskommentare:**

Fügen Sie für komplexe Logik Kommentare auf Japanisch oder Englisch hinzu.

.. code-block:: java

    // Normalisierung der Abfrage (Konvertierung von Vollbreite zu Halbbreite)
    String normalizedQuery = QueryNormalizer.normalize(query);

Klassen- und Methodendesign
~~~~~~~~~~~~~~~~~~~~

- **Prinzip der einzigen Verantwortung**: Eine Klasse hat nur eine Verantwortung
- **Kleine Methoden**: Eine Methode macht nur eine Sache
- **Aussagekräftige Namen**: Klassen- und Methodennamen sollten ihre Absicht deutlich machen

Ausnahmebehandlung
~~~~~~

.. code-block:: java

    // Gutes Beispiel: Angemessene Ausnahmebehandlung
    try {
        executeSearch(query);
    } catch (IOException e) {
        logger.error("Fehler während der Suche aufgetreten", e);
        throw new SearchException("Suche fehlgeschlagen", e);
    }

    // Zu vermeidendes Beispiel: Leerer catch-Block
    try {
        executeSearch(query);
    } catch (IOException e) {
        // Nichts tun
    }

Umgang mit null
~~~~~~~~~

- Vermeiden Sie nach Möglichkeit die Rückgabe von ``null``
- Verwendung von ``Optional`` wird empfohlen
- Kennzeichnen Sie null-Möglichkeit explizit mit ``@Nullable``-Annotation

.. code-block:: java

    // Gutes Beispiel
    public Optional<User> findUser(String id) {
        return Optional.ofNullable(userMap.get(id));
    }

    // Verwendungsbeispiel
    findUser("123").ifPresent(user -> {
        // Verarbeitung, wenn Benutzer existiert
    });

Schreiben von Tests
~~~~~~~~~~

- Schreiben Sie Tests für alle öffentlichen Methoden
- Testmethodennamen beginnen mit ``test``
- Verwenden Sie das Given-When-Then-Muster

.. code-block:: java

    @Test
    public void testSearch() {
        // Given: Testvoraussetzungen
        SearchService service = new SearchService();
        String query = "test";

        // When: Ausführung des Testobjekts
        SearchResponse response = service.search(query);

        // Then: Überprüfung der Ergebnisse
        assertNotNull(response);
        assertEquals(10, response.getDocuments().size());
    }

Code-Review-Richtlinien
========================

Pull-Request-Review-Prozess
----------------------------

1. **Automatische Überprüfung**: CI führt automatisch Builds und Tests aus
2. **Code-Review**: Betreuer überprüfen den Code
3. **Feedback**: Änderungsanfragen bei Bedarf
4. **Genehmigung**: Review wird genehmigt
5. **Merge**: Betreuer merged in den main-Branch

Review-Aspekte
----------

Im Review werden folgende Punkte überprüft:

**Funktionalität**

- Erfüllt es die Anforderungen
- Funktioniert es wie beabsichtigt
- Werden Randfälle berücksichtigt

**Code-Qualität**

- Entspricht es den Codierungskonventionen
- Ist der Code lesbar und wartbar
- Ist die Abstraktion angemessen

**Tests**

- Sind ausreichende Tests geschrieben
- Bestehen die Tests
- Führen die Tests sinnvolle Überprüfungen durch

**Performance**

- Gibt es Auswirkungen auf die Performance
- Ist die Ressourcennutzung angemessen

**Sicherheit**

- Gibt es Sicherheitsprobleme
- Ist die Eingabevalidierung angemessen

**Dokumentation**

- Ist die erforderliche Dokumentation aktualisiert
- Ist Javadoc angemessen geschrieben

Antworten auf Review-Kommentare
--------------------

Reagieren Sie auf Review-Kommentare zeitnah und höflich.

**Wenn Änderungen erforderlich sind:**

.. code-block:: text

    Vielen Dank für Ihren Hinweis. Ich habe es korrigiert.
    [Kurze Beschreibung der Änderungen]

**Wenn Diskussion erforderlich ist:**

.. code-block:: text

    Vielen Dank für Ihre Meinung.
    Aus Gründen von XX habe ich die aktuelle Implementierung gewählt,
    wäre die Implementierung von YY besser?

Best Practices für Pull Requests
================================

Größe der PR
---------

- Erstellen Sie kleine, leicht zu überprüfende PRs
- Eine PR sollte eine logische Änderung enthalten
- Teilen Sie große Änderungen in mehrere PRs auf

PR-Titel
-----------

Geben Sie einen klaren und beschreibenden Titel an:

.. code-block:: text

    feat: Filterfunktion für Suchergebnisse hinzugefügt
    fix: Timeout-Problem des Crawlers behoben
    docs: API-Dokumentation aktualisiert

PR-Beschreibung
-------

Fügen Sie folgende Informationen hinzu:

- **Änderungsinhalt**: Was wurde geändert
- **Grund**: Warum diese Änderung notwendig ist
- **Testmethode**: Wie wurde es getestet
- **Screenshots**: Bei UI-Änderungen
- **Zugehöriges Issue**: Issue-Nummer (z. B.: Closes #123)

.. code-block:: markdown

    ## Änderungsinhalt
    Funktion zum Filtern von Suchergebnissen nach Dateityp hinzugefügt.

    ## Grund
    Viele Benutzeranfragen nach "Suche nur nach bestimmten Dateitypen".

    ## Testmethode
    1. Dateityp-Filter auf der Suchseite auswählen
    2. Suche ausführen
    3. Überprüfen, dass nur Ergebnisse des ausgewählten Dateityps angezeigt werden

    ## Zugehöriges Issue
    Closes #123

Commit-Nachrichten
----------------

Schreiben Sie klare und beschreibende Commit-Nachrichten:

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**Beispiel:**

.. code-block:: text

    feat: Suchfilterfunktion hinzugefügt

    Benutzer können jetzt Suchergebnisse nach Dateityp filtern.

    - Filter-UI hinzugefügt
    - Backend-Filterverarbeitung implementiert
    - Tests hinzugefügt

    Closes #123

Verwendung von Draft-PRs
--------------

Erstellen Sie PRs, an denen Sie noch arbeiten, als Draft-PR und
ändern Sie sie zu "Ready for review", wenn sie fertig sind.

.. code-block:: text

    1. Wählen Sie beim Erstellen der PR "Create draft pull request"
    2. Klicken Sie auf "Ready for review", wenn die Arbeit abgeschlossen ist

Community-Richtlinien
======================

Verhaltenskodex
------

Die |Fess|-Community hält sich an folgenden Verhaltenskodex:

- **Respektvoll sein**: Respektieren Sie alle Menschen
- **Kooperativ sein**: Geben Sie konstruktives Feedback
- **Offen sein**: Begrüßen Sie unterschiedliche Perspektiven und Erfahrungen
- **Höflich sein**: Verwenden Sie höfliche Sprache

Kommunikation
----------------

**Wo Sie Fragen stellen können:**

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: Allgemeine Fragen und Diskussionen
- `Issue-Tracker <https://github.com/codelibs/fess/issues>`__: Fehlerberichte und Feature-Anfragen
- `Fess-Forum <https://discuss.codelibs.org/c/FessJA>`__: Japanisches Forum

**Wie man Fragen stellt:**

- Fragen Sie konkret
- Erklären Sie, was Sie versucht haben
- Fügen Sie Fehlermeldungen oder Logs hinzu
- Geben Sie Umgebungsinformationen an (OS, Java-Version usw.)

**Wie man antwortet:**

- Höflich und freundlich
- Geben Sie konkrete Lösungen an
- Bieten Sie Links zu Referenzmaterialien

Dankbarkeit ausdrücken
--------

Wir drücken Dankbarkeit für Beiträge aus.
Auch kleine Beiträge sind für das Projekt wertvoll.

Häufig gestellte Fragen
==========

F: Können auch Anfänger beitragen?
---------------------------

A: Ja, herzlich willkommen! Wir empfehlen, mit Issues zu beginnen, die das Label ``good first issue`` haben.
Auch die Verbesserung der Dokumentation ist ein für Anfänger geeigneter Beitrag.

F: Wie schnell werden Pull Requests überprüft?
-------------------------------------------------

A: Normalerweise innerhalb weniger Tage.
Dies kann jedoch je nach Zeitplan der Betreuer variieren.

F: Was passiert, wenn ein Pull Request abgelehnt wird?
-----------------------------------

A: Überprüfen Sie den Grund für die Ablehnung und Sie können ihn nach Änderungen erneut einreichen.
Wenn Sie unsicher sind, fragen Sie gerne nach.

F: Was passiert, wenn ich gegen Codierungskonventionen verstoße?
---------------------------------------

A: Es wird im Review darauf hingewiesen, also ist es kein Problem, wenn Sie es korrigieren.
Sie können es vorab überprüfen, indem Sie Checkstyle ausführen.

F: Was ist, wenn ich eine große Funktion hinzufügen möchte?
-------------------------------

A: Wir empfehlen, zuerst ein Issue zu erstellen und den Vorschlag zu diskutieren.
Durch vorherige Einigung können Sie verschwenderische Arbeit vermeiden.

F: Darf ich auf Japanisch fragen?
-------------------------------

A: Ja, sowohl Japanisch als auch Englisch sind in Ordnung.
Fess ist ein Projekt aus Japan, daher gibt es auch gute japanische Unterstützung.

Leitfaden nach Art des Beitrags
================

Verbesserung der Dokumentation
----------------

1. Forken Sie das Dokumentations-Repository:

   .. code-block:: bash

       git clone https://github.com/codelibs/fess-docs.git

2. Nehmen Sie Änderungen vor
3. Erstellen Sie einen Pull Request

Fehlerbericht
------

1. Suchen Sie nach vorhandenen Issues, um Duplikate zu vermeiden
2. Erstellen Sie ein neues Issue
3. Fügen Sie folgende Informationen hinzu:

   - Fehlerbeschreibung
   - Schritte zur Reproduktion
   - Erwartetes Verhalten
   - Tatsächliches Verhalten
   - Umgebungsinformationen

Feature-Anfrage
------------

1. Erstellen Sie ein Issue
2. Erklären Sie Folgendes:

   - Beschreibung der Funktion
   - Hintergrund und Motivation
   - Vorgeschlagene Implementierungsmethode (optional)

Code-Review
------------

Die Überprüfung der Pull Requests anderer Personen ist ebenfalls ein Beitrag:

1. Finden Sie eine interessante PR
2. Überprüfen Sie den Code
3. Geben Sie konstruktives Feedback

Lizenz
========

|Fess| wird unter der Apache License 2.0 veröffentlicht.
Beigesteuerte Code unterliegt derselben Lizenz.

Durch das Erstellen eines Pull Requests stimmen Sie zu,
dass Ihr Beitrag unter dieser Lizenz veröffentlicht wird.

Danksagung
====

Vielen Dank für Ihren Beitrag zum |Fess|-Projekt!
Ihr Beitrag macht |Fess| zu einer besseren Software.

Nächste Schritte
==========

Wenn Sie bereit sind, beizutragen:

1. Richten Sie Ihre Entwicklungsumgebung mit :doc:`setup` ein
2. Überprüfen Sie den Entwicklungsablauf mit :doc:`workflow`
3. Suchen Sie nach Issues auf `GitHub <https://github.com/codelibs/fess>`__

Referenzmaterialien
======

- `GitHub Flow <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `Wie man zu Open Source beiträgt <https://opensource.guide/ja/how-to-contribute/>`__
- `Wie man gute Commit-Nachrichten schreibt <https://chris.beams.io/posts/git-commit/>`__

Community-Ressourcen
==================

- **GitHub**: `codelibs/fess <https://github.com/codelibs/fess>`__
- **Discussions**: `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- **Forum**: `Fess-Forum <https://discuss.codelibs.org/c/FessJA>`__
- **Twitter**: `@codelibs <https://twitter.com/codelibs>`__
- **Website**: `fess.codelibs.org <https://fess.codelibs.org/ja/>`__
