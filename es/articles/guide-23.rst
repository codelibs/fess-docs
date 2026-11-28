===============================================
Despliegue en toda la empresa: lista por etapas
===============================================

Introducción
============

Cuando la prueba de Fess sale bien y se decide extenderlo a toda la empresa, lo difícil no son tanto las funciones en sí como el orden en que se configuran.
Algunos ajustes suponen mucho trabajo de corrección si se dejan para una etapa posterior.
Por ejemplo, cambiar la clave de cifrado después de registrar credenciales hace imposible descifrar los valores guardados, y cambiar después los permisos de los documentos obliga a volver a rastrear.

Este artículo muestra, etapa por etapa, el orden para desplegar Fess 15.9 en toda la empresa.
Para cada etapa indica qué configurar, qué comprobar y los indicadores que permiten decidir si se puede pasar a la siguiente.
Como indicadores usamos los informes de análisis de [Información del sistema] > [Registro de búsqueda] en la consola de administración.
No se explican aquí los procedimientos de cada función; en su lugar, enlazamos los artículos que tratan esa función.

Componentes y artículos que los tratan
======================================

Los componentes que intervienen en un despliegue en toda la empresa, y los artículos que tratan cada uno en detalle, son los siguientes.

- Fess: ofrece la página de búsqueda, la consola de administración, la API y el programador. Visión general en :doc:`guide-01`; memoria y ampliación del número de servidores en :doc:`guide-14`
- OpenSearch: además del índice de documentos, guarda las configuraciones de rastreo, los usuarios, los registros de trabajo y los registros de búsqueda. Separación y clúster en :doc:`guide-14`; instantáneas en :doc:`guide-10`
- Procesos hijos como el rastreador: el rastreo, la generación de sugerencias, la generación de miniaturas y el procesamiento de fragmentos se ejecutan, en cada trabajo, en una JVM distinta de la de Fess. Configuración del heap en :doc:`guide-14`
- Plugins: almacenes de datos (``fess-ds-*``), SSO (``fess-sso-*``), LLM y embeddings (``fess-llm-*``), MCP y búsqueda multimodal (``fess-webapp-*``), entre otros. Instale la misma versión menor que Fess (15.9.x) y reinicie Fess después de instalar o eliminar uno. Cómo crearlos: :doc:`guide-17`
- LLM y modelos de embeddings (opcional): servicios externos, o servidores como Ollama, que usan el modo de búsqueda con IA y la búsqueda semántica. Configuración en :doc:`guide-18` y :doc:`guide-19`

Lo que no se guarda en OpenSearch se gestiona por separado en cada servidor de Fess.
Son tres cosas: los ajustes de [Sistema] > [General] (``system.properties``), ``fess_config.properties`` (incluida la clave de cifrado ``app.cipher.key``) y los plugins instalados.
Para guardar una copia de ellos, consulte :doc:`guide-10`; para gestionarlos como código, :doc:`guide-16`.

Resumen de las etapas
=====================

.. list-table::
   :header-rows: 1
   :widths: 22 40 38

   * - Etapa
     - Objetivo
     - Se puede avanzar cuando
   * - 1. Prueba
     - Dejar buscar a unos pocos usuarios y averiguar qué buscan
     - Se han dejado registradas las consultas más frecuentes y las consultas sin resultados
   * - 2. Publicar la primera fuente
     - Publicar la primera fuente con permisos y establecer las bases de la operación
     - Se han registrado los valores de referencia de usuarios y tasa de clics
   * - 3. SSO e inicio de sesión
     - Iniciar sesión con el ID de la empresa y mostrar resultados distintos según el grupo
     - Los grupos del IdP aparecen en "Búsquedas por rol y grupo"
   * - 4. Añadir fuentes
     - Añadir SaaS, almacenamiento en la nube y bases de datos
     - Desaparecen las consultas sin resultados cuya causa era la falta de documentos
   * - 5. Ciclo de mejora de la calidad
     - Encontrar en el registro de búsqueda las consultas problemáticas y corregirlas
     - Los indicadores corregidos no han empeorado respecto al período anterior
   * - 6. Ampliación y automatización
     - Prepararse para el aumento de documentos y usuarios, y hacer reproducible el entorno
     - Los tiempos de respuesta de la pestaña [Rendimiento] no son peores que antes de la ampliación, aunque aumenten los usuarios
   * - 7. Funciones de IA
     - Añadir el modo de búsqueda con IA, la búsqueda semántica y MCP
     - Las solicitudes se registran en la pestaña [Chat con IA] y la tasa de errores no es mayor que justo después de la implantación

