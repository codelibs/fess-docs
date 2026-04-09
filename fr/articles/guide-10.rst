===========================================================================
Partie 10 : Exploitation stable d'un systeme de recherche -- Surveillance, sauvegarde et gestion des pannes en pratique
===========================================================================

Introduction
=============

Une fois que vous avez construit un systeme de recherche et l'avez mis a disposition des utilisateurs, il devient un systeme « qu'on ne peut plus arreter ».
Lorsque les utilisateurs s'appuient quotidiennement sur la recherche, toute indisponibilite se traduit directement par une interruption de l'activite.

Cet article fournit un guide pratique sur la surveillance, la sauvegarde et la gestion des pannes pour maintenir Fess en fonctionnement de maniere fiable.

Public cible
=============

- Administrateurs exploitant Fess dans un environnement de production
- Personnes souhaitant garantir le fonctionnement stable d'un systeme de recherche
- Personnes disposant de connaissances de base en exploitation de systemes

Vue d'ensemble de l'exploitation
=================================

L'exploitation stable de Fess repose sur les trois piliers suivants :

1. **Surveillance** : Detecter les problemes de maniere precoce
2. **Sauvegarde** : Proteger les donnees
3. **Gestion des pannes** : Retablir rapidement le service en cas de probleme

Surveillance
=============

Health Check
--------------

Fess fournit un point de terminaison de health check via l'API REST.

::

    GET http://localhost:8080/api/v1/health

En fonctionnement normal, il renvoie HTTP 200.
En appelant periodiquement ce point de terminaison depuis un outil de surveillance externe (tel que Nagios, Zabbix ou Datadog), vous pouvez surveiller l'etat operationnel de Fess.

Verification des informations systeme
--------------------------------------

Depuis [Informations systeme] dans la console d'administration, vous pouvez consulter les informations suivantes.

**Informations de collecte**

