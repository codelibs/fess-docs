==============
Entwicklungsworkflow
==============

Diese Seite erklärt den Standard-Workflow für die |Fess|-Entwicklung.
Sie können den Ablauf von Entwicklungsarbeiten wie Funktionserweiterungen, Fehlerbehebungen, Tests und Code-Reviews lernen.

.. contents:: Inhaltsverzeichnis
   :local:
   :depth: 2

Grundlegender Entwicklungsablauf
==============

Die Entwicklung von |Fess| folgt diesem Ablauf:

.. code-block:: text

    1. Überprüfung/Erstellung von Issues
       ↓
    2. Erstellung eines Branches
       ↓
    3. Codierung
       ↓
    4. Ausführung lokaler Tests
       ↓
    5. Commit
       ↓
    6. Push
       ↓
    7. Erstellung eines Pull Requests
       ↓
    8. Code-Review
       ↓
    9. Antwort auf Review-Feedback
       ↓
    10. Merge

Jeder Schritt wird im Detail erklärt.

Schritt 1: Überprüfung/Erstellung von Issues
=========================

Überprüfen Sie vor Beginn der Entwicklung die GitHub-Issues.

Überprüfung vorhandener Issues
-----------------

1. Besuchen Sie die `Fess-Issue-Seite <https://github.com/codelibs/fess/issues>`__
2. Suchen Sie nach Issues, an denen Sie arbeiten möchten
3. Kommentieren Sie das Issue, um mitzuteilen, dass Sie mit der Arbeit beginnen

.. tip::

   Für Ihren ersten Beitrag empfehlen wir, mit Issues zu beginnen, die das Label ``good first issue`` haben.

Erstellung eines neuen Issues
-----------------

Erstellen Sie bei neuen Funktionen oder Fehlerbehebungen ein Issue.

1. Klicken Sie auf `New Issue <https://github.com/codelibs/fess/issues/new>`__
2. Wählen Sie eine Issue-Vorlage
3. Füllen Sie die erforderlichen Informationen aus:

   - **Titel**: Klare und verständliche Beschreibung
   - **Beschreibung**: Detaillierter Hintergrund, erwartetes Verhalten, aktuelles Verhalten
   - **Reproduktionsschritte**: Bei Bugs
   - **Umgebungsinformationen**: OS, Java-Version, Fess-Version usw.

4. Klicken Sie auf ``Submit new issue``

Issue-Vorlagen
~~~~~~~~~~~~~~~~~~

**Fehlerbericht:**

.. code-block:: markdown

    ## Problembeschreibung
    Kurze Beschreibung des Bugs

    ## Reproduktionsschritte
    1. ...
    2. ...
    3. ...

    ## Erwartetes Verhalten
    Was sollte passieren

    ## Tatsächliches Verhalten
    Was tatsächlich passiert

    ## Umgebung
    - OS:
    - Java-Version:
    - Fess-Version:

**Feature-Anfrage:**

.. code-block:: markdown

    ## Funktionsbeschreibung
    Beschreibung der hinzuzufügenden Funktion

    ## Hintergrund und Motivation
    Warum diese Funktion benötigt wird

    ## Vorgeschlagene Implementierungsmethode
    Wie sie implementiert werden soll (optional)

Schritt 2: Erstellung eines Branches
====================

Erstellen Sie einen Arbeits-Branch.

Branch-Namenskonventionen
--------------

Branch-Namen folgen diesem Format:

.. code-block:: text

    <type>/<issue-number>-<short-description>

**Typen:**

- ``feature``: Hinzufügen neuer Funktionen
- ``fix``: Fehlerbehebung
- ``refactor``: Refactoring
- ``docs``: Dokumentationsaktualisierung
- ``test``: Hinzufügen/Ändern von Tests

**Beispiele:**

.. code-block:: bash

    # Hinzufügen einer neuen Funktion
    git checkout -b feature/123-add-search-filter

    # Fehlerbehebung
    git checkout -b fix/456-fix-crawler-timeout

    # Dokumentationsaktualisierung
    git checkout -b docs/789-update-api-docs

Schritte zur Branch-Erstellung
----------------

