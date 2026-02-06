======================================
Fess vs otras soluciones de busqueda
======================================

Introduccion
============

Al seleccionar un sistema de busqueda de texto completo, existen diversas opciones disponibles.
Esta pagina compara Fess con las principales soluciones de busqueda, explicando las caracteristicas y los casos de uso apropiados para cada una.

.. note::

   Esta comparacion se basa en informacion de enero de 2026.
   Para las funciones y cambios mas recientes, consulte la documentacion oficial de cada proyecto.

----

Fess vs OpenSearch/Elasticsearch independiente
================================================

Descripcion general
-------------------

OpenSearch y Elasticsearch son potentes motores de busqueda, pero usarlos de forma independiente requiere desarrollo adicional para crear un "sistema de busqueda" completo.
Fess utiliza OpenSearch/Elasticsearch como su backend y proporciona un sistema de busqueda completo listo para usar.

Comparacion
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Caracteristica
     - Fess
     - OpenSearch/Elasticsearch independiente
   * - Interfaz de busqueda
     - ✅ Incluida
     - ❌ Requiere desarrollo
   * - Interfaz de administracion
     - ✅ Panel de administracion web
     - ❌ Requiere desarrollo o herramientas separadas
   * - Rastreador
     - ✅ Incluido (Web/Archivos/BD)
     - ❌ Requiere desarrollo o herramientas separadas
   * - Tiempo de implementacion
     - Minutos (Docker)
     - Semanas a meses (incluyendo desarrollo)
   * - Personalizacion
     - Media (personalizacion JSP/CSS)
     - Alta (desarrollo completamente personalizado posible)
   * - Costo inicial
     - Bajo
     - Alto (costos de desarrollo)
   * - Costo operativo
     - Bajo a medio
     - Medio a alto
   * - Escalabilidad
     - Alta
     - Alta
   * - Conocimientos requeridos
     - Conocimientos basicos de TI
     - Programacion y experiencia en motores de busqueda

Cuando elegir Fess
------------------

- **Cuando necesita construir un sistema de busqueda rapidamente**
- **Cuando los recursos de desarrollo son limitados**
- **Cuando las funciones de busqueda estandar son suficientes**
- **Cuando el rastreo web y la busqueda de archivos son los principales casos de uso**

Cuando elegir OpenSearch/Elasticsearch independiente
----------------------------------------------------

- **Cuando necesita una experiencia de busqueda completamente personalizada**
- **Cuando integra la busqueda en una aplicacion existente**
- **Cuando se requiere logica de busqueda especial**
- **Cuando su equipo tiene experiencia en motores de busqueda**

.. tip::

   Despues de implementar Fess, tambien puede construir una interfaz de busqueda personalizada utilizando la API.
   Considere comenzar con Fess y personalizar segun sea necesario.

----

Fess vs Apache Solr
====================

Descripcion general
-------------------

Apache Solr es una plataforma de busqueda de codigo abierto basada en Lucene.
Ofrece alta personalizacion, pero requiere mas experiencia para la implementacion y operacion en comparacion con Fess.

Comparacion
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Caracteristica
     - Fess
     - Apache Solr
   * - Interfaz de busqueda
     - ✅ Incluida
     - ❌ Requiere desarrollo
   * - Interfaz de administracion
     - ✅ Interfaz web intuitiva
     - △ Interfaz de administracion tecnica
   * - Rastreador
     - ✅ Incluido
     - ❌ Requiere herramienta separada (Nutch, etc.)
   * - Dificultad de configuracion
     - Baja
     - Media a alta
   * - Documentacion
     - ✅ Completa
     - ✅ Completa
   * - Soporte en la nube
     - ✅ Docker/Kubernetes
     - ✅ SolrCloud
   * - Comunidad
     - Enfocada en Japon
     - Global

Cuando elegir Fess
------------------

- **Cuando el rastreo Web/Archivos es el principal caso de uso**
- **Cuando la gestion por interfaz grafica es importante**
- **Cuando la facilidad de implementacion es una prioridad**

Cuando elegir Solr
------------------

- **Cuando ya tiene experiencia con Solr**
- **Cuando se necesita busqueda distribuida con SolrCloud**
- **Cuando se requieren plugins especificos de Solr**

