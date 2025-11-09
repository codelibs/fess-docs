======
Cómo Usar
======

Esta página explica el uso básico de Fess.
Si aún no ha instalado Fess, consulte :doc:`setup` o :doc:`quick-start`.

Acerca de la interfaz de usuario de Fess
===================

Fess proporciona las siguientes interfaces de usuario:

-  Interfaz de búsqueda y resultados mediante navegador (para usuarios generales)
-  Interfaz de administración mediante navegador (para administradores)

Pantalla de Búsqueda (Para Usuarios Generales)
===========================

Acceso a la Pantalla de Búsqueda
------------------

Esta es la interfaz de usuario para que los usuarios generales busquen documentos indexados por Fess.

Al acceder a http://localhost:8080/, se mostrará el campo de entrada de términos de búsqueda y el botón de búsqueda.

Búsqueda Básica
----------

Ingrese la palabra que desea buscar y haga clic en el botón de búsqueda para ver los resultados.

|Visualización de resultados de búsqueda en el navegador|

Los resultados de búsqueda muestran la siguiente información:

- Título
- URL
- Extracto del texto (las palabras clave de búsqueda se resaltan)
- Fecha de última actualización
- Tamaño del archivo (en caso de documentos)

Búsqueda Avanzada
--------

**Búsqueda AND**

Si ingresa múltiples palabras clave separadas por espacios, se buscarán documentos que contengan todas las palabras clave.

Ejemplo: ``Fess búsqueda`` → Documentos que contienen tanto "Fess" como "búsqueda"

**Búsqueda OR**

Si ingresa ``OR`` entre las palabras clave, se buscarán documentos que contengan cualquiera de las palabras clave.

Ejemplo: ``Fess OR Elasticsearch`` → Documentos que contienen "Fess" o "Elasticsearch"

**Búsqueda NOT**

Si agrega ``-`` antes de una palabra clave que desea excluir, se buscarán documentos que no contengan esa palabra clave.

Ejemplo: ``Fess -Elasticsearch`` → Documentos que contienen "Fess" pero no "Elasticsearch"

**Búsqueda de Frases**

Si encierra palabras clave entre ``""``, buscará esa frase exacta.

Ejemplo: ``"búsqueda de texto completo"`` → Documentos que contienen la palabra "búsqueda de texto completo"

Opciones de Búsqueda
------------

Las siguientes opciones están disponibles en la pantalla de búsqueda:

- **Búsqueda por etiqueta**: Buscar solo documentos con etiquetas específicas
- **Especificación de período**: Buscar solo documentos actualizados en un período específico
- **Especificación de formato de archivo**: Buscar solo formatos de archivo específicos (PDF, Word, etc.)

Pantalla de Administración (Para Administradores)
====================

Acceso a la Pantalla de Administración
------------------

Esta es la interfaz de usuario para que los administradores gestionen Fess.

Al acceder a http://localhost:8080/admin/, se mostrará la pantalla de inicio de sesión.

Cuenta de administrador predeterminada:

- **Nombre de usuario**: ``admin``
- **Contraseña**: ``admin``

.. warning::

   **Nota importante sobre seguridad**

   Asegúrese de cambiar la contraseña predeterminada.
   Especialmente en entornos de producción, se recomienda encarecidamente cambiar la contraseña inmediatamente después del primer inicio de sesión.

.. note::

   La interfaz de administración no es compatible con Responsive Web Design.
   Se recomienda acceder desde un navegador de PC.

Principales Funciones de Administración
----------

Al iniciar sesión, puede acceder a las siguientes funciones de configuración y administración:

**Configuración del Rastreador**

- Configuración de rastreo web
- Configuración de rastreo del sistema de archivos
- Configuración de rastreo del almacén de datos

**Configuración del Sistema**

- Configuración general (zona horaria, configuración de correo, etc.)
- Gestión de usuarios y roles
- Configuración del programador
- Configuración de diseño

**Configuración de Búsqueda**

- Gestión de etiquetas
- Ajuste de relevancia de palabras clave
- Gestión de sinónimos y diccionarios

Para obtener métodos de administración detallados, consulte la Guía del Usuario.

Próximos Pasos
==========

Una vez que comprenda el uso básico, puede consultar la siguiente documentación para aprender más:

- **Guía del Usuario**: Detalles sobre la configuración de rastreo y búsqueda
- **Documentación de API**: Integración de búsqueda mediante REST API
- **Guía del Desarrollador**: Desarrollo de personalizaciones y extensiones

.. |Visualización de resultados de búsqueda en el navegador| image:: ../resources/images/en/fess_search_result.png

