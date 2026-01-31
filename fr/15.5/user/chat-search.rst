==========================
Recherche par chat IA
==========================

Apercu
====

La fonctionnalite de recherche par chat IA de |Fess| vous permet de rechercher des informations
sous forme de conversation naturelle, en complement de la recherche par mots-cles traditionnelle.
Lorsque vous posez une question, l'assistant IA analyse les resultats de recherche
et genere une reponse comprehensible.

Caracteristiques de la recherche par chat IA
====================

Recherche sous forme de dialogue
----------------

Au lieu de reflechir a des mots-cles, vous pouvez poser des questions comme dans une conversation normale.

Exemples :

- "Comment installer Fess ?"
- "Comment crawler des fichiers ?"
- "Que faire si les resultats de recherche ne s'affichent pas ?"

Reponses comprenant le contexte
------------------

L'assistant IA comprend l'intention de votre question et synthetise les informations pertinentes dans sa reponse.
Il extrait les informations necessaires de plusieurs resultats de recherche et les presente de maniere organisee.

Citation des sources
----------

Les reponses de l'IA mentionnent les sources (documents de reference).
Si vous souhaitez verifier l'exactitude de la reponse, vous pouvez consulter directement le document original.

Continuation de la conversation
----------

Il ne s'agit pas d'une seule question, vous pouvez continuer la conversation.
Vous pouvez poser des questions supplementaires en tenant compte du contexte des questions et reponses precedentes.

Comment utiliser la recherche par chat
====================

Demarrer un chat
------------------

1. Accedez a l'ecran de recherche de |Fess|
2. Cliquez sur l'icone de chat en bas a droite de l'ecran
3. Le panneau de chat s'affiche

Saisir une question
--------------

1. Entrez votre question dans la zone de texte
2. Cliquez sur le bouton d'envoi ou appuyez sur Entree
3. L'assistant IA genere une reponse

.. note::
   La generation de la reponse peut prendre quelques secondes.
   Pendant le traitement, la phase actuelle (recherche en cours, analyse en cours, etc.) s'affiche.

Verifier la reponse
--------------

La reponse de l'assistant IA s'affiche. La reponse comprend les informations suivantes :

- **Corps de la reponse** : Reponse detaillee a votre question
- **Sources** : Liens vers les documents sur lesquels la reponse est basee (sous forme [1], [2], etc.)

Cliquez sur les liens des sources pour consulter le document original.

Continuer la conversation
------------

Si vous avez des questions supplementaires, vous pouvez continuer a poser des questions :

- "Pouvez-vous m'en dire plus ?"
- "Y a-t-il d'autres methodes ?"
- "Plus de details sur XXX"

L'assistant IA repond en tenant compte du contexte de la conversation precedente.

Commencer une nouvelle conversation
------------------

Si vous souhaitez poser une question sur un autre sujet, cliquez sur le bouton "Nouveau chat".
Cela efface l'historique de conversation et demarre une nouvelle conversation.

Conseils pour poser des questions efficaces
==================

Poser des questions specifiques
----------------

Les questions specifiques obtiennent de meilleures reponses que les questions vagues.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Question vague
     - Question specifique
   * - Comment configurer ?
     - Comment modifier les parametres memoire de Fess ?
   * - Il y a une erreur
     - J'obtiens une erreur "index non trouve" lors de la recherche
   * - A propos du crawl
     - Comment configurer les exclusions lors du crawl d'un site web ?

Inclure le contexte
----------------

Inclure la situation ou l'objectif permet d'obtenir des reponses plus appropriees.

Bons exemples :

- "J'utilise Fess dans un environnement Docker. Comment changer l'emplacement de sauvegarde des logs ?"
- "C'est ma premiere utilisation de Fess. Par quoi dois-je commencer ?"

Poser des questions par etapes
----------------

Les problemes complexes deviennent plus faciles a comprendre en posant des questions par etapes.

1. "Puis-je crawler des partages de fichiers avec Fess ?"
2. "Comment me connecter via le protocole SMB ?"
3. "Que faire pour les dossiers partages necessitant une authentification ?"

Questions frequentes
============

Q: La fonctionnalite de chat ne s'affiche pas
-------------------------------

R: La fonctionnalite de chat peut ne pas etre activee.
Verifiez aupres de l'administrateur systeme si la fonctionnalite de mode IA est activee.

Q: La reponse met du temps a s'afficher
---------------------------------------

R: L'IA analyse les resultats de recherche et genere une reponse, ce qui peut prendre de quelques secondes a une dizaine de secondes.
Pendant le traitement, la phase actuelle ("Recherche en cours", "Analyse en cours", "Generation de la reponse", etc.) s'affiche.

Q: La source de la reponse semble incorrecte
-----------------------------------------

R: Cliquez sur le lien de la source pour verifier le document original.
L'IA genere des reponses basees sur les resultats de recherche, mais peut parfois mal interpreter les informations.
Pour les informations importantes, nous vous recommandons de toujours verifier le document original.

Q: La conversation precedente semble avoir ete oubliee
-----------------------------------

R: La session a peut-etre expire.
Apres une certaine periode d'inactivite, l'historique de conversation est efface.
Veuillez demarrer une nouvelle conversation.

Q: Je n'obtiens pas de reponse a certaines questions
---------------------------------------

R: Les possibilites suivantes sont a considerer :

- Les documents de recherche ne contiennent pas d'informations pertinentes
- La question est trop vague pour effectuer une recherche appropriee
- La limite de debit a ete atteinte

Essayez de reformuler votre question ou attendez un moment avant de reessayer.

Q: Puis-je poser des questions dans une autre langue que le francais ?
-------------------------------

R: Oui, selon la configuration, vous pouvez generalement poser des questions en anglais ou dans d'autres langues.
L'IA reconnait la langue de la question et tente de repondre dans la meme langue.

Notes importantes
========

Concernant les reponses de l'IA
----------------

- Les reponses de l'IA sont generees en fonction des resultats de recherche
- L'exactitude des reponses n'est pas garantie
- Pour les decisions importantes, verifiez toujours le document original
- Pour les informations les plus recentes, consultez la documentation officielle

Concernant la confidentialite
--------------------

- Les questions saisies sont utilisees pour la recherche et le traitement par l'IA
- L'historique de conversation est supprime apres la fin de la session
- Selon la configuration du systeme, des logs peuvent etre enregistres

Informations de reference
========

- :doc:`search-and` - Comment utiliser la recherche AND
- :doc:`search-not` - Comment utiliser la recherche NOT
- :doc:`search-field` - Comment utiliser la recherche par champ
- :doc:`advanced-search` - Fonctionnalites de recherche avancee
