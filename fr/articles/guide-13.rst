=========================================
Un seul Fess pour plusieurs organisations
=========================================

Introduction
============

Lorsque vous souhaitez proposer un service de recherche à chaque société d'un groupe ou à chaque service, construire un Fess par organisation multiplie d'autant les serveurs et les configurations d'exploration à gérer.
La fonctionnalité d'hôtes virtuels de Fess permet de publier un seul Fess sous plusieurs noms d'hôte et de changer, selon le nom d'hôte, les cibles de recherche, les étiquettes et la page de recherche.

Toutefois, un hôte virtuel ne fait que changer ce qui est affiché selon le nom d'hôte par lequel la requête est arrivée ; ce n'est pas un contrôle d'accès.
Pour garantir que les documents d'une organisation restent invisibles pour les autres, il faut le combiner avec des autorisations basées sur les rôles et avec la connexion.

Dans cet article, nous prenons l'exemple de deux locataires, la société A et la société B, et configurons pas à pas les éléments suivants dans Fess 15.9.

- Associer les noms d'hôte aux locataires dans « Hôte virtuel » de [Général]
- Indiquer l'hôte virtuel et les autorisations dans les configurations d'exploration et les étiquettes pour séparer les documents de chaque locataire
- Donner à chaque locataire sa propre page de recherche grâce à un thème portant le même nom que la clé de l'hôte virtuel
- Se connecter avec un utilisateur d'un locataire et vérifier que les documents des autres locataires ne sont pas visibles
- Ajouter et supprimer des locataires dans le bon ordre

Les bases des rôles, des groupes et des utilisateurs sont traitées dans :doc:`guide-05`.

À retenir d'abord : un hôte virtuel n'est pas un contrôle d'accès
=================================================================

Pour chaque requête, Fess évalue de haut en bas les lignes saisies dans « Hôte virtuel » de [Général] et utilise le nom d'hôte virtuel (ci-après, la clé) de la première ligne dont l'en-tête indiqué (en général ``Host``) correspond.
Une fois la clé déterminée, les fonctionnalités suivantes sont filtrées par cette clé.

- Résultats de recherche : seuls les documents dont la configuration d'exploration contient cette clé dans « Hôtes virtuels » sont renvoyés (il en va de même pour l'API de recherche)
- Étiquettes : seules les étiquettes dont le champ « Hôte virtuel » contient cette clé sont affichées
- Correspondance de clé, Contenu associé et Requête associée : seuls les paramètres dont le champ « Hôte virtuel » contient cette clé sont utilisés
- Page de recherche : s'il existe un thème dont le nom est la clé en minuscules, la page est affichée avec ce thème

En revanche, pour une requête qui ne correspond à aucune ligne, aucun de ces filtrages n'a lieu.
Si quelqu'un accède directement au serveur par son adresse IP, ou si un proxy inverse réécrit l'en-tête ``Host``, le filtrage par hôte virtuel disparaît et les documents de tous les locataires deviennent consultables, dans la limite des autorisations.
Une faute de frappe dans un nom d'hôte ou un numéro de port oublié dans [Général] ne provoque pas non plus d'erreur : la requête est simplement traitée comme « sans correspondance ».

Pour que les documents ne soient pas visibles d'un locataire à l'autre, combinez donc les deux mesures suivantes.

- Limiter les autorisations des documents de chaque locataire au rôle de ce locataire (par exemple ``{role}tenanta_user``)
- Exiger la connexion pour la page de recherche et attribuer aux utilisateurs le rôle de leur locataire

La configuration de cet article
===============================

.. list-table::
   :header-rows: 1
   :widths: 16 26 14 18 26

   * - Locataire
     - Nom d'hôte public
     - Clé
     - Rôle
     - Cible d'exploration
   * - Société A
     - ``search-a.example.com``
     - ``tenanta``
     - ``tenanta_user``
     - ``https://portal-a.example.com/``
   * - Société B
     - ``search-b.example.com``
     - ``tenantb``
     - ``tenantb_user``
     - ``https://portal-b.example.com/``

