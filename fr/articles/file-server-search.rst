===============================================
Recherche plein texte pour serveurs de fichiers
===============================================

Introduction
============

À mesure que chaque service ajoute ses propres serveurs de fichiers, plus personne ne sait où se trouve tel ou tel document.
La recherche Windows ne fonctionne qu'à l'intérieur d'un seul dossier partagé et ne permet donc pas de chercher sur plusieurs serveurs à la fois.
La recherche plein texte intégrée à un NAS ne fonctionne pas non plus d'un appareil à l'autre.

L'une des façons de résoudre ce problème consiste à mettre en place un serveur de recherche plein texte dédié aux serveurs de fichiers.
Cette page résume les points à vérifier avant d'adopter Fess, un serveur de recherche plein texte open source, pour rechercher dans des serveurs de fichiers.
Le contenu correspond à Fess 15.9.

Public visé
===========

- Les personnes qui ont du mal à rechercher dans les serveurs de fichiers et NAS internes
- Les personnes qui envisagent une recherche plein texte et veulent savoir si elle peut être réalisée en open source
- Les personnes qui veulent introduire une recherche sans casser les droits d'accès existants

Fess est publié sous la licence Apache License 2.0 et peut être utilisé sans frais de licence.

Où se trouvent les fichiers que l'on peut rechercher
====================================================

L'exploration de fichiers de Fess prend en charge les protocoles suivants.
Dans la console d'administration, ouvrez [Robot d'exploration] > [Système de fichiers] et indiquez dans « Chemins » l'emplacement où commence l'exploration.

.. list-table:: Protocoles pris en charge
   :header-rows: 1
   :widths: 12 33 55

   * - Protocole
     - Format du chemin
     - Usage principal
   * - ``file``
     - ``file:/home/share/documents/``
     - Répertoires du serveur qui exécute Fess, y compris les volumes NAS montés
   * - ``smb``
     - ``smb://fileserver.example.com/share/``
     - Partages de fichiers Windows et NAS qui partagent des fichiers via SMB
   * - ``smb1``
     - ``smb1://fileserver.example.com/share/``
     - Connexions utilisant l'ancienne implémentation SMB1 ; solution de repli pour les anciens appareils auxquels ``smb`` ne parvient pas à se connecter
   * - ``ftp``
     - ``ftp://fileserver.example.com/pub/``
     - Serveurs FTP
   * - ``s3``
     - ``s3://bucket-name/prefix/``
     - Amazon S3 et stockages objet compatibles S3 (nécessite le plugin ``fess-storage-s3``)
   * - ``gcs``
     - ``gcs://bucket-name/prefix/``
     - Google Cloud Storage (nécessite le plugin ``fess-storage-gcs``)

Les protocoles gérés par Fess lui-même sont déterminés par le paramètre ``crawler.file.protocols``, dont la valeur par défaut en 15.9 est ``file,smb,smb1,ftp``.
En 15.9, ``s3`` et ``gcs`` ont été retirés de Fess lui-même et déplacés dans des plugins.
Les deux plugins sont inclus dans l'image Docker ; pour un Fess installé à partir du ZIP ou des paquets RPM/DEB, installez-les depuis [Système] > [Plugin] et redémarrez Fess avant de les utiliser.

