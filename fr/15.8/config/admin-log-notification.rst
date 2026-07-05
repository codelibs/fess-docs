=========================
Notification des journaux
=========================

Aperçu
======

|Fess| dispose d'une fonctionnalité permettant de capturer automatiquement les événements de journaux de niveau ERROR ou WARN et de notifier les administrateurs.
Cette fonctionnalité permet de détecter rapidement les anomalies du système et de commencer le traitement des incidents au plus tôt.

Principales caractéristiques :

- **Canaux de notification pris en charge** : e-mail, Slack, Google Chat
- **Processus concernés** : application principale, explorateur, génération de suggestions, génération de miniatures
- **Désactivé par défaut** : fonctionnement par opt-in, une activation explicite est nécessaire

Fonctionnement
==============

La notification des journaux fonctionne selon le flux suivant.

1. Le ``LogNotificationAppender`` de Log4j2 capture les événements de journaux dont le niveau est égal ou supérieur au niveau configuré.
2. Les événements capturés sont accumulés dans un tampon en mémoire (maximum 1 000 entrées par défaut). Lorsque le tampon dépasse sa limite, les événements les plus anciens sont supprimés en premier.
3. Un minuteur écrit les événements du tampon dans l'index OpenSearch (``fess_log.notification_queue``) à intervalles de 30 secondes.
4. Le job planifié « Log Notification » lit les événements depuis OpenSearch toutes les 5 minutes, les regroupe par niveau de journalisation et envoie une notification pour chaque niveau.
5. Après l'envoi des notifications, les événements traités sont supprimés de l'index.

.. note::
   Chaque nœud n'émet de notifications que pour les journaux qu'il a lui-même enregistrés (les événements sont filtrés par ``hostname``).
   Dans une configuration en cluster, des notifications distinctes sont envoyées pour chaque nœud.

.. note::
   Afin d'éviter les boucles infinies, les journaux des loggers liés à la fonctionnalité de notification elle-même
   (``LogNotificationAppender``, ``LogNotificationHelper``, ``LogNotificationTarget``,
   ``LogNotificationJob``, ``NotificationHelper``, ainsi que ``org.codelibs.curl`` utilisé pour
   la communication HTTP) sont exclus des cibles de notification.

Configuration
=============

Activation
----------

