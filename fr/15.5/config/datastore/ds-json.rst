==================================
Connecteur JSON
==================================

Apercu
====

Le connecteur JSON fournit la fonctionnalite permettant de recuperer des donnees
a partir de fichiers JSON ou d'API JSON et de les enregistrer dans l'index |Fess|.

Cette fonctionnalite necessite le plugin ``fess-ds-json``.

Prerequis
========

1. L'installation du plugin est requise
2. L'acces au fichier JSON ou a l'API est necessaire
3. La structure du JSON doit etre comprise

Installation du plugin
------------------------

Methode 1 : Placement direct du fichier JAR

::

    # Telecharger depuis Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Placement
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # ou
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2 : Installation depuis l'interface d'administration

1. Ouvrir "Systeme" -> "Plugins"
2. Telecharger le fichier JAR
3. Redemarrer |Fess|

Configuration
========

Configurez depuis l'interface d'administration via "Crawler" -> "Data Store" -> "Nouveau".

Configuration de base
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Element
     - Exemple
   * - Nom
     - Products JSON
   * - Nom du gestionnaire
     - JsonDataStore
   * - Active
     - Oui

Configuration des parametres
----------------

Fichier local :

::

    files=/path/to/data.json
    fileEncoding=UTF-8

Fichier HTTP :

::

    files=https://api.example.com/products.json
    fileEncoding=UTF-8

API REST (avec authentification) :

::

    files=https://api.example.com/v1/items
    fileEncoding=UTF-8

Fichiers multiples :

::

    files=/path/to/data1.json,https://api.example.com/data2.json
    fileEncoding=UTF-8

Liste des parametres
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``files``
     - Oui
     - Chemin du fichier JSON ou URL de l'API (plusieurs separes par des virgules)
   * - ``fileEncoding``
     - Non
     - Encodage des caracteres (par defaut : UTF-8)