Pour rechercher dans des partages de fichiers Windows, utilisez ``smb``.
Sauf configuration particulière côté Fess, ``smb`` négocie la version de connexion avec le serveur dans la plage allant de SMB1 à SMB 3.1.1.
``smb1`` établit la connexion avec une autre implémentation (l'ancien jcifs) et n'est pas à choisir pour une nouvelle installation.

Reprendre les droits d'accès existants
======================================

Lorsqu'on ajoute la recherche à des serveurs de fichiers, la plus grande inquiétude est que « des documents qui ne devraient pas être visibles apparaissent dans les résultats de recherche ».
Si les dossiers partagés des ressources humaines ou de la comptabilité apparaissent dans les résultats de recherche de tous les employés, le système de recherche lui-même devient inutilisable.

Fess résout ce problème en reprenant dans la recherche les droits d'accès du serveur de fichiers.
Toutefois, une configuration d'exploration nouvellement créée ne filtre pas encore les résultats selon les droits. Vérifiez impérativement le mécanisme ci-dessous ainsi que la section suivante, « Supprimer {role}guest des autorisations ».

Fonctionnement
--------------

1. Lors de l'exploration, Fess lit l'ACL (liste de contrôle d'accès) de chaque fichier
2. Les comptes et groupes autorisés à lire le fichier, ainsi que les comptes et groupes à qui la lecture est refusée, sont enregistrés comme « rôles » du document dans le champ ``role``
3. Les valeurs saisies dans « Autorisations » de la configuration d'exploration sont ajoutées au même champ ``role``
4. Au moment de la recherche, Fess les compare aux rôles de l'utilisateur connecté et ne renvoie que les documents auxquels il a accès

Dans le champ ``role``, les utilisateurs sont enregistrés avec ``1`` et les groupes avec ``2`` placés devant le nom (par exemple ``1taro`` et ``2sales``).
Les entrées de refus reçoivent en plus le préfixe ``D`` (par exemple ``D2contractors``).
Une valeur saisie sous la forme ``{role}guest`` dans « Autorisations » est enregistrée comme ``Rguest``.
Les mentions ``(allow)`` et ``(deny)`` visibles dans la console d'administration sont des notations pour la saisie dans « Autorisations », et non des valeurs enregistrées.

L'extraction des rôles à partir des ACL est activée par défaut.

.. list-table:: Paramètres de reprise des droits (fess_config.properties)
   :header-rows: 1
   :widths: 38 14 48

   * - Paramètre
     - Par défaut
     - Description
   * - ``smb.role.from.file``
     - ``true``
     - Obtient les rôles à partir des ACL des fichiers explorés avec ``smb`` et ``smb1``
   * - ``file.role.from.file``
     - ``true``
     - Obtient les rôles à partir des droits d'accès des fichiers explorés avec ``file`` (voir les remarques plus bas)
   * - ``ftp.role.from.file``
     - ``true``
     - Obtient les rôles à partir du propriétaire et du groupe des fichiers explorés avec ``ftp``
   * - ``smb.available.sid.types``
     - ``1,2,4:2,5:1``
     - Les types de SID retenus comme rôles et le type sous lequel chacun est enregistré. Par défaut, les utilisateurs (1) et les groupes de domaine (2) sont enregistrés tels quels, les groupes locaux (4) comme groupes et les SID intégrés tels que Everyone (5) comme utilisateurs

Supprimer {role}guest des autorisations
---------------------------------------

Lorsque vous créez une configuration dans [Robot d'exploration] > [Système de fichiers], le champ « Autorisations » contient déjà ``{role}guest``.
Si vous l'enregistrez tel quel, chaque document reçoit ``Rguest`` en plus des rôles issus de l'ACL.
Comme les utilisateurs non connectés reçoivent le rôle ``guest``, **les fichiers restreints par ACL apparaissent tous dans les recherches effectuées sans connexion**.

Pour que le filtrage par ACL prenne effet, supprimez ``{role}guest`` du champ « Autorisations » de la configuration d'exploration et enregistrez-la.
Les documents déjà explorés sont enregistrés de nouveau avec les nouvelles autorisations lors de l'exploration suivante.

Les utilisateurs connectés, eux, ne reçoivent pas le rôle ``guest``.
Ainsi, même si ``{role}guest`` est conservé, les utilisateurs connectés obtiennent des résultats conformes aux ACL.
Comme indiqué dans « Vérifier le fonctionnement », vérifiez toujours aussi sans être connecté.

Faire correspondre les noms côté connexion
------------------------------------------

Pour que ce mécanisme fonctionne de bout en bout, les utilisateurs qui recherchent doivent eux aussi posséder les mêmes rôles.
Le document indique « les membres de ce groupe peuvent le lire » ; la correspondance est donc impossible si l'utilisateur qui recherche ne peut pas indiquer à Fess les groupes auxquels il appartient.

C'est pourquoi une recherche qui respecte les droits suppose une intégration avec Active Directory ou LDAP.
La configuration consiste à utiliser pour la connexion à Fess le même annuaire que celui qui sert à l'authentification sur les serveurs de fichiers.
LDAP se configure dans [Système] > [Général].
La procédure et la logique des rôles sont expliquées dans :doc:`guide-05`.

La correspondance se faisant sur des chaînes de noms, tenez compte des points suivants.

- Les noms tirés des ACL sont enregistrés comme des noms de compte sans le nom de domaine (``EXAMPLE\taro`` devient ``1taro``)
- Pour les utilisateurs qui se connectent via LDAP, les noms de groupe sont tirés par défaut du CN de ``memberOf``. Si le nom de compte d'un groupe sur le serveur de fichiers diffère de son CN, ils ne correspondent pas
- Les groupes intégrés tels qu'Everyone sont enregistrés comme des rôles portant ce nom. Les utilisateurs connectés via LDAP n'ont généralement pas ces rôles ; les dossiers partagés uniquement avec des groupes intégrés peuvent donc n'être affichés à personne. Si nécessaire, séparez la configuration d'exploration et complétez les rôles dans « Autorisations »

À l'inverse, si vous ne ciblez que des dossiers partagés que tous les employés peuvent voir de la même manière, cette intégration n'est pas indispensable.
C'est le point qui départage les choix lorsque vous définissez le périmètre du déploiement.

Remarques par protocole
-----------------------

``smb`` / ``smb1``
   Le compte d'exploration doit pouvoir lire non seulement le contenu des fichiers, mais aussi leurs droits d'accès (informations de sécurité).
   Les fichiers dont les droits d'accès ne peuvent pas être lus ne sont pas indexés et sont consignés dans [Informations système] > [URL d'échec].

``file``
   Si le système de fichiers ne fournit pas d'ACL (comme les systèmes de fichiers Linux courants), seuls deux rôles sont enregistrés : l'utilisateur et le groupe propriétaires.
   Un droit de lecture accordé aux « autres » ne devient pas un rôle.
   Si vous montez un NAS sur le serveur Fess et l'explorez avec ``file``, c'est le propriétaire visible au point de montage qui est enregistré, et non les ACL du NAS.
   Explorez directement avec ``smb``, sans les monter, les serveurs de fichiers sur lesquels vous souhaitez filtrer selon les ACL.

``ftp``
   Le propriétaire et le groupe renvoyés par le serveur FTP sont enregistrés comme rôles.

Quels formats de fichier sont lus jusqu'au contenu
==================================================

Fess utilise Apache Tika pour extraire le texte du contenu des fichiers.
Comme le texte lui-même est indexé, et pas seulement le nom du fichier, vous pouvez retrouver « des documents dont vous avez oublié le titre ».

Les principaux formats pris en charge sont les suivants.

- MS Office (doc, xls, ppt, docx, xlsx, pptx, etc.)
- PDF
- Texte, HTML, XML
- Texte enrichi (rtf)
- Code source (js, c, h, java, etc.)
- Archives (gz, tar, zip, etc.)

Pour la liste complète, consultez `Fichiers recherchables <https://fess.codelibs.org/fr/supported-files.html>`__.

Les fichiers sans texte, comme les PDF images et les documents numérisés, ne permettent pas de rechercher dans leur contenu en l'état.
Fess 15.9 permet d'activer l'OCR avec Tesseract, qui lit le texte des fichiers image, des images incorporées dans les documents Office et des PDF ne contenant pas de texte.
L'OCR est désactivé par défaut.
Installez ``tesseract`` sur l'hôte où s'exécute le robot d'exploration et définissez ``crawler.document.ocr.enabled=true``.
Les PDF dont seules certaines pages sont des images numérisées ne sont pas pris en charge.
Pour la procédure, consultez `Configuration de l'OCR <https://fess.codelibs.org/fr/stable/config/crawler-ocr.html>`__.
L'OCR allongeant la durée d'exploration, nous vous recommandons de vérifier d'abord la quantité de documents numérisés dans les dossiers cibles.

Architecture et dimensionnement
===============================

Fess utilise OpenSearch pour stocker l'index de recherche.
À petite échelle, Fess et OpenSearch peuvent cohabiter sur le même serveur ; lorsque le nombre de fichiers cibles augmente, vous pouvez séparer OpenSearch en cluster.

Pour estimer le dimensionnement, vérifier les points suivants en plus du nombre de fichiers rend l'estimation plus précise.

- La taille totale des dossiers cibles et la proportion de fichiers contenant du texte
- La fréquence de mise à jour (quotidienne, ou quelques fois par mois). Elle influe sur la conception de l'intervalle d'exploration
- La taille par fichier

Par défaut, la taille des fichiers pouvant être indexés est plafonnée.
Les valeurs par défaut de ``app/WEB-INF/classes/crawler/contentlength.xml`` sont de 2,5 Mo pour le HTML et de 10 Mo pour tout le reste ; les fichiers qui les dépassent ne sont pas indexés et sont consignés dans [URL d'échec].
Indépendamment, une ligne telle que ``client.maxContentLength=10485760`` dans « Paramètres de configuration » de la configuration d'exploration limite la taille des fichiers récupérés eux-mêmes (aucune limite par défaut).
Pour les dossiers contenant beaucoup de documents volumineux, décidez avant le déploiement s'il faut revoir ces limites.
Pour la configuration, consultez la section sur les paramètres de taille de fichier dans `Configuration du robot d'indexation <https://fess.codelibs.org/fr/stable/config/crawler-basic.html>`__.

L'intervalle d'exploration demande aussi de l'attention.
Fess supprime de l'index les documents qui n'ont été mis à jour par aucune exploration pendant un certain nombre de jours.
Ce nombre de jours correspond à « Supprimer les anciens documents » dans [Système] > [Général], et vaut 3 jours par défaut.
La tâche par défaut « Default Crawler » s'exécute tous les jours, ce qui ne pose pas de problème ; mais si vous la réduisez par exemple à une fois par semaine, choisissez un nombre de jours supérieur à l'intervalle d'exécution.

Critères de choix d'un outil de recherche pour serveurs de fichiers
===================================================================

Lorsque vous comparez des outils de recherche pour serveurs de fichiers, le choix est plus facile si vous vérifiez qu'ils remplissent les points suivants avant de comparer les noms de produits.

.. list-table:: Points à vérifier lors du choix d'un outil de recherche
   :header-rows: 1
   :widths: 30 70

   * - Point à vérifier
     - Avec Fess
   * - Peut-il rechercher sur plusieurs serveurs et NAS à la fois ?
     - En enregistrant plusieurs configurations d'exploration, vous pouvez rechercher sur l'ensemble depuis une seule zone de recherche
   * - Peut-il rechercher dans le contenu des fichiers ?
     - Apache Tika extrait le texte des documents Office et des PDF et le rend recherchable. Les documents numérisés deviennent recherchables lorsque l'OCR est activé
   * - Peut-il reprendre les droits d'accès existants ?
     - Il obtient les rôles à partir des ACL des fichiers explorés via SMB et filtre les résultats de recherche en conséquence. Une intégration avec Active Directory ou LDAP et une révision du champ « Autorisations » de la configuration d'exploration sont nécessaires
   * - Entraîne-t-il des frais de licence ?
     - Il est publié sous la licence Apache License 2.0 et n'entraîne aucun frais de licence
   * - Peut-on l'essayer en local ?
     - Vous pouvez le démarrer avec Docker Compose et essayer la recherche sur votre propre machine

Étapes du déploiement
=====================

1. **Le faire tourner** — Démarrez Fess en suivant le `Guide de construction rapide <https://fess.codelibs.org/fr/quick-start.html>`__ ou :doc:`guide-02`
2. **Créer une configuration d'exploration** — Dans [Robot d'exploration] > [Système de fichiers], enregistrez un nom et des chemins. Si vous filtrez selon les ACL, supprimez ``{role}guest`` du champ « Autorisations » avant d'enregistrer
3. **Configurer les identifiants** — Enregistrez le compte servant à accéder aux dossiers partagés dans [Robot d'exploration] > [Authentification de fichier], puis sélectionnez la configuration de l'étape 2 dans « Configuration de l'exploration de fichiers »
4. **Vérifier les droits du compte d'exploration** — Côté serveur de fichiers, vérifiez que le compte peut lire à la fois le contenu et les droits d'accès des dossiers cibles
5. **Intégrer la connexion** — Configurez LDAP (Active Directory) dans [Système] > [Général]
6. **Lancer l'exploration et vérifier** — Dans [Système] > [Planificateur], ouvrez « Default Crawler », cliquez sur [Démarrer maintenant], puis vérifiez le résultat comme décrit dans « Vérifier le fonctionnement » ci-dessous

Si vous avez besoin de filtrer par service, configurez également des étiquettes dans [Robot d'exploration] > [Étiquette].

Les étapes concrètes pour rechercher dans plusieurs serveurs de fichiers et sites web internes depuis une seule zone de recherche sont traitées dans :doc:`guide-04`, et la conception du filtrage des résultats par rôles et groupes dans :doc:`guide-05`.

Vérifier le fonctionnement
==========================

Une fois l'exploration terminée, vérifiez les points suivants dans l'ordre.
L'utilisateur intégré ``admin`` possède aussi le rôle ``guest`` ; ne l'utilisez donc pas pour vérifier le filtrage.

1. Ouvrez [Informations système] > [URL d'échec] et vérifiez qu'aucun fichier n'a été ignoré à cause d'une erreur d'accès ou d'un dépassement de taille
2. Dans [Informations système] > [Rechercher], recherchez un fichier d'un dossier restreint. Cet écran ne filtre pas par rôle ; tous les documents sont donc affichés
3. Cliquez sur [Mettre à jour] pour le résultat afin d'ouvrir l'écran de modification, puis vérifiez le champ ``role``. Assurez-vous qu'il contient des valeurs issues de l'ACL comme ``1taro`` ou ``2sales``, et qu'il ne contient pas ``Rguest``
4. Déconnecté, recherchez le même fichier dans la page de recherche et vérifiez qu'il n'apparaît pas
5. Connectez-vous avec un utilisateur appartenant à un groupe autorisé à lire le dossier, lancez la recherche et vérifiez que le fichier apparaît
6. Connectez-vous avec un utilisateur n'appartenant pas à ce groupe, lancez la recherche et vérifiez que le fichier n'apparaît pas

Si, à l'étape 3, les noms du champ ``role`` diffèrent de ceux côté LDAP, revoyez chacun des points de « Faire correspondre les noms côté connexion ».

Résumé
======

- Fess est un serveur de recherche open source qui permet la recherche plein texte dans les serveurs de fichiers (SMB, FTP, local). S3 et GCS sont pris en charge par des plugins
- Pour les fichiers explorés via SMB, les droits d'accès enregistrés dans les ACL servent à filtrer les résultats de recherche. La lecture des ACL est activée par défaut
- Tant que vous ne supprimez pas ``{role}guest`` du champ « Autorisations » de la configuration d'exploration, les utilisateurs non connectés voient tous les documents
- Une recherche qui respecte les droits suppose une intégration avec Active Directory ou LDAP et la correspondance des noms des deux côtés
- Apache Tika rend recherchable le contenu des documents Office et des PDF, et l'activation de l'OCR rend aussi recherchables les documents numérisés
- Vous pouvez commencer petit et étendre le système en passant OpenSearch en cluster lorsque les cibles augmentent

Articles à lire ensuite
=======================

- Étapes pour rechercher ensemble dans plusieurs serveurs de fichiers et sites web internes : :doc:`guide-04`
- Conception du filtrage des résultats par rôles et groupes : :doc:`guide-05`
- Essayer Fess en local avec Docker : :doc:`guide-02`

Références
==========

- `Crawl de système de fichiers (recherche sur serveur de fichiers) <https://fess.codelibs.org/fr/stable/admin/fileconfig-guide.html>`__
- `Authentification de fichier <https://fess.codelibs.org/fr/stable/admin/fileauth-guide.html>`__
- `Configuration du robot d'indexation : exploration Web, serveur de fichiers et bases de données <https://fess.codelibs.org/fr/stable/config/crawler-basic.html>`__
- `Configuration de l'OCR <https://fess.codelibs.org/fr/stable/config/crawler-ocr.html>`__
- `Configuration de la recherche basée sur les rôles <https://fess.codelibs.org/fr/stable/config/security-role.html>`__
- `Guide d'intégration LDAP <https://fess.codelibs.org/fr/stable/config/ldap-integration.html>`__
- `URL en échec <https://fess.codelibs.org/fr/stable/admin/failureurl-guide.html>`__
- `Fichiers recherchables <https://fess.codelibs.org/fr/supported-files.html>`__
- `Guide de construction rapide <https://fess.codelibs.org/fr/quick-start.html>`__
