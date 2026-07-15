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


Vous pouvez également ajouter vos propres champs personnalisés comme cibles de tri. Pour cela, indiquez dans ``query.additional.sort.fields`` du fichier ``fess_config.properties`` les noms des champs que vous souhaitez utiliser comme cibles de tri, séparés par des virgules (la valeur par défaut est vide). Les champs indiqués ici sont ajoutés aux champs standards ci-dessus et deviennent disponibles pour le tri. Notez que le champ à trier doit être préalablement enregistré (indexé) dans l'index.

Utilisation
-----------

Vous pouvez sélectionner les critères de tri lors de la recherche. Les critères de tri peuvent être sélectionnés dans la boîte de dialogue des options de recherche affichée en cliquant sur le bouton Options.

|image0|

De plus, pour trier dans le champ de recherche, saisissez « sort:nom_champ » dans le formulaire de recherche en séparant sort et le nom du champ par deux-points (:).

Voici un exemple de recherche de fess avec un tri croissant par taille de document.

::

    fess sort:content_length

Pour trier par ordre décroissant, ajoutez ``.desc`` après le nom du champ.

::

    fess sort:content_length.desc

Le suffixe pouvant être ajouté après le nom du champ est ``.asc`` (ordre croissant) ou ``.desc`` (ordre décroissant) ; si vous l'omettez, l'ordre croissant est utilisé.

Pour trier sur plusieurs champs, spécifiez-les séparés par des virgules (,) comme suit. Le champ indiqué en premier est prioritaire, et les documents ayant la même valeur pour ce champ sont ensuite triés selon le champ suivant.

::

    fess sort:content_length.desc,last_modified

.. note::
   Si vous indiquez un nom de champ absent de la liste des champs de tri disponibles, ou un ordre de tri autre que ``asc`` ou ``desc``, la recherche se soldera par une erreur.

.. |image0| image:: ../../../resources/images/en/15.8/user/search-sort-1.png
.. pdf            :width: 300 px
