=======================================
Instalación en Linux (Procedimientos Detallados)
=======================================

Esta página describe los procedimientos de instalación de |Fess| en entornos Linux.
Es compatible con los formatos de paquete TAR.GZ, RPM y DEB.

.. warning::

   No se recomienda ejecutar con OpenSearch integrado en entornos de producción.
   Asegúrese de construir un servidor OpenSearch externo.

Requisitos Previos
==================

- Cumplir con los requisitos del sistema descritos en :doc:`prerequisites`
- Java 21 instalado
- OpenSearch 3.3.2 disponible (o nueva instalación)

Selección del Método de Instalación
====================================

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

Instalación con Versión TAR.GZ
===============================

Paso 1: Instalación de OpenSearch
----------------------------------

1. Descarga de OpenSearch

   Descargue la versión TAR.GZ desde `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.tar.gz
       $ tar -xzf opensearch-3.3.2-linux-x64.tar.gz
       $ cd opensearch-3.3.2

   .. note::

      En este ejemplo se utiliza OpenSearch 3.3.2.
      Verifique la versión compatible con |Fess|.

2. Instalación de plugins de OpenSearch

   Instale los plugins requeridos por |Fess|.

   ::

       $ cd /path/to/opensearch-3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

   .. important::

      Las versiones de los plugins deben coincidir con la versión de OpenSearch.
      En el ejemplo anterior, se especifica 3.3.2 para todos.

3. Configuración de OpenSearch

   Agregue la siguiente configuración a ``config/opensearch.yml``.

   ::

       # Ruta para sincronización de configuración (especificar ruta absoluta)
       configsync.config_path: /path/to/opensearch-3.3.2/data/config/

       # Desactivación del plugin de seguridad (solo entorno de desarrollo)
       plugins.security.disabled: true

   .. warning::

      **Nota Importante sobre Seguridad**

      ``plugins.security.disabled: true`` debe usarse solo en entornos de desarrollo o prueba.
      En entornos de producción, habilite el plugin de seguridad de OpenSearch y configure apropiadamente la autenticación y autorización.
      Para más detalles, consulte :doc:`security`.

   .. tip::

      Ajuste otras configuraciones como nombre del clúster y configuración de red según su entorno.
      Ejemplo de configuración::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

Paso 2: Instalación de Fess
----------------------------

1. Descarga y extracción de Fess

   Descargue la versión TAR.GZ desde el `sitio de descargas <https://fess.codelibs.org/ja/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.tar.gz
       $ tar -xzf fess-15.3.2.tar.gz
       $ cd fess-15.3.2

2. Configuración de Fess

   Edite ``bin/fess.in.sh`` para configurar la información de conexión a OpenSearch.

   ::

       $ vi bin/fess.in.sh

   Agregue o modifique la siguiente configuración::

       # Punto final HTTP de OpenSearch
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

       # Ruta de ubicación de archivos de diccionario (igual que configsync.config_path de OpenSearch)
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.3.2/data/config/

   .. note::

      Si está ejecutando OpenSearch en otro host,
      cambie ``SEARCH_ENGINE_HTTP_URL`` al nombre de host o dirección IP apropiados.
      Ejemplo: ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``

3. Verificación de la instalación

   Verifique que los archivos de configuración se hayan editado correctamente::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

Paso 3: Inicio
--------------

Para los procedimientos de inicio, consulte :doc:`run`.

Instalación con Versión RPM
============================

La versión RPM se utiliza en distribuciones Linux basadas en RPM como Red Hat Enterprise Linux, CentOS, Fedora, etc.

Paso 1: Instalación de OpenSearch
----------------------------------

1. Descarga e instalación de RPM de OpenSearch

   Descargue e instale el paquete RPM desde `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.3.2-linux-x64.rpm

   Alternativamente, también puede agregar un repositorio para instalar.
   Para más detalles, consulte `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__.

2. Instalación de plugins de OpenSearch

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

3. Configuración de OpenSearch

   Agregue la siguiente configuración a ``/etc/opensearch/opensearch.yml``.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   Configuración a agregar::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      No utilice ``plugins.security.disabled: true`` en entornos de producción.
      Consulte :doc:`security` para configurar apropiadamente la seguridad.

