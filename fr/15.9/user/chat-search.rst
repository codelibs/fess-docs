====================
Mode de recherche IA
====================

Aperçu
======

Le mode de recherche IA (chat RAG) de |Fess| vous permet de rechercher des informations sous une
forme conversationnelle naturelle, en complément de la recherche classique par mots-clés. Lorsque
vous saisissez une question, l'assistant IA recherche les documents pertinents et génère, à partir
de leur contenu, une réponse facile à comprendre.

.. note::
   Le mode de recherche IA est désactivé par défaut. Pour l'utiliser, un administrateur système doit
   activer la fonctionnalité et configurer un fournisseur de LLM (grand modèle de langage).
   Pour la configuration, consultez :doc:`../config/rag-chat` et :doc:`../config/llm-overview`.

Caractéristiques du mode de recherche IA
=========================================

Recherche sous forme de dialogue
---------------------------------

Plutôt que de chercher les bons mots-clés, vous pouvez poser vos questions comme dans une
conversation ordinaire.

Exemples :

- « Comment installer Fess ? »
- « Comment crawler des fichiers ? »
- « Que faire si les résultats de recherche ne s'affichent pas ? »

Réponses tenant compte du contexte
------------------------------------

L'assistant IA analyse l'intention de la question, recherche les documents pertinents, puis en
extrait les informations nécessaires à partir de plusieurs résultats de recherche afin de fournir
une réponse organisée.

Indication explicite des sources
-----------------------------------

Les documents à l'origine de la réponse sont affichés en bas de celle-ci sous la forme d'une liste
de « sources ». Chaque source est un lien numéroté ; cliquer dessus permet de consulter directement
le document original. Le corps de la réponse peut également comporter des citations sous forme de
numéros tels que ``[1]`` ou ``[2]``, qui correspondent aux numéros de la liste des sources.

Poursuite de la conversation
-------------------------------

Vous n'êtes pas limité à une seule question : vous pouvez poursuivre la conversation. L'assistant
IA répond aux questions supplémentaires en tenant compte du contexte des questions et réponses
précédentes.

Utilisation de la recherche par chat
======================================

Ouvrir le mode de recherche IA
---------------------------------

1. Ouvrez l'écran de recherche de |Fess|
2. Cliquez sur le lien « Recherche IA » (icône de robot) dans la barre de navigation en haut de
   l'écran
3. L'écran du mode de recherche IA s'affiche

.. note::
   Le lien « Recherche IA » ne s'affiche que si le mode de recherche IA est activé et qu'un
   fournisseur de LLM est disponible. Si le lien ne s'affiche pas, consultez la section
   `Foire aux questions`_.

Saisir une question
-----------------------

1. Saisissez votre question dans la zone de texte en bas de l'écran (4000 caractères maximum par
   question)
2. Cliquez sur le bouton d'envoi (icône d'avion en papier) ou appuyez sur la touche Entrée
3. L'assistant IA commence à générer une réponse

.. note::
   Pour saisir un retour à la ligne, appuyez sur Shift+Entrée au lieu de la touche Entrée.

.. note::
   La génération de la réponse peut prendre de quelques secondes à une dizaine de secondes. Pendant
   le traitement, l'étape en cours s'affiche sous forme de barre de progression (Analyse →
   Recherche → Évaluation → Récupération → Réponse), accompagnée de messages tels que
   « Réflexion en cours... », « Recherche de mots-clés... », « Vérification des résultats... »,
   « Récupération des documents... » ou « Génération de la réponse... ». Une fois la recherche
   terminée, le nombre de documents trouvés s'affiche également.

Consulter la réponse
------------------------

La réponse de l'assistant IA s'affiche. Elle comprend les informations suivantes :

- **Corps de la réponse** : la réponse à la question, mise en forme au format Markdown
- **Sources** : la liste des liens vers les documents à l'origine de la réponse (liens numérotés ;
  un clic ouvre le document original dans un nouvel onglet)

Le corps de la réponse peut contenir des numéros de citation tels que ``[1]`` ou ``[2]``, qui
correspondent aux numéros de la liste des sources. Chaque réponse dispose d'un bouton de copie
permettant de copier son contenu dans le presse-papiers.

.. note::
   L'IA n'utilise, comme base de sa réponse, que les documents parmi les résultats de recherche
   jugés les plus pertinents. Le nombre de sources peut donc être inférieur au nombre de documents
   trouvés par la recherche.

Restreindre le périmètre de recherche
-----------------------------------------

Selon le thème utilisé, le bouton « Filtre » situé en haut de l'écran permet de restreindre le
périmètre de recherche selon des critères tels que le label, le type de fichier, la date de mise à
jour ou la taille. Cela est utile lorsque vous souhaitez interroger l'IA sur un sous-ensemble précis
de documents.

Poursuivre la conversation
------------------------------

Si vous avez des questions supplémentaires, vous pouvez continuer à poser des questions :

- « Pouvez-vous m'en dire plus ? »
- « Existe-t-il d'autres méthodes ? »
- « Plus de détails sur XXX »

L'assistant IA répond en tenant compte du contexte de la conversation précédente.

Démarrer une nouvelle conversation
--------------------------------------

Pour poser une question sur un autre sujet, cliquez sur le bouton « Nouvelle conversation »
(icône +). Cela efface l'historique de la conversation en cours et permet de démarrer une nouvelle
conversation.

Conseils pour poser des questions efficaces
=============================================

Poser des questions précises
--------------------------------

Une question précise permet d'obtenir une réponse plus appropriée qu'une question vague.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Question vague
     - Question précise
   * - Comment faire pour configurer ?
     - Comment modifier les paramètres de mémoire de Fess ?
   * - J'ai une erreur
     - J'obtiens l'erreur « index introuvable » lors d'une recherche
   * - À propos du crawl
     - Comment configurer les exclusions lors du crawl d'un site web ?

