========================
Guide de contribution
========================

Nous accueillons les contributions au projet |Fess| !
Cette page explique comment contribuer à |Fess|, les directives communautaires,
les procédures de création de pull requests, etc.

.. contents:: Table des matières
   :local:
   :depth: 2

Introduction
======

|Fess| est un projet open source,
qui se développe grâce aux contributions de la communauté.
Tout le monde peut contribuer, quel que soit son niveau d'expérience en programmation.

Méthodes de contribution
========

Vous pouvez contribuer à |Fess| de diverses manières.

Contributions de code
----------

- Ajout de nouvelles fonctionnalités
- Correction de bugs
- Amélioration des performances
- Refactoring
- Ajout de tests

Contributions à la documentation
----------------

- Amélioration des manuels utilisateur
- Ajout et mise à jour de la documentation API
- Création de tutoriels
- Traduction

Rapport de problèmes
-----------

- Rapports de bugs
- Demandes de fonctionnalités
- Questions et suggestions

Activités communautaires
--------------

- Discussions sur GitHub Discussions
- Répondre aux questions sur le forum
- Rédaction d'articles de blog et de tutoriels
- Présentations lors d'événements

Première contribution
==========

Si vous contribuez à |Fess| pour la première fois, nous vous recommandons les étapes suivantes.

Étape 1 : Comprendre le projet
---------------------------

1. Consultez les informations de base sur le `site officiel de Fess <https://fess.codelibs.org/ja/>`__
2. Comprenez l'aperçu du développement dans :doc:`getting-started`
3. Apprenez la structure du code dans :doc:`architecture`

Étape 2 : Trouver un problème
-------------------

Sur la `page des problèmes GitHub <https://github.com/codelibs/fess/issues>`__, recherchez
les problèmes avec l'étiquette ``good first issue``.

Ces problèmes sont des tâches relativement simples adaptées aux nouveaux contributeurs.

Étape 3 : Configurer l'environnement de développement
----------------------------

Configurez l'environnement de développement en suivant :doc:`setup`.

Étape 4 : Créer une branche et travailler
----------------------------

Créez une branche et commencez le codage en suivant :doc:`workflow`.

Étape 5 : Créer une pull request
--------------------------

Commitez les modifications et créez une pull request.

Conventions de codage
==============

|Fess| suit les conventions de codage suivantes pour maintenir un code cohérent.

Style de codage Java
----------------------

Style de base
~~~~~~~~~~

- **Indentation** : 4 espaces
- **Code de fin de ligne** : LF (style Unix)
- **Encodage** : UTF-8
- **Longueur de ligne** : 120 caractères maximum recommandé

Conventions de nommage
~~~~~~

- **Packages** : minuscules, séparés par des points (ex : ``org.codelibs.fess``)
- **Classes** : PascalCase (ex : ``SearchService``)
- **Interfaces** : PascalCase (ex : ``Crawler``)
- **Méthodes** : camelCase (ex : ``executeSearch``)
- **Variables** : camelCase (ex : ``searchResult``)
- **Constantes** : UPPER_SNAKE_CASE (ex : ``MAX_SEARCH_SIZE``)

Commentaires
~~~~~~

**Javadoc:**

Écrivez Javadoc pour les classes, méthodes et champs publics.

.. code-block:: java

    /**
     * Exécute une recherche.
     *
     * @param query Requête de recherche
     * @return Résultats de recherche
     * @throws SearchException En cas d'échec de la recherche
     */
    public SearchResponse executeSearch(String query) throws SearchException {
        // Implémentation
    }

**Commentaires d'implémentation:**

Ajoutez des commentaires en japonais ou en anglais pour une logique complexe.

.. code-block:: java

    // Normalisation de la requête (conversion pleine chasse en demi-chasse)
    String normalizedQuery = QueryNormalizer.normalize(query);

Conception des classes et méthodes
~~~~~~~~~~~~~~~~~~~~

- **Principe de responsabilité unique** : Une classe n'a qu'une seule responsabilité
- **Petites méthodes** : Une méthode ne fait qu'une seule chose
- **Noms significatifs** : Les noms de classes et de méthodes doivent être clairs dans leur intention

Gestion des exceptions
~~~~~~

.. code-block:: java

    // Bon exemple : Gestion appropriée des exceptions
    try {
        executeSearch(query);
    } catch (IOException e) {
        logger.error("Une erreur s'est produite lors de la recherche", e);
        throw new SearchException("L'exécution de la recherche a échoué", e);
    }

    // Exemple à éviter : Bloc catch vide
    try {
        executeSearch(query);
    } catch (IOException e) {
        // Ne fait rien
    }

Gestion de null
~~~~~~~~~

- Ne pas retourner ``null`` dans la mesure du possible
- Utilisation d'``Optional`` recommandée
- Indiquer explicitement la possibilité de null avec l'annotation ``@Nullable``

