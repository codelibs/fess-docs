============================================================
Parte 11: Ampliar sistemas existentes con la API de búsqueda
============================================================

Introducción
=============

Fess no solo puede utilizarse como un sistema de búsqueda independiente, sino también como un "microservicio de búsqueda" que proporciona funcionalidad de búsqueda a los sistemas empresariales existentes.

En este artículo se presentan patrones concretos para la integración con sistemas existentes utilizando la API de Fess.
Se abordan escenarios de integración prácticos como la incorporación de búsqueda de documentos de clientes en un CRM, la creación de un widget de búsqueda de FAQ y la construcción de un portal de documentos.

Audiencia objetivo
==================

- Personas que desean agregar funcionalidad de búsqueda a sistemas empresariales existentes
- Personas interesadas en la integración de sistemas mediante la API de Fess
- Personas con conocimientos básicos de desarrollo de aplicaciones web

Visión general de la API de Fess
=================================

A continuación se presenta un resumen de las principales APIs proporcionadas por Fess.

.. list-table:: Lista de APIs de Fess
   :header-rows: 1
   :widths: 25 45 30

   * - API
     - Propósito
     - Endpoint
   * - API de búsqueda
     - Búsqueda de texto completo de documentos
     - ``/api/v1/documents``
   * - API de etiquetas
     - Obtener etiquetas disponibles
     - ``/api/v1/labels``
   * - API de sugerencias
     - Obtener candidatos de autocompletado
     - ``/api/v1/suggest-words``
   * - API de palabras populares
     - Obtener palabras clave de búsqueda populares
     - ``/api/v1/popular-words``
   * - API de estado
     - Verificar el estado operativo del sistema
     - ``/api/v1/health``
   * - API de administración
     - Operaciones de configuración (CRUD)
     - ``/api/admin/*``

Tokens de acceso
------------------

Al utilizar la API, se recomienda la autenticación mediante tokens de acceso.

1. Cree un token de acceso en [Sistema] > [Token de acceso] en la consola de administración
2. Incluya el token en el encabezado de la solicitud de la API

::

    Authorization: Bearer {token_de_acceso}

Se pueden asignar roles a los tokens, y el control de resultados de búsqueda basado en roles también se aplica a las búsquedas realizadas a través de la API.

Patrón 1: Integración de búsqueda en un CRM
=============================================

Escenario
---------

Agregar una función de búsqueda de documentos relacionados con clientes al sistema CRM utilizado por el equipo de ventas.
Permitir la búsqueda transversal de propuestas, actas de reuniones, contratos y más desde la pantalla de clientes del CRM.

Enfoque de implementación
--------------------------

Incorporar un widget de búsqueda en la pantalla de clientes del CRM.
Enviar el nombre del cliente como consulta de búsqueda a la API de Fess y mostrar los resultados dentro de la pantalla del CRM.

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
- Utilice ``num`` para limitar el número de resultados mostrados (ajustado al espacio disponible en la pantalla del CRM)
- Es útil permitir la búsqueda no solo por nombre de cliente, sino también por nombre de proyecto o número de proyecto

Patrón 2: Widget de búsqueda de FAQ
=====================================

Escenario
---------

Agregar un widget de búsqueda de FAQ al sistema interno de gestión de consultas.
Antes de que los empleados envíen una consulta, fomentar la autoresolución buscando FAQ relacionadas.

Enfoque de implementación
--------------------------

Combinar la API de sugerencias y la API de búsqueda para mostrar candidatos en tiempo real durante la entrada de texto.

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
Cuando el usuario confirma una palabra clave y ejecuta la búsqueda, la API de búsqueda obtiene resultados de búsqueda detallados.

Puntos clave
-------------

- Dado que la capacidad de respuesta en tiempo real es crítica para la API de sugerencias, verifique la velocidad de respuesta
- Gestione las categorías de FAQ con etiquetas y proporcione filtrado por categorías
- Muestre "palabras clave buscadas frecuentemente" mediante la API de palabras populares para ayudar a los usuarios en la búsqueda

Patrón 3: Portal de documentos
================================

Escenario
---------

Construir un portal interno de gestión de documentos.
Proporcionar una interfaz que combine la navegación por categorías con la búsqueda de texto completo.

Enfoque de implementación
--------------------------

Utilizar la API de etiquetas para obtener la lista de categorías y la API de búsqueda para obtener documentos dentro de cada categoría.

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

- La API de etiquetas obtiene la lista de categorías de forma dinámica (las adiciones y eliminaciones de etiquetas se reflejan inmediatamente en el lado de la API)
- Utilice ``sort=last_modified.desc`` para mostrar los documentos más recientes en la parte superior
- La navegación sin palabras clave (obtención de todos los elementos) también es posible con ``q=*``

Patrón 4: API de indexación de contenido
==========================================

Escenario
---------

Registrar datos generados por sistemas externos (registros, informes, registros de respuestas de chatbots, etc.) en el índice de Fess para hacerlos buscables.

Enfoque de implementación
--------------------------

Mediante la API de administración de Fess, es posible registrar documentos en el índice desde fuentes externas.

Utilice el endpoint de documentos de la API de administración para enviar información como el título, la URL y el texto del cuerpo mediante una solicitud POST.

Puntos clave
-------------

- Eficaz para integrar fuentes de datos que no se pueden obtener mediante el rastreo
- El procesamiento por lotes también se puede utilizar para registrar múltiples documentos a la vez
- Establezca los permisos del token de acceso de forma adecuada y restrinja los permisos de escritura

Mejores prácticas para la integración de API
==============================================

Manejo de errores
------------------

En la integración de API, es importante el manejo de errores que tenga en cuenta las fallas de red y el mantenimiento del servidor Fess.

- Configuración de timeout: Establezca timeouts apropiados para las llamadas a la API de búsqueda
- Lógica de reintentos: Implemente reintentos para errores transitorios (aproximadamente 3 reintentos como máximo)
- Respaldo: Proporcione una visualización alternativa cuando Fess no responda (por ejemplo, "El servicio de búsqueda no está disponible actualmente")

Consideraciones de rendimiento
-------------------------------

- Caché de respuestas: Almacene en caché los resultados de la misma consulta durante un período breve
- Limitación del número de resultados: Obtenga solo el número necesario de resultados (parámetro ``num``)
- Especificación de campos: Obtenga solo los campos necesarios para reducir el tamaño de la respuesta

Seguridad
----------

- Uso de comunicación HTTPS
- Rotación de tokens de acceso
- Establecer los permisos del token al mínimo necesario (por ejemplo, solo lectura)
- Configurar CORS de forma adecuada

Resumen
========

En este artículo se presentaron patrones de integración con sistemas existentes utilizando la API de Fess.

- **Integración CRM**: Búsqueda de documentos relacionados desde la pantalla de clientes
- **Widget de FAQ**: Visualización de candidatos en tiempo real con sugerencias + búsqueda
- **Portal de documentos**: Navegación por categorías mediante la API de etiquetas
- **Indexación de contenido**: Registro de datos externos a través de la API

La API de Fess está basada en REST y es simple, lo que facilita la integración con diversos sistemas.
La capacidad de agregar funcionalidad de búsqueda a los sistemas existentes como una adición posterior es una de las mayores fortalezas de Fess.

En el próximo artículo, se abordarán escenarios para hacer que los datos de SaaS y bases de datos sean buscables.

Referencias
============

- `API de búsqueda de Fess <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__

- `API de administración de Fess <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__
