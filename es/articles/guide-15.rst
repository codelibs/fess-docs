============================================
Parte 15: Infraestructura de búsqueda segura
============================================

Introducción
=============

Los requisitos de seguridad de la información empresarial son cada vez más estrictos año tras año.
Dado que los sistemas de búsqueda agregan una gran cantidad de documentos confidenciales, son indispensables mecanismos adecuados de autenticación y autorización.

En este artículo, partimos de la búsqueda basada en roles presentada en la Parte 5 y diseñamos una arquitectura de seguridad centrada en la integración con SSO (inicio de sesión único).

Público objetivo
=================

- Personas que operan Fess en un entorno empresarial
- Personas que diseñan la integración SSO (OIDC, SAML)
- Personas que comprenden los conceptos de seguridad de confianza cero

Organización de los requisitos de seguridad
=============================================

A continuación, se organizan los requisitos de seguridad típicos de las empresas.

.. list-table:: Requisitos de seguridad
   :header-rows: 1
   :widths: 30 70

   * - Requisito
     - Descripción
   * - Inicio de sesión único
     - Integrarse con un IdP existente para eliminar operaciones de inicio de sesión adicionales
   * - Acceso basado en roles
     - Controlar los resultados de búsqueda según la afiliación y los permisos del usuario
   * - Cifrado de comunicaciones
     - Cifrar todas las comunicaciones mediante HTTPS
   * - Control de acceso a la API
     - Autenticación de API basada en tokens y gestión de permisos
   * - Registros de auditoría
     - Registrar quién buscó qué información

Opciones de integración SSO
==============================

A continuación, se presentan los protocolos SSO compatibles con Fess y los escenarios en los que cada uno es aplicable.

.. list-table:: Comparación de protocolos SSO
   :header-rows: 1
   :widths: 20 30 50

   * - Protocolo
     - IdPs representativos
     - Escenarios de aplicación
   * - OpenID Connect
     - Entra ID, Keycloak, Google
     - Entornos en la nube, infraestructura de autenticación moderna
   * - SAML 2.0
     - Entra ID, Okta, OneLogin
     - Entornos empresariales, cuando existe un IdP SAML existente
   * - SPNEGO/Kerberos
     - Active Directory
     - Entornos con autenticación integrada de Windows

Integración SSO mediante OpenID Connect / Entra ID
=====================================================

Este es el enfoque más moderno y recomendado.
Además de la integración genérica con OpenID Connect, Fess también proporciona una función de integración dedicada para Entra ID (Azure AD).
A continuación, se explica la integración utilizando Entra ID como ejemplo.

Descripción general del flujo de autenticación
-------------------------------------------------

1. Un usuario accede a Fess
2. Fess redirige al usuario a la pantalla de autenticación de Entra ID
3. El usuario se autentica en Entra ID (incluida la MFA)
4. Entra ID devuelve un token de autenticación a Fess
5. Fess obtiene la información de usuario y de grupo a partir del token
6. Se asignan roles en función de la información de grupo
7. Se proporcionan resultados de búsqueda basados en los roles

Configuración en el lado de Entra ID
--------------------------------------

1. Registre una aplicación en Entra ID
2. Configure la URI de redirección (URL de callback OIDC de Fess)
3. Otorgue los permisos de API necesarios (User.Read, GroupMember.Read.All, etc.)
4. Obtenga el ID de cliente y el secreto

Configuración en el lado de Fess
----------------------------------

Configure la información de conexión SSO en la página [Sistema] > [General] de la consola de administración.
Los principales elementos de configuración son los siguientes:

- URL del proveedor OpenID Connect (endpoint de Entra ID)
- ID de cliente
- Secreto de cliente
- Alcances (openid, profile, email, etc.)
- Configuración de claims de grupo

Mapeo de grupos a roles
-------------------------

Asigne los grupos de Entra ID a los roles de Fess.
Esto permite que la gestión de grupos en Entra ID se refleje directamente en el control de los resultados de búsqueda.

Ejemplo: Grupo de Entra ID "Engineering" -> Rol de Fess "engineering_role"

Integración SSO mediante SAML
================================

La integración SAML es adecuada para entornos donde existe un IdP SAML existente.

Descripción general del flujo de autenticación
-------------------------------------------------

En SAML, se intercambian SAML Assertions entre el SP (Service Provider = Fess) y el IdP.

