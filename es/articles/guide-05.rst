====================================================================================
Parte 5: Adaptarse a quienes buscan -- Control de resultados por departamento y permisos
====================================================================================

Introducción
============

En la entrega anterior, presentamos cómo integrar múltiples fuentes de datos para realizar búsquedas unificadas.
Sin embargo, cuando la búsqueda unificada se hace posible, surge un nuevo desafío:
el control de la "información que se puede mostrar" y la "información que no se debe mostrar".

Sería un problema que documentos confidenciales del departamento de recursos humanos aparecieran en los resultados de búsqueda de todos los empleados.
En este artículo, utilizaremos la búsqueda basada en roles de Fess para diseñar y construir el control de resultados de búsqueda según la pertenencia y los permisos de los usuarios.

Audiencia objetivo
==================

- Personas que necesitan control de acceso en los resultados de búsqueda
- Personas que desean construir una plataforma de búsqueda considerando la seguridad de la información corporativa
- Personas con conocimientos básicos de Active Directory o LDAP

Escenario
=========

Una empresa tiene 3 departamentos.

- **Ventas**: Gestiona información de clientes, presupuestos y propuestas
- **Desarrollo**: Gestiona documentos de diseño, especificaciones de código fuente y actas de reuniones
- **Recursos humanos**: Gestiona evaluaciones de personal, información salarial y reglamentos laborales

También existen documentos comunes accesibles para todos los departamentos (normativas internas, guías de beneficios, etc.).

La experiencia de búsqueda que se desea lograr es la siguiente:

- Los empleados de ventas solo pueden buscar documentos de ventas y documentos comunes
- Los empleados de desarrollo solo pueden buscar documentos de desarrollo y documentos comunes
- Los empleados de recursos humanos solo pueden buscar documentos de recursos humanos y documentos comunes
- La dirección puede buscar todos los documentos

Mecanismo de búsqueda basada en roles
======================================

La búsqueda basada en roles de Fess funciona de la siguiente manera:

1. **Durante el rastreo**: Se asigna información de rol a los documentos (qué roles pueden acceder)
2. **Al iniciar sesión**: Se obtiene la información de rol del usuario (autenticación interna de Fess o integración con autenticación externa)
3. **Durante la búsqueda**: Solo se muestran en los resultados los documentos que coinciden con los roles del usuario

Este mecanismo permite que el control de acceso se realice a nivel del motor de búsqueda.

Diseño de roles
===============

Diseño de usuarios y grupos
----------------------------

Primero, organizamos la relación entre usuarios, grupos y roles en Fess.

.. list-table:: Diseño de roles
   :header-rows: 1
   :widths: 20 30 50

   * - Grupo
     - Rol
     - Documentos accesibles
   * - sales (Ventas)
     - sales_role
     - Documentos de ventas + documentos comunes
   * - engineering (Desarrollo)
     - engineering_role
     - Documentos de desarrollo + documentos comunes
   * - hr (Recursos humanos)
     - hr_role
     - Documentos de recursos humanos + documentos comunes
   * - management (Dirección)
     - management_role
     - Todos los documentos

Configuración de grupos y roles en Fess
----------------------------------------

**Creación de roles**

1. En la pantalla de administración, seleccione [Usuarios] > [Roles]
2. Cree los siguientes roles

   - ``sales_role``
   - ``engineering_role``
   - ``hr_role``
   - ``management_role``

**Creación de grupos**

1. Seleccione [Usuarios] > [Grupos]
2. Cree los siguientes grupos

   - ``sales``
   - ``engineering``
   - ``hr``
   - ``management``

**Creación de usuarios y asignación de roles**

1. Seleccione [Usuarios] > [Usuarios]
2. Asigne grupos y roles a cada usuario

Asignar permisos en la configuración de rastreo
=================================================

Para asignar información de control de acceso a los documentos, se especifican los permisos en la configuración de rastreo.
Los permisos se introducen en formato ``{role}nombre_del_rol``, ``{group}nombre_del_grupo``, ``{user}nombre_del_usuario``, separados por saltos de línea.

Configuración de rastreo por departamento
------------------------------------------

**Servidor de archivos de ventas**

1. [Rastreador] > [Sistema de archivos] > [Crear nuevo]
2. Configure lo siguiente

   - Ruta: ``smb://fileserver/sales/``
   - Permisos: Introduzca ``{role}sales_role`` y ``{role}management_role`` separados por saltos de línea

Con esta configuración, los documentos rastreados desde el servidor de archivos de ventas solo serán visibles en los resultados de búsqueda para los usuarios que posean ``sales_role`` o ``management_role``.

**Servidor de archivos de desarrollo**

1. [Rastreador] > [Sistema de archivos] > [Crear nuevo]
2. Configure lo siguiente

   - Ruta: ``smb://fileserver/engineering/``
   - Permisos: Introduzca ``{role}engineering_role`` y ``{role}management_role`` separados por saltos de línea

**Servidor de archivos de recursos humanos**

1. [Rastreador] > [Sistema de archivos] > [Crear nuevo]
2. Configure lo siguiente

   - Ruta: ``smb://fileserver/hr/``
   - Permisos: Introduzca ``{role}hr_role`` y ``{role}management_role`` separados por saltos de línea

