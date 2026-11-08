===========================================
Parte 18: Fundamentos de la búsqueda con IA
===========================================

Introducción
=============

En los artículos anteriores, nos hemos centrado en la búsqueda de texto completo basada en palabras clave.
La búsqueda de texto completo es muy eficaz cuando los usuarios pueden introducir las palabras clave adecuadas.
Sin embargo, hay casos en los que la búsqueda por palabras clave por si sola no puede responder adecuadamente a necesidades como "no sé qué palabras clave usar para buscar" o "quiero respuestas a preguntas conceptuales".

En este artículo, organizamos el espectro de las tecnologías de búsqueda y explicamos cómo evoluciona la búsqueda desde la búsqueda por palabras clave hasta la búsqueda semántica.

Audiencia objetivo
===================

- Personas interesadas en la búsqueda con IA que desean organizar los conceptos
- Personas que están considerando la introducción de la búsqueda semántica
- Personas que desean comprender las funciones relacionadas con la IA de Fess

Espectro de las tecnologías de búsqueda
=========================================

Las tecnologías de búsqueda forman un espectro que va de lo simple a lo avanzado, como se muestra a continuación.

.. list-table:: Espectro de las tecnologías de búsqueda
   :header-rows: 1
   :widths: 20 35 45

   * - Tecnología
     - Mecanismo
     - Características
   * - Búsqueda por palabras clave
     - Compara los términos de entrada con los términos en los documentos
     - Rápida y fiable. Requiere coincidencia exacta de términos
   * - Búsqueda difusa
     - También compara términos con ortografía similar
     - Manejo de errores tipográficos
   * - Búsqueda por sinónimos
     - Expande sinónimos para la comparación
     - Manejo de variaciones de notación (configuración manual)
   * - Búsqueda semántica
     - Compara basándose en la similitud semántica
     - Encuentra documentos relacionados incluso sin coincidencia de términos
   * - Búsqueda híbrida
     - Combinación de búsqueda por palabras clave + semántica
     - Aprovecha las fortalezas de ambos enfoques

Limitaciones de la búsqueda por palabras clave
================================================

La búsqueda por palabras clave es eficaz en muchas situaciones, pero muestra sus limitaciones en los siguientes casos.

Discrepancia de vocabulario
-----------------------------

Esto ocurre cuando las palabras utilizadas por los usuarios difieren de las palabras utilizadas en los documentos.

Ejemplo: Incluso si un usuario busca "quiero cambiar el destino de la transferencia de mi salario", si el documento interno utiliza el término "procedimiento de cambio de cuenta salarial", es posible que las palabras clave no coincidan.

Esto se puede abordar parcialmente con sinónimos (véase la Parte 8), pero no es práctico registrar todas las combinaciones de vocabulario posibles de antemano.

Búsqueda conceptual
---------------------

Este es el caso en el que los usuarios desean buscar por concepto en lugar de por palabras clave específicas, como "reglas internas sobre el trabajo remoto".
En este caso, diversos documentos relacionados pueden ser relevantes, incluyendo los que tratan sobre "trabajo desde casa", "teletrabajo", "reglas de asistencia a la oficina" y "gestión de horarios".

Cómo funciona la búsqueda semántica
======================================

Representación vectorial (Embedding)
--------------------------------------

La base de la búsqueda semántica es la conversión de texto en "vectores (matrices de números)".
Estos vectores son representaciones matemáticas del "significado" del texto.

Los textos con significados similares se colocan cerca unos de otros en el espacio vectorial.
Por ejemplo, los vectores de "perro" y "mascota" están cerca, mientras que los vectores de "perro" y "automóvil" están lejos.

Funcionamiento de la búsqueda
-------------------------------

1. El usuario introduce una consulta de búsqueda
2. La consulta se convierte en un vector
3. Se calcula la similitud con los vectores de documentos en el índice
4. Los documentos se devuelven en orden de mayor similitud

