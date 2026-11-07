================================================
Partie 13 : Plateforme de recherche multi-tenant
================================================

Introduction
=============

Lorsque vous souhaitez fournir Fess à plusieurs départements internes ou à plusieurs clients en tant que MSP (fournisseur de services gérés), il est inefficace de déployer une instance Fess distincte pour chaque tenant.

Cet article explique une conception multi-tenant qui permet de servir plusieurs tenants (organisations, départements ou clients) à partir d'une seule instance Fess.

Public cible
=============

- Personnes souhaitant fournir des services de recherche à plusieurs organisations ou départements
- Personnes intéressées par la conception multi-tenant avec Fess
- Personnes souhaitant apprendre à utiliser la fonctionnalité d'hôte virtuel

Scénario
========

Nous supposons un scénario dans lequel le département informatique d'un groupe d'entreprises fournit des services de recherche à trois filiales.

.. list-table:: Configuration des tenants
   :header-rows: 1
   :widths: 25 35 40

   * - Tenant
     - Domaine
     - Cible de recherche
   * - Entreprise A (Industrie manufacturière)
     - search-a.example.com
     - Spécifications produits, documents de contrôle qualité
   * - Entreprise B (Commerce de détail)
     - search-b.example.com
     - Manuels de magasin, informations produits
   * - Entreprise C (Services)
     - search-c.example.com
     - Manuels de service client, FAQ

Chaque tenant a les exigences suivantes :

- Les données ne doivent pas être visibles entre les tenants (isolation des données)
- Chaque tenant nécessite un design différent (branding)
- Chaque tenant nécessite des paramètres de crawl indépendants

Fonctionnalité d'hôte virtuel
===============================

La fonctionnalité d'hôte virtuel de Fess permet de fournir différentes expériences de recherche en fonction du nom d'hôte utilisé pour l'accès.

Configuration de l'hôte virtuel
--------------------------------

Définissez la valeur de l'hôte virtuel dans la console d'administration.
En associant cette valeur aux paramètres de crawl et aux labels, vous pouvez réaliser l'isolation des données pour chaque tenant.

Considérations de conception
------------------------------

**Configuration DNS / répartiteur de charge**

Configurez le DNS pour que le domaine de chaque tenant pointe vers le même serveur Fess.

::

    search-a.example.com → Serveur Fess (192.168.1.100)
    search-b.example.com → Serveur Fess (192.168.1.100)
    search-c.example.com → Serveur Fess (192.168.1.100)

Fess examine les en-têtes HTTP de la requête pour déterminer quel hôte virtuel est accédé.
Par défaut, l'en-tête Host est utilisé, mais vous pouvez spécifier n'importe quel en-tête via le paramètre ``virtual.host.headers``.
Le format de configuration est ``NomEnTete:Valeur=CleHoteVirtuel`` (par exemple, ``Host:search-a.example.com=tenant-a``).

Conception de l'isolation des tenants
=======================================

Isolation des données
----------------------

L'isolation des données entre tenants est réalisée grâce au champ ``virtual_host`` des documents, fourni par la fonctionnalité d'hôte virtuel.

**Isolation par hôte virtuel**

Lorsque vous définissez la clé d'hôte virtuel dans le champ "Hôte virtuel" des paramètres de crawl, les documents indexés reçoivent un champ ``virtual_host``.
Lors de la recherche, ce champ est utilisé pour le filtrage automatique, de sorte que les utilisateurs accédant via le domaine d'un tenant ne voient que les documents de ce tenant dans les résultats de recherche.

- ``tenant-a`` : Documents de l'Entreprise A
- ``tenant-b`` : Documents de l'Entreprise B
- ``tenant-c`` : Documents de l'Entreprise C

De plus, en configurant le champ "Hôte virtuel" sur les labels, vous pouvez également séparer les labels affichés pour chaque tenant.

**Isolation par rôles**

Pour des exigences d'isolation plus strictes, combinez la recherche basée sur les rôles (voir Partie 5).
Créez des rôles pour chaque tenant et attribuez-les aux paramètres de crawl et aux utilisateurs.

Configuration du crawl
------------------------

La configuration de crawl de chaque tenant est gérée de manière indépendante.

