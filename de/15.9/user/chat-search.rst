============
KI-Suchmodus
============

Übersicht
=========

Mit der Funktion KI-Suchmodus (RAG-Chat) von |Fess| können Sie zusätzlich zur herkömmlichen
Stichwortsuche auch in natürlicher Gesprächsform nach Informationen suchen. Wenn Sie eine
Frage eingeben, durchsucht der KI-Assistent die relevanten Dokumente und generiert auf
Basis ihres Inhalts eine leicht verständliche Antwort.

.. note::
   Der KI-Suchmodus ist standardmäßig deaktiviert. Damit Sie ihn nutzen können, muss der
   Systemadministrator die Funktion aktivieren und einen LLM-Provider (Large Language Model)
   konfigurieren. Informationen zur Konfiguration finden Sie unter :doc:`../config/rag-chat`
   und :doc:`../config/llm-overview`.

Merkmale des KI-Suchmodus
=========================

Dialogbasierte Suche
--------------------

Anstatt sich Schlüsselwörter zu überlegen, können Sie Fragen wie in einem gewöhnlichen
Gespräch stellen.

Beispiele:

- "Wie installiere ich Fess?"
- "Wie kann ich Dateien crawlen?"
- "Was kann ich tun, wenn keine Suchergebnisse angezeigt werden?"

Kontextbezogene Antworten
-------------------------

Der KI-Assistent analysiert die Absicht der Frage, durchsucht relevante Dokumente und
extrahiert aus mehreren Suchergebnissen die benötigten Informationen, um daraus eine
strukturierte Antwort zu erstellen.

Angabe der Quellen
-------------------

Am unteren Rand der Antwort werden die Dokumente, auf denen die Antwort basiert, als
"Quellen" aufgelistet. Jede Quelle ist ein nummerierter Link, über den Sie das
Originaldokument direkt aufrufen können. Außerdem kann der Antworttext Zitate mit
Nummern wie ``[1]`` oder ``[2]`` enthalten, die den Nummern in der Quellenliste
entsprechen.

Gesprächsfortsetzung
--------------------

Es muss nicht bei einer einzigen Frage bleiben – Sie können das Gespräch fortsetzen.
Der KI-Assistent beantwortet weitere Fragen unter Berücksichtigung des Kontexts
vorheriger Fragen und Antworten.

Verwendung der Chat-Suche
==========================

Den KI-Suchmodus öffnen
------------------------

1. Öffnen Sie die Suchseite von |Fess|
2. Klicken Sie in der Navigationsleiste am oberen Bildschirmrand auf den Link "KI-Suche" (Roboter-Symbol)
3. Der Bildschirm des KI-Suchmodus wird angezeigt

.. note::
   Der Link "KI-Suche" wird nur angezeigt, wenn der KI-Suchmodus aktiviert ist und ein
   LLM-Provider zur Verfügung steht. Wenn der Link nicht angezeigt wird, lesen Sie den
   Abschnitt `Häufig gestellte Fragen`_.

Eine Frage eingeben
--------------------

1. Geben Sie Ihre Frage in das Textfeld am unteren Bildschirmrand ein (maximal 4000 Zeichen pro Frage)
2. Klicken Sie auf die Schaltfläche "Nachricht senden" (Papierflieger-Symbol) oder drücken Sie die Eingabetaste (Enter)
3. Der KI-Assistent beginnt mit der Generierung der Antwort

.. note::
   Wenn Sie einen Zeilenumbruch eingeben möchten, drücken Sie anstelle der Eingabetaste
   die Tastenkombination Umschalt+Eingabetaste (Shift+Enter).

.. note::
   Die Generierung der Antwort kann einige Sekunden bis zu einer knappen Minute dauern.
   Während der Verarbeitung wird der aktuelle Verarbeitungsschritt in einer
   Fortschrittsanzeige (Analyse → Suche → Bewertung → Abruf → Antwort) dargestellt,
   begleitet von Meldungen wie "Denkt nach...", "Suche läuft...",
   "Suchergebnisse werden überprüft...", "Dokumente werden abgerufen..." und
   "Antwort wird generiert...". Sobald die Suche abgeschlossen ist, wird zusätzlich die
   Anzahl der gefundenen Dokumente angezeigt.

Antwort überprüfen
-------------------

Die Antwort des KI-Assistenten wird angezeigt. Sie enthält folgende Informationen:

- **Antworttext**: Die Antwort auf Ihre Frage (im Markdown-Format formatiert)
- **Quellen**: Eine Liste nummerierter Links zu den Dokumenten, auf denen die Antwort
  basiert (ein Klick öffnet das Originaldokument in einem neuen Tab)

