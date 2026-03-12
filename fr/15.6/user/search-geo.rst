==========================
Recherche géolocalisée
==========================

En ajoutant des informations de géolocalisation (latitude et longitude) à chaque document lors de la génération de l'index, il est possible d'effectuer une recherche utilisant les informations de géolocalisation.

Utilisation
-----------

Par défaut, les paramètres suivants sont disponibles.

.. list-table::

   * - geo.<fieldname>.point
     - Spécifiez la latitude et la longitude en degrés décimaux sous forme de type Double.
   * - geo.<fieldname>.distance
     - Spécifiez la distance du document en kilomètres. Exemple : 10km

Table : Paramètres de requête


