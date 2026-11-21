===================================
Compartir sesiones HTTP entre nodos
===================================

Descripción general
===================

De forma predeterminada, cada nodo de |Fess| guarda sus sesiones HTTP en su propia memoria. Si ejecuta varios nodos de |Fess| detrás de un balanceador de carga, defina la variable de entorno ``FESS_SESSION_STORE=opensearch`` en todos los nodos. Las sesiones se guardan entonces en el índice ``fess_config.session`` del motor de búsqueda, y un nodo puede leer una sesión creada por otro. Esto incluye el estado de inicio de sesión y lo que una operación con llave de acceso o un inicio de sesión SSO conserva en la sesión entre dos solicitudes (consulte :doc:`security-passkey` y :doc:`sso-saml`). Sin valor, con un valor vacío o con ``memory``, las sesiones permanecen en la memoria de cada nodo. Un valor desconocido se notifica en la salida de error estándar y se trata como ``memory``.

Para añadir o quitar un plugin SSO, lo que invalida todas las sesiones guardadas, consulte la nota de :doc:`sso-saml`.

Guardado y fallos
=================

Un nodo guarda en el motor de búsqueda las sesiones que ha tocado una solicitud antes de enviar la respuesta, por lo que un cliente que envía su siguiente solicitud a otro nodo justo después de la respuesta, por ejemplo directamente tras iniciar sesión, encuentra allí la sesión. Los cambios realizados una vez iniciada la respuesta se guardan al final de la solicitud.

Cuando el motor de búsqueda no se puede leer o escribir, la solicitud se responde igualmente y se escribe en el registro una advertencia como «Failed to save the session to the session store.» o «Failed to load the session from the session store. The session is kept in memory only.» (como máximo una vez por minuto). El nodo conserva entonces la sesión solo en su propia memoria, y los demás nodos no la ven hasta que pueda guardarse de nuevo. Cuando un cierre de sesión no puede eliminar la sesión almacenada, el nodo rechaza esa sesión a partir de ese momento, pero los demás nodos la aceptan hasta que caduque.

Sin ``FESS_SESSION_STORE``, cada nodo conserva sus sesiones solo en su propia memoria, y un cliente que se dirige a otro nodo no tiene la sesión iniciada allí. Comparta las sesiones como se describe arriba o haga que el balanceador de carga dirija a cada cliente siempre al mismo nodo.
