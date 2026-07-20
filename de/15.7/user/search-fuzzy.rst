================
Unscharfe Suche
================

Unscharfe Suche (Fuzzy-Suche)
===============================

Wenn Sie auch nach Wörtern suchen möchten, die nicht exakt mit dem Suchbegriff übereinstimmen, können Sie die unscharfe Suche verwenden. |Fess| unterstützt unscharfe Suche (Fuzzy-Suche) basierend auf der Levenshtein-Distanz.
Dies ist hilfreich, wenn Sie auch Dokumente finden möchten, die aufgrund von Tippfehlern, abweichender Schreibweise oder Rechtschreibvarianten nicht exakt mit dem Suchbegriff übereinstimmen.
Die Levenshtein-Distanz (Editierdistanz) gibt dabei an, wie stark sich zwei Wörter voneinander unterscheiden.

Verwendung
-----------

Fügen Sie "~" nach dem Suchbegriff hinzu, auf den Sie die unscharfe Suche anwenden möchten.

Wenn Sie beispielsweise das Wort "Fess" unscharf suchen möchten, können Sie durch Eingabe des Folgenden in das Suchformular Dokumente finden, die Wörter enthalten, die "Fess" ähnlich sind (z. B. "Fes").

::

    Fess~

Der Grad der Unschärfe lässt sich angeben, indem Sie nach „~" eine Zahl zwischen 0 und 2 anhängen.
Die Zahl gibt die maximal zulässige Editierdistanz (Levenshtein-Distanz), also die Höchstanzahl an Zeicheneinfügungen, -löschungen und -ersetzungen, an. Wird sie weggelassen, gilt die standardmäßige Editierdistanz.

::

    Fess~1
    Fess~2

Mit ``~2`` werden bei der Suche Abweichungen von bis zu 2 Zeichen gegenüber ``Fess`` toleriert.

Siehe auch
==========

- :doc:`search-wildcard`
- :doc:`special-char`

