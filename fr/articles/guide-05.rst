==============================================
Filtrer les résultats par rôles et par groupes
==============================================

Introduction
============

Une fois que les documents internes peuvent tous être recherchés depuis un seul Fess, la question suivante est : « qui doit voir quoi ? ».
Il ne faut pas que les documents d'évaluation des ressources humaines apparaissent dans les résultats de recherche de tous les employés, et à l'inverse, il ne faut pas non plus que les règlements destinés à toute l'entreprise ne soient visibles que par quelques personnes.

Dans Fess, les valeurs saisies dans le champ « Autorisations » d'une configuration d'exploration sont enregistrées avec chaque document, puis comparées, à chaque recherche, aux droits de l'utilisateur connecté.
Dans cet article, nous configurons dans Fess 15.9 une visibilité par service, puis nous vérifions quels documents chaque utilisateur peut voir.

En suivant les étapes de cet article, vous saurez :

- Configurer trois niveaux de visibilité (service, direction, tous les employés) avec des groupes et des autorisations
- Utiliser directement les groupes d'Active Directory comme autorisations
- Aligner la visibilité des étiquettes sur celle des documents
- Vérifier quels documents chaque utilisateur voit, et quels droits sont enregistrés dans un document

La configuration du SSO est traitée dans :doc:`guide-15`, et l'utilisation par plusieurs organisations au moyen d'hôtes virtuels dans :doc:`guide-13`.

Fonctionnement des autorisations
================================

Écrire les autorisations
------------------------

Dans le champ « Autorisations » d'une configuration d'exploration, saisissez des valeurs aux formats suivants, une par ligne.
Si l'une d'entre elles correspond aux droits de l'utilisateur, le document s'affiche dans les résultats de recherche.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Format
     - Utilisateurs correspondants
   * - ``{user}nom_utilisateur``
     - Cet utilisateur lui-même
   * - ``{group}nom_groupe``
     - Les utilisateurs qui appartiennent à ce groupe
   * - ``{role}nom_rôle``
     - Les utilisateurs qui possèdent ce rôle
   * - ``(deny){group}nom_groupe``
     - Le document n'est pas affiché aux utilisateurs correspondants, même si une autre valeur l'autorise (utilisable aussi avec ``{user}`` et ``{role}``)

Droits d'un utilisateur
-----------------------

À chaque recherche, Fess détermine les droits de l'utilisateur comme suit.

- Utilisateur connecté : ``{user}`` avec son propre nom d'utilisateur, ``{group}`` pour chacun de ses groupes et ``{role}`` pour chacun de ses rôles
- Visiteur non connecté : ``{role}guest``

Le point important est que les utilisateurs connectés ne reçoivent pas ``{role}guest``.
Le champ « Autorisations » d'une nouvelle configuration d'exploration contient ``{role}guest`` dès le départ.
Si vous le laissez tel quel, les documents sont visibles par les visiteurs non connectés, mais pas par les utilisateurs connectés.
Pour les documents que tous les employés doivent voir, indiquez dans les autorisations un groupe (ou un rôle) auquel appartiennent tous les employés.

Notez également que l'utilisateur initial ``admin`` possède les rôles ``admin`` et ``guest``.
Si vous effectuez une recherche dans un navigateur encore connecté à la console d'administration, la recherche s'effectue en tant que ``admin`` : seuls les documents ``{role}guest`` s'affichent, et pas ceux des services.

Rôles ou groupes ?
------------------

Les rôles et les groupes sont comparés exactement de la même manière.
La différence tient à l'origine des valeurs.
Dans la gestion des utilisateurs de Fess, vous pouvez attribuer à chaque utilisateur à la fois des rôles et des groupes.
Avec l'intégration LDAP (Active Directory), les groupes auxquels appartient l'utilisateur (``memberOf``) deviennent ``{group}nom_groupe`` (seules les entrées dont le DN contient ``ou=Role`` deviennent ``{role}``).

