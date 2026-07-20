=====================================
Configuración de multitenencia
=====================================

Descripción general
===================

La funcionalidad de multitenencia de |Fess| permite operar
múltiples inquilinos (organizaciones, departamentos, clientes, etc.) de forma separada con una sola instancia de |Fess|.

Al usar la funcionalidad de host virtual, puede proporcionar para cada inquilino:

- Interfaz de búsqueda independiente
- Contenido separado
- Diseño personalizado

El host virtual actual se refleja en las funciones de filtrado de resultados de búsqueda, etiquetas, contenido relacionado,
consultas relacionadas y diseño (tema), entre otras funciones de |Fess|.

Funcionalidad de host virtual
==============================

El host virtual es una funcionalidad que proporciona diferentes entornos de búsqueda basados en el nombre de host de la solicitud HTTP.

Mecanismo
---------

1. El usuario accede a ``tenant1.example.com``
2. |Fess| identifica el nombre de host
3. Se aplica la configuración de host virtual correspondiente
4. Se muestra el contenido y la UI específicos del inquilino

Configuración de encabezados de host virtual
=============================================

Para habilitar la funcionalidad de host virtual, configure la correspondencia entre los encabezados de la solicitud HTTP
y las claves de host virtual. Existen dos métodos de configuración:

- **Pantalla de administración (recomendado)**: Configure el campo "Host Virtual" en "Sistema" -> "General".
  Este valor se guarda como configuración del sistema y se conserva tras el reinicio. Tiene prioridad sobre
  ``virtual.host.headers`` en ``fess_config.properties``.
- **Archivo de configuración**: Configure la propiedad ``virtual.host.headers`` en ``fess_config.properties``.

Ambos métodos utilizan el mismo formato de valor de configuración.

Formato de configuración
------------------------

Especifique cada entrada en el formato ``NombreEncabezado:ValorEncabezado=ClaveHostVirtual``, una por línea:

::

    # fess_config.properties
    virtual.host.headers=Host:tenant1.example.com=tenant1\n\
    Host:tenant2.example.com=tenant2

Para múltiples hosts virtuales, separe las entradas con saltos de línea.

Comportamiento de coincidencia
------------------------------

Cada vez que |Fess| recibe una solicitud, compara el valor del encabezado de solicitud correspondiente al
"NombreEncabezado" de cada línea configurada con el "ValorEncabezado" configurado.

- La comparación de valores de encabezado no distingue entre mayúsculas y minúsculas.
- Las líneas configuradas se evalúan en orden de arriba a abajo; se aplica la clave de host virtual de la primera línea que coincida.
- Si no hay coincidencia, la solicitud se trata sin host virtual (entorno común).
- El resultado de la evaluación se almacena en cache por solicitud.

Restricciones de claves de host virtual
----------------------------------------

Las claves de host virtual tienen las siguientes restricciones:

- Solo se permiten caracteres alfanuméricos y guiones bajos (``a-zA-Z0-9_``). Otros caracteres se eliminan automáticamente.
- Los siguientes nombres de clave están reservados y no se pueden usar: ``admin``, ``common``, ``error``, ``login``, ``profile``

Configuración desde la pantalla de administración
==================================================

Configuración de crawl
----------------------

Puede separar el contenido especificando el host virtual en la configuración de crawl web:

1. Iniciar sesión en la pantalla de administración
2. Crear configuración de crawl en "Crawler" -> "Web"
3. Seleccionar la clave de host virtual configurada en el campo "Host Virtual" (se admite selección múltiple)
4. El contenido crawleado con esta configuración solo será buscable en el host virtual especificado

.. note::
   El campo "Host Virtual" está disponible en las configuraciones de crawl de web, sistema de archivos y almacén de datos.
   La clave de host virtual seleccionada aquí se asigna a cada documento crawleado y se usa para filtrar
   por el host virtual actual en el momento de la búsqueda.

Control de acceso
=================

Combinación de host virtual y roles
-------------------------------------

Al combinar hosts virtuales con control de acceso basado en roles,
es posible un control de acceso más detallado.

Configure el host virtual y los permisos juntos en la configuración de crawl:

