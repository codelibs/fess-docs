===
Tag
===

Übersicht
=========

Hier wird der Bildschirm zur Verwaltung der Tags der Benutzer erläutert.

Ein Tag ist eine Markierung, die ein angemeldeter Benutzer an Dokumente in den Suchergebnissen
vergibt. Tags werden pro Benutzer verwaltet: Wer ein Tag erstellt, ist sein Besitzer, und zwei
Benutzer können denselben Namen verwenden und haben trotzdem zwei getrennte Tags. Tags sind keine
:doc:`Labels <labeltype-guide>`, die Administratoren über URL-Muster definieren; Benutzer erstellen
Tags selbst und vergeben sie an einzelne Dokumente.

Tags sind standardmäßig deaktiviert. Um sie zu nutzen, setzen Sie ``user.tag.enabled=true`` in
``fess_config.properties``. Danach können angemeldete Benutzer im mitgelieferten Theme
``bootstrap`` Tags an Suchergebnisse vergeben und wieder entfernen und über eine Tag-Facette filtern.
Unter „Meine Tags“ können sie ihre eigenen Tags umbenennen, freigeben und löschen. Freigegebene Tags
anderer Benutzer werden mit dem Präfix „Geteilt:“ angezeigt. Zur Benutzer-API und zu den
Einstellungen siehe :doc:`../api/api-tag`.

In diesem Bildschirm können Administratoren die Tags aller Benutzer auflisten, erstellen, bearbeiten
und löschen.

Verwaltung
==========

Anzeige
-------

Um die Tag-Liste zu öffnen, klicken Sie im linken Menü auf [Crawler > Tag]. Zum Anzeigen ist die
Rolle ``admin-tagtype`` oder ``admin-tagtype-view`` erforderlich, zum Erstellen, Bearbeiten und
Löschen ``admin-tagtype``.

Die Liste zeigt Name und Besitzer jedes Tags, sortiert nach Sortierreihenfolge, Name und Besitzer.
Sie können nach Name und nach Besitzer suchen; beide treffen die Tags, die den eingegebenen Text
enthalten.

Klicken Sie auf einen Namen, um das Tag zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Seite zum Erstellen eines Tags zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen“.

Konfigurationsparameter
-----------------------

Name
::::

Gibt den Tag-Namen an. Der Name wird NFKC-normalisiert, Leerzeichenfolgen werden zu einem
Leerzeichen zusammengefasst, und Anfang und Ende werden getrimmt. Das Ergebnis muss 1 bis
``user.tag.name.max.length`` (Standard: 50) Zeichen lang sein und darf kein Steuer- oder
Formatzeichen enthalten.

Besitzer
::::::::

Gibt die Benutzer-ID der Anmeldung des Benutzers an, dem das Tag gehört. Besitzer und Name zusammen
kennzeichnen ein Tag; ein Besitzer kann also keine zwei Tags gleichen Namens haben, auch nicht auf
verschiedenen virtuellen Hosts.

Wenn Sie den Besitzer ändern, wird die Benutzerberechtigung des alten Besitzers unter
„Berechtigungen“ durch die des neuen Besitzers ersetzt.

Pfade
:::::

Gibt die URLs der Dokumente an, an die das Tag vergeben wird, eine pro Zeile. Eine URL muss dem Feld
``url`` eines indexierten Dokuments genau entsprechen; reguläre Ausdrücke werden nicht verwendet. Ein
Tag kann höchstens ``user.tag.max.paths`` (Standard: 10000) URLs haben.

Berechtigungen
::::::::::::::

Gibt die Benutzer, Gruppen und Rollen an, die das Tag sehen können, wie bei Labels: {user}Benutzername
für einen Benutzer, {group}Gruppenname für eine Gruppe und {role}Rollenname für eine Rolle. Bleibt
das Feld leer, sieht nur der Besitzer das Tag.

Der Besitzer sieht seine eigenen Tags immer, unabhängig von den Berechtigungen. Ein nicht
angemeldeter Benutzer sieht nie ein Tag, unabhängig von den Berechtigungen.

Virtueller Host
:::::::::::::::

Gibt den Hostnamen des virtuellen Hosts an, auf dem das Tag angezeigt wird. Ein von einem Benutzer
erstelltes Tag erhält den virtuellen Host, über den der Benutzer zugegriffen hat. Auf einem über einen
virtuellen Host aufgerufenen Suchbildschirm sind nur die Tags sichtbar, die hier diesen virtuellen
Hostnamen haben. Ein Zugriff, der keinem virtuellen Host entspricht, sieht die Tags unabhängig von
diesem Feld. Weitere Informationen finden Sie unter
:doc:`Virtueller Host im Konfigurationshandbuch <../config/security-virtual-host>`.

Sortierreihenfolge
::::::::::::::::::

Gibt die Anzeigereihenfolge des Tags an.

Konfiguration löschen
---------------------

