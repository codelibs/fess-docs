===============================================
Recherche plein texte pour serveurs de fichiers
===============================================

Introduction
============

À mesure que les services ajoutent des serveurs de fichiers, plus personne ne sait où se trouve tel ou tel document. La recherche de Windows ne travaille que dans un dossier partagé à la fois et ne franchit pas les frontières entre serveurs ; la recherche plein texte d'un NAS s'arrête au boîtier.

Une solution consiste à placer un serveur de recherche plein texte devant les serveurs de fichiers. Cette page réunit ce qu'il faut vérifier avant de confier ce rôle à Fess, un serveur de recherche plein texte open source.

À qui s'adresse cette page
==========================

- À celles et ceux qui peinent à chercher sur un serveur de fichiers interne ou un NAS
- À celles et ceux qui évaluent la recherche plein texte et se demandent si l'open source suffit
- À celles et ceux qui veulent ajouter la recherche sans toucher aux droits d'accès existants

Fess est publié sous licence Apache 2.0 et n'entraîne aucun coût de licence.

Où les fichiers peuvent se trouver
==================================

Le robot de fichiers de Fess parle les protocoles suivants. Ils se configurent dans l'interface d'administration sous [Robot] > [Système de fichiers], comme URL de départ de l'exploration.

.. list-table:: Protocoles pris en charge
   :header-rows: 1
   :widths: 12 33 55

   * - Protocole
     - Forme de l'URL
     - Usage courant
   * - ``file``
     - ``file:///home/share/documents/``
     - Un répertoire de la machine qui exécute Fess, y compris un NAS déjà monté
   * - ``smb``
     - ``smb://fileserver.example.com/share/``
     - Partages de fichiers Windows, de SMB 2.0.2 à SMB 3.1.1
   * - ``smb1``
     - ``smb1://fileserver.example.com/share/``
     - Matériel ancien qui ne parle que SMB1/CIFS
   * - ``ftp``
     - ``ftp://fileserver.example.com/pub/``
     - Serveurs FTP
   * - ``s3``
     - ``s3://bucket-name/prefix/``
     - Amazon S3 et stockage objet compatible S3
   * - ``gcs``
     - ``gcs://bucket-name/prefix/``
     - Google Cloud Storage

L'ensemble activé est décrit par ``crawler.file.protocols``, dont la valeur par défaut est ``file,smb,smb1,ftp,s3,gcs``.

Pour les partages Windows, ``smb`` est le choix habituel. ``smb1`` subsiste pour les vieux NAS et serveurs d'impression qui ne parlent rien d'autre ; SMB1 est désactivé par défaut dans Windows pour des raisons de sécurité et n'est donc pas un choix à retenir pour une nouvelle installation.

Les droits d'accès existants sont repris
========================================

La plus grande crainte, lorsqu'on met une recherche devant un serveur de fichiers, est de voir apparaître dans les résultats des documents que l'on ne devrait pas voir. Si les dossiers des ressources humaines et de la comptabilité remontent pour tout le monde, le système de recherche est inutilisable, quelle que soit la qualité du classement.

Fess répond à cela en **reprenant dans la recherche les droits d'accès du serveur de fichiers lui-même**.

Principe de fonctionnement
--------------------------

1. Pendant l'exploration, Fess lit la liste de contrôle d'accès (ACL) de chaque fichier
2. Les comptes et groupes autorisés ou refusés sont enregistrés comme rôles du document
3. Au moment de la recherche, ces rôles sont comparés à ceux de l'utilisateur connecté, et seuls les documents autorisés sont renvoyés

L'autorisation et le refus sont tous deux traités, distingués en interne par les préfixes ``(allow)`` et ``(deny)``. La lecture des rôles depuis l'ACL est active par défaut.

.. list-table:: Réglages qui gouvernent la reprise des droits
   :header-rows: 1
   :widths: 38 14 48

   * - Réglage
     - Défaut
     - Effet
   * - ``smb.role.from.file``
     - ``true``
     - Reprend les rôles depuis l'ACL des fichiers explorés en SMB
   * - ``file.role.from.file``
     - ``true``
     - Reprend les rôles depuis les permissions du système de fichiers local
   * - ``ftp.role.from.file``
     - ``true``
     - Reprend les rôles depuis les fichiers explorés en FTP
   * - ``smb.available.sid.types``
     - ``1,2,4:2,5:1``
     - Quels types de SID deviennent des rôles ; règle le traitement des utilisateurs et des groupes

