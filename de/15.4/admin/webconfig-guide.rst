===========
Web-Crawl
===========

Übersicht
=========

Die Web-Crawl-Konfigurationsseite konfiguriert Web-Crawling.

Verwaltung
==========

Anzeige
-------

Um die Web-Crawl-Konfigurationsübersichtsseite zu öffnen, klicken Sie im linken Menü auf [Crawler > Web].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Web-Crawl-Konfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Erstellen".

|image1|

Konfigurationsparameter
-----------------------

Name
::::

Konfigurationsname.

URL
:::

Die Start-URL für das Crawling.

Zu crawlende URL
::::::::::::::::

URLs, die mit dem regulären Ausdruck (Java-Format) übereinstimmen, der in diesem Element angegeben ist, werden vom |Fess| Crawler gecrawlt.

Vom Crawlen ausgeschlossene URL
::::::::::::::::::::::::::::::::

URLs, die mit dem regulären Ausdruck (Java-Format) übereinstimmen, der in diesem Element angegeben ist, werden vom |Fess| Crawler nicht gecrawlt.

Zu durchsuchende URL
:::::::::::::::::::::

URLs, die mit dem regulären Ausdruck (Java-Format) übereinstimmen, der in diesem Element angegeben ist, werden in die Suche einbezogen.

Von der Suche ausgeschlossene URL
::::::::::::::::::::::::::::::::::

URLs, die mit dem regulären Ausdruck (Java-Format) übereinstimmen, der in diesem Element angegeben ist, werden von der Suche ausgeschlossen.

Konfigurationsparameter
:::::::::::::::::::::::

Sie können Crawl-Konfigurationsinformationen angeben.

Tiefe
:::::

Sie können die Tiefe beim Verfolgen von Links angeben, die in gecrawlten Dokumenten enthalten sind.

Maximale Zugriffszahl
:::::::::::::::::::::

Die Anzahl der zu indizierenden URLs.

User-Agent
::::::::::

Der Name des |Fess| Crawlers.

Thread-Anzahl
:::::::::::::

Die Anzahl der Crawl-Threads für diese Konfiguration.

Intervall
:::::::::

Das Zeitintervall für jeden Thread beim Crawlen von URLs.

Boost-Wert
::::::::::

Die Gewichtung von Dokumenten, die durch diese Konfiguration indiziert werden.

Berechtigung
::::::::::::

Geben Sie die Berechtigung für diese Konfiguration an.
Um beispielsweise Suchergebnisse für Benutzer anzuzeigen, die zur Gruppe „developer" gehören, geben Sie {group}developer an.
Für Benutzerebene geben Sie {user}Benutzername an, für Rollenebene {role}Rollenname und für Gruppenebene {group}Gruppenname.

Virtueller Host
:::::::::::::::

Geben Sie den Hostnamen des virtuellen Hosts an.
Weitere Details finden Sie unter :doc:`../config/virtual-host`.

Status
::::::

Wenn aktiviert, enthält der Standard-Crawler-Zeitplanjob diese Konfiguration.

Beschreibung
::::::::::::

Sie können eine Beschreibung eingeben.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt. Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

Beispiele
=========

fess.codelibs.org crawlen
-------------------------

Um eine Web-Crawl-Konfiguration zu erstellen, die Seiten unter https://fess.codelibs.org/ crawlt, verwenden Sie die folgenden Konfigurationswerte:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Konfigurationselement
     - Konfigurationswert
   * - Name
     - Fess
   * - URL
     - https://fess.codelibs.org/
   * - Zu crawlende URL
     - https://fess.codelibs.org/.*

Andere Konfigurationswerte verwenden Standardwerte.

Web-Authentifizierungs-Site crawlen
------------------------------------

Fess unterstützt das Crawlen mit BASIC-, DIGEST- und NTLM-Authentifizierung.
Weitere Details zur Web-Authentifizierung finden Sie auf der Web-Authentifizierungsseite.

Redmine
:::::::

Um eine Web-Crawl-Konfiguration zu erstellen, die passwortgeschützte Redmine-Seiten (z. B. https://<server>/) crawlt, verwenden Sie die folgenden Konfigurationswerte:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Konfigurationselement
     - Konfigurationswert
   * - Name
     - Redmine
   * - URL
     - https://<server>/my/page
   * - Zu crawlende URL
     - https://<server>/.*
   * - Konfigurationsparameter
     - client.robotsTxtEnabled=false (Optional)

Erstellen Sie dann eine Web-Authentifizierungskonfiguration mit den folgenden Konfigurationswerten:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Konfigurationselement
     - Konfigurationswert
   * - Schema
     - Form
   * - Benutzername
     - (Konto für Crawling)
   * - Passwort
     - (Passwort für das Konto)
   * - Parameter
     - | encoding=UTF-8
       | token_method=GET
       | token_url=https://<server>/login
       | token_pattern=name="authenticity_token"[^>]+value="([^"]+)"
       | token_name=authenticity_token
       | login_method=POST
       | login_url=https://<server>/login
       | login_parameters=username=${username}&password=${password}
   * - Web-Authentifizierung
     - Redmine


XWiki
:::::

Um eine Web-Crawl-Konfiguration zu erstellen, die XWiki-Seiten (z. B. https://<server>/xwiki/) crawlt, verwenden Sie die folgenden Konfigurationswerte:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Konfigurationselement
     - Konfigurationswert
   * - Name
     - XWiki
   * - URL
     - https://<server>/xwiki/bin/view/Main/
   * - Zu crawlende URL
     - https://<server>/.*
   * - Konfigurationsparameter
     - client.robotsTxtEnabled=false (Optional)

Erstellen Sie dann eine Web-Authentifizierungskonfiguration mit den folgenden Konfigurationswerten:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Konfigurationselement
     - Konfigurationswert
   * - Schema
     - Form
   * - Benutzername
     - (Konto für Crawling)
   * - Passwort
     - (Passwort für das Konto)
   * - Parameter
     - | encoding=UTF-8
       | token_method=GET
       | token_url=http://<server>/xwiki/bin/login/XWiki/XWikiLogin
       | token_pattern=name="form_token" +value="([^"]+)"
       | token_name=form_token
       | login_method=POST
       | login_url=http://<server>/xwiki/bin/loginsubmit/XWiki/XWikiLogin
       | login_parameters=j_username=${username}&j_password=${password}
   * - Web-Authentifizierung
     - XWiki


.. |image0| image:: ../../../resources/images/en/15.4/admin/webconfig-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/webconfig-2.png
.. pdf            :height: 940 px
