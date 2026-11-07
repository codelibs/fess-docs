===============================================
Parte 1 Por que las empresas necesitan búsqueda
===============================================

Introducción
============

"Aquel archivo, ¿dónde estaba?"

Es una pregunta a la que muchos profesionales se enfrentan a diario.
Servidores de archivos internos, almacenamiento en la nube, herramientas de chat, wikis, sistemas de gestión de tickets: la información crece día a día y se encuentra dispersa en todo tipo de ubicaciones.
Sabemos que la información que necesitamos existe en algún lugar, pero encontrarla puede llevar varios minutos, a veces incluso decenas de minutos.
Este "tiempo dedicado a buscar información" es precisamente uno de los grandes desafíos que enfrentan las empresas modernas.

En esta serie, "Estrategia de aprovechamiento del conocimiento con Fess", explicaremos de forma práctica cómo resolver este desafío utilizando Fess, un servidor de búsqueda de texto completo de código abierto.
En este artículo, correspondiente a la Parte 1, comenzaremos por organizar "por qué las empresas necesitan una plataforma de búsqueda" y presentaremos que tipo de software es Fess.

Público objetivo
================

- Personas que sienten que la utilización de la información interna es un desafío
- Personas que están evaluando la implementación de una solución de búsqueda empresarial
- Personas que conocen Fess por primera vez

Desafíos de la era de la sobrecarga de información
===================================================

La explosión de información y el problema de "no encontrar"
-----------------------------------------------------------

El volumen de datos digitales que poseen las empresas aumenta año tras año.
Informes, actas de reuniones, documentos de diseño, correos electrónicos, registros de chat, código fuente, datos de clientes: toda esta información constituye el conocimiento de la organización.
Sin embargo, cuanta más información existe, más difícil se vuelve encontrar lo que se necesita.

Numerosos estudios han revelado que los trabajadores del conocimiento dedican entre el 20 y el 30% de su jornada laboral a buscar información.
En una organización de 50 personas, esto equivale a que entre 10 y 15 personas pierdan su tiempo de trabajo diario en "tareas de búsqueda".

El problema estructural de los silos de información
----------------------------------------------------

La razón por la que no se encuentra la información no es simplemente porque haya mucha.
En muchas empresas, la información está fragmentada por departamentos y herramientas, formando lo que se conoce como "silos de información".

- El equipo de ventas utiliza Salesforce y carpetas compartidas
- El equipo de desarrollo utiliza Confluence y repositorios Git
- El departamento de administración general utiliza el portal interno y servidores de archivos

Cada herramienta cuenta con su propia función de búsqueda, pero no existe un medio para buscar de forma transversal entre ellas.
Como resultado, es habitual que no se encuentren "materiales creados por el equipo vecino" y se acaben recreando documentos similares desde cero.

Resolver el problema con una plataforma de búsqueda
----------------------------------------------------

La solución a estos desafíos es la "búsqueda empresarial (plataforma de búsqueda interna corporativa)".
La búsqueda empresarial proporciona un mecanismo que permite buscar de forma transversal en las diversas fuentes de datos de la organización.

Al implementar una solución de búsqueda empresarial, se pueden esperar los siguientes beneficios:

- **Reducción del tiempo de búsqueda de información**: búsqueda unificada de información dispersa en un solo punto
- **Fomento de la reutilización del conocimiento**: facilita el descubrimiento de resultados y conocimientos anteriores
- **Agilización de la toma de decisiones**: acceso rápido a la información necesaria para tomar decisiones
- **Eliminación de la dependencia de personas concretas**: reducción del estado de "solo esa persona lo sabe"

Qué es Fess
===========

Fess es un servidor de búsqueda de texto completo de código abierto.
Se distribuye bajo la licencia Apache y puede utilizarse de forma gratuita, incluyendo el uso comercial.
Está construido sobre Java y utiliza OpenSearch como motor de búsqueda.

Visión general de Fess
----------------------

Fess no es simplemente un motor de búsqueda, sino que incluye un conjunto completo de funciones necesarias como "sistema de búsqueda".

**Rastreador (Crawler)**

Recopila documentos automáticamente de diversas fuentes de datos como sitios web, servidores de archivos, almacenamiento en la nube y servicios SaaS.
Es compatible con más de 100 formatos de archivo, incluyendo HTML, PDF, Word, Excel y PowerPoint.

**Motor de búsqueda**

Utiliza OpenSearch como backend para ofrecer una búsqueda de texto completo de alta velocidad.
Es compatible con más de 20 idiomas, incluido el japonés, y puede escalar para manejar grandes volúmenes de documentos.

**Interfaz de búsqueda**

Incluye de serie una interfaz de búsqueda basada en navegador.
Ofrece una experiencia de búsqueda fácil de usar con resaltado de resultados, facetas (filtros de refinamiento) y sugerencias (autocompletado de entrada).

**Panel de administración**

Permite configurar desde el navegador los ajustes necesarios para la operación, como la configuración de rastreo, la gestión de usuarios y la gestión de diccionarios.
El sistema de búsqueda puede administrarse desde el panel de administración sin necesidad de conocimientos de línea de comandos.

**API**

Proporciona una API de búsqueda basada en JSON, lo que permite integrar la funcionalidad de búsqueda en sistemas existentes.

Por que elegir Fess
-------------------

Existen varias alternativas de búsqueda empresarial.
Es posible utilizar directamente OpenSearch o Elasticsearch, y también existen soluciones de búsqueda comerciales.
A continuación se explican las razones para elegir Fess entre estas opciones.

**Comparación con la construcción propia**