Dans cet article, toutes les unités organisationnelles, comme les services ou l'ensemble des employés, sont représentées par des groupes, afin que les mêmes valeurs d'autorisation fonctionnent aussi bien pour les utilisateurs de Fess que pour Active Directory.

Ce que nous allons construire
=============================

Prenons l'exemple d'une entreprise dont le portail intranet ``https://intra.example.com/`` comporte des pages pour chaque service et des pages pour toute l'entreprise.

.. list-table:: Groupes et utilisateurs
   :header-rows: 1
   :widths: 20 40 40

   * - Utilisateur
     - Service
     - Groupes
   * - ``sato``
     - Ventes
     - ``Sales``, ``AllStaff``
   * - ``suzuki``
     - Développement
     - ``Engineering``, ``AllStaff``
   * - ``tanaka``
     - Ressources humaines
     - ``HR``, ``AllStaff``
   * - ``yamada``
     - Direction
     - ``Executives``, ``AllStaff``

.. list-table:: Autorisations des configurations d'exploration
   :header-rows: 1
   :widths: 25 40 35

   * - Configuration d'exploration
     - URL
     - Autorisations
   * - Ventes
     - ``https://intra.example.com/sales/``
     - ``{group}Sales`` et ``{group}Executives``
   * - Développement
     - ``https://intra.example.com/dev/``
     - ``{group}Engineering`` et ``{group}Executives``
   * - Ressources humaines
     - ``https://intra.example.com/hr/``
     - ``{group}HR`` et ``{group}Executives``
   * - Toute l'entreprise
     - ``https://intra.example.com/common/``
     - ``{group}AllStaff``

Avec cette configuration, chaque utilisateur voit les documents suivants.

.. list-table:: Documents visibles par chaque utilisateur
   :header-rows: 1
   :widths: 30 70

   * - Utilisateur
     - Documents dans les résultats de recherche
   * - ``sato``
     - Ventes, Toute l'entreprise
   * - ``suzuki``
     - Développement, Toute l'entreprise
   * - ``tanaka``
     - Ressources humaines, Toute l'entreprise
   * - ``yamada``
     - Ventes, Développement, Ressources humaines, Toute l'entreprise
   * - Visiteurs non connectés
     - Aucun
   * - ``admin`` (page de recherche)
     - Aucun

Si vous souhaitez que les visiteurs non connectés voient aussi les documents de toute l'entreprise, ajoutez également ``{role}guest`` à la configuration « Toute l'entreprise ».
Dans ce cas, ``admin`` voit aussi ces documents.

Les noms de groupe sont comparés en tenant compte de la casse.
``{group}sales`` et ``{group}Sales`` sont traités comme des groupes différents : écrivez le nom du groupe et la valeur d'autorisation avec exactement la même orthographe.

Configuration avec les utilisateurs de Fess
===========================================

Créer les groupes et les utilisateurs
-------------------------------------

1. Dans la console d'administration, sous [Utilisateur] > [Groupe], cliquez sur [Créer nouveau], saisissez ``Sales`` dans « Nom » et cliquez sur [Créer]. Créez de la même manière ``Engineering``, ``HR``, ``Executives`` et ``AllStaff``
2. Sous [Utilisateur] > [Utilisateur], cliquez sur [Créer nouveau] et saisissez « Nom d'utilisateur », « Mot de passe » et « Mot de passe (confirmer) ». Le mot de passe doit comporter au moins 8 caractères
3. Dans « Groupes », sélectionnez les groupes indiqués dans le tableau ci-dessus, puis cliquez sur [Créer]

Les utilisateurs, groupes et rôles sont enregistrés dans OpenSearch ; ils sont donc conservés même si vous recréez les conteneurs dans Docker.

Créer les configurations d'exploration
--------------------------------------

