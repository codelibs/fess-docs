============================================================
Partie 13 : Plateforme de recherche multi-tenant -- Concevoir une seule instance Fess pour servir plusieurs organisations
============================================================

Introduction
=============

Lorsque vous souhaitez fournir Fess a plusieurs departements internes ou a plusieurs clients en tant que MSP (fournisseur de services geres), il est inefficace de deployer une instance Fess distincte pour chaque tenant.

Cet article explique une conception multi-tenant qui permet de servir plusieurs tenants (organisations, departements ou clients) a partir d'une seule instance Fess.

Public cible
=============

- Personnes souhaitant fournir des services de recherche a plusieurs organisations ou departements
- Personnes interessees par la conception multi-tenant avec Fess
- Personnes souhaitant apprendre a utiliser la fonctionnalite d'hote virtuel

Scenario
========

Nous supposons un scenario dans lequel le departement informatique d'un groupe d'entreprises fournit des services de recherche a trois filiales.

.. list-table:: Configuration des tenants
   :header-rows: 1
   :widths: 25 35 40

   * - Tenant
     - Domaine
     - Cible de recherche
   * - Entreprise A (Industrie manufacturiere)
     - search-a.example.com
     - Specifications produits, documents de controle qualite
   * - Entreprise B (Commerce de detail)
     - search-b.example.com
     - Manuels de magasin, informations produits
   * - Entreprise C (Services)
     - search-c.example.com
     - Manuels de service client, FAQ

Chaque tenant a les exigences suivantes :

- Les donnees ne doivent pas etre visibles entre les tenants (isolation des donnees)
- Chaque tenant necessite un design different (branding)
- Chaque tenant necessite des parametres de crawl independants

Fonctionnalite d'hote virtuel
===============================

La fonctionnalite d'hote virtuel de Fess permet de fournir differentes experiences de recherche en fonction du nom d'hote utilise pour l'acces.

Configuration de l'hote virtuel
--------------------------------

Definissez la valeur de l'hote virtuel dans la console d'administration.
En associant cette valeur aux parametres de crawl et aux labels, vous pouvez realiser l'isolation des donnees pour chaque tenant.

Considerations de conception
------------------------------

**Configuration DNS / repartiteur de charge**

Configurez le DNS pour que le domaine de chaque tenant pointe vers le meme serveur Fess.

::

    search-a.example.com → Serveur Fess (192.168.1.100)
    search-b.example.com → Serveur Fess (192.168.1.100)
    search-c.example.com → Serveur Fess (192.168.1.100)

Fess examine les en-tetes HTTP de la requete pour determiner quel hote virtuel est accede.
Par defaut, l'en-tete Host est utilise, mais vous pouvez specifier n'importe quel en-tete via le parametre ``virtual.host.headers``.
Le format de configuration est ``NomEnTete:Valeur=CleHoteVirtuel`` (par exemple, ``Host:search-a.example.com=tenant-a``).

Conception de l'isolation des tenants
=======================================

Isolation des donnees
----------------------

L'isolation des donnees entre tenants est realisee grace au champ ``virtual_host`` des documents, fourni par la fonctionnalite d'hote virtuel.

**Isolation par hote virtuel**

Lorsque vous definissez la cle d'hote virtuel dans le champ "Hote virtuel" des parametres de crawl, les documents indexes recoivent un champ ``virtual_host``.
Lors de la recherche, ce champ est utilise pour le filtrage automatique, de sorte que les utilisateurs accedant via le domaine d'un tenant ne voient que les documents de ce tenant dans les resultats de recherche.

- ``tenant-a`` : Documents de l'Entreprise A
- ``tenant-b`` : Documents de l'Entreprise B
- ``tenant-c`` : Documents de l'Entreprise C

De plus, en configurant le champ "Hote virtuel" sur les labels, vous pouvez egalement separer les labels affiches pour chaque tenant.

**Isolation par roles**

Pour des exigences d'isolation plus strictes, combinez la recherche basee sur les roles (voir Partie 5).
Creez des roles pour chaque tenant et attribuez-les aux parametres de crawl et aux utilisateurs.

Configuration du crawl
------------------------

La configuration de crawl de chaque tenant est geree de maniere independante.