Le prérequis à vérifier en premier
----------------------------------

Pour que la chaîne soit complète, **la personne qui cherche doit porter les mêmes rôles**. Le document indique « ce groupe peut me lire » ; tant que l'utilisateur qui cherche ne peut pas dire à Fess à quels groupes il appartient, il n'y a rien à comparer.

L'**intégration à Active Directory ou LDAP est donc un prérequis** pour une recherche respectueuse des droits : Fess authentifie les utilisateurs auprès de l'annuaire qui sert déjà au serveur de fichiers.

En revanche, si l'on n'indexe que des dossiers partagés que toute l'entreprise peut lire, cette intégration n'est pas nécessaire. C'est en général cette distinction qui fixe le périmètre d'un premier déploiement.

Quels formats de fichiers sont lus
==================================

Fess extrait le texte du contenu des fichiers avec Apache Tika : c'est le corps du document qui devient consultable, et pas seulement son nom. C'est ce qui permet de retrouver un document dont plus personne ne se rappelle le titre.

Les principaux formats sont :

- MS Office (doc, xls, ppt, docx, xlsx, pptx, etc.)
- PDF
- Texte brut, HTML, XML
- Texte enrichi (rtf)
- Code source (js, c, h, java, etc.)
- Archives (gz, tar, zip, etc. ; le contenu est décompressé puis indexé)

La liste complète figure sur `Fichiers recherchables <https://fess.codelibs.org/fr/supported-files.html>`__.

Les fichiers qui ne contiennent aucun texte, comme les documents numérisés et les PDF constitués d'images, ne peuvent pas être lus ainsi. Mieux vaut déterminer si l'OCR est nécessaire en examinant le contenu réel des dossiers visés avant de commencer.

Dimensionnement et architecture
===============================

Fess range son index dans OpenSearch. Une petite installation fonctionne très bien avec Fess et OpenSearch sur la même machine, et OpenSearch peut être détaché en grappe lorsque le volume augmente.

Pour dimensionner, le seul nombre de fichiers est un mauvais indicateur. Ces trois points comptent davantage :

- La taille totale des dossiers visés, et la part qui contient réellement du texte
- La fréquence des modifications, quotidienne ou mensuelle, qui détermine le calendrier d'exploration
- La taille unitaire des fichiers, les très gros pouvant être exclus de l'exploration par configuration

Pour commencer
==============

1. **Le faire tourner d'abord** — suivre le `Guide de construction rapide <https://fess.codelibs.org/fr/quick-start.html>`__. Avec Docker Compose, on obtient en quelques minutes quelque chose d'interrogeable
2. **Créer une configuration d'exploration** — enregistrer l'URL visée et l'intervalle sous [Robot] > [Système de fichiers]
3. **Renseigner les identifiants** — enregistrer le compte d'accès au partage sous [Robot] > [Authentification de fichiers]
4. **Concevoir rôles et étiquettes** — les étiquettes pour filtrer par service, les rôles pour les résultats selon les droits

Un exemple déroulé se trouve dans `Partie 4 : Recherche unifiée dans des fichiers dispersés <https://fess.codelibs.org/fr/articles/guide-04.html>`__, qui construit un champ de recherche unique au-dessus de plusieurs serveurs de fichiers et d'un site intranet.

Résumé
======

- Fess est un serveur de recherche open source capable d'indexer des serveurs de fichiers en SMB/CIFS, FTP, chemins locaux, S3 et GCS
- Pour les fichiers explorés en SMB, les droits d'accès inscrits dans l'ACL filtrent les résultats, et ce par défaut
- La recherche respectueuse des droits suppose une intégration à Active Directory ou LDAP
- Apache Tika rend consultable le corps des documents Office et des PDF
- Commencer petit, puis grandir en détachant OpenSearch en grappe

Références
==========

- `Configuration du robot : exploration Web, serveur de fichiers et base de données <https://fess.codelibs.org/fr/stable/config/crawler-basic.html>`__
- `Contrôle d'accès par rôles <https://fess.codelibs.org/fr/stable/config/security-role.html>`__
- `Fichiers recherchables <https://fess.codelibs.org/fr/supported-files.html>`__
- `Guide de construction rapide <https://fess.codelibs.org/fr/quick-start.html>`__
- `Guide d'administration <https://fess.codelibs.org/fr/stable/admin/index.html>`__