Cada etapa presupone los ajustes de las anteriores.
En particular, las etapas 2 y 3 incluyen ajustes que obligan a volver a rastrear si se cambian después, así que no altere su orden.

Etapa 1: prueba
===============

Instale un Fess de evaluación y haga que lo usen algunos departamentos.
El objetivo de esta etapa es reunir, como registros de búsqueda, lo que buscan los usuarios.

**Qué configurar**

- Siguiendo :doc:`guide-02`, inicie Fess con los archivos Compose de la etiqueta ``v15.9.0`` de docker-fess y cambie la contraseña en el primer inicio de sesión
- Cree una configuración de rastreo limitada a un solo sitio o a una sola carpeta
- Compruebe que "Registro de búsqueda" y "Registro de usuario" estén habilitados en [Sistema] > [General] (ambos lo están de forma predeterminada). Si "Registro de usuario" está deshabilitado, no se contabiliza el número de usuarios

**Qué comprobar**

- En [Información del sistema] > [Registro de trabajo], el trabajo de rastreo termina en "OK", y en [Información del sistema] > [Información de rastreo], el número de documentos registrados no es 0
- Si hay pocos documentos, revise [Información del sistema] > [URL de fallo] (:doc:`guide-02`)

**Se puede avanzar cuando**

- En la pestaña [Resumen] de [Registro de búsqueda] se muestran, para el período de prueba, las búsquedas, los usuarios, las consultas más frecuentes y las consultas sin resultados
- Haga clic en las consultas sin resultados, compruebe las búsquedas reales en la pestaña [Registros] y, según la tabla de :doc:`guide-08`, clasifique las causas en "otra forma de expresarlo", "guiar al término oficial" y "no hay documentos"
- Los términos clasificados como "no hay documentos" son candidatos a fuentes que añadir en las etapas 2 y 4. Descargue la tabla en CSV y consérvela

Etapa 2: publicar la primera fuente
===================================

Elija una fuente que vayan a usar los usuarios de toda la empresa y publíquela con permisos.
Al mismo tiempo, prepare la supervisión y las copias de seguridad necesarias para operar en producción.

**Qué configurar**

- Defina la clave de cifrado ``app.cipher.key`` antes de registrar credenciales en la autenticación web, la autenticación de archivos o los parámetros de los almacenes de datos. Si la cambia después de registrarlas, los valores guardados ya no se pueden descifrar (:doc:`guide-16`, :doc:`guide-10`)
- Cree las configuraciones de rastreo de sitios web y carpetas compartidas, la autenticación de archivos y las etiquetas (:doc:`guide-04`). Para reflejar las ACL del servidor de archivos en los resultados de búsqueda, consulte :doc:`file-server-search`
- Defina el diseño de permisos (:doc:`guide-05`). Las nuevas configuraciones de rastreo y etiquetas incluyen el permiso ``{role}guest`` y, tal como están, también son visibles para los usuarios que no han iniciado sesión. En los documentos que solo deben ver ciertos departamentos, elimine este valor y escriba después ``{group}`` u otro equivalente
- Haga coincidir los nombres de grupo que escriba en ``{group}`` con los nombres que llegarán del IdP en la etapa 3. Cambiarlos más adelante obliga a reescribir los permisos y volver a rastrear
- Si tiene configuraciones de rastreo que se ejecutan con un trabajo, por ejemplo una vez a la semana, haga que "Eliminar documentos anteriores" de [General] (3 días de forma predeterminada) sea más largo que el intervalo de rastreo (:doc:`guide-04`)
- Configure la supervisión, las notificaciones y las copias de seguridad (:doc:`guide-10`). Llame a ``/api/v2/health`` desde una herramienta de supervisión externa, configure "Correo de notificación" o "Slack Webhook URLs" en [General] y obtenga cada día el archivo de [Información del sistema] > [Copia de seguridad] mediante la API de administración
- Con Docker, los ajustes de [General] se guardan en ``system.properties`` dentro del contenedor ``fess01`` y se pierden cuando ``down`` vuelve a crear el contenedor. Inclúyalos en la copia de seguridad o páselos con ``FESS_JAVA_OPTS`` (:doc:`guide-02`, :doc:`guide-16`)
- Si es necesario, coloque un cuadro de búsqueda en el portal de la empresa (:doc:`guide-03`)