OpenSearch y Elasticsearch son motores de búsqueda potentes, pero por si solos no conforman un sistema de búsqueda completo.
Es necesario construir por cuenta propia muchas funcionalidades, como la implementación del rastreador, el procesamiento de análisis de documentos, el desarrollo de la interfaz de búsqueda y los mecanismos de gestión de permisos.
Fess proporciona todo esto de forma integrada, lo que reduce significativamente el esfuerzo de desarrollo necesario para construir un sistema de búsqueda.

**Comparación con productos comerciales**

Los productos comerciales de búsqueda empresarial son muy funcionales, pero los costos de licencia tienden a ser elevados.
Dado que Fess es de código abierto, no tiene costos de software.
Además, al estar el código fuente disponible públicamente, no existe riesgo de dependencia del proveedor (vendor lock-in).
Si se requieren personalizaciones, se pueden realizar libremente.

**Extensibilidad mediante plugins**

Fess adopta una arquitectura basada en plugins.
Se dispone de plugins para diversas fuentes de datos como Slack, SharePoint, Box, Dropbox, Confluence y Jira, entre otros.
También es posible realizar extensiones adaptadas a la era de la IA, como plugins LLM que permiten la integración con modelos de lenguaje de gran escala.

Escenarios de búsqueda realizables con Fess
============================================

¿Qué tipo de entorno de búsqueda se puede construir concretamente al utilizar Fess?
A continuación se presenta un resumen de los escenarios que se abordarán en esta serie.

Búsqueda transversal de documentos internos
--------------------------------------------

Permite buscar desde un único punto en múltiples fuentes de datos como servidores de archivos, almacenamiento en la nube y sitios web.
Incluso cuando cada departamento utiliza herramientas diferentes, los usuarios pueden acceder a la información que necesitan desde una única barra de búsqueda.

Control de acceso por departamento
----------------------------------

Es posible controlar que documentos se muestran en los resultados de búsqueda según la pertenencia y los permisos del usuario.
Los materiales confidenciales del departamento de recursos humanos no aparecen en los resultados de búsqueda del equipo de ventas.
También es posible integrarse con servicios de directorio existentes (Active Directory, LDAP) para reflejar automáticamente la información de permisos.

Incorporación de funcionalidad de búsqueda en sistemas existentes
-----------------------------------------------------------------

Es posible integrar la funcionalidad de búsqueda de Fess en portales internos y sistemas empresariales.
Se puede elegir entre varios enfoques, como Fess Site Search (FSS) que se integra fácilmente mediante JavaScript, o integraciones personalizadas utilizando la API.

Experiencia de búsqueda potenciada por IA
-----------------------------------------

Es posible implementar RAG (Retrieval-Augmented Generation), una tecnología que ha ganado gran atención en los últimos años, con Fess.
Cuando un usuario hace una pregunta en lenguaje natural, Fess busca información relevante en los documentos internos y un LLM genera la respuesta.
Como "asistente de IA interno", permite llevar el aprovechamiento del conocimiento a un nivel superior.

Estructura de la serie
=======================

Esta serie está compuesta por un total de 23 entregas.
Está diseñada para que tanto principiantes como usuarios avanzados puedan profundizar su comprensión de forma progresiva.

**Parte básica (Partes 1 a 5)**

En las primeras cinco entregas, incluyendo este artículo, se abordan la instalación de Fess y los escenarios básicos.
Se aprenderá sobre el inicio rápido con Docker Compose, la incorporación de funcionalidad de búsqueda en sitios web, la construcción de búsquedas multifuente y el control de búsqueda basado en permisos.

**Parte de soluciones prácticas (Partes 6 a 12)**

Se abordan contenidos prácticos basados en escenarios de negocio reales, como la construcción de un hub de conocimiento para equipos de desarrollo, la búsqueda transversal en almacenamiento en la nube, el ajuste de la calidad de búsqueda, el soporte multiidioma, la gestión operativa y la integración mediante API.

**Parte de arquitectura y escalamiento (Partes 13 a 17)**

Se tratan temas avanzados de arquitectura como el diseño multitenant, el escalamiento para entornos de gran escala, la arquitectura de seguridad, la automatización operativa estilo DevOps y el desarrollo de plugins.

**Parte de IA y búsqueda de próxima generación (Partes 18 a 22)**

Desde los fundamentos de la búsqueda semántica, pasando por la construcción de un asistente de IA mediante RAG, el uso como servidor MCP, la búsqueda multimodal y la analítica de búsqueda, se abordan las tecnologías de búsqueda más recientes.

**Resumen general (Parte 23)**

Se recopilan los conocimientos de toda la serie y se presenta una arquitectura de referencia para una plataforma de conocimiento con Fess como núcleo.

Conclusión
==========

En este artículo se ha presentado la necesidad de una plataforma de búsqueda en las empresas y la posición que ocupa Fess.

- La sobrecarga de información y los silos de información son desafíos comunes a muchas empresas
- La búsqueda empresarial permite buscar de forma transversal en la información dispersa
- Fess es de código abierto y proporciona un conjunto completo de funciones necesarias para un sistema de búsqueda
- También es compatible con la extensibilidad mediante plugins y la integración con IA

En la próxima entrega, presentaremos cómo iniciar Fess utilizando Docker Compose y probar la experiencia de búsqueda en el menor tiempo posible.

Referencias
===========

- `Fess <https://fess.codelibs.org/ja/>`__

- `OpenSearch <https://opensearch.org/>`__

- `GitHub - codelibs/fess <https://github.com/codelibs/fess>`__
