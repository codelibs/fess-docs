========================
Période de support produit
========================

Les produits dont la date de fin de vie (EOL) est dépassée ne feront plus l'objet de maintenance ni de mises à jour.
CodeLibs Project recommande fortement de migrer vers une version prise en charge.
Cela vous permettra d'éviter que les services et le support nécessaires ne soient plus disponibles.
Les dernières versions peuvent être téléchargées depuis la `page de téléchargement <downloads.html>`__.

Si vous avez besoin de support pour un produit dont la date de fin de vie est dépassée, veuillez consulter le `support commercial <https://www.n2sm.net/products/n2search.html>`__.

.. warning::

   **Actions recommandées avant la fin du support**

   Avant la date de fin de support, veuillez planifier et exécuter les actions suivantes :

   1. **Créer des sauvegardes** : Sauvegardez les fichiers de configuration et les données d'index
   2. **Tester dans un environnement de pré-production** : Vérifiez le fonctionnement avec la nouvelle version avant la migration en production
   3. **Consulter les notes de version** : Vérifiez les changements incompatibles et les fonctionnalités obsolètes
   4. **Planifier le calendrier de migration** : Créez un plan tenant compte des exigences de temps d'arrêt

Chemin de mise à niveau
========================

Le tableau suivant indique le chemin de mise à niveau recommandé depuis votre version actuelle vers la dernière version.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Version actuelle
     - Chemin recommandé
     - Notes
   * - 15.x vers 15.5
     - Mise à niveau directe possible
     - Consultez le `Guide de mise à niveau <15.5/install/upgrade.html>`__
   * - 14.x vers 15.5
     - Mise à niveau directe possible
     - Portez attention aux modifications des fichiers de configuration
   * - 13.x vers 15.5
     - Via 14.x recommandé
     - Mettez à niveau dans l'ordre : 13.x vers 14.19 puis vers 15.5
   * - 12.x ou antérieur vers 15.5
     - Mise à niveau par étapes requise
     - Montez de 1 à 2 versions majeures à la fois

.. note::

   Pour les procédures de mise à niveau détaillées, consultez le `Guide de mise à niveau <15.5/install/upgrade.html>`__.
   Pour les environnements à grande échelle ou les configurations complexes, nous recommandons de consulter le `support commercial <support-services.html>`__.

Ressources de migration
========================

Documents utiles pour la mise à niveau :

- `Guide de mise à niveau <15.5/install/upgrade.html>`__ - Étapes détaillées de la sauvegarde à la fin de la mise à niveau
- `Notes de version <https://github.com/codelibs/fess/releases>`__ - Modifications et notes pour chaque version
- `Dépannage <15.5/install/troubleshooting.html>`__ - Problèmes courants et solutions
- `Mise à niveau Docker <15.5/install/install-docker.html>`__ - Mise à niveau dans les environnements Docker

Tableau de maintenance
=======================

La date EOL de Fess est environ 18 mois après la date de sortie.

**Légende** :

- 🟢 **Pris en charge** : Les correctifs de sécurité et les corrections de bogues sont fournis
- 🟡 **Fin de support proche** : Le support se termine dans les 6 mois
- 🔴 **Fin de support** : Aucune maintenance n'est fournie

Versions actuellement prises en charge
----------------------------------------

.. tabularcolumns:: |p{3cm}|p{4cm}|p{3cm}|
.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Fess
     - Date EOL
     - Statut
   * - 15.6.x
     - 2027-10-01
     - 🟢 Dernière version (recommandée)
   * - 15.5.x
     - 2027-08-01
     - 🟢 Prise en charge
   * - 15.4.x
     - 2027-06-01
     - 🟢 Prise en charge
   * - 15.3.x
     - 2027-04-01
     - 🟢 Prise en charge
   * - 15.2.x
     - 2027-03-01
     - 🟢 Prise en charge
   * - 15.1.x
     - 2027-01-01
     - 🟢 Prise en charge
   * - 15.0.x
     - 2026-12-01
     - 🟢 Prise en charge
   * - 14.19.x
     - 2026-08-01
     - 🟡 Fin de support proche
   * - 14.18.x
     - 2026-05-01
     - 🟡 Fin de support proche

