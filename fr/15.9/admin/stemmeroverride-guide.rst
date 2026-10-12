====================================
Dictionnaire de remplacement Stemmer
====================================

Présentation
============

Vous pouvez remplacer la racine (stem) de mots précis par une racine que vous indiquez. Utilisez-le pour les mots dont le résultat du stemming n'est pas celui voulu.
Par exemple, en définissant ``mous`` comme racine de ``mice``, ``mice`` et ``mouse`` sont recherchés comme un même mot (le stemmer anglais transforme ``mouse`` en ``mous``).

Remplacer des caractères tels que des symboles, des codes de caractères ou des caractères pleine/demi-largeur par d'autres caractères n'est pas le rôle de ce dictionnaire. Utilisez pour cela le dictionnaire de remplacement de caractères (:doc:`mapping-guide`).

La liste affiche un dictionnaire par langue (``en/stemmer_override.txt``, etc.). Choisissez et modifiez le dictionnaire qui correspond à la langue du mot. Voir :doc:`dict-guide` pour savoir quel dictionnaire s'applique à quels champs.
Enregistrer une modification ne suffit pas pour qu'elle soit prise en compte dans les recherches. Voir :ref:`dict-apply-changes` pour savoir comment l'appliquer.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration de remplacement Stemmer illustrée ci-dessous, sélectionnez [Système > Dictionnaire] dans le menu de gauche, puis cliquez sur stemmeroverride.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Méthode de configuration
------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration de remplacement Stemmer.

|image1|

Paramètres de configuration
---------------------------

Source de conversion
:::::::::::::::::::::

Entrez le mot dont vous voulez remplacer la racine. L'analyse convertit le mot en minuscules avant de le comparer à ce dictionnaire ; saisissez-le donc en minuscules.

Après conversion
::::::::::::::::

Entrez le mot à utiliser comme racine du mot saisi dans la source de conversion.
Le mot cible est indexé tel quel, sans stemming. Les termes de recherche passant par le stemming, pour obtenir les mêmes résultats que le mot d'origine, saisissez le résultat du passage du mot ordinaire dans le stemmer (``mous`` pour ``mouse``).
Par exemple, saisissez ``mice`` comme source et ``mous`` comme cible.

Téléchargement
==============

Vous pouvez télécharger au format de dictionnaire de remplacement Stemmer.

Téléversement
=============

Vous pouvez téléverser au format de dictionnaire de remplacement Stemmer.

.. warning::

   Le téléversement remplace le contenu du dictionnaire par celui du fichier téléversé. Tout ce qui ne figure pas dans le fichier, y compris les entrées enregistrées depuis l'écran, est supprimé. Si nécessaire, téléchargez d'abord le dictionnaire et incluez son contenu dans le fichier à téléverser.


.. |image0| image:: ../../../resources/images/en/15.9/admin/stemmeroverride-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/stemmeroverride-2.png

