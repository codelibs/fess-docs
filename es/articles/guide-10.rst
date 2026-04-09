===========================================================================
Parte 10: Operacion estable de un sistema de busqueda -- Monitorizacion, copias de seguridad y recuperacion ante fallos en la practica
===========================================================================

Introduccion
=============

Una vez que ha construido un sistema de busqueda y lo ha puesto a disposicion de los usuarios, se convierte en un sistema que "no se puede detener".
Cuando los usuarios dependen de la busqueda en su trabajo diario, cualquier tiempo de inactividad se traduce directamente en una interrupcion del negocio.

Este articulo proporciona un manual practico sobre monitorizacion, copias de seguridad y recuperacion ante fallos para mantener Fess funcionando de forma fiable.

Audiencia objetivo
===================

- Administradores que operan Fess en un entorno de produccion
- Personas que desean garantizar la operacion estable de un sistema de busqueda
- Personas con conocimientos basicos de operaciones de sistemas

Vision general de la operacion
===============================

La operacion estable de Fess se basa en los siguientes tres pilares:

1. **Monitorizacion**: Detectar problemas de forma temprana
2. **Copias de seguridad**: Proteger los datos
3. **Recuperacion ante fallos**: Restaurar el servicio rapidamente cuando ocurren problemas

Monitorizacion
===============

Health Check
--------------

Fess proporciona un endpoint de health check a traves de la API REST.

::

    GET http://localhost:8080/api/v1/health

En condiciones normales, devuelve HTTP 200.
Al llamar periodicamente a este endpoint desde una herramienta de monitorizacion externa (como Nagios, Zabbix o Datadog), puede supervisar el estado operativo de Fess.

Consulta de informacion del sistema
-------------------------------------

Desde [Informacion del sistema] en la consola de administracion, puede consultar la siguiente informacion.

**Informacion de rastreo**

Puede revisar los resultados de la ultima ejecucion de rastreo (numero de documentos procesados, numero de errores, etc.).
Utilice esta funcion para verificar que los rastreos se completan correctamente.

**Informacion del sistema**

Puede consultar las versiones de Fess y OpenSearch, el uso de memoria JVM, el numero de documentos en el indice y mas.

Metricas a monitorizar
-----------------------

.. list-table:: Metricas de monitorizacion y umbrales orientativos
   :header-rows: 1
   :widths: 25 35 40

   * - Metrica
     - Metodo de verificacion
     - Condicion de alerta
   * - Proceso de Fess
     - Health API
     - Sin respuesta o HTTP 500
   * - Cluster de OpenSearch
     - Cluster Health API
     - Estado yellow / red
   * - Uso del heap JVM
     - Informacion del sistema
     - Sostenido por encima del 80 %
   * - Uso de disco
     - Comandos del SO
     - Por encima del 85 %
   * - Resultados de rastreo
     - Informacion de rastreo
     - Aumento repentino de errores, disminucion drastica del numero procesado
   * - Respuesta de busqueda
     - Registro de busqueda
     - Aumento significativo del tiempo de respuesta

Notificacion de finalizacion de rastreo
-----------------------------------------

Fess cuenta con una funcion que envia notificaciones cuando se detectan registros de error o fallos en el motor de busqueda.
Al configurar un Webhook para Slack o Google Chat, puede ser informado inmediatamente de cualquier anomalia.

Copias de seguridad
====================

Objetos de copia de seguridad
-------------------------------

Los objetos de copia de seguridad de un entorno Fess se dividen en dos categorias principales.

**1. Datos de configuracion**

Incluye la configuracion de rastreo, informacion de usuarios, datos de diccionario y otra informacion configurada a traves de la consola de administracion.
Puede obtener una copia de seguridad de los datos de configuracion desde [Informacion del sistema] > [Copia de seguridad] en la consola de administracion de Fess.

**2. Datos del indice**

Es el indice de documentos recopilados mediante rastreo.
Utilice la funcion de snapshots de OpenSearch para realizar la copia de seguridad del indice.

Estrategia de copias de seguridad
-----------------------------------

.. list-table:: Estrategia de copias de seguridad
   :header-rows: 1
   :widths: 20 25 25 30

   * - Objeto
     - Frecuencia
     - Periodo de retencion
     - Metodo
   * - Datos de configuracion
     - Diaria
     - 30 generaciones
     - Funcion de backup de Fess
   * - Indice
     - Diaria
     - 7 generaciones
     - Snapshot de OpenSearch
   * - Configuracion Docker
     - Al modificar
     - Gestionado con Git
     - Control de versiones de compose.yaml

Automatizacion de la copia de seguridad de configuracion
----------------------------------------------------------