::

    # Host virtual en la configuracion de crawl
    tenant1

    # Permisos en la configuracion de crawl
    {role}tenant1_user

Búsqueda basada en roles
------------------------

Para más detalles, consulte :doc:`security-role`.

Personalización de UI
=====================

Puede personalizar la UI para cada host virtual.

Aplicación de tema
------------------

Aplicar un tema diferente para cada host virtual:

1. Configurar tema en "Sistema" -> "Diseño"
2. Especificar tema en la configuración del host virtual

CSS personalizado
-----------------

Para aplicar CSS personalizado por host virtual, edite los archivos CSS en la pantalla de administración en "Sistema" -> "Diseño". También puede colocar plantillas personalizadas en el directorio de vista correspondiente a la clave del host virtual.

Configuración de etiquetas
--------------------------

Limitar etiquetas mostradas para cada host virtual:

1. Especificar host virtual en la configuración del tipo de etiqueta
2. La etiqueta solo se muestra en el host virtual especificado

Acceso mediante API
===================

Las solicitudes a la API de búsqueda también determinan el host virtual por el nombre de host de la solicitud
(el encabezado configurado, normalmente el encabezado ``Host``), igual que la UI. Por ejemplo,
una solicitud dirigida a ``tenant1.example.com`` se limita automáticamente al host virtual ``tenant1``
y solo se busca en el contenido de ese host virtual.

Solicitud de API
----------------

::

    curl "https://tenant1.example.com/api/v2/search?q=keyword"

Para autenticarse con un token de acceso, especifíquelo en el encabezado ``Authorization``
en formato ``Bearer``:

::

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "https://tenant1.example.com/api/v2/search?q=keyword"

.. note::
   Los tokens de acceso no están vinculados a un host virtual específico. Un token es válido para
   cualquier host virtual; el host virtual de destino se determina por el nombre de host al que se
   envía la solicitud. Si se envía el mismo token a un nombre de host diferente, se aplica al
   host virtual correspondiente. Si desea controlar el alcance del acceso independientemente del
   host virtual, combinen con el control de acceso basado en roles (:doc:`security-role`).

Configuración de DNS
====================

Ejemplo de configuración de DNS para implementar multitenencia:

Subdominios al mismo servidor
------------------------------

::

    # Configuracion de DNS
    tenant1.example.com    A    192.168.1.100
    tenant2.example.com    A    192.168.1.100

    # O comodin
    *.example.com          A    192.168.1.100

Configuración de proxy inverso
--------------------------------

Ejemplo de configuración de proxy inverso con Nginx:

::

    server {
        server_name tenant1.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

    server {
        server_name tenant2.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

Separación de datos
===================

Si se requiere separación completa de datos, considere los siguientes enfoques:

Separación a nivel de índice
------------------------------

Usar instancias e índices separados de |Fess| para cada inquilino:

::

    # Instancia Fess del inquilino 1 (fess_config.properties)
    index.document.search.index=fess_tenant1.search

    # Instancia Fess del inquilino 2 (fess_config.properties)
    index.document.search.index=fess_tenant2.search

.. note::
   ``index.document.search.index`` solo puede establecerse en un valor por instancia.
   Para una separación completa a nivel de índice, necesita ejecutar instancias separadas de |Fess| por inquilino
   o implementar código personalizado. Para multitenencia típica, la separación lógica mediante la funcionalidad de host virtual es suficiente.

Mejores prácticas
=================

1. **Convención de nombres clara**: Usar una convención de nombres consistente para hosts virtuales y roles
2. **Pruebas**: Probar exhaustivamente el funcionamiento en cada inquilino
3. **Monitoreo**: Monitorear el uso de recursos por inquilino
4. **Documentación**: Documentar la configuración de inquilinos

Limitaciones
============

- La pantalla de administración es compartida por todos los inquilinos
- La configuración del sistema afecta a todos los inquilinos
- Algunas funcionalidades pueden no ser compatibles con hosts virtuales

Información de referencia
=========================

- :doc:`security-role` - Control de acceso basado en roles
- :doc:`security-virtual-host` - Detalles de configuración de host virtual
- :doc:`../admin/design-guide` - Personalización de diseño
