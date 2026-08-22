================
Hôtes virtuels
================

À propos des hôtes virtuels
============================

|Fess| peut différencier les résultats de recherche en fonction du nom d'hôte (valeur de l'en-tête HTTP ``Host``) lors de l'accès.
Il est possible de publier un seul serveur |Fess| sous plusieurs noms d'hôte et de fournir des cibles de recherche (configurations d'exploration) et des designs de page différents pour chaque nom d'hôte.
Les résultats de recherche étant affichés via des JSP propres à chaque hôte virtuel, il est également possible de personnaliser le design.

La fonctionnalité d'hôte virtuel est désactivée par défaut (non configurée). Suivez les étapes ci-dessous pour la configurer.

Configuration système
---------------------

Configurez la correspondance entre le nom d'hôte de l'accédant et le nom d'hôte virtuel dans « Hôte virtuel » de :doc:`Guide administrateur > Configuration générale <../admin/general-guide>`. Spécifiez le nom d'hôte virtuel configuré ici dans la configuration de l'exploration.

**Format**

Décrivez un hôte virtuel par ligne selon le format suivant.

::

   nom_en-tête:valeur_en-tête=nom_hôte_virtuel

.. list-table::

   * - *nom_en-tête*
     - Nom de l'en-tête de requête HTTP utilisé pour la correspondance. En général, spécifiez ``Host``. Dans le cas d'un accès via un proxy inverse, vous pouvez également spécifier ``X-Forwarded-Host``.
   * - *valeur_en-tête*
     - Nom d'hôte (et si nécessaire, au format ``nom_hôte:numéro_port``) contenu dans l'en-tête ci-dessus. L'hôte virtuel est appliqué en cas de correspondance exacte (insensible à la casse) avec la valeur de l'en-tête envoyée par le client lors de l'accès.
   * - *nom_hôte_virtuel*
     - Nom d'hôte virtuel à spécifier dans la configuration de l'exploration

**Exemple**

::

   Host:abc.example.com=host1
   Host:192.168.1.123:8080=host2

.. note::

   La correspondance est effectuée par comparaison de chaînes de caractères avec la valeur de l'en-tête de requête, et non par résolution de nom d'hôte (DNS).
   L'en-tête ``Host`` envoyé par le navigateur ne contient pas le numéro de port lorsque l'accès se fait sur un port standard (80 pour HTTP, 443 pour HTTPS) ; pour tout autre port, le numéro de port est inclus au format ``nom_hôte:numéro_port``.
   Par conséquent, si vous publiez sur un port non standard, spécifiez le numéro de port explicitement, par exemple ``Host:abc.example.com:8080=host1``.

.. note::

   Seuls les caractères alphanumériques et les tirets bas ( ``a-z`` , ``A-Z`` , ``0-9`` , ``_`` ) peuvent être utilisés dans les noms d'hôtes virtuels.
   Les autres caractères sont automatiquement supprimés.

   De plus, les noms suivants sont réservés et ne peuvent pas être utilisés comme noms d'hôtes virtuels :
   ``admin`` , ``common`` , ``error`` , ``login`` , ``profile``

Lorsque la configuration est enregistrée, des JSP de page de recherche sont générés dans ``WEB-INF/view/nom_hôte_virtuel``.
En les modifiant, il est possible de changer le design de page pour chaque hôte virtuel. Les JSP peuvent également être modifiés depuis l'écran :doc:`Guide administrateur > Design <../admin/design-guide>`.


Configuration de l'exploration
-------------------------------

Spécifiez « Hôte virtuel » dans l'une des configurations suivantes : configuration de l'exploration Web, configuration de l'exploration de fichiers ou configuration de l'exploration de banques de données.
« Hôte virtuel » spécifie l'un des noms d'hôtes virtuels configurés dans la configuration système. Il est également possible de spécifier plusieurs hôtes virtuels pour une même configuration d'exploration (un par ligne).

Pour une recherche effectuée depuis un hôte virtuel, seuls les documents de la configuration d'exploration pour laquelle cet hôte virtuel est spécifié apparaissent dans les résultats de recherche.
Pour un accès ne correspondant à aucun hôte virtuel (accès normal sans hôte virtuel configuré), aucun filtrage n'est appliqué et tous les résultats de recherche sont affichés normalement.

**Exemple**

.. list-table::

   * - *Hôte virtuel*
     - ``host1``
