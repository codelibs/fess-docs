====================================================================
Servidor de Búsqueda Basado en Elasticsearch con Fess ~ Edición de Búsqueda Basada en Roles
====================================================================

Introducción
========

Este artículo presenta la función de búsqueda basada en roles, que es una de las características distintivas de Fess.

Este artículo utiliza Fess 15.3.0 para la explicación.
Para el método de construcción de Fess, consulte la `edición de introducción <https://fess.codelibs.org/ja/articles/article-1.html>`__.

Lectores Objetivo
========

-  Personas que desean construir un sistema de búsqueda en sistemas con autenticación como sitios de portal

-  Personas que desean construir un entorno de búsqueda según los permisos de visualización

Entorno Necesario
==========

El contenido de este artículo ha sido verificado en el siguiente entorno.

-  Ubuntu 22.04

-  OpenJDK 21

Búsqueda Basada en Roles
================

La búsqueda basada en roles de Fess es una función que diferencia los resultados de búsqueda según la información de autenticación del usuario autenticado.
Por ejemplo, el empleado de ventas A que tiene el rol de departamento de ventas verá información del rol de departamento de ventas en los resultados de búsqueda, pero el empleado técnico B que no tiene el rol de departamento de ventas no la verá incluso si busca.
Al utilizar esta función, es posible realizar búsquedas separadas por departamento o cargo para usuarios que han iniciado sesión en portales o entornos de inicio de sesión único.

Por defecto, la búsqueda basada en roles de Fess puede diferenciar los resultados de búsqueda según la información de usuario gestionada por Fess.
Además de esto, también se puede utilizar en integración con información de autenticación de LDAP o Active Directory.
Además de estos sistemas de autenticación, la información de rol también se puede obtener de las siguientes ubicaciones.

1. Parámetros de solicitud

2. Encabezados de solicitud

3. Cookies

4. Información de autenticación J2EE

Como método de uso, en servidores de portal o sistemas de inicio de sesión único tipo agente, se puede pasar información de autenticación a Fess guardando la información de autenticación en cookies para el dominio y ruta donde opera Fess durante la autenticación.
Además, en sistemas de inicio de sesión único tipo proxy inverso, se puede obtener información de rol en Fess agregando información de autenticación a parámetros de solicitud o encabezados de solicitud al acceder a Fess.
De esta manera, al integrarse con varios sistemas de autenticación, es posible diferenciar los resultados de búsqueda para cada usuario.

Configuración para Usar la Búsqueda Basada en Roles
====================================

Se asume que Fess 15.3.0 está instalado.
Si aún no lo ha instalado, instálelo consultando la `edición de introducción <https://fess.codelibs.org/ja/articles/article-1.html>`__.

Esta vez se explicará la búsqueda por roles utilizando la función de gestión de usuarios de Fess.

Descripción General de la Configuración
----------

Esta vez se crearán dos roles: departamento de ventas (sales) y departamento técnico (eng). El usuario taro pertenecerá al rol sales y podrá obtener resultados de búsqueda de \https://www.n2sm.net/, y el usuario hanako pertenecerá al rol eng y podrá obtener resultados de búsqueda de \https://fess.codelibs.org/.

Creación de Roles
------------

Primero acceda a la pantalla de administración.
\http://localhost:8080/admin/

Desde Usuario > Rol > Crear nuevo, ingrese "sales" en el nombre y cree el rol sales.
Cree el rol eng de manera similar.

Lista de roles
|image0|


Creación de Rol para Rastreador
----------------------

Presione Usuario > Rol > sales > Crear nuevo rol para rastreador.
Ingrese "Departamento de Ventas" en el nombre, mantenga el valor como "sales" y presione [Crear].
Entonces, se agregará la configuración de Departamento de Ventas a la lista de Rastreador > Rol.

De manera similar, registre el nombre del rol para rastreador del rol eng como "Departamento Técnico".

Lista de roles para rastreador
|image1|


Creación de Usuarios
--------------

