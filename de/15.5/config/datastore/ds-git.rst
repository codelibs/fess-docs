==================================
Git-Konnektor
==================================

Übersicht
=========

Der Git-Konnektor bietet die Funktionalität, Dateien aus Git-Repositories abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-git`` erforderlich.

Unterstützte Repositories
=========================

- GitHub (öffentlich/privat)
- GitLab (öffentlich/privat)
- Bitbucket (öffentlich/privat)
- Lokale Git-Repositories
- Andere Git-Hosting-Dienste

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Für private Repositories sind Anmeldedaten erforderlich
3. Lesezugriff auf das Repository ist erforderlich

Plugin-Installation
-------------------

Installieren Sie über die Administrationsoberfläche unter "System" -> "Plugins".

Oder weitere Details finden Sie unter :doc:`../../admin/plugin-guide`.

Konfiguration
=============

Konfigurieren Sie über die Administrationsoberfläche unter "Crawler" -> "Datenspeicher" -> "Neu erstellen".

Grundeinstellungen
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Einstellung
     - Beispielwert
   * - Name
     - Project Git Repository
   * - Handler-Name
     - GitDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

Beispiel für öffentliches Repository:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Beispiel für privates Repository (mit Authentifizierung):

::

    uri=https://username:personal_access_token@github.com/company/private-repo.git
    base_url=https://github.com/company/private-repo/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``uri``
     - Ja
     - URI des Git-Repositories (für Clone)
   * - ``base_url``
     - Ja
     - Basis-URL für die Dateianzeige
   * - ``extractors``
     - Nein
     - Extraktoren nach MIME-Typ
   * - ``prev_commit_id``
     - Nein
     - Vorherige Commit-ID (für differentielles Crawling)
   * - ``delete_old_docs``
     - Nein
     - Gelöschte Dateien aus dem Index entfernen (Standard: ``false``)

Skript-Einstellungen
--------------------

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    cache=""
    digest=author.toExternalString()
    anchor=
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

Verfügbare Felder
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``url``
     - URL der Datei
   * - ``path``
     - Dateipfad im Repository
   * - ``name``
     - Dateiname
   * - ``content``
     - Textinhalt der Datei
   * - ``contentLength``
     - Länge des Inhalts
   * - ``timestamp``
     - Datum der letzten Änderung
   * - ``mimetype``
     - MIME-Typ der Datei
   * - ``author``
     - Informationen zum letzten Committer

Git-Repository-Authentifizierung
================================

GitHub Personal Access Token
----------------------------

1. Personal Access Token auf GitHub generieren
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Besuchen Sie https://github.com/settings/tokens:

1. Klicken Sie auf "Generate new token" -> "Generate new token (classic)"
2. Geben Sie den Token-Namen ein (z.B.: Fess Crawler)
3. Aktivieren Sie unter Scopes "repo"
4. Klicken Sie auf "Generate token"
5. Kopieren Sie das generierte Token

2. Anmeldedaten in URI einbinden
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:ghp_abc123def456ghi789jkl012@github.com/company/repo.git

GitLab Private Token
--------------------

1. Access Token auf GitLab generieren
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unter GitLab User Settings -> Access Tokens:

1. Geben Sie den Token-Namen ein
2. Aktivieren Sie unter Scopes "read_repository"
3. Klicken Sie auf "Create personal access token"
4. Kopieren Sie das generierte Token

2. Anmeldedaten in URI einbinden
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    uri=https://username:glpat-abc123def456@gitlab.com/company/repo.git

SSH-Authentifizierung
---------------------

Bei Verwendung von SSH-Schlüsseln:

::

    uri=git@github.com:company/repo.git

.. note::
   Bei SSH-Authentifizierung müssen die SSH-Schlüssel des Benutzers konfiguriert werden, der |Fess| ausführt.

Extraktoren konfigurieren
=========================

Extraktoren nach MIME-Typ
-------------------------

Mit dem Parameter ``extractors`` können Extraktoren nach Dateityp festgelegt werden:

::

    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,application/json:textExtractor,

Format: ``<MIME-Typ-Regex>:<Extraktorname>,``

Standard-Extraktoren
~~~~~~~~~~~~~~~~~~~~

- ``textExtractor`` - Für Textdateien
- ``tikaExtractor`` - Für Binärdateien (PDF, Word usw.)

Nur Textdateien crawlen
~~~~~~~~~~~~~~~~~~~~~~~

::

    extractors=text/.*:textExtractor,

Alle Dateien crawlen
~~~~~~~~~~~~~~~~~~~~

::

    extractors=.*:tikaExtractor,

Nur bestimmte Dateitypen
~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Nur Markdown, YAML, JSON
    extractors=text/markdown:textExtractor,text/yaml:textExtractor,application/json:textExtractor,

Differentielles Crawling
========================

Nur Änderungen seit dem letzten Commit crawlen
----------------------------------------------

Nach dem ersten Crawling die ``prev_commit_id`` auf die vorherige Commit-ID setzen:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    prev_commit_id=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
    delete_old_docs=true

.. note::
   Die Commit-ID wird auf die Commit-ID des letzten Crawlings gesetzt.
   Dadurch werden nur Änderungen seit diesem Commit gecrawlt.

Verarbeitung gelöschter Dateien
-------------------------------

