=====================================================
Parte 10: Operación estable de un sistema de búsqueda
=====================================================

Introducción
=============

Una vez que ha construido un sistema de búsqueda y lo ha puesto a disposición de los usuarios, se convierte en un sistema que "no se puede detener".
Cuando los usuarios dependen de la búsqueda en su trabajo diario, cualquier tiempo de inactividad se traduce directamente en una interrupción del negocio.

Este artículo proporciona un manual práctico sobre monitorización, copias de seguridad y recuperación ante fallos para mantener Fess funcionando de forma fiable.

Audiencia objetivo
===================

- Administradores que operan Fess en un entorno de producción
- Personas que desean garantizar la operación estable de un sistema de búsqueda
- Personas con conocimientos básicos de operaciones de sistemas

Visión general de la operación
===============================

La operación estable de Fess se basa en los siguientes tres pilares:

1. **Monitorización**: Detectar problemas de forma temprana
2. **Copias de seguridad**: Proteger los datos
3. **Recuperación ante fallos**: Restaurar el servicio rápidamente cuando ocurren problemas

Monitorización
===============

Health Check
--------------

Fess proporciona un endpoint de health check a través de la API REST.

::

    GET http://localhost:8080/api/v1/health

En condiciones normales, devuelve HTTP 200.
Al llamar periódicamente a este endpoint desde una herramienta de monitorización externa (como Nagios, Zabbix o Datadog), puede supervisar el estado operativo de Fess.

Consulta de información del sistema
-------------------------------------

Desde [Información del sistema] en la consola de administración, puede consultar la siguiente información.

**Información de rastreo**

Puede revisar los resultados de la última ejecución de rastreo (número de documentos procesados, número de errores, etc.).
Utilice esta función para verificar que los rastreos se completan correctamente.

**Información del sistema**

Puede consultar las versiones de Fess y OpenSearch, el uso de memoria JVM, el número de documentos en el índice y más.

Métricas a monitorizar
-----------------------

.. list-table:: Métricas de monitorización y umbrales orientativos
   :header-rows: 1
   :widths: 25 35 40

   * - Métrica
     - Método de verificación
     - Condición de alerta
   * - Proceso de Fess
     - Health API
     - Sin respuesta o HTTP 500
   * - Clúster de OpenSearch
     - Clúster Health API
     - Estado yellow / red
   * - Uso del heap JVM
     - Información del sistema
     - Sostenido por encima del 80 %
   * - Uso de disco
     - Comandos del SO
     - Por encima del 85 %
   * - Resultados de rastreo
     - Información de rastreo
     - Aumento repentino de errores, disminución drástica del número procesado
   * - Respuesta de búsqueda
     - Registro de búsqueda
     - Aumento significativo del tiempo de respuesta

Notificación de finalización de rastreo
-----------------------------------------

Fess cuenta con una función que envía notificaciones cuando se detectan registros de error o fallos en el motor de búsqueda.
Al configurar un Webhook para Slack o Google Chat, puede ser informado inmediatamente de cualquier anomalía.

Copias de seguridad
====================

Objetos de copia de seguridad
-------------------------------

Los objetos de copia de seguridad de un entorno Fess se dividen en dos categorías principales.

**1. Datos de configuración**

Incluye la configuración de rastreo, información de usuarios, datos de diccionario y otra información configurada a través de la consola de administración.
Puede obtener una copia de seguridad de los datos de configuración desde [Información del sistema] > [Copia de seguridad] en la consola de administración de Fess.

**2. Datos del índice**

Es el índice de documentos recopilados mediante rastreo.
Utilice la función de snapshots de OpenSearch para realizar la copia de seguridad del índice.

Estrategia de copias de seguridad
-----------------------------------

.. list-table:: Estrategia de copias de seguridad
   :header-rows: 1
   :widths: 20 25 25 30

   * - Objeto
     - Frecuencia
     - Período de retención
     - Método
   * - Datos de configuración
     - Diaria
     - 30 generaciones
     - Función de backup de Fess
   * - Índice
     - Diaria
     - 7 generaciones
     - Snapshot de OpenSearch
   * - Configuración Docker
     - Al modificar
     - Gestionado con Git
     - Control de versiones de compose.yaml

Automatización de la copia de seguridad de configuración
----------------------------------------------------------

Puede automatizar la copia de seguridad de los datos de configuración utilizando la API de administración de Fess.
Configúrelo como un trabajo del programador o ejecútelo como un trabajo cron externo.

Procedimiento de restauración
-------------------------------