Der Antworttext kann Zitatnummern wie ``[1]`` oder ``[2]`` enthalten, die den Nummern in
der Quellenliste entsprechen. Jede Antwort verfügt über eine Kopieren-Schaltfläche, mit
der Sie den Antwortinhalt in die Zwischenablage kopieren können.

.. note::
   Die KI verwendet als Grundlage für die Antwort nur die Dokumente, die sie unter den
   Suchergebnissen als am relevantesten einstuft. Daher kann die Anzahl der Quellen
   geringer sein als die Anzahl der bei der Suche gefundenen Dokumente.

Suchbereich eingrenzen
------------------------

Je nach Thema können Sie über die Schaltfläche "Filter" am oberen Bildschirmrand den
Suchbereich anhand von Kriterien wie Labels, Dateityp, Änderungsdatum oder Größe
eingrenzen. Das ist praktisch, wenn Sie der KI nur zu einem bestimmten Dokumentenbereich
Fragen stellen möchten.

Das Gespräch fortsetzen
-------------------------

Wenn Sie weitere Fragen haben, können Sie direkt weiterfragen:

- "Können Sie das genauer erklären?"
- "Gibt es noch andere Möglichkeiten?"
- "Mehr Details zu XXX"

Der KI-Assistent berücksichtigt bei der Antwort den Kontext des vorherigen Gesprächs.

Ein neues Gespräch beginnen
-----------------------------

Wenn Sie zu einem anderen Thema eine Frage stellen möchten, klicken Sie auf die
Schaltfläche "Neuer Chat" (Plus-Symbol). Dadurch wird der bisherige Gesprächsverlauf
gelöscht und Sie können ein neues Gespräch beginnen.

Tipps für effektive Fragen
============================

Konkret fragen
--------------

Konkrete Fragen liefern passendere Antworten als vage Fragen.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Vage Frage
     - Konkrete Frage
   * - Wie konfiguriert man das?
     - Wie ändere ich die Speichereinstellungen von Fess?
   * - Es tritt ein Fehler auf
     - Bei der Suche erscheint die Fehlermeldung "Index nicht gefunden"
   * - Zum Crawling
     - Wie richte ich Ausschlussregeln beim Crawlen einer Website ein?

Hintergrundinformationen angeben
-----------------------------------

Wenn Sie Ihre Situation oder Ihr Ziel angeben, erhalten Sie passendere Antworten.

Gute Beispiele:

- "Ich betreibe Fess in einer Docker-Umgebung. Ich möchte den Speicherort der Logs ändern – wie mache ich das?"
- "Ich benutze Fess zum ersten Mal. Was sollte ich zuerst tun?"

Schrittweise fragen
--------------------

Bei komplexen Problemen wird das Verständnis durch schrittweises Nachfragen erleichtert.

1. "Kann Fess Dateifreigaben crawlen?"
2. "Wie stelle ich eine Verbindung über das SMB-Protokoll her?"
3. "Was mache ich, wenn der Freigabeordner eine Authentifizierung erfordert?"

Häufig gestellte Fragen
==========================

F: Der KI-Suchmodus wird nicht angezeigt
------------------------------------------

A: Möglicherweise ist der KI-Suchmodus nicht aktiviert. Der Link "KI-Suche" wird nur
angezeigt, wenn die Funktion aktiviert ist (``rag.chat.enabled=true``) und ein
LLM-Provider (z. B. OpenAI, Gemini, Ollama) konfiguriert und verfügbar ist. Fragen Sie
Ihren Systemadministrator, ob der KI-Suchmodus aktiviert und der LLM-Provider korrekt
konfiguriert ist (Details siehe :doc:`../config/rag-chat`).

F: Es dauert lange, bis die Antwort angezeigt wird
------------------------------------------------------

A: Da die KI die Frage analysiert, Dokumente durchsucht und bewertet, bevor sie die
Antwort generiert, kann dies einige Sekunden bis zu einer knappen Minute dauern.
Während der Verarbeitung wird der aktuelle Verarbeitungsschritt angezeigt
("Denkt nach...", "Suche läuft...", "Suchergebnisse werden überprüft...",
"Dokumente werden abgerufen...", "Antwort wird generiert...").

F: Die Quellen scheinen falsch zu sein
------------------------------------------

A: Klicken Sie auf den Link der Quelle, um das Originaldokument zu überprüfen. Die KI
generiert die Antwort auf Basis der Suchergebnisse, wobei es zu Interpretationsfehlern
kommen kann. Wir empfehlen, wichtige Informationen stets im Originaldokument zu
überprüfen.

