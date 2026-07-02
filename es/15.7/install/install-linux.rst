========================================================
Instalación en Linux (Procedimientos Detallados)
========================================================

Esta página describe los procedimientos de instalación de |Fess| en entornos Linux.
Es compatible con los formatos de paquete TAR.GZ, RPM y DEB.

.. warning::

   No se recomienda ejecutar con OpenSearch integrado en entornos de producción.
   Asegúrese de construir un servidor OpenSearch externo.

Requisitos Previos
===================

- Cumplir con los requisitos del sistema descritos en :doc:`prerequisites`
- Java 21 instalado
- OpenSearch 3.7.0 disponible (o nueva instalación)

Selección del Método de Instalación
=====================================

En entornos Linux, puede seleccionar entre los siguientes métodos de instalación:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Método
     - Entorno Recomendado
     - Características
   * - TAR.GZ
     - Entorno de desarrollo, entornos que requieren personalización
     - Expandible en cualquier directorio
   * - RPM
     - Sistemas basados en RHEL, CentOS, Fedora
     - Gestión de servicios posible con systemd
   * - DEB
     - Sistemas basados en Debian, Ubuntu
     - Gestión de servicios posible con systemd

Configuración del Sistema para Ejecutar OpenSearch
=====================================================

Para que OpenSearch funcione de manera estable en Linux, configure los siguientes parámetros del kernel y límites de recursos.
Estos son necesarios principalmente para la versión TAR.GZ (cuando OpenSearch se instala manualmente).
En las versiones RPM / DEB, los paquetes de OpenSearch y |Fess| configuran el número de descriptores de archivo, entre otros, a través de systemd, pero dado que ``vm.max_map_count`` es una configuración del kernel del lado del host, verifíquela con cualquiera de los dos métodos.

Número Máximo de Mapas de Memoria Virtual
--------------------------------------------

Dado que OpenSearch utiliza numerosos mapas de memoria, configure ``vm.max_map_count`` en ``262144`` o más.

Para configurarlo de forma temporal::

    $ sudo sysctl -w vm.max_map_count=262144

Para configurarlo de forma permanente::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

Número de Descriptores de Archivo
--------------------------------------------

Cuando ejecute OpenSearch manualmente (versión TAR.GZ), configure el límite superior del número de descriptores de archivo del usuario que ejecuta OpenSearch en ``65535`` o más.

Agregue lo siguiente a ``/etc/security/limits.conf`` (reemplace ``opensearch`` por el nombre del usuario que ejecuta OpenSearch)::

    opensearch  -  nofile  65535

.. note::

   En las versiones RPM / DEB, esta configuración no es necesaria, ya que el límite superior del número de descriptores de archivo se establece en la definición del servicio systemd.

Instalación con Versión TAR.GZ
=================================

Paso 1: Instalación de OpenSearch
------------------------------------

1. Descarga de OpenSearch

   Descargue la versión TAR.GZ desde `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.tar.gz
       $ tar -xzf opensearch-3.7.0-linux-x64.tar.gz
       $ cd opensearch-3.7.0

   .. note::

      En este ejemplo se utiliza OpenSearch 3.7.0.
      |Fess| 15.7 es compatible con OpenSearch 3.7.0.

2. Instalación de plugins de OpenSearch

   Instale los plugins que requiere |Fess|.

   ::

       $ cd /path/to/opensearch-3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

   .. important::

      Las versiones de los plugins deben coincidir con la versión de OpenSearch.
      En el ejemplo anterior, se especifica 3.7.0 para todos.

3. Configuración de OpenSearch

   Agregue la siguiente configuración a ``config/opensearch.yml``.

   ::

       # Ruta para sincronización de configuración (especificar ruta absoluta)
       configsync.config_path: /path/to/opensearch-3.7.0/data/config/

       # Desactivación del plugin de seguridad (solo entorno de desarrollo)
       plugins.security.disabled: true

   .. warning::

      **Nota Importante sobre Seguridad**

      ``plugins.security.disabled: true`` debe usarse únicamente en entornos de desarrollo o de prueba.
      En entornos de producción, habilite el plugin de seguridad de OpenSearch y configure adecuadamente la autenticación y la autorización.
      Si habilita el plugin de seguridad en OpenSearch 2.12 o posterior, es necesario configurar la contraseña de administrador (variable de entorno ``OPENSEARCH_INITIAL_ADMIN_PASSWORD``) en el primer inicio.
      Para más detalles, consulte :doc:`security`.

   .. tip::

      Ajuste otras configuraciones, como el nombre del clúster y la configuración de red, según su entorno.
      Ejemplo de configuración::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

   .. tip::

      El tamaño de heap de OpenSearch se configura mediante ``-Xms`` / ``-Xmx`` en ``config/jvm.options``.
      Se recomienda especificar el mismo valor en ``-Xms`` y ``-Xmx``, tomando como referencia la mitad o menos de la memoria física disponible, y menos de 32 GB.

Paso 2: Instalación de Fess
------------------------------

1. Descarga y extracción de Fess

   Descargue la versión TAR.GZ desde el `sitio de descargas <https://fess.codelibs.org/es/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.tar.gz
       $ tar -xzf fess-15.7.0.tar.gz
       $ cd fess-15.7.0