.. list-table:: Paramètres de crawl par tenant
   :header-rows: 1
   :widths: 15 30 25 30

   * - Tenant
     - Cible de crawl
     - Planification
     - Label
   * - Entreprise A
     - smb://fs-a/docs/
     - Quotidien à 1h00
     - tenant-a
   * - Entreprise B
     - https://portal-b.example.com/
     - Quotidien à 2h00
     - tenant-b
   * - Entreprise C
     - smb://fs-c/manuals/
     - Quotidien à 3h00
     - tenant-c

Thèmes par tenant
==================

En utilisant la fonctionnalité de thèmes de Fess, vous pouvez fournir des designs différents pour chaque tenant.

Conception des thèmes
----------------------

Préparez des thèmes correspondant aux couleurs de marque et au logo de chaque tenant.

- Entreprise A : Un design sobre pour une entreprise industrielle (tons bleus)
- Entreprise B : Un design lumineux pour le commerce de détail (tons verts)
- Entreprise C : Un design convivial pour une entreprise de services (tons oranges)

Association des hôtes virtuels et des thèmes
----------------------------------------------

En changeant de thème pour chaque hôte virtuel, les utilisateurs de chaque tenant verront un écran de recherche avec l'image de marque de leur propre entreprise.

Fess propose des thèmes intégrés tels que ``simple``, ``docsearch`` et ``codesearch``, et prend également en charge les thèmes personnalisés.

Isolation de l'accès API
=========================

Jetons d'accès API par tenant
-------------------------------

Émettez des jetons d'accès individuels pour chaque tenant.
En associant des rôles aux jetons, l'isolation des tenants est également appliquée à l'accès API.

.. list-table:: Configuration des jetons d'accès
   :header-rows: 1
   :widths: 20 30 50

   * - Tenant
     - Nom du jeton
     - Rôle attribué
   * - Entreprise A
     - tenant-a-api-token
     - tenant-a-role
   * - Entreprise B
     - tenant-b-api-token
     - tenant-b-role
   * - Entreprise C
     - tenant-c-api-token
     - tenant-c-role

Lorsque le système d'un tenant s'intègre via l'API (voir Partie 11), l'utilisation de jetons spécifiques au tenant garantit qu'il ne peut pas accéder aux données des autres tenants.

Considérations opérationnelles
================================

Gestion des ressources
-----------------------

Étant donné qu'une seule instance Fess sert plusieurs tenants, une attention particulière à l'allocation des ressources est nécessaire.

- **Répartition de la charge de crawl** : Échelonnez les planifications de crawl des tenants pour éviter l'exécution simultanée
- **Taille de l'index** : Surveillez la taille totale de l'index de tous les tenants
- **Mémoire** : Ajustez le tas JVM en fonction du nombre de tenants et de documents

Ajout et suppression de tenants
---------------------------------

Standardisez la procédure d'ajout de nouveaux tenants.

1. Créer un label
2. Créer un rôle
3. Enregistrer les paramètres de crawl
4. Configurer l'hôte virtuel
5. Émettre un jeton d'accès
6. Ajouter les paramètres DNS

Lors de la suppression d'un tenant, n'oubliez pas de supprimer les données d'index associées.

Critères de mise à l'échelle
------------------------------

Si vous observez les symptômes suivants, envisagez de diviser ou de mettre à l'échelle les instances Fess (voir Partie 14).

- Dégradation des temps de réponse de recherche
- Les crawls ne se terminent pas dans la fenêtre planifiée
- Erreurs fréquentes de mémoire insuffisante
- Le nombre de tenants dépasse 10

Résumé
=======

Cet article a expliqué la conception multi-tenant utilisant la fonctionnalité d'hôte virtuel de Fess.

- Accès spécifique par tenant via les hôtes virtuels
- Isolation des données à l'aide de labels et de rôles
- Branding spécifique par tenant grâce aux thèmes
- Isolation des tenants via les jetons d'accès API
- Gestion des ressources et critères de mise à l'échelle

Avec une seule instance Fess, vous pouvez servir efficacement plusieurs tenants, en maintenant des coûts de gestion faibles tout en répondant aux exigences de chaque tenant.

Le prochain article traitera des stratégies de mise à l'échelle pour les systèmes de recherche.

Références
==========

- `Fess Virtual Host <https://fess.codelibs.org/ja/15.5/config/virtual-host.html>`__

- `Fess Configuration des labels <https://fess.codelibs.org/ja/15.5/admin/labeltype.html>`__
