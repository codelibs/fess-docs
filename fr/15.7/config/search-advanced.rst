==========================================
Paramètres avancés liés à la recherche
==========================================

Les paramètres décrits ci-dessous sont spécifiés dans fess_config.properties.
Un redémarrage de |Fess| est nécessaire après modification.

Recherche floue
===============

Une recherche floue est appliquée aux mots-clés de 4 caractères ou plus, ce qui permet de trouver des correspondances avec une différence d'un caractère.
Pour désactiver ce paramètre, spécifiez ``-1``.
::

    query.boost.fuzzy.min.length=-1

La valeur initiale est ``4``. Pour les paramètres détaillés de la recherche floue, consultez la section « Paramètres de pertinence (boost) » ci-dessous.

Valeur du délai d'expiration lors de la recherche
==================================================

Vous pouvez spécifier la valeur du délai d'expiration lors de la recherche en millisecondes.
La valeur initiale est de 10 secondes (10000 millisecondes).
::

    query.timeout=10000

Nombre maximum de caractères lors de la recherche
==================================================

Vous pouvez spécifier le nombre maximum de caractères de la requête de recherche.
Les requêtes dont la longueur dépasse cette valeur ne sont pas acceptées.
La valeur initiale est de 1000 caractères.
::

    query.max.length=1000

Journalisation du délai d'expiration lors de la recherche
==========================================================

Paramètre de journalisation en cas de délai d'expiration lors de la recherche.
La valeur initiale est ``true`` (activé).
::

    query.timeout.logging=true

Affichage du nombre de correspondances
=======================================

Spécifie la limite supérieure du nombre de correspondances comptabilisé avec précision.
Par défaut, lorsque plus de 10 000 résultats sont trouvés, l'affichage est le suivant :

``Résultats de recherche pour xxxxx environ 10 000 ou plus 1 - 10 sur (4.94 secondes)``

Si l'affichage du nombre exact de correspondances supérieur à 10 000 est nécessaire, spécifiez une valeur plus grande.
::

    query.track.total.hits=10000

.. note::
   La définition d'une valeur élevée peut affecter les performances de recherche. Définissez une valeur appropriée en fonction de l'utilisation.

Décalage maximum des résultats de recherche
============================================

Spécifie la limite supérieure du décalage (position de départ de la recherche) pouvant être obtenu comme résultat de recherche.
Si un décalage supérieur à cette valeur est spécifié, la recherche génère une erreur.
Cette valeur fonctionne comme limite supérieure lors de la navigation vers des pages profondes par pagination.
La valeur initiale est 100000.
::

    query.max.search.result.offset=100000

Seuil de relance de recherche par opérateur OR
===============================================

Si le nombre de correspondances lors d'une recherche normale est inférieur ou égal à la valeur spécifiée ici, la recherche est relancée avec l'opérateur OR.
Cela permet de compléter les résultats même lorsque la recherche AND renvoie peu de correspondances.
La valeur initiale est ``-1``, ce qui désactive cette fonctionnalité.
::

    query.orsearch.min.hit.count=-1

Nom du champ lors de la recherche par géolocalisation
======================================================

Spécifie le nom du champ cible lors de la recherche par géolocalisation.
Pour spécifier plusieurs champs, séparez-les par des virgules.
La valeur initiale est ``location``.
::

    query.geo.fields=location

Pour plus d'informations sur l'utilisation de la recherche par géolocalisation, consultez :doc:`search-geosearch`.

Spécification de langue dans les paramètres de requête
=======================================================

Spécifie le nom du paramètre pour définir la langue dans les paramètres de requête.
Par exemple, en passant ``browser_lang=en`` dans l'URL comme paramètre de requête, la langue d'affichage de l'écran passe à l'anglais.
::

    query.browser.lang.parameter.name=browser_lang

Langue par défaut pour la recherche
=====================================

Spécifie la langue par défaut ciblée lors de la recherche, séparée par des virgules.
Si une valeur est définie, elle est utilisée en priorité par rapport à la langue du paramètre de requête ou du navigateur.
La valeur initiale est vide (non spécifiée), et la langue du paramètre de requête ou du navigateur est utilisée.
::

    query.default.languages=

Correspondance des codes de langue
====================================

Spécifie la correspondance de normalisation des codes de langue utilisés lors de la recherche.
Convertit les codes de langue transmis par le navigateur ou la requête vers les codes de langue utilisés en interne par |Fess|.
En règle générale, aucune modification n'est nécessaire. Les correspondances des principales langues sont définies dans les valeurs initiales.
::

    query.language.mapping=\
    ar=ar\n\
    bg=bg\n\
    ...

