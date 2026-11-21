===================================
Compartir sesiones HTTP entre nodos
===================================

Descripción general
===================

De forma predeterminada, cada nodo de |Fess| guarda sus sesiones HTTP en su propia memoria. Si ejecuta varios nodos de |Fess| detrás de un balanceador de carga, defina la variable de entorno ``FESS_SESSION_STORE=opensearch`` en todos los nodos. Las sesiones se guardan entonces en el índice ``fess_config.session`` del motor de búsqueda, y un nodo puede leer una sesión creada por otro. Esto incluye el estado de inicio de sesión y lo que una operación con llave de acceso o un inicio de sesión SSO conserva en la sesión entre dos solicitudes (consulte :doc:`security-passkey` y :doc:`sso-saml`). Sin valor, con un valor vacío o con ``memory``, las sesiones permanecen en la memoria de cada nodo. Un valor desconocido se notifica en la salida de error estándar y se trata como ``memory``.

Para añadir o quitar un plugin SSO, lo que invalida todas las sesiones guardadas, consulte la nota de :doc:`sso-saml`.

Requisito con varios nodos
==========================

Configure sesiones persistentes (afinidad de cliente) en el balanceador de carga, incluso cuando las sesiones se comparten, de modo que un cliente se dirija siempre al mismo nodo.

Un nodo guarda la sesión en el motor de búsqueda antes de enviar la respuesta, por lo que, en funcionamiento normal, otro nodo puede leer la sesión en cuanto el cliente ha recibido la respuesta. Sin embargo, esto no está garantizado. Cuando una sesión no se puede guardar, solo se escribe una advertencia en el registro del nodo y la solicitud se responde con normalidad. Además, justo después de iniciarse un nodo, una solicitud que pasa a otro nodo puede no encontrar la sesión. En ambos casos, un cliente que envía su siguiente solicitud a otro nodo de inmediato, por ejemplo justo después de iniciar sesión, puede ser tratado como no autenticado y recibir ``401``. En las pruebas, esto ocurrió de forma ocasional con solicitudes enviadas justo después de iniciarse un nodo, y dejó de ocurrir cuando el nodo se había calentado. Con sesiones persistentes, el cliente llega siempre al nodo que creó la sesión, y las sesiones compartidas solo se necesitan para trasladar la sesión cuando ese nodo deja de estar disponible.
