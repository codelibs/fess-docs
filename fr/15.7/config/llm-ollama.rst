==========================
Configuration Ollama
==========================

Apercu
====

Ollama est une plateforme open source permettant d'executer des grands modeles de langage (LLM) en local.
La fonctionnalite d'integration Ollama de |Fess| est fournie sous forme de plugin ``fess-llm-ollama``, et convient a une utilisation en environnement prive.

L'utilisation d'Ollama permet d'utiliser la fonctionnalite du mode de recherche IA sans envoyer de donnees a l'exterieur.

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
- ``gemma4:e4b`` - Gemma 4 de Google (E4B parametres, par defaut)
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

    # Telecharger le modele par defaut (Gemma 4 E4B)
    ollama pull gemma4:e4b

    # Telecharger Llama 3.3
    ollama pull llama3.3:70b

    # Verifier le fonctionnement du modele
    ollama run gemma4:e4b "Hello, how are you?"

Installation du plugin
========================

La fonctionnalite d'integration Ollama est fournie sous forme de plugin.
Pour utiliser Ollama, l'installation du plugin ``fess-llm-ollama`` est necessaire.

1. Telechargez `fess-llm-ollama-15.7.0.jar`.
2. Placez-le dans le repertoire ``app/WEB-INF/plugin/`` du repertoire d'installation de |Fess|.

::

    cp fess-llm-ollama-15.7.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Redemarrez |Fess|.

.. note::
   La version du plugin doit correspondre a la version de |Fess|.

Configuration de base
========

Les configurations LLM sont reparties dans plusieurs fichiers de configuration.

Configuration minimale
--------

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

    # URL d'Ollama (environnement local)
    rag.llm.ollama.api.url=http://localhost:11434

    # Modele a utiliser
    rag.llm.ollama.model=gemma4:e4b

``system.properties`` (configurable egalement via Administration > Systeme > General) :

::

    # Definir le fournisseur LLM sur Ollama
    rag.llm.name=ollama

.. note::
   La configuration du fournisseur LLM peut egalement etre effectuee via l'administration (Administration > Systeme > General) en configurant ``rag.llm.name``.

Configuration recommandee (environnement de production)
--------------------

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

    # URL d'Ollama
    rag.llm.ollama.api.url=http://localhost:11434

    # Configuration du modele (utiliser un modele plus grand)
    rag.llm.ollama.model=llama3.3:70b

    # Configuration du timeout (augmente pour les grands modeles)
    rag.llm.ollama.timeout=120000

    # Controle du nombre de requetes simultanees
    rag.llm.ollama.max.concurrent.requests=5

``system.properties`` :

::

    # Configuration du fournisseur LLM
    rag.llm.name=ollama

Elements de configuration
========