Pour chaque service, créez une configuration d'exploration sous [Robot d'exploration] > [Web].
Le tableau suivant montre l'exemple des Ventes.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Valeur
   * - Nom
     - ``Portail Ventes``
   * - URL
     - ``https://intra.example.com/sales/``
   * - URL incluses
     - ``https://intra.example.com/sales/.*``
   * - Autorisations
     - Supprimez la valeur initiale ``{role}guest`` et saisissez les deux lignes suivantes

::

    {group}Sales
    {group}Executives

Créez de la même manière Développement, Ressources humaines et Toute l'entreprise, en modifiant l'URL et les autorisations comme indiqué dans le tableau.
Une fois les configurations créées, cliquez sur [Démarrer maintenant] pour « Default Crawler » sous [Système] > [Planificateur] afin de lancer l'exploration.
Pour savoir comment vérifier que l'exploration est terminée, consultez :doc:`guide-02`.

.. note::

   Dans les configurations d'exploration de systèmes de fichiers (SMB ou fichiers locaux), les droits lus dans l'ACL du fichier sont enregistrés dans le document **en plus** des valeurs du champ « Autorisations ».
   Ce comportement est activé par défaut.
   Les documents d'un serveur de fichiers peuvent donc être visibles plus largement que la portée indiquée dans « Autorisations ».
   Pour la combinaison avec les ACL, consultez :doc:`file-server-search`.
   Les autorisations des configurations d'exploration de magasins de données sont traitées dans :doc:`datastore-basics`.

Utiliser les groupes d'Active Directory
=======================================

Si vos utilisateurs sont gérés dans Active Directory, configurez l'intégration LDAP au lieu de créer des utilisateurs et des groupes dans Fess.
Les groupes présents dans l'attribut ``memberOf`` de l'utilisateur connecté deviennent des droits ``{group}``.

Configurer la connexion LDAP
----------------------------

Remplissez la section « LDAP » de [Système] > [Général], puis cliquez sur [Mettre à jour].

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Exemple
   * - URL LDAP
     - ``ldap://ad.example.com:389``
   * - DN de base
     - ``dc=example,dc=com``
   * - DN de liaison
     - ``cn=fess,cn=Users,dc=example,dc=com`` (compte de service pour les recherches)
   * - Mot de passe
     - Mot de passe du compte de service
   * - DN de l'utilisateur
     - ``%s@example.com`` (``%s`` est remplacé par le nom de connexion)
   * - Filtre de compte
     - ``sAMAccountName=%s``
   * - Attribut memberOf
     - ``memberOf``

Pour le détail de chaque champ et la manière d'écrire un « Filtre de groupe » qui résout les groupes imbriqués, consultez le `Guide d'intégration LDAP <https://fess.codelibs.org/fr/stable/config/ldap-integration.html>`__.

