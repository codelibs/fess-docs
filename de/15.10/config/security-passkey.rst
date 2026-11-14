==================================================
Konfiguration der Anmeldung mit Passkey (WebAuthn)
==================================================

Übersicht
=========

|Fess| ermöglicht es einem lokalen Benutzer (einem Benutzer, der unter „Benutzer“ in der Administrationsoberfläche angelegt wurde), sich statt mit einem Passwort mit einem Passkey (WebAuthn) anzumelden. Die Funktion ist neu in 15.10 und standardmäßig deaktiviert.

- Ein Benutzer kann sich entweder mit dem Passwort oder mit einem Passkey anmelden. Es handelt sich nicht um eine Multi-Faktor-Authentifizierung, die beides verlangt.
- Erfasst werden nur lokale Benutzer des Index ``fess_user``. Ein LDAP- oder SSO-Benutzer kann keinen Passkey registrieren, und eine Anmeldung mit Passkey fragt nie LDAP ab.
- |Fess| speichert den öffentlichen Schlüssel und den Namen eines Passkeys und Ähnliches. Der private Schlüssel bleibt im Authenticator des Benutzers (ein Browser, ein Betriebssystem, ein Sicherheitsschlüssel usw.) und gelangt nie zu |Fess|.

Einstellungen
=============