1. Holen Sie sich den neuesten main-Branch:

   .. code-block:: bash

       git checkout main
       git pull origin main

2. Erstellen Sie einen neuen Branch:

   .. code-block:: bash

       git checkout -b feature/123-add-search-filter

3. Überprüfen Sie, dass der Branch erstellt wurde:

   .. code-block:: bash

       git branch

Schritt 3: Codierung
==================

Implementieren Sie Funktionen oder beheben Sie Fehler.

Codierungskonventionen
--------------

|Fess| folgt den folgenden Codierungskonventionen.

Grundlegender Stil
~~~~~~~~~~~~~~

- **Einrückung**: 4 Leerzeichen
- **Zeilenlänge**: maximal 120 Zeichen empfohlen
- **Kodierung**: UTF-8
- **Zeilenumbruch**: LF (Unix-Stil)

Namenskonventionen
~~~~~~

- **Klassennamen**: PascalCase (z. B.: ``SearchService``)
- **Methodennamen**: camelCase (z. B.: ``executeSearch``)
- **Konstanten**: UPPER_SNAKE_CASE (z. B.: ``MAX_SEARCH_SIZE``)
- **Variablen**: camelCase (z. B.: ``searchResults``)

Kommentare
~~~~~~

- **Javadoc**: Erforderlich für öffentliche Klassen und Methoden
- **Implementierungskommentare**: Fügen Sie Erklärungen auf Japanisch oder Englisch für komplexe Logik hinzu

**Beispiel:**

.. code-block:: java

    /**
     * Führt die Suche aus.
     *
     * @param query Suchanfrage
     * @return Suchergebnisse
     */
    public SearchResponse executeSearch(String query) {
        // Abfrage normalisieren
        String normalizedQuery = normalizeQuery(query);

        // Suche ausführen
        return searchEngine.search(normalizedQuery);
    }

Umgang mit null
~~~~~~~~~

- Vermeiden Sie nach Möglichkeit die Rückgabe von ``null``
- Verwendung von ``Optional`` wird empfohlen
- Führen Sie null-Prüfungen explizit durch

**Beispiel:**

.. code-block:: java

    // Gutes Beispiel
    public Optional<User> findUser(String id) {
        return userRepository.findById(id);
    }

    // Zu vermeidendes Beispiel
    public User findUser(String id) {
        return userRepository.findById(id);  // Möglichkeit von null
    }

Ausnahmebehandlung
~~~~~~

- Fangen und behandeln Sie Ausnahmen angemessen
- Protokollieren Sie Ausgaben
- Geben Sie Benutzern verständliche Nachrichten

**Beispiel:**

.. code-block:: java

    try {
        // Verarbeitung
    } catch (IOException e) {
        logger.error("Dateilesefehler", e);
        throw new FessSystemException("Datei konnte nicht gelesen werden", e);
    }

Logging
~~~~~~

Verwenden Sie angemessene Log-Ebenen:

- ``ERROR``: Bei Fehlern
- ``WARN``: Bei zu warnenden Situationen
- ``INFO``: Wichtige Informationen
- ``DEBUG``: Debug-Informationen
- ``TRACE``: Detaillierte Trace-Informationen

**Beispiel:**

.. code-block:: java

    if (logger.isDebugEnabled()) {
        logger.debug("Suchanfrage: {}", query);
    }

Tests während der Entwicklung
------------

Testen Sie während der Entwicklung auf folgende Weise:

Lokale Ausführung
~~~~~~~~~~

Führen Sie Fess von der IDE oder der Kommandozeile aus und überprüfen Sie den Betrieb:

.. code-block:: bash

    mvn compile exec:java

Debug-Ausführung
~~~~~~~~~~

Verwenden Sie den Debugger der IDE, um das Verhalten des Codes zu verfolgen.

Ausführen von Unit-Tests
~~~~~~~~~~~~~~

Führen Sie Tests im Zusammenhang mit Änderungen aus:

.. code-block:: bash

    # Bestimmte Testklasse ausführen
    mvn test -Dtest=SearchServiceTest

    # Alle Tests ausführen
    mvn test

Weitere Informationen finden Sie unter :doc:`building`.

Schritt 4: Ausführen lokaler Tests
=========================

