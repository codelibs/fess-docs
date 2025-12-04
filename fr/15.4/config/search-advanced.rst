===========
Paramètres liés à la recherche
===========

Les paramètres décrits ci-dessous sont spécifiés dans fess_config.properties.
Un redémarrage de |Fess| est nécessaire après modification.

Recherche floue
=========

Une recherche floue est appliquée aux mots-clés de 4 caractères ou plus, ce qui permet de trouver des correspondances avec une différence d'un caractère.
Pour désactiver ce paramètre, spécifiez `-1`.
::

    query.boost.fuzzy.min.length=-1

Valeur du délai d'expiration lors de la recherche
=================

Vous pouvez spécifier la valeur du délai d'expiration lors de la recherche.
La valeur initiale est de 10 secondes.
::

    query.timeout=10000

Nombre maximum de caractères lors de la recherche
==============

Vous pouvez spécifier le nombre maximum de caractères lors de la recherche.
La valeur initiale est de 1000 caractères.
::

    query.max.length=1000

Sortie des journaux lors d'un délai d'expiration de recherche
=======================

Paramètre de sortie des journaux en cas de délai d'expiration lors de la recherche.
La valeur initiale est `true (activé)`.
::

    query.timeout.logging=true

Affichage du nombre de correspondances
===========

À spécifier lorsqu'un affichage du nombre de correspondances supérieur à 10 000 est nécessaire.
Par défaut, lorsque plus de 10 000 résultats sont trouvés, l'affichage est le suivant :

`Résultats de recherche pour xxxxx environ 10 000 ou plus 1 - 10 sur (4.94 secondes)`

::

    query.track.total.hits=10000

Nom de l'index lors de la recherche par géolocalisation
=======================

Spécifie le nom de l'index lors de la recherche par géolocalisation.
La valeur initiale est `location`.
::

    query.geo.fields=location

Spécification de langue dans les paramètres de requête
=======================

Spécifie le nom du paramètre pour spécifier la langue dans les paramètres de requête.
Par exemple, en passant `browser_lang=en` dans l'URL comme paramètre de requête, la langue d'affichage de l'écran passe à l'anglais.
::

    query.browser.lang.parameter.name=browser_lang

Spécification de la recherche par préfixe
==============

Lors d'une recherche de correspondance exacte, si spécifiée avec `〜\*`, effectue une recherche par préfixe.
La valeur initiale est `true (activé)`.
::

    query.replace.term.with.prefix.query=true

Chaînes de mise en surbrillance
==============

Les phrases sont délimitées par les chaînes spécifiées ici pour obtenir un affichage de surbrillance naturel.
Les chaînes spécifiées sont des caractères Unicode avec u comme délimiteur de début.
::

    query.highlight.terminal.chars=u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61

La valeur initiale est définie comme suit (après décodage) :

``! , . ? ։ ؟ ۔ ܀ ܁ ܂ । ၊ ။ ። ፧ ፨ ᙮ ᠃ ᠉ ‼ ‽ ⁇ ⁈ ⁉ 。 ﹒ ﹗ ！ ． ？ ｡``

Fragments de mise en surbrillance
==================

Spécifie le nombre de caractères des fragments de mise en surbrillance récupérés d'OpenSearch et le nombre de fragments.
::

    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

Méthode de génération de la mise en surbrillance
==============

Spécifie la méthode de génération de la mise en surbrillance dans OpenSearch.
::

    query.highlight.type=fvh

Balises cibles de mise en surbrillance
===============

Spécifie les balises de début et de fin des cibles de mise en surbrillance.
::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>

Valeurs transmises au surligneur d'OpenSearch
===========================

Spécifie les valeurs transmises au surligneur d'OpenSearch.
::

    query.highlight.boundary.chars=u0009u000Au0013u0020
    query.highlight.boundary.max.scan=20
    query.highlight.boundary.scanner=chars
    query.highlight.encoder=default

Noms de champs à ajouter à la réponse
========================

Spécifie les noms de champs à ajouter à la réponse lors d'une recherche normale ou d'une recherche API.
::

    query.additional.response.fields=
    query.additional.api.response.fields=

Ajout de noms de champs
==============

À spécifier lors de l'ajout de noms de champs de recherche ou de noms de champs de facettes.
::

    query.additional.search.fields=
    query.additional.facet.fields=

Paramètres pour obtenir les résultats de recherche au format XML compatible GSA
===================================

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