Versions en fin de vie
------------------------

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Fess
     - Date EOL
   * - 14.17.x
     - 2026-03-01
   * - 14.16.x
     - 2026-02-01
   * - 14.15.x
     - 2026-01-01
   * - 14.14.x
     - 2025-11-01
   * - 14.13.x
     - 2025-10-01
   * - 14.12.x
     - 2025-08-01
   * - 14.11.x
     - 2025-04-01
   * - 14.10.x
     - 2025-01-01
   * - 14.9.x
     - 2024-12-01
   * - 14.8.x
     - 2024-11-01
   * - 14.7.x
     - 2024-09-01
   * - 14.6.x
     - 2024-07-01
   * - 14.5.x
     - 2024-05-01
   * - 14.4.x
     - 2024-02-24
   * - 14.3.x
     - 2023-12-28
   * - 14.2.x
     - 2023-10-26
   * - 14.1.x
     - 2023-09-08
   * - 14.0.x
     - 2023-08-08
   * - 13.16.x
     - 2023-06-07
   * - 13.15.x
     - 2023-03-22
   * - 13.14.x
     - 2023-02-03
   * - 13.13.x
     - 2022-11-25
   * - 13.12.x
     - 2022-09-23
   * - 13.11.x
     - 2022-08-10
   * - 13.10.x
     - 2022-05-11
   * - 13.9.x
     - 2022-02-18
   * - 13.8.x
     - 2021-12-18
   * - 13.7.x
     - 2021-11-13
   * - 13.6.x
     - 2021-08-11
   * - 13.5.x
     - 2021-06-02
   * - 13.4.x
     - 2021-04-01
   * - 13.3.x
     - 2021-01-31
   * - 13.2.x
     - 2020-12-25
   * - 13.1.x
     - 2020-11-20
   * - 13.0.x
     - 2020-10-10
   * - 12.7.x
     - 2020-11-20
   * - 12.6.x
     - 2020-09-26
   * - 12.5.x
     - 2020-07-29
   * - 12.4.x
     - 2020-05-14
   * - 12.3.x
     - 2020-02-23
   * - 12.2.x
     - 2020-12-13
   * - 12.1.x
     - 2019-08-19
   * - 12.0.x
     - 2019-06-02
   * - 11.4.x
     - 2019-03-23
   * - 11.3.x
     - 2019-02-14
   * - 11.2.x
     - 2018-12-15
   * - 11.1.x
     - 2018-11-11
   * - 11.0.x
     - 2018-08-13
   * - 10.3.x
     - 2018-05-24
   * - 10.2.x
     - 2018-02-30
   * - 10.1.x
     - 2017-12-09
   * - 10.0.x
     - 2017-08-05
   * - 9.4.x
     - 2016-11-21
   * - 9.3.x
     - 2016-05-06
   * - 9.2.x
     - 2015-12-28
   * - 9.1.x
     - 2015-09-26
   * - 9.0.x
     - 2015-08-07
   * - 8.x
     - 2014-08-23
   * - 7.x
     - 2014-02-03
   * - 6.x
     - 2013-09-02
   * - 5.x
     - 2013-06-15
   * - 4.x
     - 2012-06-19
   * - 3.x
     - 2011-09-07
   * - 2.x
     - 2011-07-16
   * - 1.x
     - 2011-04-10

Foire aux questions
====================

Q : Puis-je continuer à utiliser Fess après la fin de la période de support ?
------------------------------------------------------------------------------

R : Techniquement, c'est possible, mais les correctifs de sécurité et les corrections de bogues ne seront plus fournis.
Pour atténuer les risques de sécurité, nous recommandons fortement de mettre à niveau vers une version prise en charge.

Q : Combien de temps prend une mise à niveau ?
------------------------------------------------

R : Cela dépend de l'échelle de votre environnement, mais généralement de 2 à 4 heures.
Pour les environnements à grande échelle ou les configurations complexes, nous recommandons de tester d'abord dans un environnement de pré-production.
Consultez le `Guide de mise à niveau <15.5/install/upgrade.html>`__ pour plus de détails.

Q : Que faire si je rencontre un problème avec une version en fin de vie ?
---------------------------------------------------------------------------

R : Vous disposez des options suivantes :

1. **Mettre à niveau vers la dernière version** : L'action recommandée
2. **Poser la question sur les forums communautaires** : Vous pourrez peut-être obtenir des conseils d'autres utilisateurs
3. **Consulter le support commercial** : Le `support commercial N2SM <support-services.html>`__ peut assurer la maintenance de versions spécifiques

Q : Que dois-je vérifier avant de mettre à niveau ?
-----------------------------------------------------

R : Veuillez vérifier les éléments suivants :

1. Consultez les `Notes de version <https://github.com/codelibs/fess/releases>`__ pour les changements incompatibles
2. Vérifiez la compatibilité de la version d'OpenSearch
3. Si vous avez des personnalisations, vérifiez la compatibilité des paramètres et des plugins
4. Créez des sauvegardes complètes

Q : La mise à niveau dans un environnement Docker nécessite-t-elle des étapes spéciales ?
------------------------------------------------------------------------------------------

R : Vous devrez sauvegarder les volumes Docker et obtenir les nouveaux fichiers Docker Compose.
Consultez le `Guide d'installation Docker <15.5/install/install-docker.html>`__ pour plus de détails.
