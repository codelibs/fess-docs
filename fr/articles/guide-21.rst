================================================
Rechercher images et texte ensemble (multimodal)
================================================

Introduction
============

Les serveurs de fichiers et les sites internes contiennent un grand nombre d'images, comme des photos de produits ou de chantiers, dont le contenu n'est décrit par rien d'autre que le nom du fichier.
Avec la recherche par mots-clés, on ne peut trouver une image qu'à partir des mots présents dans son nom de fichier ou ses métadonnées.

Le plugin de recherche multimodale ``fess-webapp-multimodal`` permet de rechercher, avec des mots comme « coucher de soleil sur la montagne » ou « chien », les images dont le contenu s'en rapproche.
Dans cet article, nous effectuons les opérations suivantes avec Fess 15.9.

- Démarrer l'environnement Docker d'évaluation ``docker-multimodalsearch`` dans sa version 15.9, explorer des images et les rechercher
- Vérifier, dans la réponse de l'API de recherche, que les images ont été trouvées par la recherche vectorielle
- Passer en revue les réglages nécessaires pour l'intégrer à un Fess existant, ainsi que les pièges courants

Ce qui est possible et ce qui ne l'est pas
==========================================

Commençons par délimiter le périmètre de ``fess-webapp-multimodal`` en 15.9.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Élément
     - Comportement en 15.9
   * - Sens de la recherche
     - Uniquement la recherche d'images à partir de texte. Il n'existe pas de fonction permettant d'envoyer une image pour trouver des images similaires
   * - Images vectorisées
     - Uniquement les fichiers dont le type MIME est ``image/gif``, ``image/jpeg`` ou ``image/png``. Les fichiers BMP et TIFF ne sont pas vectorisés
   * - Images contenues dans des PDF ou des documents Office
     - Elles ne sont pas vectorisées. Pour rechercher le texte présent dans les images, utilisez l'OCR (fonction distincte)
   * - Documents autres que des images
     - Ils sont recherchés comme d'habitude par mots-clés (BM25). Les images et les documents texte apparaissent mélangés dans les résultats
   * - Termes de recherche dans une autre langue que l'anglais (par exemple le français)
     - Il faut un modèle CLIP multilingue. Le modèle par défaut de ``docker-multimodalsearch`` est un modèle multilingue qui, selon le README, ne se limite pas à l'anglais (le README cite l'exemple du japonais)
   * - Recherche sémantique sur le texte
     - Ne peut pas être utilisée dans le même Fess (voir plus loin)

Pour l'OCR, consultez `Configuration de l'OCR <https://fess.codelibs.org/fr/stable/config/crawler-ocr.html>`__.

Fonctionnement
==============

CLIP est un modèle qui projette le texte et les images dans un même espace vectoriel.
Le vecteur du texte « chien » se trouve près des vecteurs des images montrant un chien ; on peut donc rechercher des images d'après la proximité des vecteurs.

Depuis Fess 15.8, le stockage et la recherche des vecteurs sont assurés par Fess lui-même.
Le plugin n'ajoute que la partie qui dialogue avec le serveur CLIP.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Moment
     - Traitement
   * - À l'exploration
     - Les images GIF/JPEG/PNG sont envoyées au serveur CLIP, converties en vecteurs, puis écrites dans le champ vectoriel ``content_chunk_vector`` de Fess
   * - À la recherche
     - Le terme de recherche est converti en vecteur par le serveur CLIP, puis les images proches sont recherchées. Cette recherche s'exécute en parallèle de la recherche par mots-clés, et les deux sont fusionnées en un seul résultat par Rank Fusion
   * - Résultats
     - Les documents trouvés par la recherche vectorielle portent ``multi_modal`` dans le champ ``searcher``. Ceux trouvés par la recherche par mots-clés portent ``default``

Pour le fonctionnement de Rank Fusion, consultez `Recherche hybride et Rank Fusion (sémantique + mots-clés) <https://fess.codelibs.org/fr/stable/config/rank-fusion.html>`__.

Essayer avec docker-multimodalsearch
====================================

