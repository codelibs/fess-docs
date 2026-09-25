==========================
Dictionnaire de mots vides
==========================

Présentation
============

Les mots vides sont des mots que l'analyseur supprime lors de l'indexation des documents et lors des
recherches. Le dictionnaire de mots vides permet de gérer les mots à supprimer.

.. note::

   Les dictionnaires de mots vides sont des fichiers par langue (``en/stopwords.txt``,
   ``ja/stopwords.txt``, etc.), et chacun n'est utilisé que par l'analyseur de sa langue.
   ``en/stopwords.txt`` sert à analyser les champs ``content`` et ``title`` ainsi que les champs
   ``_en`` comme ``content_en``, tandis que ``content_ja`` et ``title_ja`` des documents détectés
   comme japonais sont analysés avec ``ja/stopwords.txt``. Les champs propres à une langue comme
   ``content_ja`` sont ajoutés à la requête selon la langue de la requête ; un mot ajouté uniquement à
   ``en/stopwords.txt`` peut donc encore correspondre par l'intermédiaire d'un champ propre à une
   langue. Pour qu'un mot ne corresponde plus, ajoutez-le aussi au dictionnaire de mots vides de la
   langue des documents.

   Les mots vides sont comparés à chaque jeton produit par l'analyseur. Un mot que l'analyseur découpe
   en plusieurs jetons, comme un mot mêlant lettres et chiffres, n'est pas supprimé s'il est ajouté tel
   quel. Vous pouvez vérifier le découpage d'un mot avec l'API ``_analyze`` d'OpenSearch.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration des mots vides illustrée ci-dessous, sélectionnez [Système > Dictionnaire] dans le menu de gauche, puis cliquez sur stopwords.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Méthode de configuration
------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration des mots vides.

|image1|

Paramètres de configuration
---------------------------

Informations sur le mot
:::::::::::::::::::::::

Entrez le mot à supprimer en tant que mot vide.

Téléchargement
==============

Vous pouvez télécharger le dictionnaire de mots vides sous forme de fichier texte contenant un mot par ligne.

Téléversement
=============

Vous pouvez téléverser un fichier texte contenant un mot par ligne. Les lignes commençant par ``#`` sont traitées comme des commentaires.


.. |image0| image:: ../../../resources/images/en/15.9/admin/stopwords-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/stopwords-2.png

