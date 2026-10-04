=====
Label
=====

Übersicht
=========


Hier wird die Konfiguration von Labels erläutert.
Labels können Dokumente klassifizieren, die in Suchergebnissen angezeigt werden.
Die Label-Konfiguration gibt Pfade an, auf die Labels angewendet werden sollen, mithilfe regulärer Ausdrücke.
Wenn Labels registriert sind, wird ein Label-Dropdown-Feld in den Suchoptionen angezeigt.

Die hier vorgenommene Label-Konfiguration gilt für Web- oder Dateisystem-Crawl-Konfigurationen.

Verwaltung
==========

Anzeige
-------

Um die Label-Konfigurationsübersichtsseite zu öffnen, klicken Sie im linken Menü auf [Crawler > Label].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Label-Konfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Name
::::

Geben Sie den Namen an, der im Label-Auswahl-Dropdown-Feld bei der Suche angezeigt werden soll.

Wert
::::

Geben Sie die Kennung zur Klassifizierung von Dokumenten an.
Geben Sie alphanumerische Zeichen an.

Zielpfad
::::::::

Konfigurieren Sie Pfade, auf die Labels angewendet werden sollen, mithilfe regulärer Ausdrücke.
Sie können mehrere Pfade angeben, indem Sie mehrere Zeilen schreiben.
Dokumente, die mit den hier angegebenen Pfaden übereinstimmen, erhalten das Label.

Ausgeschlossener Pfad
:::::::::::::::::::::

Konfigurieren Sie Pfade, die vom Crawl-Ziel ausgeschlossen werden sollen, mithilfe regulärer Ausdrücke.
Sie können mehrere Pfade angeben, indem Sie mehrere Zeilen schreiben.

Berechtigung
::::::::::::

Geben Sie die Berechtigung für diese Konfiguration an.
Um beispielsweise Suchergebnisse für Benutzer anzuzeigen, die zur Gruppe „developer" gehören, geben Sie {group}developer an.
Für Benutzerebene geben Sie {user}Benutzername an, für Rollenebene {role}Rollenname und für Gruppenebene {group}Gruppenname.

Virtueller Host
:::::::::::::::

Geben Sie den Hostnamen des virtuellen Hosts an.
Weitere Details finden Sie unter :doc:`Virtueller Host im Konfigurationshandbuch <../config/security-virtual-host>`.

Ein über einen virtuellen Host aufgerufener Suchbildschirm zeigt nur die Labels an, in deren Feld dieser virtuelle Host angegeben ist.
Ein Label mit leerem Feld wird nicht angezeigt, wenn der Suchbildschirm über einen virtuellen Host aufgerufen wird.
Bei einem Zugriff, der keinem virtuellen Host entspricht, werden unabhängig von diesem Feld alle Labels angezeigt.

Pro Label kann nur ein virtueller Host angegeben werden.
Um dasselbe Label auf mehreren virtuellen Hosts anzuzeigen, erstellen Sie für jeden virtuellen Host ein Label mit demselben Namen und Wert und tragen im Feld „Virtueller Host" jeweils dessen Namen ein.
Da der Wert gleich ist, grenzt jedes dieser Labels auf dieselben Dokumente ein.

Anzeigereihenfolge
::::::::::::::::::

Geben Sie die Anzeigereihenfolge der Labels an.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

.. |image0| image:: ../../../resources/images/en/15.9/admin/labeltype-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/labeltype-2.png
