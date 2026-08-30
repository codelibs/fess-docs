===============
Connecteur JSON
===============

Aperçu
======

Le connecteur JSON fournit la fonctionnalité permettant de récupérer des données à partir de
fichiers JSON présents sur le système de fichiers local et de les enregistrer dans l'index
|Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-json``.

Il prend en charge les trois formats suivants ; par défaut, le format est déterminé
automatiquement à partir du contenu du fichier.

- Format JSON Lines (un objet JSON par ligne)
- Tableau d'objets JSON (mis en forme ou tenu sur une seule ligne, les deux étant possibles)
- Objet JSON unique

Comme les enregistrements sont lus un par un, même un tableau volumineux n'entraîne pas le
maintien de l'intégralité du fichier en mémoire.

.. note::

   Ce connecteur ne traite que les fichiers JSON présents sur le système de fichiers local.
   Il ne prend pas en charge la récupération distante via HTTP ou un autre protocole ; si le
   paramètre ``urls`` est spécifié, cela ne sera pas ignoré mais provoquera une erreur.

Prérequis
=========

1. L'installation du plugin est requise
2. L'accès au fichier JSON est nécessaire
3. La structure du JSON doit être connue

Installation du plugin
----------------------

Méthode 1 : Installation depuis l'interface d'administration

1. Ouvrir « Système » → « Plugins »
2. Téléverser le fichier JAR
3. Redémarrer |Fess|

Méthode 2 : Placement direct du fichier JAR

::

    # Télécharger depuis le dépôt CodeLibs
    wget https://maven.codelibs.org/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Placement
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # ou
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

.. note::

   À partir de la version 15.8.0, les fichiers JAR sont distribués via le
   `dépôt CodeLibs <https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-json/>`_.
   Pour les versions 15.7.0 et antérieures, ils se trouvent sur
   `Maven Central <https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/>`_.

Configuration
=============

Configurez depuis l'interface d'administration via « Crawler » → « Data Store » → « Nouveau ».

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple
   * - Nom
     - Products JSON
   * - Nom du gestionnaire
     - JsonDataStore
   * - Activé
     - Oui

Configuration des paramètres
----------------------------

Fichier local :

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

Fichiers multiples :

::

    files=/var/data/data1.json,/var/data/data2.json
    file_encoding=UTF-8

Spécification d'un répertoire :

::

    directories=/var/data/json_dir/
    file_encoding=UTF-8

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - Paramètre
     - Valeur par défaut
     - Description
   * - ``files``
     -
     - Chemins des fichiers JSON à traiter (plusieurs fichiers séparés par des virgules). Ils sont traités dans l'ordre indiqué.
   * - ``directories``
     -
     - Chemins des répertoires contenant des fichiers JSON (plusieurs répertoires séparés par des virgules).
   * - ``recursive``
     - ``false``
     - Indique si ``directories`` doit être parcouru y compris ses sous-répertoires.
   * - ``max_depth``
     - ``10``
     - Lorsque ``recursive=true``, nombre de niveaux de sous-répertoires à descendre pour chaque répertoire. La valeur ``0`` produit le même comportement que ``recursive=false``.
   * - ``include_pattern``
     -
     - Expression régulière à laquelle le chemin absolu du fichier doit correspondre entièrement.
   * - ``exclude_pattern``
     -
     - Expression régulière à laquelle le chemin absolu du fichier ne doit pas correspondre.
   * - ``file_suffixes``
     - ``.json,.jsonl``
     - Suffixes des fichiers ciblés (plusieurs suffixes séparés par des virgules). La casse n'est pas prise en compte.
   * - ``file_encoding``
     - ``UTF-8``
     - Encodage des caractères du fichier.
   * - ``format``
     - ``auto``
     - Format du document. L'une des valeurs suivantes : ``auto``, ``jsonl``, ``json``.
   * - ``root_path``
     -
     - JSON Pointer indiquant l'emplacement à partir duquel lire les enregistrements (exemple : ``/data/items``).

