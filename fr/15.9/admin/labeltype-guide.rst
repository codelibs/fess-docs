=========
Étiquette
=========

Présentation
============


Cette section explique la configuration des étiquettes.
Les étiquettes permettent de classifier les documents affichés dans les résultats de recherche.
La configuration des étiquettes spécifie les chemins auxquels ajouter des étiquettes par expression régulière.
Si des étiquettes sont enregistrées, une liste déroulante d'étiquettes s'affiche dans les options de recherche.

Cette configuration d'étiquette est appliquée aux configurations de crawl Web ou de système de fichiers.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration des étiquettes illustrée ci-dessous, cliquez sur [Robot d'exploration > Étiquette] dans le menu de gauche.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Création de configuration
-------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration des étiquettes.

|image1|

Paramètres de configuration
---------------------------

Nom
::::

Spécifie le nom affiché dans la liste déroulante de sélection d'étiquette lors de la recherche.

Valeur
::::::

Spécifie l'identifiant lors de la classification des documents.
Spécifiez en caractères alphanumériques.

Chemins cibles
::::::::::::::

Configure les chemins auxquels ajouter l'étiquette par expression régulière.
Vous pouvez en spécifier plusieurs en écrivant sur plusieurs lignes.
L'étiquette sera définie pour les documents correspondant aux chemins spécifiés ici.

Chemins exclus
::::::::::::::

Configure par expression régulière ce que vous souhaitez exclure des chemins cibles de crawl.
Vous pouvez en spécifier plusieurs en écrivant sur plusieurs lignes.

Permission
::::::::::

Spécifie la permission pour cette configuration.
Pour la méthode de spécification de permission, par exemple, pour afficher les résultats de recherche aux utilisateurs appartenant au groupe developer, spécifiez {group}developer.
La spécification par utilisateur est {user}nom_utilisateur, par rôle {role}nom_rôle, par groupe {group}nom_groupe.

Hôte virtuel
::::::::::::

Spécifie le nom d'hôte de l'hôte virtuel.
Pour plus de détails, consultez :doc:`Configuration de l'hôte virtuel dans le guide de configuration <../config/security-virtual-host>`.

Sur un écran de recherche consulté via un hôte virtuel, seules les étiquettes dont ce champ indique le nom de cet hôte virtuel sont affichées.
Les étiquettes dont ce champ est vide ne sont pas affichées lors d'un accès via un hôte virtuel.
Lors d'un accès qui ne correspond à aucun hôte virtuel, toutes les étiquettes sont affichées, quel que soit ce champ.

Une étiquette n'accepte qu'un seul hôte virtuel.
Pour afficher la même étiquette sur plusieurs hôtes virtuels, créez pour chaque hôte virtuel une étiquette ayant le même nom et la même valeur, et indiquez dans le champ d'hôte virtuel de chacune le nom de cet hôte virtuel.
La valeur étant identique, chacune de ces étiquettes filtre les mêmes documents.

Ordre de tri
::::::::::::

Spécifie l'ordre d'affichage des étiquettes.

Type
::::

Indiquez « Étiquette » ou « Tag ». Une étiquette ordinaire est une « Étiquette ». Un « Tag » est un tag
que les utilisateurs ajoutent depuis l'écran de recherche (voir « Tags » ci-dessous). Une étiquette
existante sans type est traitée comme une « Étiquette ».


Suppression de configuration
----------------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher l'écran de confirmation.
Appuyer sur le bouton Supprimer supprimera la configuration.

Tags
----

Avec ``user.tag.enabled=true`` (par défaut : ``false``) dans ``fess_config.properties``, les
utilisateurs connectés peuvent taguer les résultats de recherche. Dans le thème fourni
``bootstrap``, les tags s'affichent sur les résultats, les utilisateurs peuvent ajouter des tags et
retirer les leurs, et une facette « Tags » restreint les résultats. Pour l'API, voir
:doc:`../api/api-tag`.

Un tag est enregistré comme une étiquette du type « Tag » : le nom est le nom du tag, la valeur est le
SHA-256 du nom, les chemins inclus sont les URL taguées (une par ligne, correspondance exacte) et les
permissions décident qui peut voir le tag. L'utilisateur qui ajoute un tag est ajouté à ses
permissions.

- Un tag n'est visible que si les permissions de son étiquette correspondent à l'appelant. Les
  administrateurs peuvent modifier un tag sur cette page pour le partager avec un rôle ou un groupe,
  ou le supprimer.
- Les tags de même nom sont fusionnés en une seule étiquette ; les utilisateurs qui ont ajouté un tag
  de même nom voient donc où se trouvent les tags des autres.
- Les tags ne figurent ni dans l'API de liste des étiquettes (``/api/v2/labels``) ni dans les choix
  d'étiquettes de l'écran de recherche.
- Les tags comptent dans la limite des étiquettes (``page.labeltype.max.fetch.size``, par défaut :
  1000). Une fois la limite atteinte, aucun nouveau tag ne peut être créé.
- Après qu'un administrateur a modifié ou supprimé un tag sur cette page, les documents indexés
  conservent les anciennes valeurs jusqu'à un nouveau crawl ou l'exécution du job « Label Updater ».
- Un document peut avoir jusqu'à ``user.tag.max.document.tags`` (par défaut : 100) tags, et un nom
  de tag peut compter jusqu'à ``user.tag.name.max.length`` (par défaut : 50) caractères.

.. |image0| image:: ../../../resources/images/en/15.9/admin/labeltype-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/labeltype-2.png