----

Fess vs Google Site Search / Custom Search
==========================================

Descripcion general
-------------------

Google Site Search (GSS) fue descontinuado en 2018.
El sucesor, Google Custom Search (Programmable Search Engine), tiene limitaciones.
Fess es un objetivo de migracion ideal desde GSS.

Comparacion
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Caracteristica
     - Fess
     - Google Custom Search
   * - Visualizacion de anuncios
     - ✅ Ninguna
     - ❌ Se muestran (nivel gratuito)
   * - Ubicacion de datos
     - ✅ Autogestionado
     - ❌ Servidores de Google
   * - Control de indices
     - ✅ Control total
     - △ Limitado
   * - Personalizacion
     - ✅ Libremente personalizable
     - △ Limitada
   * - Busqueda de contenido interno
     - ✅ Soportada
     - ❌ No soportada
   * - Costo mensual
     - Solo costos de servidor
     - Gratuito (con anuncios) a de pago
   * - Ajuste de relevancia de busqueda
     - ✅ Ajuste detallado posible
     - △ Limitado

Cuando elegir Fess
------------------

- **Cuando no desea mostrar anuncios**
- **Cuando el contenido interno debe ser buscable**
- **Cuando desea control sobre los resultados de busqueda**
- **Cuando desea gestionar los datos usted mismo**

.. tip::

   Con Fess Site Search (FSS), puede implementar busqueda en sitios
   simplemente insertando JavaScript, igual que Google Site Search.

----

Fess vs Productos de busqueda comerciales
==========================================

Descripcion general
-------------------

Comparacion con productos comerciales como Microsoft SharePoint Search, Autonomy y Google Cloud Search.

Comparacion
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Caracteristica
     - Fess
     - Productos comerciales (General)
   * - Costo de licencia
     - ✅ Gratuito (OSS)
     - ❌ Costoso
   * - Dependencia del proveedor
     - ✅ Ninguna
     - ❌ Si
   * - Personalizacion
     - ✅ Codigo fuente disponible
     - △ Limitada
   * - Riqueza de funciones
     - ○ Basica a intermedia
     - ✅ Funciones avanzadas
   * - Soporte
     - △ Comunidad + Comercial
     - ✅ Soporte del proveedor
   * - Funciones de IA/ML
     - △ Sugerencias basicas
     - ✅ Funciones avanzadas de IA
   * - Integracion empresarial
     - ○ Principales sistemas soportados
     - ✅ Amplia integracion

Cuando elegir Fess
------------------

- **Cuando desea minimizar costos**
- **Cuando desea evitar la dependencia del proveedor**
- **Cuando las funciones de busqueda basicas son suficientes**
- **Cuando desea aprovechar el codigo abierto**

Cuando elegir productos comerciales
------------------------------------

- **Cuando se necesitan funciones avanzadas de IA/ML**
- **Cuando se requiere soporte integral del proveedor**
- **Cuando se necesita integracion con ecosistemas comerciales existentes**

.. note::

   La version comercial de Fess, `N2 Search <https://www.n2sm.net/products/n2search.html>`__,
   proporciona funciones empresariales adicionales y soporte.

----

Guia de seleccion
=================

Utilice el siguiente diagrama de flujo para seleccionar la solucion optima:

::

    Tiene suficientes recursos de desarrollo?
          │
    ┌─────┴─────┐
    │           │
   Si          No
    │           │
    ▼           ▼
  Son los requisitos  →  Considere Fess
  especializados?
    │
    ├── Si → OpenSearch/Elasticsearch independiente
    │         o productos comerciales
    │
    └── No → Es suficiente Fess?
              │
              ├── Si → Fess
              │
              └── No → Reevaluar requisitos

Resumen
=======

Fess es una opcion optima como "sistema de busqueda listo para usar" para muchos casos.

**Fortalezas de Fess**:

- Implementacion en minutos
- Construir un sistema de busqueda sin desarrollo
- Codigo abierto y gratuito

**Proximos pasos**:

1. Pruebe Fess con el `Inicio rapido <../quick-start.html>`__
2. Evalue segun sus requisitos
3. Consulte el `Soporte Comercial <../support-services.html>`__ si es necesario