Bei ``delete_old_docs=true`` werden aus dem Git-Repository gelöschte Dateien auch aus dem Index entfernt.

Anwendungsbeispiele
===================

GitHub öffentliches Repository
------------------------------

Parameter:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/.*:textExtractor,application/xml:textExtractor,
    delete_old_docs=false

Skript:

::

    url=url
    host="github.com"
    site="github.com/codelibs/fess/" + path
    title=name
    content=content
    last_modified=timestamp
    mimetype=mimetype

GitHub privates Repository
--------------------------

Parameter:

::

    uri=https://username:ghp_abc123def456ghi789jkl012@github.com/company/repo.git
    base_url=https://github.com/company/repo/blob/main/
    extractors=text/.*:textExtractor,application/xml:textExtractor,application/javascript:textExtractor,
    delete_old_docs=false

Skript:

::

    url=url
    title=name
    content=content
    digest=author.toExternalString()
    content_length=contentLength
    last_modified=timestamp
    mimetype=mimetype

GitLab (selbst gehostet)
------------------------

Parameter:

::

    uri=https://username:glpat-abc123@gitlab.company.com/team/project.git
    base_url=https://gitlab.company.com/team/project/-/blob/main/
    extractors=text/.*:textExtractor,
    prev_commit_id=
    delete_old_docs=false

Skript:

::

    url=url
    host="gitlab.company.com"
    site="gitlab.company.com/team/project/" + path
    title=name
    content=content
    last_modified=timestamp

Nur Dokumentation crawlen (Markdown-Dateien)
--------------------------------------------

Parameter:

::

    uri=https://github.com/codelibs/fess.git
    base_url=https://github.com/codelibs/fess/blob/master/
    extractors=text/markdown:textExtractor,text/plain:textExtractor,
    delete_old_docs=false

Skript:

::

    if (mimetype.startsWith("text/")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
    }

Nur bestimmte Verzeichnisse crawlen
-----------------------------------

Filterung im Skript:

::

    if (path.startsWith("docs/") || path.startsWith("README")) {
        url=url
        title=name
        content=content
        last_modified=timestamp
        mimetype=mimetype
    }

Fehlerbehebung
==============

Authentifizierungsfehler
------------------------

**Symptom**: ``Authentication failed`` oder ``Not authorized``

**Zu überprüfen**:

1. Überprüfen Sie, ob das Personal Access Token korrekt ist
2. Überprüfen Sie, ob das Token die entsprechenden Berechtigungen hat (``repo``-Scope)
3. Überprüfen Sie, ob das URI-Format korrekt ist:

   ::

       # Korrekt
       uri=https://username:token@github.com/company/repo.git

       # Falsch
       uri=https://github.com/company/repo.git?token=...

4. Überprüfen Sie das Ablaufdatum des Tokens

Repository nicht gefunden
-------------------------

**Symptom**: ``Repository not found``

**Zu überprüfen**:

1. Überprüfen Sie, ob die Repository-URL korrekt ist
2. Überprüfen Sie, ob das Repository existiert und nicht gelöscht wurde
3. Überprüfen Sie die Anmeldedaten
4. Überprüfen Sie, ob Sie Zugriff auf das Repository haben

Keine Dateien abrufbar
----------------------

**Symptom**: Crawling erfolgreich, aber 0 Dateien

**Zu überprüfen**:

1. Überprüfen Sie die ``extractors``-Einstellung
2. Überprüfen Sie, ob Dateien im Repository existieren
3. Überprüfen Sie die Skript-Einstellungen
4. Überprüfen Sie, ob Dateien im Zielbranch existieren

MIME-Typ-Fehler
---------------

**Symptom**: Bestimmte Dateien werden nicht gecrawlt

**Lösung**:

Passen Sie die Extraktor-Einstellungen an:

::

    # Alle Dateien als Ziel
    extractors=.*:tikaExtractor,

    # Bestimmte MIME-Typen hinzufügen
    extractors=text/.*:textExtractor,application/json:textExtractor,application/xml:textExtractor,

Große Repositories
------------------

**Symptom**: Crawling dauert lange oder Speicherüberlauf

**Lösung**:

1. Mit ``extractors`` Zieldateien einschränken
2. Mit Skript nur bestimmte Verzeichnisse filtern
3. Differentielles Crawling verwenden (``prev_commit_id`` setzen)
4. Crawl-Intervall anpassen

Branch angeben
--------------

Um einen anderen als den Standard-Branch zu crawlen:

::

    uri=https://github.com/company/repo.git#develop
    base_url=https://github.com/company/repo/blob/develop/

Geben Sie den Branch-Namen nach ``#`` an.

URL-Generierung
===============

base_url-Muster
---------------

**GitHub**:

::

    base_url=https://github.com/user/repo/blob/master/

**GitLab**:

::

    base_url=https://gitlab.com/user/repo/-/blob/main/

**Bitbucket**:

::

    base_url=https://bitbucket.org/user/repo/src/master/

``base_url`` und Dateipfad werden kombiniert, um die URL zu generieren.

URL-Generierung im Skript
-------------------------

::

    url=base_url + path
    title=name
    content=content

Oder benutzerdefinierte URL:

::

    url="https://github.com/mycompany/repo/blob/main/" + path
    title=name
    content=content

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `GitHub Personal Access Tokens <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_
- `GitLab Personal Access Tokens <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_
