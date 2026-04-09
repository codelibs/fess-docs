============================================================
Parte 21: Busqueda cruzada de imagenes y texto -- Gestion del conocimiento de nueva generacion con busqueda multimodal
============================================================

Introduccion
=============

En los articulos anteriores, nos hemos centrado principalmente en la busqueda de documentos basados en texto.
Sin embargo, el conocimiento empresarial incluye una gran cantidad de contenido mas alla del texto.
Fotos de productos, planos de diseno, imagenes de diapositivas de presentaciones, fotos de pizarras: si estas "imagenes" tambien pudieran buscarse, las posibilidades de aprovechamiento del conocimiento se ampliarian significativamente.

En este articulo, presentamos como construir un entorno de busqueda multimodal que permite la busqueda cruzada de texto e imagenes.

Publico objetivo
=================

- Personas que enfrentan desafios en la busqueda de documentos que contienen imagenes
- Personas interesadas en aplicaciones de la busqueda vectorial
- Personas que desean comprender el concepto de IA multimodal

Que es la busqueda multimodal?
================================

La busqueda multimodal es una tecnologia que permite la busqueda cruzada entre diferentes tipos de datos (texto, imagenes, audio, etc.).

Por ejemplo, al buscar con el texto "diseno de un coche deportivo rojo", se muestran en los resultados imagenes que coinciden conceptualmente.
Es un mecanismo que permite buscar imagenes a partir de texto, o texto a partir de imagenes.

Modelo CLIP
-----------

La base de la busqueda multimodal son modelos como CLIP (Contrastive Language-Image Pre-Training).
CLIP convierte texto e imagenes en el mismo espacio vectorial, lo que permite calcular la similitud entre texto e imagenes.

Busqueda multimodal en Fess
=============================

Fess puede lograr la busqueda cruzada de texto e imagenes a traves de su plugin de busqueda multimodal.

Componentes
------------

Los componentes de la busqueda multimodal son los siguientes:

1. **Servidor CLIP**: Convierte texto e imagenes en vectores
2. **OpenSearch**: Busca vectores mediante KNN (K-Nearest Neighbor)
3. **Fess**: Proporciona rastreo, indexacion e interfaz de busqueda

Procedimiento de configuracion
--------------------------------

**1. Preparacion del servidor CLIP**

Prepare un servidor para ejecutar el modelo CLIP.
Se recomienda un entorno con GPU disponible.

Puede agregar un servidor CLIP utilizando Docker Compose.

**2. Instalacion del plugin**

Instale el plugin de busqueda multimodal para Fess.

**3. Configuracion del indice KNN**

Configure los ajustes del indice KNN para realizar busquedas vectoriales en OpenSearch.
Establezca las dimensiones del vector de acuerdo con el modelo CLIP que este utilizando.

**4. Configuracion de rastreo**

Configure directorios y sitios web que contengan imagenes como objetivos de rastreo.
Los archivos de imagen (PNG, JPEG, GIF, etc.) tambien se recopilan como objetivos de rastreo.

Experiencia de busqueda
========================

Buscar imagenes con texto
---------------------------

Al buscar con texto como "foto exterior del producto", "pizarra de reunion" o "plano de diseno", se muestran en los resultados imagenes que coinciden conceptualmente.

Se muestran miniaturas en los resultados de busqueda, lo que permite encontrar visualmente las imagenes deseadas.

Resultados mixtos de texto e imagenes
----------------------------------------

En la busqueda multimodal, se devuelven resultados de busqueda que contienen una mezcla de documentos de texto e imagenes.
Se utiliza Rank Fusion (vease la Parte 18) para integrar los resultados de la busqueda de texto y la busqueda de imagenes.

Casos de uso
=============

Manufactura: Busqueda de imagenes de piezas y productos
---------------------------------------------------------

En la manufactura, se gestionan enormes cantidades de fotos de piezas e imagenes de productos.
Al buscar con texto como "pieza metalica redonda" o al buscar piezas similares a partir de la foto de una pieza especifica, se pueden aprovechar los activos de diseno anteriores.

Equipos de diseno: Gestion de activos de diseno
--------------------------------------------------

Los equipos de diseno gestionan grandes volumenes de activos visuales como logotipos, iconos, material fotografico y maquetas.
Como se puede buscar con lenguaje natural como "fondo con degradado azul", el descubrimiento de activos se facilita.

Investigacion y desarrollo: Busqueda de datos experimentales
---------------------------------------------------------------

Los departamentos de I+D gestionan graficos de resultados experimentales, fotografias de microscopio e imagenes de datos de medicion.
Al hacer que estas imagenes sean buscables, se facilita la consulta de datos experimentales anteriores.

Consideraciones para la implementacion
=========================================

Requisitos de hardware
-----------------------

La busqueda multimodal requiere recursos computacionales para ejecutar el modelo CLIP.

- **Recomendado**: Servidor con GPU (NVIDIA GPU)
- **Minimo**: Puede funcionar con CPU, pero la velocidad de indexacion se reduce

El tiempo de indexacion depende de la velocidad de procesamiento del modelo, por lo que se recomienda encarecidamente un entorno con GPU al indexar una gran cantidad de imagenes.

Formatos de imagen compatibles
---------------------------------

Se admiten los formatos de imagen comunes (JPEG, PNG, GIF, BMP, TIFF, etc.).
La compatibilidad con imagenes dentro de PDF e imagenes incrustadas en documentos de oficina depende de la configuracion de rastreo.

Implementacion gradual
------------------------

La busqueda multimodal puede implementarse como una adicion a un entorno de busqueda de texto existente.

1. Primero, realice una implementacion de prueba en directorios y sitios con muchas imagenes
2. Verifique la calidad de busqueda y el uso
3. Amplie el alcance gradualmente

Resumen
========

En este articulo, presentamos la busqueda cruzada de imagenes y texto mediante busqueda multimodal.

- El concepto de busqueda multimodal (espacio vectorial unificado para texto e imagenes mediante CLIP)
- Componentes y configuracion de la busqueda multimodal en Fess
- La experiencia de buscar imagenes con texto y buscar imagenes similares con imagenes
- Casos de uso en manufactura, diseno e investigacion y desarrollo
- Requisitos de GPU y un enfoque de implementacion gradual

En el proximo articulo, abordaremos la visualizacion del conocimiento organizacional a traves del analisis de datos de busqueda.

Referencias
============

- `OpenSearch KNN Search <https://opensearch.org/docs/latest/search-plugins/knn/>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
