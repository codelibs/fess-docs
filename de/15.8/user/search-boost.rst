==================
Boost-Suche
==================

Boost-Suche (Gewichtete Suche)
================================

Wenn Sie unter den Suchbegriffen einen bestimmten Suchbegriff bevorzugen möchten, verwenden Sie die Boost-Suche. Mit der Boost-Suche ist eine Suche entsprechend der Wichtigkeit der Suchbegriffe möglich.

Verwendung
------------

Um die Boost-Suche zu verwenden, geben Sie den Boost-Wert (Gewichtungswert) unmittelbar nach dem Suchbegriff im Format „^Boost-Wert“ an. Zwischen dem Suchbegriff und dem Boost-Wert darf kein Leerzeichen stehen.

Wenn Sie beispielsweise bei der Suche nach „Apfel Orange“ „Apfel“ stärker gewichten möchten, geben Sie Folgendes in das Suchformular ein:

::

    Apfel^100 Orange

In diesem Beispiel wird der Boost-Wert nur auf „Apfel“ angewendet, nicht auf „Orange“.

Boost-Wert
------------

Als Boost-Wert geben Sie eine Zahl an. Neben Ganzzahlen können auch Dezimalzahlen wie ``2.5`` angegeben werden.

- Bei Angabe eines Werts größer als 1 erhöht sich die Gewichtung dieses Suchbegriffs.
- Bei Angabe eines Werts größer als 0 und kleiner als 1 (z. B. ``0.5``) verringert sich die Gewichtung dieses Suchbegriffs.

Der Boost-Wert legt nicht absolut die Score der Suchergebnisse fest, sondern passt die relative Gewichtung im Verhältnis zu den anderen Suchbegriffen an.

Kombination mit anderer Suchsyntax
------------------------------------

Die Boost-Suche kann mit anderer Suchsyntax kombiniert werden. So kann beispielsweise auch einem Suchbegriff, für den ein Feld angegeben ist, ein Boost-Wert hinzugefügt werden.

::

    title:Apfel^100 Orange

In diesem Beispiel werden Dokumente bevorzugt, die im Feld title „Apfel“ enthalten.
