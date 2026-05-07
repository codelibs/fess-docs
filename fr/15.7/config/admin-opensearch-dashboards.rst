===================================
Configuration de la visualisation des journaux de recherche
===================================

À propos de la visualisation des journaux de recherche
========================

|Fess| collecte les journaux de recherche et de clics des utilisateurs.
Les journaux de recherche collectés peuvent être analysés et visualisés à l'aide d'`OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__.

Informations pouvant être visualisées
----------------

Avec la configuration par défaut, les informations suivantes peuvent être visualisées.

-  Temps moyen pour afficher les résultats de recherche
-  Nombre de recherches par seconde
-  Classement des User Agent des utilisateurs accédant
-  Classement des mots-clés de recherche
-  Classement des mots-clés de recherche avec 0 résultat
-  Nombre total de résultats de recherche
-  Tendances de recherche dans le temps

En utilisant la fonction Visualize pour créer de nouveaux graphiques et les ajouter au Dashboard, vous pouvez construire votre propre tableau de bord de surveillance.

Configuration de la visualisation des données avec OpenSearch Dashboards
==============================================

Installation d'OpenSearch Dashboards
------------------------------------

OpenSearch Dashboards est un outil de visualisation des données d'OpenSearch utilisé par |Fess|.
Installez OpenSearch Dashboards en suivant la `documentation officielle d'OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__.

Modification du fichier de configuration
------------------

Pour permettre à OpenSearch Dashboards de reconnaître OpenSearch utilisé par |Fess|, modifiez le fichier de configuration ``config/opensearch_dashboards.yml``.

::

    opensearch.hosts: ["http://localhost:9201"]

Remplacez ``localhost`` par le nom d'hôte ou l'adresse IP appropriée selon votre environnement.
Dans la configuration par défaut de |Fess|, OpenSearch démarre sur le port 9201.

.. note::
   Si le numéro de port d'OpenSearch est différent, modifiez-le avec le numéro de port approprié.

Démarrage d'OpenSearch Dashboards
-----------------------------

Après avoir modifié le fichier de configuration, démarrez OpenSearch Dashboards.

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

Après le démarrage, accédez à ``http://localhost:5601`` dans votre navigateur.

Configuration du modèle d'index
--------------------------

1. Sélectionnez le menu « Management » depuis l'écran d'accueil d'OpenSearch Dashboards.
2. Sélectionnez « Index Patterns ».
3. Cliquez sur le bouton « Create index pattern ».
4. Entrez ``fess_log*`` dans Index pattern name.
5. Cliquez sur le bouton « Next step ».
6. Sélectionnez ``requestedAt`` dans Time field.
7. Cliquez sur le bouton « Create index pattern ».

Vous êtes maintenant prêt à visualiser les journaux de recherche de |Fess|.

Création de visualisations et de tableaux de bord
----------------------------

Création de visualisations de base
~~~~~~~~~~~~~~~~~~~~

1. Sélectionnez « Visualize » dans le menu de gauche.
2. Cliquez sur le bouton « Create visualization ».
3. Sélectionnez le type de visualisation (graphique linéaire, graphique circulaire, graphique à barres, etc.).
4. Sélectionnez le modèle d'index ``fess_log*`` que vous avez créé.
5. Configurez les métriques et les buckets (unités d'agrégation) nécessaires.
6. Cliquez sur le bouton « Save » pour enregistrer la visualisation.

Création de tableaux de bord
~~~~~~~~~~~~~~~~~~~~

1. Sélectionnez « Dashboard » dans le menu de gauche.
2. Cliquez sur le bouton « Create dashboard ».
3. Cliquez sur le bouton « Add » pour ajouter les visualisations que vous avez créées.
4. Ajustez la mise en page et cliquez sur le bouton « Save » pour enregistrer.

Configuration du fuseau horaire
------------------

Si l'affichage de l'heure n'est pas correct, configurez le fuseau horaire.

1. Sélectionnez « Management » dans le menu de gauche.
2. Sélectionnez « Advanced Settings ».
3. Recherchez ``dateFormat:tz``.
4. Définissez le fuseau horaire sur une valeur appropriée (par exemple : ``Asia/Tokyo`` ou ``UTC``).
5. Cliquez sur le bouton « Save ».

Vérification des données de journal
----------------

1. Sélectionnez « Discover » dans le menu de gauche.
2. Sélectionnez le modèle d'index ``fess_log*``.
3. Les données du journal de recherche s'affichent.
4. Vous pouvez spécifier la période à afficher avec la sélection de plage de temps en haut à droite.

Principaux champs de journal de recherche
----------------------

Les journaux de recherche de |Fess| contiennent les informations suivantes.

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
     - Temps de réponse des résultats de recherche (millisecondes)
   * - ``queryTime``
     - Temps d'exécution de la requête (millisecondes)
   * - ``hitCount``
     - Nombre de résultats trouvés
   * - ``userAgent``
     - Informations du navigateur de l'utilisateur
   * - ``clientIp``
     - Adresse IP du client
   * - ``languages``
     - Langue utilisée
   * - ``roles``
     - Informations de rôle de l'utilisateur
   * - ``user``
     - Nom d'utilisateur (lors de la connexion)

En utilisant ces champs, vous pouvez analyser les journaux de recherche sous différents angles.

Dépannage
----------------------

Si les données ne s'affichent pas
~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez qu'OpenSearch fonctionne correctement.
- Vérifiez que la configuration ``opensearch.hosts`` dans ``opensearch_dashboards.yml`` est correcte.
- Vérifiez que des recherches ont été effectuées dans |Fess| et que les journaux sont enregistrés.
- Vérifiez que la plage de temps du modèle d'index est configurée de manière appropriée.

En cas d'erreur de connexion
~~~~~~~~~~~~~~~~~~~~~~~~

- Vérifiez que le numéro de port d'OpenSearch est correct.
- Vérifiez la configuration du pare-feu ou des groupes de sécurité.
- Vérifiez qu'il n'y a pas d'erreurs dans les fichiers journaux d'OpenSearch.
