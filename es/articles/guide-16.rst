============================================================
Parte 16: Automatizacion de la infraestructura de busqueda -- Gestion con pipelines CI/CD e Infrastructure as Code
============================================================

Introduccion
=============

Cuando la configuracion de un sistema de busqueda se gestiona manualmente, resulta dificil reproducir los entornos y aumenta el riesgo de errores de configuracion.
Adoptando practicas modernas de DevOps, gestionemos y automaticemos tambien la infraestructura de busqueda como codigo.

En este articulo se presenta un enfoque para gestionar las configuraciones de Fess como codigo y automatizar los despliegues.

Publico objetivo
=================

- Personas que desean automatizar las operaciones del sistema de busqueda
- Personas que desean aplicar metodos DevOps/IaC a la infraestructura de busqueda
- Personas con conocimientos basicos de Docker y CI/CD

Aplicacion de Infrastructure as Code
=======================================

Los siguientes elementos se gestionan como "codigo" para los entornos de Fess.

.. list-table:: Objetivos de gestion IaC
   :header-rows: 1
   :widths: 25 35 40

   * - Objetivo
     - Metodo de gestion
     - Control de versiones
   * - Configuracion de Docker
     - compose.yaml
     - Git
   * - Configuracion de Fess
     - Archivos de respaldo / API de administracion
     - Git
   * - Datos de diccionario
     - Exportacion mediante API de administracion
     - Git
   * - Configuracion de OpenSearch
     - Archivos de configuracion
     - Git

Definicion de entornos con Docker Compose
============================================

Archivo Docker Compose para produccion
-----------------------------------------

Ampliamos la configuracion basica utilizada en la Parte 2 para definir una configuracion adecuada para entornos de produccion.

.. code-block:: yaml

    services:
      fess:
        image: ghcr.io/codelibs/fess:15.5.1
        environment:
          - SEARCH_ENGINE_HTTP_URL=http://opensearch:9200
          - FESS_DICTIONARY_PATH=/usr/share/opensearch/config/dictionary/
        ports:
          - "8080:8080"
        depends_on:
          opensearch:
            condition: service_healthy
        restart: unless-stopped

      opensearch:
        image: ghcr.io/codelibs/fess-opensearch:3.6.0
        environment:
          - discovery.type=single-node
          - OPENSEARCH_JAVA_OPTS=-Xmx4g -Xms4g
          - DISABLE_INSTALL_DEMO_CONFIG=true
          - DISABLE_SECURITY_PLUGIN=true
          - FESS_DICTIONARY_PATH=/usr/share/opensearch/config/dictionary/
        volumes:
          - opensearch-data:/usr/share/opensearch/data
          - opensearch-dictionary:/usr/share/opensearch/config/dictionary
        healthcheck:
          test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
          interval: 30s
          timeout: 10s
          retries: 3
          start_period: 90s
        restart: unless-stopped

    volumes:
      opensearch-data:
      opensearch-dictionary:

Los puntos clave son los siguientes.

- Definicion del health check: Fess se inicia solo cuando OpenSearch esta listo
- Persistencia de volumenes: Los datos se mantienen de forma permanente
- Politica de reinicio: Recuperacion automatica ante fallos
- Configuracion explicita del heap de la JVM

Automatizacion de la configuracion con la API de administracion
=================================================================

Mediante el uso de la API de administracion de Fess, puede gestionar las configuraciones de forma programatica sin utilizar la interfaz grafica.

Exportar configuracion
-----------------------

Exporte la configuracion actual de Fess y guardela como codigo.

Puede exportar desde la consola de administracion en [Informacion del sistema] > [Respaldo].
Tambien es posible exportar mediante scripts utilizando la API de administracion.

Importar configuracion
-----------------------

Aplique la configuracion a un nuevo entorno de Fess utilizando los archivos de configuracion guardados.
Esto facilita la reconstruccion o replicacion de entornos.

Uso de la CLI fessctl
======================

