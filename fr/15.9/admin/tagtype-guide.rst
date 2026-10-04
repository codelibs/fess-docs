===
Tag
===

Présentation
============

Cette section explique l'écran qui gère les tags des utilisateurs.

Un tag est une marque qu'un utilisateur connecté pose sur des documents des résultats de recherche.
Les tags sont gérés par utilisateur : l'utilisateur qui crée un tag en est le propriétaire, et deux
utilisateurs peuvent employer le même nom et avoir malgré tout deux tags distincts. Les tags ne sont
pas des :doc:`étiquettes <labeltype-guide>`, que les administrateurs définissent par des motifs
d'URL ; les utilisateurs créent eux-mêmes leurs tags et les posent sur des documents précis.

Les tags sont désactivés par défaut. Pour les utiliser, définissez ``user.tag.enabled=true`` dans
``fess_config.properties``. Une fois activés, le thème ``bootstrap`` fourni permet aux utilisateurs
connectés de poser des tags sur les résultats de recherche et de les retirer, et de filtrer avec une
facette de tags. « Mes tags » leur permet de renommer, partager et supprimer leurs propres tags. Les
tags partagés des autres utilisateurs s'affichent avec le préfixe « Partagé : ». Pour l'API
utilisateur et les paramètres, voir :doc:`../api/api-tag`.

