====================
Recherche avec tri
====================

Il est possible de trier les résultats de recherche en spécifiant un champ tel que la date de recherche.

Champs de tri
-------------

Par défaut, vous pouvez trier en spécifiant les champs suivants.

.. list-table::
   :header-rows: 1

   * - Nom du champ
     - Description
   * - created
     - Date d'exploration
   * - content_length
     - Taille du document exploré
   * - last_modified
     - Date de dernière modification du document exploré
   * - filename
     - Nom du fichier
   * - score
     - Score de pertinence
   * - timestamp
     - Date d'indexation du document
   * - click_count
     - Nombre de clics sur le document
   * - favorite_count
     - Nombre de fois où le document a été ajouté aux favoris

Table : Liste des champs de tri


Vous pouvez également ajouter vos propres champs personnalisés comme cibles de tri.

Utilisation
-----------

Vous pouvez sélectionner les critères de tri lors de la recherche. Les critères de tri peuvent être sélectionnés dans la boîte de dialogue des options de recherche affichée en cliquant sur le bouton Options.

|image0|

De plus, pour trier dans le champ de recherche, saisissez « sort:nom_champ » dans le formulaire de recherche en séparant sort et le nom du champ par deux-points (:).

Voici un exemple de recherche de fess avec un tri croissant par taille de document.

::

    fess sort:content_length

Pour trier par ordre décroissant, procédez comme suit.

::

    fess sort:content_length.desc

Pour trier sur plusieurs champs, spécifiez-les séparés par des virgules comme suit.

::

    fess sort:content_length.desc,last_modified

.. |image0| image:: ../../../resources/images/en/15.3/user/search-sort-1.png
.. pdf            :width: 300 px
