========
Hôtes virtuels
========

À propos des hôtes virtuels
==============

|Fess| peut différencier les résultats de recherche en fonction du nom d'hôte (partie hôte de l'URL) lors de l'accès.
Comme les résultats de recherche sont affichés dans leurs JSP respectifs, il est également possible de modifier le design.

Configuration système
----------

Configurez « Hôte virtuel » dans :doc:`Guide administrateur > Configuration générale <../admin/general-guide>`. Spécifiez le nom d'hôte virtuel configuré ici dans la configuration de l'exploration.

**Format**

::

   Host:nom_hôte[:numéro_port]=nom_hôte_virtuel

.. list-table::

   * - *nom_hôte*
     - Nom d'hôte ou adresse IP résolvable (DNS) par le système
   * - *numéro_port*
     - Optionnel. Par défaut 80.
   * - *nom_hôte_virtuel*
     - Nom d'hôte virtuel à spécifier dans la configuration de l'exploration

**Exemple**

::

   Host:abc.example.com:8080=host1
   Host:192.168.1.123:8080=host2

Une fois la configuration effectuée, les JSP de la page de recherche sont générés dans ``WEB-INF/view/nom_hôte_virtuel``.
En les modifiant, il est également possible de changer le design de la page pour chaque hôte virtuel.


Configuration de l'exploration
---------

Spécifiez « Hôte virtuel » dans l'une des configurations suivantes : configuration de l'exploration Web, configuration de l'exploration de fichiers ou configuration de l'exploration de banques de données.
« Hôte virtuel » spécifie l'un des noms d'hôtes virtuels configurés dans la configuration système.

**Exemple**

.. list-table::

   * - *Hôte virtuel*
     - ``host1``