fessctl es una herramienta de linea de comandos para Fess.
Muchas de las operaciones que se pueden realizar en la consola de administracion tambien se pueden ejecutar desde la linea de comandos.

Operaciones principales
-------------------------

- Crear, actualizar y eliminar configuraciones de rastreo (web, sistema de archivos, almacen de datos)
- Ejecutar trabajos del planificador
- Gestionar usuarios, roles y grupos
- Gestionar configuraciones de busqueda como key match, etiquetas y boosts

Mediante el uso de la CLI, puede convertir los cambios de configuracion en scripts e integrarlos en pipelines CI/CD.

Construccion de pipelines CI/CD
=================================

Flujo de trabajo para cambios de configuracion
-------------------------------------------------

Gestione los cambios de configuracion del sistema de busqueda con el siguiente flujo de trabajo.

1. **Cambio**: Modificar los archivos de configuracion y gestionarlos en una rama de Git
2. **Revision**: Revisar los cambios mediante pull requests
3. **Prueba**: Verificar el comportamiento en un entorno de staging
4. **Despliegue**: Aplicar la configuracion al entorno de produccion

Ejemplo de automatizacion con GitHub Actions
-----------------------------------------------

Este es un ejemplo de aplicacion automatica de cambios al entorno de produccion cuando se fusionan cambios en los archivos de configuracion.

.. code-block:: yaml

    name: Deploy Fess Config
    on:
      push:
        branches: [main]
        paths:
          - 'fess-config/**'
          - 'dictionary/**'

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - name: Apply dictionary updates
            run: |
              # Transferir archivos de diccionario al servidor Fess
              scp dictionary/* fess-server:/opt/fess/dictionary/

          - name: Verify Fess health
            run: |
              # Verificar el estado operativo de Fess mediante la API de salud
              curl -s https://fess.example.com/api/v1/health

Automatizacion de respaldos
=============================

Automaticemos tambien los respaldos periodicos.

Script de respaldo
-------------------

Utilice cron o las funciones de programacion de CI/CD para realizar respaldos periodicos.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    BACKUP_DIR="/backup/fess/$(date +%Y%m%d)"
    mkdir -p "${BACKUP_DIR}"

    # Obtener la lista de archivos de respaldo de Fess
    curl -s -o "${BACKUP_DIR}/fess-backup-files.json" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/files"

    # Descargar datos de configuracion (ejemplo: fess_config.bulk)
    curl -s -o "${BACKUP_DIR}/fess_config.bulk" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/file/fess_config.bulk"

    # Eliminar respaldos antiguos (mas de 30 dias)
    find /backup/fess -type d -mtime +30 -exec rm -rf {} +

    echo "Backup completed: ${BACKUP_DIR}"

Procedimiento de reconstruccion del entorno
=============================================

Documente el procedimiento para reconstruir completamente un entorno para la recuperacion ante desastres o la creacion de entornos de prueba.

1. Iniciar los contenedores con Docker Compose
2. Esperar hasta que el health check de OpenSearch devuelva green/yellow
3. Importar la configuracion de Fess (mediante la API de administracion o la funcion de restauracion)
4. Colocar los archivos de diccionario
5. Ejecutar los trabajos de rastreo
6. Verificar el funcionamiento (pruebas de busqueda)

Al convertir este procedimiento en un script, puede reconstruir los entornos rapidamente.

Resumen
========

En este articulo se presento un enfoque para gestionar la infraestructura de busqueda de Fess utilizando practicas de DevOps.

- Codificacion de las definiciones de entorno con Docker Compose
- Automatizacion de la configuracion con la API de administracion y fessctl
- Automatizacion del despliegue de cambios de configuracion con pipelines CI/CD
- Automatizacion de respaldos y procedimientos de reconstruccion de entornos

Evolucione las operaciones de su infraestructura de busqueda de "leer manuales y configurar manualmente" a "ejecutar codigo y desplegar automaticamente".

En el proximo articulo se tratara la extension de Fess mediante el desarrollo de plugins.

Referencias
============

- `Fess Admin API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__
