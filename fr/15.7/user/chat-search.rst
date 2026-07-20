==============================
Mode de recherche IA
==============================

Aperçu
====

La fonctionnalité de mode de recherche IA de |Fess| vous permet de rechercher des informations
sous forme de conversation naturelle, en complément de la recherche par mots-clés traditionnelle.
Lorsque vous posez une question, l'assistant IA analyse les résultats de recherche
et génère une réponse compréhensible.

Caractéristiques du mode de recherche IA
====================

Recherche sous forme de dialogue
----------------

Au lieu de réfléchir à des mots-clés, vous pouvez poser des questions comme dans une conversation normale.

Exemples :

- "Comment installer Fess ?"
- "Comment crawler des fichiers ?"
- "Que faire si les résultats de recherche ne s'affichent pas ?"

Réponses comprenant le contexte
------------------

L'assistant IA comprend l'intention de votre question et synthétise les informations pertinentes dans sa réponse.
Il extrait les informations nécessaires de plusieurs résultats de recherche et les présente de manière organisée.

Citation des sources
----------

Les réponses de l'IA mentionnent les sources (documents de référence).
Si vous souhaitez vérifier l'exactitude de la réponse, vous pouvez consulter directement le document original.

Continuation de la conversation
----------

Il ne s'agit pas d'une seule question, vous pouvez continuer la conversation.
Vous pouvez poser des questions supplémentaires en tenant compte du contexte des questions et réponses précédentes.

Comment utiliser la recherche par chat
====================

Démarrer un chat
------------------

1. Accédez à l'écran de recherche de |Fess|
2. Cliquez sur l'icône de chat en bas à droite de l'écran
3. Le panneau de chat s'affiche

Saisir une question
--------------

1. Entrez votre question dans la zone de texte
2. Cliquez sur le bouton d'envoi ou appuyez sur Entrée
3. L'assistant IA génère une réponse

.. note::
   La génération de la réponse peut prendre quelques secondes.
   Pendant le traitement, la phase actuelle (recherche en cours, analyse en cours, etc.) s'affiche.

Vérifier la réponse
--------------

La réponse de l'assistant IA s'affiche. La réponse comprend les informations suivantes :

- **Corps de la réponse** : Réponse détaillée à votre question
- **Sources** : Liens vers les documents sur lesquels la réponse est basée (sous forme [1], [2], etc.)

Cliquez sur les liens des sources pour consulter le document original.

Continuer la conversation
------------

Si vous avez des questions supplémentaires, vous pouvez continuer à poser des questions :

- "Pouvez-vous m'en dire plus ?"
- "Y a-t-il d'autres méthodes ?"
- "Plus de détails sur XXX"

L'assistant IA répond en tenant compte du contexte de la conversation précédente.

Commencer une nouvelle conversation
------------------

Si vous souhaitez poser une question sur un autre sujet, cliquez sur le bouton "Nouveau chat".
Cela efface l'historique de conversation et démarre une nouvelle conversation.

Conseils pour poser des questions efficaces
==================

Poser des questions spécifiques
----------------

Les questions spécifiques obtiennent de meilleures réponses que les questions vagues.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Question vague
     - Question spécifique
   * - Comment configurer ?
     - Comment modifier les paramètres mémoire de Fess ?
   * - Il y a une erreur
     - J'obtiens une erreur "index non trouvé" lors de la recherche
   * - À propos du crawl
     - Comment configurer les exclusions lors du crawl d'un site web ?

Inclure le contexte
----------------

Inclure la situation ou l'objectif permet d'obtenir des réponses plus appropriées.

Bons exemples :

- "J'utilise Fess dans un environnement Docker. Comment changer l'emplacement de sauvegarde des logs ?"
- "C'est ma première utilisation de Fess. Par quoi dois-je commencer ?"

Poser des questions par étapes
----------------

Les problèmes complexes deviennent plus faciles à comprendre en posant des questions par étapes.

1. "Puis-je crawler des partages de fichiers avec Fess ?"
2. "Comment me connecter via le protocole SMB ?"
3. "Que faire pour les dossiers partagés nécessitant une authentification ?"

Questions fréquentes
============

Q: La fonctionnalité de chat ne s'affiche pas
-------------------------------

R: La fonctionnalité de chat peut ne pas être activée.
Vérifiez auprès de l'administrateur système si la fonctionnalité de mode de recherche IA est activée.

Q: La réponse met du temps à s'afficher
---------------------------------------

R: L'IA analyse les résultats de recherche et génère une réponse, ce qui peut prendre de quelques secondes à une dizaine de secondes.
Pendant le traitement, la phase actuelle ("Recherche en cours", "Analyse en cours", "Génération de la réponse", etc.) s'affiche.

Q: La source de la réponse semble incorrecte
-----------------------------------------

R: Cliquez sur le lien de la source pour vérifier le document original.
L'IA génère des réponses basées sur les résultats de recherche, mais peut parfois mal interpréter les informations.
Pour les informations importantes, nous vous recommandons de toujours vérifier le document original.

Q: La conversation précédente semble avoir été oubliée
-----------------------------------

R: La session a peut-être expiré.
Après une certaine période d'inactivité, l'historique de conversation est effacé.
Veuillez démarrer une nouvelle conversation.

Q: Je n'obtiens pas de réponse à certaines questions
---------------------------------------

R: Les possibilités suivantes sont à considérer :

- Les documents de recherche ne contiennent pas d'informations pertinentes
- La question est trop vague pour effectuer une recherche appropriée
- La limite de débit a été atteinte

Essayez de reformuler votre question ou attendez un moment avant de réessayer.

Q: Puis-je poser des questions dans une autre langue que le français ?
-------------------------------

R: Oui, selon la configuration, vous pouvez généralement poser des questions en anglais ou dans d'autres langues.
L'IA reconnaît la langue de la question et tente de répondre dans la même langue.

Notes importantes
========

Concernant les réponses de l'IA
----------------

- Les réponses de l'IA sont générées en fonction des résultats de recherche
- L'exactitude des réponses n'est pas garantie
- Pour les décisions importantes, vérifiez toujours le document original
- Pour les informations les plus récentes, consultez la documentation officielle

Concernant la confidentialité
--------------------

- Les questions saisies sont utilisées pour la recherche et le traitement par l'IA
- L'historique de conversation est supprimé après la fin de la session
- Selon la configuration du système, des logs peuvent être enregistrés

Informations de référence
========

- :doc:`search-and` - Comment utiliser la recherche AND
- :doc:`search-not` - Comment utiliser la recherche NOT
- :doc:`search-field` - Comment utiliser la recherche par champ
- :doc:`advanced-search` - Fonctionnalités de recherche avancée