``docker-multimodalsearch`` est un environnement Docker Compose qui regroupe les conteneurs et les réglages nécessaires pour essayer immédiatement la recherche multimodale.
Avec le tag ``v15.9.0``, les services suivants démarrent.

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Service
     - Rôle
   * - ``fess01``
     - Fess lui-même. L'image est ``ghcr.io/codelibs/fess:15.9.0-noble`` et le plugin ``fess-webapp-multimodal:15.9.0`` est intégré au démarrage. La page de recherche utilise le thème de galerie d'images ``mosaic``
   * - ``search01``
     - OpenSearch 3.9.0. Le port 9200 n'est publié que sur l'interface de bouclage de l'hôte (127.0.0.1)
   * - ``clip_server``
     - Le serveur CLIP. Le modèle par défaut est le modèle multilingue ``xlm-roberta-base-ViT-B-32::laion5b-s13b-b90k`` (512 dimensions), qui tourne sur le CPU
   * - ``content``
     - Un nginx qui sert les images d'exemple à ``http://content/``. Il n'est accessible que depuis le réseau des conteneurs
   * - ``init-fess-verify``
     - S'exécute une seule fois au démarrage, vérifie que le champ vectoriel de l'index correspond aux réglages, puis se termine

Prérequis
---------

- Docker (commande ``docker compose``), Git, bash
- Une connexion Internet (pour récupérer les images et le modèle CLIP ; selon le README, le modèle pèse environ 1,6 Go)
- Sous Linux, augmentez ``vm.max_map_count`` pour OpenSearch (comme dans les étapes de préparation de :doc:`guide-02`)

Obtenir la version 15.9
-----------------------

La branche par défaut de ``docker-multimodalsearch`` suit la prochaine version en cours de développement ; récupérez donc le tag ``v15.9.0``.

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-multimodalsearch.git
    $ cd docker-multimodalsearch
    $ cp .env.example .env

Ouvrez ``.env`` et changez la source des thèmes pour la branche de 15.9.

::

    FESS_THEMES_REF=15.9.x

Dans ``v15.9.0``, ``.env.example`` contient toujours ``FESS_THEMES_REF=main``, mais le thème ``mosaic`` de la branche ``main`` de ``fess-themes`` cible désormais Fess 15.10 et ultérieur (``minFessVersion: 15.10``).
Le thème ``mosaic`` pour 15.9 se trouve dans la branche ``15.9.x``.

Laissez ``FESS_VERSION=15.9.0`` et ``FESS_PLUGINS=fess-webapp-multimodal:15.9.0`` tels quels dans ``.env``.
La version du plugin doit correspondre à celle de Fess.

Installer et démarrer
---------------------

::

    $ bash bin/setup.sh
    $ docker compose up -d

``bin/setup.sh`` crée les répertoires de données, récupère le thème et prépare le script de génération des vignettes.
Au premier ``docker compose up -d``, l'image de ``clip_server`` est construite et le modèle CLIP est téléchargé.
``fess01`` attend que ``clip_server`` soit prêt avant de démarrer ; le premier démarrage prend donc quelques minutes.

Vérifiez l'état avec les commandes suivantes.

::

    $ docker compose ps -a
    $ docker compose logs init-fess-verify

Si ``fess01`` passe à ``(healthy)``, que ``init-fess-verify`` se termine avec ``Exited (0)`` et que le journal contient la ligne suivante, le champ vectoriel a été créé conformément aux réglages.

::

    [init-fess-verify] OK: dimension=512, engine=lucene, space_type=cosinesimil, index.knn=true

Explorer les images d'exemple
-----------------------------

Récupérez les images d'exemple (animaux, véhicules, nourriture, nature, bâtiments) ainsi que des fichiers HTML et PDF.

::

    $ bash bin/fetch-sample-images.sh

Lancez ensuite l'exploration depuis la console d'administration.

