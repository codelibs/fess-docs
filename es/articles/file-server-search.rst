==============================================
Búsqueda open source en servidores de archivos
==============================================

Introducción
============

A medida que cada departamento añade servidores de archivos, ya nadie sabe dónde está un documento concreto. La búsqueda de Windows trabaja sobre una carpeta compartida cada vez y no cruza la frontera entre servidores, y la búsqueda de texto completo de un NAS termina en la propia caja.

Una salida es poner un servidor de búsqueda de texto completo delante de los servidores de archivos. Esta página reúne lo que conviene comprobar antes de dar ese papel a Fess, un servidor de búsqueda de texto completo de código abierto.

A quién va dirigida
===================

- A quienes tienen dificultades para buscar en un servidor de archivos interno o un NAS
- A quienes evalúan la búsqueda de texto completo y se preguntan si el código abierto basta
- A quienes quieren añadir búsqueda sin alterar los permisos de acceso existentes

Fess se publica bajo la licencia Apache 2.0 y no conlleva coste de licencia.

Dónde pueden estar los archivos
===============================

El rastreador de archivos de Fess habla los siguientes protocolos. Se configuran en la interfaz de administración en [Rastreador] > [Sistema de archivos], como URL de inicio del rastreo.

.. list-table:: Protocolos admitidos
   :header-rows: 1
   :widths: 12 33 55

   * - Protocolo
     - Forma de la URL
     - Uso habitual
   * - ``file``
     - ``file:///home/share/documents/``
     - Un directorio de la máquina que ejecuta Fess, incluido un NAS ya montado
   * - ``smb``
     - ``smb://fileserver.example.com/share/``
     - Recursos compartidos de Windows, desde SMB 2.0.2 hasta SMB 3.1.1
   * - ``smb1``
     - ``smb1://fileserver.example.com/share/``
     - Equipos antiguos que solo hablan SMB1/CIFS
   * - ``ftp``
     - ``ftp://fileserver.example.com/pub/``
     - Servidores FTP
   * - ``s3``
     - ``s3://bucket-name/prefix/``
     - Amazon S3 y almacenamiento de objetos compatible con S3
   * - ``gcs``
     - ``gcs://bucket-name/prefix/``
     - Google Cloud Storage

El conjunto activo se define en ``crawler.file.protocols``, cuyo valor predeterminado es ``file,smb,smb1,ftp,s3,gcs``.

Para los recursos compartidos de Windows lo normal es ``smb``. ``smb1`` se conserva para NAS y servidores de impresión antiguos que no hablan nada más; SMB1 está desactivado de forma predeterminada en Windows por motivos de seguridad, así que no es una opción para una instalación nueva.

Los permisos de acceso existentes se heredan
============================================

La mayor preocupación al poner una búsqueda delante de un servidor de archivos es que aparezcan en los resultados documentos que alguien no debería ver. Si las carpetas de recursos humanos y de contabilidad salen para todo el mundo, el sistema de búsqueda es inservible por bueno que sea el orden de los resultados.

Fess resuelve esto **llevando a la búsqueda los propios permisos de acceso del servidor de archivos**.

Cómo funciona
-------------

1. Durante el rastreo, Fess lee la lista de control de acceso (ACL) de cada archivo
2. Las cuentas y los grupos permitidos o denegados se registran como roles de ese documento
3. Al buscar, esos roles se comparan con los del usuario que ha iniciado sesión y solo vuelven los documentos permitidos

Se tratan tanto el permiso como la denegación, distinguidos internamente por los prefijos ``(allow)`` y ``(deny)``. La lectura de roles desde la ACL está activada de forma predeterminada.

.. list-table:: Ajustes que rigen la herencia de permisos
   :header-rows: 1
   :widths: 38 14 48

   * - Ajuste
     - Predeterminado
     - Efecto
   * - ``smb.role.from.file``
     - ``true``
     - Toma los roles de la ACL de los archivos rastreados por SMB
   * - ``file.role.from.file``
     - ``true``
     - Toma los roles de los permisos del sistema de archivos local
   * - ``ftp.role.from.file``
     - ``true``
     - Toma los roles de los archivos rastreados por FTP
   * - ``smb.available.sid.types``
     - ``1,2,4:2,5:1``
     - Qué tipos de SID se convierten en roles; ajusta el trato de usuarios y grupos