F: Das vorherige Gespräch scheint vergessen worden zu sein
----------------------------------------------------------------

A: Möglicherweise ist die Gesprächssitzung abgelaufen. Wenn über einen bestimmten
Zeitraum (standardmäßig 30 Minuten) keine Aktivität stattfindet, wird der
Gesprächsverlauf gelöscht. Da der Gesprächsverlauf zudem nur temporär im Arbeitsspeicher
des Servers gehalten wird, geht er auch bei einem Neustart des Servers verloren.
Beginnen Sie in diesem Fall ein neues Gespräch.

.. note::
   Die hier genannte "Sitzung" bezieht sich auf die Gesprächssitzung des KI-Suchmodus
   und ist von der Anmeldesitzung bei |Fess| zu unterscheiden.

F: Ich erhalte auf bestimmte Fragen keine Antwort
-------------------------------------------------------

A: Folgende Ursachen sind möglich:

- In den durchsuchten Dokumenten sind keine relevanten Informationen enthalten
- Die Frage ist zu vage formuliert, sodass keine geeignete Suche möglich ist
- Das Rate-Limit wurde erreicht (die maximale Anzahl an Anfragen pro Minute oder die
  maximale Anzahl gleichzeitiger Anfragen wurde überschritten)

Formulieren Sie die Frage um oder warten Sie eine Weile, bevor Sie es erneut versuchen.

F: Gibt es eine Begrenzung für die Anzahl der eingebbaren Zeichen?
------------------------------------------------------------------------

A: Pro Frage sind maximal 4000 Zeichen zulässig. Unterhalb des Textfelds wird ein
Zeichenzähler angezeigt, der eine Warnung ausgibt, sobald Sie sich der Obergrenze
nähern. Fassen Sie lange Fragen auf die wesentlichen Punkte zusammen.

F: Kann ich auch in anderen Sprachen als Japanisch fragen?
------------------------------------------------------------------

A: Ja, in den meisten Fällen können Sie auch auf Englisch oder in anderen Sprachen
fragen. Die KI versucht, basierend auf der Anzeigesprache des Browsers bzw. der
Oberfläche, so weit wie möglich in derselben Sprache zu antworten. Dies erfolgt jedoch
nach bestem Bemühen (Best Effort), sodass die Antwort je nach Situation nicht in der
gewünschten Sprache erfolgen kann.

Hinweise
========

Über die KI-Antworten
-----------------------

- Die Antworten der KI werden auf Grundlage der Suchergebnisse generiert
- Die Genauigkeit der Antworten wird nicht garantiert
- Überprüfen Sie für wichtige Entscheidungen stets das Originaldokument (die Quelle)
- Aktuelle Informationen finden Sie in der offiziellen Dokumentation

Zum Datenschutz
-----------------

- Eingegebene Fragen werden für die Suche sowie für die KI-Verarbeitung durch den
  konfigurierten LLM-Provider verwendet
- Wenn ein externer LLM-Dienst (z. B. OpenAI oder Gemini) konfiguriert ist, werden der
  Inhalt der Frage sowie die Suchergebnisse an diesen Dienst übermittelt. Wenn die
  Verarbeitung ausschließlich intern erfolgen soll, wenden Sie sich an Ihren
  Administrator bezüglich der Nutzung eines lokal betriebenen Providers (z. B. Ollama)
- Der Gesprächsverlauf wird temporär im Arbeitsspeicher des Servers gespeichert und
  gelöscht, wenn die Sitzung abläuft, "Neuer Chat" ausgeführt wird oder der Server neu
  gestartet wird
- Wie bei der regulären Suche gilt auch hier die Zugriffskontrolle über Rollen
  (Berechtigungen) und Labels; Dokumente, auf die kein Zugriff besteht, werden nicht als
  Grundlage für die Antwort verwendet
- Je nach Systemkonfiguration können Protokolle aufgezeichnet werden

Referenzinformationen
======================

- :doc:`../config/rag-chat` - Konfiguration der Funktion KI-Suchmodus (für Administratoren)
- :doc:`../config/llm-overview` - Konfiguration des LLM-Providers
- :doc:`../api/api-chat` - Chat-API (Nutzung über Programme)
- :doc:`search-and` - Verwendung der UND-Suche
- :doc:`search-not` - Verwendung der NICHT-Suche
- :doc:`search-field` - Verwendung der Feldsuche
- :doc:`advanced-search` - Erweiterte Suchfunktionen
