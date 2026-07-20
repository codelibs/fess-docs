===========
NOT-Suche
===========

Wenn Sie nach Dokumenten suchen möchten, die ein bestimmtes Wort nicht enthalten, können Sie die NOT-Suche verwenden.
Dies wird auch als Ausschlusssuche bezeichnet und ist hilfreich, wenn Sie bestimmte Schlüsselwörter aus den Suchergebnissen ausschließen und dadurch irrelevante Treffer reduzieren möchten.

Verwendung
-----------

Bei der NOT-Suche wird NOT vor das Wort gesetzt, das nicht enthalten sein soll. NOT
muss in Großbuchstaben geschrieben werden und erfordert Leerzeichen davor und danach.

Wenn Sie beispielsweise nach Dokumenten suchen möchten, die "Suchbegriff1" enthalten, aber "Suchbegriff2" nicht enthalten, geben Sie Folgendes ein:

::

    Suchbegriff1 NOT Suchbegriff2

.. note::

    NOT muss in Großbuchstaben geschrieben werden. Wenn es wie ``not`` in Kleinbuchstaben geschrieben wird, wird es nicht als Operator behandelt, sondern als gewöhnliches Suchwort "not" gesucht. Wird zudem direkt vor dem auszuschließenden Wort ein ``-`` vorangestellt, wie in ``Suchbegriff1 -Suchbegriff2``, hat dies dieselbe Bedeutung wie NOT.

Mit runden Klammern ``( )`` können Sie die NOT-Suche mit anderen Suchbedingungen kombinieren. Wenn Sie beispielsweise nach Dokumenten suchen möchten, die entweder "Suchbegriff1" oder "Suchbegriff2" enthalten, aber "Suchbegriff3" nicht enthalten, geben Sie Folgendes ein:

::

    (Suchbegriff1 OR Suchbegriff2) NOT Suchbegriff3

Sie können die NOT-Suche auch für ein bestimmtes Feld durchführen. Im folgenden Beispiel werden Dokumente gesucht, die im Feld title "Suchbegriff1" enthalten, aber im Feld title "Suchbegriff2" nicht enthalten.

::

    title:Suchbegriff1 NOT title:Suchbegriff2

Siehe auch
-----------

- :doc:`search-and`
- :doc:`search-or`
- :doc:`special-char`