Die Passkey-Einstellungen gehören in ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` beim ZIP-Paket, ``/etc/fess/fess_config.properties`` beim RPM/DEB-Paket). In der Administrationsoberfläche gibt es unter „System“ > „Allgemein“ kein Feld dafür, und sie können nicht in ``system.properties`` gesetzt werden. Zum Übernehmen einer Änderung ist ein Neustart von |Fess| erforderlich. Bei Docker können Sie sie als ``-Dfess.config.passkey.enabled=true`` in ``FESS_JAVA_OPTS`` übergeben (siehe :doc:`../install/install-docker`).

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Schlüssel
     - Standardwert
     - Beschreibung
   * - ``passkey.enabled``
     - ``false``
     - Aktiviert die Anmeldung mit Passkey. Auch bei ``true`` bleibt die Funktion deaktiviert, solange ``passkey.rp.id`` und ``passkey.origins`` unten keine verwendbaren Werte enthalten.
   * - ``passkey.rp.id``
     - (leer)
     - Relying-Party-ID: die Domain, an die die Passkeys gebunden sind (zum Beispiel ``example.com``). Ein Passkey funktioniert nur auf diesem Host und seinen Subdomains.
   * - ``passkey.rp.name``
     - ``Fess``
     - Der Name der Relying Party, den der Browser beim Erstellen eines Passkeys anzeigt.
   * - ``passkey.origins``
     - (leer)
     - Die Origins (durch Komma getrennt), von denen ein Passkey-Vorgang angenommen wird (zum Beispiel ``https://fess.example.com``). Jeder Eintrag muss eine ``http``- oder ``https``-Origin mit Hostnamen sein.

Ein Beispiel, das die Funktion aktiviert:
::

    passkey.enabled=true
    passkey.rp.id=example.com
    passkey.rp.name=Fess
    passkey.origins=https://fess.example.com

- ``passkey.rp.id`` ist die Domain, an die jeder Passkey gebunden ist. Wird sie geändert, nachdem Benutzer Passkeys registriert haben, werden alle unbrauchbar, und die Benutzer müssen sich unter der neuen ID erneut registrieren. Wählen Sie sie daher nur einmal. Der Host jeder Origin in ``passkey.origins`` muss ``passkey.rp.id`` oder eine Subdomain davon sein.
- ``passkey.origins`` listet unverändert die Origins (Schema, Host und Port) auf, unter denen Benutzer |Fess| im Browser öffnen, nicht die Adressen hinter einem Reverse-Proxy. Ein Vorgang von einer anderen Origin wird abgelehnt.

Wenn die Funktion deaktiviert bleibt
------------------------------------

Auch mit ``passkey.enabled=true`` bleiben die Passkeys in den folgenden Fällen **ohne jede Fehlermeldung auf dem Bildschirm deaktiviert**. Die Anmeldebildschirme zeigen keine Passkey-Schaltfläche, jede API unter ``/api/v2/auth/passkey`` antwortet mit ``404``, und ``features.passkey_enabled`` von ``/api/v2/ui/config`` ist ``false``. Der Grund steht in einer Warnung in ``fess.log``; jede Warnung wird nach dem Start nur einmal geschrieben.

- ``passkey.rp.id`` oder ``passkey.origins`` ist leer: ``passkey.enabled is true but passkey.rp.id or passkey.origins is empty, so passkeys are disabled.``
- ``passkey.origins`` enthält keinen Eintrag: ``passkey.enabled is true but passkey.origins holds no origin, so passkeys are disabled.``
- ``passkey.origins`` enthält einen Eintrag, der keine ``http``- oder ``https``-Origin ist (ein Wert ohne Hostnamen, ein anderes Schema usw.): ``passkey.origins holds an entry that is not an http or https origin, so passkeys are disabled: entry=...``

Ist ``passkey.origins`` verwendbar, aber die Origin, die ein Benutzer öffnet, nicht darin enthalten, wird jede Registrierung und jede Anmeldung abgelehnt. Der Bildschirm des Benutzers nennt keinen Grund, sehen Sie daher in ``fess.log`` nach: ``A passkey response came from an origin that is not in passkey.origins: origin=...`` zeigt die abgelehnte Origin und die Einstellung (nur die erste wird geschrieben). Ergänzen Sie diese Origin in ``passkey.origins``.

Verwendung
==========

Anmeldung
---------

Sind Passkeys aktiviert und unterstützt der Browser WebAuthn, erscheint in der Anmeldung des Suchbildschirms und auf der Anmeldeseite der Administrationsoberfläche die Schaltfläche „Mit Passkey anmelden“. Der Browser fragt nach dem Authenticator, und der Benutzer meldet sich an, ohne einen Benutzernamen einzugeben.

Eine Anmeldung mit Passkey unterliegt demselben Limit je IP-Adresse (``theme.api.login.*``) wie eine Anmeldung mit Passwort. Ein Fehlversuch wird angerechnet, ein Erfolg gibt die Anrechnung zurück (siehe :doc:`rate-limiting`). Der Bildschirm nennt den Grund eines Fehlschlags nicht; er zeigt dieselbe Meldung wie bei einem falschen Passwort.

Passkeys registrieren und löschen
---------------------------------

Ein lokaler Benutzer registriert und löscht seine eigenen Passkeys im Abschnitt „Passkeys“ auf „Passwort ändern“ (``/profile``) im Benutzermenü des Suchbildschirms.

1. Geben Sie einen Namen für den Passkey (bis zu 64 Zeichen) und das aktuelle Passwort ein und klicken Sie auf „Passkey registrieren“.
2. Folgen Sie den Hinweisen des Browsers, um den Passkey auf einem Authenticator zu erstellen.

- Für jede Registrierung ist das aktuelle Passwort erforderlich. Ein lokaler Benutzer, dessen Name und Passwort auch das Verzeichnis (LDAP) akzeptiert, kann keinen Passkey registrieren, weil die Passwortprüfung nicht erkennen kann, welches Konto sie geprüft hat.
- Ein Benutzer kann bis zu 20 Passkeys haben.
- Der Abschnitt „Passkeys“ wird einem Benutzer nicht angezeigt, der keine Passkeys hat und keinen registrieren kann (ein LDAP- oder SSO-Benutzer oder ein Browser ohne WebAuthn).
- Das Löschen eines Passkeys **beendet die übrigen Anmeldesitzungen** des Benutzers, damit eine mit einem verlorenen Authenticator geöffnete Sitzung nicht bestehen bleibt. Es funktioniert wie eine Passwortänderung (siehe „Beziehung zum Passwort“ unten). Die Sitzung, die das Löschen vorgenommen hat, bleibt bestehen.

Aktionen des Administrators
---------------------------

Die Detailseite eines Benutzers unter „Benutzer“ in der Administrationsoberfläche listet die Passkeys des Benutzers auf (Bezeichnung, Erstellungszeitpunkt, Zeitpunkt der letzten Verwendung). Ein Administrator kann keinen Passkey registrieren, aber ein Administrator mit Bearbeitungsberechtigung kann einen mit „Zurücksetzen“ löschen, zum Beispiel wenn der Benutzer den Authenticator verloren hat. Der Benutzer kann dann einen neuen Passkey registrieren. Ein Zurücksetzen beendet außerdem die Anmeldesitzungen dieses Benutzers (siehe „Beziehung zum Passwort“ unten).

Nachdem ``passkey.enabled`` wieder auf ``false`` gesetzt wurde, listet die Detailseite die Passkeys eines Benutzers, der welche hat, weiterhin auf, und sie können gelöscht werden. Das Deaktivieren der Funktion löscht keine Passkey-Daten.

Beziehung zum Passwort
======================

- Ein Passkey und ein Passwort sind getrennte Zugangsdaten. Wird das Passwort eines Benutzers geändert oder von einem Administrator neu gesetzt, werden die registrierten Passkeys nicht gelöscht, und sie können weiterhin zur Anmeldung verwendet werden.
- Wird ein Passwort geändert, enden die übrigen Anmeldesitzungen des Benutzers (siehe :doc:`../install/security`). Das schließt eine mit einem Passkey geöffnete Sitzung ein. Jede Sitzung prüft höchstens einmal je ``password.changed.check.interval`` Sekunden (Standard ``60``), sodass die Sitzungen innerhalb dieser Zeit enden.
- Das Löschen eines Passkeys beendet die übrigen Sitzungen auf dieselbe Weise (siehe oben).

Löschen und Umbenennen von Benutzern
====================================

Ein Passkey ist nur über den Benutzernamen an einen Benutzer gebunden. Damit ein anderer Benutzer desselben Namens ihn nicht erbt, werden Passkeys auch in diesen Fällen gelöscht:

- Wenn ein Benutzer gelöscht wird.
- Wenn ein Benutzer angelegt wird (jeder unter diesem Namen verbliebene Passkey wird gelöscht).
- Wenn ein Benutzer umbenannt wird (die Passkeys des bisherigen und des neuen Namens werden gelöscht). Ein Passkey folgt einer Umbenennung nicht, der Benutzer registriert sich daher erneut. Eine Umbenennung in einen Namen, den bereits ein anderer Benutzer hat, wird abgelehnt, bevor ein Passkey gelöscht wird.

Speicherung und Sicherung
=========================

Passkeys werden im Index ``fess_user.passkey`` gespeichert (das Präfix ist ``index.user.index``, standardmäßig ``fess_user``). Der Index wird beim Start von |Fess| auch dann angelegt, wenn Passkeys deaktiviert sind, und er wird beim Löschen oder Umbenennen eines Benutzers sowie auf der Benutzerdetailseite verwendet. Darf |Fess| keine Indizes anlegen, legen Sie ihn vor dem Upgrade an (siehe :ref:`upgrade-1510-passkey`).

Der Index gehört nicht zum Alias ``fess_user``, daher enthält ``fess_user.bulk`` unter „Sicherung“ in der Administrationsoberfläche keine Passkeys. Nach einer Wiederherstellung aus einer Sicherung registrieren die Benutzer ihre Passkeys erneut.

Anforderungen
=============

- **HTTPS**: Browser erlauben WebAuthn nur in einem sicheren Kontext (HTTPS oder ``localhost``). |Fess| akzeptiert in ``passkey.origins`` auch eine ``http``-Origin, aber betreiben Sie |Fess| in der Produktion über HTTPS und geben Sie ``https://``-Origins an (siehe „HTTPS aktivieren“ in :doc:`../install/security`).
- **Browser**: Erforderlich ist ein Browser mit der WebAuthn-API (``PublicKeyCredential``). In einem Browser ohne sie werden weder die Anmeldeschaltfläche noch der Registrierungsabschnitt angezeigt.
- **Authenticator**: Er muss auffindbare Anmeldedaten (Discoverable Credentials) und die Benutzerverifizierung (PIN, Biometrie usw.) unterstützen. |Fess| verlangt beides, unterstützt die Signaturalgorithmen ES256 und RS256 und verwendet keine Attestation.
- **Mehrere Knoten**: Die Challenge eines Passkey-Vorgangs wird 5 Minuten lang in der HTTP-Sitzung gehalten. Wenn Sie mehrere Knoten hinter einem Load Balancer betreiben, teilen Sie die Sitzungen zwischen den Knoten (Umgebungsvariable ``FESS_SESSION_STORE=opensearch``) oder lassen Sie den Load Balancer jede Sitzung an einen Knoten binden.

API
===

Die Passkey-APIs liegen unter ``/api/v2/auth/passkey``. Alle antworten mit ``404``, solange Passkeys deaktiviert sind. ``features.passkey_enabled`` von ``/api/v2/ui/config`` zeigt an, ob die Funktion verfügbar ist (siehe :doc:`../api/api-uiconfig`).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Endpunkt
     - Beschreibung
   * - ``POST /api/v2/auth/passkey/login/options``
     - Ruft die Anmeldeoptionen (die Challenge) ab.
   * - ``POST /api/v2/auth/passkey/login/verify``
     - Prüft die Antwort des Authenticators und meldet an.
   * - ``GET /api/v2/auth/passkey``
     - Listet die Passkeys des angemeldeten Benutzers auf und zeigt an, ob der Benutzer einen registrieren kann (``can_register``).
   * - ``POST /api/v2/auth/passkey/register/options``
     - Prüft das aktuelle Passwort (``current_password``) und ruft die Registrierungsoptionen ab.
   * - ``POST /api/v2/auth/passkey/register/verify``
     - Prüft den Namen (``label``) und die Antwort des Authenticators und registriert den Passkey.
   * - ``DELETE /api/v2/auth/passkey/{credentialId}``
     - Löscht einen Passkey des angemeldeten Benutzers.

Die ``register``-Aufrufe und das Löschen benötigen den Header ``X-Fess-CSRF-Token``. Die beiden Anmeldeaufrufe benötigen wie ``/api/v2/auth/login`` kein CSRF-Token.

Fehlerbehebung
==============

Die Passkey-Schaltfläche wird nicht angezeigt
---------------------------------------------

- Prüfen Sie ``features.passkey_enabled`` von ``/api/v2/ui/config``. Ist es ``false``, suchen Sie in ``fess.log`` nach einer Warnung, um zu sehen, ob die Einstellungen verwendbar sind (siehe „Wenn die Funktion deaktiviert bleibt“ oben).
- Prüfen Sie, ob |Fess| nach der Änderung neu gestartet wurde.
- Prüfen Sie, ob der Browser WebAuthn unterstützt und die Seite über HTTPS (oder ``localhost``) geöffnet wurde.
- Wenn Sie ein anderes als das mitgelieferte Theme verwenden, muss das Theme die Passkey-Schaltfläche unterstützen.

Registrierung oder Anmeldung schlägt fehl
-----------------------------------------

- Enthält ``fess.log`` eine Warnung mit ``is not in passkey.origins``, ergänzen Sie die im Browser geöffnete Origin in ``passkey.origins``.
- Nachdem ``passkey.rp.id`` geändert wurde, können die davor registrierten Passkeys nicht mehr verwendet werden. Löschen Sie die alten Passkeys und registrieren Sie sich erneut.
