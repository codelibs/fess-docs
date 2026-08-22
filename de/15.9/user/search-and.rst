===========
AND-Suche
===========

Wenn Sie nach Dokumenten suchen möchten, die alle angegebenen Suchbegriffe enthalten, verwenden Sie die AND-Suche. Wenn Sie mehrere Wörter durch Leerzeichen getrennt in das Suchfeld eingeben, wird standardmäßig eine AND-Suche durchgeführt, sodass Sie AND auch weglassen können und dennoch das gleiche Ergebnis erhalten.

Verwendung
-----------

Um eine AND-Suche zu verwenden, fügen Sie AND zwischen den Suchbegriffen ein. AND
muss in Großbuchstaben geschrieben werden und erfordert Leerzeichen davor und danach. AND
kann auch weggelassen werden.

Wenn Sie beispielsweise nach Dokumenten suchen möchten, die sowohl "Suchbegriff1" als auch "Suchbegriff2" enthalten, geben Sie Folgendes in das Suchformular ein:

::

    Suchbegriff1 AND Suchbegriff2

Wenn Sie AND weglassen und stattdessen Folgendes eingeben, erhalten Sie das gleiche Ergebnis:

::

    Suchbegriff1 Suchbegriff2

Sie können mit AND auch drei oder mehr Suchbegriffe miteinander verknüpfen.

::

    Suchbegriff1 AND Suchbegriff2 AND Suchbegriff3

.. note::

    AND muss in Großbuchstaben geschrieben werden. Wenn es wie ``and`` in Kleinbuchstaben geschrieben wird, wird es nicht als Operator behandelt, sondern als gewöhnliches Suchwort "and" gesucht. ``&&`` kann ebenfalls mit derselben Bedeutung wie AND verwendet werden.

Mit runden Klammern ``( )`` können Sie die AND-Suche mit anderen Suchbedingungen kombinieren. Wenn Sie beispielsweise nach Dokumenten suchen möchten, die "Suchbegriff1" sowie entweder "Suchbegriff2" oder "Suchbegriff3" enthalten, geben Sie Folgendes ein:

::

    Suchbegriff1 AND (Suchbegriff2 OR Suchbegriff3)

Sie können die AND-Suche auch für bestimmte Felder durchführen. Im folgenden Beispiel werden Dokumente gesucht, die im Feld title "Suchbegriff1" sowie im Feld content "Suchbegriff2" enthalten.

::

    title:Suchbegriff1 AND content:Suchbegriff2