1. Un usuario accede a Fess
2. Fess envía un SAML AuthnRequest al IdP
3. El IdP autentica al usuario
4. El IdP devuelve una SAML Response (que contiene atributos de usuario) a Fess
5. Fess asigna roles en función de los atributos de usuario

Configuración en el lado de Fess
----------------------------------

Para la integración SAML, se requieren las siguientes configuraciones:

- URL de metadatos o archivo XML del IdP
- ID de entidad del SP
- Assertion Consumer Service URL
- Mapeo de atributos (nombre de usuario, dirección de correo electrónico, grupos)

Integración SPNEGO / Kerberos
================================

En entornos de Windows Active Directory, se puede utilizar la autenticación integrada de Windows mediante SPNEGO/Kerberos.
Cuando se accede a través de un navegador desde un PC unido al dominio, la autenticación se realiza automáticamente sin operaciones de inicio de sesión adicionales.

Este método es el más transparente para los usuarios, pero la configuración es la más compleja.
Se requiere un entorno de dominio de Active Directory como prerrequisito.

Cifrado de comunicaciones
===========================

Configuración de SSL/TLS
--------------------------

En entornos de producción, se recomienda realizar todos los accesos a Fess a través de HTTPS.

**Método de proxy inverso (recomendado)**

Despliegue Nginx o Apache HTTP Server como proxy inverso para realizar la terminación SSL.
Fess en si opera sobre HTTP, y el proxy inverso maneja HTTPS.

::

    [Cliente] --HTTPS--> [Nginx] --HTTP--> [Fess]

La ventaja de este método es que la gestión de certificados se centraliza en el proxy inverso.

**Método de configuración directa en Fess**

También es posible configurar certificados SSL directamente en el Tomcat de Fess.
Esto es adecuado para entornos de pequeña escala o cuando no se despliega un proxy inverso.

Seguridad del acceso a la API
================================

A continuación, se refuerza la seguridad de la integración con la API presentada en la Parte 11.

Diseño de permisos de tokens
------------------------------

Configure los permisos adecuados para los tokens de acceso.

.. list-table:: Ejemplo de diseño de tokens
   :header-rows: 1
   :widths: 25 25 50

   * - Propósito
     - Permisos
     - Notas
   * - Widget de búsqueda
     - Solo búsqueda (solo lectura)
     - Utilizado en el frontend
   * - Procesamiento por lotes
     - Búsqueda + Indexación
     - Utilizado en el lado del servidor
   * - Automatización de administración
     - Acceso a la API de administración
     - Utilizado en scripts operativos

Gestión de tokens
------------------

- Rotación periódica (cada 3 a 6 meses)
- Revocación inmediata de los tokens que ya no son necesarios
- Supervisión del uso de tokens

Auditoría y registros
=======================

Los registros de auditoría en un sistema de búsqueda son importantes para investigar incidentes de seguridad y garantizar el cumplimiento normativo.

Registros generados por Fess
------------------------------

- **Registros de búsqueda**: Quién buscó qué (se pueden consultar en [Información del sistema] > [Registro de búsqueda] en la consola de administración)
- **Registros de auditoría** (``audit.log``): Operaciones como inicio de sesión, cierre de sesión, acceso y cambios de permisos se registran de manera unificada

Retención de registros
-----------------------

Configure el período de retención de registros según los requisitos de seguridad.
Si existen requisitos de cumplimiento normativo, considere el reenvío de registros a un sistema externo de gestión de registros (SIEM).

Resumen
========

En este artículo, diseñamos una arquitectura de seguridad para Fess en un entorno empresarial.

- Tres opciones de integración SSO (OIDC, SAML, SPNEGO) y sus escenarios de aplicación
- Diseño de la integración con Entra ID mediante OpenID Connect
- Cifrado de comunicaciones mediante SSL/TLS
- Diseño de permisos para tokens de acceso a la API
- Gestión de registros de auditoría

Construya una infraestructura de búsqueda segura manteniendo el equilibrio entre seguridad y usabilidad.

En el próximo artículo, se abordará la automatización de la infraestructura de búsqueda.

Referencias
============

- `Configuración SSO de Fess <https://fess.codelibs.org/ja/15.5/config/sso.html>`__

- `Configuración de seguridad de Fess <https://fess.codelibs.org/ja/15.5/config/security.html>`__
