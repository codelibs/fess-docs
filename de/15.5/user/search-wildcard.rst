====================
Wildcard-Suche
====================

Sie können Wildcards für ein oder mehrere Zeichen innerhalb von Suchbegriffen verwenden. ? kann als Wildcard für ein Zeichen angegeben werden, und \* kann als Wildcard für mehrere Zeichen angegeben werden. Wildcards können für Wörter verwendet werden. Wildcard-Suchen für Sätze sind nicht möglich.

Verwendung
-----------

Um ein Ein-Zeichen-Wildcard zu verwenden, nutzen Sie ? wie folgt:

::

    te?t

In diesem Fall wird es als Ein-Zeichen-Wildcard behandelt, z. B. text oder test.

Um ein Mehrzeichen-Wildcard zu verwenden, nutzen Sie \* wie folgt:

::

    test*

In diesem Fall wird es als Mehrzeichen-Wildcard behandelt, z. B. test, tests oder tester. Außerdem

::

    te*t

kann innerhalb des Suchbegriffs verwendet werden.

Nutzungsbedingungen
---------------------

Wildcards werden auf im Index registrierte Zeichenketten angewendet.
Daher funktionieren Wildcards für Japanisch nicht wie erwartet, wenn der Index mit bi-gram erstellt wurde, da Japanisch als bedeutungslose Zeichenkette mit fester Länge behandelt wird.
Um Wildcards für Japanisch zu verwenden, nutzen Sie bitte Felder, die morphologische Analyse verwenden.
