============================================================
Parte 18: Fundamentos de la busqueda con IA -- Evolucion de la busqueda por palabras clave a la busqueda semantica
============================================================

Introduccion
=============

En los articulos anteriores, nos hemos centrado en la busqueda de texto completo basada en palabras clave.
La busqueda de texto completo es muy eficaz cuando los usuarios pueden introducir las palabras clave adecuadas.
Sin embargo, hay casos en los que la busqueda por palabras clave por si sola no puede responder adecuadamente a necesidades como "no se que palabras clave usar para buscar" o "quiero respuestas a preguntas conceptuales".

En este articulo, organizamos el espectro de las tecnologias de busqueda y explicamos como evoluciona la busqueda desde la busqueda por palabras clave hasta la busqueda semantica.

Audiencia objetivo
===================

- Personas interesadas en la busqueda con IA que desean organizar los conceptos
- Personas que estan considerando la introduccion de la busqueda semantica
- Personas que desean comprender las funciones relacionadas con la IA de Fess

Espectro de las tecnologias de busqueda
=========================================

Las tecnologias de busqueda forman un espectro que va de lo simple a lo avanzado, como se muestra a continuacion.

.. list-table:: Espectro de las tecnologias de busqueda
   :header-rows: 1
   :widths: 20 35 45

   * - Tecnologia
     - Mecanismo
     - Caracteristicas
   * - Busqueda por palabras clave
     - Compara los terminos de entrada con los terminos en los documentos
     - Rapida y fiable. Requiere coincidencia exacta de terminos
   * - Busqueda difusa
     - Tambien compara terminos con ortografia similar
     - Manejo de errores tipograficos
   * - Busqueda por sinonimos
     - Expande sinonimos para la comparacion
     - Manejo de variaciones de notacion (configuracion manual)
   * - Busqueda semantica
     - Compara basandose en la similitud semantica
     - Encuentra documentos relacionados incluso sin coincidencia de terminos
   * - Busqueda hibrida
     - Combinacion de busqueda por palabras clave + semantica
     - Aprovecha las fortalezas de ambos enfoques

Limitaciones de la busqueda por palabras clave
================================================

La busqueda por palabras clave es eficaz en muchas situaciones, pero muestra sus limitaciones en los siguientes casos.

Discrepancia de vocabulario
-----------------------------

Esto ocurre cuando las palabras utilizadas por los usuarios difieren de las palabras utilizadas en los documentos.

Ejemplo: Incluso si un usuario busca "quiero cambiar el destino de la transferencia de mi salario", si el documento interno utiliza el termino "procedimiento de cambio de cuenta salarial", es posible que las palabras clave no coincidan.

Esto se puede abordar parcialmente con sinonimos (vease la Parte 8), pero no es practico registrar todas las combinaciones de vocabulario posibles de antemano.

Busqueda conceptual
---------------------

Este es el caso en el que los usuarios desean buscar por concepto en lugar de por palabras clave especificas, como "reglas internas sobre el trabajo remoto".
En este caso, diversos documentos relacionados pueden ser relevantes, incluyendo los que tratan sobre "trabajo desde casa", "teletrabajo", "reglas de asistencia a la oficina" y "gestion de horarios".

Como funciona la busqueda semantica
======================================

Representacion vectorial (Embedding)
--------------------------------------

La base de la busqueda semantica es la conversion de texto en "vectores (matrices de numeros)".
Estos vectores son representaciones matematicas del "significado" del texto.

Los textos con significados similares se colocan cerca unos de otros en el espacio vectorial.
Por ejemplo, los vectores de "perro" y "mascota" estan cerca, mientras que los vectores de "perro" y "automovil" estan lejos.

Funcionamiento de la busqueda
-------------------------------

1. El usuario introduce una consulta de busqueda
2. La consulta se convierte en un vector
3. Se calcula la similitud con los vectores de documentos en el indice
4. Los documentos se devuelven en orden de mayor similitud