El requisito que conviene comprobar primero
-------------------------------------------

Para que la cadena funcione de extremo a extremo, **quien busca debe llevar los mismos roles**. El documento registra «este grupo puede leerme»; mientras el usuario que busca no pueda decirle a Fess a qué grupos pertenece, no hay nada que comparar.

Por eso la **integración con Active Directory o LDAP es un requisito** para una búsqueda que respete los permisos: Fess autentica a los usuarios contra el mismo directorio que ya usa el servidor de archivos.

En cambio, si solo se indexan carpetas compartidas que toda la empresa puede leer, la integración no hace falta. Esa distinción suele decidir el alcance de un primer despliegue.

Qué formatos de archivo se leen
===============================

Fess extrae el texto del contenido de los archivos con Apache Tika, de modo que se puede buscar en el cuerpo del documento y no solo en su nombre. Eso es lo que permite encontrar un documento cuyo título ya nadie recuerda.

Los formatos principales son:

- MS Office (doc, xls, ppt, docx, xlsx, pptx, entre otros)
- PDF
- Texto plano, HTML, XML
- Texto enriquecido (rtf)
- Código fuente (js, c, h, java, entre otros)
- Archivos comprimidos (gz, tar, zip, entre otros; el contenido se expande y también se indexa)

La lista completa está en `Archivos Objetivo de Búsqueda <https://fess.codelibs.org/es/supported-files.html>`__.

Los archivos que no contienen texto alguno, como los documentos escaneados y los PDF formados solo por imágenes, no se pueden leer por esta vía. Conviene decidir si hace falta OCR mirando antes qué hay realmente en las carpetas de destino.

Dimensionamiento y arquitectura
===============================

Fess guarda su índice en OpenSearch. Una instalación pequeña funciona sin problema con Fess y OpenSearch en la misma máquina, y OpenSearch se puede separar en un clúster cuando el volumen crece.

Para dimensionar, el número de archivos por sí solo es mala guía. Estos tres puntos pesan más:

- El tamaño total de las carpetas de destino y qué parte contiene realmente texto
- Con qué frecuencia cambia el contenido, a diario o al mes, lo que determina la planificación del rastreo
- El tamaño de cada archivo, ya que los muy grandes se pueden excluir del rastreo por configuración

Cómo empezar
============

1. **Ponerlo en marcha primero** — seguir la `Guía de Configuración Rápida <https://fess.codelibs.org/es/quick-start.html>`__. Con Docker Compose se obtiene algo consultable en pocos minutos
2. **Crear una configuración de rastreo** — registrar la URL de destino y el intervalo en [Rastreador] > [Sistema de archivos]
3. **Registrar las credenciales** — dar de alta la cuenta de acceso al recurso compartido en [Rastreador] > [Autenticación de archivos]
4. **Diseñar roles y etiquetas** — etiquetas para filtrar por departamento, roles para resultados según permisos

Hay un ejemplo desarrollado en `Parte 4: Buscar archivos dispersos de forma centralizada <https://fess.codelibs.org/es/articles/guide-04.html>`__, que construye un único cuadro de búsqueda sobre varios servidores de archivos y un sitio de intranet.

Resumen
=======

- Fess es un servidor de búsqueda de código abierto capaz de indexar servidores de archivos por SMB/CIFS, FTP, rutas locales, S3 y GCS
- En los archivos rastreados por SMB, los permisos registrados en la ACL filtran los resultados, y esto viene activado de fábrica
- La búsqueda que respeta los permisos exige integración con Active Directory o LDAP
- Apache Tika hace consultable el cuerpo de los documentos de Office y los PDF
- Empezar en pequeño y crecer separando OpenSearch en un clúster

Referencias
===========

- `Configuración del Rastreador: Rastreo Web, de Servidores de Archivos y de Bases de Datos <https://fess.codelibs.org/es/stable/config/crawler-basic.html>`__
- `Control de acceso mediante roles <https://fess.codelibs.org/es/stable/config/security-role.html>`__
- `Archivos Objetivo de Búsqueda <https://fess.codelibs.org/es/supported-files.html>`__
- `Guía de Configuración Rápida <https://fess.codelibs.org/es/quick-start.html>`__
- `Guía de administración <https://fess.codelibs.org/es/stable/admin/index.html>`__