Spécification de la recherche par préfixe
==========================================

Si le terme de recherche est suivi de ``*`` (ex. : ``recherche*``), ce terme est recherché en tant que requête de préfixe.
La valeur initiale est ``true`` (activé). En spécifiant ``false``, les termes se terminant par ``*`` sont recherchés tels quels.
::

    query.replace.term.with.prefix.query=true

Chaînes de mise en surbrillance
=================================

Les phrases sont délimitées par les chaînes spécifiées ici pour obtenir un affichage de surbrillance naturel.
Les chaînes spécifiées sont des caractères Unicode avec u comme délimiteur de début.
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

La valeur initiale est définie comme suit (après décodage) :

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

Fragments de mise en surbrillance
==================================

Spécifie le nombre de caractères des fragments de mise en surbrillance récupérés d'OpenSearch et le nombre de fragments.
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

Méthode de génération de la mise en surbrillance
=================================================

Spécifie la méthode de génération de la mise en surbrillance dans OpenSearch.
::

    query.highlight.type=fvh

Balises cibles de mise en surbrillance
=======================================

Spécifie les balises de début et de fin des cibles de mise en surbrillance.
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

Valeurs transmises au surligneur d'OpenSearch
==============================================

Spécifie les valeurs transmises au surligneur d'OpenSearch.
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

Paramètres avancés de surlignage
==================================

Paramètres pour contrôler le comportement détaillé du surlignage.
::

    query.highlight.force.source=false
    query.highlight.fragmenter=span
    query.highlight.fragment.offset=-1
    query.highlight.no.match.size=0
    query.highlight.order=score
    query.highlight.phrase.limit=256
    query.highlight.content.description.fields=hl_content,digest
    query.highlight.boundary.position.detect=true
    query.highlight.text.fragment.type=query
    query.highlight.text.fragment.size=3
    query.highlight.text.fragment.prefix.length=5
    query.highlight.text.fragment.suffix.length=5

Noms de champs à ajouter à la réponse
=======================================

Spécifie les noms de champs à ajouter à la réponse lors d'une recherche normale ou d'une recherche API.
Correspond respectivement à la réponse lors d'une recherche normale, d'une recherche API (JSON/GSA), d'une recherche par défilement et de l'affichage du cache.
::

    query.additional.response.fields=
    query.additional.api.response.fields=
    query.additional.scroll.response.fields=
    query.additional.cache.response.fields=

Pour plus de détails sur les champs de réponse de la recherche par défilement, consultez :doc:`search-scroll`.

Ajout de noms de champs
=========================

À spécifier lors de l'ajout de noms de champs de recherche, de noms de champs de facettes, de noms de champs de tri, etc.
::

    query.additional.default.fields=
    query.additional.search.fields=
    query.additional.facet.fields=
    query.additional.sort.fields=
    query.additional.highlighted.fields=
    query.additional.analyzed.fields=
    query.additional.not.analyzed.fields=

La signification de chaque paramètre est la suivante :

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Paramètre
     - Description
   * - ``query.additional.default.fields``
     - Ajoute aux champs par défaut ciblés par les requêtes sans spécification de champ.
   * - ``query.additional.search.fields``
     - Ajoute aux champs pouvant être recherchés avec une spécification de champ.
   * - ``query.additional.facet.fields``
     - Ajoute aux champs pouvant être utilisés comme facettes.
   * - ``query.additional.sort.fields``
     - Ajoute aux champs pouvant être utilisés comme critères de tri.
   * - ``query.additional.highlighted.fields``
     - Ajoute aux champs ciblés par la mise en surbrillance.
   * - ``query.additional.analyzed.fields``
     - Ajoute aux champs traités comme sujets à l'analyse par l'Analyzer.
   * - ``query.additional.not.analyzed.fields``
     - Ajoute aux champs non soumis à l'analyse par l'Analyzer.

Regroupement (collapse) des documents similaires
=================================================

Paramètres de la fonctionnalité collapse qui regroupe les documents similaires (quasi-doublons) par le champ ``content_minhash_bits``.
``query.collapse.inner.hits.name`` est le nom du champ dans les résultats de recherche où sont stockés les documents similaires,
``query.collapse.inner.hits.size`` est le nombre de documents similaires récupérés par groupe (``0`` signifie aucune récupération),
``query.collapse.inner.hits.sorts`` est la condition de tri lors de la récupération des documents similaires,
``query.collapse.max.concurrent.group.results`` représente le nombre maximum de requêtes simultanées lors de la récupération des groupes.
::

    query.collapse.max.concurrent.group.results=4
    query.collapse.inner.hits.name=similar_docs
    query.collapse.inner.hits.size=0
    query.collapse.inner.hits.sorts=