.. code-block:: java

    // Bon exemple
    public Optional<User> findUser(String id) {
        return Optional.ofNullable(userMap.get(id));
    }

    // Exemple d'utilisation
    findUser("123").ifPresent(user -> {
        // Traitement si l'utilisateur existe
    });

Rédaction de tests
~~~~~~~~~~

- Écrire des tests pour toutes les méthodes publiques
- Les noms de méthodes de test commencent par ``test``
- Utiliser le modèle Given-When-Then

.. code-block:: java

    @Test
    public void testSearch() {
        // Given: Conditions préalables du test
        SearchService service = new SearchService();
        String query = "test";

        // When: Exécution du sujet du test
        SearchResponse response = service.search(query);

        // Then: Vérification des résultats
        assertNotNull(response);
        assertEquals(10, response.getDocuments().size());
    }

Directives de revue de code
========================

Processus de revue des pull requests
----------------------------

1. **Vérification automatique** : CI exécute automatiquement la compilation et les tests
2. **Revue de code** : Les mainteneurs examinent le code
3. **Retour d'information** : Demandes de modifications si nécessaire
4. **Approbation** : La revue est approuvée
5. **Fusion** : Les mainteneurs fusionnent dans la branche main

Points de revue
----------

Les revues vérifient les points suivants :

**Fonctionnalité**

- Répond-elle aux exigences
- Fonctionne-t-elle comme prévu
- Les cas limites sont-ils pris en compte

**Qualité du code**

- Suit-elle les conventions de codage
- Le code est-il lisible et maintenable
- Les abstractions sont-elles appropriées

**Tests**

- Suffisamment de tests sont-ils écrits
- Les tests passent-ils
- Les tests font-ils des vérifications significatives

**Performance**

- Y a-t-il un impact sur les performances
- L'utilisation des ressources est-elle appropriée

**Sécurité**

- Y a-t-il des problèmes de sécurité
- La validation des entrées est-elle appropriée

**Documentation**

- La documentation nécessaire est-elle mise à jour
- Javadoc est-elle écrite de manière appropriée

Réponse aux commentaires de revue
--------------------

Répondez rapidement et poliment aux commentaires de revue.

**En cas de modifications nécessaires:**

.. code-block:: text

    Merci pour votre remarque. J'ai effectué les corrections.
    [Brève explication des modifications]

**En cas de discussion nécessaire:**

.. code-block:: text

    Merci pour votre avis.
    J'ai utilisé l'implémentation actuelle pour la raison XX,
    mais pensez-vous qu'une implémentation YY serait meilleure ?

Meilleures pratiques des pull requests
================================

Taille de la PR
---------

- Viser des PR petites et faciles à examiner
- Inclure un seul changement logique par PR
- Diviser les grands changements en plusieurs PR

Titre de la PR
-----------

Donnez un titre clair et descriptif :

.. code-block:: text

    feat: Ajouter une fonctionnalité de filtrage des résultats de recherche
    fix: Corriger le problème de timeout du crawler
    docs: Mettre à jour la documentation API

Description de la PR
-------

Incluez les informations suivantes :

