=============================================
Parte 13: Plataforma de búsqueda multi-tenant
=============================================

Introducción
=============

Cuando se desea ofrecer Fess a múltiples departamentos internos o a múltiples clientes como MSP (Proveedor de Servicios Gestionados), construir una instancia de Fess independiente para cada tenant resulta ineficiente.

En este artículo se explica un diseño multi-tenant que permite servir a múltiples tenants (organizaciones, departamentos o clientes) desde una única instancia de Fess.

Audiencia objetivo
===================

- Personas que desean ofrecer servicios de búsqueda a múltiples organizaciones o departamentos
- Personas interesadas en el diseño multi-tenant con Fess
- Personas que desean aprender a utilizar la función de host virtual

Escenario
=========

Suponemos un escenario en el que el departamento de TI de un grupo empresarial ofrece servicios de búsqueda a tres filiales.

.. list-table:: Configuración de tenants
   :header-rows: 1
   :widths: 25 35 40

   * - Tenant
     - Dominio
     - Objetivo de búsqueda
   * - Empresa A (Manufactura)
     - search-a.example.com
     - Especificaciones de productos, documentos de control de calidad
   * - Empresa B (Comercio minorista)
     - search-b.example.com
     - Manuales de tienda, información de productos
   * - Empresa C (Servicios)
     - search-c.example.com
     - Manuales de atención al cliente, FAQ

Cada tenant tiene los siguientes requisitos:

- Los datos no deben ser visibles entre tenants (aislamiento de datos)
- Cada tenant necesita un diseño diferente (branding)
- Cada tenant necesita configuraciones de rastreo independientes

Función de host virtual
=========================

La función de host virtual de Fess permite ofrecer diferentes experiencias de búsqueda según el nombre de host utilizado para acceder.

Configuración del host virtual
-------------------------------

Establezca el valor del host virtual en la consola de administración.
Al asociar este valor con las configuraciones de rastreo y las etiquetas, se puede lograr el aislamiento de datos para cada tenant.

Consideraciones de diseño
--------------------------

**Configuración de DNS / balanceador de carga**

Configure el DNS para que el dominio de cada tenant apunte al mismo servidor Fess.

::

    search-a.example.com → Servidor Fess (192.168.1.100)
    search-b.example.com → Servidor Fess (192.168.1.100)
    search-c.example.com → Servidor Fess (192.168.1.100)

Fess examina las cabeceras HTTP de la solicitud para determinar a cuál host virtual se está accediendo.
Por defecto se utiliza la cabecera Host, pero puede especificar cualquier cabecera mediante la configuración ``virtual.host.headers``.
El formato de configuración es ``NombreCabecera:Valor=ClaveHostVirtual`` (por ejemplo, ``Host:search-a.example.com=tenant-a``).

Diseño de aislamiento de tenants
==================================

Aislamiento de datos
---------------------

El aislamiento de datos entre tenants se logra mediante el campo ``virtual_host`` en los documentos, proporcionado por la función de host virtual.

**Aislamiento mediante host virtual**

Cuando se establece la clave de host virtual en el campo "Host virtual" de la configuración de rastreo, los documentos rastreados reciben un campo ``virtual_host``.
Durante la búsqueda, este campo se utiliza para el filtrado automático, de modo que los usuarios que acceden a través del dominio de cada tenant solo ven los documentos de ese tenant en los resultados de búsqueda.

- ``tenant-a``: Documentos de la Empresa A
- ``tenant-b``: Documentos de la Empresa B
- ``tenant-c``: Documentos de la Empresa C

Además, al configurar el campo "Host virtual" en las etiquetas, también se pueden separar las etiquetas mostradas para cada tenant.

**Aislamiento mediante roles**

Cuando se requiere un aislamiento más estricto, se combina con la búsqueda basada en roles (véase Parte 5).
Cree roles para cada tenant y asígnelos a las configuraciones de rastreo y a los usuarios.

Configuración de rastreo
--------------------------

La configuración de rastreo de cada tenant se gestiona de forma independiente.

