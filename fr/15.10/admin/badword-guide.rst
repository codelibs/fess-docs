===========
Mots exclus
===========

Présentation
============

Cette section explique la configuration des mots exclus des suggestions.
Les suggestions sont affichées en fonction des termes de recherche, mais vous pouvez configurer ces mots pour qu'ils ne soient pas affichés dans les suggestions.


Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration des mots exclus des suggestions illustrée ci-dessous, cliquez sur [Suggérer > Mot incorrect] dans le menu de gauche.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Création de configuration
-------------------------

Pour ouvrir la page de création de mots exclus des suggestions, cliquez sur le bouton Nouvelle création.

|image1|

Paramètres de configuration
---------------------------

Candidat de suggestion
::::::::::::::::::::::

Enregistre les mots NG.
Les mots enregistrés ici ne seront plus affichés dans les suggestions.

.. note::
   Un mot exclu enregistré n'est pas appliqué immédiatement aux suggestions. Il est retiré des candidats de suggestion existants lorsque la tâche « Suggest Indexer », qui reconstruit l'index de suggestions, s'exécute (par défaut tous les jours à 12:00). Pour l'appliquer tout de suite, cliquez sur « Suggest Indexer » dans [Système > Planificateur], puis sur le bouton « Démarrer maintenant ». Il en va de même pour les mots enregistrés par téléversement d'un fichier CSV.

Suppression de configuration
----------------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher l'écran de confirmation.
Appuyer sur le bouton Supprimer supprimera la configuration.

Téléchargement
==============

Télécharge les mots enregistrés au format CSV.

|image2|

Contenu du CSV
--------------

La première ligne est l'en-tête.
Les mots exclus sont listés à partir de la deuxième ligne.

::

"BadWord"
"検索エンジン"

Téléversement
=============

Enregistre les mots au format CSV.

|image3|

Contenu du CSV
--------------

La première ligne est l'en-tête.
Décrivez les mots exclus à partir de la deuxième ligne.

::

"BadWord"
"検索エンジン"

.. |image0| image:: ../../../resources/images/en/15.10/admin/badword-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/badword-2.png
.. |image2| image:: ../../../resources/images/en/15.10/admin/badword-3.png
.. |image3| image:: ../../../resources/images/en/15.10/admin/badword-4.png
