=====================
Dictionnaire Kuromoji
=====================

Présentation
============

Vous pouvez enregistrer des noms de personnes, des noms propres, des termes spécialisés, etc. pour l'analyse morphologique.

Ce dictionnaire concerne le japonais (``ja/kuromoji.txt``) et n'est utilisé que pour l'analyse des champs ``_ja`` tels que ``content_ja``.
Enregistrer une modification ne suffit pas pour qu'elle soit prise en compte dans les recherches. Voir :ref:`dict-apply-changes` pour savoir comment l'appliquer. Ce dictionnaire agissant au moment de l'indexation, les documents déjà présents dans l'index ne sont pas concernés tant qu'ils ne sont pas crawlés à nouveau.

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

.. warning::

   Le téléversement remplace le contenu du dictionnaire par celui du fichier téléversé. Les mots qui ne figurent pas dans le fichier, y compris ceux enregistrés depuis l'écran, sont supprimés. Si nécessaire, téléchargez d'abord le dictionnaire et incluez son contenu dans le fichier à téléverser.

.. note::

   Le dictionnaire fourni contient déjà les deux exemples ci-dessus (« 朝青龍 » et « 関西国際空港 »).
   Dans l'analyse de ``content_ja``, les caractères sont remplacés par le dictionnaire de remplacement de caractères ``ja/mapping.txt`` avant l'analyse morphologique (voir :doc:`mapping-guide`). Le fichier ``ja/mapping.txt`` fourni contient ``龍 => 竜`` ; « 朝青龍 » est donc remplacé par ``朝青竜`` avant l'analyse ; il ne correspond pas à « 朝青龍 » du dictionnaire et est découpé en ``朝 青 竜``.
   Pour vérifier l'effet d'un enregistrement, utilisez un mot absent du dictionnaire et ne contenant aucun caractère remplacé par ``ja/mapping.txt``.


.. |image0| image:: ../../../resources/images/en/15.9/admin/kuromoji-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/kuromoji-2.png
