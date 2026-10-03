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

Art
:::

Geben Sie „Label“ oder „Tag“ an. Ein gewöhnliches Label ist „Label“. „Tag“ ist ein Tag, den Benutzer
auf der Suchseite hinzufügen (siehe „Tags“ unten). Ein bestehendes Label ohne Art wird als „Label“
behandelt.


Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

Tags
----

Mit ``user.tag.enabled=true`` (Standard: ``false``) in ``fess_config.properties`` können
angemeldete Benutzer Suchergebnisse taggen. Im mitgelieferten Theme ``bootstrap`` werden Tags an den
Ergebnissen angezeigt, Benutzer können Tags hinzufügen und eigene entfernen, und eine Facette „Tags“
grenzt die Ergebnisse ein. Zur API siehe :doc:`../api/api-tag`.

Ein Tag wird als Label der Art „Tag“ gespeichert: Der Name ist der Tag-Name, der Wert der SHA-256
des Namens, die eingeschlossenen Pfade sind die getaggten URLs (eine je Zeile, exakte
Übereinstimmung), und die Berechtigungen bestimmen, wer das Tag sehen kann. Ein Benutzer, der ein Tag
hinzufügt, wird zu dessen Berechtigungen hinzugefügt.

- Ein Tag ist nur sichtbar, wenn die Berechtigungen seines Labels auf den Aufrufer zutreffen.
  Administratoren können ein Tag auf dieser Seite bearbeiten, um es mit einer Rolle oder Gruppe zu
  teilen, oder es löschen.
- Tags mit gleichem Namen werden zu einem Label zusammengeführt; Benutzer, die ein Tag gleichen
  Namens hinzugefügt haben, sehen daher gegenseitig, wo ihre Tags gesetzt sind.
- Tags erscheinen weder in der Label-Listen-API (``/api/v2/labels``) noch in der Label-Auswahl der
  Suchseite.
- Tags zählen zum Label-Limit (``page.labeltype.max.fetch.size``, Standard: 1000). Ist das Limit
  erreicht, kann kein neues Tag erstellt werden.
- Ändert oder löscht ein Administrator ein Tag auf dieser Seite, behalten die indexierten Dokumente die
  alten Werte, bis sie erneut gecrawlt werden oder der Job „Label Updater“ läuft.
- Ein Dokument kann bis zu ``user.tag.max.document.tags`` (Standard: 100) Tags haben, ein Tag-Name bis
  zu ``user.tag.name.max.length`` (Standard: 50) Zeichen.

.. |image0| image:: ../../../resources/images/en/15.9/admin/labeltype-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/labeltype-2.png