- **Modifications** : Ce qui a été modifié
- **Raison** : Pourquoi ce changement est nécessaire
- **Méthode de test** : Comment cela a été testé
- **Captures d'écran** : En cas de modifications de l'interface utilisateur
- **Problème connexe** : Numéro du problème (ex : Closes #123)

.. code-block:: markdown

    ## Modifications
    Ajout d'une fonctionnalité permettant de filtrer les résultats de recherche par type de fichier.

    ## Raison
    De nombreuses demandes d'utilisateurs souhaitant "rechercher uniquement un type de fichier spécifique".

    ## Méthode de test
    1. Sélectionner le filtre de type de fichier sur l'écran de recherche
    2. Exécuter la recherche
    3. Vérifier que seuls les résultats du type de fichier sélectionné sont affichés

    ## Problème connexe
    Closes #123

Messages de commit
----------------

Écrivez des messages de commit clairs et descriptifs :

.. code-block:: text

    <type>: <sujet>

    <corps>

    <pied de page>

**Exemple:**

.. code-block:: text

    feat: Ajouter une fonctionnalité de filtre de recherche

    Permet aux utilisateurs de filtrer les résultats de recherche par type de fichier.

    - Ajout de l'interface utilisateur de filtre
    - Implémentation du traitement de filtre backend
    - Ajout de tests

    Closes #123

Utilisation des Draft PR
--------------

Créez des PR en cours de travail comme Draft PR,
et changez en Ready for review une fois terminé.

.. code-block:: text

    1. Sélectionner « Create draft pull request » lors de la création de PR
    2. Cliquer sur « Ready for review » une fois le travail terminé

Directives de la communauté
======================

Code de conduite
------

La communauté |Fess| respecte le code de conduite suivant :

- **Être respectueux** : Respecter toutes les personnes
- **Être coopératif** : Fournir des retours constructifs
- **Être ouvert** : Accueillir différentes perspectives et expériences
- **Être poli** : S'efforcer d'utiliser un langage courtois

Communication
----------------

**Où poser des questions:**

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__ : Questions générales et discussions
- `Suivi des problèmes <https://github.com/codelibs/fess/issues>`__ : Rapports de bugs et demandes de fonctionnalités
- `Forum Fess <https://discuss.codelibs.org/c/FessJA>`__ : Forum en japonais

**Comment poser des questions:**

- Poser des questions spécifiques
- Expliquer ce qui a été essayé
- Inclure les messages d'erreur et les journaux
- Indiquer les informations d'environnement (OS, version Java, etc.)

**Comment répondre:**

- Poliment et gentiment
- Proposer des solutions concrètes
- Fournir des liens vers des ressources de référence

Expression de gratitude
--------

Exprimez votre gratitude pour les contributions.
Même les petites contributions ont de la valeur pour le projet.

Questions fréquentes
==========

Q: Les débutants peuvent-ils contribuer ?
---------------------------

R: Oui, avec plaisir ! Nous vous recommandons de commencer par les problèmes avec l'étiquette ``good first issue``.
L'amélioration de la documentation est également une contribution adaptée aux débutants.

Q: Dans combien de temps les pull requests sont-elles examinées ?
-------------------------------------------------

R: Normalement, elles sont examinées dans les quelques jours.
Cependant, cela peut varier en fonction du calendrier des mainteneurs.

Q: Que se passe-t-il si une pull request est rejetée ?
-----------------------------------

R: Vérifiez la raison du rejet et, si nécessaire, corrigez et soumettez à nouveau.
Si vous avez des questions, n'hésitez pas à les poser.

Q: Que faire en cas de violation des conventions de codage ?
---------------------------------------

R: Elles seront signalées lors de la revue, donc les corriger ne posera pas de problème.
Vous pouvez vérifier à l'avance en exécutant Checkstyle.

Q: Comment ajouter une grande fonctionnalité ?
-------------------------------

R: Nous vous recommandons de créer d'abord un problème et de discuter de la proposition.
Obtenir un accord préalable permet d'éviter un travail inutile.

Q: Puis-je poser des questions en japonais ?
-------------------------------

R: Oui, le japonais et l'anglais sont acceptés.
Fess est un projet d'origine japonaise, donc le support en japonais est également complet.

Guides par type de contribution
================

Amélioration de la documentation
----------------

1. Forkez le dépôt de documentation :

   .. code-block:: bash

       git clone https://github.com/codelibs/fess-docs.git

2. Apportez des modifications
3. Créez une pull request

Rapport de bugs
------

1. Recherchez les problèmes existants pour vérifier les doublons
2. Créez un nouveau problème
3. Incluez les informations suivantes :

   - Description du bug
   - Étapes de reproduction
   - Comportement attendu
   - Comportement réel
   - Informations sur l'environnement

Demande de fonctionnalité
------------

1. Créez un problème
2. Expliquez ce qui suit :

   - Description de la fonctionnalité
   - Contexte et motivation
   - Méthode d'implémentation proposée (facultatif)

Revue de code
------------

Examiner les pull requests d'autres personnes est également une contribution :

1. Trouvez une PR qui vous intéresse
2. Vérifiez le code
3. Fournissez des retours constructifs

Licence
========

|Fess| est publié sous la licence Apache License 2.0.
Le code contribué sera également soumis à la même licence.

En créant une pull request,
vous acceptez que votre contribution soit publiée sous cette licence.

Remerciements
====

Merci de contribuer au projet |Fess| !
Votre contribution rend |Fess| meilleur.

Étapes suivantes
==========

Si vous êtes prêt à contribuer :

1. Configurez l'environnement de développement avec :doc:`setup`
2. Vérifiez le flux de développement avec :doc:`workflow`
3. Cherchez des problèmes sur `GitHub <https://github.com/codelibs/fess>`__

Ressources de référence
======

- `GitHub Flow <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `Comment contribuer à l'open source <https://opensource.guide/ja/how-to-contribute/>`__
- `Comment écrire de bons messages de commit <https://chris.beams.io/posts/git-commit/>`__

Ressources de la communauté
==================

- **GitHub** : `codelibs/fess <https://github.com/codelibs/fess>`__
- **Discussions** : `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- **Forum** : `Forum Fess <https://discuss.codelibs.org/c/FessJA>`__
- **Twitter** : `@codelibs <https://twitter.com/codelibs>`__
- **Site Web** : `fess.codelibs.org <https://fess.codelibs.org/ja/>`__
