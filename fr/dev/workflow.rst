==============
Flux de travail de développement
==============

Cette page explique le flux de travail standard pour le développement de |Fess|.
Vous apprendrez comment procéder aux travaux de développement tels que l'ajout de fonctionnalités, la correction de bugs, les tests et la revue de code.

.. contents:: Table des matières
   :local:
   :depth: 2

Flux de base du développement
==============

Le développement de |Fess| se déroule comme suit :

.. code-block:: text

    1. Vérification/création d'un problème
       ↓
    2. Création d'une branche
       ↓
    3. Codage
       ↓
    4. Exécution des tests locaux
       ↓
    5. Commit
       ↓
    6. Push
       ↓
    7. Création d'une pull request
       ↓
    8. Revue de code
       ↓
    9. Réponse au retour de revue
       ↓
    10. Fusion

Chaque étape est expliquée en détail.

Étape 1 : Vérification/création d'un problème
=========================

Avant de commencer le développement, vérifiez les problèmes GitHub.

Vérification des problèmes existants
-----------------

1. Accédez à la `page des problèmes Fess <https://github.com/codelibs/fess/issues>`__
2. Trouvez un problème sur lequel vous souhaitez travailler
3. Commentez le problème pour indiquer que vous commencez à travailler dessus

.. tip::

   Pour une première contribution, nous vous recommandons de commencer par les problèmes avec l'étiquette ``good first issue``.

Création d'un nouveau problème
-----------------

Pour une nouvelle fonctionnalité ou une correction de bug, créez un problème.

1. Cliquez sur `New Issue <https://github.com/codelibs/fess/issues/new>`__
2. Sélectionnez le modèle de problème
3. Remplissez les informations nécessaires :

   - **Titre** : Description concise et claire
   - **Description** : Contexte détaillé, comportement attendu, comportement actuel
   - **Étapes de reproduction** : En cas de bug
   - **Informations sur l'environnement** : OS, version Java, version Fess, etc.

4. Cliquez sur ``Submit new issue``

Modèle de problème
~~~~~~~~~~~~~~~~~~

**Rapport de bug :**

.. code-block:: markdown

    ## Description du problème
    Description concise du bug

    ## Étapes de reproduction
    1. ...
    2. ...
    3. ...

    ## Comportement attendu
    Comment cela devrait-il être

    ## Comportement réel
    Comment cela se comporte actuellement

    ## Environnement
    - OS:
    - Version Java:
    - Version Fess:

**Demande de fonctionnalité :**

.. code-block:: markdown

    ## Description de la fonctionnalité
    Description de la fonctionnalité à ajouter

    ## Contexte et motivation
    Pourquoi cette fonctionnalité est-elle nécessaire

    ## Méthode d'implémentation proposée
    Comment l'implémenter (facultatif)

Étape 2 : Création d'une branche
====================

Créez une branche de travail.

Convention de nommage des branches
--------------

Les noms de branches suivent le format suivant :

.. code-block:: text

    <type>/<numéro-problème>-<description-courte>

**Types de type :**

- ``feature`` : Ajout de nouvelle fonctionnalité
- ``fix`` : Correction de bug
- ``refactor`` : Refactoring
- ``docs`` : Mise à jour de la documentation
- ``test`` : Ajout/modification de tests

**Exemples :**

.. code-block:: bash

    # Ajout de nouvelle fonctionnalité
    git checkout -b feature/123-add-search-filter

    # Correction de bug
    git checkout -b fix/456-fix-crawler-timeout

    # Mise à jour de la documentation
    git checkout -b docs/789-update-api-docs

Procédure de création de branche
----------------

1. Obtenez la dernière branche main :

   .. code-block:: bash

       git checkout main
       git pull origin main

2. Créez une nouvelle branche :

   .. code-block:: bash

       git checkout -b feature/123-add-search-filter

3. Vérifiez que la branche a été créée :

   .. code-block:: bash

       git branch

Étape 3 : Codage
==================

Implémentez la fonctionnalité ou corrigez le bug.

Conventions de codage
--------------

|Fess| suit les conventions de codage suivantes.

Style de base
~~~~~~~~~~~~~~

- **Indentation** : 4 espaces
- **Longueur de ligne** : 120 caractères maximum recommandé
- **Encodage** : UTF-8
- **Code de fin de ligne** : LF (style Unix)

Conventions de nommage
~~~~~~

- **Nom de classe** : PascalCase (ex : ``SearchService``)
- **Nom de méthode** : camelCase (ex : ``executeSearch``)
- **Constantes** : UPPER_SNAKE_CASE (ex : ``MAX_SEARCH_SIZE``)
- **Variables** : camelCase (ex : ``searchResults``)

Commentaires
~~~~~~

- **Javadoc** : Obligatoire pour les classes et méthodes publiques
- **Commentaires d'implémentation** : Ajoutez des explications en japonais ou en anglais pour une logique complexe

**Exemple :**

