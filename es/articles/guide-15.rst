============================================================
Parte 15: Infraestructura de busqueda segura -- Integracion SSO y control de acceso a la busqueda en un entorno de confianza cero
============================================================

Introduccion
=============

Los requisitos de seguridad de la informacion empresarial son cada vez mas estrictos ano tras ano.
Dado que los sistemas de busqueda agregan una gran cantidad de documentos confidenciales, son indispensables mecanismos adecuados de autenticacion y autorizacion.

En este articulo, partimos de la busqueda basada en roles presentada en la Parte 5 y disenamos una arquitectura de seguridad centrada en la integracion con SSO (inicio de sesion unico).

Publico objetivo
=================

- Personas que operan Fess en un entorno empresarial
- Personas que disenan la integracion SSO (OIDC, SAML)
- Personas que comprenden los conceptos de seguridad de confianza cero

Organizacion de los requisitos de seguridad
=============================================

A continuacion, se organizan los requisitos de seguridad tipicos de las empresas.

.. list-table:: Requisitos de seguridad
   :header-rows: 1
   :widths: 30 70

   * - Requisito
     - Descripcion
   * - Inicio de sesion unico
     - Integrarse con un IdP existente para eliminar operaciones de inicio de sesion adicionales
   * - Acceso basado en roles
     - Controlar los resultados de busqueda segun la afiliacion y los permisos del usuario
   * - Cifrado de comunicaciones
     - Cifrar todas las comunicaciones mediante HTTPS
   * - Control de acceso a la API
     - Autenticacion de API basada en tokens y gestion de permisos
   * - Registros de auditoria
     - Registrar quien busco que informacion

Opciones de integracion SSO
==============================

A continuacion, se presentan los protocolos SSO compatibles con Fess y los escenarios en los que cada uno es aplicable.

.. list-table:: Comparacion de protocolos SSO
   :header-rows: 1
   :widths: 20 30 50

   * - Protocolo
     - IdPs representativos
     - Escenarios de aplicacion
   * - OpenID Connect
     - Entra ID, Keycloak, Google
     - Entornos en la nube, infraestructura de autenticacion moderna
   * - SAML 2.0
     - Entra ID, Okta, OneLogin
     - Entornos empresariales, cuando existe un IdP SAML existente
   * - SPNEGO/Kerberos
     - Active Directory
     - Entornos con autenticacion integrada de Windows

Integracion SSO mediante OpenID Connect / Entra ID
=====================================================

Este es el enfoque mas moderno y recomendado.
Ademas de la integracion generica con OpenID Connect, Fess tambien proporciona una funcion de integracion dedicada para Entra ID (Azure AD).
A continuacion, se explica la integracion utilizando Entra ID como ejemplo.

Descripcion general del flujo de autenticacion
-------------------------------------------------

1. Un usuario accede a Fess
2. Fess redirige al usuario a la pantalla de autenticacion de Entra ID
3. El usuario se autentica en Entra ID (incluida la MFA)
4. Entra ID devuelve un token de autenticacion a Fess
5. Fess obtiene la informacion de usuario y de grupo a partir del token
6. Se asignan roles en funcion de la informacion de grupo
7. Se proporcionan resultados de busqueda basados en los roles

Configuracion en el lado de Entra ID
--------------------------------------

1. Registre una aplicacion en Entra ID
2. Configure la URI de redireccion (URL de callback OIDC de Fess)
3. Otorgue los permisos de API necesarios (User.Read, GroupMember.Read.All, etc.)
4. Obtenga el ID de cliente y el secreto

Configuracion en el lado de Fess
----------------------------------

Configure la informacion de conexion SSO en la pagina [Sistema] > [General] de la consola de administracion.
Los principales elementos de configuracion son los siguientes:

- URL del proveedor OpenID Connect (endpoint de Entra ID)
- ID de cliente
- Secreto de cliente
- Alcances (openid, profile, email, etc.)
- Configuracion de claims de grupo

Mapeo de grupos a roles
-------------------------

Asigne los grupos de Entra ID a los roles de Fess.
Esto permite que la gestion de grupos en Entra ID se refleje directamente en el control de los resultados de busqueda.

Ejemplo: Grupo de Entra ID "Engineering" -> Rol de Fess "engineering_role"

Integracion SSO mediante SAML
================================

La integracion SAML es adecuada para entornos donde existe un IdP SAML existente.

Descripcion general del flujo de autenticacion
-------------------------------------------------