.. note::

   Les noms de paramètres sont indiqués ici en snake_case, mais leur équivalent en camelCase
   (par exemple ``fileEncoding`` pour ``file_encoding``) peut être utilisé de la même manière.

.. note::

   Spécifiez au moins l'un des paramètres ``files`` ou ``directories``.
   Si les deux sont vides, une erreur se produit.
   Les deux ne sont pas exclusifs l'un de l'autre : si les deux sont spécifiés, ils sont tous
   deux traités.
   Si un même fichier est atteint par les deux, il n'est lu qu'une seule fois.

Ordre d'exploration des fichiers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Les fichiers spécifiés via ``files`` sont traités dans l'ordre indiqué.
- Les fichiers trouvés sous ``directories`` sont traités par ordre croissant de date de
  dernière modification.
- Les fichiers spécifiés via ``files`` sont traités avant ceux trouvés sous ``directories``.

Le filtrage par ``file_suffixes`` s'applique également aux fichiers spécifiés directement via
``files``. Les fichiers dont le suffixe ne correspond pas sont ignorés, et la raison en est
indiquée dans le log.

Un chemin inexistant, un répertoire spécifié dans ``files``, ou un fichier spécifié dans
``directories`` sont, dans tous les cas, consignés dans le log comme avertissement, et le crawl
lui-même se poursuit.

``format``
----------

``auto`` lit le début du document et détermine le format à partir de sa syntaxe. Quel que soit
le format parmi les trois, cette méthode permet de le déterminer correctement dès lors que le
fichier est correctement écrit.

Il convient de spécifier explicitement ``format=jsonl`` lorsqu'il s'agit d'un fichier au format
JSON Lines dont les lignes situées près du début risquent d'être corrompues (ligne de bannière,
log de progression, enregistrement interrompu en cours de transfert, etc.). En effet, la
détection automatique doit pouvoir ignorer de telles lignes pour effectuer son jugement.

Ce paramètre détermine également l'étendue de l'impact d'un enregistrement invalide.

- **Format JSON Lines** : chaque ligne est analysée indépendamment, de sorte que le coût d'une
  ligne invalide se limite à cette seule ligne. L'échec est enregistré dans les URL en échec
  sous la clé ``<chemin absolu du fichier>@<numéro de ligne>``, et le traitement se poursuit
  normalement à partir de la ligne suivante.
- **Autres formats** : comme la lecture se fait sous forme de flux de jetons, un seul échec
  peut entraîner celui des enregistrements suivants. Un document interrompu au milieu d'un
  objet ne peut pas être récupéré, et si un nombre défini d'échecs consécutifs se produit, le
  traitement du fichier est interrompu avec un avertissement.

``root_path``
-------------

Spécifier un JSON Pointer désignant un tableau imbriqué permet d'enregistrer chacun de ses
éléments comme un enregistrement.

::

    root_path=/data/items

.. code-block:: json

    { "meta": { "count": 2 }, "data": { "items": [ { "id": "1" }, { "id": "2" } ] } }

- Si le pointeur désigne un tableau, chacun de ses éléments constitue un enregistrement.
- Si le pointeur désigne un objet, cet objet constitue un unique enregistrement.
- Si aucune correspondance n'est trouvée, il n'y a pas d'erreur ; le nombre d'enregistrements
  est simplement de 0.
- Les séquences d'échappement du JSON Pointer sont prises en charge (``~1`` pour ``/``, ``~0``
  pour ``~``).

``root_path`` est prioritaire sur ``format``. En effet, un document atteint via un JSON Pointer
n'est pas lu ligne par ligne ; si ``root_path`` est spécifié en même temps que
``format=jsonl``, un avertissement à ce sujet est consigné dans le log.

