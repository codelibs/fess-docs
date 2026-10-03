==================================
Configuration de l'OCR
==================================

Aperçu
======

|Fess| extrait le texte des documents avec Apache Tika.
L'analyseur OCR Tesseract de Tika est fourni avec |Fess|. Une fois activé, |Fess| reconnaît le texte des images et des PDF numérisés et le rend consultable par la recherche.

L'OCR s'exécute lorsque les deux conditions suivantes sont réunies :

- La commande ``tesseract`` est installée sur l'hôte où s'exécute le processus du crawler de |Fess|
- L'OCR est activé dans |Fess|

L'OCR est désactivé par défaut.
Si ``tesseract`` n'est pas installé, |Fess| ignore l'OCR. Aucune erreur ne se produit.

Éléments concernés par l'OCR
============================

Lorsque l'OCR est activé, il s'applique aux éléments suivants :

- Les fichiers image (PNG, JPEG, TIFF, GIF, BMP, etc.)
- Les images intégrées dans des documents traités par Tika (par exemple, les fichiers Office)
- Les PDF dont la couche de texte est vide (PDF numérisés)

Traitement des PDF numérisés
----------------------------

|Fess| extrait normalement le texte des PDF avec PDFBox.
Lorsque l'OCR est activé et que PDFBox n'obtient aucun texte d'un PDF, |Fess| extrait de nouveau le PDF via Tika.
Tika convertit les pages en images et leur applique l'OCR.

.. note::
   Les PDF qui contiennent déjà du texte ne sont pas traités par l'OCR.
   Les PDF mixtes, dont seules certaines pages sont des images numérisées, ne sont pas couverts.

Installation de Tesseract
=========================

Installez Tesseract sur l'hôte où s'exécute |Fess|.
Pour reconnaître le texte japonais, vous avez aussi besoin des données d'entraînement japonaises (traineddata).

Debian / Ubuntu ::

    $ sudo apt-get install tesseract-ocr tesseract-ocr-jpn