Esto permite encontrar documentos semánticamente relacionados incluso cuando las palabras clave no coinciden exactamente.

Búsqueda semántica en Fess
============================

Fess puede lograr una búsqueda basada en vectores a través de plugins de búsqueda semántica.

Activación de la búsqueda semántica
--------------------------------------

1. Instalar el plugin de búsqueda semántica
2. Configurar el modelo de embedding
3. Reconstruir el índice (vectorizar los documentos existentes)

Elección del modelo de embedding
-----------------------------------

Seleccione un modelo (modelo de embedding) para convertir texto en vectores.

Los criterios de selección son los siguientes:

- **Soporte de idiomas**: Si puede manejar adecuadamente el idioma objetivo
- **Precisión**: Calidad de los vectores (precisión en la captura del significado)
- **Velocidad**: Tiempo requerido para la conversión
- **Coste**: Tarifas de uso de API, requisitos de hardware

Búsqueda híbrida: Rank Fusion
================================

La búsqueda semántica es potente, pero no omnipotente.
Para buscar nombres propios o en casos que requieren coincidencia exacta, la búsqueda por palabras clave es más apropiada.

El concepto de búsqueda híbrida
---------------------------------

La búsqueda híbrida ejecuta tanto la búsqueda por palabras clave como la búsqueda semántica, y luego integra los resultados.

Fess utiliza Rank Fusion para fusionar los resultados de diferentes métodos de búsqueda.
En concreto, el algoritmo RRF (Reciprocal Rank Fusion) asegura que los documentos que ocupan posiciones altas en ambos resultados de búsqueda se clasifiquen finalmente en las primeras posiciones.

Ventajas de la búsqueda híbrida
---------------------------------

- Combina la "fiabilidad" de la búsqueda por palabras clave con la "flexibilidad" de la búsqueda semántica
- Los nombres propios se cubren con la búsqueda por palabras clave
- Las búsquedas conceptuales se cubren con la búsqueda semántica
- La calidad general de la búsqueda mejora en comparación con el uso exclusivo de uno de los dos métodos

Criterios para la adopción
============================

La búsqueda semántica no debe introducirse necesariamente en todos los entornos.

Casos en los que se debe considerar la adopción
--------------------------------------------------

- Hay muchas "consultas sin resultados" en los registros de búsqueda
- Los usuarios informan que "no conocen las palabras clave adecuadas"
- Se desea soportar preguntas en lenguaje natural (un prerrequisito para RAG en la Parte 19)
- Se desea mejorar la búsqueda entre idiomas para documentos multilingües

Casos en los que aún no es necesaria
---------------------------------------

- Se obtiene una calidad de búsqueda suficiente con búsqueda por palabras clave + sinónimos
- El número de documentos es reducido y los usuarios conocen las palabras clave apropiadas
- Los recursos de cómputo (GPU o costes de API en la nube) son limitados

Adopción gradual
------------------

1. Primero, mejorar la calidad con búsqueda por palabras clave + sinónimos (Parte 8)
2. Si las consultas sin resultados siguen siendo frecuentes, considerar la búsqueda semántica
3. Utilizar la búsqueda híbrida para beneficiarse de ambos enfoques

Resumen
========

En este artículo, hemos organizado el camino de evolución desde la búsqueda por palabras clave hasta la búsqueda semántica.

- El espectro de las tecnologías de búsqueda (palabras clave -> difusa -> sinónimos -> semántica -> híbrida)
- Cómo funciona la búsqueda semántica (representación vectorial y cálculo de similitud)
- Búsqueda semántica y búsqueda híbrida en Fess (Rank Fusion)
- Criterios para la adopción y un enfoque gradual

En el próximo artículo, desarrollaremos aun más la búsqueda semántica y construiremos un asistente de IA utilizando RAG.

Referencias
============

- `Funciones de búsqueda con IA de Fess <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `Búsqueda vectorial de OpenSearch <https://opensearch.org/docs/latest/search-plugins/knn/>`__
