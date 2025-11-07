=========================================
Instalación en Windows (Procedimientos Detallados)
=========================================

Esta página describe los procedimientos de instalación de |Fess| en entornos Windows.
Describe el método de instalación utilizando el paquete ZIP.

.. warning::

   No se recomienda ejecutar con OpenSearch integrado en entornos de producción.
   Asegúrese de construir un servidor OpenSearch externo.

Requisitos Previos
==================

- Cumplir con los requisitos del sistema descritos en :doc:`prerequisites`
- Java 21 instalado
- OpenSearch 3.3.0 disponible (o nueva instalación)
- Variable de entorno ``JAVA_HOME`` de Windows configurada apropiadamente

Verificación de la Instalación de Java
=======================================

Abra el Símbolo del sistema o PowerShell y verifique la versión de Java con el siguiente comando.

En caso de Símbolo del sistema::

    C:\> java -version

En caso de PowerShell::

    PS C:\> java -version

Verifique que se muestre Java 21 o posterior.

Configuración de Variables de Entorno
======================================

1. Configuración de la variable de entorno ``JAVA_HOME``

   Configure el directorio donde está instalado Java como ``JAVA_HOME``.

   Ejemplo::

       JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.1.12-hotspot

2. Agregar a la variable de entorno ``PATH``

   Agregue ``%JAVA_HOME%\bin`` a la variable de entorno ``PATH``.

.. tip::

   Método para configurar variables de entorno:

   1. Abra "Configuración" desde el menú "Inicio"
   2. Haga clic en "Sistema" → "Acerca de" → "Configuración avanzada del sistema"
   3. Haga clic en el botón "Variables de entorno"
   4. Configure en "Variables de entorno del sistema" o "Variables de entorno del usuario"

Paso 1: Instalación de OpenSearch
==================================

Descarga de OpenSearch
-----------------------

1. Descargue el paquete ZIP para Windows desde `Download OpenSearch <https://opensearch.org/downloads.html>`__.

2. Extraiga el archivo ZIP descargado en cualquier directorio.

   Ejemplo::

       C:\opensearch-3.3.0

   .. note::

      Se recomienda seleccionar un directorio que no contenga caracteres japoneses o espacios en la ruta.

Instalación de Plugins de OpenSearch
-------------------------------------

Abra el Símbolo del sistema **con privilegios de administrador** y ejecute los siguientes comandos.

::

    C:\> cd C:\opensearch-3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-minhash:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.0

.. important::

   Las versiones de los plugins deben coincidir con la versión de OpenSearch.
   En el ejemplo anterior, se especifica 3.3.0 para todos.

Configuración de OpenSearch
----------------------------

Abra ``config\opensearch.yml`` con un editor de texto y agregue la siguiente configuración.

::

    # Ruta para sincronización de configuración (especificar ruta absoluta)
    configsync.config_path: C:/opensearch-3.3.0/data/config/

    # Desactivación del plugin de seguridad (solo entorno de desarrollo)
    plugins.security.disabled: true

.. warning::

   **Nota Importante sobre Seguridad**

   ``plugins.security.disabled: true`` debe usarse solo en entornos de desarrollo o prueba.
   En entornos de producción, habilite el plugin de seguridad de OpenSearch y configure apropiadamente la autenticación y autorización.
   Para más detalles, consulte :doc:`security`.

.. note::

   En Windows, use ``/`` en lugar de ``\`` como separador de ruta.
   Escriba ``C:/opensearch-3.3.0/data/config/`` en lugar de ``C:\opensearch-3.3.0\data\config\``.

.. tip::

   Otras configuraciones recomendadas::

       cluster.name: fess-cluster
       node.name: fess-node-1
       network.host: 0.0.0.0
       discovery.type: single-node

Paso 2: Instalación de Fess
============================

Descarga de Fess
----------------

1. Descargue el paquete ZIP para Windows desde el `sitio de descargas <https://fess.codelibs.org/ja/downloads.html>`__.

2. Extraiga el archivo ZIP descargado en cualquier directorio.

   Ejemplo::

       C:\fess-15.3.0

   .. note::

      Se recomienda seleccionar un directorio que no contenga caracteres japoneses o espacios en la ruta.

Configuración de Fess
---------------------

Abra ``bin\fess.in.bat`` con un editor de texto y agregue o modifique la siguiente configuración.

::

    set SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    set FESS_DICTIONARY_PATH=C:/opensearch-3.3.0/data/config/

