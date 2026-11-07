================================================
Parte 20: Conectar agentes de IA con la búsqueda
================================================

Introducción
============

En el artículo anterior, construimos un asistente de IA utilizando el modo de búsqueda con IA integrado de Fess.
Sin embargo, esa no es la única forma de aprovechar la IA.
Existe un método para utilizar Fess como "herramienta de búsqueda" desde Claude Desktop y otros agentes de IA.

En este artículo, configuraremos Fess como un servidor MCP (Model Context Protocol) y construiremos un entorno en el que las herramientas de IA externas puedan buscar documentos internos de forma transparente.

Público objetivo
================

- Personas interesadas en la integración de agentes de IA con sistemas de búsqueda
- Personas que desean comprender el concepto de MCP
- Personas que utilizan herramientas de IA como Claude Desktop en sus operaciones empresariales

¿Qué es MCP?
============

MCP (Model Context Protocol) es un protocolo que permite a las aplicaciones de IA acceder a fuentes de datos y herramientas externas.
Permite a los modelos de IA realizar operaciones como "buscar", "leer un archivo" y "llamar a una API" de manera estandarizada.

Al exponer Fess como un servidor MCP, los agentes de IA pueden ejecutar operaciones como "buscar documentos internos" en un contexto natural.

Un cambio de paradigma
-----------------------

La búsqueda tradicional seguía el modelo de "un humano introduce palabras clave y lee los resultados".
Con MCP, se hace realidad un nuevo modelo: "un agente de IA busca de forma autonoma, interpreta los resultados y los incorpora en sus respuestas".

Esto representa un cambio de "los humanos buscan" a "la IA busca en nombre de los humanos".

Construcción del servidor MCP de Fess
=======================================

Instalación del plugin
------------------------

La funcionalidad del servidor MCP de Fess se proporciona como un plugin webapp.

1. En el panel de administración, vaya a [Sistema] > [Plugins]
2. Instale ``fess-webapp-mcp``
3. Reinicie Fess

Funciones proporcionadas por el servidor MCP
----------------------------------------------

El servidor MCP de Fess proporciona las siguientes funciones a los agentes de IA.

**Tools**

- **search**: Búsqueda de texto completo en documentos internos
- **get_index_stats**: Obtención del número de documentos del índice e información de memoria JVM

Los agentes de IA pueden invocar estas herramientas para buscar en el índice de Fess o verificar el estado del sistema.

**Resources**

- **fess://index/stats**: Estadísticas del índice (número de documentos, información de configuración, memoria JVM)

**Prompts**

- **basic_search**: Generación de consultas de búsqueda básicas
- **advanced_search**: Generación de consultas de búsqueda detalladas que incluyen orden de clasificación y número de resultados

Integración con Claude Desktop
================================

Configuración de Claude Desktop
---------------------------------

Para conectar el servidor MCP de Fess a Claude Desktop, agregue la información del servidor MCP al archivo de configuración de Claude Desktop.

Agregue la siguiente configuración al archivo de configuración (claude_desktop_config.json).

.. code-block:: json

    {
      "mcpServers": {
        "fess": {
          "url": "http://localhost:8080/mcp"
        }
      }
    }

Ejemplos de uso
----------------

Una vez que Fess está conectado como servidor MCP en Claude Desktop, se hacen posibles interacciones como las siguientes.

**Ejemplo 1: Búsqueda de documentos internos**

    Usuario: "Por favor, infórmeme sobre el procedimiento de reembolso de gastos de viaje de negocios."

    Claude: (Invoca la herramienta de búsqueda de Fess)
    He buscado en los documentos internos sobre el reembolso de gastos de viaje de negocios.
    El procedimiento de reembolso es el siguiente:
    1. Crear un informe de viaje de negocios...
    [Del Manual de Reembolso de Gastos de Viaje (portal/manual/travel-expense.html)]

**Ejemplo 2: Investigación cruzada de documentos**

    Usuario: "Por favor, resuma las disposiciones sobre contraseñas en nuestra política de seguridad."

    Claude: (Busca en Fess "contraseña política de seguridad" e integra múltiples resultados)
    Las disposiciones sobre contraseñas están documentadas en los siguientes documentos:
    - Política Básica de Seguridad de la Información: Las contraseñas deben tener al menos 12 caracteres...
    - Reglamento de Gestión de Cuentas: Deben cambiarse cada 90 días...
    - Reglamento de Acceso Remoto: La autenticación multifactor es obligatoria...

Los agentes de IA interpretan los resultados de búsqueda y generan respuestas que integran información de múltiples documentos.

Integración con otras herramientas de IA
==========================================

Dado que MCP es un protocolo estándar, Fess puede utilizarse desde herramientas de IA compatibles con MCP distintas de Claude Desktop.

Uso desde agentes de IA personalizados
----------------------------------------

También es posible conectarse a Fess mediante el protocolo MCP desde agentes de IA desarrollados internamente.
Puede invocar la funcionalidad de búsqueda de Fess programáticamente utilizando bibliotecas cliente de MCP.

Consideraciones de seguridad
==============================

A continuación se presentan las consideraciones de seguridad al exponer el servidor MCP.

Control de acceso
------------------

- Restrinja el acceso al servidor MCP solo a clientes de confianza
- Restricciones a nivel de red (firewall, VPN)
- Autenticación mediante tokens de API

Control de permisos en los resultados de búsqueda
---------------------------------------------------

La búsqueda basada en roles de Fess (tratada en la Parte 5) también se aplica a las búsquedas a través de MCP.
Al asociar roles con tokens de API, puede controlar el alcance de los documentos a los que los agentes de IA pueden acceder.

Manejo de datos
----------------

Al integrar con servicios de IA basados en la nube, tenga en cuenta que el texto de los resultados de búsqueda se envía externamente.
Si se incluyen documentos altamente confidenciales, considere la combinación con un LLM local (Ollama) o el filtrado de los resultados de búsqueda.

Resumen
========

En este artículo, explicamos cómo exponer Fess como un servidor MCP e integrarlo con agentes de IA.

- El concepto del protocolo MCP y el paradigma "la IA busca"
- Instalación y configuración del plugin fess-webapp-mcp
- Ejemplos de integración con Claude Desktop
- Consideraciones de seguridad (control de acceso, permisos, manejo de datos)

Al permitir que los agentes de IA accedan directamente al conocimiento interno, las posibilidades de aprovechamiento del conocimiento se amplían significativamente.

En el próximo artículo, trataremos la búsqueda multimodal.

Referencias
===========

- `Fess MCP Server <https://github.com/codelibs/fess-webapp-mcp>`__

- `Model Context Protocol <https://modelcontextprotocol.io/>`__