Préférence de recherche
========================

Spécifie la préférence (valeur déterminant le shard sur lequel effectuer la recherche) transmise à OpenSearch lors d'une recherche API au format JSON.
En spécifiant ``_query``, la valeur de hachage de la requête de recherche est utilisée comme préférence, ce qui oriente les requêtes identiques vers le même shard.
La valeur initiale est ``_query``.
::

    query.json.default.preference=_query

Paramètres de pertinence (boost)
==================================

Spécifie les valeurs de boost utilisées pour le calcul de la pertinence (score) lors de la recherche.
Les paramètres avec ``.lang`` correspondent aux valeurs de boost pour les champs par langue (ex. : ``content_ja``).
::

    query.boost.title=0.5
    query.boost.title.lang=1.0
    query.boost.content=0.05
    query.boost.content.lang=0.1
    query.boost.important_content=-1.0
    query.boost.important_content.lang=-1.0

Les valeurs de boost et le comportement de la recherche floue sont spécifiés ci-dessous.
``query.boost.fuzzy.min.length`` est le nombre minimum de caractères pour appliquer la recherche floue (``-1`` pour désactiver).
::

    query.boost.fuzzy.min.length=4
    query.boost.fuzzy.title=0.01
    query.boost.fuzzy.title.fuzziness=AUTO
    query.boost.fuzzy.title.expansions=10
    query.boost.fuzzy.title.prefix_length=0
    query.boost.fuzzy.title.transpositions=true
    query.boost.fuzzy.content=0.005
    query.boost.fuzzy.content.fuzziness=AUTO
    query.boost.fuzzy.content.expansions=10
    query.boost.fuzzy.content.prefix_length=0
    query.boost.fuzzy.content.transpositions=true

Paramètres du type de requête
===============================

Spécifie le type de requête utilisé lors de la recherche et son comportement détaillé.
``query.default.query_type`` est le type de requête utilisé par défaut,
``query.dismax.tie_breaker`` est la valeur du tie breaker pour la requête dismax,
``query.bool.minimum_should_match`` est la valeur minimum_should_match pour la requête bool (non spécifiée si vide).
::

    query.default.query_type=bool
    query.dismax.tie_breaker=0.1
    query.bool.minimum_should_match=

Paramètres détaillés de la recherche par préfixe et de la recherche floue
==========================================================================

Spécifie le comportement détaillé des requêtes de préfixe et des requêtes floues.
::

    query.prefix.expansions=50
    query.prefix.slop=0
    query.fuzzy.prefix_length=0
    query.fuzzy.expansions=50
    query.fuzzy.transpositions=true

Paramètres des facettes
========================

Spécifie le comportement par défaut de la recherche par facettes.
``query.facet.fields`` est le champ cible des facettes,
``query.facet.fields.size`` est la limite supérieure du nombre de facettes récupérées,
``query.facet.fields.min_doc_count`` est le nombre minimum de documents à afficher dans les facettes,
``query.facet.fields.sort`` est l'ordre de tri des facettes,
``query.facet.fields.missing`` est la valeur attribuée aux documents sans valeur.
::

    query.facet.fields=label
    query.facet.fields.size=100
    query.facet.fields.min_doc_count=1
    query.facet.fields.sort=count.desc
    query.facet.fields.missing=

Paramètres pour obtenir les résultats de recherche au format XML compatible GSA
================================================================================

Utilisé lors de l'obtention des résultats de recherche au format XML compatible GSA.

Spécifie les noms de champs à ajouter à la réponse lors de l'utilisation du format XML compatible GSA.
    ::

        query.gsa.response.fields=UE,U,T,RK,S,LANG

Spécifie la langue lors de l'utilisation du format XML compatible GSA.
    ::

        query.gsa.default.lang=en

Spécifie le tri par défaut lors de l'utilisation du format XML compatible GSA.
    ::

        query.gsa.default.sort=

Spécifie le préfixe des métadonnées lors de l'utilisation du format XML compatible GSA.
    ::

        query.gsa.meta.prefix=MT_

Spécifie le champ charset lors de l'utilisation du format XML compatible GSA.
    ::

        query.gsa.index.field.charset=charset

Spécifie le champ content_type lors de l'utilisation du format XML compatible GSA.
    ::

        query.gsa.index.field.content_type.=content_type

Spécifie la préférence par défaut lors de l'utilisation du format XML compatible GSA.
    ::

        query.gsa.default.preference=_query