.. note::

   - Si está ejecutando OpenSearch en otro host, cambie ``SEARCH_ENGINE_HTTP_URL`` al nombre de host o dirección IP apropiados.
   - Use ``/`` como separador de ruta.

Verificación de la Instalación
-------------------------------

Verifique que los archivos de configuración se hayan editado correctamente.

En el Símbolo del sistema::

    C:\> findstr "SEARCH_ENGINE_HTTP_URL" C:\fess-15.3.0\bin\fess.in.bat
    C:\> findstr "FESS_DICTIONARY_PATH" C:\fess-15.3.0\bin\fess.in.bat

Paso 3: Inicio
==============

Para los procedimientos de inicio, consulte :doc:`run`.

Registro como Servicio de Windows (Opcional)
=============================================

Al registrar |Fess| y OpenSearch como servicios de Windows, se puede configurar para que inicien automáticamente al iniciar el sistema.

.. note::

   Para registrar como servicio de Windows, es necesario usar herramientas de terceros (como NSSM).
   Para procedimientos detallados, consulte la documentación de cada herramienta.

Ejemplo Usando NSSM
--------------------

1. Descargue y extraiga `NSSM (Non-Sucking Service Manager) <https://nssm.cc/download>`__.

2. Registre OpenSearch como servicio::

       C:\> nssm install OpenSearch C:\opensearch-3.3.0\bin\opensearch.bat

3. Registre Fess como servicio::

       C:\> nssm install Fess C:\fess-15.3.0\bin\fess.bat

4. Configure la dependencia del servicio (Fess depende de OpenSearch)::

       C:\> sc config Fess depend= OpenSearch

5. Inicio del servicio::

       C:\> net start OpenSearch
       C:\> net start Fess

Configuración del Cortafuegos
==============================

Abra los puertos necesarios en el Firewall de Windows Defender.

1. Abra "Panel de control" → "Firewall de Windows Defender" → "Configuración avanzada"

2. Cree una nueva regla en "Reglas de entrada"

   - Tipo de regla: Puerto
   - Protocolo y puerto: TCP, 8080
   - Acción: Permitir conexión
   - Nombre: Fess Web Interface

O ejecute en PowerShell::

    PS C:\> New-NetFirewallRule -DisplayName "Fess Web Interface" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow

Solución de Problemas
======================

Conflicto de Números de Puerto
-------------------------------

Si los puertos 8080 o 9200 ya están en uso, puede verificarlo con el siguiente comando::

    C:\> netstat -ano | findstr :8080
    C:\> netstat -ano | findstr :9200

Cambie el número de puerto en uso o detenga el proceso que está en conflicto.

Limitación de Longitud de Ruta
-------------------------------

En Windows, existe una limitación en la longitud de la ruta. Se recomienda instalar en una ruta lo más corta posible.

Ejemplo::

    C:\opensearch  (recomendado)
    C:\Program Files\opensearch-3.3.0  (no recomendado - ruta larga)

Java no Reconocido
------------------

Si aparece un error al ejecutar el comando ``java -version``:

1. Verifique que la variable de entorno ``JAVA_HOME`` esté configurada correctamente
2. Verifique que ``%JAVA_HOME%\bin`` esté incluido en la variable de entorno ``PATH``
3. Reinicie el Símbolo del sistema para reflejar la configuración

Próximos Pasos
==============

Después de completar la instalación, consulte la siguiente documentación:

- :doc:`run` - Inicio de |Fess| y configuración inicial
- :doc:`security` - Configuración de seguridad para entornos de producción
- :doc:`troubleshooting` - Solución de problemas

Preguntas Frecuentes
=====================

P: ¿Se recomienda la operación en Windows Server?
--------------------------------------------------

R: Sí, la operación en Windows Server es posible.
Al operar en Windows Server, regístrelo como servicio de Windows y configure el monitoreo apropiado.

P: ¿Cuál es la diferencia entre las versiones de 64 bits y 32 bits?
--------------------------------------------------------------------

R: |Fess| y OpenSearch solo admiten la versión de 64 bits.
No funcionan en Windows de 32 bits.

P: ¿Qué hacer si la ruta contiene japonés?
-------------------------------------------

R: En la medida de lo posible, instale en una ruta que no contenga caracteres japoneses o espacios.
Si es absolutamente necesario usar una ruta con japonés, es necesario escapar apropiadamente la ruta en el archivo de configuración.