Klicken Sie auf der Listenseite auf einen Namen und dann auf die Schaltfläche „Löschen“, um einen
Bestätigungsbildschirm anzuzeigen. Ein Klick auf „Löschen“ löscht das Tag, und sein Wert wird aus den
Dokumenten entfernt.

Freigabe
========

Gibt ein Benutzer ein Tag frei, werden die Werte von ``role.search.guest.permissions`` (Standard:
``{role}guest``) zu seinen Berechtigungen hinzugefügt. Ob ein Tag sichtbar ist, wird mit diesen
Werten zusätzlich zu den Rollen des angemeldeten Benutzers entschieden; ein freigegebenes Tag ist
daher für jeden angemeldeten Benutzer sichtbar, der auch danach filtern kann. Das Aufheben der
Freigabe entfernt nur diese Werte.

In diesem Bildschirm kann ein Administrator den Berechtigungen auch Gruppen oder Rollen hinzufügen,
um ein Tag nur bestimmten Benutzern zu zeigen. Nur der Besitzer und Administratoren können ein Tag
ändern; andere Benutzer können die für sie sichtbaren Tags nur anzeigen und zum Filtern verwenden.

Wie Änderungen die Dokumente erreichen
======================================

Ein Dokument speichert seine Tags im Feld ``tag`` des Index als ``base64url(Name):base64url(Besitzer)``.

- Das Erstellen, Bearbeiten und Löschen von Tags sowie das Vergeben und Entfernen durch Benutzer
  werden sofort in den Tags (Index ``fess_config.tag_type``) gespeichert. Die Dokumente werden über
  eine Warteschlange im Speicher aktualisiert, die der Job „Log Aggregator“ (``log_aggregator``)
  jede Minute gesammelt anwendet; die Suchergebnisse spiegeln eine Änderung daher erst nach bis zu
  etwa einer Minute wider.
- Das Ändern der Pfade in diesem Bildschirm aktualisiert die Dokumente der hinzugefügten und
  entfernten URLs. Das Ändern von Name oder Besitzer ersetzt den alten Wert an den Dokumenten durch
  den neuen.
- Wenn Dokumente durch einen Crawl oder einen Datenspeicher indexiert werden, wird ihr Feld ``tag``
  aus den Pfaden der Tags gesetzt; Tags bleiben daher bei einem erneuten Crawl erhalten.
- Der Job „Tag Updater“ (``tag_updater``) baut das Feld ``tag`` aller Dokumente aus den Tags neu auf.
  Er hat keinen Zeitplan; führen Sie ihn bei Bedarf über den Scheduler aus.

Hinweise für den Betrieb
========================

- **Führen Sie Log Aggregator auf jedem Knoten aus.** Jede JVM hat ihre eigene Warteschlange, die nur
  der Log Aggregator dieses Knotens verarbeitet. Belassen Sie das Ziel des Jobs ``log_aggregator``
  auf dem Standardwert ``all``; ist es auf einige Knoten beschränkt, erreichen die von den anderen
  Knoten angenommenen Änderungen die Dokumente nie.
- **Führen Sie Tag Updater in den folgenden Fällen aus.** Die Warteschlange liegt im Speicher, daher
  gehen noch nicht angewendete Änderungen bei einem Neustart von |Fess| verloren. Solange
  ``user.tag.enabled=false`` gilt, erreichen Tag-Änderungen die Dokumente nicht, und ein erneuter
  Crawl löscht ihr Feld ``tag``. Auch nach einer Wiederherstellung aus einer Sicherung müssen die
  Tags der Dokumente neu aufgebaut werden. Und wenn die Warteschlange ``user.tag.queue.max.size``
  (Standard: 10000) überschreitet, werden die überzähligen Änderungen mit einem WARN-Log verworfen.
  In jedem dieser Fälle baut ``tag_updater`` die Tags der Dokumente neu auf.
- **Der Besitzer eines Tags ist die Benutzer-ID der Anmeldung.** Ändert sich eine Benutzer-ID,
  bleiben die Tags bei der alten ID. Bei SAML muss die NameID persistent sein. Bei Entra ID ist der
  Besitzer der UPN, bei LDAP der Benutzername in der bei der Anmeldung eingegebenen Groß- und
  Kleinschreibung. Das Löschen eines Benutzers lässt seine Tags bestehen; löschen Sie nicht mehr
  benötigte Tags in diesem Bildschirm.
- **Vorhandene Indizes funktionieren ebenfalls.** Hat der Dokumentindex beim Start keine Zuordnung
  für das Feld ``tag``, wird sie als ``keyword`` hinzugefügt. Vorhandene Felder werden nicht
  geändert.
- Die Tags werden im Index ``fess_config.tag_type`` gespeichert. Sie sind in ``fess_config.bulk``
  einer Sicherung enthalten, nicht aber in ``fess_basic_config.bulk``.