1. Connectez-vous à ``http://localhost:8080/admin/`` avec ``admin`` / ``admin`` et définissez un nouveau mot de passe si on vous le demande
2. Dans [Robot d'exploration] > [Web], cliquez sur [Créer nouveau], saisissez ``content`` dans « Nom » et ``http://content/`` dans « URL », puis cliquez sur [Créer]
3. Dans [Système] > [Planificateur], ouvrez « Default Crawler » et cliquez sur [Démarrer maintenant]
4. Dans [Informations système] > [Informations sur l'exploration], attendez la fin de l'exploration

Les vecteurs des images sont écrits pendant cette exploration.
Selon le README, les exemples fournis enregistrent 43 documents (37 images, 5 HTML, 1 PDF).
Ce nombre est indicatif.

Rechercher
----------

Ouvrez ``http://localhost:8080/`` et recherchez ``chien``, ``coucher de soleil sur la montagne`` ou ``mountain sunset``.
Le modèle par défaut est multilingue : des images sont renvoyées aussi bien en français qu'en anglais.

Le thème ``mosaic`` affiche les résultats sous forme de galerie de vignettes et attribue à chaque résultat un badge « Mot-clé », « Visuelle » ou « Mixte ».
« Visuelle » désigne la similarité d'image, et « Mixte » un résultat trouvé à la fois par mots-clés et par l'image.

Les vignettes sont générées par une tâche en arrière-plan après l'exploration.
Si certaines ne s'affichent pas juste après l'exploration, patientez un peu puis rechargez la page.

Pour arrêter, exécutez ``docker compose down``.
Les données restent sous ``./data``.

Vérifier le comportement
========================

Examiner ``searcher`` dans l'API de recherche
---------------------------------------------

Le champ ``searcher`` de la réponse de l'API de recherche indique si la recherche vectorielle a été utilisée.
Si ``jq`` est installé, exécutez la commande suivante.

::

    $ curl -s -G 'http://localhost:8080/api/v2/search' --data-urlencode 'q=chien' | jq -c '.response.data[] | {url, searcher}'

Les valeurs de ``searcher`` ont la signification suivante.

- ``["multi_modal"]`` : trouvé par similarité d'image
- ``["default"]`` : trouvé par la recherche par mots-clés
- Les deux : trouvé par les deux

Si tous les résultats n'ont que ``["default"]``, la recherche vectorielle n'a pas été exécutée.
Vérifiez si la recherche relève de l'un des cas de la section « Recherches où la recherche vectorielle ne s'exécute pas » ci-dessous.

Par défaut, ``searcher`` n'est pas inclus dans la réponse de l'API.
``docker-multimodalsearch`` définit ``query.additional.api.response.fields=searcher`` de ``fess_config.properties`` par une option de démarrage (``-Dfess.config.query.additional.api.response.fields=searcher``) ; le champ est donc inclus dans la réponse.
Pour le détail de l'API de recherche, consultez `API de recherche <https://fess.codelibs.org/fr/stable/api/api-search.html>`__.

Vérifier que les vecteurs ont été écrits
----------------------------------------

Si la recherche ne renvoie aucune image, comptez dans OpenSearch les documents qui possèdent des vecteurs (dans cet environnement, le port 9200 n'est utilisable que depuis l'hôte).

::

    $ curl -s 'http://localhost:9200/fess.search/_count' -H 'Content-Type: application/json' -d '{"query":{"nested":{"path":"content_chunk_vector","query":{"exists":{"field":"content_chunk_vector.vector"}}}}}'

Si ``count`` vaut 0, aucun vecteur n'a été créé lors de l'exploration.
Vérifiez dans ``docker compose logs fess01`` et dans les journaux du robot d'exploration si l'avertissement ``Failed to convert an image to a vector.`` apparaît.

Recherches où la recherche vectorielle ne s'exécute pas
-------------------------------------------------------

Dans les cas suivants, la recherche vectorielle n'est pas exécutée et les résultats proviennent uniquement de la recherche par mots-clés.
Aucune erreur n'est signalée : soyez donc attentif, car cela passe facilement inaperçu.

- Recherches avec un ordre de tri (paramètre ``sort``). Si vous définissez la « Valeur de tri par défaut » dans [Système] > [Général], le thème ``mosaic`` envoie cette valeur comme ``sort`` ; les recherches ordinaires relèvent alors aussi de ce cas
- Recherches utilisant une syntaxe de recherche dans le terme : phrase (``"coucher de soleil sur la montagne"``), caractère générique (``dog*``), pondération (``dog^2``), exclusion (``-dog``), ``allintitle:``, ``allinurl:``
- Recherches sans terme, avec seulement des conditions de filtrage comme les étiquettes
- Pages à partir du 101e résultat (lorsque la position de départ atteint au moins la moitié de ``rank.fusion.window_size`` (valeur par défaut 200))
- Lorsque le serveur CLIP est injoignable (``fess.log`` affiche un WARN tel que ``Embedding provider is unavailable``)

En revanche, si vous utilisez avec le terme de recherche une désignation de champ comme ``filetype:jpg`` ou un filtre par étiquette, la recherche vectorielle est bien exécutée et restreinte par cette condition.

Intégrer à un Fess existant
===========================

Pour l'intégrer à un Fess 15.9 existant sans passer par ``docker-multimodalsearch``, procédez comme suit.

1. Installer le plugin
----------------------

Installez ``fess-webapp-multimodal`` 15.9.x par l'une des méthodes suivantes, puis redémarrez Fess.

- Dans la console d'administration, [Système] > [Plugin] > [Installer]
- ``bin/fess-setup install plugin fess-webapp-multimodal:15.9.0``
- Avec Docker, ajoutez ``fess-webapp-multimodal:15.9.0`` à la variable d'environnement ``FESS_PLUGINS``

Pour plus de détails, consultez `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__.

2. Préparer un serveur CLIP
---------------------------

Le plugin se connecte à une API HTTP au même format que le serveur CLIP de Jina.
Il utilise ``POST /post`` pour la vectorisation et ``GET /health`` pour la vérification de la connexion.
Si ``/health`` ne renvoie pas de code 2xx, le plugin continue de fonctionner avec la recherche vectorielle désactivée.
La destination se définit avec ``content_chunker.embedding.clip.api.url`` ; sa valeur par défaut est ``http://localhost:51000``.

- Le ``docker/compose.yaml`` du dépôt du plugin démarre ``jinaai/clip-server``. Sa configuration ``docker/clip_config.yaml`` ne précise pas de modèle ; c'est donc le modèle par défaut qui est utilisé (ViT-B/32 à 512 dimensions selon le README). En outre, ce fichier Compose exige un GPU
- Pour utiliser des termes de recherche dans une autre langue que l'anglais (par exemple le français), préparez un serveur exécutant un modèle multilingue, comme le ``docker/clip-server`` de ``docker-multimodalsearch``

3. Configurer system.properties
-------------------------------

Les réglages de la recherche multimodale s'écrivent dans ``system.properties``.
Ce fichier se trouve dans ``app/WEB-INF/conf/system.properties`` pour la version ZIP, ``/etc/fess/system.properties`` pour les paquets RPM/DEB et ``/opt/fess/system.properties`` pour Docker.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=clip
    content_chunker.embedding.dimension=512
    content_chunker.embedding.clip.api.url=http://localhost:51000
    content_chunker.search.enabled=true

- Réglez ``content_chunker.embedding.dimension`` sur le nombre de dimensions produit par le modèle CLIP (512 pour la famille ViT-B/32)
- ``content_chunker.search.enabled`` n'est lu qu'au démarrage ; redémarrez donc Fess après l'avoir défini
- Pour passer les réglages en options de démarrage, utilisez ``-Dfess.system.<clé>``. S'ils sont écrits dans ``fess_config.properties`` ou sous forme ``-Dfess.config.<clé>``, ils sont ignorés, sans aucun avertissement
- Les valeurs de ``system.properties`` ont priorité sur ``-Dfess.system.*``. Si une clé figure aux deux endroits, c'est la valeur du fichier qui est utilisée
- Dans les fichiers Compose de docker-fess, ``fess01`` n'a pas de volume : ``docker compose down`` fait perdre ``system.properties``. Avec Docker, la méthode fiable consiste à lister ``-Dfess.system.<clé>=<valeur>`` dans la variable d'environnement ``FESS_JAVA_OPTS`` (c'est aussi ce que fait le ``compose.yaml`` de ``docker-multimodalsearch``)

Pour la liste des clés, consultez la section « Référence de configuration » de `Recherche sémantique (chunking de contenu + recherche vectorielle) <https://fess.codelibs.org/fr/stable/config/search-semantic.html>`__.
La recherche multimodale utilise les mêmes clés ``content_chunker.*``.

4. Recréer l'index
------------------

Le mapping du champ vectoriel ``content_chunk_vector`` est créé, lors de la création de l'index, avec le nombre de dimensions alors configuré.
Si vous avez démarré Fess ne serait-ce qu'une fois avant d'effectuer les réglages ci-dessus, exécutez la « Réindexation » dans [Informations système] > [Maintenance] en activant « Remplacer les alias ».
Pour plus de détails, consultez `Maintenance <https://fess.codelibs.org/fr/stable/admin/maintenance-guide.html>`__.

5. Activer les vignettes
------------------------

Dans une recherche d'images, sans vignettes, impossible de distinguer les résultats.
Les vignettes sont désactivées par défaut.

- Dans [Système] > [Général], activez « Afficher la miniature » et enregistrez
- La génération de vignettes pour les images, les PDF et les documents Office nécessite des outils externes comme ImageMagick. Ils ne sont pas inclus dans l'image Docker par défaut (Alpine) ; utilisez donc une image ``-noble`` (par exemple ``ghcr.io/codelibs/fess:15.9.0-noble``)

Pour les outils nécessaires, consultez `Configuration des vignettes <https://fess.codelibs.org/fr/stable/config/crawler-thumbnail.html>`__.

6. Explorer et vérifier
-----------------------

Explorez un site ou un dossier contenant des images GIF/JPEG/PNG.
Les vecteurs des images sont écrits lors de l'exploration.

Pour vérifier ``searcher`` dans l'API de recherche, définissez ``query.additional.api.response.fields=searcher`` dans ``fess_config.properties`` (ou ``-Dfess.config.query.additional.api.response.fields=searcher`` en option de démarrage).

Laissez désactivée la tâche « Content Chunk Vector Indexer » du planificateur (elle est désactivée par défaut).
C'est le robot d'exploration qui écrit les vecteurs des images ; cette tâche est donc inutile.
Si vous l'activez, les documents texte sont eux aussi vectorisés par la partie texte de CLIP, et le champ ``content`` est découpé.

Remarques pour l'exploitation
=============================

Incompatible avec la recherche sémantique sur le texte
------------------------------------------------------

Le plugin remplace le traitement de recherche de la recherche sémantique de Fess (``semanticChunkSearcher``) par un traitement dédié à CLIP.
De plus, ``content_chunker.embedding.name`` ne peut contenir qu'une seule valeur.
C'est pourquoi la recherche sémantique sur le texte de :doc:`guide-18` et la recherche multimodale ne peuvent pas être utilisées simultanément dans un même Fess.
Si vous avez besoin des deux, déployez des instances Fess distinctes.

Notez par ailleurs que si vous restreignez les traitements de recherche utilisés avec ``rank.fusion.searchers``, la recherche vectorielle est exclue si ``multi_modal`` n'y figure pas.
En temps normal, laissez ce réglage vide.

Aller jusqu'à la réexploration en cas de changement de modèle
-------------------------------------------------------------

Changez toujours le modèle et le nombre de dimensions ensemble.
Le nombre de dimensions est figé dans le mapping lors de la création de l'index ; après le changement, les étapes suivantes sont donc nécessaires.

1. Dans [Informations système] > [Maintenance], exécutez la « Réindexation » (avec « Remplacer les alias » activé) pour recréer l'index avec le nouveau nombre de dimensions
2. Relancez l'exploration

La réindexation ne fait que copier les documents ; elle ne recalcule pas les vecteurs.
Même à nombre de dimensions égal, changer de modèle ou de serveur CLIP modifie l'espace vectoriel : supprimez donc les documents, puis relancez l'exploration.
Dans ``docker-multimodalsearch``, modifiez ``CLIP_MODEL_NAME`` et ``MULTIMODAL_DIMENSION`` dans ``.env``.
La procédure figure dans la section « Model swap » du README.

CPU et GPU
----------

Le modèle par défaut de ``docker-multimodalsearch`` (512 dimensions) est prévu pour fonctionner sur le CPU, et ``CLIP_DEVICE=cpu`` est la valeur par défaut.
Si vous passez au modèle plus grand ``xlm-roberta-large-ViT-H-14::frozen_laion5b_s13b_b90k`` (1024 dimensions), un GPU est recommandé ; avec ``CLIP_DEVICE=auto``, le GPU est utilisé s'il est disponible.

Résumé
======

- ``fess-webapp-multimodal`` permet de rechercher des images GIF/JPEG/PNG à partir de texte. La recherche par image et la vectorisation des images intégrées aux documents ne sont pas possibles
- Pour l'essayer, utilisez ``v15.9.0`` de ``docker-multimodalsearch`` et indiquez ``FESS_THEMES_REF=15.9.x``
- Les réglages ``content_chunker.*`` s'écrivent dans ``system.properties`` (ou sous forme ``-Dfess.system.*``)
- Pour savoir si la recherche vectorielle a été utilisée, cherchez ``multi_modal`` dans ``searcher`` de l'API de recherche
- Les termes de recherche dans une autre langue que l'anglais (par exemple le français) nécessitent un modèle multilingue, et la recherche multimodale ne peut pas cohabiter avec la recherche sémantique sur le texte dans un même Fess

Articles suivants
=================

- :doc:`guide-18` — Rechercher des documents texte par vecteurs (configuration distincte de la recherche multimodale)
- :doc:`guide-02` — Les bases de l'exécution de Fess avec Docker
- :doc:`guide-11` — Intégrer Fess aux systèmes métier avec l'API de recherche

Références
==========

- `docker-multimodalsearch (v15.9.0) <https://github.com/codelibs/docker-multimodalsearch/tree/v15.9.0>`__
- `fess-webapp-multimodal (15.9.0) <https://github.com/codelibs/fess-webapp-multimodal/tree/fess-webapp-multimodal-15.9.0>`__