Une clé ne peut contenir que des caractères alphanumériques et des traits de soulignement (``a-zA-Z0-9_``).
Les autres caractères sont supprimés à l'enregistrement : si vous écrivez ``tenant-a``, la clé devient ``tenanta``, et un ``tenant-a`` saisi dans une configuration d'exploration ne correspondra pas.
``admin``, ``common``, ``error``, ``login`` et ``profile`` sont réservés et ne peuvent pas être utilisés.

Les champs « Hôtes virtuels » des configurations d'exploration et « Hôte virtuel » des étiquettes sont en saisie libre, et la comparaison avec la clé est sensible à la casse.
Les noms de thème ne peuvent eux aussi contenir que des minuscules : choisir dès le départ des clés en minuscules alphanumériques évite les erreurs.

Étape 1 : associer les noms d'hôte aux clés
===========================================

Dans la console d'administration, ouvrez [Système] > [Général], saisissez dans « Hôte virtuel » une entrée ``nom-d-en-tête:valeur=clé`` par ligne, puis mettez à jour.

::

    Host:search-a.example.com=tenanta
    Host:search-b.example.com=tenantb

La valeur de l'en-tête est comparée en correspondance exacte, sans distinction de casse.
Lorsqu'un navigateur accède à un port autre que les ports standard (80 et 443), il ajoute le numéro de port à l'en-tête ``Host`` ; si les utilisateurs accèdent directement au port 8080 de Fess, indiquez donc aussi le port comme suit.
Vous pouvez également écrire les deux formes l'une à la suite de l'autre.

::

    Host:search-a.example.com:8080=tenanta
    Host:search-b.example.com:8080=tenantb

Le paramètre prend effet dès l'enregistrement ; aucun redémarrage n'est nécessaire.
Vous pouvez aussi l'écrire au même format dans ``virtual.host.headers`` de ``fess_config.properties``, mais si [Général] contient une valeur, c'est elle qui prévaut.

Si Fess est placé derrière un proxy inverse, transmettez jusqu'à Fess l'en-tête ``Host`` envoyé par le navigateur.
Par défaut, Nginx définit ``Host`` sur la destination de ``proxy_pass`` ; ``proxy_set_header Host $host;`` est donc nécessaire.

::

    server {
        server_name search-a.example.com search-b.example.com;
        location / {
            proxy_pass http://127.0.0.1:8080;
            proxy_set_header Host $host;
        }
    }

Dans une configuration qui réécrit ``Host``, vous pouvez à la place indiquer ``X-Forwarded-Host`` comme nom d'en-tête (par exemple ``X-Forwarded-Host:search-a.example.com=tenanta``).