Cree los usuarios taro y hanako desde Usuario > Usuario > Crear nuevo con la siguiente configuración.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * -
     - Taro
     - Hanako
   * - Nombre de usuario
     - taro
     - hanako
   * - Contraseña
     - taro
     - hanako
   * - Rol
     - sales
     - eng


Verificación de Usuarios Registrados
------------------

Con la configuración actual, hay tres usuarios que pueden iniciar sesión en Fess: admin, taro y hanako.
Verifique que pueda iniciar sesión con cada uno.
Acceda a \http://localhost:8080/admin/ e inicie sesión con el usuario admin para mostrar la pantalla de administración normalmente.
A continuación, cierre sesión del usuario admin. Haga clic en el botón en la parte superior derecha de la pantalla de administración.

Botón de cierre de sesión
|image2|

Ingrese el nombre de usuario y contraseña e inicie sesión con taro o hanako.
Si el inicio de sesión es exitoso, se mostrará la pantalla de búsqueda de \http://localhost:8080/.

Adición de Configuración de Rastreo
------------------

Registre los objetivos de rastreo.
Esta vez, los usuarios con rol de departamento de ventas solo podrán buscar en \https://www.n2sm.net/, y los usuarios con rol de departamento técnico solo podrán buscar en \https://fess.codelibs.org/.
Para registrar estas configuraciones de rastreo, haga clic en Rastreador > Web > Crear nuevo para crear la configuración de rastreo web.
Esta vez use la siguiente configuración. Los demás valores son predeterminados.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * -
     - N2SM
     - Fess
   * - Nombre
     - N2SM
     - Fess
   * - URL
     - \https://www.n2sm.net/
     - \https://fess.codelibs.org/
   * - URL a rastrear
     - \https://www.n2sm.net/.*
     - \https://fess.codelibs.org/.*
   * - Número máximo de accesos
     - 10
     - 10
   * - Intervalo
     - 3000 milisegundos
     - 3000 milisegundos
   * - Rol
     - Departamento de Ventas
     - Departamento Técnico

Inicio del Rastreo
--------------

Después de registrar la configuración de rastreo, presione [Iniciar ahora] desde Sistema > Programador > Default Crawler. Espere un momento hasta que se complete el rastreo.

Búsqueda
----

Después de completar el rastreo, acceda a \http://localhost:8080/, busque una palabra como "fess" sin iniciar sesión y verifique que no se muestren resultados de búsqueda.
A continuación, inicie sesión con el usuario taro y busque de manera similar.
Dado que el usuario taro tiene el rol sales, solo se mostrarán los resultados de búsqueda de \https://www.n2sm.net/.

Pantalla de búsqueda con rol sales
|image3|

Cierre sesión del usuario taro e inicie sesión con el usuario hanako.
Al buscar de manera similar que antes, dado que el usuario hanako tiene el rol eng, solo se mostrarán los resultados de búsqueda de \https://fess.codelibs.org/.

Pantalla de búsqueda con rol eng
|image4|

Resumen
======

Se ha presentado la búsqueda basada en roles, que es una de las funciones de seguridad de Fess.
Se explicó centrándose en la búsqueda basada en roles utilizando información de autenticación J2EE, pero dado que la transferencia de información de autenticación a Fess es una implementación genérica, creo que puede corresponder a varios sistemas de autenticación.
Dado que es posible diferenciar los resultados de búsqueda según los atributos del usuario, también es posible realizar sistemas que requieren búsqueda según los permisos de visualización, como sitios de portal internos o carpetas compartidas.

Material de Referencia
========

-  `Fess <https://fess.codelibs.org/ja/>`__

.. |image0| image:: ../../resources/images/en/article/3/role-1.png
.. |image1| image:: ../../resources/images/en/article/3/role-2.png
.. |image2| image:: ../../resources/images/en/article/3/logout.png
.. |image3| image:: ../../resources/images/en/article/3/search-by-sales.png
.. |image4| image:: ../../resources/images/en/article/3/search-by-eng.png
