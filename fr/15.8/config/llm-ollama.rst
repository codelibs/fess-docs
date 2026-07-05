==========================
Configuration Ollama
==========================

Apercu
======

Ollama est une plateforme open source permettant d'executer des grands modeles de langage (LLM) en local.
La fonctionnalite d'integration Ollama de |Fess| est fournie sous forme de plugin ``fess-llm-ollama``, et convient a une utilisation en environnement prive.

L'utilisation d'Ollama permet d'utiliser la fonctionnalite du mode de recherche IA sans envoyer de donnees a l'exterieur.

Caracteristiques principales
-----------------------------

- **Execution locale** : Les donnees ne sont pas envoyees a l'exterieur, garantissant la confidentialite
- **Modeles varies** : Prise en charge de nombreux modeles dont Llama, Mistral, Gemma, CodeLlama
- **Efficacite des couts** : Pas de cout API (seulement les couts materiels)
- **Personnalisation** : Possibilite d'utiliser des modeles affines independamment

Modeles pris en charge
-----------------------

Principaux modeles disponibles avec Ollama :

- ``llama3.3:70b`` - Llama 3.3 de Meta (70B parametres)
- ``gemma4:e4b`` - Gemma 4 de Google (E4B parametres, par defaut)
- ``mistral:7b`` - Mistral de Mistral AI (7B parametres)
- ``codellama:13b`` - Code Llama de Meta (13B parametres)
- ``phi3:3.8b`` - Phi-3 de Microsoft (3.8B parametres)

.. note::
   Pour la derniere liste des modeles disponibles, consultez `Ollama Library <https://ollama.com/library>`__.

Prerequis
=========

Avant d'utiliser Ollama, verifiez les points suivants.

1. **Installation d'Ollama** : Telechargez et installez depuis `https://ollama.com/ <https://ollama.com/>`__
2. **Telechargement du modele** : Telechargez le modele a utiliser dans Ollama
3. **Demarrage du serveur Ollama** : Verifiez qu'Ollama fonctionne

Installation d'Ollama
---------------------

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
------------------------

::

    # Telecharger le modele par defaut (Gemma 4 E4B)
    ollama pull gemma4:e4b

    # Telecharger Llama 3.3
    ollama pull llama3.3:70b

    # Verifier le fonctionnement du modele
    ollama run gemma4:e4b "Hello, how are you?"

Installation du plugin
======================

La fonctionnalite d'integration Ollama est fournie sous forme de plugin.
Pour utiliser Ollama, l'installation du plugin ``fess-llm-ollama`` est necessaire.

1. Telechargez `fess-llm-ollama-15.8.0.jar`.
2. Placez-le dans le repertoire ``app/WEB-INF/plugin/`` du repertoire d'installation de |Fess|.

::

    cp fess-llm-ollama-15.8.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Redemarrez |Fess|.

.. note::
   La version du plugin doit correspondre a la version de |Fess|.

Configuration de base
=====================

Les configurations LLM sont reparties dans plusieurs fichiers de configuration.

Configuration minimale
----------------------

``system.properties`` (configurable egalement via Administration > Systeme > General) :

::

    # Definir le fournisseur LLM sur Ollama
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

    # URL d'Ollama (environnement local)
    rag.llm.ollama.api.url=http://localhost:11434

    # Modele a utiliser
    rag.llm.ollama.model=gemma4:e4b

.. note::
   La configuration du fournisseur LLM peut egalement etre effectuee via l'administration (Administration > Systeme > General) en configurant ``rag.llm.name``.

Configuration recommandee (environnement de production)
-------------------------------------------------------

``system.properties`` (configurable egalement via Administration > Systeme > General) :

::

    # Configuration du fournisseur LLM
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

    # URL d'Ollama
    rag.llm.ollama.api.url=http://localhost:11434

    # Configuration du modele (utiliser un grand modele)
    rag.llm.ollama.model=llama3.3:70b

    # Configuration du timeout (augmente pour les grands modeles)
    rag.llm.ollama.timeout=120000

    # Controle du nombre de requetes simultanees
    rag.llm.ollama.max.concurrent.requests=5

Elements de configuration
=========================

Tous les elements de configuration disponibles pour le client Ollama. Tous sauf ``rag.llm.name`` se configurent dans ``fess_config.properties``.

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
     - Intervalle de verification de disponibilite (secondes). Une valeur inferieure ou egale a ``0`` desactive la verification periodique de disponibilite
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

Configuration avancee
---------------------

Elements de configuration avances relatifs a l'historique et a la taille du contexte.