**Qué comprobar**

- Al iniciar sesión con usuarios de distintos departamentos, cambian los documentos visibles. En los permisos registrados en los documentos de cada departamento ya no figura el rol guest inicial (cómo comprobarlo, en :doc:`guide-05`)
- ``/api/v2/health`` devuelve 200, y con [Enviar correo de prueba] de [General] llega un correo
- Ejecute una vez a mano el script de copia de seguridad y compruebe que el archivo obtenido no está vacío (:doc:`guide-10`)

**Se puede avanzar cuando**

[Registro de búsqueda] no indica el estado de la supervisión ni de las copias de seguridad de esta etapa.
Eso se juzga con el apartado "Qué comprobar" anterior.
En el registro de búsqueda se toman los valores de referencia del uso tras la publicación.

- En la pestaña [Resumen], compruebe las búsquedas, los usuarios, la tasa de cero resultados y la tasa de clics del período posterior a la publicación, y guárdelos en CSV. En las etapas siguientes se comparan con estos valores mediante "Comparar con el período anterior"
- En "URL con más clics" de la pestaña [Clics] aparecen las URL de la fuente publicada
- Si indica un número de días en "Eliminar registros de búsqueda anteriores" de [General], los registros más antiguos no se pueden usar para comparar (el valor predeterminado ``-1`` no elimina nada). Decida el período de conservación

Etapa 3: SSO e inicio de sesión
===============================

Haga que los usuarios inicien sesión con el proveedor de identidad (IdP) de la empresa y muestre resultados de búsqueda distintos según los grupos del IdP.

Aquí, SSO se refiere a los cuatro métodos que Fess 15.9 ofrece como plugins.
Entra ID usa ``fess-sso-entraid``; OpenID Connect, ``fess-sso-oidc`` ("SSO Type" es ``oic``); SAML, ``fess-sso-saml``, y SPNEGO, ``fess-sso-spnego``.
Las imágenes Docker incluyen los cuatro, pero las imágenes ``-slim`` no.
Con los paquetes ZIP, RPM y DEB, instálelos desde [Sistema] > [Plugin] o con ``bin/fess-setup``.

LDAP no es SSO.
Los ajustes LDAP de [General] comprueban el ID y la contraseña introducidos en la página de inicio de sesión de Fess contra Active Directory u otro directorio similar, y obtienen los grupos a los que pertenece el usuario (:doc:`guide-05`).
SPNEGO usa estos ajustes LDAP para obtener los grupos.

**Qué configurar**

- Instale el plugin, reinicie Fess y configure "SSO Type" y los datos del IdP en [General]. La URL de retorno que se registra en el IdP es ``https://<host de Fess>/sso/`` (:doc:`guide-15`)
- Si Fess está detrás de un proxy inverso que termina TLS, indique a Fess el esquema y el puerto externos (:doc:`guide-15`)
- Si los usuarios que no han iniciado sesión no deben poder buscar, habilite "Requiere inicio de sesión" en [General]

"Requiere inicio de sesión" afecta a algo más que la página de búsqueda.

- La API de búsqueda de ``/api/v2/`` devuelve 401 a las llamadas que no tienen sesión iniciada ni un token de acceso válido. Prepare tokens para las llamadas desde los sistemas de negocio (:doc:`guide-11`)
- Con el valor predeterminado ``mcp.auth.mode=none``, ``/mcp`` rechaza con HTTP 403 las llamadas de los agentes de IA. Si lo usa, cambie el ajuste para que se autentique con tokens de acceso (:doc:`guide-20`)

**Qué comprobar**

- Al abrir ``/sso/`` se puede iniciar sesión a través del IdP, y los documentos visibles para cada departamento cambian según el diseño de la etapa 2 (:doc:`guide-15`)
- Si ejecuta Fess en varios servidores, las sesiones persistentes (sticky sessions) están habilitadas en el balanceador de carga. En 15.9, las sesiones de inicio de sesión se guardan en la memoria de cada Fess