.. list-table:: Parametres de crawl par tenant
   :header-rows: 1
   :widths: 15 30 25 30

   * - Tenant
     - Cible de crawl
     - Planification
     - Label
   * - Entreprise A
     - smb://fs-a/docs/
     - Quotidien a 1h00
     - tenant-a
   * - Entreprise B
     - https://portal-b.example.com/
     - Quotidien a 2h00
     - tenant-b
   * - Entreprise C
     - smb://fs-c/manuals/
     - Quotidien a 3h00
     - tenant-c

Themes par tenant
==================

En utilisant la fonctionnalite de themes de Fess, vous pouvez fournir des designs differents pour chaque tenant.

Conception des themes
----------------------

Preparez des themes correspondant aux couleurs de marque et au logo de chaque tenant.

- Entreprise A : Un design sobre pour une entreprise industrielle (tons bleus)
- Entreprise B : Un design lumineux pour le commerce de detail (tons verts)
- Entreprise C : Un design convivial pour une entreprise de services (tons oranges)

Association des hotes virtuels et des themes
----------------------------------------------

En changeant de theme pour chaque hote virtuel, les utilisateurs de chaque tenant verront un ecran de recherche avec l'image de marque de leur propre entreprise.

Fess propose des themes integres tels que ``simple``, ``docsearch`` et ``codesearch``, et prend egalement en charge les themes personnalises.

Isolation de l'acces API
=========================

Jetons d'acces API par tenant
-------------------------------

Emettez des jetons d'acces individuels pour chaque tenant.
En associant des roles aux jetons, l'isolation des tenants est egalement appliquee a l'acces API.

.. list-table:: Configuration des jetons d'acces
   :header-rows: 1
   :widths: 20 30 50

   * - Tenant
     - Nom du jeton
     - Role attribue
   * - Entreprise A
     - tenant-a-api-token
     - tenant-a-role
   * - Entreprise B
     - tenant-b-api-token
     - tenant-b-role
   * - Entreprise C
     - tenant-c-api-token
     - tenant-c-role

Lorsque le systeme d'un tenant s'integre via l'API (voir Partie 11), l'utilisation de jetons specifiques au tenant garantit qu'il ne peut pas acceder aux donnees des autres tenants.

Considerations operationnelles
================================

Gestion des ressources
-----------------------

Etant donne qu'une seule instance Fess sert plusieurs tenants, une attention particuliere a l'allocation des ressources est necessaire.

- **Repartition de la charge de crawl** : Echelonnez les planifications de crawl des tenants pour eviter l'execution simultanee
- **Taille de l'index** : Surveillez la taille totale de l'index de tous les tenants
- **Memoire** : Ajustez le tas JVM en fonction du nombre de tenants et de documents

Ajout et suppression de tenants
---------------------------------

Standardisez la procedure d'ajout de nouveaux tenants.

1. Creer un label
2. Creer un role
3. Enregistrer les parametres de crawl
4. Configurer l'hote virtuel
5. Emettre un jeton d'acces
6. Ajouter les parametres DNS

Lors de la suppression d'un tenant, n'oubliez pas de supprimer les donnees d'index associees.

Criteres de mise a l'echelle
------------------------------

Si vous observez les symptomes suivants, envisagez de diviser ou de mettre a l'echelle les instances Fess (voir Partie 14).

- Degradation des temps de reponse de recherche
- Les crawls ne se terminent pas dans la fenetre planifiee
- Erreurs frequentes de memoire insuffisante
- Le nombre de tenants depasse 10

Resume
=======

Cet article a explique la conception multi-tenant utilisant la fonctionnalite d'hote virtuel de Fess.

- Acces specifique par tenant via les hotes virtuels
- Isolation des donnees a l'aide de labels et de roles
- Branding specifique par tenant grace aux themes
- Isolation des tenants via les jetons d'acces API
- Gestion des ressources et criteres de mise a l'echelle

Avec une seule instance Fess, vous pouvez servir efficacement plusieurs tenants, en maintenant des couts de gestion faibles tout en repondant aux exigences de chaque tenant.

Le prochain article traitera des strategies de mise a l'echelle pour les systemes de recherche.

References
==========

- `Fess Virtual Host <https://fess.codelibs.org/ja/15.5/config/virtual-host.html>`__

- `Fess Configuration des labels <https://fess.codelibs.org/ja/15.5/admin/labeltype.html>`__
