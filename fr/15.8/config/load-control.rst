=====================================
Configuration du contrôle de charge
=====================================

Aperçu
======

|Fess| dispose de deux types de fonctionnalités de contrôle de charge qui protègent la stabilité du système en fonction de l'utilisation CPU.

**Contrôle de charge des requêtes HTTP** (``web.load.control`` / ``api.load.control``) :

- Surveillance en temps réel de l'utilisation CPU du cluster OpenSearch
- Seuils indépendants configurables pour les requêtes web et les requêtes API
- Retourne HTTP 429 (Too Many Requests) lorsque les seuils sont dépassés
- Le panneau d'administration, la connexion et les ressources statiques sont exclus du contrôle
- Désactivé par défaut (seuil=100)

**Contrôle de charge adaptatif** (``adaptive.load.control``) :

- Surveille l'utilisation CPU système du serveur Fess lui-même
- Ralentit automatiquement les tâches en arrière-plan telles que le crawling, l'indexation, les mises à jour de suggestions et la génération de vignettes
- Lorsque l'utilisation CPU atteint ou dépasse le seuil, les threads de traitement sont mis en pause et reprennent lorsqu'elle descend en dessous du seuil
- Activé par défaut (seuil=50)

Configuration du contrôle de charge des requêtes HTTP
=====================================================

Définissez les propriétés suivantes dans ``fess_config.properties`` :

::

    # Seuil d'utilisation CPU pour les requetes web (%)
    # Les requetes sont rejetees lorsque l'utilisation CPU d'OpenSearch atteint ou depasse cette valeur
    # Definir a 100 pour desactiver (defaut : 100)
    web.load.control=100

    # Seuil d'utilisation CPU pour les requetes API (%)
    # Les requetes sont rejetees lorsque l'utilisation CPU d'OpenSearch atteint ou depasse cette valeur
    # Definir a 100 pour desactiver (defaut : 100)
    api.load.control=100

    # Intervalle de surveillance de l'utilisation CPU (secondes)
    # Intervalle pour recuperer l'utilisation CPU du cluster OpenSearch
    # Defaut : 1
    load.control.monitor.interval=1

.. note::
   Lorsque ``web.load.control`` et ``api.load.control`` sont tous deux définis à 100 (défaut),
   la surveillance CPU d'OpenSearch ne démarre pas.

Fonctionnement
==============

Mécanisme de surveillance
-------------------------

Lorsque le contrôle de charge est activé (l'un ou l'autre des seuils est inférieur à 100), LoadControlMonitorTarget surveille périodiquement l'utilisation CPU du cluster OpenSearch.

- Récupère les statistiques OS de tous les noeuds du cluster OpenSearch
- Enregistre l'utilisation CPU la plus élevée parmi tous les noeuds
- Surveille à l'intervalle spécifié par ``load.control.monitor.interval`` (défaut : 1 seconde)
- La surveillance démarre de manière différée lors de la première requête

.. note::
   Si la récupération des informations de surveillance échoue, l'utilisation CPU est réinitialisée à 0.
   Les trois premiers échecs consécutifs sont enregistrés au niveau WARNING dans les logs ; à partir
   du quatrième échec, le niveau passe à DEBUG (afin d'éviter une inflation des logs en cas d'échecs
   persistants). Le compteur d'échecs est réinitialisé dès qu'une surveillance réussit.

Contrôle des requêtes
---------------------

Lorsqu'une requête arrive, LoadControlFilter la traite dans l'ordre suivant :

1. Vérifier si le chemin est exclu (si exclu, laisser passer)
2. Déterminer le type de requête (Web / API)
3. Obtenir le seuil correspondant
4. Si le seuil est de 100 ou plus, ne pas contrôler (laisser passer)
5. Comparer l'utilisation CPU actuelle avec le seuil
6. Si l'utilisation CPU >= seuil, retourner HTTP 429

**Requêtes exclues :**