**Se puede avanzar cuando**

- En "Búsquedas por rol y grupo" de la pestaña [Audiencia] de [Registro de búsqueda] aparecen filas de los grupos recibidos del IdP con la forma ``{group}<nombre del grupo>``
- Si no aparecen filas de grupos, o bien los usuarios buscan sin iniciar sesión (se contabilizan en la fila ``{role}guest``), o bien los grupos no llegan a Fess
- El número de usuarios de la pestaña [Resumen] no ha bajado mucho respecto al valor de referencia de la etapa 2. Compruebe con la columna "Usuarios" de "Búsquedas por rol y grupo" que ningún departamento ha dejado de usar la búsqueda por la introducción del inicio de sesión

Etapa 4: añadir fuentes
=======================

Añada fuentes distintas de los sitios web y los servidores de archivos mediante plugins de almacén de datos.
Los pasos comunes a todas las fuentes (instalación del plugin, parámetros y scripts, permisos, trabajos y cómo comprobar los resultados) están reunidos en :doc:`datastore-basics`.
Léalo primero.

**Qué configurar**

- Instale el plugin de cada fuente y reinicie

  - Git, Confluence/Jira, Slack: ``fess-ds-git``, ``fess-ds-atlassian``, ``fess-ds-slack`` (:doc:`guide-06`)
  - Google Drive, SharePoint/OneDrive, Box: ``fess-ds-gsuite``, ``fess-ds-microsoft365``, ``fess-ds-box`` (:doc:`guide-07`)
  - Bases de datos, CSV, Salesforce: ``fess-ds-db``, ``fess-ds-csv``, ``fess-ds-salesforce`` (:doc:`guide-12`)
  - Para una fuente sin plugin correspondiente, cree su propio plugin (:doc:`guide-17`)

- Las configuraciones de almacén de datos también incluyen ``{role}guest``. Decida en cada configuración si hereda los permisos de la fuente o si los escribe con las entradas ``{group}`` de la etapa 2
- Con [Crear nuevo trabajo], dé a cada configuración su propio trabajo para poder tratar por fuente los límites de frecuencia de las API y la caducidad de las credenciales
- Asigne una etiqueta a cada fuente para poder filtrar en la página de búsqueda. Las configuraciones de almacén de datos no tienen campo de etiqueta, así que asígnela con un script o con "Rutas incluidas" de la etiqueta (:doc:`datastore-basics`)

**Qué comprobar**

- Un trabajo de almacén de datos puede terminar en "OK" aunque se produzca un error en el conector. Compruebe a la vez "Tamaño del índice (Almacén de datos)" en [Información de rastreo], [URL de fallo] y ``fess-crawler.log`` (:doc:`datastore-basics`)
- En las fuentes que heredan permisos, al buscar con usuarios con permisos distintos cambian los documentos visibles

**Se puede avanzar cuando**

- Las consultas sin resultados que clasificó como "no hay documentos" en las etapas 1 y 2 desaparecen de las consultas sin resultados de la pestaña [Consultas] en el período posterior a la incorporación de la fuente
- En "URL con más clics" de la pestaña [Clics] aparecen documentos de las fuentes añadidas. Si una fuente no aparece, o no se busca o no sale en las primeras posiciones de los resultados. Lo segundo se trata en la etapa 5

Etapa 5: ciclo de mejora de la calidad
======================================

Cuando ya estén todas las fuentes, revise periódicamente el registro de búsqueda y corrija las consultas problemáticas.
Cómo elegir la corrección y cómo aplicarla se explica en :doc:`guide-08`.

**Qué configurar**

- Use sinónimos o consultas relacionadas para las consultas sin resultados, y la coincidencia de clave o el impulso de documento para los documentos que quedan enterrados en posiciones bajas (:doc:`guide-08`). Después de cambiar el diccionario de sinónimos, recargue el índice de documentos en [Información del sistema] > [Mantenimiento]
- Si se escapan documentos que mezclan japonés, inglés y chino, revise los campos y diccionarios de cada idioma (:doc:`guide-09`)
- Cuando necesite agregaciones que no ofrecen los informes integrados (URL abiertas por consulta, consultas sin resultados por rol, evolución mensual durante un período largo, etc.), use OpenSearch Dashboards (:doc:`guide-22`)
- Para gestionar como código los diccionarios y los ajustes de coincidencia de clave, consulte :doc:`guide-16`