**Documentos comunes**

1. [Rastreador] > [Web] o [Sistema de archivos] > [Crear nuevo]
2. Permisos: Deje el valor predeterminado ``{role}guest``

De forma predeterminada, se introduce automáticamente ``{role}guest``. Dado que todos los usuarios, incluidos los usuarios invitados, poseen el rol ``guest``, todos los usuarios pueden ver los resultados de búsqueda.

Integración con autenticación externa
=======================================

En entornos empresariales reales, en la mayoría de los casos se desea integrar con un servicio de directorio existente en lugar de utilizar la gestión de usuarios propia de Fess.

Integración con Active Directory / LDAP
-----------------------------------------

Fess es compatible con la integración LDAP y permite realizar la autenticación y la asignación de roles utilizando la información de usuarios de Active Directory.

Para habilitar la integración LDAP, se configura la información de conexión LDAP en el archivo de configuración de Fess.

Los principales elementos de configuración son los siguientes:

- URL del servidor LDAP
- Bind DN (cuenta de conexión)
- Base DN de búsqueda de usuarios
- Base DN de búsqueda de grupos
- Mapeo de atributos de usuario

Cuando la integración LDAP está habilitada, los usuarios pueden iniciar sesión en Fess con sus cuentas de Active Directory.
La información de los grupos a los que pertenecen se refleja automáticamente como roles, por lo que no es necesario configurar manualmente los roles para cada usuario en Fess.

Integración SSO
----------------

Como configuración más avanzada, también es posible la integración con inicio de sesión único (SSO).
Fess es compatible con los siguientes protocolos SSO:

- **OpenID Connect (OIDC)**: Entra ID (Azure AD), Keycloak, etc.
- **SAML**: Integración con diversos IdP
- **SPNEGO/Kerberos**: Autenticación integrada de Windows

Con la integración SSO, los usuarios pueden acceder automáticamente a Fess con sus credenciales habituales, y la información de roles también se refleja automáticamente.
Los detalles de la integración SSO se tratarán en profundidad en la Parte 15: "Plataforma de búsqueda segura".

Verificación del funcionamiento
================================

Una vez completada la configuración de la búsqueda basada en roles, verifiquemos el funcionamiento.

Procedimiento de verificación
------------------------------

1. Inicie sesión con un usuario de ventas y busque "presupuesto"
   → Verifique que solo se muestren documentos de ventas y documentos comunes

2. Inicie sesión con un usuario de desarrollo y busque con la misma palabra clave
   → Verifique que no se muestren documentos de ventas

3. Inicie sesión con un usuario de la dirección y busque con la misma palabra clave
   → Verifique que se muestren documentos de todos los departamentos

Puntos de verificación
-----------------------

- Que los documentos sin permisos no aparezcan en absoluto en los resultados de búsqueda
- Que los documentos comunes se muestren para todos los usuarios
- El comportamiento de búsqueda sin haber iniciado sesión (alcance de la vista de invitado)

Consideraciones de diseño
===========================

Granularidad de los roles
--------------------------

La granularidad de los roles se determina según la estructura organizativa y los requisitos de seguridad.

**Granularidad gruesa**: Configurar roles por departamento (escenario de este artículo)

- Ventaja: Configuración simple, fácil de administrar
- Desventaja: No permite un control de acceso detallado dentro del departamento

**Granularidad fina**: Configurar roles por proyecto o equipo

- Ventaja: Permite un control de acceso detallado
- Desventaja: El número de roles aumenta y la administración se vuelve compleja

Se recomienda comenzar con una granularidad gruesa y refinar según sea necesario.

Integración con ACL del servidor de archivos
----------------------------------------------

Al rastrear servidores de archivos, también es posible utilizar la información de ACL (listas de control de acceso) de los archivos para el control de permisos.
En este caso, la configuración de permisos del sistema de archivos se refleja directamente en el control de visualización de los resultados de búsqueda.

Si desea aprovechar las ACL del servidor de archivos, consulte los elementos de configuración relacionados con permisos en la configuración de rastreo.

Resumen
=======

En este artículo, diseñamos y construimos el control de resultados de búsqueda por departamento utilizando la búsqueda basada en roles de Fess.

- Diseño y registro de roles, grupos y usuarios
- Asignación de roles en la configuración de rastreo
- Reflejo automático de roles mediante integración con Active Directory / LDAP
- Opciones de integración SSO (OIDC, SAML, SPNEGO)

La búsqueda basada en roles permite ofrecer la comodidad de la búsqueda unificada mientras se garantiza la seguridad de la información.
Aquí concluye la sección de fundamentos. A partir de la próxima entrega, abordaremos la sección de soluciones prácticas, comenzando con la construcción de un hub de conocimiento para equipos de desarrollo.

Referencias
============

- `Configuración de roles en Fess <https://fess.codelibs.org/ja/15.5/admin/role.html>`__

- `Integración LDAP en Fess <https://fess.codelibs.org/ja/15.5/config/ldap.html>`__