.. warning::

   ``root_path`` doit commencer par ``/``. Si le ``/`` initial est omis, comme dans
   ``data/items``, la valeur ne peut pas être interprétée comme un JSON Pointer et l'ensemble
   de la configuration Data Store échoue.
   Dans ce cas, l'URL en échec est enregistrée non pas sous le nom du paramètre mais sous celui
   de la configuration Data Store ; déterminez quel paramètre en est la cause à partir du
   message ``JSON Pointer expression must start with '/'`` figurant dans le log.

.. note::

   Si vous lisez, sans spécifier ``root_path``, un document mis en forme sur plusieurs lignes
   dont les enregistrements font partie d'une structure englobante (dite « wrapper »,
   contenant par exemple des métadonnées ainsi qu'un tableau), l'analyse ligne par ligne est
   tentée, ce qui empêche d'obtenir les enregistrements attendus et provoque l'enregistrement
   d'échecs.
   Pour ce type de document, spécifiez ``root_path``.

Configuration du script
-----------------------

Les valeurs de chaque champ sont construites en référençant les valeurs des champs de l'objet
JSON. Les champs de premier niveau de l'objet JSON sont accessibles directement dans le script
en tant que **variables sans préfixe** (sans préfixe ``data.`` ni autre).

Objet JSON simple :

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description
    digest=description
    host="shop.example.com"
    site="shop.example.com"

Les objets imbriqués sont accessibles comme des maps, et les tableaux imbriqués comme des
listes :

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    first_tag=tags[0]

Champs disponibles
~~~~~~~~~~~~~~~~~~

- ``<nom_du_champ>`` — Référence directe par le nom d'un champ de premier niveau de l'objet
  JSON
- ``<parent>.<enfant>`` — Champ d'un objet imbriqué
- ``<tableau>[<index>]`` — Élément d'un tableau

.. note::

   Si la valeur d'un champ vaut ``null``, ce champ n'est pas enregistré dans le document.

.. note::

   Dans |Fess| 15.9, le moteur de script intégré est devenu JavaScript.
   Groovy est fourni sous forme de plugin ``fess-script-groovy``.
   Le moteur à utiliser est indiqué via le paramètre de la configuration Data Store
   ``script_type`` (par exemple ``script_type=javascript``). Si ce paramètre est omis,
   ``groovy`` est utilisé.
   Les références simples et les concaténations de chaînes telles que dans les exemples
   ci-dessus fonctionnent de la même manière avec les deux moteurs, mais les autres notations
   diffèrent selon le moteur.

Remarques
=========

Un paramètre dont le nom correspond à ``app.encrypt.property.pattern`` (par défaut, les
paramètres se terminant par ``password``, ``key``, ``token`` ou ``secret``) est référencé
depuis le script comme valant ``null``. Cela permet d'éviter que des identifiants inscrits dans
les paramètres de la configuration Data Store ne soient copiés dans un champ de l'index.

Si un champ de même nom existe côté enregistrement, la valeur de l'enregistrement est
prioritaire, comme pour les autres paramètres.

.. note::

   La correspondance porte sur une égalité exacte, sensible à la casse, avec le nom du
   paramètre. ``access_token`` est concerné, mais pas son équivalent en camelCase
   ``accessToken``. Si vous inscrivez des identifiants dans un paramètre, utilisez le
   snake_case.

Paramètres incorrects et erreurs
================================

Si une valeur non valide est spécifiée pour ``format``, ``include_pattern``,
``exclude_pattern`` ou ``urls``, le crawl se termine avant même la lecture des fichiers, et une
URL en échec incluant le nom du paramètre concerné (exemple : ``JsonDataStore:format``) est
enregistrée.

Si une valeur non numérique est spécifiée pour ``max_depth``, cela est consigné dans le log et
la valeur par défaut est utilisée.

.. note::

   Le crawl d'une configuration Data Store se termine comme un job normal même si aucun élément
   n'a pu être récupéré. Si le nombre d'éléments récupérés diffère de ce qui était attendu,
   vérifiez le nombre de documents dans l'index, les URL en échec, ainsi que le fichier
   ``fess-crawler.log``.

Exemples d'utilisation
======================

Catalogue de produits
---------------------

