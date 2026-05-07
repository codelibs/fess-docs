==================================
Configuration du controle de charge
==================================

Apercu
======

|Fess| dispose de deux types de fonctionnalites de controle de charge qui protegent la stabilite du systeme en fonction de l'utilisation CPU.

**Controle de charge des requetes HTTP** (``web.load.control`` / ``api.load.control``) :

- Surveillance en temps reel de l'utilisation CPU du cluster OpenSearch
- Seuils independants pour les requetes web et les requetes API
- Retourne HTTP 429 (Too Many Requests) lorsque les seuils sont depasses
- Le panneau d'administration, la connexion et les ressources statiques sont exclus du controle
- Desactive par defaut (seuil=100)

**Controle de charge adaptatif** (``adaptive.load.control``) :

- Surveille l'utilisation CPU systeme du serveur Fess lui-meme
- Ralentit automatiquement les taches en arriere-plan telles que le crawling, l'indexation, les mises a jour de suggestions et la generation de vignettes
- Lorsque l'utilisation CPU atteint ou depasse le seuil, les threads de traitement sont mis en pause et reprennent lorsqu'elle descend en dessous du seuil
- Active par defaut (seuil=50)

Configuration du controle de charge des requetes HTTP
=====================================================

Definissez les proprietes suivantes dans ``fess_config.properties`` :

::

    # Seuil d'utilisation CPU pour les requetes web (%)
    # Les requetes sont rejetees lorsque l'utilisation CPU atteint ou depasse cette valeur
    # Definir a 100 pour desactiver (defaut : 100)
    web.load.control=100

    # Seuil d'utilisation CPU pour les requetes API (%)
    # Les requetes sont rejetees lorsque l'utilisation CPU atteint ou depasse cette valeur
    # Definir a 100 pour desactiver (defaut : 100)
    api.load.control=100

    # Intervalle de surveillance de l'utilisation CPU (secondes)
    # Intervalle pour recuperer l'utilisation CPU du cluster OpenSearch
    # Defaut : 1
    load.control.monitor.interval=1

.. note::
   Lorsque ``web.load.control`` et ``api.load.control`` sont tous deux definis a 100 (defaut),
   la fonctionnalite de controle de charge est completement desactivee et la surveillance ne demarre pas.

Fonctionnement
==============

Mecanisme de surveillance
-------------------------

Lorsque le controle de charge est active (un seuil est inferieur a 100), LoadControlMonitorTarget surveille periodiquement l'utilisation CPU du cluster OpenSearch.

- Recupere les statistiques OS de tous les noeuds du cluster OpenSearch
- Enregistre l'utilisation CPU la plus elevee parmi tous les noeuds
- Surveille a l'intervalle specifie par ``load.control.monitor.interval`` (defaut : 1 seconde)
- La surveillance demarre de maniere differee lors de la premiere requete

.. note::
   Si la recuperation des informations de surveillance echoue, l'utilisation CPU est reinitialisee a 0.
   Apres 3 echecs consecutifs, le niveau de log passe de WARNING a DEBUG.

Controle des requetes
---------------------

Lorsqu'une requete arrive, LoadControlFilter la traite dans l'ordre suivant :

1. Verifier si le chemin est exclu (si exclu, laisser passer)
2. Determiner le type de requete (Web / API)
3. Obtenir le seuil correspondant
4. Si le seuil est de 100 ou plus, ne pas controler (laisser passer)
5. Comparer l'utilisation CPU actuelle avec le seuil
6. Si l'utilisation CPU >= seuil, retourner HTTP 429

**Requetes exclues :**

