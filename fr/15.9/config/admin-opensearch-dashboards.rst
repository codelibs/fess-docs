===========================================================
Configuration de la visualisation des journaux de recherche
===========================================================

À propos de la visualisation des journaux de recherche
======================================================

|Fess| collecte les journaux de recherche et de clics des utilisateurs.
Les journaux de recherche collectés peuvent être analysés et visualisés à l'aide d'`OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__.

|Fess| inclut un fichier de définition de tableau de bord ``extension/kibana/fess_log.ndjson`` pour visualiser les journaux de recherche.
En important ce fichier dans OpenSearch Dashboards, vous pouvez utiliser immédiatement les tableaux de bord prédéfinis.

Informations pouvant être visualisées
--------------------------------------

En important la définition de tableau de bord incluse (``fess_log.ndjson``), le tableau de bord ``fess_log`` ainsi que les 6 visualisations suivantes sont enregistrés.

-  Temps de réponse moyen pour afficher les résultats de recherche (``average-response-time``)
-  Nombre de requêtes de recherche par unité de temps (``search-query-counts-per-sec``)
-  Classement des User Agent des utilisateurs accédant (``rank-of-UserAgent``)
-  Classement des mots-clés de recherche (``search-term-rank``)
-  Classement des mots-clés de recherche avec 0 résultat (``search-term-rank-of-no-results``)
-  Nombre moyen de résultats de recherche (``hit-counts``)

En plus de cela, vous pouvez créer de nouveaux graphiques à l'aide de la fonction Visualize et les ajouter au tableau de bord pour construire votre propre tableau de bord de surveillance.

Configuration de la visualisation des données avec OpenSearch Dashboards
========================================================================

Installation d'OpenSearch Dashboards
-------------------------------------

OpenSearch Dashboards est un outil de visualisation des données d'OpenSearch utilisé par |Fess|.
Installez OpenSearch Dashboards en suivant la `documentation officielle d'OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__.

Modification du fichier de configuration
-----------------------------------------

Pour permettre à OpenSearch Dashboards de reconnaître OpenSearch utilisé par |Fess|, modifiez le fichier de configuration ``config/opensearch_dashboards.yml``.

::

    opensearch.hosts: ["http://localhost:9201"]

Remplacez ``localhost`` par le nom d'hôte ou l'adresse IP appropriée selon votre environnement.
Dans la configuration par défaut de |Fess|, OpenSearch démarre sur le port 9201.

.. note::
   Si le numéro de port d'OpenSearch est différent, modifiez-le avec le numéro de port approprié.

Démarrage d'OpenSearch Dashboards
-----------------------------------

Après avoir modifié le fichier de configuration, démarrez OpenSearch Dashboards.

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

Après le démarrage, accédez à ``http://localhost:5601`` dans votre navigateur.

Configuration du modèle d'index
---------------------------------

Créez un modèle d'index pour visualiser les journaux de recherche.