Führen Sie vor dem Commit unbedingt Tests aus.

Ausführen von Unit-Tests
--------------

.. code-block:: bash

    mvn test

Ausführen von Integrationstests
--------------

.. code-block:: bash

    mvn verify

Überprüfung des Code-Stils
--------------------

.. code-block:: bash

    mvn checkstyle:check

Ausführen aller Prüfungen
-------------------

.. code-block:: bash

    mvn clean verify

Schritt 5: Commit
==============

Committen Sie Ihre Änderungen.

Commit-Nachrichten-Konventionen
--------------------

Commit-Nachrichten folgen diesem Format:

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**Typen:**

- ``feat``: Neue Funktion
- ``fix``: Fehlerbehebung
- ``docs``: Nur Dokumentationsänderungen
- ``style``: Änderungen, die die Bedeutung des Codes nicht beeinflussen (Formatierung usw.)
- ``refactor``: Refactoring
- ``test``: Hinzufügen/Ändern von Tests
- ``chore``: Änderungen am Build-Prozess oder an Tools

**Beispiel:**

.. code-block:: text

    feat: Suchfilterfunktion hinzugefügt

    Benutzer können jetzt Suchergebnisse nach Dateityp filtern.

    Fixes #123

Commit-Schritte
----------

1. Änderungen stagen:

   .. code-block:: bash

       git add .

2. Commit:

   .. code-block:: bash

       git commit -m "feat: Suchfilterfunktion hinzugefügt"

3. Commit-Historie überprüfen:

   .. code-block:: bash

       git log --oneline

Commit-Granularität
------------

- Ein Commit sollte eine logische Änderung enthalten
- Teilen Sie große Änderungen in mehrere Commits auf
- Commit-Nachrichten sollten verständlich und spezifisch sein

Schritt 6: Push
==============

Pushen Sie den Branch in das Remote-Repository.

.. code-block:: bash

    git push origin feature/123-add-search-filter

Beim ersten Push:

.. code-block:: bash

    git push -u origin feature/123-add-search-filter

Schritt 7: Erstellung eines Pull Requests
=========================

Erstellen Sie einen Pull Request (PR) auf GitHub.

Schritte zur PR-Erstellung
-----------

1. Besuchen Sie das `Fess-Repository <https://github.com/codelibs/fess>`__
2. Klicken Sie auf den Tab ``Pull requests``
3. Klicken Sie auf ``New pull request``
4. Wählen Sie den Base-Branch (``main``) und den Vergleichs-Branch (Arbeits-Branch)
5. Klicken Sie auf ``Create pull request``
6. Füllen Sie den PR-Inhalt aus (folgen Sie der Vorlage)
7. Klicken Sie auf ``Create pull request``

PR-Vorlage
---------------

.. code-block:: markdown

    ## Änderungsinhalt
    Was in diesem PR geändert wurde

    ## Zugehöriges Issue
    Closes #123

    ## Art der Änderung
    - [ ] Neue Funktion
    - [ ] Fehlerbehebung
    - [ ] Refactoring
    - [ ] Dokumentationsaktualisierung
    - [ ] Sonstiges

    ## Testmethode
    Wie diese Änderung getestet wurde

    ## Checkliste
    - [ ] Code funktioniert
    - [ ] Tests hinzugefügt
    - [ ] Dokumentation aktualisiert
    - [ ] Codierungskonventionen befolgt

PR-Beschreibung
-------

Die PR-Beschreibung sollte Folgendes enthalten:

- **Zweck der Änderung**: Warum diese Änderung notwendig ist
- **Änderungsinhalt**: Was geändert wurde
- **Testmethode**: Wie es getestet wurde
- **Screenshots**: Bei UI-Änderungen

Schritt 8: Code-Review
====================

Betreuer überprüfen den Code.

Review-Aspekte
------------

Im Review werden folgende Punkte überprüft:

- Code-Qualität
- Einhaltung von Codierungskonventionen
- Vollständigkeit der Tests
- Auswirkungen auf die Performance
- Sicherheitsprobleme
- Aktualisierung der Dokumentation

Beispiele für Review-Kommentare
------------------

**Genehmigung:**

.. code-block:: text

    LGTM (Looks Good To Me)