- Chemins commencant par ``/admin`` (panneau d'administration)
- Chemins commencant par ``/error`` (pages d'erreur)
- Chemins commencant par ``/login`` (pages de connexion)
- Ressources statiques (``.css``, ``.js``, ``.png``, ``.jpg``, ``.gif``, ``.ico``, ``.svg``, ``.woff``, ``.woff2``, ``.ttf``, ``.eot``)

**Pour les requetes web :**

- Retourne le code de statut HTTP 429
- Affiche la page d'erreur (``busy.jsp``)

**Pour les requetes API :**

- Retourne le code de statut HTTP 429
- Retourne une reponse JSON :

::

    {
        "response": {
            "status": 9,
            "message": "Server is busy. Please retry after 60 seconds.",
            "retry_after": 60
        }
    }

Exemples de configuration
=========================

Limiter uniquement les requetes web
------------------------------------

Configuration qui limite uniquement les requetes de recherche web sans restreindre l'API :

::

    # Web : Rejeter les requetes lorsque l'utilisation CPU est de 80% ou plus
    web.load.control=80

    # API : Aucune restriction
    api.load.control=100

    # Intervalle de surveillance : 1 seconde
    load.control.monitor.interval=1

Limiter a la fois le web et l'API
----------------------------------

Exemple avec des seuils differents pour le web et l'API :

::

    # Web : Rejeter les requetes lorsque l'utilisation CPU est de 70% ou plus
    web.load.control=70

    # API : Rejeter les requetes lorsque l'utilisation CPU est de 80% ou plus
    api.load.control=80

    # Intervalle de surveillance : 2 secondes
    load.control.monitor.interval=2

.. note::
   En definissant le seuil API plus haut que le seuil web, vous pouvez realiser un controle progressif
   ou les requetes web sont restreintes en premier lors d'une charge elevee, et les requetes API sont egalement
   restreintes lorsque la charge augmente davantage.

Difference avec la limitation de debit
=======================================

|Fess| dispose d'une fonctionnalite de :doc:`rate-limiting` separee du controle de charge.
Celles-ci protegent le systeme avec des approches differentes.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - Limitation de debit
     - Controle de charge
   * - Base de controle
     - Nombre de requetes (par unite de temps)
     - Utilisation CPU d'OpenSearch
   * - Objectif
     - Prevention des requetes excessives
     - Protection du moteur de recherche contre la charge elevee
   * - Unite de limite
     - Par adresse IP
     - Ensemble du systeme
   * - Reponse
     - HTTP 429
     - HTTP 429
   * - Portee
     - Toutes les requetes HTTP
     - Requetes web / Requetes API (panneau d'administration etc. exclu)

La combinaison des deux fonctionnalites permet une protection systeme plus robuste.

Controle de charge adaptatif
============================

Le controle de charge adaptatif ajuste automatiquement la vitesse de traitement des taches
en arriere-plan en fonction de l'utilisation CPU systeme du serveur Fess.

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

- Surveille l'utilisation CPU systeme du serveur ou Fess s'execute
- Lorsque l'utilisation CPU atteint ou depasse le seuil, les threads de traitement concernes attendent que l'utilisation CPU descende en dessous du seuil
- Lorsque l'utilisation CPU descend en dessous du seuil, le traitement reprend automatiquement

**Taches en arriere-plan concernees :**

- Crawling (Web / Systeme de fichiers)
- Indexation (enregistrement de documents)
- Traitement du magasin de donnees
- Mises a jour des suggestions
- Generation de vignettes
- Sauvegarde et restauration

.. note::
   Le controle de charge adaptatif est active par defaut (seuil=50).
   Il fonctionne independamment du controle de charge des requetes HTTP (``web.load.control`` / ``api.load.control``).

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - Controle de charge des requetes HTTP
     - Controle de charge adaptatif
   * - Cible de surveillance
     - Utilisation CPU d'OpenSearch
     - Utilisation CPU systeme du serveur Fess
   * - Cible de controle
     - Requetes HTTP (Web / API)
     - Taches en arriere-plan
   * - Methode de controle
     - Rejette les requetes en retournant HTTP 429
     - Met en pause temporairement les threads de traitement
   * - Defaut
     - Desactive (seuil=100)
     - Active (seuil=50)

Depannage
=========

Le controle de charge ne s'active pas
--------------------------------------

**Cause** : La configuration n'est pas correctement appliquee

**Points a verifier** :

1. Verifier si ``web.load.control`` ou ``api.load.control`` est defini en dessous de 100
2. Verifier si le fichier de configuration est correctement lu
3. Verifier si |Fess| a ete redemarre

Les requetes legitimes sont rejetees
--------------------------------------

**Cause** : Les seuils sont trop bas

**Solution** :

1. Augmenter les valeurs de ``web.load.control`` ou ``api.load.control``
2. Ajuster ``load.control.monitor.interval`` pour modifier la frequence de surveillance
3. Augmenter les ressources du cluster OpenSearch

.. warning::
   Definir des seuils trop bas peut entrainer le rejet de requetes meme sous charge normale.
   Verifiez l'utilisation CPU normale de votre cluster OpenSearch avant de definir des seuils appropries.

Le crawling est lent
--------------------

**Cause** : Les threads sont en etat d'attente en raison du controle de charge adaptatif

**Points a verifier** :

1. Verifier si ``Cpu Load XX% is greater than YY%`` apparait dans les logs
2. Verifier si le seuil ``adaptive.load.control`` est trop bas

**Solution** :

1. Augmenter la valeur de ``adaptive.load.control`` (ex : 70)
2. Augmenter les ressources CPU du serveur Fess
3. Definir a 0 pour desactiver le controle de charge adaptatif (non recommande)

Informations de reference
=========================

- :doc:`rate-limiting` - Configuration de la limitation de debit