Tous les elements de configuration disponibles pour le client Ollama. Tous se configurent dans ``fess_config.properties``.

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
     - ``gemma4:e4b``
   * - ``rag.llm.ollama.timeout``
     - Timeout de la requete (millisecondes)
     - ``60000``
   * - ``rag.llm.ollama.availability.check.interval``
     - Intervalle de verification de disponibilite (secondes)
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - Nombre maximum de requetes simultanees
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - Nombre maximum de documents pertinents lors de l'evaluation
     - ``3``
   * - ``rag.llm.ollama.concurrency.wait.timeout``
     - Delai d'attente de l'acquisition d'un permis de controle de concurrence (millisecondes)
     - ``30000``
   * - ``rag.llm.ollama.connect.timeout``
     - Timeout de connexion TCP (millisecondes). Peut etre specifie separement de ``rag.llm.ollama.timeout``
     - ``5000``
   * - ``rag.llm.ollama.retry.max``
     - Nombre maximum de tentatives HTTP (lors d'erreurs ``429`` et ``5xx``)
     - ``3``
   * - ``rag.llm.ollama.retry.base.delay.ms``
     - Delai de base du backoff exponentiel (millisecondes)
     - ``2000``

Controle de la concurrence
------------

``rag.llm.ollama.max.concurrent.requests`` permet de controler le nombre de requetes simultanees vers Ollama.
La valeur par defaut est 5. Ajustez-la en fonction des ressources du serveur Ollama.
Un nombre trop eleve de requetes simultanees peut surcharger le serveur Ollama et reduire la vitesse de reponse.

Configuration par type de prompt
======================

Dans |Fess|, les parametres du LLM peuvent etre personnalises par type de prompt.
La configuration s'ecrit dans ``fess_config.properties``.

Les parametres suivants peuvent etre configures par type de prompt :

- ``rag.llm.ollama.{promptType}.temperature`` - Temperature lors de la generation
- ``rag.llm.ollama.{promptType}.max.tokens`` - Nombre maximum de tokens
- ``rag.llm.ollama.{promptType}.context.max.chars`` - Nombre maximum de caracteres du contexte

Types de prompt disponibles :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Type de prompt
     - Description
   * - ``intent``
     - Prompt pour determiner l'intention de l'utilisateur
   * - ``evaluation``
     - Prompt d'evaluation des resultats de recherche
   * - ``unclear``
     - Prompt de reponse pour les requetes peu claires
   * - ``noresults``
     - Prompt pour le cas ou il n'y a pas de resultats de recherche
   * - ``docnotfound``
     - Prompt pour le cas ou le document n'est pas trouve
   * - ``answer``
     - Prompt de generation de reponse
   * - ``summary``
     - Prompt de generation de resume
   * - ``faq``
     - Prompt de generation de FAQ
   * - ``direct``
     - Prompt de reponse directe

Exemple de configuration::

    # Configurer la temperature lors de la generation de reponse
    rag.llm.ollama.answer.temperature=0.7

    # Configurer le nombre maximum de tokens lors de la generation de resume
    rag.llm.ollama.summary.max.tokens=2048

    # Configurer le nombre maximum de caracteres du contexte lors de la determination d'intention
    rag.llm.ollama.intent.context.max.chars=4000

Options du modele Ollama
======================

Les parametres du modele Ollama peuvent etre configures dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.ollama.top.p``
     - Valeur d'echantillonnage Top-P (0.0 a 1.0)
     - (Non defini)
   * - ``rag.llm.ollama.top.k``
     - Valeur d'echantillonnage Top-K
     - (Non defini)
   * - ``rag.llm.ollama.num.ctx``
     - Taille de la fenetre de contexte
     - (Non defini)
   * - ``rag.llm.ollama.default.*``
     - Configuration de repli par defaut
     - (Non defini)
   * - ``rag.llm.ollama.options.*``
     - Options globales
     - (Non defini)

Exemple de configuration::

    # Echantillonnage Top-P
    rag.llm.ollama.top.p=0.9

    # Echantillonnage Top-K
    rag.llm.ollama.top.k=40

    # Taille de la fenetre de contexte
    rag.llm.ollama.num.ctx=4096

Prise en charge des modeles de reflexion
==============

Lors de l'utilisation de modeles de reflexion (thinking model) tels que gemma4 ou qwen3.5, |Fess| prend en charge la configuration du budget de reflexion (thinking budget).

Configurez les elements suivants dans ``fess_config.properties`` :

::

    # Configuration du budget de reflexion
    rag.llm.ollama.thinking.budget=1024

La configuration du budget de reflexion permet de controler le nombre de tokens alloues a l'etape de "reflexion" du modele avant la generation de la reponse.

Configuration reseau
================

Configuration Docker
--------------

Le depot officiel `docker-fess <https://github.com/codelibs/docker-fess>`__
fournit un overlay Ollama (``compose-ollama.yaml``). Etapes minimales :

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    docker exec -it ollama01 ollama pull gemma4:e4b

Contenu de ``compose-ollama.yaml`` (reference pour un setup equivalent) :

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-ollama:15.7.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434 -Dfess.system.rag.llm.name=ollama"
        depends_on:
          - ollama01

      ollama01:
        image: ollama/ollama:latest
        ports:
          - "11434:11434"
        volumes:
          - ollama-data:/root/.ollama

    volumes:
      ollama-data:

Notes :

- ``FESS_PLUGINS=fess-llm-ollama:15.7.0`` fait que ``run.sh`` du conteneur telecharge et installe automatiquement le plugin JAR dans ``app/WEB-INF/plugin/``
- ``-Dfess.config.rag.chat.enabled=true`` active le mode IA
- ``-Dfess.config.rag.llm.ollama.api.url=...`` definit l'URL du serveur Ollama (utilisez le nom de service du reseau Docker Compose, par exemple ``ollama01``)
- ``-Dfess.system.rag.llm.name=ollama`` n'agit que comme valeur par defaut initiale avant qu'une valeur ne soit persistee dans OpenSearch. Apres demarrage, le parametre peut aussi etre modifie sous Administration > Systeme > General (section RAG)

.. note::
   Les variables d'environnement en majuscules de type ``RAG_CHAT_ENABLED`` ou ``RAG_LLM_NAME`` ne sont pas reconnues directement par |Fess|. Les valeurs de configuration doivent imperativement etre transmises dans ``FESS_JAVA_OPTS`` sous la forme ``-Dfess.config.<key>`` (famille ``fess_config.properties``) ou ``-Dfess.system.<key>`` (famille ``system.properties``).

Serveur Ollama distant
----------------------

Lorsqu'Ollama s'execute sur un serveur different de Fess :

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama n'a pas de fonctionnalite d'authentification par defaut, donc si vous le rendez accessible de l'exterieur,
   envisagez des mesures de securite au niveau reseau (pare-feu, VPN, etc.).

Utilisation via un proxy HTTP
=============================

Le client Ollama partage la configuration de proxy HTTP commune a |Fess|. Si une connexion au serveur Ollama doit passer par un proxy (par exemple lors de l'utilisation d'un serveur Ollama distant), specifiez les proprietes suivantes dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``http.proxy.host``
     - Nom d'hote du proxy (chaine vide pour ne pas utiliser de proxy)
     - ``""``
   * - ``http.proxy.port``
     - Numero de port du proxy
     - ``8080``
   * - ``http.proxy.username``
     - Nom d'utilisateur pour l'authentification du proxy (facultatif ; lorsqu'il est renseigne, l'authentification Basic est activee)
     - ``""``
   * - ``http.proxy.password``
     - Mot de passe pour l'authentification du proxy
     - ``""``

.. note::
   Comme Ollama s'execute generalement en local ou sur un reseau interne, la configuration d'un proxy n'est necessaire que dans des cas limites (par exemple, lors de l'utilisation d'un serveur Ollama distant uniquement accessible via un proxy d'entreprise).
   Cette configuration s'applique egalement a tous les acces HTTP de |Fess|, notamment ceux du crawler.

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
   * - ``gemma4:e4b``
     - Petit-Moyen
     - 8GB+
     - Usage general equilibre, support du thinking (par defaut)
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
    ollama run gemma4:e4b --verbose

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

4. Verifier si le plugin ``fess-llm-ollama`` est bien place dans ``app/WEB-INF/plugin/``

Modele introuvable
--------------------

**Symptome** : Log affichant "Configured model not found in Ollama"

**Solution** :

1. Verifier si le nom du modele est exact (peut necessiter le tag ``:latest``) ::

    # Verifier la liste des modeles
    ollama list

2. Telecharger le modele necessaire ::

    ollama pull gemma4:e4b

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
- :doc:`rag-chat` - Details de la fonctionnalite de mode de recherche IA