1. Sélectionnez « Management » (ou « Dashboards Management » selon la version d'OpenSearch Dashboards) dans le menu de gauche.
2. Sélectionnez « Index Patterns ».
3. Cliquez sur le bouton « Create index pattern ».
4. Entrez ``fess_log*`` dans Index pattern name.
5. Cliquez sur le bouton « Next step ».
6. Sélectionnez ``requestedAt`` dans Time field.
7. Cliquez sur le bouton « Create index pattern ».

.. note::
   Les journaux de recherche de |Fess| sont enregistrés dans plusieurs index commençant par ``fess_log``, tels que ``fess_log.search_log`` pour les journaux de recherche et ``fess_log.click_log`` pour les journaux de clics.
   En spécifiant le modèle d'index ``fess_log*``, vous pouvez cibler tous ces index en même temps.

Import de la définition de tableau de bord
-------------------------------------------

En important la définition de tableau de bord incluse avec |Fess|, vous pouvez utiliser les visualisations et tableaux de bord prédéfinis.

1. Sélectionnez « Management » (ou « Dashboards Management » selon la version d'OpenSearch Dashboards) dans le menu de gauche.
2. Sélectionnez « Saved Objects ».
3. Cliquez sur « Import ».
4. Sélectionnez ``extension/kibana/fess_log.ndjson`` dans le répertoire d'installation de |Fess|.
5. Cliquez sur « Import » pour exécuter l'importation.

Une fois l'importation terminée, 6 visualisations et le tableau de bord ``fess_log`` sont enregistrés.

Affichage du tableau de bord
------------------------------

1. Sélectionnez « Dashboard » dans le menu de gauche.
2. Sélectionnez le tableau de bord ``fess_log``.
3. Les résultats de visualisation des journaux de recherche s'affichent.
4. Vous pouvez spécifier la période à afficher avec la sélection de plage de temps en haut à droite.

Création de visualisations personnalisées
------------------------------------------

En plus des tableaux de bord inclus, vous pouvez également créer vos propres visualisations et tableaux de bord.

Création de visualisations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Sélectionnez « Visualize » dans le menu de gauche.
2. Cliquez sur le bouton « Create visualization ».
3. Sélectionnez le type de visualisation (graphique linéaire, graphique circulaire, graphique à barres, etc.).
4. Sélectionnez le modèle d'index ``fess_log*`` que vous avez créé.
5. Configurez les métriques et les buckets (unités d'agrégation) nécessaires.
6. Cliquez sur le bouton « Save » pour enregistrer la visualisation.

Création de tableaux de bord
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Sélectionnez « Dashboard » dans le menu de gauche.
2. Cliquez sur le bouton « Create dashboard ».
3. Cliquez sur le bouton « Add » pour ajouter les visualisations que vous avez créées.
4. Ajustez la mise en page et cliquez sur le bouton « Save » pour enregistrer.

Configuration du fuseau horaire
---------------------------------

Si l'affichage de l'heure n'est pas correct, configurez le fuseau horaire.

1. Sélectionnez « Management » (ou « Dashboards Management » selon la version d'OpenSearch Dashboards) dans le menu de gauche.
2. Sélectionnez « Advanced Settings ».
3. Recherchez ``dateFormat:tz``.
4. Définissez le fuseau horaire sur une valeur appropriée (par exemple : ``Asia/Tokyo`` ou ``UTC``).
5. Cliquez sur le bouton « Save ».

Vérification des données de journal
-------------------------------------

1. Sélectionnez « Discover » dans le menu de gauche.
2. Sélectionnez le modèle d'index ``fess_log*``.
3. Les données du journal de recherche s'affichent.
4. Vous pouvez spécifier la période à afficher avec la sélection de plage de temps en haut à droite.

Principaux champs de journal de recherche
------------------------------------------

Les journaux de recherche de |Fess| (``fess_log.search_log``) contiennent les informations suivantes.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Nom du champ
     - Description
   * - ``queryId``
     - Identifiant unique de la requête de recherche
   * - ``searchWord``
     - Mot-clé de recherche
   * - ``requestedAt``
     - Date et heure d'exécution de la recherche
   * - ``responseTime``
     - Temps de réponse total du traitement de la recherche (millisecondes)
   * - ``queryTime``
     - Temps d'exécution de la requête vers le moteur de recherche (millisecondes)
   * - ``hitCount``
     - Nombre de résultats de recherche trouvés
   * - ``hitCountRelation``
     - Relation indiquant si le nombre de résultats est une valeur exacte ou une valeur minimale (``eq`` : nombre exact, ``gte`` : valeur spécifiée ou plus)
   * - ``queryOffset``
     - Position de départ pour la récupération des résultats de recherche
   * - ``queryPageSize``
     - Nombre de résultats affichés par page
   * - ``userAgent``
     - Informations du navigateur de l'utilisateur
   * - ``referer``
     - URL de la page référente depuis laquelle la recherche a été effectuée
   * - ``clientIp``
     - Adresse IP du client
   * - ``languages``
     - Langue utilisée dans la requête
   * - ``accessType``
     - Type d'accès (``web``, ``json``, ``gsa``, ``admin``, ``other``)
   * - ``roles``
     - Informations de rôle de l'utilisateur
   * - ``user``
     - Nom d'utilisateur (lors de la connexion)
   * - ``virtualHost``
     - Nom d'hôte virtuel (si configuré)

En utilisant ces champs, vous pouvez analyser les journaux de recherche sous différents angles.

Dépannage
----------

Si les données ne s'affichent pas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez qu'OpenSearch fonctionne correctement.
- Vérifiez que la configuration ``opensearch.hosts`` dans ``opensearch_dashboards.yml`` est correcte.
- Vérifiez que des recherches ont été effectuées dans |Fess| et que les journaux sont enregistrés.
- Vérifiez que la plage de temps en haut à droite est configurée pour inclure la période pendant laquelle les journaux ont été enregistrés.
- Si l'affichage de l'heure est décalé, vérifiez la configuration de ``dateFormat:tz``.

En cas d'erreur de connexion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que le numéro de port d'OpenSearch est correct.
- Vérifiez la configuration du pare-feu ou des groupes de sécurité.
- Vérifiez qu'il n'y a pas d'erreurs dans les fichiers journaux d'OpenSearch.