**Änderungsanfrage:**

.. code-block:: text

    Ist hier nicht eine null-Prüfung erforderlich?

**Vorschlag:**

.. code-block:: text

    Diese Verarbeitung könnte besser in eine Helper-Klasse verschoben werden.

Schritt 9: Antwort auf Review-Feedback
===================================

Reagieren Sie auf Review-Kommentare.

Schritte zur Beantwortung von Feedback
----------------------

1. Lesen Sie die Review-Kommentare
2. Nehmen Sie erforderliche Änderungen vor
3. Änderungen committen:

   .. code-block:: bash

       git add .
       git commit -m "fix: Auf Review-Kommentare reagiert"

4. Push:

   .. code-block:: bash

       git push origin feature/123-add-search-filter

5. Antworten Sie auf Kommentare auf der PR-Seite

Antworten auf Kommentare
--------------

Antworten Sie immer auf Review-Kommentare:

.. code-block:: text

    Korrigiert. Bitte überprüfen Sie.

Oder:

.. code-block:: text

    Vielen Dank für Ihren Hinweis.
    Aus Gründen von XX habe ich die aktuelle Implementierung gewählt, wie wäre es?

Schritt 10: Merge
=============

Nach Genehmigung des Reviews merged der Betreuer den PR.

Maßnahmen nach dem Merge
------------

1. Aktualisieren Sie den lokalen main-Branch:

   .. code-block:: bash

       git checkout main
       git pull origin main

2. Löschen Sie den Arbeits-Branch:

   .. code-block:: bash

       git branch -d feature/123-add-search-filter

3. Löschen Sie den Remote-Branch (falls nicht automatisch auf GitHub gelöscht):

   .. code-block:: bash

       git push origin --delete feature/123-add-search-filter

Häufige Entwicklungsszenarien
==================

Funktionserweiterung
------

1. Erstellen Sie ein Issue (oder überprüfen Sie ein vorhandenes)
2. Erstellen Sie einen Branch: ``feature/xxx-description``
3. Implementieren Sie die Funktion
4. Fügen Sie Tests hinzu
5. Aktualisieren Sie die Dokumentation
6. Erstellen Sie einen PR

Fehlerbehebung
------

1. Überprüfen Sie das Fehlerbericht-Issue
2. Erstellen Sie einen Branch: ``fix/xxx-description``
3. Fügen Sie einen Test hinzu, der den Fehler reproduziert
4. Beheben Sie den Fehler
5. Überprüfen Sie, dass die Tests bestehen
6. Erstellen Sie einen PR

Refactoring
--------------

1. Erstellen Sie ein Issue (erklären Sie den Grund für das Refactoring)
2. Erstellen Sie einen Branch: ``refactor/xxx-description``
3. Führen Sie das Refactoring durch
4. Überprüfen Sie, dass vorhandene Tests bestehen
5. Erstellen Sie einen PR

Dokumentationsaktualisierung
--------------

1. Erstellen Sie einen Branch: ``docs/xxx-description``
2. Aktualisieren Sie die Dokumentation
3. Erstellen Sie einen PR

Entwicklungstipps
==========

Effiziente Entwicklung
----------

- **Kleine Commits**: Committen Sie häufig
- **Frühes Feedback**: Nutzen Sie Draft-PRs
- **Testautomatisierung**: Nutzen Sie CI/CD
- **Code-Review**: Überprüfen Sie auch den Code anderer

Problemlösung
--------

Nutzen Sie bei Schwierigkeiten Folgendes:

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- `Fess-Forum <https://discuss.codelibs.org/c/FessJA>`__
- GitHub-Issue-Kommentare

Nächste Schritte
==========

Nachdem Sie den Workflow verstanden haben, lesen Sie auch folgende Dokumentation:

- :doc:`building` - Details zu Build und Test
- :doc:`contributing` - Richtlinien für Beiträge
- :doc:`architecture` - Verständnis der Codebasis

Referenzmaterialien
======

- `GitHub Flow <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `Richtlinien für Commit-Nachrichten <https://chris.beams.io/posts/git-commit/>`__
- `Best Practices für Code-Reviews <https://google.github.io/eng-practices/review/>`__