Fournir du contexte
------------------------

Indiquer la situation ou l'objectif permet d'obtenir des réponses plus adaptées.

Bons exemples :

- « J'utilise Fess dans un environnement Docker. Comment changer l'emplacement de stockage des
  logs ? »
- « C'est la première fois que j'utilise Fess. Que dois-je faire en premier ? »

Poser des questions par étapes
-----------------------------------

Les problèmes complexes deviennent plus faciles à traiter lorsqu'on les aborde par étapes.

1. « Fess peut-il crawler des partages de fichiers ? »
2. « Comment se connecter via le protocole SMB ? »
3. « Que faire pour un dossier partagé nécessitant une authentification ? »

Foire aux questions
======================

Q : Le mode de recherche IA ne s'affiche pas
------------------------------------------------

R : Il est possible que le mode de recherche IA ne soit pas activé. Le lien « Recherche IA » ne
s'affiche que si la fonctionnalité est activée (``rag.chat.enabled=true``) et qu'un fournisseur de
LLM (OpenAI, Gemini, Ollama, etc.) est configuré et disponible. Demandez à votre administrateur
système de vérifier que le mode de recherche IA est activé et que le fournisseur de LLM est
correctement configuré (pour plus de détails, consultez :doc:`../config/rag-chat`).

Q : La réponse met du temps à s'afficher
--------------------------------------------

R : L'IA analyse la question, recherche puis évalue les documents avant de générer une réponse, ce
qui peut prendre de quelques secondes à une dizaine de secondes. Pendant le traitement, l'étape en
cours s'affiche (« Réflexion en cours... », « Recherche de mots-clés... »,
« Vérification des résultats... », « Récupération des documents... »,
« Génération de la réponse... »).

Q : Les sources semblent incorrectes
-----------------------------------------

R : Cliquez sur les liens des sources pour vérifier le document original. L'IA génère sa réponse à
partir des résultats de recherche, mais son interprétation peut parfois être erronée. Pour toute
information importante, il est recommandé de toujours la vérifier dans le document original.

Q : La conversation précédente semble avoir été oubliée
------------------------------------------------------------

R : Il est possible que la session de conversation ait expiré. Après une certaine durée
d'inactivité (30 minutes par défaut), l'historique de la conversation est effacé. De plus,
l'historique de conversation est conservé temporairement en mémoire sur le serveur : il est donc
également perdu en cas de redémarrage du serveur. Dans ce cas, démarrez une nouvelle conversation.

.. note::
   La « session » évoquée ici est la session de conversation du mode de recherche IA ; elle est
   distincte de la session de connexion à |Fess|.

Q : Je n'obtiens pas de réponse à une question précise
------------------------------------------------------------

R : Plusieurs causes sont possibles :

- les documents recherchés ne contiennent pas d'information pertinente
- la question est trop vague pour permettre une recherche appropriée
- la limite de débit a été atteinte (dépassement du nombre maximal de requêtes par minute ou du
  nombre maximal d'exécutions simultanées)

Reformulez votre question ou patientez un moment avant de réessayer.

Q : Y a-t-il une limite au nombre de caractères que je peux saisir ?
--------------------------------------------------------------------------

R : Oui, 4000 caractères maximum par question. Un compteur de caractères s'affiche sous la zone de
texte et passe en alerte lorsque la limite approche. Pour une question longue, concentrez-vous sur
l'essentiel afin de la raccourcir.

Q : Puis-je poser des questions dans une langue autre que le japonais ?
--------------------------------------------------------------------------

R : Oui, dans la plupart des cas, vous pouvez poser vos questions en anglais ou dans d'autres
langues. L'IA tente de répondre dans la même langue que celle du navigateur ou de l'affichage de
l'écran, dans la mesure du possible. Il s'agit toutefois d'un traitement au mieux (best effort) :
selon les cas, la réponse peut ne pas être dans la langue attendue.

Remarques importantes
=========================

À propos des réponses de l'IA
----------------------------------

- les réponses de l'IA sont générées à partir des résultats de recherche
- l'exactitude des réponses n'est pas garantie
- pour toute décision importante, vérifiez toujours le document original (la source)
- pour les informations les plus récentes, consultez la documentation officielle

À propos de la confidentialité
------------------------------------

- les questions saisies sont utilisées pour la recherche et pour le traitement par l'IA du
  fournisseur de LLM configuré
- si un service LLM externe est configuré (OpenAI, Gemini, etc.), le contenu des questions et des
  résultats de recherche est transmis à ce service ; si vous souhaitez un traitement strictement
  interne, demandez à votre administrateur d'utiliser un fournisseur fonctionnant localement
  (Ollama, par exemple)
- l'historique de conversation est conservé temporairement en mémoire sur le serveur ; il est
  supprimé lors de l'expiration de la session, de l'exécution de « Nouvelle conversation » ou d'un
  redémarrage du serveur
- comme pour la recherche classique, le contrôle d'accès par rôle (permission) et par label
  s'applique : les documents non consultables par l'utilisateur ne peuvent pas servir de base à la
  réponse
- selon la configuration du système, des journaux peuvent être enregistrés

Informations de référence
===============================

- :doc:`../config/rag-chat` - Configuration du mode de recherche IA (pour les administrateurs)
- :doc:`../config/llm-overview` - Configuration des fournisseurs de LLM
- :doc:`../api/api-chat` - Chat API (utilisation programmatique)
- :doc:`search-and` - Utilisation de la recherche AND
- :doc:`search-not` - Utilisation de la recherche NOT
- :doc:`search-field` - Utilisation de la recherche par champ
- :doc:`advanced-search` - Fonctionnalités de recherche avancée
