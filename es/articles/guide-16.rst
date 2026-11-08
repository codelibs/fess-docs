==========================================================
Parte 16: Automatización de la infraestructura de búsqueda
==========================================================

Introducción
=============

Cuando la configuración de un sistema de búsqueda se gestiona manualmente, resulta difícil reproducir los entornos y aumenta el riesgo de errores de configuración.
Adoptando prácticas modernas de DevOps, gestionemos y automaticemos también la infraestructura de búsqueda como código.

En este artículo se presenta un enfoque para gestionar las configuraciones de Fess como código y automatizar los despliegues.

Público objetivo
=================

- Personas que desean automatizar las operaciones del sistema de búsqueda
- Personas que desean aplicar métodos DevOps/IaC a la infraestructura de búsqueda
- Personas con conocimientos básicos de Docker y CI/CD

Aplicación de Infrastructure as Code
=======================================

Los siguientes elementos se gestionan como "código" para los entornos de Fess.

.. list-table:: Objetivos de gestión IaC
   :header-rows: 1
   :widths: 25 35 40

   * - Objetivo
     - Método de gestión
     - Control de versiones
   * - Configuración de Docker
     - compose.yaml
     - Git
   * - Configuración de Fess
     - Archivos de respaldo / API de administración
     - Git
   * - Datos de diccionario
     - Exportación mediante API de administración
     - Git
   * - Configuración de OpenSearch
     - Archivos de configuración
     - Git

Definición de entornos con Docker Compose
============================================

Archivo Docker Compose para producción
-----------------------------------------

Ampliamos la configuración básica utilizada en la Parte 2 para definir una configuración adecuada para entornos de producción.

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

- Definición del health check: Fess se inicia solo cuando OpenSearch está listo
- Persistencia de volúmenes: Los datos se mantienen de forma permanente
- Política de reinicio: Recuperación automática ante fallos
- Configuración explícita del heap de la JVM

Automatización de la configuración con la API de administración
=================================================================

Mediante el uso de la API de administración de Fess, puede gestionar las configuraciones de forma programática sin utilizar la interfaz gráfica.

Exportar configuración
-----------------------

Exporte la configuración actual de Fess y guárdela como código.

Puede exportar desde la consola de administración en [Información del sistema] > [Respaldo].
También es posible exportar mediante scripts utilizando la API de administración.

Importar configuración
-----------------------

Aplique la configuración a un nuevo entorno de Fess utilizando los archivos de configuración guardados.
Esto facilita la reconstrucción o replicación de entornos.

Uso de la CLI fessctl
======================

fessctl es una herramienta de línea de comandos para Fess.
Muchas de las operaciones que se pueden realizar en la consola de administración también se pueden ejecutar desde la línea de comandos.

Operaciones principales
-------------------------

- Crear, actualizar y eliminar configuraciones de rastreo (web, sistema de archivos, almacén de datos)
- Ejecutar trabajos del planificador
- Gestionar usuarios, roles y grupos
- Gestionar configuraciones de búsqueda como key match, etiquetas y boosts

Mediante el uso de la CLI, puede convertir los cambios de configuración en scripts e integrarlos en pipelines CI/CD.

Construcción de pipelines CI/CD
=================================

Flujo de trabajo para cambios de configuración
-------------------------------------------------

Gestione los cambios de configuración del sistema de búsqueda con el siguiente flujo de trabajo.

1. **Cambio**: Modificar los archivos de configuración y gestionarlos en una rama de Git
2. **Revisión**: Revisar los cambios mediante pull requests
3. **Prueba**: Verificar el comportamiento en un entorno de staging
4. **Despliegue**: Aplicar la configuración al entorno de producción

Ejemplo de automatización con GitHub Actions
-----------------------------------------------

Este es un ejemplo de aplicación automática de cambios al entorno de producción cuando se fusionan cambios en los archivos de configuración.

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

Automatización de respaldos
=============================

Automaticemos también los respaldos periódicos.

Script de respaldo
-------------------

Utilice cron o las funciones de programación de CI/CD para realizar respaldos periódicos.

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

Procedimiento de reconstrucción del entorno
=============================================

Documente el procedimiento para reconstruir completamente un entorno para la recuperación ante desastres o la creación de entornos de prueba.

1. Iniciar los contenedores con Docker Compose
2. Esperar hasta que el health check de OpenSearch devuelva green/yellow
3. Importar la configuración de Fess (mediante la API de administración o la función de restauración)
4. Colocar los archivos de diccionario
5. Ejecutar los trabajos de rastreo
6. Verificar el funcionamiento (pruebas de búsqueda)

Al convertir este procedimiento en un script, puede reconstruir los entornos rápidamente.

Resumen
========

En este artículo se presentó un enfoque para gestionar la infraestructura de búsqueda de Fess utilizando prácticas de DevOps.

- Codificación de las definiciones de entorno con Docker Compose
- Automatización de la configuración con la API de administración y fessctl
- Automatización del despliegue de cambios de configuración con pipelines CI/CD
- Automatización de respaldos y procedimientos de reconstrucción de entornos

Evolucione las operaciones de su infraestructura de búsqueda de "leer manuales y configurar manualmente" a "ejecutar código y desplegar automáticamente".

En el próximo artículo se tratará la extensión de Fess mediante el desarrollo de plugins.

Referencias
============

- `Fess Admin API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__
