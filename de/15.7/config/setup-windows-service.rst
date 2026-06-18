================================
Registrierung als Windows-Dienst
================================

Registrierung als Windows-Dienst
=================================

|Fess| kann als Windows-Dienst registriert werden. Nach der Registrierung als Dienst kann |Fess| beim Systemstart automatisch gestartet werden.
Zum Betrieb von |Fess| muss OpenSearch gestartet sein.
In diesem Dokument wird davon ausgegangen, dass |Fess| unter ``c:\opt\fess`` und OpenSearch unter ``c:\opt\opensearch`` installiert sind (passen Sie die Pfade an Ihre Umgebung an).

.. note::
   |Fess| und OpenSearch unterstützen ausschließlich die 64-Bit-Version.

Vorbereitung
------------

Setzen Sie ``JAVA_HOME`` als Systemumgebungsvariable. ``service.bat`` wird mit einem Fehler beendet, wenn ``JAVA_HOME`` nicht gesetzt ist.

Registrierung von OpenSearch als Dienst
----------------------------------------

Öffnen Sie die Eingabeaufforderung mit Administratorrechten und führen Sie ``c:\opt\opensearch\bin\opensearch-service.bat`` aus.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

Weitere Informationen finden Sie in der `OpenSearch-Dokumentation <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/windows/>`_.

Konfiguration von |Fess|
------------------------

Der Dienst wird über ``c:\opt\fess\bin\service.bat`` registriert. ``service.bat`` liest bei der Registrierung ``bin\fess.in.bat`` ein und übernimmt dessen Inhalt als Startoptionen für |Fess|.
Fügen Sie die Verbindungseinstellungen für OpenSearch in ``c:\opt\fess\bin\fess.in.bat`` ein.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=c:/opt/opensearch/data/config/

.. note::
   - Geben Sie unter ``fess.search_engine.http_address`` die Verbindungsadresse des registrierten OpenSearch-Dienstes an. Ohne diese Einstellung kann |Fess| die Verbindungsadresse nicht ermitteln und startet die eingebettete OpenSearch-Version, die in Produktionsumgebungen nicht empfohlen wird.
   - Wenn OpenSearch auf einem anderen Host läuft, ändern Sie den Hostnamen oder die IP-Adresse entsprechend.
   - Verwenden Sie ``/`` als Pfadtrennzeichen.

Die Standard-Portnummer für Such- und Verwaltungsoberfläche von |Fess| ist ``8080``. Um den Port zu ändern, bearbeiten Sie ``-Dfess.port`` in ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80

.. note::
   Bei der Registrierung als Dienst ist ``-Dfess.port=8080`` auch in ``FESS_PARAMS`` in ``bin\service.bat`` fest eingetragen. Da dieser Wert Vorrang vor der Einstellung in ``fess.in.bat`` hat, muss beim Ändern des Ports auch ``FESS_PARAMS`` in ``service.bat`` entsprechend angepasst werden.

Dienstanpassung (optional)
--------------------------

Durch das Setzen von Umgebungsvariablen vor der Ausführung von ``service.bat install`` kann die Dienstkonfiguration angepasst werden. Die wichtigsten Umgebungsvariablen sind:

.. list-table::
   :header-rows: 1

   * - Umgebungsvariable
     - Beschreibung
   * - ``FESS_START_TYPE``
     - Starttyp (``auto`` oder ``manual``). Standardwert ist ``manual``.
   * - ``FESS_HEAP_SIZE``
     - Heap-Größe (z. B. ``1g``). Um minimale und maximale Heap-Größe separat anzugeben, verwenden Sie ``FESS_MIN_MEM`` (Standard ``256m``) und ``FESS_MAX_MEM`` (Standard ``1g``).
   * - ``SERVICE_USERNAME`` / ``SERVICE_PASSWORD``
     - Windows-Konto, unter dem der Dienst ausgeführt wird.
   * - ``SERVICE_DISPLAY_NAME``
     - Anzeigename des Dienstes.
   * - ``SERVICE_DESCRIPTION``
     - Beschreibung des Dienstes.

Registrierungsmethode
---------------------

Führen Sie ``c:\opt\fess\bin\service.bat`` aus einer Eingabeaufforderung mit Administratorrechten aus.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.

Dienstkonfiguration
-------------------

Beim manuellen Start des Dienstes starten Sie zuerst den OpenSearch-Dienst und dann den |Fess|-Dienst.
Für den automatischen Start beim Systemstart werden Starttyp und Abhängigkeiten konfiguriert.

1. Setzen Sie in den allgemeinen Diensteinstellungen den Starttyp auf „Automatisch (Verzögerter Start)".
2. Dienstabhängigkeiten werden in der Registrierung konfiguriert.

Fügen Sie im Registrierungs-Editor (regedit) den folgenden Schlüssel und Wert hinzu.

.. list-table::

   * - *Schlüssel*
     - ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fess-service-x64\DependOnService``
   * - *Wert*
     - ``opensearch-service-x64``

Nach dem Hinzufügen wird opensearch-service-x64 in den Abhängigkeiten der |Fess|-Diensteigenschaften angezeigt.

.. note::
   Wenn Sie die Umgebungsvariable ``FESS_START_TYPE=auto`` vor ``service.bat install`` setzen, wird der Starttyp als „Automatisch" registriert. Da „Automatisch (Verzögerter Start)" und die Konfiguration von Abhängigkeiten über ``service.bat`` nicht möglich sind, führen Sie diese Einstellungen wie oben beschrieben durch.

Dienstverwaltung
----------------

Mit ``service.bat`` können die folgenden Befehle zur Steuerung des Dienstes verwendet werden.

.. list-table::
   :header-rows: 1

   * - Befehl
     - Beschreibung
   * - ``service.bat install``
     - Registriert den Dienst.
   * - ``service.bat remove``
     - Entfernt den Dienst.
   * - ``service.bat start``
     - Startet den Dienst.
   * - ``service.bat stop``
     - Stoppt den Dienst.
   * - ``service.bat manager``
     - Startet die grafische Benutzeroberfläche zur Dienstverwaltung.
