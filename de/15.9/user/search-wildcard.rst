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

kann innerhalb des Suchbegriffs verwendet werden. Außerdem

::

    *test

kann auch am Anfang des Suchbegriffs verwendet werden.

Sie können die Wildcard-Suche auch auf ein bestimmtes Feld anwenden. Im folgenden Beispiel werden im Feld title Dokumente gesucht, die ein mit te beginnendes und mit t endendes Wort enthalten.

::

    title:te*t

Wenn kein Feld angegeben wird, erfolgt die Suche in den Feldern title und content.

Nutzungsbedingungen
---------------------

Beachten Sie bei der Verwendung der Wildcard-Suche die folgenden Punkte:

* Wildcards werden auf im Index registrierte Zeichenketten (Token) angewendet. Da der Suchbegriff nicht erneut analysiert wird, funktionieren Wildcards für Japanisch nicht wie erwartet, wenn der Index beispielsweise mit bi-gram erstellt wurde, da Japanisch dabei als bedeutungslose Zeichenkette fester Länge behandelt wird. Wenn Sie Wildcards für Japanisch verwenden möchten, nutzen Sie bitte Felder, die morphologische Analyse verwenden.
* Wildcard-Muster unterscheiden zwischen Groß- und Kleinschreibung. Da im Index registrierte Wörter normalerweise in Kleinbuchstaben umgewandelt werden, verwenden Sie im Muster bitte Kleinbuchstaben. Beispielsweise stimmt ``Test*`` nicht mit dem in Kleinbuchstaben registrierten ``test`` überein.
* Eine Suche mit einer Wildcard am Anfang (zum Beispiel ``*test``) durchsucht alle Wörter im Index und kann daher länger dauern.
