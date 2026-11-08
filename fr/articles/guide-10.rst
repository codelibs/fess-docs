=========================================================
Partie 10 : Exploitation stable d'un système de recherche
=========================================================

Introduction
=============

Une fois que vous avez construit un système de recherche et l'avez mis à disposition des utilisateurs, il devient un système « qu'on ne peut plus arrêter ».
Lorsque les utilisateurs s'appuient quotidiennement sur la recherche, toute indisponibilité se traduit directement par une interruption de l'activité.

Cet article fournit un guide pratique sur la surveillance, la sauvegarde et la gestion des pannes pour maintenir Fess en fonctionnement de manière fiable.

Public cible
=============

- Administrateurs exploitant Fess dans un environnement de production
- Personnes souhaitant garantir le fonctionnement stable d'un système de recherche
- Personnes disposant de connaissances de base en exploitation de systèmes

Vue d'ensemble de l'exploitation
=================================

L'exploitation stable de Fess repose sur les trois piliers suivants :

1. **Surveillance** : Détecter les problèmes de manière précoce
2. **Sauvegarde** : Protéger les données
3. **Gestion des pannes** : Rétablir rapidement le service en cas de problème

Surveillance
=============

Health Check
--------------

Fess fournit un point de terminaison de health check via l'API REST.

::

    GET http://localhost:8080/api/v1/health

En fonctionnement normal, il renvoie HTTP 200.
En appelant périodiquement ce point de terminaison depuis un outil de surveillance externe (tel que Nagios, Zabbix ou Datadog), vous pouvez surveiller l'état opérationnel de Fess.

Vérification des informations système
--------------------------------------

Depuis [Informations système] dans la console d'administration, vous pouvez consulter les informations suivantes.

**Informations de collecte**