.. list-table::
   :header-rows: 1
   :widths: 45 35 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.ollama.chat.evaluation.description.max.chars``
     - Nombre maximum de caracteres de la description lors de l'evaluation
     - ``500``
   * - ``rag.llm.ollama.history.max.chars``
     - Nombre maximum de caracteres de l'historique de conversation
     - ``4000``
   * - ``rag.llm.ollama.intent.history.max.messages``
     - Nombre maximum de messages dans l'historique lors de la determination d'intention
     - ``6``
   * - ``rag.llm.ollama.intent.history.max.chars``
     - Nombre maximum de caracteres dans l'historique lors de la determination d'intention
     - ``3000``
   * - ``rag.llm.ollama.history.assistant.max.chars``
     - Nombre maximum de caracteres de l'historique des reponses de l'assistant
     - ``500``
   * - ``rag.llm.ollama.history.assistant.summary.max.chars``
     - Nombre maximum de caracteres de l'historique des resumes de l'assistant
     - ``500``

Controle de la concurrence
--------------------------

``rag.llm.ollama.max.concurrent.requests`` permet de controler le nombre de requetes simultanees vers Ollama.
La valeur par defaut est 5. Ajustez-la en fonction des ressources du serveur Ollama.
Un nombre trop eleve de requetes simultanees peut surcharger le serveur Ollama et reduire la vitesse de reponse.

Configuration par type de prompt
=================================

Dans |Fess|, les parametres du LLM peuvent etre personnalises par type de prompt.
La configuration s'ecrit dans ``fess_config.properties``.

Les parametres suivants peuvent etre configures par type de prompt :

