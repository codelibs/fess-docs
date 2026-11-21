==========================================
Partager les sessions HTTP entre les nœuds
==========================================

Présentation
============

Par défaut, chaque nœud |Fess| conserve ses sessions HTTP dans sa propre mémoire. Si vous exécutez plusieurs nœuds |Fess| derrière un répartiteur de charge, définissez la variable d'environnement ``FESS_SESSION_STORE=opensearch`` sur chaque nœud. Les sessions sont alors conservées dans l'index ``fess_config.session`` du moteur de recherche, et un nœud peut lire une session créée par un autre nœud. Cela comprend l'état de connexion ainsi que ce qu'une opération par clé d'accès ou une connexion SSO conserve dans la session entre deux requêtes (voir :doc:`security-passkey` et :doc:`sso-saml`). Sans valeur, avec une valeur vide ou avec ``memory``, les sessions restent dans la mémoire de chaque nœud. Une valeur inconnue est signalée sur la sortie d'erreur standard et traitée comme ``memory``.

Pour l'ajout ou la suppression d'un plugin SSO, qui invalide toutes les sessions stockées, voir la note de :doc:`sso-saml`.

Enregistrement et pannes
========================

Un nœud enregistre dans le moteur de recherche les sessions qu'une requête a utilisées avant d'envoyer la réponse ; un client qui envoie sa requête suivante à un autre nœud juste après la réponse, par exemple juste après une connexion, y retrouve donc la session. Les modifications faites après le début de la réponse sont enregistrées à la fin de la requête.

Lorsque le moteur de recherche ne peut pas être lu ou écrit, la requête reçoit tout de même sa réponse et un avertissement tel que « Failed to save the session to the session store. » ou « Failed to load the session from the session store. The session is kept in memory only. » est écrit dans le journal (au plus une fois par minute). Le nœud ne conserve alors la session que dans sa propre mémoire, et les autres nœuds ne la voient pas tant qu'elle ne peut pas être de nouveau enregistrée. Lorsqu'une déconnexion ne peut pas supprimer la session stockée, le nœud refuse désormais cette session, mais les autres nœuds l'acceptent jusqu'à son expiration.

Sans ``FESS_SESSION_STORE``, chaque nœud ne conserve ses sessions que dans sa propre mémoire, et un client dirigé vers un autre nœud n'y est pas connecté. Partagez les sessions comme décrit ci-dessus, ou configurez le répartiteur de charge pour qu'il dirige toujours chaque client vers le même nœud.