Dans cet écran, les administrateurs listent, créent, modifient et suppriment les tags de tous les
utilisateurs.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste des tags, cliquez sur [Robot d'exploration > Tag] dans le menu de gauche.
L'affichage requiert le rôle ``admin-tagtype`` ou ``admin-tagtype-view`` ; la création, la
modification et la suppression requièrent ``admin-tagtype``.

La liste affiche le nom et le propriétaire de chaque tag, par ordre de tri, nom et propriétaire. Vous
pouvez rechercher par nom et par propriétaire ; chacun correspond aux tags qui contiennent le texte
saisi.

Cliquez sur un nom pour modifier le tag.

Création de configuration
-------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de création d'un tag.

Paramètres de configuration
---------------------------

Nom
:::

Spécifie le nom du tag. Le nom est normalisé en NFKC, les suites d'espaces sont réduites à une seule
et les extrémités sont rognées. Le résultat doit compter de 1 à ``user.tag.name.max.length`` (par
défaut : 50) caractères et ne peut contenir ni caractère de contrôle ni caractère de format.

Propriétaire
::::::::::::

Spécifie l'identifiant de connexion de l'utilisateur à qui appartient le tag. Le propriétaire et le
nom identifient ensemble un tag : un propriétaire ne peut donc pas avoir deux tags de même nom, même
sur des hôtes virtuels différents.

Lorsque vous changez le propriétaire, la permission utilisateur de l'ancien propriétaire dans
Autorisations est remplacée par celle du nouveau propriétaire.

Chemins
:::::::

Spécifie les URL des documents sur lesquels poser le tag, une par ligne. Une URL doit être égale au
champ ``url`` d'un document indexé ; les expressions régulières ne sont pas utilisées. Un tag peut
avoir au plus ``user.tag.max.paths`` (par défaut : 10000) URL.

Autorisations
:::::::::::::

Spécifie les utilisateurs, groupes et rôles qui peuvent voir le tag, comme pour les étiquettes :
{user}nom d'utilisateur pour un utilisateur, {group}nom de groupe pour un groupe et {role}nom de rôle
pour un rôle. Laissé vide, seul le propriétaire peut voir le tag.

Le propriétaire voit toujours ses propres tags, quelles que soient les autorisations. Un utilisateur
non connecté ne voit jamais de tag, quelles que soient les autorisations.

Hôte virtuel
::::::::::::

Spécifie le nom d'hôte de l'hôte virtuel sur lequel le tag est affiché. Un tag créé par un
utilisateur reçoit l'hôte virtuel par lequel l'utilisateur accédait. Sur un écran de recherche
accédé par un hôte virtuel, seuls les tags portant ici ce nom d'hôte virtuel sont visibles. Un accès
qui ne correspond à aucun hôte virtuel voit les tags quelle que soit la valeur de ce champ. Pour plus
de détails, consultez :doc:`Hôte virtuel dans le guide de configuration <../config/security-virtual-host>`.

Ordre de tri
::::::::::::

Spécifie l'ordre d'affichage du tag.

Suppression de configuration
----------------------------

Cliquez sur un nom dans la page de liste, puis sur le bouton Supprimer pour afficher l'écran de
confirmation. Appuyer sur le bouton Supprimer supprime le tag, et sa valeur est retirée des documents.

Partage
=======

Quand un utilisateur partage un tag, les valeurs de ``role.search.guest.permissions`` (par défaut :
``{role}guest``) sont ajoutées à ses autorisations. La visibilité d'un tag est décidée en ajoutant ces
valeurs aux rôles de l'utilisateur connecté : un tag partagé est donc visible par tout utilisateur
connecté, qui peut aussi filtrer avec. Annuler le partage retire uniquement ces valeurs.

Dans cet écran, un administrateur peut aussi ajouter des groupes ou des rôles aux autorisations pour
ne montrer un tag qu'à certains utilisateurs. Seuls le propriétaire et les administrateurs peuvent
modifier un tag ; les autres utilisateurs peuvent seulement afficher les tags qu'ils voient et filtrer
avec.

Comment les modifications atteignent les documents
==================================================

Un document conserve ses tags dans le champ ``tag`` de l'index, sous la forme
``base64url(nom):base64url(propriétaire)``.

- La création, la modification et la suppression des tags, ainsi que leur pose et leur retrait par
  les utilisateurs, sont enregistrées immédiatement dans les tags (l'index ``fess_config.tag_type``).
  Les documents sont mis à jour via une file d'attente en mémoire que la tâche « Log Aggregator »
  (``log_aggregator``) applique en bloc chaque minute ; les résultats de recherche reflètent donc une
  modification au bout d'une minute environ au plus.
- Modifier les chemins dans cet écran met à jour les documents des URL ajoutées et retirées. Modifier
  le nom ou le propriétaire remplace l'ancienne valeur des documents par la nouvelle.
- Lorsque des documents sont indexés par un crawl ou un magasin de données, leur champ ``tag`` est
  défini à partir des chemins des tags ; les tags survivent donc à un nouveau crawl.
- La tâche « Tag Updater » (``tag_updater``) reconstruit le champ ``tag`` de tous les documents à
  partir des tags. Elle n'a pas de planification ; exécutez-la depuis le planificateur au besoin.

Remarques pour l'exploitation
=============================

- **Exécutez Log Aggregator sur chaque nœud.** Chaque JVM a sa propre file d'attente, que seul le
  Log Aggregator de ce nœud traite. Laissez la cible de la tâche ``log_aggregator`` à la valeur par
  défaut ``all`` ; si elle est limitée à certains nœuds, les modifications reçues par les autres
  nœuds n'atteignent jamais les documents.
- **Exécutez Tag Updater dans les cas suivants.** La file d'attente est en mémoire : les
  modifications pas encore appliquées sont perdues au redémarrage de |Fess|. Tant que
  ``user.tag.enabled=false``, les modifications de tags n'atteignent pas les documents et un nouveau
  crawl efface leur champ ``tag``. Après une restauration depuis une sauvegarde, les tags des
  documents doivent aussi être reconstruits. Enfin, lorsque la file dépasse
  ``user.tag.queue.max.size`` (par défaut : 10000), les modifications en trop sont abandonnées avec
  un journal WARN. Dans chacun de ces cas, exécuter ``tag_updater`` reconstruit les tags des
  documents.
- **Le propriétaire d'un tag est l'identifiant de connexion.** Si un identifiant change, les tags
  restent attachés à l'ancien. Avec SAML, le NameID doit être persistant. Avec Entra ID, le
  propriétaire est l'UPN, et avec LDAP, le nom d'utilisateur avec la casse saisie à la connexion.
  Supprimer un utilisateur laisse ses tags ; supprimez dans cet écran ceux qui ne servent plus.
- **Les index existants fonctionnent aussi.** Au démarrage, si l'index des documents n'a pas de
  mapping pour le champ ``tag``, il est ajouté en ``keyword``. Les champs existants ne sont pas
  modifiés.
- Les tags sont stockés dans l'index ``fess_config.tag_type``. Ils sont inclus dans
  ``fess_config.bulk`` d'une sauvegarde, mais pas dans ``fess_basic_config.bulk``.
