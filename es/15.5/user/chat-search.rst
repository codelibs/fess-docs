==========================
Busqueda con chat de IA
==========================

Descripcion general
===================

La funcionalidad de busqueda con chat de IA de |Fess| le permite buscar informacion
en formato de conversacion natural, ademas de la busqueda tradicional por palabras clave.
Al ingresar una pregunta, el asistente de IA analiza los resultados de busqueda
y genera una respuesta facil de entender.

Caracteristicas de la busqueda con chat de IA
=============================================

Busqueda en formato de dialogo
------------------------------

En lugar de pensar en palabras clave, puede hacer preguntas como en una conversacion normal.

Ejemplos:

- "Por favor explicame como instalar Fess"
- "Como hago para crawlear archivos?"
- "Que hacer cuando no se muestran los resultados de busqueda?"

Respuestas con comprension del contexto
---------------------------------------

El asistente de IA entiende la intencion de la pregunta y resume la informacion relacionada en su respuesta.
Extrae la informacion necesaria de multiples resultados de busqueda y la proporciona de forma organizada.

Cita de fuentes
---------------

Las respuestas de la IA indican claramente las fuentes (documentos de referencia).
Si desea verificar la precision de la respuesta, puede consultar directamente el documento original.

Continuacion de la conversacion
-------------------------------

No termina con una sola pregunta; puede continuar la conversacion.
Puede hacer preguntas adicionales basadas en el contexto de las preguntas y respuestas anteriores.

Como usar la busqueda con chat
==============================

Iniciar chat
------------

1. Acceda a la pantalla de busqueda de |Fess|
2. Haga clic en el icono de chat en la esquina inferior derecha
3. Se mostrara el panel de chat

Ingresar una pregunta
---------------------

1. Ingrese una pregunta en el cuadro de texto
2. Haga clic en el boton de enviar o presione la tecla Enter
3. El asistente de IA generara una respuesta

.. note::
   La generacion de la respuesta puede tomar varios segundos.
   Durante el procesamiento, se muestra la fase actual (buscando, analizando, etc.).

Verificar la respuesta
----------------------

Se muestra la respuesta del asistente de IA. La respuesta incluye la siguiente informacion:

- **Cuerpo de la respuesta**: Respuesta detallada a la pregunta
- **Fuentes**: Enlaces a los documentos base de la respuesta (en formato [1], [2], etc.)

Al hacer clic en los enlaces de las fuentes, puede consultar los documentos originales.

Continuar la conversacion
-------------------------

Si tiene preguntas adicionales, puede continuar preguntando:

- "Por favor explicame mas detalladamente"
- "Hay otra manera?"
- "Mas sobre XXX"

El asistente de IA responde considerando el contexto de la conversacion anterior.

Comenzar una nueva conversacion
-------------------------------

Si desea preguntar sobre un tema diferente, haga clic en el boton "Nuevo chat".
Esto borrara el historial de conversacion y podra comenzar una nueva conversacion.

Consejos para hacer preguntas efectivas
=======================================

Hacer preguntas especificas
---------------------------

Las preguntas especificas obtienen respuestas mas apropiadas que las vagas.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Pregunta vaga
     - Pregunta especifica
   * - Como configuro?
     - Como cambio la configuracion de memoria de Fess?
   * - Tengo un error
     - Aparece el error "indice no encontrado" al buscar
   * - Sobre el crawl
     - Como configuro exclusiones al crawlear un sitio web?

Incluir informacion de contexto
-------------------------------

Incluir situacion o proposito ayuda a obtener respuestas mas apropiadas.

Buenos ejemplos:

- "Estoy ejecutando Fess en un entorno Docker. Como cambio la ubicacion de guardado de logs?"
- "Es mi primera vez usando Fess. Que debo hacer primero?"

Hacer preguntas paso a paso
---------------------------

Los problemas complejos se entienden mejor haciendo preguntas paso a paso.

1. "Puedo crawlear archivos compartidos con Fess?"
2. "Explicame como conectar con protocolo SMB"
3. "Que hago si la carpeta compartida requiere autenticacion?"

Preguntas frecuentes
====================

P: No se muestra la funcion de chat
-----------------------------------

R: Es posible que la funcion de chat no este habilitada.
Consulte con el administrador del sistema si la funcion de chat RAG esta habilitada.

P: Toma tiempo mostrar la respuesta
------------------------------------

R: Como la IA analiza los resultados de busqueda y genera la respuesta, puede tomar de varios segundos a decenas de segundos.
Durante el procesamiento, se muestra la fase actual ("Buscando", "Analizando", "Generando respuesta", etc.).

P: La fuente de la respuesta parece incorrecta
----------------------------------------------

R: Por favor haga clic en el enlace de la fuente y verifique el documento original.
Aunque la IA genera respuestas basadas en resultados de busqueda, puede haber errores de interpretacion.
Para informacion importante, recomendamos siempre verificar el documento original.

P: Parece que olvido la conversacion anterior
---------------------------------------------

R: Es posible que la sesion haya expirado.
Si no hay operaciones durante cierto tiempo, el historial de conversacion se borra.
Por favor inicie una nueva conversacion.

P: No obtengo respuesta para ciertas preguntas
----------------------------------------------

R: Las posibles causas son:

- No hay informacion relacionada en los documentos de busqueda
- La pregunta es ambigua y no se puede buscar apropiadamente
- Se ha alcanzado el limite de tasa

Intente reformular la pregunta o espere un momento antes de intentar de nuevo.

P: Puedo hacer preguntas en idiomas distintos al espanol?
---------------------------------------------------------

R: Si, dependiendo de la configuracion, en muchos casos puede hacer preguntas en ingles u otros idiomas.
La IA reconoce el idioma de la pregunta e intenta responder en el mismo idioma.

Notas
=====

Sobre las respuestas de la IA
-----------------------------

- Las respuestas de la IA se generan basadas en los resultados de busqueda
- La precision de las respuestas no esta garantizada
- Para decisiones importantes, asegurese de verificar el documento original
- Para la informacion mas reciente, confirme en la documentacion oficial

Sobre privacidad
----------------

- Las preguntas ingresadas se usan para busqueda y procesamiento de IA
- El historial de conversacion se elimina despues de terminar la sesion
- Dependiendo de la configuracion del sistema, los logs pueden registrarse

Informacion de referencia
=========================

- :doc:`search-and` - Como usar busqueda AND
- :doc:`search-not` - Como usar busqueda NOT
- :doc:`search-field` - Como usar busqueda por campo
- :doc:`advanced-search` - Funciones de busqueda avanzada
