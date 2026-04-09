============================================================
Parte 13: Plataforma de busqueda multi-tenant -- Diseno de una unica instancia de Fess para servir a multiples organizaciones
============================================================

Introduccion
=============

Cuando se desea ofrecer Fess a multiples departamentos internos o a multiples clientes como MSP (Proveedor de Servicios Gestionados), construir una instancia de Fess independiente para cada tenant resulta ineficiente.

En este articulo se explica un diseno multi-tenant que permite servir a multiples tenants (organizaciones, departamentos o clientes) desde una unica instancia de Fess.

Audiencia objetivo
===================

- Personas que desean ofrecer servicios de busqueda a multiples organizaciones o departamentos
- Personas interesadas en el diseno multi-tenant con Fess
- Personas que desean aprender a utilizar la funcion de host virtual

Escenario
=========

Suponemos un escenario en el que el departamento de TI de un grupo empresarial ofrece servicios de busqueda a tres filiales.

.. list-table:: Configuracion de tenants
   :header-rows: 1
   :widths: 25 35 40

   * - Tenant
     - Dominio
     - Objetivo de busqueda
   * - Empresa A (Manufactura)
     - search-a.example.com
     - Especificaciones de productos, documentos de control de calidad
   * - Empresa B (Comercio minorista)
     - search-b.example.com
     - Manuales de tienda, informacion de productos
   * - Empresa C (Servicios)
     - search-c.example.com
     - Manuales de atencion al cliente, FAQ

Cada tenant tiene los siguientes requisitos:

- Los datos no deben ser visibles entre tenants (aislamiento de datos)
- Cada tenant necesita un diseno diferente (branding)
- Cada tenant necesita configuraciones de rastreo independientes

Funcion de host virtual
=========================

La funcion de host virtual de Fess permite ofrecer diferentes experiencias de busqueda segun el nombre de host utilizado para acceder.

Configuracion del host virtual
-------------------------------

Establezca el valor del host virtual en la consola de administracion.
Al asociar este valor con las configuraciones de rastreo y las etiquetas, se puede lograr el aislamiento de datos para cada tenant.

Consideraciones de diseno
--------------------------

**Configuracion de DNS / balanceador de carga**

Configure el DNS para que el dominio de cada tenant apunte al mismo servidor Fess.

::

    search-a.example.com → Servidor Fess (192.168.1.100)
    search-b.example.com → Servidor Fess (192.168.1.100)
    search-c.example.com → Servidor Fess (192.168.1.100)

Fess examina las cabeceras HTTP de la solicitud para determinar a cual host virtual se esta accediendo.
Por defecto se utiliza la cabecera Host, pero puede especificar cualquier cabecera mediante la configuracion ``virtual.host.headers``.
El formato de configuracion es ``NombreCabecera:Valor=ClaveHostVirtual`` (por ejemplo, ``Host:search-a.example.com=tenant-a``).

Diseno de aislamiento de tenants
==================================

Aislamiento de datos
---------------------

El aislamiento de datos entre tenants se logra mediante el campo ``virtual_host`` en los documentos, proporcionado por la funcion de host virtual.

**Aislamiento mediante host virtual**

Cuando se establece la clave de host virtual en el campo "Host virtual" de la configuracion de rastreo, los documentos rastreados reciben un campo ``virtual_host``.
Durante la busqueda, este campo se utiliza para el filtrado automatico, de modo que los usuarios que acceden a traves del dominio de cada tenant solo ven los documentos de ese tenant en los resultados de busqueda.

- ``tenant-a``: Documentos de la Empresa A
- ``tenant-b``: Documentos de la Empresa B
- ``tenant-c``: Documentos de la Empresa C

Ademas, al configurar el campo "Host virtual" en las etiquetas, tambien se pueden separar las etiquetas mostradas para cada tenant.

**Aislamiento mediante roles**

Cuando se requiere un aislamiento mas estricto, se combina con la busqueda basada en roles (vease Parte 5).
Cree roles para cada tenant y asignelos a las configuraciones de rastreo y a los usuarios.

Configuracion de rastreo
--------------------------

La configuracion de rastreo de cada tenant se gestiona de forma independiente.

.. list-table:: Configuracion de rastreo por tenant
   :header-rows: 1
   :widths: 15 30 25 30

   * - Tenant
     - Objetivo de rastreo
     - Programacion
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

Utilizando la funcion de temas de Fess, se pueden ofrecer disenos diferentes para cada tenant.

Diseno de temas
----------------

Prepare temas que se ajusten a los colores de marca y el logotipo de cada tenant.

- Empresa A: Un diseno solido propio de una empresa manufacturera (tonos azules)
- Empresa B: Un diseno brillante para el comercio minorista (tonos verdes)
- Empresa C: Un diseno amigable para una empresa de servicios (tonos naranjas)

Vinculacion de hosts virtuales y temas
----------------------------------------

Al cambiar los temas para cada host virtual, los usuarios de cada tenant veran una pantalla de busqueda con la imagen de marca de su propia empresa.

Fess ofrece temas integrados como ``simple``, ``docsearch`` y ``codesearch``, y tambien admite temas personalizados.

Aislamiento del acceso API
============================

Tokens de acceso API por tenant
---------------------------------

Emita tokens de acceso individuales para cada tenant.
Al asociar roles con los tokens, el aislamiento de tenants tambien se aplica al acceso por API.

.. list-table:: Configuracion de tokens de acceso
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

Cuando el sistema de cada tenant se integra mediante API (vease Parte 11), el uso de tokens especificos del tenant garantiza que no se pueda acceder a los datos de otros tenants.

Consideraciones operativas
============================

Gestion de recursos
--------------------

Dado que una unica instancia de Fess sirve a multiples tenants, es necesario prestar atencion a la asignacion de recursos.

- **Distribucion de carga del rastreo**: Escalone las programaciones de rastreo de los tenants para evitar la ejecucion simultanea
- **Tamano del indice**: Supervise el tamano total del indice de todos los tenants
- **Memoria**: Ajuste el heap de la JVM segun el numero de tenants y documentos

Adicion y eliminacion de tenants
----------------------------------

Estandarice el procedimiento para agregar nuevos tenants.

1. Crear una etiqueta
2. Crear un rol
3. Registrar la configuracion de rastreo
4. Configurar el host virtual
5. Emitir un token de acceso
6. Agregar la configuracion DNS

Al eliminar un tenant, no olvide eliminar tambien los datos de indice asociados.

Criterios de escalado
----------------------

Si observa los siguientes sintomas, considere dividir o escalar las instancias de Fess (vease Parte 14).

- Degradacion de los tiempos de respuesta de busqueda
- Los rastreos no se completan dentro del periodo programado
- Errores frecuentes por falta de memoria
- El numero de tenants supera los 10

Resumen
========

En este articulo se explico el diseno multi-tenant utilizando la funcion de host virtual de Fess.

- Acceso especifico por tenant mediante hosts virtuales
- Aislamiento de datos mediante etiquetas y roles
- Branding especifico por tenant mediante temas
- Aislamiento de tenants mediante tokens de acceso API
- Gestion de recursos y criterios de escalado

Con una unica instancia de Fess, puede servir eficientemente a multiples tenants, manteniendo bajos los costos de gestion y cumpliendo con los requisitos de cada tenant.

En el proximo articulo se abordaran las estrategias de escalado para sistemas de busqueda.

Referencias
============

- `Fess Virtual Host <https://fess.codelibs.org/ja/15.5/config/virtual-host.html>`__

- `Fess Configuracion de etiquetas <https://fess.codelibs.org/ja/15.5/admin/labeltype.html>`__