- ``rag.llm.ollama.{promptType}.temperature`` - Temperature lors de la generation
- ``rag.llm.ollama.{promptType}.max.tokens`` - Nombre maximum de tokens (mappe sur ``num_predict`` dans l'API Ollama)
- ``rag.llm.ollama.{promptType}.context.max.chars`` - Nombre maximum de caracteres du contexte
- ``rag.llm.ollama.{promptType}.thinking.budget`` - Budget de reflexion (controle de la reflexion en forme booleenne ; voir « Prise en charge des modeles de reflexion »)
- ``rag.llm.ollama.{promptType}.thinking.level`` - Niveau de reflexion (chaine de caracteres ``high`` / ``medium`` / ``low`` ; voir « Prise en charge des modeles de reflexion »)
- ``rag.llm.ollama.{promptType}.top.p`` - Valeur d'echantillonnage Top-P
- ``rag.llm.ollama.{promptType}.top.k`` - Valeur d'echantillonnage Top-K
- ``rag.llm.ollama.{promptType}.num.ctx`` - Taille de la fenetre de contexte

Chaque parametre est resolu dans l'ordre suivant : ``rag.llm.ollama.{promptType}.<param>`` (configuration specifique au type de prompt) → ``rag.llm.ollama.default.<param>`` (repli commun a tous les types de prompt) → valeur par defaut codee en dur pour chaque type de prompt. Les valeurs explicitement specifiees dans la requete sont toujours prioritaires.

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
   * - ``queryregeneration``
     - Prompt de regeneration de requete

Chaque type de prompt dispose de valeurs par defaut codees en dur qui s'appliquent si aucune configuration n'est fournie.

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Type de prompt
     - temperature
     - max.tokens
     - thinking.budget
     - context.max.chars
   * - ``intent``
     - ``0.1``
     - ``256``
     - ``0``
     - ``6000``
   * - ``evaluation``
     - ``0.1``
     - ``512``
     - ``0``
     - ``6000``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - (non defini)
     - ``10000``
   * - ``summary``
     - ``0.3``
     - ``8192``
     - (non defini)
     - ``10000``
   * - ``faq``
     - ``0.7``
     - ``4096``
     - (non defini)
     - ``6000``
   * - ``direct``
     - ``0.7``
     - ``4096``
     - (non defini)
     - ``6000``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``
     - ``6000``

Exemple de configuration ::

    # Configurer la temperature lors de la generation de reponse
    rag.llm.ollama.answer.temperature=0.7

    # Configurer le nombre maximum de tokens lors de la generation de resume
    rag.llm.ollama.summary.max.tokens=2048

    # Configurer le nombre maximum de caracteres du contexte lors de la determination d'intention
    rag.llm.ollama.intent.context.max.chars=4000

Options du modele Ollama
========================

Les parametres du modele Ollama peuvent etre configures dans ``fess_config.properties``.
En utilisant le format ``rag.llm.ollama.default.<param>``, la valeur est utilisee comme repli commun a tous les types de prompt.
Le repli via ``default`` s'applique non seulement a ``top.p`` / ``top.k`` / ``num.ctx``, mais aussi a ``temperature`` / ``max.tokens`` / ``thinking.budget`` / ``thinking.level``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.ollama.default.top.p``
     - Valeur d'echantillonnage Top-P (0.0 a 1.0). Peut etre remplacee par type de prompt avec ``rag.llm.ollama.{promptType}.top.p``
     - (non defini)
   * - ``rag.llm.ollama.default.top.k``
     - Valeur d'echantillonnage Top-K. Peut etre remplacee par type de prompt avec ``rag.llm.ollama.{promptType}.top.k``
     - (non defini)
   * - ``rag.llm.ollama.default.num.ctx``
     - Taille de la fenetre de contexte. Peut etre remplacee par type de prompt avec ``rag.llm.ollama.{promptType}.num.ctx``
     - (non defini)
   * - ``rag.llm.ollama.default.temperature``
     - Valeur de repli de la temperature de generation. Peut etre remplacee par type de prompt avec ``rag.llm.ollama.{promptType}.temperature``
     - (non defini)
   * - ``rag.llm.ollama.default.max.tokens``
     - Valeur de repli du nombre maximum de tokens. Peut etre remplacee par type de prompt avec ``rag.llm.ollama.{promptType}.max.tokens``
     - (non defini)
   * - ``rag.llm.ollama.default.thinking.budget``
     - Valeur de repli du budget de reflexion. Peut etre remplacee par type de prompt avec ``rag.llm.ollama.{promptType}.thinking.budget``
     - (non defini)
   * - ``rag.llm.ollama.default.thinking.level``
     - Valeur de repli du niveau de reflexion (``high`` / ``medium`` / ``low``). Peut etre remplacee par type de prompt avec ``rag.llm.ollama.{promptType}.thinking.level``
     - (non defini)
   * - ``rag.llm.ollama.options.*``
     - Options globales transmises directement a l'API Ollama. Le suffixe est utilise comme nom d'option (ex. : ``rag.llm.ollama.options.repeat_penalty=1.1``). Les valeurs sont automatiquement converties en Integer, Double, Boolean ou String
     - (non defini)

Exemple de configuration ::

    # Echantillonnage Top-P par defaut (commun a tous les types de prompt)
    rag.llm.ollama.default.top.p=0.9

    # Echantillonnage Top-K par defaut
    rag.llm.ollama.default.top.k=40

    # Taille de la fenetre de contexte par defaut
    rag.llm.ollama.default.num.ctx=4096

    # Modifier Top-P uniquement pour la generation de reponse
    rag.llm.ollama.answer.top.p=0.95

    # Options globales (transmises directement a l'API Ollama)
    rag.llm.ollama.options.repeat_penalty=1.1

Prise en charge des modeles de reflexion
=========================================

Lors de l'utilisation de modeles de reflexion (thinking model) tels que gemma4 ou qwen3, |Fess| prend en charge la configuration du budget de reflexion (thinking budget).

Le budget de reflexion se configure par type de prompt dans ``fess_config.properties`` :

::

    # Configuration du budget de reflexion lors de la generation de reponse
    rag.llm.ollama.answer.thinking.budget=1024

    # Configuration du budget de reflexion lors de la generation de resume
    rag.llm.ollama.summary.thinking.budget=1024

La configuration du budget de reflexion permet de controler le nombre de tokens alloues a l'etape de « reflexion » du modele avant la generation de la reponse.

.. note::
   Avec Ollama, le budget de reflexion est converti en indicateur booleen (``think: true`` si la valeur est superieure a 0, ``think: false`` si la valeur est 0). Le controle fin par nombre de tokens n'est pas disponible en raison des contraintes de l'API Ollama.

Niveau de reflexion (thinking level)
--------------------------------------

Certains modeles comme gpt-oss ignorent l'indicateur ``think`` booleen et requierent la specification du niveau de reflexion sous forme de chaine de caracteres ``high`` / ``medium`` / ``low``.
Pour ces modeles, utilisez ``rag.llm.ollama.{promptType}.thinking.level``.

::

    # Configuration du niveau de reflexion lors de la generation de reponse
    rag.llm.ollama.answer.thinking.level=high

    # Configuration du niveau de reflexion lors de la generation de resume
    rag.llm.ollama.summary.thinking.level=medium

Les valeurs acceptees pour ``thinking.level`` sont ``high`` / ``medium`` / ``low`` (insensible a la casse). Une valeur non valide est ignoree et un avertissement est emis dans les journaux.

.. note::
   Si ``thinking.level`` (forme chaine) et ``thinking.budget`` (forme booleenne) sont tous les deux configures, ``thinking.level`` est prioritaire. Utilisez ``thinking.level`` pour les modeles de la famille GPT-OSS, et ``thinking.budget`` pour les autres modeles de reflexion.

Configuration reseau
====================

Configuration Docker
--------------------

Le depot officiel `docker-fess <https://github.com/codelibs/docker-fess>`__ de |Fess| inclut un overlay Ollama ``compose-ollama.yaml``. Les etapes minimales sont les suivantes.

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    docker exec -it ollama01 ollama pull gemma4:e4b

``compose-ollama.yaml`` est configure pour utiliser un GPU NVIDIA (NVIDIA Container Toolkit requis). Son contenu est le suivant.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-ollama:15.8.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434"
        depends_on:
          - ollama01

      ollama01:
        image: ollama/ollama:latest
        container_name: ollama01
        ports:
          - "11434:11434"
        volumes:
          - ollama-data:/root/.ollama
        networks:
          - search_net
        restart: unless-stopped
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

    volumes:
      ollama-data:
        driver: local

Points importants :

- ``FESS_PLUGINS=fess-llm-ollama:15.8.0`` fait que le script de demarrage recupere automatiquement le JAR du plugin et le place dans ``app/WEB-INF/plugin/`` (adaptez la version a votre installation |Fess|)
- ``-Dfess.config.rag.chat.enabled=true`` active le mode de recherche IA
- ``-Dfess.config.rag.llm.ollama.api.url=...`` specifie l'URL du serveur Ollama (dans le reseau Docker Compose, le nom de service tel que ``ollama01`` est utilise pour la resolution)
- Le fournisseur LLM par defaut (``rag.llm.name``) etant ``ollama``, aucune specification explicite n'est necessaire si Ollama est le seul fournisseur utilise. En cas de basculement depuis un autre fournisseur, ajoutez ``-Dfess.system.rag.llm.name=ollama`` dans ``FESS_JAVA_OPTS``, ou configurez-le apres le demarrage dans l'administration sous « Systeme > General », section RAG
- Le bloc ``deploy.resources.reservations.devices`` configure l'utilisation du GPU. Si vous n'utilisez pas de GPU (execution CPU uniquement), supprimez ce bloc

.. note::
   Les variables d'environnement en majuscules de type ``RAG_CHAT_ENABLED`` ou ``RAG_LLM_NAME`` ne sont pas reconnues directement par |Fess|. Les valeurs de configuration doivent imperativement etre transmises dans ``FESS_JAVA_OPTS`` sous la forme ``-Dfess.config.<key>`` (famille ``fess_config.properties``) ou ``-Dfess.system.<key>`` (famille ``system.properties``).

Serveur Ollama distant
----------------------

Lorsqu'Ollama s'execute sur un serveur different de Fess :

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama n'a pas de fonctionnalite d'authentification par defaut. Si vous le rendez accessible de l'exterieur,
   envisagez des mesures de securite au niveau reseau (pare-feu, VPN, etc.).

Utilisation via un proxy HTTP
==============================

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
================================

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
     - Usage general equilibre, support du mode reflexion (par defaut)
   * - ``mistral:7b``
     - Moyen
     - 8GB+
     - Reponses de haute qualite requises
   * - ``llama3.3:70b``
     - Grand
     - 48GB+
     - Reponses de meilleure qualite, raisonnement complexe

Prise en charge GPU
-------------------

Ollama prend en charge l'acceleration GPU. L'utilisation d'un GPU NVIDIA
ameliore considerablement la vitesse d'inference.

::

    # Verification de la prise en charge GPU
    ollama run gemma4:e4b --verbose

Depannage
=========

Erreur de connexion
-------------------

**Symptome** : Erreur dans la fonctionnalite de chat, LLM affiche comme indisponible

**Points a verifier** :

1. Verifier si Ollama fonctionne ::

    curl http://localhost:11434/api/tags

2. Verifier si le modele est telecharge ::

    ollama list

3. Verifier les parametres du pare-feu

4. Verifier si le plugin ``fess-llm-ollama`` est bien place dans ``app/WEB-INF/plugin/``

Modele introuvable
------------------

**Symptome** : Le journal affiche « Configured model not found »

**Solution** :

1. Verifier si le nom du modele est exact (peut necessiter le tag ``:latest``) ::

    # Verifier la liste des modeles
    ollama list

2. Telecharger le modele necessaire ::

    ollama pull gemma4:e4b

Timeout
-------

**Symptome** : La requete expire

**Solution** :

1. Augmenter le temps de timeout ::

    rag.llm.ollama.timeout=120000

2. Envisager un modele plus petit ou un environnement GPU

Configuration de debogage
--------------------------

Pour investiguer les problemes, ajustez le niveau de log de |Fess| pour afficher des logs detailles lies a Ollama.

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

Informations de reference
==========================

- `Site officiel Ollama <https://ollama.com/>`__
- `Bibliotheque de modeles Ollama <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - Apercu de l'integration LLM
- :doc:`rag-chat` - Details de la fonctionnalite de mode de recherche IA
