====================================
Selección del Método de Instalación
====================================

Esta página describe una descripción general de los métodos de instalación de |Fess|.
Seleccione el método de instalación apropiado según su entorno.

.. warning::

   **Nota Importante para Entornos de Producción**

   No se recomienda ejecutar con OpenSearch integrado en entornos de producción o pruebas de carga.
   Asegúrese de construir un servidor OpenSearch externo.

Verificación de Requisitos Previos
===================================

Antes de comenzar la instalación, verifique los requisitos del sistema.

Para más detalles, consulte :doc:`prerequisites`.

Comparación de Métodos de Instalación
======================================

|Fess| se puede instalar mediante los siguientes métodos. Seleccione según su entorno y propósito.

.. list-table::
   :header-rows: 1
   :widths: 15 25 30 30

   * - Método
     - SO Objetivo
     - Uso Recomendado
     - Documentación Detallada
   * - Docker
     - Linux, Windows, macOS
     - Entorno de desarrollo/evaluación, configuración rápida
     - :doc:`install-docker`
   * - TAR.GZ
     - Linux, macOS
     - Entornos que requieren personalización
     - :doc:`install-linux`
   * - RPM
     - RHEL, CentOS, Fedora
     - Entorno de producción (basado en RPM)
     - :doc:`install-linux`
   * - DEB
     - Debian, Ubuntu
     - Entorno de producción (basado en DEB)
     - :doc:`install-linux`
   * - ZIP
     - Windows
     - Desarrollo/producción en entorno Windows
     - :doc:`install-windows`

Características de Cada Método de Instalación
==============================================

Versión Docker
--------------

**Ventajas:**

- Configuración más rápida posible
- No se requiere gestión de dependencias
- Ideal para construir entornos de desarrollo
- Fácil inicio y detención de contenedores

**Desventajas:**

- Se requiere conocimiento de Docker

**Entorno Recomendado:** Entorno de desarrollo, entorno de evaluación, POC, entorno de producción

Para más detalles: :doc:`install-docker`

Versión de Paquetes Linux (TAR.GZ/RPM/DEB)
-------------------------------------------

**Ventajas:**

- Alto rendimiento en entorno nativo
- Gestión como servicio del sistema (RPM/DEB)
- Personalización detallada posible

**Desventajas:**

- Se requiere instalación manual de Java y OpenSearch
- Requiere esfuerzo de configuración

**Entorno Recomendado:** Entorno de producción, entornos que requieren personalización

Para más detalles: :doc:`install-linux`

Versión Windows (ZIP)
---------------------

**Ventajas:**

- Funciona en entorno nativo de Windows
- No se requiere instalador

**Desventajas:**

- Se requiere instalación manual de Java y OpenSearch
- Requiere esfuerzo de configuración

**Entorno Recomendado:** Desarrollo/evaluación en entorno Windows, operación de producción en Windows Server

Para más detalles: :doc:`install-windows`

Flujo Básico de Instalación
============================

El flujo básico es el mismo para todos los métodos de instalación.

1. **Verificación de Requisitos del Sistema**

   Consulte :doc:`prerequisites` para verificar que se cumplen los requisitos del sistema.

2. **Descarga del Software**

   Descargue |Fess| desde el `sitio de descargas <https://fess.codelibs.org/ja/downloads.html>`__.

   Para la versión Docker, obtenga el archivo Docker Compose.

3. **Configuración de OpenSearch**

   Para versiones que no sean Docker, debe configurar OpenSearch por separado.

   - Instalación de OpenSearch 3.3.2
   - Instalación de plugins requeridos
   - Edición de archivos de configuración

4. **Configuración de Fess**

   - Instalación de Fess
   - Edición de archivos de configuración (como información de conexión a OpenSearch)

5. **Inicio y Verificación**

   - Inicio del servicio
   - Verificación de funcionamiento accediendo desde el navegador

   Para más detalles, consulte :doc:`run`.

Componentes Necesarios
=======================

Para ejecutar |Fess|, se requieren los siguientes componentes.

Fess Principal
--------------

El cuerpo del sistema de búsqueda de texto completo. Proporciona funciones como interfaz Web, rastreador e indexador.

OpenSearch
----------

Se utiliza OpenSearch como motor de búsqueda.

- **Versión Compatible**: OpenSearch 3.3.2
- **Plugins Requeridos**:

  - opensearch-analysis-fess
  - opensearch-analysis-extension
  - opensearch-minhash
  - opensearch-configsync

.. important::

   Es necesario que coincidan las versiones de OpenSearch y los plugins.
   La falta de coincidencia de versiones causa errores de inicio y comportamiento inesperado.

Java (excepto versión Docker)
------------------------------

Para las versiones TAR.GZ/ZIP/RPM/DEB, se requiere Java 21 o posterior.

- Recomendado: `Eclipse Temurin <https://adoptium.net/temurin>`__
- También se puede usar OpenJDK 21 o posterior

.. note::

   Para la versión Docker, Java está incluido en la imagen Docker, por lo que no es necesario instalarlo por separado.

Próximos Pasos
==============

Verifique los requisitos del sistema y seleccione el método de instalación apropiado.

1. :doc:`prerequisites` - Verificación de requisitos del sistema
2. Selección del método de instalación:

   - :doc:`install-docker` - Instalación con Docker
   - :doc:`install-linux` - Instalación en Linux
   - :doc:`install-windows` - Instalación en Windows

3. :doc:`run` - Inicio de |Fess| y configuración inicial
4. :doc:`security` - Configuración de seguridad (en caso de entorno de producción)

Preguntas Frecuentes
=====================

P: ¿Es OpenSearch obligatorio?
-------------------------------

R: Sí, es obligatorio. |Fess| utiliza OpenSearch como motor de búsqueda.
Para la versión Docker, se configura automáticamente, pero para otros métodos, debe instalarlo manualmente.

P: ¿Se puede actualizar desde versiones anteriores?
----------------------------------------------------

R: Sí, es posible. Para más detalles, consulte :doc:`upgrade`.

P: ¿Se puede configurar con múltiples servidores?
--------------------------------------------------

R: Sí, es posible. Puede ejecutar Fess y OpenSearch en servidores separados.
Además, al configurar OpenSearch en clúster, es posible lograr alta disponibilidad y mejora del rendimiento.

Descargas
=========

|Fess| y los componentes relacionados se pueden descargar desde:

- **Fess**: `Sitio de descargas <https://fess.codelibs.org/ja/downloads.html>`__
- **OpenSearch**: `Download OpenSearch <https://opensearch.org/downloads.html>`__
- **Java (Adoptium)**: `Adoptium <https://adoptium.net/>`__
- **Docker**: `Get Docker <https://docs.docker.com/get-docker/>`__

Información de Versión
=======================

Este documento está dirigido a las siguientes versiones:

- **Fess**: 15.5.0
- **OpenSearch**: 3.3.2
- **Java**: 21 o posterior
- **Docker**: 20.10 o posterior
- **Docker Compose**: 2.0 o posterior

Para documentación de versiones anteriores, consulte la documentación de cada versión.