- Chemins commençant par ``/admin`` (panneau d'administration)
- Chemins commençant par ``/error`` (pages d'erreur)
- Chemins commençant par ``/login`` (pages de connexion)
- Ressources statiques (``.css``, ``.js``, ``.png``, ``.jpg``, ``.gif``, ``.ico``, ``.svg``, ``.woff``, ``.woff2``, ``.ttf``, ``.eot``)

**Pour les requêtes web :**

- Retourne le code de statut HTTP 429
- Affiche la page d'erreur (``busy.jsp``)

**Pour les requêtes API :**

- Retourne le code de statut HTTP 429
- Ajoute l'en-tête de réponse HTTP ``Retry-After: 60``
- Retourne une réponse JSON :

::

    {
        "response": {
            "status": 9,
            "message": "Server is busy. Please retry after 60 seconds.",
            "retry_after": 60
        }
    }

.. note::
   Lorsqu'une requête est rejetée, le message suivant est enregistré au niveau INFO dans les logs du serveur :
   ``Rejecting request due to high CPU load: path=..., cpu=...%, threshold=...%``
   Cela permet de vérifier quel chemin a été rejeté et pour quel seuil.

Exemples de configuration
=========================

Limiter uniquement les requêtes web
------------------------------------

Configuration qui limite uniquement les requêtes de recherche web sans restreindre l'API :

::

    # Web : Rejeter les requetes lorsque l'utilisation CPU est de 80% ou plus
    web.load.control=80

    # API : Aucune restriction
    api.load.control=100

    # Intervalle de surveillance : 1 seconde
    load.control.monitor.interval=1

Limiter à la fois le web et l'API
----------------------------------

Exemple avec des seuils différents pour le web et l'API :

::

    # Web : Rejeter les requetes lorsque l'utilisation CPU est de 70% ou plus
    web.load.control=70

    # API : Rejeter les requetes lorsque l'utilisation CPU est de 80% ou plus
    api.load.control=80

    # Intervalle de surveillance : 2 secondes
    load.control.monitor.interval=2

.. note::
   En définissant le seuil API plus haut que le seuil web, vous pouvez réaliser un contrôle progressif
   où les requêtes web sont restreintes en premier lors d'une charge élevée, et les requêtes API sont
   également restreintes lorsque la charge augmente davantage.

Différence avec la limitation de débit
=======================================

|Fess| dispose d'une fonctionnalité de :doc:`rate-limiting` séparée du contrôle de charge.
Ces deux mécanismes protègent le système avec des approches différentes.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - Limitation de débit
     - Contrôle de charge
   * - Base de contrôle
     - Nombre de requêtes (par unité de temps)
     - Utilisation CPU d'OpenSearch
   * - Objectif
     - Prévention des requêtes excessives
     - Protection du moteur de recherche contre la surcharge
   * - Unité de limite
     - Par adresse IP
     - Ensemble du système
   * - Réponse
     - HTTP 429
     - HTTP 429
   * - Portée
     - Toutes les requêtes HTTP
     - Requêtes web / Requêtes API (panneau d'administration etc. exclu)

La combinaison des deux fonctionnalités permet une protection système plus robuste.

Contrôle de charge adaptatif
============================

Le contrôle de charge adaptatif ajuste automatiquement la vitesse de traitement des tâches
en arrière-plan en fonction de l'utilisation CPU système du serveur Fess.

Configuration
-------------

``fess_config.properties`` :

::

    # Seuil d'utilisation CPU du controle de charge adaptatif (%)
    # Met en pause les taches en arriere-plan lorsque l'utilisation CPU systeme atteint ou depasse cette valeur
    # Definir a 0 ou moins pour desactiver (defaut : 50)
    adaptive.load.control=50

Comportement
------------

- Surveille l'utilisation CPU système du serveur où Fess s'exécute
- Lorsque l'utilisation CPU atteint ou dépasse le seuil, les threads de traitement concernés attendent que l'utilisation CPU descende en dessous du seuil
- Lorsque l'utilisation CPU descend en dessous du seuil, le traitement reprend automatiquement

**Tâches en arrière-plan concernées :**

- Crawling (Web / Système de fichiers)
- Indexation (enregistrement de documents)
- Traitement du magasin de données
- Mises à jour des suggestions
- Génération de vignettes
- Sauvegarde et restauration

.. note::
   Le contrôle de charge adaptatif est activé par défaut (seuil=50).
   Il fonctionne indépendamment du contrôle de charge des requêtes HTTP (``web.load.control`` / ``api.load.control``).

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - Contrôle de charge des requêtes HTTP
     - Contrôle de charge adaptatif
   * - Cible de surveillance
     - Utilisation CPU d'OpenSearch
     - Utilisation CPU système du serveur Fess
   * - Cible de contrôle
     - Requêtes HTTP (Web / API)
     - Tâches en arrière-plan
   * - Méthode de contrôle
     - Rejette les requêtes en retournant HTTP 429
     - Met en pause temporairement les threads de traitement
   * - Défaut
     - Désactivé (seuil=100)
     - Activé (seuil=50)

Dépannage
=========

Le contrôle de charge ne s'active pas
--------------------------------------

**Cause** : La configuration n'est pas correctement appliquée

**Points à vérifier** :

1. Vérifier si ``web.load.control`` ou ``api.load.control`` est défini en dessous de 100
2. Vérifier si le fichier de configuration est correctement lu
3. Vérifier si |Fess| a été redémarré

Les requêtes légitimes sont rejetées
--------------------------------------

**Cause** : Les seuils sont trop bas

**Solution** :

1. Augmenter les valeurs de ``web.load.control`` ou ``api.load.control``
2. Ajuster ``load.control.monitor.interval`` pour modifier la fréquence de surveillance
3. Augmenter les ressources du cluster OpenSearch

.. warning::
   Définir des seuils trop bas peut entraîner le rejet de requêtes même sous charge normale.
   Vérifiez l'utilisation CPU normale de votre cluster OpenSearch avant de définir des seuils appropriés.

Le crawling est lent
--------------------

**Cause** : Les threads sont en état d'attente en raison du contrôle de charge adaptatif

**Points à vérifier** :

1. Vérifier si ``Cpu Load XX% is greater than YY%`` apparaît dans les logs
2. Vérifier si le seuil ``adaptive.load.control`` est trop bas

**Solution** :

1. Augmenter la valeur de ``adaptive.load.control`` (ex : 70)
2. Augmenter les ressources CPU du serveur Fess
3. Définir à 0 pour désactiver le contrôle de charge adaptatif (non recommandé)

Informations de référence
=========================

- :doc:`rate-limiting` - Configuration de la limitation de débit