Activation depuis l'interface d'administration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Connectez-vous à l'interface d'administration.
2. Sélectionnez « Général » dans le menu « Système ».
3. Activez la case à cocher « Log Notification ».
4. Sélectionnez le niveau cible de notification dans « Log Notification Level » (``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. Cliquez sur le bouton « Mettre à jour ».

.. note::
   Par défaut, seul le niveau ``ERROR`` est ciblé pour la notification.
   Si vous sélectionnez ``WARN``, les niveaux ``WARN`` et ``ERROR`` seront tous deux notifiés.

Activation via les propriétés système
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vous pouvez également configurer directement les propriétés système (``system.properties``) enregistrées dans les paramètres « Général » de l'interface d'administration.

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

Configuration des destinataires
-------------------------------

Les destinataires (adresses e-mail, URL de Webhook Slack / Google Chat) sont tous configurés
dans les paramètres « Système » → « Général » de l'interface d'administration. Configurez au moins
un destinataire. Si aucun destinataire n'est configuré, le job de notification des journaux se termine
sans rien envoyer.

Notification par e-mail
~~~~~~~~~~~~~~~~~~~~~~~~

Pour utiliser la notification par e-mail, la configuration suivante est nécessaire.

1. Configuration du serveur de messagerie (``fess_env.properties``) :

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. Dans les paramètres « Général » de l'interface d'administration, saisissez les adresses e-mail dans le champ « E-mail de notification ».
   Plusieurs adresses peuvent être séparées par des virgules.

Notification Slack
~~~~~~~~~~~~~~~~~~~

Saisissez l'URL du Incoming Webhook de Slack dans le champ « Slack Webhook URLs » des paramètres « Général » de l'interface d'administration.
Plusieurs URL peuvent être séparées par des virgules ou des espaces.
Cette valeur est enregistrée dans la propriété système ``slack.webhook.urls``.

Notification Google Chat
~~~~~~~~~~~~~~~~~~~~~~~~~~

Saisissez l'URL du Webhook de Google Chat dans le champ « Google Chat Webhook URLs » des paramètres « Général » de l'interface d'administration.
Plusieurs URL peuvent être séparées par des virgules ou des espaces.
Cette valeur est enregistrée dans la propriété système ``google.chat.webhook.urls``.

.. note::
   Si vous configurez uniquement l'URL de Webhook Slack ou Google Chat sans configurer « E-mail de notification »,
   aucun e-mail n'est envoyé et seules les notifications vers Slack / Google Chat sont effectuées.
   Slack / Google Chat reçoivent en tant que message le même objet et le même corps que la notification par e-mail.

Propriétés de configuration
===========================

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
     - Période d'agrégation affichée dans le message de notification (en secondes). Valeur purement indicative qui ne correspond pas à l'intervalle réel d'exécution du job (voir la note ci-dessous).
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
   La modification de ``log.notification.flush.interval`` prend effet après le redémarrage de |Fess|.
   Les autres propriétés prennent effet dès le cycle de notification suivant.

.. note::
   ``log.notification.interval`` est la valeur utilisée pour le texte « au cours des N dernières secondes »
   affiché dans le message de notification ; elle ne modifie pas la fréquence d'exécution du job. L'intervalle
   d'exécution réel est déterminé par la configuration cron du job planifié « Log Notification »
   (5 minutes par défaut). Pour modifier l'intervalle d'exécution du job, modifiez l'expression cron de ce job
   depuis « Système » → « Planificateur », et ajustez également ``log.notification.interval`` afin que
   l'affichage corresponde à la réalité.

Format des messages de notification
===================================

Notification par e-mail
-----------------------

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
    Total: 2 event(s) in the last 300 seconds

    --- Log Details ---
    Total: 2 event(s)

    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   Les événements ERROR et WARN sont envoyés sous forme de notifications séparées pour chaque niveau.

.. note::
   Lorsque le nombre d'événements à afficher dépasse ``log.notification.max.display.events``, le début de
   la partie détails devient ``Total: N event(s) (showing M)`` et la mention ``... and X more`` est ajoutée
   à la fin. Lorsqu'un message de journal dépasse ``log.notification.max.message.length``, sa fin est tronquée
   par ``...`` ; et lorsque l'ensemble de la partie détails dépasse ``log.notification.max.details.length``,
   le reste est tronqué.

Notification Slack / Google Chat
--------------------------------

Les notifications Slack et Google Chat sont envoyées sous forme de messages avec un contenu similaire.

Guide d'exploitation
====================

Configuration recommandée
-------------------------

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
----------------

La fonctionnalité de notification des journaux utilise l'index ``fess_log.notification_queue`` pour le stockage
temporaire des événements (le nom de l'index est obtenu en ajoutant ``.notification_queue`` à la valeur de
``index.log`` (``fess_log`` par défaut)). Cet index est créé automatiquement lors de la première utilisation
de la fonctionnalité.
Les événements étant supprimés après l'envoi des notifications, la taille de l'index ne devrait normalement pas devenir importante.

.. note::
   Le nombre d'événements traités par exécution de job est limité par ``log.notification.search.size`` (1 000 par
   défaut). Les événements accumulés au-delà de cette limite sont supprimés en bloc après l'envoi des notifications
   et ne sont pas reportés aux exécutions suivantes. Dans les environnements où un grand volume de journaux est
   généré en peu de temps, augmentez ``log.notification.search.size`` selon les besoins.

Dépannage
=========

Les notifications ne sont pas envoyées
--------------------------------------

1. **Vérifier l'activation**

   Vérifiez que « Log Notification » est activée dans les paramètres « Général » de l'interface d'administration.

2. **Vérifier les destinataires**

   Vérifiez qu'au moins un destinataire (« E-mail de notification », « Slack Webhook URLs » ou
   « Google Chat Webhook URLs ») est configuré. Si aucun n'est configuré, le job affiche
   ``No notification targets configured.`` et n'envoie rien.

3. **Vérifier la configuration du serveur de messagerie**

   Si vous utilisez la notification par e-mail, vérifiez que le serveur de messagerie est correctement
   configuré dans ``fess_env.properties``.

4. **Vérifier le job planifié**

   Vérifiez que le job « Log Notification » est activé dans « Système » → « Planificateur ».
   Si ce job est désactivé, aucune notification n'est envoyée.

5. **Vérifier les journaux**

   Vérifiez les messages d'erreur liés aux notifications dans ``fess.log``.

   ::

       grep -i "notification" /var/log/fess/fess.log

Les notifications sont trop nombreuses
--------------------------------------

1. **Augmenter le niveau de journalisation**

   Changez le niveau de notification de ``WARN`` à ``ERROR``.

2. **Traiter la cause racine**

   Si des erreurs se produisent fréquemment, examinez la cause racine des erreurs.

Le contenu des notifications est tronqué
----------------------------------------

Ajustez les propriétés suivantes.

- ``log.notification.max.details.length`` : nombre maximum de caractères pour la partie détails
- ``log.notification.max.display.events`` : nombre maximum d'événements affichés
- ``log.notification.max.message.length`` : nombre maximum de caractères par message

Informations de référence
=========================

- :doc:`admin-logging` - Configuration des journaux
- :doc:`setup-memory` - Configuration de la mémoire
