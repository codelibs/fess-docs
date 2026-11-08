==============================================
Parte 21: Búsqueda cruzada de imágenes y texto
==============================================

Introducción
=============

En los artículos anteriores, nos hemos centrado principalmente en la búsqueda de documentos basados en texto.
Sin embargo, el conocimiento empresarial incluye una gran cantidad de contenido más allá del texto.
Fotos de productos, planos de diseño, imágenes de diapositivas de presentaciones, fotos de pizarras: si estas "imágenes" también pudieran buscarse, las posibilidades de aprovechamiento del conocimiento se ampliarían significativamente.

En este artículo, presentamos cómo construir un entorno de búsqueda multimodal que permite la búsqueda cruzada de texto e imágenes.

Público objetivo
=================

- Personas que enfrentan desafíos en la búsqueda de documentos que contienen imágenes
- Personas interesadas en aplicaciones de la búsqueda vectorial
- Personas que desean comprender el concepto de IA multimodal

¿Qué es la búsqueda multimodal?
================================

La búsqueda multimodal es una tecnología que permite la búsqueda cruzada entre diferentes tipos de datos (texto, imágenes, audio, etc.).

Por ejemplo, al buscar con el texto "diseño de un coche deportivo rojo", se muestran en los resultados imágenes que coinciden conceptualmente.
Es un mecanismo que permite buscar imágenes a partir de texto, o texto a partir de imágenes.

Modelo CLIP
-----------

La base de la búsqueda multimodal son modelos como CLIP (Contrastive Language-Image Pre-Training).
CLIP convierte texto e imágenes en el mismo espacio vectorial, lo que permite calcular la similitud entre texto e imágenes.

Búsqueda multimodal en Fess
=============================

Fess puede lograr la búsqueda cruzada de texto e imágenes a través de su plugin de búsqueda multimodal.

Componentes
------------

Los componentes de la búsqueda multimodal son los siguientes:

1. **Servidor CLIP**: Convierte texto e imágenes en vectores
2. **OpenSearch**: Busca vectores mediante KNN (K-Nearest Neighbor)
3. **Fess**: Proporciona rastreo, indexación e interfaz de búsqueda

Procedimiento de configuración
--------------------------------

**1. Preparación del servidor CLIP**

Prepare un servidor para ejecutar el modelo CLIP.
Se recomienda un entorno con GPU disponible.

Puede agregar un servidor CLIP utilizando Docker Compose.

**2. Instalación del plugin**

Instale el plugin de búsqueda multimodal para Fess.

**3. Configuración del índice KNN**

Configure los ajustes del índice KNN para realizar búsquedas vectoriales en OpenSearch.
Establezca las dimensiones del vector de acuerdo con el modelo CLIP que esté utilizando.

**4. Configuración de rastreo**

Configure directorios y sitios web que contengan imágenes como objetivos de rastreo.
Los archivos de imagen (PNG, JPEG, GIF, etc.) también se recopilan como objetivos de rastreo.

Experiencia de búsqueda
========================

Buscar imágenes con texto
---------------------------

Al buscar con texto como "foto exterior del producto", "pizarra de reunión" o "plano de diseño", se muestran en los resultados imágenes que coinciden conceptualmente.

Se muestran miniaturas en los resultados de búsqueda, lo que permite encontrar visualmente las imágenes deseadas.

Resultados mixtos de texto e imágenes
----------------------------------------

En la búsqueda multimodal, se devuelven resultados de búsqueda que contienen una mezcla de documentos de texto e imágenes.
Se utiliza Rank Fusion (véase la Parte 18) para integrar los resultados de la búsqueda de texto y la búsqueda de imágenes.

Casos de uso
=============

Manufactura: Búsqueda de imágenes de piezas y productos
---------------------------------------------------------

En la manufactura, se gestionan enormes cantidades de fotos de piezas e imágenes de productos.
Al buscar con texto como "pieza metálica redonda" o al buscar piezas similares a partir de la foto de una pieza específica, se pueden aprovechar los activos de diseño anteriores.

Equipos de diseño: Gestión de activos de diseño
--------------------------------------------------

Los equipos de diseño gestionan grandes volúmenes de activos visuales como logotipos, iconos, material fotográfico y maquetas.
Como se puede buscar con lenguaje natural como "fondo con degradado azul", el descubrimiento de activos se facilita.

Investigación y desarrollo: Búsqueda de datos experimentales
---------------------------------------------------------------

Los departamentos de I+D gestionan gráficos de resultados experimentales, fotografías de microscopio e imágenes de datos de medición.
Al hacer que estas imágenes sean buscables, se facilita la consulta de datos experimentales anteriores.

Consideraciones para la implementación
=========================================

Requisitos de hardware
-----------------------

La búsqueda multimodal requiere recursos computacionales para ejecutar el modelo CLIP.

- **Recomendado**: Servidor con GPU (NVIDIA GPU)
- **Mínimo**: Puede funcionar con CPU, pero la velocidad de indexación se reduce

El tiempo de indexación depende de la velocidad de procesamiento del modelo, por lo que se recomienda encarecidamente un entorno con GPU al indexar una gran cantidad de imágenes.

Formatos de imagen compatibles
---------------------------------

Se admiten los formatos de imagen comunes (JPEG, PNG, GIF, BMP, TIFF, etc.).
La compatibilidad con imágenes dentro de PDF e imágenes incrustadas en documentos de oficina depende de la configuración de rastreo.

Implementación gradual
------------------------

La búsqueda multimodal puede implementarse como una adición a un entorno de búsqueda de texto existente.

1. Primero, realice una implementación de prueba en directorios y sitios con muchas imágenes
2. Verifique la calidad de búsqueda y el uso
3. Amplíe el alcance gradualmente

Resumen
========

En este artículo, presentamos la búsqueda cruzada de imágenes y texto mediante búsqueda multimodal.

- El concepto de búsqueda multimodal (espacio vectorial unificado para texto e imágenes mediante CLIP)
- Componentes y configuración de la búsqueda multimodal en Fess
- La experiencia de buscar imágenes con texto y buscar imágenes similares con imágenes
- Casos de uso en manufactura, diseño e investigación y desarrollo
- Requisitos de GPU y un enfoque de implementación gradual

En el próximo artículo, abordaremos la visualización del conocimiento organizacional a través del análisis de datos de búsqueda.

Referencias
============

- `OpenSearch KNN Search <https://opensearch.org/docs/latest/search-plugins/knn/>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