RHEL / Rocky Linux / AlmaLinux (activez d'abord EPEL) ::

    $ sudo dnf install tesseract tesseract-langpack-jpn

Pour vérifier les langues installées, exécutez ::

    $ tesseract --list-langs

Activation de l'OCR
===================

Définissez les propriétés suivantes dans ``fess_config.properties``.

- Paquet ZIP : ``app/WEB-INF/classes/fess_config.properties``
- Paquet RPM/DEB : ``/etc/fess/fess_config.properties``

::

    # Activer l'OCR (par défaut : false)
    crawler.document.ocr.enabled=true

    # Langue(s) de Tesseract, reliées par + (par défaut : eng)
    crawler.document.ocr.language=jpn+eng

    # Délai d'expiration en secondes pour une exécution de Tesseract (par défaut : 120)
    crawler.document.ocr.timeout=120

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Propriété
     - Par défaut
     - Description
   * - ``crawler.document.ocr.enabled``
     - ``false``
     - Définissez ``true`` pour activer l'OCR.
   * - ``crawler.document.ocr.language``
     - ``eng``
     - Langue(s) de Tesseract. Reliez plusieurs langues avec ``+`` (par exemple, ``jpn+eng``). Les données d'entraînement (traineddata) correspondantes doivent être installées.
   * - ``crawler.document.ocr.timeout``
     - ``120``
     - Délai d'expiration d'une exécution de Tesseract (une image ou une page de PDF), en secondes.

Vous pouvez aussi définir ces propriétés comme propriétés système de la JVM.
Par exemple, indiquez-les dans ``FESS_JAVA_OPTS``. C'est pratique dans les environnements Docker.

::

    -Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng

.. note::
   Redémarrez |Fess| après avoir modifié ces paramètres.

Utiliser l'OCR avec Docker
==========================

Pour utiliser l'OCR dans un environnement Docker, ajoutez Tesseract à l'image de |Fess|.
Construisez une image avec Tesseract à l'aide de ``compose/tesseract/Dockerfile`` de `docker-fess <https://github.com/codelibs/docker-fess>`__.

Exemple de ``compose/tesseract/Dockerfile`` ::

    FROM ghcr.io/codelibs/fess:15.9.0

    RUN apk add --no-cache tesseract-ocr tesseract-ocr-data-osd tesseract-ocr-data-eng tesseract-ocr-data-jpn

Dans ``compose/compose.yaml``, remplacez la ligne ``image:`` par ``build: ./tesseract`` et activez la ligne ``FESS_JAVA_OPTS``.
Cela fonctionne comme ``build: ./playwright``.

::

    services:
      fess01:
        # image: ghcr.io/codelibs/fess:15.9.0
        build: ./tesseract
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng"

Après la modification, reconstruisez l'image et démarrez les conteneurs ::

    $ docker compose up -d --build

.. note::
   Si vous utilisez une image de base qui n'est pas Alpine, comme ``-noble`` ou ``-al2023``, ajoutez Tesseract avec le gestionnaire de paquets de cette distribution à la place de ``apk``.

Consultez :doc:`../install/install-docker` pour plus de détails.

Paramètres par configuration de crawl
=====================================

Si vous indiquez ``config.tika.tesseract.config`` dans les « Paramètres de configuration » d'une configuration de crawl, vous pouvez remplacer les paramètres d'OCR pour cette seule configuration de crawl.

::

    config.tika.tesseract.config=tesseract.properties

``tesseract.properties`` est un nom de ressource du classpath, et non un chemin du système de fichiers.
Placez le fichier dans le répertoire de configuration de |Fess|, qui se trouve dans le classpath du crawler.

- Paquet ZIP : ``app/WEB-INF/classes/``
- Paquet RPM/DEB : ``/etc/fess/``

Dans ``tesseract.properties``, écrivez des propriétés de ``TesseractOCRConfig`` de Tika.
Seules les clés simples, telles que ``language`` et ``timeoutSeconds``, sont appliquées de manière fiable.

::

    language=jpn
    timeoutSeconds=300

Pour cette configuration de crawl, ces valeurs ont priorité sur les paramètres globaux décrits ci-dessus.

Remarques d'exploitation
========================

- L'OCR sollicite fortement le processeur et ralentit considérablement le crawl. Envisagez de réduire le nombre de threads du crawler ou de n'activer l'OCR que pour les configurations de crawl qui en ont besoin.
- Pour les nouvelles configurations de crawl Web, le motif d'URL exclues par défaut exclut les URL d'images (jpg, png, gif, etc.). Pour explorer les images d'un site Web, supprimez-les de « URL exclues du crawl ». Le crawl de fichiers inclut les images.
- Les limites de taille du crawler s'appliquent également. Pour la limite de taille d'indexation par type de fichier (par défaut : 10 Mo), consultez :doc:`crawler-basic`.
- La précision de l'OCR dépend de la qualité de la numérisation. L'écriture manuscrite n'est en général pas bien reconnue.
- Les fichiers indexés avant l'activation de l'OCR ne sont pas traités par l'OCR tels quels. Avec le crawl incrémental activé (« Vérifier la dernière modification » dans :doc:`../admin/general-guide`), un fichier dont la date de modification n'a pas changé n'est pas récupéré à nouveau lors d'un nouveau crawl. Pour appliquer l'OCR à ces fichiers, désactivez « Vérifier la dernière modification » le temps d'un crawl, ou supprimez les documents de l'index puis relancez le crawl.

Remarques sur la mise à niveau
==============================

Jusqu'à la version 15.8, le fichier ``tika.xml`` fourni excluait ``org.apache.tika.parser.ocr.TesseractOCRParser``.
Depuis la version 15.9, le fichier ``tika.xml`` fourni n'exclut plus cet analyseur.

Si vous avez conservé un fichier ``tika.xml`` personnalisé, supprimez la ligne suivante :

::

    <parser-exclude class="org.apache.tika.parser.ocr.TesseractOCRParser"/>

Si cette ligne reste en place, l'OCR reste désactivé même avec ``crawler.document.ocr.enabled=true``.

L'emplacement de ``tika.xml`` est le suivant :

- Paquet ZIP : ``app/WEB-INF/conf/tika.xml``
- Paquet RPM/DEB : ``/etc/fess/tika.xml``

Vérification de l'OCR
=====================

1. Créez une configuration de crawl de fichiers pour un dossier contenant une image numérisée (une image comportant du texte).
2. Lancez le crawl.
3. Recherchez un mot qui figure dans l'image et vérifiez que l'image apparaît dans les résultats de recherche.

Si l'image n'apparaît pas, vérifiez les points suivants :

- ``tesseract --list-langs`` affiche la langue utilisée
- ``crawler.document.ocr.enabled`` vaut ``true``
- ``tika.xml`` n'exclut plus ``TesseractOCRParser``
- Le ``fess-crawler.log`` du crawl affiche ``OCR is enabled`` (l'avertissement ``Tesseract OCR is not available`` signifie que |Fess| ne peut pas utiliser Tesseract)