Es importante verificar el procedimiento de restauración con antelación para estar preparado en caso de fallo.

1. Detener Fess
2. Restaurar los datos de configuración (a través de la consola de administración o API)
3. Restaurar desde un snapshot de OpenSearch si es necesario
4. Iniciar Fess
5. Verificar el funcionamiento

Realice ensayos del procedimiento de restauración periódicamente para confirmar su exactitud y conocer el tiempo necesario.

Recuperación ante fallos
=========================

Fallos comunes y soluciones
-----------------------------

**Fess no arranca**

- Revise el archivo de log (logs/fess.log)
- Memoria JVM insuficiente: Ajuste el parámetro ``-Xmx``
- Conflicto de puertos: Verifique si el puerto 8080 está siendo utilizado por otro proceso
- Fallo de conexión con OpenSearch: Verifique que OpenSearch este en ejecución

**El rastreo falla**

- Revise el registro de trabajos ([Información del sistema] > [Registro de trabajos])
- Conectividad de red: Verifique la conectividad con el objetivo de rastreo
- Error de autenticación: Verifique la validez de las credenciales (contraseña, token)
- URLs con fallo: Consulte los detalles en [Información del sistema] > [URLs con fallo]

**La búsqueda es lenta**

- Verifique el estado del clúster de OpenSearch (si está en yellow/red, se requiere acción)
- Verifique el tamaño del índice (si ha crecido excesivamente)
- Verifique el heap JVM (si la recolección de basura ocurre con frecuencia)
- Si hay un rastreo en curso, verifique si el rendimiento mejora tras su finalización

**Los resultados de búsqueda están desactualizados**

- Verifique el calendario de rastreo (si se ejecuta normalmente)
- Verifique si el número máximo de accesos en la configuración de rastreo es insuficiente
- Verifique si el sitio objetivo está bloqueando los rastreos (robots.txt)

Gestión de URLs con fallo
----------------------------

Las URLs a las que no se pudo acceder durante el rastreo se registran como "URLs con fallo".
Puede revisarlas en [Información del sistema] > [URLs con fallo] en la consola de administración.

Si hay muchas URLs con fallo, verifique lo siguiente:

- Si el servidor objetivo está caído
- Si hay problemas con la ruta de red
- Si las credenciales siguen siendo válidas
- Si el intervalo de rastreo es demasiado corto, causando una carga excesiva en el servidor objetivo

Gestión de logs
-----------------

Los archivos de log de Fess se generan en las siguientes ubicaciones:

- **Log de Fess**: ``logs/fess.log`` (Log de aplicación)
- **Información de rastreo**: [Información del sistema] > [Información de rastreo] en la consola de administración
- **Registro de trabajos**: [Información del sistema] > [Registro de trabajos] en la consola de administración
- **Registro de búsqueda**: [Información del sistema] > [Registro de búsqueda] en la consola de administración

Asegúrese de que la rotación de logs este configurada para evitar que los archivos de log crezcan excesivamente.

Lista de verificación operativa
=================================

A continuación se presenta una lista de verificación de los elementos que deben comprobarse durante las operaciones rutinarias.

**Verificaciones diarias**

- ¿Se completó el rastreo correctamente?
- ¿El health check devuelve resultados normales?
- ¿El uso de disco está por debajo del umbral?

**Verificaciones semanales**

- Tasa de resultados vacíos en los registros de búsqueda (véase Parte 8)
- Revisión y tratamiento de URLs con fallo
- ¿Se están realizando las copias de seguridad correctamente?

**Verificaciones mensuales**

- Tendencias del tamaño del índice
- Tendencias del uso de memoria JVM
- Actualizaciones del diccionario (véase Parte 9)
- Revisión de parches de seguridad

Resumen
========

Este artículo cubrió la monitorización, las copias de seguridad y la recuperación ante fallos para la operación estable de Fess.

- Monitorización con la Health API y la consola de administración
- Estrategia de copias de seguridad para datos de configuración y datos del índice
- Patrones de fallos comunes y soluciones
- Listas de verificación operativas diarias, semanales y mensuales

Para mantener la expectativa de que "la búsqueda simplemente funciona", establezca un marco operativo proactivo.

En el próximo artículo se tratarán patrones de integración con sistemas existentes utilizando la API de búsqueda.

Referencias
============

- `Fess Administración del sistema <https://fess.codelibs.org/ja/15.5/admin/systeminfo.html>`__

- `Fess Copia de seguridad <https://fess.codelibs.org/ja/15.5/admin/backup.html>`__