Vous pouvez consulter les resultats de la derniere execution de collecte (nombre de documents traites, nombre d'erreurs, etc.).
Utilisez cette fonctionnalite pour verifier que les collectes se terminent correctement.

**Informations systeme**

Vous pouvez consulter les versions de Fess et OpenSearch, l'utilisation memoire de la JVM, le nombre de documents dans l'index, et plus encore.

Indicateurs a surveiller
--------------------------

.. list-table:: Indicateurs de surveillance et seuils indicatifs
   :header-rows: 1
   :widths: 25 35 40

   * - Indicateur
     - Methode de verification
     - Condition d'alerte
   * - Processus Fess
     - Health API
     - Pas de reponse ou HTTP 500
   * - Cluster OpenSearch
     - Cluster Health API
     - Statut yellow / red
   * - Utilisation du heap JVM
     - Informations systeme
     - Maintenu au-dessus de 80 %
   * - Utilisation disque
     - Commandes OS
     - Au-dessus de 85 %
   * - Resultats de collecte
     - Informations de collecte
     - Augmentation soudaine des erreurs, diminution drastique du nombre traite
   * - Reponse de recherche
     - Journal de recherche
     - Augmentation significative du temps de reponse

Notification de fin de collecte
---------------------------------

Fess dispose d'une fonctionnalite qui envoie des notifications lorsque des journaux d'erreurs ou des pannes du moteur de recherche sont detectes.
En configurant un Webhook pour Slack ou Google Chat, vous pouvez etre immediatement informe de toute anomalie.

Sauvegarde
===========

Objets de sauvegarde
----------------------

Les objets de sauvegarde d'un environnement Fess se divisent en deux categories principales.

**1. Donnees de configuration**

Cela inclut les parametres de collecte, les informations utilisateur, les donnees de dictionnaire et d'autres informations configurees via la console d'administration.
Vous pouvez obtenir une sauvegarde des donnees de configuration depuis [Informations systeme] > [Sauvegarde] dans la console d'administration de Fess.

**2. Donnees d'index**

Il s'agit de l'index des documents collectes par le processus de collecte.
Utilisez la fonctionnalite de snapshot d'OpenSearch pour sauvegarder l'index.

Strategie de sauvegarde
-------------------------

.. list-table:: Strategie de sauvegarde
   :header-rows: 1
   :widths: 20 25 25 30

   * - Objet
     - Frequence
     - Duree de retention
     - Methode
   * - Donnees de configuration
     - Quotidienne
     - 30 generations
     - Fonctionnalite de sauvegarde Fess
   * - Index
     - Quotidienne
     - 7 generations
     - Snapshot OpenSearch
   * - Configuration Docker
     - A chaque modification
     - Gere par Git
     - Gestion de versions de compose.yaml

Automatisation de la sauvegarde des donnees de configuration
--------------------------------------------------------------

Vous pouvez automatiser la sauvegarde des donnees de configuration en utilisant l'API d'administration de Fess.
Configurez-la comme un travail du planificateur ou executez-la comme un travail cron externe.

Procedure de restauration
---------------------------

Il est important de verifier la procedure de restauration a l'avance pour etre prepare en cas de panne.

1. Arreter Fess
2. Restaurer les donnees de configuration (via la console d'administration ou l'API)
3. Restaurer a partir d'un snapshot OpenSearch si necessaire
4. Demarrer Fess
5. Verifier le fonctionnement

Effectuez regulierement des repetitions de la procedure de restauration pour confirmer son exactitude et connaitre le temps necessaire.

Gestion des pannes
===================

Pannes courantes et solutions
-------------------------------

**Fess ne demarre pas**

- Verifiez le fichier journal (logs/fess.log)
- Memoire JVM insuffisante : Ajustez le parametre ``-Xmx``
- Conflit de port : Verifiez si le port 8080 est utilise par un autre processus
- Echec de connexion a OpenSearch : Verifiez qu'OpenSearch est en cours d'execution

**La collecte echoue**

- Verifiez le journal des travaux ([Informations systeme] > [Journal des travaux])
- Connectivite reseau : Verifiez la connectivite vers la cible de collecte
- Erreur d'authentification : Verifiez la validite des identifiants (mot de passe, jeton)
- URLs en echec : Consultez les details dans [Informations systeme] > [URLs en echec]

**La recherche est lente**

- Verifiez l'etat du cluster OpenSearch (si le statut est yellow/red, une action est requise)
- Verifiez la taille de l'index (si elle a augmente de maniere excessive)
- Verifiez le heap JVM (si la collecte des dechets se produit frequemment)
- Si une collecte est en cours, verifiez si les performances s'ameliorent apres sa fin

**Les resultats de recherche sont obsoletes**

- Verifiez le calendrier de collecte (s'il s'execute normalement)
- Verifiez si le nombre maximal d'acces dans les parametres de collecte est insuffisant
- Verifiez si le site cible bloque les collectes (robots.txt)

Gestion des URLs en echec
----------------------------

Les URLs auxquelles il n'a pas ete possible d'acceder pendant la collecte sont enregistrees comme « URLs en echec ».
Vous pouvez les consulter dans [Informations systeme] > [URLs en echec] dans la console d'administration.

Si de nombreuses URLs en echec sont presentes, verifiez les points suivants :

- Si le serveur cible est en panne
- S'il y a des problemes de routage reseau
- Si les identifiants sont toujours valides
- Si l'intervalle de collecte est trop court, causant une charge excessive sur le serveur cible

Gestion des journaux
----------------------

Les fichiers journaux de Fess sont generes aux emplacements suivants :

- **Journal Fess** : ``logs/fess.log`` (Journal de l'application)
- **Informations de collecte** : [Informations systeme] > [Informations de collecte] dans la console d'administration
- **Journal des travaux** : [Informations systeme] > [Journal des travaux] dans la console d'administration
- **Journal de recherche** : [Informations systeme] > [Journal de recherche] dans la console d'administration

Assurez-vous que la rotation des journaux est configuree pour eviter une croissance excessive des fichiers journaux.

Liste de controle operationnelle
==================================

Voici une liste de controle des elements a verifier lors des operations courantes.

**Verifications quotidiennes**

- La collecte s'est-elle terminee avec succes ?
- Le health check renvoie-t-il des resultats normaux ?
- L'utilisation disque est-elle en dessous du seuil ?

**Verifications hebdomadaires**

- Taux de resultats nuls dans les journaux de recherche (voir Partie 8)
- Examen et traitement des URLs en echec
- Les sauvegardes sont-elles effectuees correctement ?

**Verifications mensuelles**

- Evolution de la taille de l'index
- Tendances de l'utilisation memoire JVM
- Mises a jour du dictionnaire (voir Partie 9)
- Verification des correctifs de securite

Synthese
=========

Cet article a couvert la surveillance, la sauvegarde et la gestion des pannes pour l'exploitation stable de Fess.

- Surveillance avec la Health API et la console d'administration
- Strategie de sauvegarde pour les donnees de configuration et les donnees d'index
- Schemas de pannes courants et solutions
- Listes de controle operationnelles quotidiennes, hebdomadaires et mensuelles

Pour maintenir l'attente que « la recherche fonctionne tout simplement », mettez en place un cadre operationnel proactif.

Le prochain article traitera des schemas d'integration avec les systemes existants en utilisant l'API de recherche.

References
===========

- `Fess Administration systeme <https://fess.codelibs.org/ja/15.5/admin/systeminfo.html>`__

- `Fess Sauvegarde <https://fess.codelibs.org/ja/15.5/admin/backup.html>`__