**Qué comprobar**

- Al buscar los términos corregidos en la página de búsqueda, aparece el documento deseado, o aparece en las primeras posiciones
- En la coincidencia de clave, el documento objetivo se muestra en el campo "URL" de la página de detalles (:doc:`guide-08`)

**Se puede avanzar cuando**

Esta etapa no termina nunca; se repite.
El efecto de cada mejora se comprueba así:

- Ponga el período en "Personalizado" a partir del día siguiente al cambio y habilite "Comparar con el período anterior"
- Si corrigió consultas sin resultados, mire la tasa de cero resultados de la pestaña [Resumen] y las consultas sin resultados de la pestaña [Consultas]; si corrigió el orden, mire la posición media de clic de la pestaña [Consultas] y la distribución de posiciones de clic de la pestaña [Clics]
- Si los términos corregidos han desaparecido de la lista y los indicadores generales no han empeorado respecto al período anterior, mantenga el cambio

Etapa 6: ampliación y automatización
====================================

Cuando aumenten los documentos o los usuarios, compruebe qué es lo que falta antes de ampliar.
Al mismo tiempo, haga posible volver a crear el mismo entorno.

**Qué configurar**

- Compruebe qué falta según los síntomas (:doc:`guide-14`). Un OutOfMemoryError en ``fess-crawler.log`` indica falta de memoria en la JVM del rastreador (``jvm.crawler.options``), y no se soluciona aumentando el heap del propio Fess (``FESS_HEAP_SIZE``)
- Considere, en este orden: separar OpenSearch en otro servidor, convertirlo en un clúster de 3 nodos y ejecutar Fess en varios servidores (:doc:`guide-14`)
- Si ejecuta Fess en varios servidores, deje el rastreo a uno solo. Configure tanto ``scheduler.target.name`` como "Objetivo" en [Sistema] > [Programador] (:doc:`guide-14`)
- Con varios servidores, mantenga iguales en todos ellos ``app.cipher.key``, ``fess_config.properties``, los ajustes de [General] y los plugins
- Fije la etiqueta de la imagen Docker y las versiones de los plugins, y haga que los ajustes se puedan aplicar con fessctl y la API de administración (:doc:`guide-16`)
- Para que varias organizaciones compartan un mismo Fess, combine hosts virtuales y roles. Los hosts virtuales por sí solos no son un control de acceso (:doc:`guide-13`)

**Qué comprobar**

- Antes y después de ampliar, compare el uso del heap de ``/api/admin/stats`` y la duración del rastreo en [Información del sistema] > [Registro de trabajo] (:doc:`guide-10`)
- Con varios servidores, se obtienen los mismos resultados de búsqueda desde cualquier servidor, y el rastreo solo se ejecuta en el servidor asignado. Hacer clic en [Iniciar ahora] en otro servidor no lo ejecuta (:doc:`guide-14`)
- Se pueden restaurar los ajustes desde una copia de seguridad en un entorno recreado (:doc:`guide-10`)

**Se puede avanzar cuando**

- En la pestaña [Rendimiento] de [Registro de búsqueda], la mediana, el p95 y el p99 del tiempo de respuesta son menores que antes de la ampliación, o no han subido aunque aumenten los usuarios
- Busque los términos que aparecen en "Consultas más lentas" para distinguir si solo son lentos ciertos términos o si todo es lento

Por cierto, la función para guardar las sesiones de inicio de sesión en OpenSearch y compartirlas entre varios servidores está disponible a partir de 15.10.
En 15.9, se opera con las sesiones persistentes mencionadas antes.

Etapa 7: funciones de IA
========================

Cada función de IA necesita una preparación distinta.
Añada primero las que se ajusten a su objetivo.

**Modo de búsqueda con IA (RAG)**

- Un LLM responde a las preguntas de los usuarios basándose en documentos internos (:doc:`guide-19`)
- No hace falta búsqueda vectorial. Los documentos de respaldo se reúnen con una búsqueda normal, por lo que los permisos de las etapas 2 y 3 se aplican tal cual, y los documentos que un usuario no puede ver no se usan en la respuesta
- Se necesitan tres cosas: ``rag.chat.enabled=true`` en ``fess_config.properties`` (el valor predeterminado es ``false`` y no hay opción para ello en la consola de administración), un plugin ``fess-llm-*`` y "Proveedor de LLM" en [General]
- Puede restringir qué usuarios lo usan con "Permisos del chat" en [General]