Paramètres :

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

Script :

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description
    digest=category
    host="shop.example.com"
    site="shop.example.com"

Fichier de réponse d'API enregistrée
------------------------------------

Paramètres :

::

    files=/var/data/response.json
    root_path=/data/items

Script :

::

    url="https://example.com/item/" + id
    title=title
    content=body
    host="example.com"
    site="example.com"

Traitement récursif d'un répertoire
-----------------------------------

Paramètres :

::

    directories=/var/data/exports
    recursive=true
    max_depth=3
    include_pattern=.*\.jsonl
    file_encoding=UTF-8

Dépannage
=========

Fichier introuvable
-------------------

**Symptôme** : le log affiche ``... does not exist.``, ``... is not a file.`` ou
``... is skipped because its suffix is not one of ...``

**Points à vérifier** :

1. Vérifier que le chemin du fichier est correct
2. Vérifier que le fichier existe
3. Vérifier que le suffixe du fichier correspond à ``file_suffixes`` (par défaut ``.json`` ou
   ``.jsonl``)
4. Vérifier que l'utilisateur exécutant |Fess| dispose des droits de lecture

Erreur d'analyse JSON
---------------------

**Symptôme** : le log affiche ``Failed to parse ...`` ou ``Failed to read ...``, ou une URL en
échec est enregistrée

**Points à vérifier** :

1. Vérifier que le fichier est un JSON valide

   ::

       # Pour un fichier au format JSON Lines, vérifier que chaque ligne est un objet JSON valide
       cat data.jsonl | jq -c .

       # Pour un tableau ou un objet unique
       jq . data.json

2. Vérifier que l'encodage des caractères est correct
3. Vérifier que le fichier n'est pas interrompu en cours de route
4. Vérifier qu'il ne contient pas de commentaires (les commentaires ne sont pas autorisés par
   le standard JSON)

Impossible de récupérer les données
-----------------------------------

**Symptôme** : le crawl réussit mais le nombre d'éléments est 0

**Points à vérifier** :

1. Si ``root_path`` est spécifié, vérifier que ce JSON Pointer correspond à la structure du
   document (si ce n'est pas le cas, il n'y a pas d'erreur, mais le nombre d'éléments est de 0)
2. Vérifier que ``include_pattern``, ``exclude_pattern`` et ``file_suffixes`` n'excluent pas la
   totalité des fichiers ciblés. Dans ce cas, le log affiche ``No sources to process``
3. Vérifier que la configuration du script est correcte (les références de champs doivent être
   sans préfixe ``data.``)
4. Vérifier que les noms de champs sont corrects (y compris la casse)
5. Vérifier que ``url`` est bien construit. Si ``url`` est vide, chaque enregistrement concerné
   est comptabilisé comme un échec

Caractères illisibles
---------------------

**Symptôme** : les caractères du document enregistré sont corrompus

Si vous spécifiez pour ``file_encoding`` un encodage qui existe réellement mais qui est
incorrect, il n'y a pas d'erreur : le document est enregistré tel quel, avec des caractères
corrompus. Vérifiez l'encodage réel du fichier. Si vous spécifiez un nom d'encodage qui
n'existe pas, une URL en échec est enregistrée pour chaque fichier concerné.

Fichiers JSON volumineux
------------------------

**Symptôme** : mémoire insuffisante ou timeout

Comme les enregistrements sont lus un par un, la taille totale du fichier n'a pas d'impact
direct sur la consommation de mémoire. Cependant, un problème peut survenir si un enregistrement
est extrêmement volumineux, ou si la charge liée à l'indexation est élevée.

**Solution** :

1. Diviser le fichier JSON en plusieurs fichiers
2. Augmenter la taille du tas de |Fess|

Informations de référence
=========================

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-csv` - Connecteur CSV
- :doc:`ds-database` - Connecteur de base de données
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `JSON Pointer (RFC 6901) <https://datatracker.ietf.org/doc/html/rfc6901>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