Esto permite encontrar documentos semanticamente relacionados incluso cuando las palabras clave no coinciden exactamente.

Busqueda semantica en Fess
============================

Fess puede lograr una busqueda basada en vectores a traves de plugins de busqueda semantica.

Activacion de la busqueda semantica
--------------------------------------

1. Instalar el plugin de busqueda semantica
2. Configurar el modelo de embedding
3. Reconstruir el indice (vectorizar los documentos existentes)

Eleccion del modelo de embedding
-----------------------------------

Seleccione un modelo (modelo de embedding) para convertir texto en vectores.

Los criterios de seleccion son los siguientes:

- **Soporte de idiomas**: Si puede manejar adecuadamente el idioma objetivo
- **Precision**: Calidad de los vectores (precision en la captura del significado)
- **Velocidad**: Tiempo requerido para la conversion
- **Coste**: Tarifas de uso de API, requisitos de hardware

Busqueda hibrida: Rank Fusion
================================

La busqueda semantica es potente, pero no omnipotente.
Para buscar nombres propios o en casos que requieren coincidencia exacta, la busqueda por palabras clave es mas apropiada.

El concepto de busqueda hibrida
---------------------------------

La busqueda hibrida ejecuta tanto la busqueda por palabras clave como la busqueda semantica, y luego integra los resultados.

Fess utiliza Rank Fusion para fusionar los resultados de diferentes metodos de busqueda.
En concreto, el algoritmo RRF (Reciprocal Rank Fusion) asegura que los documentos que ocupan posiciones altas en ambos resultados de busqueda se clasifiquen finalmente en las primeras posiciones.

Ventajas de la busqueda hibrida
---------------------------------

- Combina la "fiabilidad" de la busqueda por palabras clave con la "flexibilidad" de la busqueda semantica
- Los nombres propios se cubren con la busqueda por palabras clave
- Las busquedas conceptuales se cubren con la busqueda semantica
- La calidad general de la busqueda mejora en comparacion con el uso exclusivo de uno de los dos metodos

Criterios para la adopcion
============================

La busqueda semantica no debe introducirse necesariamente en todos los entornos.

Casos en los que se debe considerar la adopcion
--------------------------------------------------

- Hay muchas "consultas sin resultados" en los registros de busqueda
- Los usuarios informan que "no conocen las palabras clave adecuadas"
- Se desea soportar preguntas en lenguaje natural (un prerrequisito para RAG en la Parte 19)
- Se desea mejorar la busqueda entre idiomas para documentos multilingues

Casos en los que aun no es necesaria
---------------------------------------

- Se obtiene una calidad de busqueda suficiente con busqueda por palabras clave + sinonimos
- El numero de documentos es reducido y los usuarios conocen las palabras clave apropiadas
- Los recursos de computo (GPU o costes de API en la nube) son limitados

Adopcion gradual
------------------

1. Primero, mejorar la calidad con busqueda por palabras clave + sinonimos (Parte 8)
2. Si las consultas sin resultados siguen siendo frecuentes, considerar la busqueda semantica
3. Utilizar la busqueda hibrida para beneficiarse de ambos enfoques

Resumen
========

En este articulo, hemos organizado el camino de evolucion desde la busqueda por palabras clave hasta la busqueda semantica.

- El espectro de las tecnologias de busqueda (palabras clave -> difusa -> sinonimos -> semantica -> hibrida)
- Como funciona la busqueda semantica (representacion vectorial y calculo de similitud)
- Busqueda semantica y busqueda hibrida en Fess (Rank Fusion)
- Criterios para la adopcion y un enfoque gradual

En el proximo articulo, desarrollaremos aun mas la busqueda semantica y construiremos un asistente de IA utilizando RAG.

Referencias
============

- `Funciones de busqueda con IA de Fess <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `Busqueda vectorial de OpenSearch <https://opensearch.org/docs/latest/search-plugins/knn/>`__