**Búsqueda semántica y búsqueda multimodal**

- La búsqueda semántica encuentra documentos de significado cercano aunque no coincidan las palabras clave (:doc:`guide-18`). El proveedor de embeddings se elige con ``content_chunker.embedding.name``. El valor predeterminado ``opensearch`` usa un modelo de ML Commons de OpenSearch, mientras que ``ollama``, ``openai``, ``gemini`` y ``bedrock`` requieren el plugin ``fess-llm-*`` correspondiente
- Para habilitarla en un entorno existente, vuelva a crear el índice y después genere los vectores de todos los documentos. Con modelos de pago por uso como OpenAI, el primer procesamiento genera un coste por todos los documentos
- La búsqueda multimodal usa el plugin ``fess-webapp-multimodal`` y un servidor CLIP para buscar imágenes mediante texto (:doc:`guide-21`)
- Estas dos no se pueden usar a la vez en un mismo Fess. Si necesita ambas, construya instancias de Fess separadas

**MCP**

- Permite que los agentes de IA busquen en Fess (:doc:`guide-20`). Al instalar el plugin ``fess-webapp-mcp`` queda disponible ``/mcp``
- Con el valor predeterminado ``mcp.auth.mode=none``, cualquiera que llegue a ``/mcp`` puede buscar como invitado. Antes de abrirlo dentro de la empresa, cambie el ajuste para que se autentique con tokens de acceso u otro método

**Qué comprobar**

- Modo de búsqueda con IA: al preguntar con [Búsqueda IA] en la página de búsqueda, se muestran la respuesta y sus fuentes. Con usuarios de permisos distintos, los documentos que no pueden ver no aparecen entre las fuentes (:doc:`guide-19`)
- Búsqueda semántica y búsqueda multimodal: se escriben vectores en los documentos, y la respuesta de la API de búsqueda muestra que se usa la búsqueda vectorial (:doc:`guide-18`, :doc:`guide-21`)
- MCP: tras cambiar el ajuste de autenticación, se rechazan las llamadas sin token (:doc:`guide-20`)

**Se puede avanzar cuando**

- Para el modo de búsqueda con IA, mire en la pestaña [Chat con IA] de [Registro de búsqueda] las solicitudes, los usuarios, la tasa de errores y el tiempo de respuesta medio. El número de tokens solo se registra si el plugin de LLM lo informa, y el contenido de las preguntas y respuestas no se registra
- Para la búsqueda semántica, habilite "Comparar con el período anterior" en un período que empiece el día siguiente a la implantación, y compare la tasa de cero resultados, la tasa de clics y los tiempos de respuesta de la pestaña [Rendimiento]
- MCP y la búsqueda multimodal no tienen indicadores propios en [Registro de búsqueda]. Júzguelos con el apartado "Qué comprobar" anterior y con los comentarios de los departamentos que los usan

Artículos relacionados
======================

- Empezar la prueba: :doc:`guide-02`
- Publicar la primera fuente con permisos: :doc:`guide-04`, :doc:`guide-05`, :doc:`file-server-search`
- Supervisión y copias de seguridad: :doc:`guide-10`
- SSO: :doc:`guide-15`
- Añadir fuentes: :doc:`datastore-basics`
- Mejorar la calidad con el registro de búsqueda: :doc:`guide-08`
- Ampliación y configuración como código: :doc:`guide-14`, :doc:`guide-16`
- Funciones de IA: :doc:`guide-19`, :doc:`guide-18`, :doc:`guide-20`

Referencias
===========

- `Registro de búsqueda <https://fess.codelibs.org/es/stable/admin/searchlog-guide.html>`__
- `General <https://fess.codelibs.org/es/stable/admin/general-guide.html>`__
- `Complemento <https://fess.codelibs.org/es/stable/admin/plugin-guide.html>`__
- `Requisitos del sistema <https://fess.codelibs.org/es/stable/install/prerequisites.html>`__
- `Foro de discusión de Fess <https://discuss.codelibs.org/c/FessEN/>`__
