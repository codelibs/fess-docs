==================================
Plugin Ingest
==================================

Vue d'ensemble
==============

Les plugins Ingest fournissent une fonctionnalité de traitement et de
transformation des données juste avant que les documents ne soient
enregistrés dans l'index. Chaque document récupéré lors du crawl passe
par les Ingester enregistrés avant d'être envoyé à l'index.

Cas d'utilisation
=================

- Normalisation du texte (conversion pleine largeur/demi-largeur,
  mise en forme des espaces, etc.)
- Ajout de métadonnées ou de champs personnalisés
- Masquage d'informations sensibles
- Conversion de valeurs (par exemple : décodage d'embeddings vectoriels
  encodés)

Classe Ingester
===============

La fonctionnalité Ingest s'implémente en héritant de la classe abstraite
``org.codelibs.fess.ingest.Ingester``. ``Ingester`` fournit des méthodes
``process`` appelées selon le type de crawl et l'étape de traitement.
Les implémentations par défaut renvoient toutes le ``target`` reçu tel
quel (elles ne font rien), il suffit donc de ne surcharger que les
méthodes nécessaires.

- ``protected Map<String, Object> process(Map<String, Object> target)``

  Point de délégation commun aux deux méthodes basées sur ``Map``. En la
  surchargeant, elle s'applique aux documents du crawl de datastore ainsi
  qu'à ceux du crawl Web/fichier (lors de l'enregistrement dans l'index).
  Pour de nombreux cas d'usage, surcharger uniquement cette méthode
  suffit.

- ``public Map<String, Object> process(Map<String, Object> target, DataStoreParams params)``

  Appelée lors du crawl de datastore. Par défaut, elle délègue à
  ``process(target)``.

- ``public Map<String, Object> process(Map<String, Object> target, AccessResult<String> accessResult)``

  Appelée lors de l'enregistrement dans l'index pour le crawl Web/fichier.
  Par défaut, elle délègue à ``process(target)``.

- ``public ResultData process(ResultData target, ResponseData responseData)``

  Appelée lors du traitement de la réponse pour le crawl Web/fichier
  (avant l'enregistrement du résultat d'accès). Par défaut, elle renvoie
  ``target`` tel quel.

Ordre d'exécution (priority)
----------------------------

Lorsque plusieurs Ingester sont enregistrés, ils s'exécutent par ordre
croissant du champ ``priority`` (les valeurs les plus petites en
premier). La valeur par défaut est ``99``. Elle peut être définie
directement dans le constructeur ou modifiée via ``setPriority(int)``.

.. code-block:: java

    public int getPriority()
    public void setPriority(final int priority)

Exemple d'implémentation
========================

Exemple de surcharge de ``process(Map<String, Object>)`` qui normalise
le contenu et ajoute un champ personnalisé :

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {

        public ExampleIngester() {
            // Définit l'ordre d'exécution (plus la valeur est petite, plus tôt l'exécution a lieu ; la valeur par défaut est 99)
            setPriority(50);
        }

        @Override
        protected Map<String, Object> process(final Map<String, Object> target) {
            // Normalisation du contenu
            final Object content = target.get("content");
            if (content instanceof String) {
                target.put("content", ((String) content).trim().replaceAll("\\s+", " "));
            }

            // Ajout d'un champ personnalisé
            target.put("ingested_by", ExampleIngester.class.getSimpleName());

            // Renvoie le document traité
            return target;
        }
    }

.. note::

    Si la méthode ``process`` renvoie ``null``, l'enregistrement dans
    l'index échoue. Comme il n'existe aucun mécanisme pour ignorer un
    document, veillez à toujours renvoyer ``target``.

Enregistrement
==============

Les Ingester s'enregistrent via le conteneur DI. Le plugin doit inclure
``fess_ingest++.xml``. Le suffixe ``++`` à la fin du nom de fichier
correspond à la convention de fusion qui ajoute la configuration au
fichier ``fess_ingest.xml`` du cœur de |Fess| (qui définit
``ingestFactory``, chargé de gérer les Ingester).

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleIngester"
                   class="org.codelibs.fess.ingest.example.ExampleIngester">
            <postConstruct name="register"/>
        </component>
    </components>

Grâce à ``<postConstruct name="register"/>``, ``Ingester#register()``
est appelée après la création du composant, ce qui l'enregistre
lui-même dans ``ingestFactory``.

Il n'existe aucun paramètre de configuration dans
``fess_config.properties`` pour la fonctionnalité Ingest. L'activation
ou la désactivation dépend de l'installation ou non du plugin, et
l'ordre d'exécution est contrôlé par ``priority``.

Flux d'exécution
================

Les Ingester sont appelés par ordre croissant de ``priority``, juste
avant que le document traité ne soit envoyé à l'index, aux emplacements
suivants :

- **Crawl de datastore** : ``process(Map, DataStoreParams)`` est
  appelée juste avant l'envoi du document.
- **Crawl Web/fichier (traitement de la réponse)** :
  ``process(ResultData, ResponseData)`` est appelée avant
  l'enregistrement du résultat du crawl.
- **Crawl Web/fichier (enregistrement dans l'index)** :
  ``process(Map, AccessResult)`` est appelée juste avant l'envoi du
  document.

Dans tous les cas, si un Ingester lève une exception, un message
d'avertissement est journalisé et le traitement se poursuit
(l'enregistrement du document dans l'index n'est pas interrompu).

.. note::

    Comme les Ingester sont enregistrés dans l'environnement
    d'exécution du crawler (``ingestFactory``), ils fonctionnent dans
    le cadre du traitement de crawl.

Implémentations de référence
=============================

À titre de référence pour l'implémentation, les plugins suivants sont
publiés sur GitHub par `CodeLibs <https://github.com/codelibs>`__ :

- ``fess-ingest-example`` - exemple d'implémentation minimale
- ``fess-webapp-multimodal`` - plugin contenant ``EmbeddingIngester``,
  qui décode les embeddings vectoriels

Informations complémentaires
=============================

- :doc:`plugin-architecture` - Architecture des plugins
