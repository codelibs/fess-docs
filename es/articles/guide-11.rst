===========================================================================
Parte 11: Ampliar sistemas existentes con la API de busqueda -- Patrones de integracion con CRM y sistemas internos
===========================================================================

Introduccion
=============

Fess no solo puede utilizarse como un sistema de busqueda independiente, sino tambien como un "microservicio de busqueda" que proporciona funcionalidad de busqueda a los sistemas empresariales existentes.

En este articulo se presentan patrones concretos para la integracion con sistemas existentes utilizando la API de Fess.
Se abordan escenarios de integracion practicos como la incorporacion de busqueda de documentos de clientes en un CRM, la creacion de un widget de busqueda de FAQ y la construccion de un portal de documentos.

Audiencia objetivo
==================

- Personas que desean agregar funcionalidad de busqueda a sistemas empresariales existentes
- Personas interesadas en la integracion de sistemas mediante la API de Fess
- Personas con conocimientos basicos de desarrollo de aplicaciones web

Vision general de la API de Fess
=================================

A continuacion se presenta un resumen de las principales APIs proporcionadas por Fess.

.. list-table:: Lista de APIs de Fess
   :header-rows: 1
   :widths: 25 45 30

   * - API
     - Proposito
     - Endpoint
   * - API de busqueda
     - Busqueda de texto completo de documentos
     - ``/api/v1/documents``
   * - API de etiquetas
     - Obtener etiquetas disponibles
     - ``/api/v1/labels``
   * - API de sugerencias
     - Obtener candidatos de autocompletado
     - ``/api/v1/suggest-words``
   * - API de palabras populares
     - Obtener palabras clave de busqueda populares
     - ``/api/v1/popular-words``
   * - API de estado
     - Verificar el estado operativo del sistema
     - ``/api/v1/health``
   * - API de administracion
     - Operaciones de configuracion (CRUD)
     - ``/api/admin/*``

Tokens de acceso
------------------

Al utilizar la API, se recomienda la autenticacion mediante tokens de acceso.

1. Cree un token de acceso en [Sistema] > [Token de acceso] en la consola de administracion
2. Incluya el token en el encabezado de la solicitud de la API

::

    Authorization: Bearer {token_de_acceso}

Se pueden asignar roles a los tokens, y el control de resultados de busqueda basado en roles tambien se aplica a las busquedas realizadas a traves de la API.

Patron 1: Integracion de busqueda en un CRM
=============================================

Escenario
---------

Agregar una funcion de busqueda de documentos relacionados con clientes al sistema CRM utilizado por el equipo de ventas.
Permitir la busqueda transversal de propuestas, actas de reuniones, contratos y mas desde la pantalla de clientes del CRM.

Enfoque de implementacion
--------------------------

Incorporar un widget de busqueda en la pantalla de clientes del CRM.
Enviar el nombre del cliente como consulta de busqueda a la API de Fess y mostrar los resultados dentro de la pantalla del CRM.

.. code-block:: javascript

    // Widget de busqueda dentro de la pantalla del CRM
    async function searchCustomerDocs(customerName) {
      const params = new URLSearchParams({
        q: customerName,
        num: '5',
        'fields.label': 'sales-docs'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

Puntos clave
-------------

- Utilice ``fields.label`` para limitar los resultados a documentos relacionados con ventas
- Utilice ``num`` para limitar el numero de resultados mostrados (ajustado al espacio disponible en la pantalla del CRM)
- Es util permitir la busqueda no solo por nombre de cliente, sino tambien por nombre de proyecto o numero de proyecto

Patron 2: Widget de busqueda de FAQ
=====================================

Escenario
---------

Agregar un widget de busqueda de FAQ al sistema interno de gestion de consultas.
Antes de que los empleados envien una consulta, fomentar la autoresolucion buscando FAQ relacionadas.

Enfoque de implementacion
--------------------------

Combinar la API de sugerencias y la API de busqueda para mostrar candidatos en tiempo real durante la entrada de texto.

.. code-block:: javascript

    // Sugerencias durante la entrada de texto
    async function getSuggestions(query) {
      const params = new URLSearchParams({ q: query, num: '5' });
      const url = `https://fess.example.com/api/v1/suggest-words?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

La API de sugerencias se utiliza para mostrar candidatos mientras el usuario escribe palabras clave.
Cuando el usuario confirma una palabra clave y ejecuta la busqueda, la API de busqueda obtiene resultados de busqueda detallados.

Puntos clave
-------------

- Dado que la capacidad de respuesta en tiempo real es critica para la API de sugerencias, verifique la velocidad de respuesta
- Gestione las categorias de FAQ con etiquetas y proporcione filtrado por categorias
- Muestre "palabras clave buscadas frecuentemente" mediante la API de palabras populares para ayudar a los usuarios en la busqueda

Patron 3: Portal de documentos
================================

Escenario
---------

Construir un portal interno de gestion de documentos.
Proporcionar una interfaz que combine la navegacion por categorias con la busqueda de texto completo.

Enfoque de implementacion
--------------------------

Utilizar la API de etiquetas para obtener la lista de categorias y la API de busqueda para obtener documentos dentro de cada categoria.

.. code-block:: javascript

    // Obtener lista de etiquetas
    async function getLabels() {
      const url = 'https://fess.example.com/api/v1/labels';
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

    // Busqueda filtrada por etiqueta
    async function searchByLabel(query, label) {
      const params = new URLSearchParams({
        q: query || '*',
        'fields.label': label,
        num: '20',
        sort: 'last_modified.desc'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

Puntos clave
-------------

- La API de etiquetas obtiene la lista de categorias de forma dinamica (las adiciones y eliminaciones de etiquetas se reflejan inmediatamente en el lado de la API)
- Utilice ``sort=last_modified.desc`` para mostrar los documentos mas recientes en la parte superior
- La navegacion sin palabras clave (obtencion de todos los elementos) tambien es posible con ``q=*``

Patron 4: API de indexacion de contenido
==========================================

Escenario
---------

Registrar datos generados por sistemas externos (registros, informes, registros de respuestas de chatbots, etc.) en el indice de Fess para hacerlos buscables.

Enfoque de implementacion
--------------------------

Mediante la API de administracion de Fess, es posible registrar documentos en el indice desde fuentes externas.

Utilice el endpoint de documentos de la API de administracion para enviar informacion como el titulo, la URL y el texto del cuerpo mediante una solicitud POST.

Puntos clave
-------------

- Eficaz para integrar fuentes de datos que no se pueden obtener mediante el rastreo
- El procesamiento por lotes tambien se puede utilizar para registrar multiples documentos a la vez
- Establezca los permisos del token de acceso de forma adecuada y restrinja los permisos de escritura

Mejores practicas para la integracion de API
==============================================

Manejo de errores
------------------

En la integracion de API, es importante el manejo de errores que tenga en cuenta las fallas de red y el mantenimiento del servidor Fess.

- Configuracion de timeout: Establezca timeouts apropiados para las llamadas a la API de busqueda
- Logica de reintentos: Implemente reintentos para errores transitorios (aproximadamente 3 reintentos como maximo)
- Respaldo: Proporcione una visualizacion alternativa cuando Fess no responda (por ejemplo, "El servicio de busqueda no esta disponible actualmente")

Consideraciones de rendimiento
-------------------------------

- Cache de respuestas: Almacene en cache los resultados de la misma consulta durante un periodo breve
- Limitacion del numero de resultados: Obtenga solo el numero necesario de resultados (parametro ``num``)
- Especificacion de campos: Obtenga solo los campos necesarios para reducir el tamano de la respuesta

Seguridad
----------

- Uso de comunicacion HTTPS
- Rotacion de tokens de acceso
- Establecer los permisos del token al minimo necesario (por ejemplo, solo lectura)
- Configurar CORS de forma adecuada

Resumen
========

En este articulo se presentaron patrones de integracion con sistemas existentes utilizando la API de Fess.

- **Integracion CRM**: Busqueda de documentos relacionados desde la pantalla de clientes
- **Widget de FAQ**: Visualizacion de candidatos en tiempo real con sugerencias + busqueda
- **Portal de documentos**: Navegacion por categorias mediante la API de etiquetas
- **Indexacion de contenido**: Registro de datos externos a traves de la API

La API de Fess esta basada en REST y es simple, lo que facilita la integracion con diversos sistemas.
La capacidad de agregar funcionalidad de busqueda a los sistemas existentes como una adicion posterior es una de las mayores fortalezas de Fess.

En el proximo articulo, se abordaran escenarios para hacer que los datos de SaaS y bases de datos sean buscables.

Referencias
============

- `API de busqueda de Fess <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__

- `API de administracion de Fess <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__
