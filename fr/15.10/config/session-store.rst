==========================================
Partager les sessions HTTP entre les nœuds
==========================================

Présentation
============

Par défaut, chaque nœud |Fess| conserve ses sessions HTTP dans sa propre mémoire. Si vous exécutez plusieurs nœuds |Fess| derrière un répartiteur de charge, définissez la variable d'environnement ``FESS_SESSION_STORE=opensearch`` sur chaque nœud. Les sessions sont alors conservées dans l'index ``fess_config.session`` du moteur de recherche, et un nœud peut lire une session créée par un autre nœud. Cela comprend l'état de connexion ainsi que ce qu'une opération par clé d'accès ou une connexion SSO conserve dans la session entre deux requêtes (voir :doc:`security-passkey` et :doc:`sso-saml`). Sans valeur, avec une valeur vide ou avec ``memory``, les sessions restent dans la mémoire de chaque nœud. Une valeur inconnue est signalée sur la sortie d'erreur standard et traitée comme ``memory``.

Pour l'ajout ou la suppression d'un plugin SSO, qui invalide toutes les sessions stockées, voir la note de :doc:`sso-saml`.

Prérequis avec plusieurs nœuds
==============================

Configurez des sessions persistantes (affinité client) sur le répartiteur de charge même lorsque les sessions sont partagées, afin qu'un client soit toujours dirigé vers le même nœud.

Un nœud enregistre une session dans le moteur de recherche avant d'envoyer la réponse ; en fonctionnement normal, un autre nœud peut donc lire la session dès que le client a reçu la réponse. Ce n'est toutefois pas garanti. Lorsqu'une session ne peut pas être enregistrée, seul un avertissement est écrit dans le journal du nœud, et la requête reçoit tout de même sa réponse normale. De plus, juste après le démarrage d'un nœud, une requête qui passe à un autre nœud peut ne pas retrouver la session. Dans les deux cas, un client qui envoie sa requête suivante à un autre nœud immédiatement, par exemple juste après une connexion, peut être traité comme non connecté et recevoir ``401``. Lors des tests, cela s'est produit occasionnellement pour des requêtes envoyées juste après le démarrage d'un nœud, et plus du tout une fois le nœud échauffé. Avec des sessions persistantes, le client atteint toujours le nœud qui a créé la session, et les sessions partagées ne servent plus qu'à reprendre la session lorsque ce nœud n'est plus disponible.
