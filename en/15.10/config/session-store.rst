===================================
Sharing HTTP Sessions Between Nodes
===================================

Overview
========

By default, each |Fess| node keeps its HTTP sessions in its own memory. When you run several |Fess| nodes behind a load balancer, set the environment variable ``FESS_SESSION_STORE=opensearch`` on every node. The sessions are then kept in the ``fess_config.session`` index of the search engine, and a node can read a session that another node created. This includes the login state and what a passkey ceremony or an SSO login keeps in the session between two requests (see :doc:`security-passkey` and :doc:`sso-saml`). With no value, an empty value or ``memory``, the sessions stay in the memory of each node. An unknown value is reported on the standard error output and treated as ``memory``.

For adding or removing an SSO plugin, which invalidates every stored session, see the note in :doc:`sso-saml`.

Saving and Failures
===================

A node saves the sessions that a request touched to the search engine before it sends the response, so a client that sends its next request to another node right after the response, for example directly after a login, finds the session there. Changes made after the response has been started are saved at the end of the request.

When the search engine cannot be read or written, the request is still answered, and a warning such as "Failed to save the session to the session store." or "Failed to load the session from the session store. The session is kept in memory only." is written to the log (at most once a minute). The node then keeps the session only in its own memory, and the other nodes do not see it until it can be saved again. When a logout cannot delete the stored session, the node refuses that session from then on, but the other nodes accept it until it expires.

Without ``FESS_SESSION_STORE``, each node keeps its sessions only in its own memory, and a client that is sent to another node is not logged in there. Either share the sessions as described above, or make the load balancer send each client to the same node.