En SAML, se intercambian SAML Assertions entre el SP (Service Provider = Fess) y el IdP.

1. Un usuario accede a Fess
2. Fess envia un SAML AuthnRequest al IdP
3. El IdP autentica al usuario
4. El IdP devuelve una SAML Response (que contiene atributos de usuario) a Fess
5. Fess asigna roles en funcion de los atributos de usuario

Configuracion en el lado de Fess
----------------------------------

Para la integracion SAML, se requieren las siguientes configuraciones:

- URL de metadatos o archivo XML del IdP
- ID de entidad del SP
- Assertion Consumer Service URL
- Mapeo de atributos (nombre de usuario, direccion de correo electronico, grupos)

Integracion SPNEGO / Kerberos
================================

En entornos de Windows Active Directory, se puede utilizar la autenticacion integrada de Windows mediante SPNEGO/Kerberos.
Cuando se accede a traves de un navegador desde un PC unido al dominio, la autenticacion se realiza automaticamente sin operaciones de inicio de sesion adicionales.

Este metodo es el mas transparente para los usuarios, pero la configuracion es la mas compleja.
Se requiere un entorno de dominio de Active Directory como prerrequisito.

Cifrado de comunicaciones
===========================

Configuracion de SSL/TLS
--------------------------

En entornos de produccion, se recomienda realizar todos los accesos a Fess a traves de HTTPS.

**Metodo de proxy inverso (recomendado)**

Despliegue Nginx o Apache HTTP Server como proxy inverso para realizar la terminacion SSL.
Fess en si opera sobre HTTP, y el proxy inverso maneja HTTPS.

::

    [Cliente] --HTTPS--> [Nginx] --HTTP--> [Fess]

La ventaja de este metodo es que la gestion de certificados se centraliza en el proxy inverso.

**Metodo de configuracion directa en Fess**

Tambien es posible configurar certificados SSL directamente en el Tomcat de Fess.
Esto es adecuado para entornos de pequena escala o cuando no se despliega un proxy inverso.

Seguridad del acceso a la API
================================

A continuacion, se refuerza la seguridad de la integracion con la API presentada en la Parte 11.

Diseno de permisos de tokens
------------------------------

Configure los permisos adecuados para los tokens de acceso.

.. list-table:: Ejemplo de diseno de tokens
   :header-rows: 1
   :widths: 25 25 50

   * - Proposito
     - Permisos
     - Notas
   * - Widget de busqueda
     - Solo busqueda (solo lectura)
     - Utilizado en el frontend
   * - Procesamiento por lotes
     - Busqueda + Indexacion
     - Utilizado en el lado del servidor
   * - Automatizacion de administracion
     - Acceso a la API de administracion
     - Utilizado en scripts operativos

Gestion de tokens
------------------

- Rotacion periodica (cada 3 a 6 meses)
- Revocacion inmediata de los tokens que ya no son necesarios
- Supervision del uso de tokens

Auditoria y registros
=======================

Los registros de auditoria en un sistema de busqueda son importantes para investigar incidentes de seguridad y garantizar el cumplimiento normativo.

Registros generados por Fess
------------------------------

- **Registros de busqueda**: Quien busco que (se pueden consultar en [Informacion del sistema] > [Registro de busqueda] en la consola de administracion)
- **Registros de auditoria** (``audit.log``): Operaciones como inicio de sesion, cierre de sesion, acceso y cambios de permisos se registran de manera unificada

Retencion de registros
-----------------------

Configure el periodo de retencion de registros segun los requisitos de seguridad.
Si existen requisitos de cumplimiento normativo, considere el reenvio de registros a un sistema externo de gestion de registros (SIEM).

Resumen
========

En este articulo, disenamos una arquitectura de seguridad para Fess en un entorno empresarial.

- Tres opciones de integracion SSO (OIDC, SAML, SPNEGO) y sus escenarios de aplicacion
- Diseno de la integracion con Entra ID mediante OpenID Connect
- Cifrado de comunicaciones mediante SSL/TLS
- Diseno de permisos para tokens de acceso a la API
- Gestion de registros de auditoria

Construya una infraestructura de busqueda segura manteniendo el equilibrio entre seguridad y usabilidad.

En el proximo articulo, se abordara la automatizacion de la infraestructura de busqueda.

Referencias
============

- `Configuracion SSO de Fess <https://fess.codelibs.org/ja/15.5/config/sso.html>`__

- `Configuracion de seguridad de Fess <https://fess.codelibs.org/ja/15.5/config/security.html>`__