Paso 2: Instalación de Fess
----------------------------

1. Instalación de RPM de Fess

   Descargue e instale el paquete RPM desde el `sitio de descargas <https://fess.codelibs.org/ja/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.rpm
       $ sudo rpm -ivh fess-15.3.2.rpm

2. Configuración de Fess

   Edite ``/usr/share/fess/bin/fess.in.sh``.

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   Agregue o modifique la siguiente configuración::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. Registro del servicio

   **En caso de usar chkconfig**::

       $ sudo /sbin/chkconfig --add opensearch
       $ sudo /sbin/chkconfig --add fess

   **En caso de usar systemd** (recomendado)::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

Paso 3: Inicio
--------------

Para los procedimientos de inicio, consulte :doc:`run`.

Instalación con Versión DEB
============================

La versión DEB se utiliza en distribuciones Linux basadas en DEB como Debian, Ubuntu, etc.

Paso 1: Instalación de OpenSearch
----------------------------------

1. Descarga e instalación de DEB de OpenSearch

   Descargue e instale el paquete DEB desde `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.deb
       $ sudo dpkg -i opensearch-3.3.2-linux-x64.deb

   Alternativamente, también puede agregar un repositorio para instalar.
   Para más detalles, consulte `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__.

2. Instalación de plugins de OpenSearch

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

3. Configuración de OpenSearch

   Agregue la siguiente configuración a ``/etc/opensearch/opensearch.yml``.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   Configuración a agregar::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      No utilice ``plugins.security.disabled: true`` en entornos de producción.
      Consulte :doc:`security` para configurar apropiadamente la seguridad.

Paso 2: Instalación de Fess
----------------------------

1. Instalación de DEB de Fess

   Descargue e instale el paquete DEB desde el `sitio de descargas <https://fess.codelibs.org/ja/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.deb
       $ sudo dpkg -i fess-15.3.2.deb

2. Configuración de Fess

   Edite ``/usr/share/fess/bin/fess.in.sh``.

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   Agregue o modifique la siguiente configuración::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. Registro del servicio

   Habilite el servicio usando systemd::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

Paso 3: Inicio
--------------

Para los procedimientos de inicio, consulte :doc:`run`.

Verificación Posterior a la Instalación
========================================

Después de completar la instalación, verifique lo siguiente:

1. **Verificación de archivos de configuración**

   - Archivo de configuración de OpenSearch (opensearch.yml)
   - Archivo de configuración de Fess (fess.in.sh)

2. **Permisos de directorio**

   Verifique que existan los directorios especificados en la configuración y que se hayan establecido los permisos apropiados.

   Para versión TAR.GZ::

       $ ls -ld /path/to/opensearch-3.3.2/data/config/

   Para versiones RPM/DEB::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **Verificación de versión de Java**

   ::

       $ java -version

   Verifique que esté instalado Java 21 o posterior.

Próximos Pasos
==============

Después de completar la instalación, consulte la siguiente documentación:

- :doc:`run` - Inicio de |Fess| y configuración inicial
- :doc:`security` - Configuración de seguridad para entornos de producción
- :doc:`troubleshooting` - Solución de problemas

Preguntas Frecuentes
=====================

P: ¿Funcionan otras versiones de OpenSearch?
---------------------------------------------

R: |Fess| depende de una versión específica de OpenSearch.
Se recomienda encarecidamente usar la versión recomendada (3.3.2) para garantizar la compatibilidad de los plugins.
Si usa otras versiones, también debe ajustar apropiadamente las versiones de los plugins.

P: ¿Se puede compartir el mismo OpenSearch entre múltiples instancias de Fess?
-------------------------------------------------------------------------------

R: Es posible, pero no se recomienda. Se recomienda preparar un clúster de OpenSearch dedicado para cada instancia de Fess.
Si comparte OpenSearch entre múltiples instancias de Fess, tenga cuidado con las colisiones de nombres de índice.

P: ¿Cómo configurar OpenSearch en clúster?
-------------------------------------------

R: Consulte la documentación oficial de OpenSearch `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__.
Al configurar en clúster, debe eliminar la configuración ``discovery.type: single-node`` y agregar la configuración de clúster apropiada.