2. Configuración de Fess

   Edite ``bin/fess.in.sh`` para configurar la información de conexión a OpenSearch.
   Este archivo incluye, de forma predeterminada, la configuración para conectarse a un clúster externo de OpenSearch, comentada de antemano.

   ::

       $ vi bin/fess.in.sh

   Descomente (elimine el ``#`` inicial de) las siguientes 2 líneas ubicadas cerca del principio del archivo.

   Antes del cambio (estado predeterminado)::

       # External opensearch cluster
       #SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       #FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   Después del cambio::

       # External opensearch cluster
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.7.0/data/config/

   .. note::

      - Configure ``FESS_DICTIONARY_PATH`` con la misma ruta que especificó en ``configsync.config_path`` dentro de ``opensearch.yml`` de OpenSearch.
      - Si ejecuta OpenSearch en otro host, cambie ``SEARCH_ENGINE_HTTP_URL`` al nombre de host o dirección IP apropiados. Ejemplo: ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``
      - No agregue una nueva línea ``SEARCH_ENGINE_HTTP_URL=...``; en su lugar, descomente y edite la línea existente.

   .. tip::

      Para cambiar el tamaño de heap de |Fess|, edite ``FESS_MIN_MEM`` (predeterminado: ``256m``) y ``FESS_MAX_MEM`` (predeterminado: ``2g``) en ``bin/fess.in.sh``, o configure la variable de entorno ``FESS_HEAP_SIZE``.

3. Verificación de la instalación

   Verifique que el archivo de configuración se haya editado correctamente::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

Paso 3: Inicio
------------------

Para conocer los procedimientos de inicio, consulte :doc:`run`.

Instalación con Versión RPM
==============================

La versión RPM se utiliza en distribuciones Linux basadas en RPM, como Red Hat Enterprise Linux, CentOS, Fedora, entre otras.

Paso 1: Instalación de OpenSearch
------------------------------------

1. Descarga e instalación del RPM de OpenSearch

   Descargue e instale el paquete RPM desde `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.7.0-linux-x64.rpm

   Alternativamente, también puede agregar un repositorio para instalarlo.
   Para más detalles, consulte `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__.

2. Instalación de plugins de OpenSearch

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

3. Configuración de OpenSearch

   Agregue la siguiente configuración a ``/etc/opensearch/opensearch.yml``.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   Configuración a agregar::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      No utilice ``plugins.security.disabled: true`` en entornos de producción.
      Consulte :doc:`security` para configurar la seguridad de manera adecuada.

Paso 2: Instalación de Fess
------------------------------

1. Instalación del RPM de Fess

   Descargue e instale el paquete RPM desde el `sitio de descargas <https://fess.codelibs.org/es/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.rpm
       $ sudo rpm -ivh fess-15.7.0.rpm

2. Configuración de Fess

   En la versión RPM, edite el archivo de configuración de variables de entorno ``/etc/sysconfig/fess``.
   Este archivo se conserva incluso al actualizar el paquete (no edite directamente ``/usr/share/fess/bin/fess.in.sh``, ya que se sobrescribe durante la actualización).

   ::

       $ sudo vi /etc/sysconfig/fess

   Configure la información de conexión a OpenSearch. Los valores predeterminados son los siguientes. Cámbielos según sea necesario::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      Especifique en ``FESS_DICTIONARY_PATH`` la misma ruta que en ``configsync.config_path`` de ``opensearch.yml``.

3. Registro y habilitación del servicio

   Habilite el servicio utilizando systemd (systemd es el estándar en RHEL 8 y posteriores, y CentOS 8 y posteriores)::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      El servicio de |Fess| depende del servicio de OpenSearch, por lo que es necesario iniciar OpenSearch primero.

   .. note::

      En entornos tradicionales que no utilizan systemd, puede registrar |Fess| con ``chkconfig``::

          $ sudo /sbin/chkconfig --add fess

Paso 3: Inicio
------------------

Para conocer los procedimientos de inicio, consulte :doc:`run`.

Instalación con Versión DEB
==============================

La versión DEB se utiliza en distribuciones Linux basadas en DEB, como Debian, Ubuntu, entre otras.

Paso 1: Instalación de OpenSearch
------------------------------------

1. Descarga e instalación del DEB de OpenSearch

   Descargue e instale el paquete DEB desde `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.deb
       $ sudo dpkg -i opensearch-3.7.0-linux-x64.deb

   Alternativamente, también puede agregar un repositorio para instalarlo.
   Para más detalles, consulte `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__.

2. Instalación de plugins de OpenSearch

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

3. Configuración de OpenSearch

   Agregue la siguiente configuración a ``/etc/opensearch/opensearch.yml``.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   Configuración a agregar::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      No utilice ``plugins.security.disabled: true`` en entornos de producción.
      Consulte :doc:`security` para configurar la seguridad de manera adecuada.

Paso 2: Instalación de Fess
------------------------------

1. Instalación del DEB de Fess

   Descargue e instale el paquete DEB desde el `sitio de descargas <https://fess.codelibs.org/es/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.deb
       $ sudo dpkg -i fess-15.7.0.deb

2. Configuración de Fess

   En la versión DEB, edite el archivo de configuración de variables de entorno ``/etc/default/fess``.
   Este archivo se conserva incluso al actualizar el paquete (no edite directamente ``/usr/share/fess/bin/fess.in.sh``, ya que se sobrescribe durante la actualización).

   ::

       $ sudo vi /etc/default/fess

   Configure la información de conexión a OpenSearch. Los valores predeterminados son los siguientes. Cámbielos según sea necesario::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      Especifique en ``FESS_DICTIONARY_PATH`` la misma ruta que en ``configsync.config_path`` de ``opensearch.yml``.

3. Registro y habilitación del servicio

   Habilite el servicio utilizando systemd::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      El servicio de |Fess| depende del servicio de OpenSearch, por lo que es necesario iniciar OpenSearch primero.

Paso 3: Inicio
------------------

Para conocer los procedimientos de inicio, consulte :doc:`run`.

Verificación Posterior a la Instalación
==========================================

Después de completar la instalación, verifique lo siguiente:

1. **Verificación de los archivos de configuración**

   - Archivo de configuración de OpenSearch (opensearch.yml)
   - Archivo de configuración de |Fess|

     - Versión TAR.GZ: ``bin/fess.in.sh``
     - Versión RPM: ``/etc/sysconfig/fess``
     - Versión DEB: ``/etc/default/fess``

2. **Permisos de directorio**

   Verifique que exista el directorio especificado en la configuración (``configsync.config_path`` / ``FESS_DICTIONARY_PATH``) y que tenga los permisos apropiados.

   Para la versión TAR.GZ::

       $ ls -ld /path/to/opensearch-3.7.0/data/config/

   Para las versiones RPM/DEB::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **Verificación de los parámetros del kernel**

   ::

       $ sysctl vm.max_map_count

   Confirme que el valor sea ``262144`` o superior.

4. **Verificación de la versión de Java**

   ::

       $ java -version

   Verifique que esté instalado Java 21 o posterior.

Próximos Pasos
=================

Después de completar la instalación, consulte la siguiente documentación:

- :doc:`run` - Inicio de |Fess| y configuración inicial
- :doc:`security` - Configuración de seguridad para entornos de producción
- :doc:`troubleshooting` - Solución de problemas

Preguntas Frecuentes
=======================

P: ¿Funciona con otras versiones de OpenSearch?
--------------------------------------------------

R: |Fess| depende de una versión específica de OpenSearch.
Para garantizar la compatibilidad de los plugins, se recomienda encarecidamente utilizar la versión recomendada (3.7.0).
Si utiliza otra versión, también deberá ajustar adecuadamente las versiones de los plugins.

P: ¿Se puede compartir el mismo OpenSearch entre varias instancias de Fess?
--------------------------------------------------------------------------------

R: Es posible, pero no se recomienda. Se recomienda preparar un clúster de OpenSearch dedicado para cada instancia de Fess.
Si comparte OpenSearch entre varias instancias de Fess, tenga cuidado con las colisiones de nombres de índice.

P: ¿Cómo configurar OpenSearch en modo clúster?
--------------------------------------------------

R: Consulte la documentación oficial de OpenSearch `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__.
Para configurar un clúster, debe eliminar la configuración ``discovery.type: single-node`` y agregar la configuración de clúster apropiada.
