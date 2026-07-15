===========================
Recherche par étiquette
===========================

Recherche par étiquette (recherche par catégorie)
===================================================

En ajoutant aux documents ciblés par la recherche des informations d'étiquette permettant de les catégoriser, il devient possible d'effectuer une recherche filtrée en spécifiant une étiquette. L'utilisation des étiquettes permet par exemple de limiter le périmètre de recherche par service, par site ou par type de document.

En enregistrant au préalable les étiquettes dans l'écran d'administration, le filtrage par étiquette devient disponible sur l'écran de recherche. Les étiquettes disponibles peuvent être sélectionnées de manière multiple dans un menu déroulant lors de la recherche ; si plusieurs étiquettes sont sélectionnées, les documents auxquels au moins l'une de ces étiquettes est associée sont inclus dans la recherche. Si aucune étiquette n'est enregistrée, le menu déroulant des étiquettes ne s'affiche pas.

.. note::
    Comme des permissions peuvent être définies pour chaque étiquette, seules les étiquettes auxquelles l'utilisateur effectuant la recherche a accès s'affichent dans le menu déroulant. Par ailleurs, les étiquettes affichées peuvent également varier selon l'hôte virtuel ou la locale (langue). Ainsi, même si une étiquette est enregistrée, elle peut ne pas apparaître dans le menu déroulant selon l'utilisateur.

Une étiquette se définit en spécifiant, au moyen d'une expression régulière portant sur le chemin de l'URL, les documents auxquels elle doit être appliquée. Pour la procédure d'enregistrement des étiquettes et les éléments de configuration, consultez le :doc:`guide de gestion des étiquettes <../admin/labeltype-guide>`.

Utilisation
-----------

Il est possible de sélectionner une étiquette lors de la recherche. Les informations d'étiquette peuvent être sélectionnées dans les options de recherche affichées en cliquant sur le bouton « Options ».

|image0|

En créant un index avec des étiquettes configurées, il est possible d'effectuer une recherche pour chaque document auquel une étiquette a été attribuée. Une recherche sans spécifier d'étiquette correspond à une recherche complète classique, comme d'habitude.

L'attribution des étiquettes aux documents s'effectue, lors du crawl et de la création de l'index, en comparant l'URL du document avec le chemin défini pour l'étiquette. Par conséquent, si vous ajoutez ou modifiez la définition d'une étiquette (chemins cibles ou chemins exclus), ce changement ne sera pas automatiquement répercuté sur les documents déjà indexés. Pour appliquer les modifications, recrawlez les documents concernés ou exécutez la tâche « Label Updater » enregistrée dans le planificateur afin de mettre à jour l'index.

.. |image0| image:: ../../../resources/images/en/15.8/user/search-label-1.png
.. pdf   :width: 300 px
