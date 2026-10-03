=======================
Dictionnaire de mapping
=======================

Présentation
============

Vous pouvez mapper des caractères spécifiques (symboles, codes de caractères, pleine/demi-largeur) vers d'autres caractères.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration de mapping illustrée ci-dessous, sélectionnez [Système > Dictionnaire] dans le menu de gauche, puis cliquez sur mapping.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Méthode de configuration
------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration de mapping.

|image1|

Paramètres de configuration
---------------------------

Source de conversion
:::::::::::::::::::::

Entrez les caractères (symboles, codes de caractères, pleine/demi-largeur) à mapper.

Après conversion
::::::::::::::::

Développe les caractères entrés dans la source de conversion avec les caractères après conversion.

Téléchargement
==============

Vous pouvez télécharger au format de dictionnaire de mapping.

Téléversement
=============

Vous pouvez téléverser au format de dictionnaire de mapping.

Dictionnaires de mapping fournis
================================

Le ``mapping.txt`` par défaut sert à l'analyse des champs de recherche comme ``title`` et
``content``. Il ramène les hiragana, les petits kana et les katakana demi-chasse aux katakana pleine
chasse, de sorte que りんご, リンゴ et ﾘﾝｺﾞ se correspondent. Dans |Fess| 15.9, il unifie aussi les
graphies suivantes :

- ゐ et ゑ (en イ et エ), les petits kana comme ゎ, ゕ, ゖ, ヮ, ヵ, ヶ et ㇰ-ㇿ, ainsi que ゝ et ゞ (en ヽ et ヾ)
- ヴ, ヴャ, ヴュ et ヴョ, le hiragana ゔ, ｳﾞ demi-chasse, et ウ ou う suivi d'une marque de voisement
  combinante (U+3099) ; par exemple, ラヴ devient ラブ et レヴュー devient レビユー

De plus, ‐ ‑ ‒ – — ― ⁻ ₋ − et － écrits juste après un kana sont traités comme la marque de voyelle
longue ー (``prolonged_sound_mark_filter``) : サ―バ－ et サ−バ‐ correspondent donc à サーバー. Le
trait d'union ASCII (``-``) et un tiret après un kanji, une lettre ou un chiffre (東京－大阪,
2026−10−02) ne sont pas modifiés.

``ja/mapping.txt`` pour le japonais (les champs ``*_ja``) conserve les hiragana et les petits kana
tels quels, car l'analyseur morphologique en a besoin, et n'unifie que des graphies comme ヴ.

.. note::

   Ces réglages s'appliquent à un index de documents nouvellement créé. Un index existant conserve
   ses réglages d'analyse et ses dictionnaires jusqu'à sa réindexation. Pour les appliquer à un
   index existant, réindexez avec « Réinitialiser les dictionnaires » activé sur la page
   :doc:`maintenance-guide`. La réinitialisation écrase les modifications de ``mapping.txt`` /
   ``ja/mapping.txt`` faites dans l'écran d'administration.

.. |image0| image:: ../../../resources/images/en/15.9/admin/mapping-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/mapping-2.png

