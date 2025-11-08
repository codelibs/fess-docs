====================================
Servidor de Búsqueda de Texto Completo de Código Abierto - Guía de Desarrollo de |Fess|
====================================

Esta guía proporciona la información necesaria para participar en el desarrollo de |Fess|.
Está dirigida a una amplia audiencia, desde aquellos que están abordando el desarrollo de |Fess| por primera vez hasta desarrolladores experimentados.

.. contents:: Índice
   :local:
   :depth: 2

Audiencia Objetivo
========

Esta guía está dirigida a las siguientes personas:

- Desarrolladores que desean contribuir con nuevas funciones o mejoras a |Fess|
- Ingenieros que desean comprender el código de |Fess|
- Personas que desean personalizar y usar |Fess|
- Personas interesadas en participar en proyectos de código abierto

Conocimientos Previos Necesarios
============

Para participar en el desarrollo de |Fess|, los siguientes conocimientos son útiles:

**Obligatorio**

- Conocimientos básicos de programación en Java (Java 21 o posterior)
- Uso básico de Git y GitHub
- Uso básico de Maven

**Recomendado**

- Conocimiento del framework LastaFlute
- Conocimiento de DBFlute
- Conocimiento de OpenSearch/Elasticsearch
- Experiencia en desarrollo de aplicaciones web

Estructura de la Guía de Desarrollo
==============

Esta guía consta de las siguientes secciones.

:doc:`getting-started`
    Explica una visión general del desarrollo de |Fess| y los primeros pasos para comenzar el desarrollo.
    Puede comprender la pila de tecnología necesaria para el desarrollo y la visión general del proyecto.

:doc:`setup`
    Explica en detalle el procedimiento de configuración del entorno de desarrollo.
    Desde la instalación de las herramientas necesarias como Java, IDE, OpenSearch,
    hasta la obtención y ejecución del código fuente de |Fess|, se explica paso a paso.

:doc:`architecture`
    Explica la arquitectura y la estructura del código de |Fess|.
    Al comprender los paquetes principales, módulos y patrones de diseño,
    puede proceder con el desarrollo de manera eficiente.

:doc:`workflow`
    Explica el flujo de trabajo estándar del desarrollo de |Fess|.
    Puede aprender cómo proceder con el trabajo de desarrollo, como agregar funciones, corregir errores, revisión de código y pruebas.

:doc:`building`
    Explica cómo construir y probar |Fess|.
    Explica el uso de herramientas de construcción, la ejecución de pruebas unitarias,
    y cómo crear paquetes de distribución.

:doc:`contributing`
    Explica cómo contribuir al proyecto |Fess|.
    Puede aprender sobre la creación de pull requests, convenciones de codificación,
    y métodos de comunicación con la comunidad.

Inicio Rápido
==============

Si desea comenzar a desarrollar |Fess| de inmediato, siga estos pasos:

1. **Verificación de Requisitos del Sistema**

   Para el desarrollo, se necesitan las siguientes herramientas:

   - Java 21 o posterior
   - Maven 3.x o posterior
   - Git
   - IDE (Eclipse, IntelliJ IDEA, etc.)

2. **Obtención del Código Fuente**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

3. **Descarga de Plugins de OpenSearch**

   .. code-block:: bash

       mvn antrun:run

4. **Ejecución**

   Ejecute ``org.codelibs.fess.FessBoot`` desde el IDE,
   o ejecútelo desde Maven:

   .. code-block:: bash

       mvn compile exec:java

Consulte :doc:`setup` para más detalles.

Opciones de Entorno de Desarrollo
==============

El desarrollo de |Fess| se puede realizar en cualquiera de los siguientes entornos:

Entorno de Desarrollo Local
--------------

Este es el entorno de desarrollo más común. Instale las herramientas de desarrollo en su propia máquina,
y desarrolle usando un IDE.

**Ventajas:**

- Construcción y ejecución rápidas
- Puede aprovechar al máximo las funciones del IDE
- Puede trabajar sin conexión

**Desventajas:**

- La configuración inicial lleva tiempo
- Pueden ocurrir problemas debido a diferencias en el entorno

Entorno de Desarrollo con Docker
------------------------

Puede construir un entorno de desarrollo consistente usando contenedores Docker.

**Ventajas:**

- Se mantiene la consistencia del entorno
- Configuración fácil
- Fácil de volver a un estado limpio

**Desventajas:**

- Se requiere conocimiento de Docker
- El rendimiento puede disminuir en algunos casos

Consulte :doc:`setup` para más detalles.

Preguntas Frecuentes
==========

P: ¿Cuáles son las especificaciones mínimas necesarias para el desarrollo?
--------------------------------

R: Se recomienda lo siguiente:

- CPU: 4 núcleos o más
- Memoria: 8GB o más
- Disco: 20GB o más de espacio libre

P: ¿Qué IDE debo usar?
---------------------------------

R: Puede usar su IDE favorito, como Eclipse, IntelliJ IDEA, VS Code, etc.
Esta guía explica principalmente usando Eclipse como ejemplo,
pero puede desarrollar de manera similar con otros IDEs.

P: ¿Es obligatorio el conocimiento de LastaFlute o DBFlute?
------------------------------------------

R: No es obligatorio, pero facilita el desarrollo si lo tiene.
Aunque esta guía también explica el uso básico,
consulte la documentación oficial de cada framework para más detalles.

P: ¿Por dónde debo empezar mi primera contribución?
------------------------------------------------------

R: Se recomienda comenzar con trabajos relativamente fáciles como:

- Mejora de la documentación
- Adición de pruebas
- Corrección de errores
- Pequeñas mejoras a las funciones existentes

Consulte :doc:`contributing` para más detalles.

Recursos Relacionados
==========

Recursos Oficiales
----------

- `Sitio Oficial de Fess <https://fess.codelibs.org/ja/>`__
- `Repositorio de GitHub <https://github.com/codelibs/fess>`__
- `Rastreador de Problemas <https://github.com/codelibs/fess/issues>`__
- `Discusiones <https://github.com/codelibs/fess/discussions>`__

Documentación Técnica
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

Comunidad
----------

- `Foro de la Comunidad de Fess <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__

Próximos Pasos
==========

Para comenzar el desarrollo, se recomienda comenzar leyendo :doc:`getting-started`.

.. toctree::
   :maxdepth: 2
   :caption: Índice:

   getting-started
   setup
   architecture
   workflow
   building
   contributing
