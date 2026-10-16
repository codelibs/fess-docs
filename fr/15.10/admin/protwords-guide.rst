======================
Dictionnaire Protwords
======================

Présentation
============

Vous pouvez gérer les mots à exclure du traitement de stemming.
Le traitement de stemming étant essentiellement basé sur des règles, une normalisation non intentionnelle peut se produire.
Par exemple, le mot Maine (nom d'un état américain) serait normalisé en main.

Pour que ce mot reste recherchable tel quel, enregistrez ``maine`` (écrivez les mots en minuscules ; voir « Paramètres de configuration »).

La liste affiche un dictionnaire par langue (``en/protwords.txt``, ``de/protwords.txt``, etc.). Choisissez et modifiez le dictionnaire qui correspond à la langue du mot. Voir :doc:`dict-guide` pour savoir quel dictionnaire s'applique à quels champs.
Enregistrer une modification ne suffit pas pour qu'elle soit prise en compte dans les recherches. Voir :ref:`dict-apply-changes` pour savoir comment l'appliquer.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration Protwords illustrée ci-dessous, sélectionnez [Système > Dictionnaire] dans le menu de gauche, puis cliquez sur protwords.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Méthode de configuration
------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration Protwords.

|image1|

Paramètres de configuration
---------------------------

Informations sur les mots
::::::::::::::::::::::::::

Entrez les mots à exclure du traitement de stemming.

Entrez les mots en minuscules. L'analyse convertit le mot en minuscules avant de le comparer à ce dictionnaire ; saisir ``Maine`` ne le protège donc pas. Dans l'exemple de la présentation, saisissez ``maine``.


Téléchargement
==============

Vous pouvez télécharger au format de dictionnaire Protwords.

Téléversement
=============

Vous pouvez téléverser au format de dictionnaire Protwords.

.. warning::

   Le téléversement remplace le contenu du dictionnaire par celui du fichier téléversé. Les mots qui ne figurent pas dans le fichier, y compris ceux enregistrés depuis l'écran, sont supprimés. Si nécessaire, téléchargez d'abord le dictionnaire et incluez son contenu dans le fichier à téléverser.


.. |image0| image:: ../../../resources/images/en/15.10/admin/protwords-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/protwords-2.png