Vous pouvez consulter les résultats de la dernière exécution de collecte (nombre de documents traités, nombre d'erreurs, etc.).
Utilisez cette fonctionnalité pour vérifier que les collectes se terminent correctement.

**Informations système**

Vous pouvez consulter les versions de Fess et OpenSearch, l'utilisation mémoire de la JVM, le nombre de documents dans l'index, et plus encore.

Indicateurs à surveiller
--------------------------

.. list-table:: Indicateurs de surveillance et seuils indicatifs
   :header-rows: 1
   :widths: 25 35 40

   * - Indicateur
     - Méthode de vérification
     - Condition d'alerte
   * - Processus Fess
     - Health API
     - Pas de réponse ou HTTP 500
   * - Cluster OpenSearch
     - Cluster Health API
     - Statut yellow / red
   * - Utilisation du heap JVM
     - Informations système
     - Maintenu au-dessus de 80 %
   * - Utilisation disque
     - Commandes OS
     - Au-dessus de 85 %
   * - Résultats de collecte
     - Informations de collecte
     - Augmentation soudaine des erreurs, diminution drastique du nombre traité
   * - Réponse de recherche
     - Journal de recherche
     - Augmentation significative du temps de réponse

Notification de fin de collecte
---------------------------------

Fess dispose d'une fonctionnalité qui envoie des notifications lorsque des journaux d'erreurs ou des pannes du moteur de recherche sont détectés.
En configurant un Webhook pour Slack ou Google Chat, vous pouvez être immédiatement informé de toute anomalie.

Sauvegarde
===========

Objets de sauvegarde
----------------------

Les objets de sauvegarde d'un environnement Fess se divisent en deux catégories principales.

**1. Données de configuration**

Cela inclut les paramètres de collecte, les informations utilisateur, les données de dictionnaire et d'autres informations configurées via la console d'administration.
Vous pouvez obtenir une sauvegarde des données de configuration depuis [Informations système] > [Sauvegarde] dans la console d'administration de Fess.

**2. Données d'index**

Il s'agit de l'index des documents collectés par le processus de collecte.
Utilisez la fonctionnalité de snapshot d'OpenSearch pour sauvegarder l'index.

Stratégie de sauvegarde
-------------------------

.. list-table:: Stratégie de sauvegarde
   :header-rows: 1
   :widths: 20 25 25 30

   * - Objet
     - Fréquence
     - Durée de rétention
     - Méthode
   * - Données de configuration
     - Quotidienne
     - 30 générations
     - Fonctionnalité de sauvegarde Fess
   * - Index
     - Quotidienne
     - 7 générations
     - Snapshot OpenSearch
   * - Configuration Docker
     - À chaque modification
     - Géré par Git
     - Gestion de versions de compose.yaml

Automatisation de la sauvegarde des données de configuration
--------------------------------------------------------------

Vous pouvez automatiser la sauvegarde des données de configuration en utilisant l'API d'administration de Fess.
Configurez-la comme un travail du planificateur ou exécutez-la comme un travail cron externe.

Procédure de restauration
---------------------------

Il est important de vérifier la procédure de restauration à l'avance pour être préparé en cas de panne.

1. Arrêter Fess
2. Restaurer les données de configuration (via la console d'administration ou l'API)
3. Restaurer à partir d'un snapshot OpenSearch si nécessaire
4. Démarrer Fess
5. Vérifier le fonctionnement

Effectuez régulièrement des répétitions de la procédure de restauration pour confirmer son exactitude et connaître le temps nécessaire.

Gestion des pannes
===================

Pannes courantes et solutions
-------------------------------

**Fess ne démarre pas**

- Vérifiez le fichier journal (logs/fess.log)
- Mémoire JVM insuffisante : Ajustez le paramètre ``-Xmx``
- Conflit de port : Vérifiez si le port 8080 est utilisé par un autre processus
- Échec de connexion à OpenSearch : Vérifiez qu'OpenSearch est en cours d'exécution

**La collecte échoue**

- Vérifiez le journal des travaux ([Informations système] > [Journal des travaux])
- Connectivité réseau : Vérifiez la connectivité vers la cible de collecte
- Erreur d'authentification : Vérifiez la validité des identifiants (mot de passe, jeton)
- URLs en échec : Consultez les détails dans [Informations système] > [URLs en échec]

**La recherche est lente**

- Vérifiez l'état du cluster OpenSearch (si le statut est yellow/red, une action est requise)
- Vérifiez la taille de l'index (si elle a augmenté de manière excessive)
- Vérifiez le heap JVM (si la collecte des déchets se produit fréquemment)
- Si une collecte est en cours, vérifiez si les performances s'améliorent après sa fin

**Les résultats de recherche sont obsolètes**

- Vérifiez le calendrier de collecte (s'il s'exécute normalement)
- Vérifiez si le nombre maximal d'accès dans les paramètres de collecte est insuffisant
- Vérifiez si le site cible bloque les collectes (robots.txt)

Gestion des URLs en échec
----------------------------

Les URLs auxquelles il n'a pas été possible d'accéder pendant la collecte sont enregistrées comme « URLs en échec ».
Vous pouvez les consulter dans [Informations système] > [URLs en échec] dans la console d'administration.

Si de nombreuses URLs en échec sont présentes, vérifiez les points suivants :

- Si le serveur cible est en panne
- S'il y a des problèmes de routage réseau
- Si les identifiants sont toujours valides
- Si l'intervalle de collecte est trop court, causant une charge excessive sur le serveur cible

Gestion des journaux
----------------------

Les fichiers journaux de Fess sont générés aux emplacements suivants :

- **Journal Fess** : ``logs/fess.log`` (Journal de l'application)
- **Informations de collecte** : [Informations système] > [Informations de collecte] dans la console d'administration
- **Journal des travaux** : [Informations système] > [Journal des travaux] dans la console d'administration
- **Journal de recherche** : [Informations système] > [Journal de recherche] dans la console d'administration

Assurez-vous que la rotation des journaux est configurée pour éviter une croissance excessive des fichiers journaux.

Liste de contrôle opérationnelle
==================================

Voici une liste de contrôle des éléments à vérifier lors des opérations courantes.

**Vérifications quotidiennes**

- La collecte s'est-elle terminée avec succès ?
- Le health check renvoie-t-il des résultats normaux ?
- L'utilisation disque est-elle en dessous du seuil ?

**Vérifications hebdomadaires**

- Taux de résultats nuls dans les journaux de recherche (voir Partie 8)
- Examen et traitement des URLs en échec
- Les sauvegardes sont-elles effectuées correctement ?

**Vérifications mensuelles**

- Évolution de la taille de l'index
- Tendances de l'utilisation mémoire JVM
- Mises à jour du dictionnaire (voir Partie 9)
- Vérification des correctifs de sécurité

Synthèse
=========

Cet article a couvert la surveillance, la sauvegarde et la gestion des pannes pour l'exploitation stable de Fess.

- Surveillance avec la Health API et la console d'administration
- Stratégie de sauvegarde pour les données de configuration et les données d'index
- Schémas de pannes courants et solutions
- Listes de contrôle opérationnelles quotidiennes, hebdomadaires et mensuelles

Pour maintenir l'attente que « la recherche fonctionne tout simplement », mettez en place un cadre opérationnel proactif.

Le prochain article traitera des schémas d'intégration avec les systèmes existants en utilisant l'API de recherche.

Références
===========

- `Fess Administration système <https://fess.codelibs.org/ja/15.5/admin/systeminfo.html>`__

- `Fess Sauvegarde <https://fess.codelibs.org/ja/15.5/admin/backup.html>`__
