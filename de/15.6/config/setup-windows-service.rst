===================
Registrierung als Windows-Dienst
===================

Registrierung als Windows-Dienst
======================

|Fess| kann als Windows-Dienst registriert werden.
Zum Betrieb von |Fess| muss OpenSearch gestartet sein.
In diesem Dokument wird davon ausgegangen, dass |Fess| unter ``c:\opt\fess`` und OpenSearch unter ``c:\opt\opensearch`` installiert sind.

Vorbereitung
------

Setzen Sie JAVA_HOME als Systemumgebungsvariable.

Registrierung von OpenSearch als Dienst
-------------------------

Führen Sie ``c:\opt\opensearch\bin\opensearch-service.bat`` als Administrator von der Eingabeaufforderung aus.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

Weitere Informationen finden Sie in der `OpenSearch-Dokumentation <https://opensearch.org/docs/2.4/install-and-configure/install-opensearch/windows/>`_.

Konfiguration
----

Bearbeiten Sie ``c:\opt\fess\bin\fess.in.bat`` und setzen Sie den Installationspfad von OpenSearch in SEARCH_ENGINE_HOME.

::

    set SEARCH_ENGINE_HOME=c:/opt/opensearch

Die Standardportnummer für Such- und Verwaltungsoberfläche von |Fess| ist 8080. Um auf Port 80 zu ändern, ändern Sie fess.port in ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80


Registrierungsmethode
------

Führen Sie ``c:\opt\fess\bin\service.bat`` als Administrator von der Eingabeaufforderung aus.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.


Dienstkonfiguration
-----------

Beim manuellen Start des Dienstes starten Sie zuerst den OpenSearch-Dienst und dann den |Fess|-Dienst.
Für den automatischen Start fügen Sie eine Abhängigkeit hinzu.

1. Setzen Sie in den allgemeinen Diensteinstellungen den Starttyp auf „Automatisch (verzögerter Start)".
2. Dienstabhängigkeiten werden in der Registry konfiguriert.

Fügen Sie im Registrierungs-Editor (regedit) den folgenden Schlüssel und Wert hinzu.

.. list-table::

   * - *Schlüssel*
     - ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fess-service-x64\DependOnService``
   * - *Wert*
     - ``opensearch-service-x64``

Nach dem Hinzufügen wird opensearch-service-x64 in den Abhängigkeiten der |Fess|-Diensteigenschaften angezeigt.