.. warning::

   Les paramètres de [Général] sont enregistrés dans ``system.properties``.
   Dans la configuration docker-fess, ce fichier se trouve dans le conteneur ``fess01`` ; il est donc perdu lorsque vous recréez le conteneur avec ``down`` → ``up`` (voir la section sur l'arrêt et le redémarrage dans :doc:`guide-02`).

Correspondance entre noms de groupe et autorisations
----------------------------------------------------

La valeur du ``CN`` le plus à l'extrémité du DN du groupe devient le nom du groupe.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Valeur de memberOf
     - Droit de l'utilisateur
   * - ``CN=Sales,OU=Groups,DC=example,DC=com``
     - ``{group}Sales``
   * - ``CN=AllStaff,OU=Groups,DC=example,DC=com``
     - ``{group}AllStaff``

Si vous nommez les groupes d'Active Directory ``Sales``, ``Engineering``, ``HR``, ``Executives`` et ``AllStaff``, les configurations d'exploration du chapitre précédent fonctionnent telles quelles.
Si les noms diffèrent, adaptez les valeurs d'autorisation aux noms des groupes d'Active Directory.

Pour l'ensemble des employés, prévoyez un groupe dont tout le monde est membre direct.
Le groupe principal d'Active Directory (généralement ``Domain Users``) ne figure pas dans l'attribut ``memberOf`` ; écrire ``{group}Domain Users`` ne correspond donc à rien.

Pour vérifier quels droits un utilisateur a reçus, passez le niveau de journalisation de ``org.codelibs.fess.ldap`` à DEBUG.
Lorsque les droits sont obtenus depuis LDAP, une ligne commençant par ``Roles:`` est écrite dans ``fess.log``.
Pour la configuration, consultez la section « Configuration du débogage » du Guide d'intégration LDAP.
Les valeurs de cette ligne apparaissent dans le format interne décrit plus loin (par exemple ``2Sales``).

Pour permettre la connexion par SSO (Entra ID, OpenID Connect, SAML, SPNEGO), il faut le plugin ``fess-sso-*`` correspondant à chaque méthode.
La façon dont les groupes et les rôles sont transmis diffère aussi selon la méthode ; consultez :doc:`guide-15`.

Aligner la visibilité des étiquettes
====================================

Les étiquettes ont elles aussi des « Autorisations », qui déterminent si l'étiquette apparaît parmi les choix d'étiquettes de la page de recherche.
Elles n'ont aucune incidence sur l'affichage des documents, mais comme les nouvelles étiquettes contiennent elles aussi ``{role}guest`` dès le départ, elles n'apparaissent pas, en l'état, dans les choix des utilisateurs connectés.

Voici l'exemple d'une étiquette à attribuer aux documents des ressources humaines.
Sous [Robot d'exploration] > [Étiquette], cliquez sur [Créer nouveau] et saisissez ce qui suit.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Valeur
   * - Nom
     - ``Ressources humaines``
   * - Valeur
     - ``hr`` (caractères alphanumériques et traits de soulignement uniquement)
   * - Chemins inclus
     - ``https://intra.example.com/hr/.*``
   * - Autorisations
     - ``{group}HR`` et ``{group}Executives`` (même portée que les documents)

Les autorisations d'une étiquette s'appliquent aux choix dès son enregistrement.
En revanche, les « Chemins inclus », qui attribuent l'étiquette aux documents, sont appliqués lors de l'exploration : lancez donc une exploration après avoir créé l'étiquette.

Réexplorer après une modification des droits
============================================

Les autorisations sont enregistrées dans les documents lors de l'exploration.
Modifier les « Autorisations » d'une configuration d'exploration ne change pas les droits des documents déjà présents dans l'index.
Après la modification, exécutez une tâche qui inclut cette configuration d'exploration (par exemple « Default Crawler »).

Pour les configurations d'exploration Web et de systèmes de fichiers, les documents dont les droits ont changé sont récupérés à nouveau lors de l'exploration suivante, et l'ancien document ayant la même URL est remplacé.
Tant que la réexploration n'est pas terminée, les documents continuent d'apparaître dans les résultats avec leurs anciens droits.
Lorsque vous restreignez la visibilité, lancez l'exploration immédiatement.

Pour réexplorer immédiatement une seule configuration d'exploration, cliquez sur [Créer une nouvelle tâche] dans la page de détails de cette configuration, puis exécutez la tâche créée avec [Démarrer maintenant].

Vérifier le fonctionnement
==========================

Rechercher en tant que chaque utilisateur
-----------------------------------------

1. Ouvrez ``http://localhost:8080/`` dans une fenêtre de navigation privée. Dans une fenêtre connectée à la console d'administration, la recherche s'effectue en tant que ``admin``
2. Effectuez une recherche sans vous connecter et vérifiez que ni les documents des services ni ceux de toute l'entreprise ne s'affichent
3. Connectez-vous en tant que ``sato`` à l'aide du lien de connexion en haut de la page de recherche, et vérifiez que seuls les documents des Ventes et de toute l'entreprise s'affichent
4. Cliquez sur le nom d'utilisateur en haut de la page, choisissez « Déconnexion », puis vérifiez de la même manière avec ``suzuki``, ``tanaka`` et ``yamada``

Pour la vérification, rechercher un mot présent dans tous les documents (par exemple le nom de l'entreprise) permet de comparer plus facilement l'étendue des documents affichés.

Consulter les droits enregistrés dans un document
-------------------------------------------------

Si les documents ne s'affichent pas comme prévu, vérifiez les droits enregistrés dans le document.

1. Dans la console d'administration, ouvrez [Informations système] > [Rechercher] et recherchez des mots de l'URL ou du titre du document. Cet écran ne filtre pas selon les droits et affiche tous les documents
2. Cliquez sur [Mettre à jour] pour le document concerné : l'écran de modification s'ouvre et affiche les droits enregistrés dans le champ ``role``. Contentez-vous de les consulter, sans enregistrer

Les valeurs du champ ``role`` sont affichées dans le format interne suivant.

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Autorisation
     - Affichage dans le champ role
     - Exemple
   * - ``{user}nom_utilisateur``
     - ``1`` + nom
     - ``1sato``
   * - ``{group}nom_groupe``
     - ``2`` + nom
     - ``2Sales``
   * - ``{role}nom_rôle``
     - ``R`` + nom
     - ``Rguest``
   * - Avec ``(deny)``
     - Préfixe ``D``
     - ``D2Sales``

Si le champ ``role`` d'un document des Ventes contient ``2Sales`` et ``2Executives``, les autorisations sont enregistrées comme configuré.
S'il reste ``Rguest``, soit vous n'avez pas réexploré après avoir modifié les autorisations, soit vous avez oublié de supprimer la valeur initiale ``{role}guest``.

Ne rien montrer aux utilisateurs non connectés
==============================================

Si vous placez Fess sur un réseau accessible à des personnes extérieures à l'entreprise, ou si vous n'autorisez tout simplement pas la recherche sans connexion, activez « Connexion requise » dans [Système] > [Général].
Une fois cette option activée, les visiteurs non connectés ne peuvent plus effectuer de recherche.

Ce paramètre est indépendant du filtrage par autorisations.
Même s'il reste des documents portant ``{role}guest``, ils ne sont plus affichés aux visiteurs non connectés.
Ce paramètre est lui aussi enregistré dans ``system.properties`` ; avec Docker, la même précaution que pour les paramètres LDAP s'applique.

Pour aller plus loin
====================

- Filtrer la visibilité avec les ACL d'un serveur de fichiers : :doc:`file-server-search`
- Permettre la connexion par SSO avec les comptes de l'entreprise : :doc:`guide-15`
- Utiliser un seul Fess pour plusieurs organisations : :doc:`guide-13`
- Attribuer aussi des droits aux documents de Slack ou d'un stockage cloud : :doc:`datastore-basics`
- Rechercher dans Git, Confluence, Jira et Slack d'une équipe de développement : :doc:`guide-06`

Références
==========

- `Configuration de la recherche basée sur les rôles <https://fess.codelibs.org/fr/stable/config/security-role.html>`__
- `Recherche par rôle (pour les utilisateurs) <https://fess.codelibs.org/fr/stable/user/role-search.html>`__
- `Guide d'intégration LDAP <https://fess.codelibs.org/fr/stable/config/ldap-integration.html>`__
- `Utilisateur <https://fess.codelibs.org/fr/stable/admin/user-guide.html>`__
- `Groupe <https://fess.codelibs.org/fr/stable/admin/group-guide.html>`__
- `Étiquette <https://fess.codelibs.org/fr/stable/admin/labeltype-guide.html>`__
- `Recherche (console d'administration) <https://fess.codelibs.org/fr/stable/admin/searchlist-guide.html>`__