.. warning::

   Les paramètres de [Général] sont enregistrés dans ``system.properties`` à l'intérieur du conteneur.
   ``fess01`` de docker-fess n'a pas de volume : si vous recréez le conteneur avec ``docker compose down``, la valeur de « Hôte virtuel » est perdue elle aussi (elle est conservée avec ``stop`` et ``start``).
   Le thème que vous téléverserez à une étape ultérieure est également stocké dans le conteneur et sera perdu de la même façon.
   Pour savoir comment conserver les paramètres, consultez `Installation avec Docker (Détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__.

Étape 2 : créer les rôles et les utilisateurs des locataires
============================================================

1. Dans [Utilisateur] > [Rôle], créez les rôles nommés ``tenanta_user`` et ``tenantb_user``.
2. Dans [Utilisateur] > [Utilisateur], créez les utilisateurs de chaque locataire et sélectionnez le rôle de leur locataire dans « Rôles ».
3. Dans [Système] > [Général], activez « Connexion requise ».

Les utilisateurs connectés ne reçoivent pas ``{role}guest`` : ils recherchent uniquement avec les autorisations de leur utilisateur, de leurs groupes et de leurs rôles.
Si vous souhaitez utiliser directement les groupes LDAP ou SSO, vous pouvez indiquer ``{group}<nom du groupe>`` à la place d'un rôle.
Pour le fonctionnement des autorisations et l'intégration LDAP, consultez :doc:`guide-05` ; pour le SSO, consultez :doc:`guide-15`.

Étape 3 : créer une étiquette par locataire
===========================================

Une étiquette est attribuée, au moment de l'exploration, aux documents dont l'URL correspond à « Chemins inclus ».
Créez-la donc avant l'exploration.

Dans [Robot d'exploration] > [Étiquette], cliquez sur [Créer nouveau] et saisissez ce qui suit pour la société A (créez celle de la société B de la même façon).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Valeur
   * - Nom
     - ``Portail société A``
   * - Valeur
     - ``tenanta_docs`` (caractères alphanumériques et traits de soulignement uniquement)
   * - Chemins inclus
     - ``https://portal-a\.example\.com/.*``
   * - Autorisations
     - ``{role}tenanta_user``
   * - Hôte virtuel
     - ``tenanta``

Les autorisations d'une nouvelle étiquette contiennent ``{role}guest``.
Une étiquette n'est affichée que si l'utilisateur possède un rôle figurant dans ses autorisations ; si vous laissez ``{role}guest``, l'étiquette n'est donc pas affichée aux utilisateurs connectés du locataire.

Une étiquette dont le champ « Hôte virtuel » est vide n'est pas affichée lors d'un accès par un hôte virtuel.
Une étiquette ne peut avoir qu'un seul hôte virtuel : si plusieurs locataires doivent voir la même étiquette, créez autant d'étiquettes de même nom et de même valeur que de locataires, et saisissez la clé correspondante dans le champ « Hôte virtuel » de chacune.
Il en va de même pour Correspondance de clé, Contenu associé et Requête associée : les paramètres dont le champ « Hôte virtuel » est vide ne sont pas utilisés sur les hôtes des locataires.

Étape 4 : indiquer l'hôte virtuel et les autorisations dans la configuration d'exploration
==========================================================================================

Dans [Robot d'exploration] > [Web], créez la configuration d'exploration de la société A.
Les configurations d'exploration de système de fichiers et de magasin de données comportent les deux mêmes champs.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Valeur
   * - Nom
     - ``Portail société A``
   * - URL
     - ``https://portal-a.example.com/``
   * - URL incluses
     - ``https://portal-a.example.com/.*``
   * - Autorisations
     - ``{role}tenanta_user`` (supprimez le ``{role}guest`` saisi par défaut)
   * - Hôtes virtuels
     - ``tenanta``

Si vous laissez ``{role}guest``, ces documents deviennent visibles lors d'un accès par adresse IP ou avant la connexion.

Pour des documents destinés à plusieurs locataires, comme un recueil de règlements commun au groupe, écrivez dans une seule configuration d'exploration une ligne par locataire, pour les deux locataires, dans « Hôtes virtuels » et dans « Autorisations ».

::

    Hôtes virtuels:
    tenanta
    tenantb

    Autorisations:
    {role}tenanta_user
    {role}tenantb_user

Les hôtes virtuels et les autorisations sont écrits dans les documents au moment de l'exploration.
Si vous les modifiez dans une configuration déjà explorée, les documents existants ne reflètent pas la modification avant une nouvelle exploration.

Après avoir enregistré la configuration, créez une tâche dédiée au locataire avec [Créer une nouvelle tâche] sur l'écran de détails, ou exécutez ``Default Crawler`` avec [Démarrer maintenant] dans [Système] > [Planificateur].

Étape 5 : préparer une page de recherche propre à chaque locataire
==================================================================

Dans Fess 15.9, la page de recherche est affichée par un thème.
Si vous installez un thème dont le ``name`` de ``theme.yml`` est la clé en minuscules, ce thème est utilisé pour les requêtes portant cette clé.
Il n'est pas nécessaire d'en faire le thème par défaut ; les requêtes qui ne correspondent à aucune clé utilisent le thème par défaut.

Créez-le en copiant le thème ``bootstrap`` fourni.
Avec Docker, extrayez-le du conteneur comme suit.

::

    $ docker cp fess01:/usr/share/fess/app/themes/bootstrap ./tenanta

1. Dans ``tenanta/theme.yml``, remplacez ``name`` par ``tenanta`` et ``displayName`` par exemple par ``Recherche société A``.
2. Remplacez ``assets/styles.css`` (couleurs) ainsi que ``assets/logo-head.png`` et ``assets/logo.png`` (logos). ``index.html`` n'a pas besoin d'être modifié.
3. Créez l'archive de sorte que ``theme.yml`` se trouve à la racine du ZIP.

   ::

       $ cd tenanta && zip -r ../tenanta.zip .

4. Téléversez ``tenanta.zip`` avec [Téléverser] dans [Système] > [Thème].

La page de connexion (``/login/``) est commune à tous les locataires et ne peut pas être modifiée par un thème.
Pour plus de détails sur la copie du thème fourni, consultez le `Guide de développement des thèmes <https://fess.codelibs.org/fr/stable/dev/theme-development.html>`__.

