========================
Versteckte Suchkriterien
========================

Wenn Sie eine bestimmte Suchbedingung weitergeben möchten, ohne deren Text auf dem Bildschirm anzuzeigen, können Sie den Parameter ``ex_q`` verwenden. Die in ``ex_q`` angegebene Bedingung wird nicht im Suchfeld angezeigt und bleibt auch dann erhalten, wenn der Bildschirm durch Paginierung oder Facettenfilterung aktualisiert wird.

In ``ex_q`` können Sie dieselbe Abfragesyntax wie beim regulären Suchbegriff (``q``) verwenden – das Format ``field:value``, Phrasen, Bereichsangaben, Operatoren wie ``OR`` und weitere. Die angegebene Bedingung wird bei der Suche standardmäßig per AND mit der Bedingung von ``q`` verknüpft. Das heißt, Dokumente, die der Bedingung von ``ex_q`` nicht entsprechen, werden aus den Suchergebnissen ausgeschlossen.

Verwendung
----------

Wenn Sie eine Suche ausführen (z. B. über ein Suchformular), fügen Sie den Wert von ``ex_q`` als verstecktes Formularfeld oder als URL-Abfrageparameter hinzu und führen Sie die Suche aus. So können Sie suchen, ohne die Bedingung auf dem Bildschirm anzuzeigen.

Sie können ``ex_q`` mehrfach angeben. Wie im folgenden Beispiel gezeigt, wird bei Übergabe mehrerer ``ex_q``-Werte jeder davon als Suchbedingung hinzugefügt (leere oder doppelte Werte werden ignoriert).

.. code-block:: none

    /search?q=keyword&ex_q=label:manual&ex_q=filetype:pdf

Beibehaltung bei der Paginierung
--------------------------------

Fess fügt Paginierungslinks (z. B. nächste/vorherige Seite) und Links zur Facettenfilterung automatisch den Wert von ``ex_q`` hinzu. Dadurch bleibt die Bedingung von ``ex_q`` auch dann erhalten, wenn der Bildschirm durch diese Aktionen aktualisiert wird.

Wird dagegen über das normale Suchfeld ein Suchbegriff eingegeben und erneut gesucht, wird ``ex_q`` nicht übernommen. Wenn die Bedingung auch über das Suchfeld erhalten bleiben soll, richten Sie in Ihrem eigenen Suchformular ein verstecktes ``ex_q``-Feld ein und senden Sie ``ex_q`` bei jeder Suche mit.

.. note::

    * Wenn die Länge eines einzelnen ``ex_q``-Werts ``query.max.length`` (Standardwert: 1000 Zeichen) überschreitet, wird dieser Wert ohne Fehlermeldung ignoriert.
    * ``ex_q`` kann nicht nur für die Suche im Web-Bildschirm, sondern auch über die Such-API (``/api/v2``) verwendet werden. In der API gelten die Obergrenze für die Anzahl der ``ex_q``-Elemente pro Anfrage (``api.v2.param.max.array.size``, Standardwert: 100) sowie die Obergrenze für die Länge jedes Elements (``api.v2.param.max.length``, Standardwert: 1000 Zeichen).
