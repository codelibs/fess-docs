================
Notification des journaux
================

Aperçu
====

|Fess| dispose d'une fonctionnalité permettant de capturer automatiquement les événements de journaux de niveau ERROR ou WARN et de notifier les administrateurs.
Cette fonctionnalité permet de détecter rapidement les anomalies du système et de commencer le traitement des incidents au plus tôt.

Principales caractéristiques :

- **Canaux de notification pris en charge** : e-mail, Slack, Google Chat
- **Processus concernés** : application principale, explorateur, génération de suggestions, génération de miniatures
- **Désactivé par défaut** : fonctionnement par opt-in, une activation explicite est nécessaire

Fonctionnement
======

La notification des journaux fonctionne selon le flux suivant.

1. Le ``LogNotificationAppender`` de Log4j2 capture les événements de journaux dont le niveau est égal ou supérieur au niveau configuré.
2. Les événements capturés sont accumulés dans un tampon en mémoire (maximum 1 000 entrées).
3. Un minuteur écrit les événements du tampon dans l'index OpenSearch (``fess_log.notification_queue``) à intervalles de 30 secondes.
4. Un job planifié lit les événements depuis OpenSearch toutes les 5 minutes, les regroupe par niveau de journalisation et envoie les notifications.
5. Après l'envoi des notifications, les événements traités sont supprimés de l'index.

.. note::
   Les journaux de la fonctionnalité de notification elle-même (``LogNotificationHelper``, ``LogNotificationJob``, etc.)
   sont exclus des cibles de notification afin d'éviter les boucles infinies.

Configuration
============

Activation
------

Activation depuis l'interface d'administration
~~~~~~~~~~~~~~~~~~~~

1. Connectez-vous à l'interface d'administration.
2. Sélectionnez « Général » dans le menu « Système ».
3. Activez la case à cocher « Notification des journaux ».
4. Sélectionnez le niveau cible de notification dans « Niveau de notification des journaux » (``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. Cliquez sur le bouton « Mettre à jour ».

.. note::
   Par défaut, seul le niveau ``ERROR`` est ciblé pour la notification.
   Si vous sélectionnez ``WARN``, les niveaux ``WARN`` et ``ERROR`` seront tous deux notifiés.

Activation via les propriétés système
~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez également activer cette fonctionnalité en configurant directement les propriétés système enregistrées dans les paramètres « Général » de l'interface d'administration.

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

Configuration des destinataires
------------

Notification par e-mail
~~~~~~~~~~

Pour utiliser la notification par e-mail, la configuration suivante est nécessaire.

1. Configuration du serveur de messagerie (``fess_env.properties``) :

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. Dans les paramètres « Général » de l'interface d'administration, saisissez les adresses e-mail dans le champ « Destinataires ». Plusieurs adresses peuvent être séparées par des virgules.

Notification Slack
~~~~~~~~~~

En configurant l'URL du Incoming Webhook de Slack, vous pouvez envoyer des notifications vers un canal Slack.

Notification Google Chat
~~~~~~~~~~~~~~~~

En configurant l'URL du Webhook de Google Chat, vous pouvez envoyer des notifications vers un espace Google Chat.

Propriétés de configuration
==============

Les propriétés suivantes peuvent être configurées dans ``fess_config.properties``.

.. list-table:: Propriétés de configuration de la notification des journaux
   :header-rows: 1
   :widths: 40 15 45

   * - Propriété
     - Valeur par défaut
     - Description
   * - ``log.notification.flush.interval``
     - ``30``
     - Intervalle de vidage du tampon vers OpenSearch (en secondes)
   * - ``log.notification.buffer.size``
     - ``1000``
     - Nombre maximum d'événements conservés dans le tampon en mémoire
   * - ``log.notification.interval``
     - ``300``
     - Intervalle d'exécution du job de notification (en secondes)
   * - ``log.notification.search.size``
     - ``1000``
     - Nombre maximum d'événements récupérés depuis OpenSearch par exécution de job
   * - ``log.notification.max.display.events``
     - ``50``
     - Nombre maximum d'événements inclus dans un message de notification
   * - ``log.notification.max.message.length``
     - ``200``
     - Nombre maximum de caractères par message de journal (les caractères excédentaires sont tronqués)
   * - ``log.notification.max.details.length``
     - ``3000``
     - Nombre maximum de caractères pour la partie détails du message de notification

.. note::
   Les modifications de ces propriétés prennent effet après le redémarrage de |Fess|.

Format des messages de notification
====================

Notification par e-mail
----------

La notification par e-mail est envoyée dans le format suivant.

**Objet :**

::

    [FESS] ERROR Log Alert: hostname

**Corps :**

::

    --- Server Info ---
    Host Name: hostname

    --- Log Summary ---
    Level: ERROR
    Total: 5 event(s) in the last 300 seconds

    --- Log Details ---
    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   Les événements ERROR et WARN sont envoyés sous forme de notifications séparées pour chaque niveau.

Notification Slack / Google Chat
------------------------

Les notifications Slack et Google Chat sont envoyées sous forme de messages avec un contenu similaire.

Guide d'exploitation
==========

Configuration recommandée
--------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Environnement
     - Niveau recommandé
     - Raison
   * - Environnement de production
     - ``ERROR``
     - Notifier uniquement les erreurs critiques et réduire le bruit
   * - Environnement de staging
     - ``WARN``
     - Inclure les problèmes potentiels dans les notifications
   * - Environnement de développement
     - Désactivé
     - Consulter directement les fichiers journaux

Index OpenSearch
----------------------

La fonctionnalité de notification des journaux utilise l'index ``fess_log.notification_queue`` pour le stockage temporaire des événements.
Cet index est créé automatiquement lors de la première utilisation de la fonctionnalité.
Les événements étant supprimés après l'envoi des notifications, la taille de l'index ne devrait normalement pas devenir importante.

Dépannage
======================

Les notifications ne sont pas envoyées
------------------

1. **Vérifier l'activation**

   Vérifiez que « Notification des journaux » est activée dans les paramètres « Général » de l'interface d'administration.

2. **Vérifier les destinataires**

   Pour la notification par e-mail, vérifiez qu'une adresse e-mail est configurée dans le champ « Destinataires ».

3. **Vérifier la configuration du serveur de messagerie**

   Vérifiez que le serveur de messagerie est correctement configuré dans ``fess_env.properties``.

4. **Vérifier les journaux**

   Vérifiez les messages d'erreur liés aux notifications dans ``fess.log``.

   ::

       grep -i "notification" /var/log/fess/fess.log

Les notifications sont trop nombreuses
--------------

1. **Augmenter le niveau de journalisation**

   Changez le niveau de notification de ``WARN`` à ``ERROR``.

2. **Traiter la cause racine**

   Si des erreurs se produisent fréquemment, examinez la cause racine des erreurs.

Le contenu des notifications est tronqué
------------------------

Ajustez les propriétés suivantes.

- ``log.notification.max.details.length`` : nombre maximum de caractères pour la partie détails
- ``log.notification.max.display.events`` : nombre maximum d'événements affichés
- ``log.notification.max.message.length`` : nombre maximum de caractères par message

Informations de référence
========

- :doc:`admin-logging` - Configuration des journaux
- :doc:`setup-memory` - Configuration de la mémoire