.. code-block:: java

    /**
     * Exécute une recherche.
     *
     * @param query Requête de recherche
     * @return Résultats de recherche
     */
    public SearchResponse executeSearch(String query) {
        // Normalisation de la requête
        String normalizedQuery = normalizeQuery(query);

        // Exécution de la recherche
        return searchEngine.search(normalizedQuery);
    }

Gestion de null
~~~~~~~~~

- Ne retournez pas ``null`` dans la mesure du possible
- Utilisation d'``Optional`` recommandée
- Effectuez explicitement les vérifications ``null``

**Exemple :**

.. code-block:: java

    // Bon exemple
    public Optional<User> findUser(String id) {
        return userRepository.findById(id);
    }

    // Exemple à éviter
    public User findUser(String id) {
        return userRepository.findById(id);  // Possibilité de null
    }

Gestion des exceptions
~~~~~~

- Attrapez et traitez correctement les exceptions
- Effectuez la journalisation
- Fournissez des messages compréhensibles à l'utilisateur

**Exemple :**

.. code-block:: java

    try {
        // Traitement
    } catch (IOException e) {
        logger.error("Erreur de lecture de fichier", e);
        throw new FessSystemException("La lecture du fichier a échoué", e);
    }

Journalisation
~~~~~~

Utilisez le niveau de journalisation approprié :

- ``ERROR`` : En cas d'erreur
- ``WARN`` : Situations nécessitant un avertissement
- ``INFO`` : Informations importantes
- ``DEBUG`` : Informations de débogage
- ``TRACE`` : Informations de trace détaillées

**Exemple :**

.. code-block:: java

    if (logger.isDebugEnabled()) {
        logger.debug("Requête de recherche: {}", query);
    }

Tests pendant le développement
------------

Pendant le développement, testez de la manière suivante :

Exécution locale
~~~~~~~~~~

Exécutez Fess dans l'IDE ou en ligne de commande et vérifiez le fonctionnement :

.. code-block:: bash

    mvn compile exec:java

Exécution en débogage
~~~~~~~~~~

Utilisez le débogueur de l'IDE pour suivre le comportement du code.

Exécution des tests unitaires
~~~~~~~~~~~~~~

Exécutez les tests liés aux modifications :

.. code-block:: bash

    # Exécuter une classe de test spécifique
    mvn test -Dtest=SearchServiceTest

    # Exécuter tous les tests
    mvn test

Consultez :doc:`building` pour plus de détails.

Étape 4 : Exécution des tests locaux
=========================

Avant de commiter, exécutez toujours les tests.

Exécution des tests unitaires
--------------

.. code-block:: bash

    mvn test

Exécution des tests d'intégration
--------------

.. code-block:: bash

    mvn verify

Vérification du style de code
--------------------

.. code-block:: bash

    mvn checkstyle:check

Exécution de toutes les vérifications
-------------------

.. code-block:: bash

    mvn clean verify

Étape 5 : Commit
==============

Commitez les modifications.

Convention des messages de commit
--------------------

Les messages de commit suivent le format suivant :

.. code-block:: text

    <type>: <sujet>

    <corps>

    <pied de page>

**Types de type :**

- ``feat`` : Nouvelle fonctionnalité
- ``fix`` : Correction de bug
- ``docs`` : Modification de documentation uniquement
- ``style`` : Modifications n'affectant pas la signification du code (formatage, etc.)
- ``refactor`` : Refactoring
- ``test`` : Ajout/modification de tests
- ``chore`` : Modifications du processus de compilation ou des outils

**Exemple :**

.. code-block:: text

    feat: Ajouter une fonctionnalité de filtre de recherche

    Permet aux utilisateurs de filtrer les résultats de recherche par type de fichier.

    Fixes #123

Procédure de commit
----------

1. Mettez en staging les modifications :

   .. code-block:: bash

       git add .

2. Commitez :

   .. code-block:: bash

       git commit -m "feat: Ajouter une fonctionnalité de filtre de recherche"

3. Vérifiez l'historique des commits :

   .. code-block:: bash

       git log --oneline

Granularité des commits
------------

- Incluez un seul changement logique par commit
- Divisez les grands changements en plusieurs commits
- Les messages de commit doivent être clairs et spécifiques

Étape 6 : Push
==============

Poussez la branche vers le dépôt distant.

.. code-block:: bash

    git push origin feature/123-add-search-filter

Pour le premier push :

.. code-block:: bash

    git push -u origin feature/123-add-search-filter

Étape 7 : Création d'une pull request
=========================

Créez une pull request (PR) sur GitHub.

Procédure de création de PR
-----------

1. Accédez au `dépôt Fess <https://github.com/codelibs/fess>`__
2. Cliquez sur l'onglet ``Pull requests``
3. Cliquez sur ``New pull request``
4. Sélectionnez la branche de base (``main``) et la branche de comparaison (branche de travail)
5. Cliquez sur ``Create pull request``
6. Remplissez le contenu de la PR (suivez le modèle)
7. Cliquez sur ``Create pull request``

