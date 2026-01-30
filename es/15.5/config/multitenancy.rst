==================================
Configuracion de multitenencia
==================================

Descripcion general
===================

La funcionalidad de multitenencia de |Fess| permite operar
multiples inquilinos (organizaciones, departamentos, clientes, etc.) de forma separada con una sola instancia de |Fess|.

Al usar la funcionalidad de host virtual, puede proporcionar para cada inquilino:

- Interfaz de busqueda independiente
- Contenido separado
- Diseno personalizado

Funcionalidad de host virtual
=============================

El host virtual es una funcionalidad que proporciona diferentes entornos de busqueda basados en el nombre de host de la solicitud HTTP.

Mecanismo
---------

1. El usuario accede a ``tenant1.example.com``
2. |Fess| identifica el nombre de host
3. Se aplica la configuracion de host virtual correspondiente
4. Se muestra el contenido y la UI especificos del inquilino

Configuracion de host virtual
=============================

Configuracion desde la pantalla de administracion
-------------------------------------------------

1. Iniciar sesion en la pantalla de administracion
2. Navegar a "Crawler" -> "Host Virtual"
3. Hacer clic en "Crear nuevo"
4. Configurar lo siguiente:

   - **Nombre de host**: ``tenant1.example.com``
   - **Ruta**: ``/tenant1`` (opcional)

Vinculacion con configuracion de crawl
--------------------------------------

Puede separar el contenido especificando el host virtual en la configuracion de crawl web:

1. Crear configuracion de crawl en "Crawler" -> "Web"
2. Seleccionar el host virtual objetivo en el campo "Host Virtual"
3. El contenido crawleado con esta configuracion solo sera buscable en el host virtual especificado

Control de acceso
=================

Combinacion de host virtual y roles
-----------------------------------

Al combinar hosts virtuales con control de acceso basado en roles,
es posible un control de acceso mas detallado:

::

    # Ejemplo de configuracion
    virtual.host=tenant1.example.com
    permissions=role_tenant1_user

Busqueda basada en roles
------------------------

Para mas detalles, consulte :doc:`security-role`.

Personalizacion de UI
=====================

Puede personalizar la UI para cada host virtual.

Aplicacion de tema
------------------

Aplicar un tema diferente para cada host virtual:

1. Configurar tema en "Sistema" -> "Diseno"
2. Especificar tema en la configuracion del host virtual

CSS personalizado
-----------------

Aplicar CSS personalizado para cada host virtual:

::

    # Archivo CSS especifico del host virtual
    /webapp/WEB-INF/view/tenant1/css/custom.css

Configuracion de etiquetas
--------------------------

Limitar etiquetas mostradas para cada host virtual:

1. Especificar host virtual en la configuracion del tipo de etiqueta
2. La etiqueta solo se muestra en el host virtual especificado

Autenticacion API
=================

Controlar el acceso a la API para cada host virtual:

Token de acceso
---------------

Emitir tokens de acceso vinculados al host virtual:

1. Crear token en "Sistema" -> "Tokens de Acceso"
2. Asociar host virtual con el token

Solicitud de API
----------------

::

    curl -H "Authorization: Bearer TENANT_TOKEN" \
         "https://tenant1.example.com/api/v1/search?q=keyword"

Configuracion de DNS
====================

Ejemplo de configuracion de DNS para implementar multitenencia:

Subdominios al mismo servidor
-----------------------------

::

    # Configuracion de DNS
    tenant1.example.com    A    192.168.1.100
    tenant2.example.com    A    192.168.1.100

    # O comodin
    *.example.com          A    192.168.1.100

Configuracion de proxy inverso
------------------------------

Ejemplo de configuracion de proxy inverso con Nginx:

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

Separacion de datos
===================

Si se requiere separacion completa de datos, considere los siguientes enfoques:

Separacion a nivel de indice
----------------------------

Usar indices separados para cada inquilino:

::

    # Indice para inquilino 1
    index.document.search.index=fess_tenant1.search

    # Indice para inquilino 2
    index.document.search.index=fess_tenant2.search

.. note::
   La separacion a nivel de indice puede requerir implementacion personalizada.

Mejores practicas
=================

1. **Convencion de nombres clara**: Usar una convencion de nombres consistente para hosts virtuales y roles
2. **Pruebas**: Probar exhaustivamente el funcionamiento en cada inquilino
3. **Monitoreo**: Monitorear el uso de recursos por inquilino
4. **Documentacion**: Documentar la configuracion de inquilinos

Limitaciones
============

- La pantalla de administracion es compartida por todos los inquilinos
- La configuracion del sistema afecta a todos los inquilinos
- Algunas funcionalidades pueden no ser compatibles con hosts virtuales

Informacion de referencia
=========================

- :doc:`security-role` - Control de acceso basado en roles
- :doc:`security-virtual-host` - Detalles de configuracion de host virtual
- :doc:`../admin/design-guide` - Personalizacion de diseno
