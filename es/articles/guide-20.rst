============================================================
Parte 20: Conectar agentes de IA con la busqueda -- Integrar Fess en herramientas de IA externas mediante el servidor MCP
============================================================

Introduccion
============

En el articulo anterior, construimos un asistente de IA utilizando el modo de busqueda con IA integrado de Fess.
Sin embargo, esa no es la unica forma de aprovechar la IA.
Existe un metodo para utilizar Fess como "herramienta de busqueda" desde Claude Desktop y otros agentes de IA.

En este articulo, configuraremos Fess como un servidor MCP (Model Context Protocol) y construiremos un entorno en el que las herramientas de IA externas puedan buscar documentos internos de forma transparente.

Publico objetivo
================

- Personas interesadas en la integracion de agentes de IA con sistemas de busqueda
- Personas que desean comprender el concepto de MCP
- Personas que utilizan herramientas de IA como Claude Desktop en sus operaciones empresariales

Que es MCP?
===========

MCP (Model Context Protocol) es un protocolo que permite a las aplicaciones de IA acceder a fuentes de datos y herramientas externas.
Permite a los modelos de IA realizar operaciones como "buscar", "leer un archivo" y "llamar a una API" de manera estandarizada.

Al exponer Fess como un servidor MCP, los agentes de IA pueden ejecutar operaciones como "buscar documentos internos" en un contexto natural.

Un cambio de paradigma
-----------------------

La busqueda tradicional seguia el modelo de "un humano introduce palabras clave y lee los resultados".
Con MCP, se hace realidad un nuevo modelo: "un agente de IA busca de forma autonoma, interpreta los resultados y los incorpora en sus respuestas".

Esto representa un cambio de "los humanos buscan" a "la IA busca en nombre de los humanos".

Construccion del servidor MCP de Fess
=======================================

Instalacion del plugin
------------------------

La funcionalidad del servidor MCP de Fess se proporciona como un plugin webapp.

1. En el panel de administracion, vaya a [Sistema] > [Plugins]
2. Instale ``fess-webapp-mcp``
3. Reinicie Fess

Funciones proporcionadas por el servidor MCP
----------------------------------------------

El servidor MCP de Fess proporciona las siguientes funciones a los agentes de IA.

**Tools**

- **search**: Busqueda de texto completo en documentos internos
- **get_index_stats**: Obtencion del numero de documentos del indice e informacion de memoria JVM

Los agentes de IA pueden invocar estas herramientas para buscar en el indice de Fess o verificar el estado del sistema.

**Resources**

- **fess://index/stats**: Estadisticas del indice (numero de documentos, informacion de configuracion, memoria JVM)

**Prompts**

- **basic_search**: Generacion de consultas de busqueda basicas
- **advanced_search**: Generacion de consultas de busqueda detalladas que incluyen orden de clasificacion y numero de resultados

Integracion con Claude Desktop
================================

Configuracion de Claude Desktop
---------------------------------

Para conectar el servidor MCP de Fess a Claude Desktop, agregue la informacion del servidor MCP al archivo de configuracion de Claude Desktop.

Agregue la siguiente configuracion al archivo de configuracion (claude_desktop_config.json).

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

Una vez que Fess esta conectado como servidor MCP en Claude Desktop, se hacen posibles interacciones como las siguientes.

**Ejemplo 1: Busqueda de documentos internos**

    Usuario: "Por favor, informeme sobre el procedimiento de reembolso de gastos de viaje de negocios."

    Claude: (Invoca la herramienta de busqueda de Fess)
    He buscado en los documentos internos sobre el reembolso de gastos de viaje de negocios.
    El procedimiento de reembolso es el siguiente:
    1. Crear un informe de viaje de negocios...
    [Del Manual de Reembolso de Gastos de Viaje (portal/manual/travel-expense.html)]

**Ejemplo 2: Investigacion cruzada de documentos**

    Usuario: "Por favor, resuma las disposiciones sobre contrasenas en nuestra politica de seguridad."

    Claude: (Busca en Fess "contrasena politica de seguridad" e integra multiples resultados)
    Las disposiciones sobre contrasenas estan documentadas en los siguientes documentos:
    - Politica Basica de Seguridad de la Informacion: Las contrasenas deben tener al menos 12 caracteres...
    - Reglamento de Gestion de Cuentas: Deben cambiarse cada 90 dias...
    - Reglamento de Acceso Remoto: La autenticacion multifactor es obligatoria...

Los agentes de IA interpretan los resultados de busqueda y generan respuestas que integran informacion de multiples documentos.

Integracion con otras herramientas de IA
==========================================

Dado que MCP es un protocolo estandar, Fess puede utilizarse desde herramientas de IA compatibles con MCP distintas de Claude Desktop.

Uso desde agentes de IA personalizados
----------------------------------------

Tambien es posible conectarse a Fess mediante el protocolo MCP desde agentes de IA desarrollados internamente.
Puede invocar la funcionalidad de busqueda de Fess programaticamente utilizando bibliotecas cliente de MCP.

Consideraciones de seguridad
==============================

A continuacion se presentan las consideraciones de seguridad al exponer el servidor MCP.

Control de acceso
------------------

- Restrinja el acceso al servidor MCP solo a clientes de confianza
- Restricciones a nivel de red (firewall, VPN)
- Autenticacion mediante tokens de API

Control de permisos en los resultados de busqueda
---------------------------------------------------

La busqueda basada en roles de Fess (tratada en la Parte 5) tambien se aplica a las busquedas a traves de MCP.
Al asociar roles con tokens de API, puede controlar el alcance de los documentos a los que los agentes de IA pueden acceder.

Manejo de datos
----------------

Al integrar con servicios de IA basados en la nube, tenga en cuenta que el texto de los resultados de busqueda se envia externamente.
Si se incluyen documentos altamente confidenciales, considere la combinacion con un LLM local (Ollama) o el filtrado de los resultados de busqueda.

Resumen
========

En este articulo, explicamos como exponer Fess como un servidor MCP e integrarlo con agentes de IA.

- El concepto del protocolo MCP y el paradigma "la IA busca"
- Instalacion y configuracion del plugin fess-webapp-mcp
- Ejemplos de integracion con Claude Desktop
- Consideraciones de seguridad (control de acceso, permisos, manejo de datos)

Al permitir que los agentes de IA accedan directamente al conocimiento interno, las posibilidades de aprovechamiento del conocimiento se amplian significativamente.

En el proximo articulo, trataremos la busqueda multimodal.

Referencias
===========

- `Fess MCP Server <https://github.com/codelibs/fess-webapp-mcp>`__

- `Model Context Protocol <https://modelcontextprotocol.io/>`__
