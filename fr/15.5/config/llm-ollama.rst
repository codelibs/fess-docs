==========================
Configuration Ollama
==========================

Apercu
====

Ollama est une plateforme open source permettant d'executer des grands modeles de langage (LLM) en local.
Il est configure comme fournisseur LLM par defaut de |Fess| et convient a une utilisation en environnement prive.

L'utilisation d'Ollama permet d'utiliser la fonctionnalite de chat IA sans envoyer de donnees a l'exterieur.

Caracteristiques principales
--------

- **Execution locale** : Les donnees ne sont pas envoyees a l'exterieur, garantissant la confidentialite
- **Modeles varies** : Prise en charge de nombreux modeles dont Llama, Mistral, Gemma, CodeLlama
- **Efficacite des couts** : Pas de cout API (seulement les couts materiels)
- **Personnalisation** : Possibilite d'utiliser des modeles affines

Modeles pris en charge
----------

Principaux modeles disponibles avec Ollama :

- ``llama3.3:70b`` - Llama 3.3 de Meta (70B parametres)
- ``gemma3:4b`` - Gemma 3 de Google (4B parametres, par defaut)
- ``mistral:7b`` - Mistral de Mistral AI (7B parametres)
- ``codellama:13b`` - Code Llama de Meta (13B parametres)
- ``phi3:3.8b`` - Phi-3 de Microsoft (3.8B parametres)

.. note::
   Pour la derniere liste des modeles disponibles, consultez `Ollama Library <https://ollama.com/library>`__.

Prerequis
========

Avant d'utiliser Ollama, verifiez les points suivants.

1. **Installation d'Ollama** : Telechargez et installez depuis `https://ollama.com/ <https://ollama.com/>`__
2. **Telechargement du modele** : Telechargez le modele a utiliser dans Ollama
3. **Demarrage du serveur Ollama** : Verifiez qu'Ollama fonctionne

Installation d'Ollama
--------------------

Linux/macOS
~~~~~~~~~~~

::

    curl -fsSL https://ollama.com/install.sh | sh

Windows
~~~~~~~

Telechargez et executez l'installateur depuis le site officiel.

Docker
~~~~~~

::

    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

Telechargement du modele
--------------------

::

    # Telecharger le modele par defaut (Gemma 3 4B)
    ollama pull gemma3:4b

    # Telecharger Llama 3.3
    ollama pull llama3.3:70b

    # Verifier le fonctionnement du modele
    ollama run gemma3:4b "Hello, how are you?"

Configuration de base
========

Ajoutez les parametres suivants dans ``app/WEB-INF/conf/fess_config.properties``.

Configuration minimale
--------

::

    # Activer la fonctionnalite de mode IA
    rag.chat.enabled=true

    # Definir le fournisseur LLM sur Ollama
    rag.llm.type=ollama

    # URL d'Ollama (environnement local)
    rag.llm.ollama.api.url=http://localhost:11434

    # Modele a utiliser
    rag.llm.ollama.model=gemma3:4b

Configuration recommandee (environnement de production)
--------------------

::

    # Activer la fonctionnalite de mode IA
    rag.chat.enabled=true

    # Configuration du fournisseur LLM
    rag.llm.type=ollama

    # URL d'Ollama
    rag.llm.ollama.api.url=http://localhost:11434

    # Configuration du modele (utiliser un modele plus grand)
    rag.llm.ollama.model=llama3.3:70b

    # Configuration du timeout (augmente pour les grands modeles)
    rag.llm.ollama.timeout=120000

Elements de configuration
========

Tous les elements de configuration disponibles pour le client Ollama.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.ollama.api.url``
     - URL de base du serveur Ollama
     - ``http://localhost:11434``
   * - ``rag.llm.ollama.model``
     - Nom du modele a utiliser (modele telecharge dans Ollama)
     - ``gemma3:4b``
   * - ``rag.llm.ollama.timeout``
     - Timeout de la requete (millisecondes)
     - ``60000``

Configuration reseau
================

Configuration Docker
--------------

Exemple de configuration lorsque |Fess| et Ollama fonctionnent tous deux dans Docker.

``docker-compose.yml`` :

::

    version: '3'
    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma3:4b
        depends_on:
          - ollama
        # ... autres configurations

      ollama:
        image: ollama/ollama
        volumes:
          - ollama_data:/root/.ollama
        ports:
          - "11434:11434"

    volumes:
      ollama_data:

.. note::
   Dans l'environnement Docker Compose, utilisez ``ollama`` comme nom d'hote (pas ``localhost``).

Serveur Ollama distant
----------------------

Lorsqu'Ollama s'execute sur un serveur different de Fess :

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama n'a pas de fonctionnalite d'authentification par defaut, donc si vous le rendez accessible de l'exterieur,
   envisagez des mesures de securite au niveau reseau (pare-feu, VPN, etc.).

Guide de selection des modeles
==================

Guide pour la selection du modele selon l'usage.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modele
     - Taille
     - VRAM requise
     - Usage
   * - ``phi3:3.8b``
     - Petit
     - 4GB+
     - Environnement leger, questions-reponses simples
   * - ``gemma3:4b``
     - Petit-Moyen
     - 6GB+
     - Usage general equilibre (par defaut)
   * - ``mistral:7b``
     - Moyen
     - 8GB+
     - Reponses de haute qualite requises
   * - ``llama3.3:70b``
     - Grand
     - 48GB+
     - Reponses de meilleure qualite, raisonnement complexe

Prise en charge GPU
-------

Ollama prend en charge l'acceleration GPU. L'utilisation d'un GPU NVIDIA
ameliore considerablement la vitesse d'inference.

::

    # Verification de la prise en charge GPU
    ollama run gemma3:4b --verbose

Depannage
======================

Erreur de connexion
----------

**Symptome** : Erreur dans la fonctionnalite de chat, LLM affiche comme indisponible

**Points a verifier** :

1. Verifier si Ollama fonctionne ::

    curl http://localhost:11434/api/tags

2. Verifier si le modele est telecharge ::

    ollama list

3. Verifier les parametres du pare-feu

Modele introuvable
--------------------

**Symptome** : Log affichant "Configured model not found in Ollama"

**Solution** :

1. Verifier si le nom du modele est exact (peut necessiter le tag ``:latest``) ::

    # Verifier la liste des modeles
    ollama list

2. Telecharger le modele necessaire ::

    ollama pull gemma3:4b

Timeout
------------

**Symptome** : La requete expire

**Solution** :

1. Augmenter le temps de timeout ::

    rag.llm.ollama.timeout=120000

2. Envisager un modele plus petit ou un environnement GPU

Configuration de debogage
------------

Pour investiguer les problemes, ajustez le niveau de log de |Fess| pour afficher des logs detailles lies a Ollama.

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

Informations de reference
========

- `Site officiel Ollama <https://ollama.com/>`__
- `Bibliotheque de modeles Ollama <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - Apercu de l'integration LLM
- :doc:`rag-chat` - Details de la fonctionnalite de mode IA
