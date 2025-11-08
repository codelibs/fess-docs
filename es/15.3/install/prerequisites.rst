====================
Requisitos del Sistema
====================

Esta página describe los requisitos de hardware y software necesarios para ejecutar |Fess|.

Requisitos de Hardware
======================

Requisitos Mínimos
------------------

Los siguientes son los requisitos mínimos para entornos de evaluación y desarrollo:

- CPU: 2 núcleos o más
- Memoria: 4GB o más
- Espacio en Disco: 10GB o más de espacio libre

Requisitos Recomendados
-----------------------

Para entornos de producción, se recomiendan las siguientes especificaciones:

- CPU: 4 núcleos o más
- Memoria: 8GB o más (escalar según el tamaño del índice)
- Espacio en Disco:

  - Área del Sistema: 20GB o más
  - Área de Datos: 3 veces el tamaño del índice o más (incluyendo réplicas)

- Red: 1Gbps o más

.. note::

   Si el tamaño del índice aumenta significativamente o ejecuta rastreos frecuentes,
   escale apropiadamente la memoria y el espacio en disco.

Requisitos de Software
======================

Sistema Operativo
-----------------

|Fess| funciona en los siguientes sistemas operativos:

**Linux**

- Red Hat Enterprise Linux 8 o posterior
- CentOS 8 o posterior
- Ubuntu 20.04 LTS o posterior
- Debian 11 o posterior
- Otras distribuciones de Linux (entornos donde se pueda ejecutar Java 21)

**Windows**

- Windows Server 2019 o posterior
- Windows 10 o posterior

**Otros**

- macOS 11 (Big Sur) o posterior (recomendado solo para entornos de desarrollo)
- Entornos donde se pueda ejecutar Docker

Software Requerido
------------------

Dependiendo del método de instalación, se requiere el siguiente software:

Versión TAR.GZ/ZIP/RPM/DEB
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Java 21**: Se recomienda `Eclipse Temurin <https://adoptium.net/temurin>`__

  - OpenJDK 21 o posterior
  - Eclipse Temurin 21 o posterior

- **OpenSearch 3.3.0**: Obligatorio para entornos de producción (la versión integrada no es recomendada)

  - Versión compatible: OpenSearch 3.3.0
  - Tenga cuidado con la compatibilidad de plugins en otras versiones

Versión Docker
~~~~~~~~~~~~~~

- **Docker**: 20.10 o posterior
- **Docker Compose**: 2.0 o posterior

Requisitos de Red
=================

Puertos Necesarios
------------------

Los puertos principales utilizados por |Fess| son los siguientes:

.. list-table::
   :header-rows: 1
   :widths: 15 15 50

   * - Puerto
     - Protocolo
     - Uso
   * - 8080
     - HTTP
     - Interfaz Web de |Fess| (pantalla de búsqueda y administración)
   * - 9200
     - HTTP
     - API HTTP de OpenSearch (comunicación de |Fess| a OpenSearch)
   * - 9300
     - TCP
     - Comunicación de transporte de OpenSearch (durante configuración en clúster)

.. warning::

   En entornos de producción, se recomienda encarecidamente restringir el acceso directo externo a los puertos 9200 y 9300.
   Estos puertos deben usarse solo para comunicación interna entre |Fess| y OpenSearch.

Configuración del Cortafuegos
------------------------------

Si necesita hacer |Fess| accesible desde el exterior, debe abrir el puerto 8080.

**Linux (en caso de firewalld)**

::

    $ sudo firewall-cmd --permanent --add-port=8080/tcp
    $ sudo firewall-cmd --reload

**Linux (en caso de iptables)**

::

    $ sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
    $ sudo iptables-save

Requisitos del Navegador
=========================

Para las pantallas de administración y búsqueda de |Fess|, se recomiendan los siguientes navegadores:

- Google Chrome (última versión)
- Mozilla Firefox (última versión)
- Microsoft Edge (última versión)
- Safari (última versión)

.. note::

   Internet Explorer no es compatible.

Lista de Verificación de Requisitos Previos
============================================

Antes de la instalación, verifique los siguientes elementos:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Elemento de Verificación
     - Estado
   * - ¿Se cumplen los requisitos de hardware?
     - □
   * - ¿Está instalado Java 21? (excepto versión Docker)
     - □
   * - ¿Está instalado Docker? (versión Docker)
     - □
   * - ¿Están disponibles los puertos necesarios?
     - □
   * - ¿Es apropiada la configuración del cortafuegos?
     - □
   * - ¿Hay suficiente espacio libre en disco?
     - □
   * - ¿Es normal la conexión de red? (si va a rastrear sitios externos)
     - □

Próximos Pasos
==============

Después de verificar los requisitos del sistema, proceda con los procedimientos de instalación según su entorno:

- :doc:`install-linux` - Instalación para Linux (TAR.GZ/RPM/DEB)
- :doc:`install-windows` - Instalación para Windows (ZIP)
- :doc:`install-docker` - Instalación para Docker
- :doc:`install` - Descripción general de los métodos de instalación
