====================
Dictionnaire Kuromoji
=====================

Présentation
============

Vous pouvez enregistrer des noms de personnes, des noms propres, des termes spécialisés, etc. pour l'analyse morphologique.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration Kuromoji illustrée ci-dessous, sélectionnez [Système > Dictionnaire] dans le menu de gauche, puis cliquez sur kuromoji.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Méthode de configuration
------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration Kuromoji.

|image1|

Paramètres de configuration
---------------------------

Jeton
:::::

Entrez le mot à traiter lors de l'analyse morphologique.

Division
::::::::

Si le mot est composé d'un mot composé, vous pouvez le faire correspondre même lorsqu'il est recherché avec des mots divisés.
Par exemple, en entrant « 全文 検索 エンジン » pour « 全文検索エンジン », vous pouvez également effectuer une recherche avec des mots divisés.

Lecture
:::::::

Entrez la lecture du mot entré comme jeton en katakana.
Si une division est effectuée, entrez-la de manière divisée.
Par exemple, entrez « ゼンブン ケンサク エンジン ».

Partie du discours
::::::::::::::::::

Entrez la partie du discours du mot entré.

Téléchargement
==============

Vous pouvez télécharger au format de dictionnaire Kuromoji.

Téléversement
=============

Vous pouvez téléverser au format de dictionnaire Kuromoji.
Le format de dictionnaire Kuromoji est séparé par des virgules (,) et suit le format « jeton,jeton divisé,lecture du jeton divisé,partie du discours ».
Les jetons divisés sont séparés par des espaces.
Si aucune division n'est nécessaire, le jeton et le jeton divisé sont égaux.
Par exemple, cela ressemble à ce qui suit.

::

    朝青龍,朝青龍,アサショウリュウ,カスタム名詞
    関西国際空港,関西 国際 空港,カンサイ コクサイ クウコウ,カスタム名詞


.. |image0| image:: ../../../resources/images/en/15.5/admin/kuromoji-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/kuromoji-2.png