Vérifier la séparation
======================

Avant de basculer le DNS, vous pouvez ajouter ``127.0.0.1 search-a.example.com search-b.example.com`` au fichier ``/etc/hosts`` de votre poste et essayer chaque hôte depuis un navigateur, par exemple ``http://search-a.example.com:8080/`` ([Général] doit alors contenir les lignes avec le port).
Vérifiez les quatre cas suivants en recherchant un mot présent dans les cibles d'exploration.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Accès
     - Résultat attendu
   * - Utilisateur de la société A via ``search-a.example.com``
     - Seuls les documents de la société A apparaissent. La seule étiquette est « Portail société A ». La page s'affiche avec le thème de la société A
   * - Utilisateur de la société A via ``search-b.example.com``
     - 0 résultat (l'utilisateur n'a pas d'autorisation sur les documents de la société B, et les documents de la société A sont exclus par l'hôte virtuel)
   * - Utilisateur de la société A via l'adresse IP (``http://<serveur>:8080/``)
     - Seuls les documents de la société A apparaissent (pas de filtrage par hôte virtuel, mais les autorisations les protègent)
   * - Accès sans connexion
     - Impossible de rechercher avant de se connecter

Si vous avez créé des documents communs aux deux locataires, ils apparaissent aussi dans les lignes 1 à 3.
Si des documents de la société B apparaissent à la ligne 3, il reste un ``{role}guest`` dans l'une des configurations d'exploration.
Si la ligne 1 donne 0 résultat, comparez les lignes de [Général] (avec ou sans numéro de port) à l'orthographe du champ « Hôtes virtuels » de la configuration d'exploration.