Puede automatizar la copia de seguridad de los datos de configuracion utilizando la API de administracion de Fess.
Configurelo como un trabajo del programador o ejecutelo como un trabajo cron externo.

Procedimiento de restauracion
-------------------------------

Es importante verificar el procedimiento de restauracion con antelacion para estar preparado en caso de fallo.

1. Detener Fess
2. Restaurar los datos de configuracion (a traves de la consola de administracion o API)
3. Restaurar desde un snapshot de OpenSearch si es necesario
4. Iniciar Fess
5. Verificar el funcionamiento

Realice ensayos del procedimiento de restauracion periodicamente para confirmar su exactitud y conocer el tiempo necesario.

Recuperacion ante fallos
=========================

Fallos comunes y soluciones
-----------------------------

**Fess no arranca**

- Revise el archivo de log (logs/fess.log)
- Memoria JVM insuficiente: Ajuste el parametro ``-Xmx``
- Conflicto de puertos: Verifique si el puerto 8080 esta siendo utilizado por otro proceso
- Fallo de conexion con OpenSearch: Verifique que OpenSearch este en ejecucion

**El rastreo falla**

- Revise el registro de trabajos ([Informacion del sistema] > [Registro de trabajos])
- Conectividad de red: Verifique la conectividad con el objetivo de rastreo
- Error de autenticacion: Verifique la validez de las credenciales (contrasena, token)
- URLs con fallo: Consulte los detalles en [Informacion del sistema] > [URLs con fallo]

**La busqueda es lenta**

- Verifique el estado del cluster de OpenSearch (si esta en yellow/red, se requiere accion)
- Verifique el tamano del indice (si ha crecido excesivamente)
- Verifique el heap JVM (si la recoleccion de basura ocurre con frecuencia)
- Si hay un rastreo en curso, verifique si el rendimiento mejora tras su finalizacion

**Los resultados de busqueda estan desactualizados**

- Verifique el calendario de rastreo (si se ejecuta normalmente)
- Verifique si el numero maximo de accesos en la configuracion de rastreo es insuficiente
- Verifique si el sitio objetivo esta bloqueando los rastreos (robots.txt)

Gestion de URLs con fallo
----------------------------

Las URLs a las que no se pudo acceder durante el rastreo se registran como "URLs con fallo".
Puede revisarlas en [Informacion del sistema] > [URLs con fallo] en la consola de administracion.

Si hay muchas URLs con fallo, verifique lo siguiente:

- Si el servidor objetivo esta caido
- Si hay problemas con la ruta de red
- Si las credenciales siguen siendo validas
- Si el intervalo de rastreo es demasiado corto, causando una carga excesiva en el servidor objetivo

Gestion de logs
-----------------

Los archivos de log de Fess se generan en las siguientes ubicaciones:

- **Log de Fess**: ``logs/fess.log`` (Log de aplicacion)
- **Informacion de rastreo**: [Informacion del sistema] > [Informacion de rastreo] en la consola de administracion
- **Registro de trabajos**: [Informacion del sistema] > [Registro de trabajos] en la consola de administracion
- **Registro de busqueda**: [Informacion del sistema] > [Registro de busqueda] en la consola de administracion

Asegurese de que la rotacion de logs este configurada para evitar que los archivos de log crezcan excesivamente.

Lista de verificacion operativa
=================================

A continuacion se presenta una lista de verificacion de los elementos que deben comprobarse durante las operaciones rutinarias.

**Verificaciones diarias**

- Se completo el rastreo correctamente?
- El health check devuelve resultados normales?
- El uso de disco esta por debajo del umbral?

**Verificaciones semanales**

- Tasa de resultados vacios en los registros de busqueda (vease Parte 8)
- Revision y tratamiento de URLs con fallo
- Se estan realizando las copias de seguridad correctamente?

**Verificaciones mensuales**

- Tendencias del tamano del indice
- Tendencias del uso de memoria JVM
- Actualizaciones del diccionario (vease Parte 9)
- Revision de parches de seguridad

Resumen
========

Este articulo cubrio la monitorizacion, las copias de seguridad y la recuperacion ante fallos para la operacion estable de Fess.

- Monitorizacion con la Health API y la consola de administracion
- Estrategia de copias de seguridad para datos de configuracion y datos del indice
- Patrones de fallos comunes y soluciones
- Listas de verificacion operativas diarias, semanales y mensuales

Para mantener la expectativa de que "la busqueda simplemente funciona", establezca un marco operativo proactivo.

En el proximo articulo se trataran patrones de integracion con sistemas existentes utilizando la API de busqueda.

Referencias
============

- `Fess Administracion del sistema <https://fess.codelibs.org/ja/15.5/admin/systeminfo.html>`__

- `Fess Copia de seguridad <https://fess.codelibs.org/ja/15.5/admin/backup.html>`__
