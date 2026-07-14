==========
OR-Suche
==========

Wenn Sie nach Dokumenten suchen möchten, die einen der Suchbegriffe enthalten, verwenden Sie die OR-Suche. Wenn Sie mehrere Wörter in das Suchfeld eingeben, wird standardmäßig eine AND-Suche durchgeführt.

Verwendung
-----------

Um eine OR-Suche zu verwenden, fügen Sie OR zwischen den Suchbegriffen ein. OR
muss in Großbuchstaben geschrieben werden und erfordert Leerzeichen davor und danach.

Wenn Sie beispielsweise nach Dokumenten suchen möchten, die entweder "Suchbegriff1" oder "Suchbegriff2" enthalten, geben Sie Folgendes in das Suchformular ein:

::

    Suchbegriff1 OR Suchbegriff2

Sie können mit OR auch drei oder mehr Suchbegriffe miteinander verknüpfen.

::

    Suchbegriff1 OR Suchbegriff2 OR Suchbegriff3

.. note::

    OR muss in Großbuchstaben geschrieben werden. Wenn es wie ``or`` in Kleinbuchstaben geschrieben wird, wird es nicht als Operator behandelt, sondern als gewöhnliches Suchwort "or" gesucht. ``||`` kann ebenfalls mit derselben Bedeutung wie OR verwendet werden.

Mit runden Klammern ``( )`` können Sie die OR-Suche mit anderen Suchbedingungen kombinieren. Wenn Sie beispielsweise nach Dokumenten suchen möchten, die entweder "Suchbegriff1" oder "Suchbegriff2" sowie "Suchbegriff3" enthalten, geben Sie Folgendes ein:

::

    (Suchbegriff1 OR Suchbegriff2) Suchbegriff3

Sie können die OR-Suche auch für bestimmte Felder durchführen. Im folgenden Beispiel werden Dokumente gesucht, die im Feld title "Suchbegriff1" oder im Feld content "Suchbegriff2" enthalten.

::

    title:Suchbegriff1 OR content:Suchbegriff2