La même vérification est possible avec l'API de recherche.
Dans [Système] > [Jeton d'accès], créez un jeton avec l'autorisation ``{role}tenanta_user``, puis appelez l'API en changeant l'en-tête ``Host``.

::

    $ curl -s -H "Authorization: Bearer <jeton de la société A>" \
        -H "Host: search-a.example.com:8080" \
        "http://localhost:8080/api/v2/search?q=fess"
    $ curl -s -H "Authorization: Bearer <jeton de la société A>" \
        -H "Host: search-b.example.com:8080" \
        "http://localhost:8080/api/v2/search?q=fess"

Le comportement est celui attendu si ``response.record_count`` vaut 1 ou plus pour le premier appel et 0 pour le second.
Un jeton d'accès n'est pas lié à un hôte virtuel : c'est le nom d'hôte de destination de la requête qui détermine l'hôte virtuel.
Ce qu'un jeton peut voir est déterminé par ses autorisations ; attribuez donc toujours aux jetons remis aux systèmes d'un locataire le seul rôle de ce locataire.
Pour l'utilisation de l'API, consultez :doc:`guide-11`.

Une fois l'exploitation commencée, vous pouvez consulter le nombre de recherches par hôte virtuel dans l'onglet [Audience] de [Informations système] > [Journal de recherche].

Ajouter et supprimer des locataires
===================================

Pour ajouter un locataire, procédez dans l'ordre suivant, car les étapes ultérieures utilisent des valeurs définies aux étapes précédentes.

1. Ajouter une ligne dans « Hôte virtuel » de [Général]
2. Créer le rôle, les utilisateurs et, si nécessaire, les jetons d'accès
3. Créer les étiquettes (avec hôte virtuel et autorisations)
4. Créer les configurations d'exploration (avec hôte virtuel et autorisations), puis lancer l'exploration
5. Téléverser le thème
6. Vérifier les quatre cas de « Vérifier la séparation »
7. Publier via le DNS et le proxy inverse

Pour supprimer un locataire, fermez au contraire d'abord les points d'entrée.

1. Retirer le nom d'hôte du DNS et du proxy inverse
2. Supprimer les configurations d'exploration et les tâches créées pour elles ([Système] > [Planificateur])
3. Supprimer les documents de l'index (voir ci-dessous)
4. Supprimer les jetons d'accès, les utilisateurs et le rôle
5. Supprimer les étiquettes, les correspondances de clé et les autres paramètres de cette clé, ainsi que le thème
6. Supprimer la ligne dans « Hôte virtuel » de [Général]

Supprimer une configuration d'exploration ne retire pas de l'index les documents déjà explorés.
Supprimez les documents dans [Informations système] > [Rechercher].
Cet écran n'applique aucun filtrage par rôle ni par hôte virtuel : les documents de tous les locataires sont concernés.
Recherchez dans le champ de recherche avec l'étiquette du locataire, par exemple ``label:tenantb_docs``, vérifiez que le nombre et les résultats ne contiennent que des documents de la société B, puis cliquez sur [Tout supprimer par cette requête].
Pour des documents web, vous pouvez aussi indiquer le début de l'URL, par exemple ``site:portal-b.example.com``.

N'utilisez pas de requête comme ``virtual_host:tenantb``.
Par défaut, ``virtual_host`` ne fait pas partie des champs utilisables pour la recherche : la chaîne entière est traitée comme une recherche de ce texte dans le corps des documents, et ne permet pas de sélectionner les documents voulus.

L'option d'instances séparées
=============================

Lorsque plusieurs locataires partagent un même Fess, les éléments suivants ne peuvent pas être séparés.

- La console d'administration et les administrateurs : tout administrateur peut modifier les paramètres, les utilisateurs et les documents de tous les locataires
- Les paramètres valables pour tout le système, comme ceux de [Général] et les dictionnaires
- La page de connexion

Si vous souhaitez confier l'administration à chaque locataire, ou si des obligations contractuelles imposent des index séparés, lancez un Fess par locataire et utilisez des noms d'index différents.
``compose/multi-instance`` de docker-fess relie deux Fess (ports 8080 et 8081) à un même OpenSearch.

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess
    $ git checkout v15.9.0
    $ cd compose/multi-instance
    $ docker compose -f compose.yaml -f compose-fess01.yaml -f compose-fess02.yaml up -d

Dans le ``FESS_JAVA_OPTS`` de chaque Fess, les noms d'index des documents, des suggestions, de l'exploration, de la configuration, des utilisateurs, des journaux et des dictionnaires (8 éléments, comme ``-Dfess.config.index.document.search.index=fess01.search``) sont différents pour chaque instance.
Comme la configuration et les utilisateurs sont eux aussi séparés par index, la console d'administration, les utilisateurs et les journaux de recherche sont également propres à chaque locataire.
Pour ajouter un locataire, copiez ``compose-fess02.yaml`` et changez le nom du service, le port et tous les noms d'index.

.. warning::

   Dans cette configuration, OpenSearch expose le port 9200 avec le plugin de sécurité désactivé.
   Toute personne pouvant atteindre le port 9200 peut lire les index de tous les locataires ; fermez donc ce port en production.

Pour aller plus loin
====================

- Approfondir la conception des autorisations avec les rôles, les groupes et LDAP : :doc:`guide-05`
- Appeler l'API de recherche depuis les systèmes d'un locataire : :doc:`guide-11`
- Faire se connecter les utilisateurs par SSO et protéger l'accès : :doc:`guide-15`
- Étendre Fess et OpenSearch à mesure que les locataires augmentent : :doc:`guide-14`
- Intégrer la page de recherche dans un site existant : :doc:`guide-03`

Références
==========

- `Hôtes virtuels <https://fess.codelibs.org/fr/stable/config/security-virtual-host.html>`__
- `Configuration multi-locataire (multi-tenant) <https://fess.codelibs.org/fr/stable/config/multitenancy.html>`__
- `Configuration de la recherche basée sur les rôles <https://fess.codelibs.org/fr/stable/config/security-role.html>`__
- `Étiquette <https://fess.codelibs.org/fr/stable/admin/labeltype-guide.html>`__
- `Thème <https://fess.codelibs.org/fr/stable/admin/theme-guide.html>`__
- `Recherche <https://fess.codelibs.org/fr/stable/admin/searchlist-guide.html>`__
- `docker-fess multi-instance (v15.9.0) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose/multi-instance>`__
