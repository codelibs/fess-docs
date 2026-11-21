===================================
Sharing HTTP Sessions Between Nodes
===================================

Overview
========

By default, each |Fess| node keeps its HTTP sessions in its own memory. When you run several |Fess| nodes behind a load balancer, set the environment variable ``FESS_SESSION_STORE=opensearch`` on every node. The sessions are then kept in the ``fess_config.session`` index of the search engine, and a node can read a session that another node created. This includes the login state and what a passkey ceremony or an SSO login keeps in the session between two requests (see :doc:`security-passkey` and :doc:`sso-saml`). With no value, an empty value or ``memory``, the sessions stay in the memory of each node. An unknown value is reported on the standard error output and treated as ``memory``.

For adding or removing an SSO plugin, which invalidates every stored session, see the note in :doc:`sso-saml`.

Prerequisite for Several Nodes
==============================

Set up sticky sessions (client affinity) on the load balancer even when the sessions are shared, so that a client is always sent to the same node.

A node saves a session to the search engine before it sends the response, so in normal operation another node can read the session as soon as the client has received the response. This is not guaranteed, however. When a session cannot be saved, only a warning is written to the log of the node, and the request itself is still answered normally. Also, right after a node has started, a request that moves to another node may not find the session. In both cases a client that sends its next request to another node at once, for example directly after a login, can be treated as not logged in and receive ``401``. In tests this happened occasionally for requests sent right after a node had started, and no longer after the node had warmed up. With sticky sessions the client always reaches the node that created the session, and the shared sessions are only needed to carry the session over when that node is no longer available.