.. list-table:: Configuración de rastreo por tenant
   :header-rows: 1
   :widths: 15 30 25 30

   * - Tenant
     - Objetivo de rastreo
     - Programación
     - Etiqueta
   * - Empresa A
     - smb://fs-a/docs/
     - Diariamente a las 1:00
     - tenant-a
   * - Empresa B
     - https://portal-b.example.com/
     - Diariamente a las 2:00
     - tenant-b
   * - Empresa C
     - smb://fs-c/manuals/
     - Diariamente a las 3:00
     - tenant-c

Temas por tenant
=================

Utilizando la función de temas de Fess, se pueden ofrecer diseños diferentes para cada tenant.

Diseño de temas
----------------

Prepare temas que se ajusten a los colores de marca y el logotipo de cada tenant.

- Empresa A: Un diseño sólido propio de una empresa manufacturera (tonos azules)
- Empresa B: Un diseño brillante para el comercio minorista (tonos verdes)
- Empresa C: Un diseño amigable para una empresa de servicios (tonos naranjas)

Vinculación de hosts virtuales y temas
----------------------------------------

Al cambiar los temas para cada host virtual, los usuarios de cada tenant verán una pantalla de búsqueda con la imagen de marca de su propia empresa.

Fess ofrece temas integrados como ``simple``, ``docsearch`` y ``codesearch``, y también admite temas personalizados.

Aislamiento del acceso API
============================

Tokens de acceso API por tenant
---------------------------------

Emita tokens de acceso individuales para cada tenant.
Al asociar roles con los tokens, el aislamiento de tenants también se aplica al acceso por API.

.. list-table:: Configuración de tokens de acceso
   :header-rows: 1
   :widths: 20 30 50

   * - Tenant
     - Nombre del token
     - Rol asignado
   * - Empresa A
     - tenant-a-api-token
     - tenant-a-role
   * - Empresa B
     - tenant-b-api-token
     - tenant-b-role
   * - Empresa C
     - tenant-c-api-token
     - tenant-c-role

Cuando el sistema de cada tenant se integra mediante API (véase Parte 11), el uso de tokens específicos del tenant garantiza que no se pueda acceder a los datos de otros tenants.

Consideraciones operativas
============================

Gestión de recursos
--------------------

Dado que una única instancia de Fess sirve a múltiples tenants, es necesario prestar atención a la asignación de recursos.

- **Distribución de carga del rastreo**: Escalone las programaciones de rastreo de los tenants para evitar la ejecución simultánea
- **Tamaño del índice**: Supervise el tamaño total del índice de todos los tenants
- **Memoria**: Ajuste el heap de la JVM según el número de tenants y documentos

Adición y eliminación de tenants
----------------------------------

Estandarice el procedimiento para agregar nuevos tenants.

1. Crear una etiqueta
2. Crear un rol
3. Registrar la configuración de rastreo
4. Configurar el host virtual
5. Emitir un token de acceso
6. Agregar la configuración DNS

Al eliminar un tenant, no olvide eliminar también los datos de índice asociados.

Criterios de escalado
----------------------

Si observa los siguientes síntomas, considere dividir o escalar las instancias de Fess (véase Parte 14).

- Degradación de los tiempos de respuesta de búsqueda
- Los rastreos no se completan dentro del período programado
- Errores frecuentes por falta de memoria
- El número de tenants supera los 10

Resumen
========

En este artículo se explicó el diseño multi-tenant utilizando la función de host virtual de Fess.

- Acceso específico por tenant mediante hosts virtuales
- Aislamiento de datos mediante etiquetas y roles
- Branding específico por tenant mediante temas
- Aislamiento de tenants mediante tokens de acceso API
- Gestión de recursos y criterios de escalado

Con una única instancia de Fess, puede servir eficientemente a múltiples tenants, manteniendo bajos los costos de gestión y cumpliendo con los requisitos de cada tenant.

En el próximo artículo se abordarán las estrategias de escalado para sistemas de búsqueda.

Referencias
============

- `Fess Virtual Host <https://fess.codelibs.org/ja/15.5/config/virtual-host.html>`__

- `Fess Configuración de etiquetas <https://fess.codelibs.org/ja/15.5/admin/labeltype.html>`__
