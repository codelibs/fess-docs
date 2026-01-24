=======================
Dictionnaire de synonymes
=========================

Présentation
============

Vous pouvez gérer les synonymes de mots ayant la même signification (comme GB, gigabyte, etc.).

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration des synonymes illustrée ci-dessous, sélectionnez [Système > Dictionnaire] dans le menu de gauche, puis cliquez sur synonym.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Méthode de configuration
------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration des synonymes.

|image1|

Paramètres de configuration
---------------------------

Concernant la création d'index, comme la configuration standard est bi-gram, il est nécessaire de s'assurer que le mot après conversion ne soit pas un caractère unique.
De plus, lors de l'enregistrement de synonymes, il est nécessaire de s'enregistrer comme suit :

* Enregistrer les hiragana en katakana
* Enregistrer les petits katakana en grands katakana
* Enregistrer les caractères alphanumériques pleine largeur en demi-largeur
* Ne pas enregistrer les synonymes en double

Source de conversion
:::::::::::::::::::::

Entrez le mot à traiter comme synonyme.

Après conversion
::::::::::::::::

Développe le mot entré dans la source de conversion avec le mot après conversion.
Par exemple, si vous souhaitez traiter « TV » comme « TV » et « テレビ », entrez « TV » dans la source de conversion et entrez « TV » et « テレビ » dans l'après conversion.

Téléchargement
==============

Vous pouvez télécharger au format de dictionnaire de synonymes fourni par Apache Lucene.

Téléversement
=============

Vous pouvez téléverser au format de dictionnaire de synonymes fourni par Apache Lucene.
Comme les synonymes sont un remplacement d'un groupe de mots par un autre groupe de mots, la description du dictionnaire utilise la virgule (,) et la conversion (=>).
Par exemple, pour remplacer « TV » par « テレビ », utilisez => et décrivez comme suit.

::

    TV=>テレビ

Pour traiter « fess » et « フェス » de manière similaire, décrivez comme suit.

::

    fess,フエス=>fess,フエス

Dans le cas ci-dessus, vous pouvez également omettre => et décrire comme suit.

::

    fess,フエス


.. |image0| image:: ../../../resources/images/en/15.5/admin/synonym-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/synonym-2.png