Modèle de PR
---------------

.. code-block:: markdown

    ## Modifications
    Ce qui a été modifié dans cette PR

    ## Problème connexe
    Closes #123

    ## Type de modification
    - [ ] Nouvelle fonctionnalité
    - [ ] Correction de bug
    - [ ] Refactoring
    - [ ] Mise à jour de la documentation
    - [ ] Autre

    ## Méthode de test
    Comment cette modification a été testée

    ## Liste de vérification
    - [ ] Le code fonctionne
    - [ ] Des tests ont été ajoutés
    - [ ] La documentation a été mise à jour
    - [ ] Les conventions de codage sont respectées

Description de la PR
-------

La description de la PR doit inclure :

- **Objectif de la modification** : Pourquoi cette modification est-elle nécessaire
- **Contenu de la modification** : Ce qui a été modifié
- **Méthode de test** : Comment cela a été testé
- **Captures d'écran** : En cas de modifications de l'interface utilisateur

Étape 8 : Revue de code
====================

Les mainteneurs examinent le code.

Points de revue
------------

Les revues vérifient les points suivants :

- Qualité du code
- Conformité aux conventions de codage
- Complétude des tests
- Impact sur les performances
- Problèmes de sécurité
- Mise à jour de la documentation

Exemples de commentaires de revue
------------------

**Approbation :**

.. code-block:: text

    LGTM (Looks Good To Me)

**Demande de modification :**

.. code-block:: text

    Une vérification null n'est-elle pas nécessaire ici ?

**Suggestion :**

.. code-block:: text

    Il serait peut-être mieux de déplacer ce traitement dans une classe Helper.

Étape 9 : Réponse au retour de revue
===================================

Répondez aux commentaires de revue.

Procédure de réponse au retour
----------------------

1. Lisez les commentaires de revue
2. Effectuez les modifications nécessaires
3. Commitez les modifications :

   .. code-block:: bash

       git add .
       git commit -m "fix: Répondre aux commentaires de revue"

4. Poussez :

   .. code-block:: bash

       git push origin feature/123-add-search-filter

5. Répondez aux commentaires sur la page PR

Réponse aux commentaires
--------------

Répondez toujours aux commentaires de revue :

.. code-block:: text

    Modifications effectuées. Veuillez vérifier.

Ou :

.. code-block:: text

    Merci pour votre remarque.
    J'ai utilisé l'implémentation actuelle pour la raison XX, qu'en pensez-vous ?

Étape 10 : Fusion
=============

Lorsque la revue est approuvée, les mainteneurs fusionnent la PR.

Actions après la fusion
------------

1. Mettez à jour la branche main locale :

   .. code-block:: bash

       git checkout main
       git pull origin main

2. Supprimez la branche de travail :

   .. code-block:: bash

       git branch -d feature/123-add-search-filter

3. Supprimez la branche distante (si elle n'est pas automatiquement supprimée sur GitHub) :

   .. code-block:: bash

       git push origin --delete feature/123-add-search-filter

Scénarios de développement courants
==================

Ajout de fonctionnalité
------

1. Créez un problème (ou vérifiez un problème existant)
2. Créez une branche : ``feature/xxx-description``
3. Implémentez la fonctionnalité
4. Ajoutez des tests
5. Mettez à jour la documentation
6. Créez une PR

Correction de bug
------

1. Vérifiez le problème de rapport de bug
2. Créez une branche : ``fix/xxx-description``
3. Ajoutez un test reproduisant le bug
4. Corrigez le bug
5. Vérifiez que le test passe
6. Créez une PR

Refactoring
--------------

1. Créez un problème (expliquez la raison du refactoring)
2. Créez une branche : ``refactor/xxx-description``
3. Effectuez le refactoring
4. Vérifiez que les tests existants passent
5. Créez une PR

Mise à jour de la documentation
--------------

1. Créez une branche : ``docs/xxx-description``
2. Mettez à jour la documentation
3. Créez une PR

Conseils de développement
==========

Développement efficace
----------

- **Petits commits** : Commitez fréquemment
- **Retour précoce** : Utilisez les Draft PR
- **Automatisation des tests** : Utilisez CI/CD
- **Revue de code** : Examinez également le code des autres

Résolution de problèmes
--------

En cas de difficulté, utilisez les ressources suivantes :

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- `Forum Fess <https://discuss.codelibs.org/c/FessJA>`__
- Commentaires de problème GitHub

Étapes suivantes
==========

Après avoir compris le flux de travail, consultez également la documentation suivante :

- :doc:`building` - Détails sur la compilation et les tests
- :doc:`contributing` - Directives de contribution
- :doc:`architecture` - Compréhension du code source

Ressources de référence
======

- `GitHub Flow <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `Directives des messages de commit <https://chris.beams.io/posts/git-commit/>`__
- `Meilleures pratiques de revue de code <https://google.github.io/eng-practices/review/>`__
