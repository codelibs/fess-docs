============================
Connecteur SharePoint Server
============================

Aperçu
======

Le connecteur SharePoint Server récupère les fichiers des bibliothèques de documents et
les éléments de liste d'un déploiement **SharePoint Server** sur site (2013, 2016, 2019
ou Subscription Edition) via son API REST/OData (et, pour 2013, son API XML/Atom), puis
les enregistre dans l'index |Fess|.

Cette fonctionnalité nécessite le plugin ``fess-ds-sharepoint``.

.. note::

   Si vous devez crawler SharePoint Online (Microsoft 365), utilisez
   :doc:`ds-microsoft365` et non ce connecteur. La prise en charge OAuth de ce
   connecteur ne cible que l'authentification application uniquement (application-only)
   d'Azure ACS, et il n'intègre aucune intégration avec l'API Microsoft Graph.

Versions prises en charge : SharePoint Server 2013 / 2016 / 2019 / Subscription Edition
(SE)

Contenu pris en charge
======================

- Fichiers des bibliothèques de documents
- Éléments de liste
- Pièces jointes des éléments de liste

Prérequis
=========

1. L'installation du plugin est requise
2. Le compte de crawl doit disposer d'un accès en lecture aux sites, listes et
   bibliothèques de documents crawlés
3. Choisissez exactement une méthode d'authentification - NTLM, Kerberos (SPNEGO) ou
   OAuth (ACS) - et tenez ses identifiants prêts

Installation du plugin
----------------------

Installez-le depuis l'interface d'administration via « Système » → « Plugin » :

1. Téléchargez ``fess-ds-sharepoint-X.X.X.jar``
2. Placez-le sous ``$FESS_HOME/app/WEB-INF/lib`` (ou
   ``/usr/share/fess/app/WEB-INF/lib``)
3. Redémarrez |Fess|

Consultez :doc:`../../admin/plugin-guide` pour plus de détails.

Configuration
=============

Configurez ce connecteur depuis l'interface d'administration via « Crawler » → « Data
Store » → « Nouveau ».

Configuration de base
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Élément
     - Exemple
   * - Nom
     - SharePoint
   * - Nom du gestionnaire
     - SharePointDataStore
   * - Activé
     - Oui

Configuration des paramètres
----------------------------

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

Liste des paramètres
~~~~~~~~~~~~~~~~~~~~

**URL / Site**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``url``
     - Oui
     - URL de base du serveur SharePoint, par exemple
       ``http://sharepoint.example.com/``
   * - ``site.name``
     - Conditionnel
     - Nom de la collection de sites crawlée sous
       ``/sites/<site.name>/``. Non nécessaire si
       ``site.path`` est défini
   * - ``site.path``
     - Non
     - Chemin d'accès géré relatif au serveur du site (par
       exemple ``/teams/eng`` ; utilisez ``/`` pour la
       collection de sites racine). Lorsqu'il est défini, il
       est utilisé tel quel à la place du préfixe codé en dur
       ``/sites/``, et ``site.name`` n'est plus requis
   * - ``site.list_id``
     - Non
     - Crawle une seule liste par son GUID (mode Crawl de
       liste)
   * - ``site.list_name``
     - Non
     - Crawle une seule liste par son nom d'affichage (mode
       Crawl de liste)
   * - ``site.doclib_path``
     - Non
     - Chemin de la bibliothèque de documents sous le site
       (mode Crawl de bibliothèque de documents), par exemple
       ``/Shared Documents``
   * - ``site.exclude_list``
     - Non
     - Motifs regex séparés par des virgules des noms de types
       d'entité de liste à exclure. S'applique uniquement à un
       crawl de site complet
   * - ``site.exclude_folder``
     - Non
     - Motifs regex séparés par des virgules des titres de
       dossiers de premier niveau à exclure. S'applique
       uniquement à un crawl de site complet
   * - ``site.crawl_subsites``
     - Non
     - Parcourt récursivement les sous-sites du site (par
       défaut : ``false``). Voir `Sous-sites et chemins
       d'accès gérés`_
   * - ``site.max_depth``
     - Non
     - Nombre de niveaux de sous-sites que
       ``site.crawl_subsites`` peut parcourir (par défaut :
       ``10``) ; la racine est à la profondeur 0

**Authentification**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``auth.ntlm.user``
     - Non
     - Nom d'utilisateur NTLM. Le définir active NTLM
       (``DOMAIN\user`` fonctionne)
   * - ``auth.ntlm.password``
     - Non
     - Mot de passe NTLM
   * - ``auth.ntlm.domain``
     - Non
     - Domaine Windows, envoyé comme champ NTLM distinct
   * - ``auth.ntlm.workstation``
     - Non
     - Nom de poste de travail envoyé lors de la négociation
       NTLM
   * - ``auth.kerberos.principal``
     - Non
     - Principal client, écrit sous la forme ``user@REALM``.
       Le définir active Kerberos/SPNEGO
   * - ``auth.kerberos.keytab``
     - Non
     - Chemin vers un keytab contenant une clé pour le
       principal. Mutuellement exclusif avec
       ``auth.kerberos.password``
   * - ``auth.kerberos.password``
     - Non
     - Mot de passe du principal, utilisé uniquement si aucun
       keytab n'est défini
   * - ``auth.kerberos.strip_port``
     - Non
     - Supprime le port du nom de principal de service (par
       défaut : ``true``)
   * - ``auth.kerberos.use_canonical_hostname``
     - Non
     - Résout l'hôte cible vers son nom canonique avant de
       construire le nom de principal de service (par défaut :
       ``false``)
   * - ``auth.kerberos.krb5_conf``
     - Non
     - Chemin vers un ``krb5.conf``. Appliqué uniquement si
       ``java.security.krb5.conf`` n'est pas déjà défini
   * - ``auth.kerberos.debug``
     - Non
     - Active la sortie de débogage de ``Krb5LoginModule``
       (par défaut : ``false``)
   * - ``auth.oauth.client_id``
     - Non
     - ID client OAuth application uniquement
       (application-only) d'Azure ACS. Le définir active OAuth
   * - ``auth.oauth.client_secret``
     - Non
     - Secret client OAuth
   * - ``auth.oauth.tenant``
     - Non
     - Nom du tenant, sans ``.sharepoint.com``
   * - ``auth.oauth.realm``
     - Non
     - ID de royaume/répertoire (realm/directory) Azure AD

**Une seule** des options ``auth.kerberos.principal``, ``auth.ntlm.user`` et
``auth.oauth.client_id`` peut être définie. Voir `Authentification`_ ci-dessous.

**Liste**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``list.items.number_per_page``
     - Non
     - Taille de page pour ``GetListItems`` (par défaut :
       ``100``)
   * - ``list.item.content.include_fields``
     - Non
     - Noms de champs séparés par des virgules ; si défini,
       seuls ces champs de l'élément de liste sont concaténés
       dans ``content``
   * - ``list.item.content.exclude_fields``
     - Non
     - Motifs de noms de champs séparés par des virgules
       (chacun traité comme une regex), exclus de ``content``
       en plus d'un vaste ensemble intégré de champs standard
   * - ``list.is_sub_page``
     - Non
     - Traite les éléments de liste comme des sous-pages
       SitePages/wiki, ce qui affecte le repli de pagination
       et la forme du lien web (par défaut : ``false``)

**HTTP**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``http.connection_timeout``
     - Non
     - Délai de connexion HTTP en ms ; également utilisé comme
       délai d'attente du pool de connexions (par défaut :
       ``30000``)
   * - ``http.socket_timeout``
     - Non
     - Délai de socket HTTP (lecture) en ms (par défaut :
       ``30000``)
   * - ``proxy_host``
     - Non
     - Hôte du proxy HTTP
   * - ``proxy_port``
     - Conditionnel
     - Port du proxy HTTP ; requis si ``proxy_host`` est
       défini (par défaut : ``-1`` = pas de proxy)

**Filtrage et contenu**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``include_pattern``
     - Non
     - Regex que la valeur d'un élément doit satisfaire pour
       être crawlé. Voir la note sous ce tableau pour savoir
       de quelle valeur il s'agit
   * - ``exclude_pattern``
     - Non
     - Regex qui exclut du crawl un élément correspondant
   * - ``supported_mimetypes``
     - Non
     - Regex séparées par des virgules dont le type MIME d'un
       fichier doit satisfaire au moins une (par défaut :
       ``.*``)
   * - ``max_content_length``
     - Non
     - Taille maximale de fichier en octets ; un fichier
       dépassant la limite est ignoré, pas mis en échec (par
       défaut : ``-1`` = pas de limite)
   * - ``extractor_name``
     - Non
     - Extracteur de repli utilisé uniquement pour un type
       MIME que la fabrique d'extracteurs ne mappe pas (par
       défaut : ``tikaExtractor``)

**Comportement**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``sp.version``
     - Non
     - Définir à ``2013`` pour basculer vers la famille d'API
       XML/Atom ``GetXxxByServerRelativeUrl`` de SharePoint
       2013 (non défini ⇒ dialecte REST SharePoint Online /
       2016+)
   * - ``retry_limit``
     - Non
     - Nombre maximal de tentatives par unité de crawl en cas
       d'exception serveur/client SharePoint (par défaut :
       ``2``)
   * - ``role.skip``
     - Non
     - Ignore complètement la récupération des permissions par
       élément (par défaut : ``false``). Voir `Permissions`_
   * - ``ignore_error``
     - Non
     - Journalise et ignore un échec d'extraction de contenu
       d'un fichier au lieu de mettre en échec la cible de
       crawl (par défaut : ``false``)
   * - ``default_permissions``
     - Non
     - Chaînes de permission séparées par des virgules,
       fusionnées dans la liste de rôles de chaque document en
       plus de ce que SharePoint a renvoyé
   * - ``delete_old_docs``
     - Non
     - Indique si les documents non actualisés lors de cette
       exécution sont supprimés (par défaut du cœur :
       ``true``). Ce plugin le force à ``false`` pour
       l'exécution en cours dès qu'une cible de crawl a échoué
   * - ``number_of_threads``
     - Non
     - Nombre de cibles de crawl traitées simultanément (par
       défaut : ``1`` = pas de pool de threads), plafonné au
       double du nombre de processeurs. Voir `Crawl parallèle
       et charge`_
   * - ``script_type``
     - Non
     - Moteur de script pour le Script de la configuration de
       données (par défaut : ``groovy``)
   * - ``readInterval``
     - Non
     - Pause entre deux résultats de crawl successifs, en ms
       (par défaut : ``0``). Notez l'orthographe en camelCase,
       contrairement à tous les autres paramètres ci-dessus

Configuration du script
-----------------------

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

Champs disponibles
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 20 32 32

   * - Clé
     - Élément de liste
       (ItemCrawl)
     - Fichier de bibliothèque
       (FolderCrawl->FileCrawl)
     - Pièce jointe
       (ItemAttachmentsCrawl->FileCrawl)
   * - ``url``
     - Lien web
     - URL du fichier
     - URL du fichier
   * - ``host``
     - Nom d'hôte
     - Nom d'hôte
     - Nom d'hôte
   * - ``site``
     - Chemin relatif au
       serveur
       (``FileRef``)
     - Chemin relatif au serveur
     - Chemin relatif au serveur
   * - ``title``
     - Champ ``Title``,
       sinon
       ``FileLeafRef``/nom
       de fichier
     - La valeur de liste ``Title``
       propre au fichier de la
       bibliothèque si présente,
       sinon le nom de fichier
     - Nom de fichier
   * - ``titleWithListName``
     - ``"[listName]
       title"``
     - ``"[listName] filename"`` (le
       nom de liste est toujours
       vide pour un crawl de
       bibliothèque de documents,
       donc il s'agit en pratique du
       seul nom de fichier)
     - ``"[listName] filename"``
   * - ``listName``
     - Nom d'affichage de
       la liste, ou
       ``""``
     - Toujours ``""``
     - Nom réel de la liste
   * - ``content``
     - Concaténation des
       valeurs de champs
     - Texte extrait
     - Texte extrait
   * - ``digest``
     - ``content`` abrégé
     - ``content`` abrégé
     - ``content`` abrégé
   * - ``content_length``
     - ``content.length()``
     - ``content.length()``
     - ``content.length()``
   * - ``last_modified``
     - Depuis le listing
     - Depuis le listing
     - Depuis le listing
   * - ``created``
     - Depuis le listing
     - Depuis le listing
     - Depuis le listing
   * - ``mimetype``
     - Toujours
       ``text/html``
     - Détecté
     - Détecté
   * - ``filetype``
     - Dérivé de
       ``mimetype``
     - Dérivé de ``mimetype``
     - Dérivé de ``mimetype``
   * - ``role``
     - Liste de
       permissions,
       uniquement si non
       vide
     - Liste de permissions,
       uniquement si non vide
     - Liste de permissions,
       uniquement si non vide
   * - ``list_name``
     - Présent
     - **Absent**
     - Présent
   * - ``list_id``
     - Présent
     - **Absent**
     - Présent
   * - ``item_id``
     - Présent
     - **Absent**
     - Présent

.. note::

   ``content_length`` correspond à ``content.length()`` - le nombre de caractères
   (unités de code UTF-16) du texte extrait ou concaténé, et non la taille du fichier en
   octets. Ceci diffère de ``file.size`` dans les connecteurs Box, Google Drive et
   Dropbox, qui est la taille réelle en octets issue des métadonnées de fichier propres
   à chaque service. Ne comparez pas le ``content_length`` de ce connecteur à ces
   valeurs.

**Clés dynamiques : ``val_*``**

Chaque clé du ``FieldValuesAsText`` d'un élément de liste (la map brute des valeurs de
champs que SharePoint renvoie pour cet élément, y compris les clés de métadonnées OData
telles que ``odata.metadata``) est exposée sous deux noms : une fois sans préfixe
(uniquement si ce nom n'est pas déjà l'une des clés fixes ci-dessus), et une fois avec
le préfixe ``val_``, systématiquement - par exemple, un champ ``Status`` devient à la
fois ``Status`` et ``val_Status``.

Les clés ``val_*`` n'existent que sur le **chemin de crawl des éléments de liste
(ItemCrawl)**. Un fichier de bibliothèque de documents (FolderCrawl->FileCrawl) ou une
pièce jointe d'élément de liste (ItemAttachmentsCrawl->FileCrawl) ne produit jamais de
clé ``val_*``.

Authentification
================

Trois méthodes d'authentification sont disponibles, et **une seule peut être
configurée**. Définir plus d'une des options ``auth.kerberos.principal``,
``auth.ntlm.user`` et ``auth.oauth.client_id`` fait échouer le job de configuration de
données avec une erreur de validation avant qu'aucune requête ne soit émise. C'est voulu
: un seul jeu d'identifiants est enregistré auprès du client HTTP, et la portée sous
laquelle il est enregistré correspond aussi bien à un défi ``Negotiate`` qu'à un défi
``NTLM``, donc en configurer plus d'une produirait sinon des 401 que rien dans le
journal n'expliquerait.

NTLM
----

::

    auth.ntlm.user={Nom d'utilisateur SharePoint}
    auth.ntlm.password={Mot de passe}
    auth.ntlm.domain={Domaine Windows. Optionnel ; non défini par défaut.}
    auth.ntlm.workstation={Nom de poste de travail envoyé lors de la négociation NTLM. Optionnel ; non défini par défaut.}

``auth.ntlm.domain`` et ``auth.ntlm.workstation`` sont tous deux non définis par défaut,
ce qui construit exactement les identifiants que ce connecteur a toujours construits.
Écrire le domaine dans le nom d'utilisateur sous la forme ``DOMAIN\user`` continue de
fonctionner. Définir ``auth.ntlm.domain`` envoie le domaine comme champ NTLM distinct,
ce qui est ce que veut un serveur qui rejette la forme combinée.

Kerberos (SPNEGO)
-----------------

**Périmètre pris en charge :** une seule JVM crawler, un ``krb5.conf`` par instance
Fess, un keytab ou un mot de passe, aucune délégation, aucune liaison de canal (channel
binding), et mutuellement exclusif avec NTLM et OAuth. Tout ce qui sort de ce périmètre
n'est pas pris en charge.

::

    auth.kerberos.principal={Principal client, écrit sous la forme user@REALM. Le définir active Kerberos.}
    auth.kerberos.keytab={Chemin vers un keytab contenant une clé pour le principal. Mutuellement exclusif avec auth.kerberos.password.}
    auth.kerberos.password={Mot de passe du principal. Utilisé uniquement si aucun keytab n'est défini.}
    auth.kerberos.strip_port={true ou false. Supprime le port du nom de principal de service. Par défaut true.}
    auth.kerberos.use_canonical_hostname={true ou false. Résout l'hôte cible vers son nom canonique pour le nom de principal de service. Par défaut false.}
    auth.kerberos.krb5_conf={Chemin vers un krb5.conf. Appliqué uniquement si java.security.krb5.conf n'est pas déjà défini.}
    auth.kerberos.debug={true ou false. Sortie de débogage de Krb5LoginModule. Par défaut false.}

- **``krb5.conf`` doit être placé dans ``jvm.crawler.options``**, sous la forme
  ``-Djava.security.krb5.conf=/path/to/krb5.conf``. Le crawl des data stores s'exécute
  dans le **processus enfant** du crawler, donc définir ce paramètre à un endroit qui
  n'affecte que le webapp n'a aucun effet, et un redémarrage du webapp ne prend pas en
  compte un changement - le job de crawl doit être réexécuté.
  ``auth.kerberos.krb5_conf`` est une commodité pour le cas où rien n'a encore défini
  cette propriété : il **n'écrase jamais une valeur déjà définie**, car cette propriété
  est globale à la JVM et une seule JVM crawler exécute toutes les configurations de
  données d'un job de crawl. Lorsqu'il renonce à écraser, il journalise un avertissement
  nommant les deux chemins.
- **Placez ``udp_preference_limit = 1`` dans la section ``[libdefaults]`` de
  ``krb5.conf``.** Sans cela, le JDK tente d'abord l'UDP, et lorsque le KDC ne répond
  pas (injoignable, un pare-feu qui bloque l'UDP 88, ou une réponse plus grande que la
  taille du datagramme), il retente trois fois à trente secondes d'intervalle avant de
  basculer sur TCP. Un crawl qui semble bloqué pendant environ une minute et demie par
  authentification, sans rien dans le journal, en est généralement la cause.
- **Écrivez toujours le principal sous la forme ``user@REALM``.** ``default_realm`` est
  global à la JVM, et plusieurs fermes SharePoint dans des royaumes (realms) différents
  peuvent avoir à partager un seul ``krb5.conf``, donc un simple ``user`` se résout par
  rapport au royaume que ce fichier indique, quel qu'il soit.
- **``auth.kerberos.use_canonical_hostname`` vaut ``false`` par défaut**, délibérément à
  l'inverse du défaut propre d'Apache HttpClient. Une fois activé, l'hôte cible passe
  par une résolution DNS inverse avant que le nom de principal de service ne soit
  construit, ce qui, sous des mappages d'accès alternatifs ou derrière un équilibreur de
  charge, peut produire un nom pour lequel aucun SPN n'est enregistré - et l'échec
  résultant ne dit rien sur le DNS. Ne l'activez que si le SPN est réellement enregistré
  sous le nom canonique.
- **IIS Extended Protection réglé sur ``tokenChecking=Require`` ne peut pas
  fonctionner.** Ni Apache HttpClient 4.5 ni 5.x ne prennent en charge la liaison de
  canal (channel binding). IIS règle ce paramètre par défaut sur ``None``, donc ce n'est
  généralement pas rencontré, et il n'existe aucun contournement lorsque c'est le cas.
- **Le ticket est obtenu une seule fois, lors de la construction du client HTTP du
  crawl, et n'est jamais renouvelé.** Un crawl qui dure plus longtemps que la durée de
  vie du ticket commence à échouer à s'authentifier en cours de route.
- **``auth.kerberos.password`` est stocké et affiché en texte clair**, exactement comme
  ``auth.ntlm.password``. Fess n'a aucun mécanisme de masquage pour les paramètres des
  gestionnaires de data store ; l'écran d'édition de la configuration de données les
  affiche dans une zone de texte brut. Préférez ``auth.kerberos.keytab``, et donnez au
  fichier keytab des permissions restrictives.
- ``auth.kerberos.debug=true`` fait écrire ``Krb5LoginModule`` sur la sortie standard du
  processus crawler, et non dans le journal de Fess.

OAuth (ACS)
-----------

::

    auth.oauth.client_id={ID client OAuth}
    auth.oauth.client_secret={Secret client OAuth}
    auth.oauth.tenant={Nom du tenant, sans .sharepoint.com}
    auth.oauth.realm={ID de royaume/répertoire Azure AD}

Définir ``auth.oauth.client_id`` active un flux client-credentials (application
uniquement) vers le Windows Azure Access Control Service,
``https://accounts.accesscontrol.windows.net/{realm}/tokens/OAuth/2``. Le jeton d'accès
est récupéré une seule fois, lors de la construction du client HTTP du crawl, appliqué
comme en-tête ``Authorization`` ``Bearer`` sur chaque requête, et rafraîchi puis retenté
une seule fois en cas de 401. **Microsoft a déprécié ACS et prévu son retrait** ; ce
connecteur journalise un avertissement à ce sujet à chaque crawl configuré avec OAuth.
Aucun flux d'enregistrement d'application Entra ID (par certificat ou secret client)
n'est implémenté ici - seule l'authentification ACS application uniquement, historique
(legacy), est prise en charge.

Seule la présence de ``auth.oauth.client_id`` est vérifiée avant l'activation d'OAuth ;
``client_secret``, ``tenant`` et ``realm`` sont lus inconditionnellement et peuvent
rester vides en silence s'ils sont omis, ce qui casse l'acquisition du jeton sans
message de validation dédié.

**``sp.version=2013`` et OAuth n'ont jamais fonctionné ensemble.** Tous les appels d'API
SharePoint 2013 effectués par ce connecteur passent par le client XML/Atom, et aucun
chemin de code de ce client n'attache de jeton OAuth à une requête - donc si les deux
sont définis, chaque requête est envoyée sans authentification. Le crawl journalise un
avertissement le disant explicitement et mentionnant ``auth.ntlm.*`` comme alternative ;
cela ne fait pas échouer le job. Utilisez ``auth.ntlm.*`` pour SharePoint 2013.

Permissions
===========

``role.skip=true`` (par défaut ``false``) ignore complètement la récupération des
permissions par élément : aucun appel ``GetListItemRole`` n'est effectué, la clé
``role`` n'est jamais définie pour l'élément, et le document finit par ne porter que le
paramètre de permission statique de la configuration de données et, si configuré,
``default_permissions`` - aucune permission dérivée de SharePoint ne l'atteint.

Lorsque les rôles sont récupérés, les utilisateurs, groupes de sécurité et groupes
SharePoint propres à SharePoint sont développés et mappés vers les rôles de recherche
Fess :

- Un compte ou groupe **AD sur site** (nom de connexion contenant une barre oblique
  inverse, ne commençant pas par un préfixe de revendication (claim) Azure) est mappé
  via les assistants de rôle utilisateur/groupe AD standard.
- Un compte **Azure AD (Entra ID)** (nom de connexion commençant par
  ``i:0#.f|membership|``) est mappé **deux fois** - une fois par sa valeur de
  revendication Azure complète, une fois par la partie compte AD précédant le ``@`` dans
  cette revendication - de sorte qu'un rôle de style Entra ID et un rôle de style AD
  sont tous deux ajoutés pour le même utilisateur. Un groupe de sécurité marqué comme
  Azure (par l'un de plusieurs préfixes de style revendication, y compris le groupe
  spécial « tout le monde » ``spo-grid-all-users``) est mappé de la même façon, sous les
  deux formes.
- Un **groupe SharePoint** voit sa propre appartenance (utilisateurs, groupes de
  sécurité, groupes imbriqués) développée récursivement, avec une protection contre les
  groupes déjà visités pour arrêter la récursion infinie entre des groupes qui se
  contiennent mutuellement.

``default_permissions`` (séparés par des virgules) est fusionné **après** tout ce qui
précède, et s'applique même lorsque SharePoint n'a renvoyé aucun rôle pour l'élément -
le cas produit aussi bien par ``role.skip=true`` que par « SharePoint n'a rien
renvoyé ». La liste de rôles finale est l'union du paramètre de permission statique de
la configuration de données, des rôles dérivés de SharePoint (sauf s'ils sont ignorés)
et de ``default_permissions``, après suppression des doublons.

Sous-sites et chemins d'accès gérés
===================================

Définir ``site.path`` utilise tel quel le chemin d'accès géré relatif au serveur
indiqué, à la place du préfixe codé en dur ``/sites/``, et ``site.name`` n'est plus
requis.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scénario
     - Configuration
   * - Collection de sites racine
     - ``site.path=/``
   * - Le site ``/teams/eng``
     - ``site.path=/teams/eng``
   * - La forme classique
       ``/sites/mysite/``
     - ``site.name=mysite`` (laisser ``site.path`` non défini)

Définir ``site.crawl_subsites`` (par défaut ``false``) fait qu'un crawl de site complet
- un crawl où ni ``site.list_name`` ni ``site.doclib_path`` n'est défini - parcourt
récursivement les sous-sites du site, découverts via ``_api/web/webinfos``. Le laisser
non défini fait que le crawl continue d'émettre exactement les mêmes requêtes
qu'auparavant, y compris de ne jamais demander ``webinfos``.

Les documents d'un sous-site atterrissent dans la même configuration de données que ceux
du site racine, sous leurs propres chemins relatifs au serveur - rien dans l'index ne
marque un document comme provenant d'un sous-site plutôt que de la racine.

``site.max_depth`` (par défaut ``10``) limite le nombre de niveaux de sous-sites en
dessous du site racine qui sont crawlés une fois ``site.crawl_subsites=true``. Le site
racine lui-même est à la profondeur 0, donc ``site.max_depth=1`` crawle les enfants
directs de la racine et rien de plus. Le définir en dessous de ``1`` alors que
``site.crawl_subsites=true`` désactive de fait la fonctionnalité - aucun sous-site n'est
crawlé - et un avertissement est journalisé au démarrage du crawl.

Activer le crawl des sous-sites **multiplie le temps total du crawl** par environ le
nombre de sous-sites découverts (limité par ``site.max_depth``) : chacun reçoit son
propre listing complet de dossiers, son propre listing de listes et, s'il n'est pas à la
limite de profondeur, son propre appel ``webinfos``, en plus de tout ce que le crawl du
site racine effectue déjà.

``number_of_threads`` et ``readInterval``, décrits dans `Crawl parallèle et charge`_,
s'appliquent à un crawl récursif de sous-sites de la même façon qu'à tout autre crawl.

Crawl parallèle et charge
=========================

``number_of_threads`` (par défaut ``1``) est le nombre de cibles de crawl traitées
simultanément. Avec la valeur par défaut, le crawl s'exécute exactement comme avant :
chaque cible est crawlée sur le thread de crawl et **aucun pool de threads n'est créé**.

La valeur est **plafonnée au double du nombre de processeurs** de la machine exécutant
Fess, de sorte qu'une configuration de données ne peut pas demander plus de parallélisme
que l'hôte ne peut en servir. Une valeur inférieure à ``1`` - ou une valeur vide ou
impossible à analyser - retombe à ``1`` plutôt que d'être honorée ou de faire échouer le
job. Une valeur qui a été plafonnée, ou une valeur inférieure à ``1``, est journalisée
avec à la fois la valeur demandée et la valeur réelle ; une valeur impossible à analyser
journalise un avertissement. Une valeur vide ne journalise rien, car un champ vide
signifie simplement que le paramètre n'a pas été défini.

Le pool de connexions HTTP est dimensionné en conséquence. Apache HttpClient n'autorise
par défaut que 2 connexions par route, et un crawl entier constitue une seule route :
sans l'augmenter, chaque thread au-delà du deuxième passerait le crawl à attendre une
connexion plutôt qu'à émettre des requêtes.

**``readInterval`` continue de cadencer la remise des documents, un document par
intervalle, quelle que soit sa valeur.** Les threads accélèrent la découverte et la
récupération par le crawl ; ils n'accélèrent pas l'arrivée des documents à l'indexeur.
C'est voulu : diviser l'intervalle configuré par l'opérateur par le nombre de threads
multiplierait exactement la charge que cet intervalle est censé limiter. Un worker qui
termine un document pendant que les précédents sont encore en cours de remise attend
simplement.

Ce que l'augmentation de ``number_of_threads`` **multiplie** réellement, c'est le débit
de requêtes vers SharePoint. L'attente de repli (backoff) sur 503 et l'attente liée à
``X-SharePointHealthScore`` décrites ci-dessous sont appliquées par cible de crawl, sur
le thread qui la crawle, donc ``n`` threads génèrent jusqu'à ``n`` fois les requêtes
d'un crawl mono-thread - y compris pendant une période où la ferme signale qu'elle est
occupée. Sur une ferme sur site, augmentez cette valeur progressivement.

Deux facteurs plafonnent ce que des threads supplémentaires apportent réellement :

- **La première fois que l'appartenance de chaque groupe SharePoint est lue, elle l'est
  par un seul thread à la fois.** Les permissions sont résolues via un cache partagé par
  tout le crawl, protégé par un verrou unique maintenu pendant les recherches des
  membres d'un groupe. Ce verrou empêche qu'un thread ne transmette à un autre un groupe
  dont les membres sont encore en cours de lecture, ce qui indexerait les éléments que
  ce groupe protège sans aucune de ses permissions. Une fois un groupe mis en cache,
  toute référence ultérieure à celui-ci est une recherche peu coûteuse ; il s'agit donc
  d'un **coût de cache froid** : le crawl d'un site comportant de nombreux groupes
  distincts passe ses premières minutes plus proche d'un fonctionnement mono-thread que
  de ``n`` threads, tandis qu'un site dont les éléments partagent une poignée de groupes
  le remarque à peine. ``role.skip=true``, qui ne lit aucune permission, évite
  entièrement ce coût.
- La découverte est séquentielle par site : les listings de dossiers et de listes d'un
  site constituent une seule cible de crawl, donc les threads n'ont rien à se répartir
  tant que cette cible n'est pas terminée et que ce qu'elle a trouvé n'est pas mis en
  file d'attente.

**Une réponse 503** est retentée comme n'importe quelle autre erreur, jusqu'à
``retry_limit`` fois, mais avec une attente croissante avant chaque nouvelle tentative :
2 secondes, puis 4, puis 8, en doublant jusqu'à un plafond de 30 secondes, chacune
randomisée entre 70 et 129 % de cette valeur. Une cible de crawl qui continue de
renvoyer 503 paie cette attente avant chaque nouvelle tentative qu'elle obtient
réellement, mais pas après la dernière.

**Chaque réponse** - qu'elle réussisse ou non, y compris une page d'un listing que le
crawl s'apprête à écarter - est inspectée pour l'en-tête de réponse
``X-SharePointHealthScore`` (0 = inactif à 10 = très occupé). Un score de 9 ou plus fait
attendre le crawl avant toute autre action : un score de 9 attend environ 2 secondes, un
score de 10 environ 4 secondes, et ainsi de suite, en doublant pour chaque point au-delà
de 9. **Cela s'accumule sur l'ensemble du crawl, sans plafond global** : une ferme se
maintenant à un score de santé de 9 sous charge soutenue ajoute environ 2 secondes à
*chaque requête* effectuée par ce connecteur - y compris chaque page de chaque listing
de dossiers et de listes - ce qui peut transformer un crawl qui prendrait autrement des
heures en un crawl nettement plus long. Si un crawl ralentit de façon inattendue d'un
ordre de grandeur, vérifiez le score de santé de la ferme durant cette période avant de
supposer autre chose.

Exemples d'utilisation
======================

Tous ces exemples supposent NTLM. Pour utiliser Kerberos ou OAuth à la place, voir
`Authentification`_ et remplacer les lignes ``auth.ntlm.*``.

Crawl de liste
--------------

Paramètres :

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.list_name=Tasks

Script :

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Crawl de bibliothèque de documents
----------------------------------

Paramètres :

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

Script :

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Crawl d'un site ``/teams/``
---------------------------

``site.path`` permet de pointer directement vers une bibliothèque de documents sur un
site situé sous un chemin d'accès géré autre que ``/sites/``.

Paramètres :

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/teams/eng
    site.doclib_path=/Shared Documents

Script :

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Crawl récursif des sous-sites
-----------------------------

Démarre à la collection de sites racine et suit les sous-sites jusqu'à 3 niveaux de
profondeur.

Paramètres :

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/
    site.crawl_subsites=true
    site.max_depth=3

Script :

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

Limitations
===========

- **Aucun crawl incrémental ou différentiel d'aucune sorte.** Il n'existe dans ce
  connecteur aucun jeton de changement, aucune delta-query, ni aucun filtrage « modifié
  depuis » - chaque exécution effectue un listing complet de chaque liste, dossier et
  fichier qu'elle est configurée pour atteindre. ``delete_old_docs`` contrôle uniquement
  si les documents que le crawl complet en cours n'a pas revus sont supprimés après coup
  ; il s'agit d'un nettoyage a posteriori, pas d'une récupération incrémentale.
- **``%`` et ``#`` dans les noms de fichiers/dossiers** sont pris en charge sur le
  chemin de code par défaut (non ``2013``). Seuls SharePoint Server 2019 et la
  Subscription Edition acceptent ces deux caractères dans un nom ; 2016 les refuse
  toujours explicitement, et 2013 également. Le chemin par défaut atteint un tel
  fichier via les points de terminaison ``...ByServerRelativePath(decodedUrl=...)``,
  qui reçoivent le chemin décodé, et l'exploration échappe les deux caractères dans
  le lien sous lequel elle indexe le fichier. **``sp.version=2013`` ne permet pas
  d'atteindre un tel fichier**, car ce chemin utilise les points de terminaison plus
  anciens ``...ByServerRelativeUrl(...)``, qui lisent leur argument comme une URL
  déjà encodée. Il s'agit d'une limite délibérée et non d'une lacune : une ferme
  SharePoint 2013 ne peut pas contenir un tel nom. Cela ne compte donc que si
  ``sp.version=2013`` est pointé vers un serveur 2019 ou Subscription Edition, ce
  qui n'est pas une configuration à utiliser. Voir
  `Use of # and % characters in file and folder names
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2019>`__
  et `File names - expanded support for special characters
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2016>`__.
- **IIS Extended Protection avec ``tokenChecking=Require`` ne peut pas être pris en
  charge.** Ni Apache HttpClient 4.5 ni 5.x n'implémentent la liaison de canal (channel
  binding), dont dépend Extended Protection en mode ``Require``. IIS règle ce paramètre
  par défaut sur ``None``, donc la plupart des fermes ne sont pas concernées, et il
  n'existe aucun contournement pour une ferme où il est réglé sur ``Require``.
- **Les mots de passe dans les paramètres de la configuration de données sont stockés et
  affichés en texte clair.** Cela s'applique aussi bien à ``auth.ntlm.password`` qu'à
  ``auth.kerberos.password`` : Fess n'a aucun mécanisme de masquage pour les paramètres
  des gestionnaires de data store, et l'écran d'édition de la configuration de données
  les affiche dans une zone de texte brut. Préférez ``auth.kerberos.keytab`` à
  ``auth.kerberos.password`` là où Kerberos est disponible, et donnez au fichier keytab
  des permissions restrictives.
- **``sp.version=2013`` et OAuth n'ont jamais fonctionné ensemble.** Tout appel d'API
  SharePoint 2013 passe par le client XML/Atom, et aucun chemin de code de ce client
  n'attache de jeton OAuth à une requête, donc si les deux sont définis, chaque requête
  est envoyée sans authentification. Utilisez ``auth.ntlm.*`` pour SharePoint 2013.
- **Les chemins d'accès gérés autres que ``/sites/`` et celui défini via ``site.path``
  ne sont toujours pas découverts automatiquement.** ``site.crawl_subsites`` ne parcourt
  récursivement qu'à partir du site racine que vous configurez, et ``site.path``
  n'atteint que le seul chemin d'accès géré que vous définissez, pas tous les chemins
  d'accès gérés de la ferme.

Dépannage
=========

L'authentification échoue silencieusement
-----------------------------------------

**Symptôme** : les requêtes reviennent en 401 (ou similaire) sans rien de clair dans le
journal pour expliquer pourquoi

**Points à vérifier** :

1. Vérifiez si plus d'une des options ``auth.kerberos.principal``, ``auth.ntlm.user`` et
   ``auth.oauth.client_id`` est définie - en définir deux ou plus fait échouer le job
   avec une erreur de validation avant que le crawl ne démarre
2. Pour Kerberos, confirmez que ``-Djava.security.krb5.conf=...`` est défini dans
   ``jvm.crawler.options``. Le définir à un endroit qui n'affecte que le webapp n'a
   aucun effet. Après l'avoir modifié, réexécutez le job de crawl - redémarrer le webapp
   ne le prend pas en compte
3. Pour Kerberos, confirmez que ``udp_preference_limit = 1`` est défini dans la section
   ``[libdefaults]`` de ``krb5.conf``. Sans cela, un KDC qui ne répond pas peut faire
   durer chaque authentification environ 90 secondes (trois tentatives UDP de 30
   secondes) sans rien dans le journal
4. Confirmez que le principal est écrit sous la forme ``user@REALM`` - un simple
   ``user`` se résout par rapport au ``default_realm`` que le ``krb5.conf`` partagé
   indique
5. Pour OAuth, confirmez que ``client_secret``, ``tenant`` et ``realm`` ne sont pas
   vides - seule la présence de ``client_id`` est validée, donc les autres peuvent être
   vides en silence
6. Confirmez qu'IIS Extended Protection n'est pas réglé sur ``tokenChecking=Require`` -
   il n'existe aucun contournement pour ce paramètre
7. Pour un crawl de longue durée, vérifiez s'il n'a commencé à échouer qu'à mi-parcours
   - le ticket Kerberos est obtenu une seule fois à la construction du client HTTP et
   n'est jamais renouvelé, donc un crawl qui dépasse la durée de vie du ticket commence
   à échouer en cours de route

Le crawl est lent (503 et le Health Score)
------------------------------------------

**Symptôme** : le crawl prend beaucoup plus de temps que prévu, ou expire

**Points à vérifier** :

1. Vérifiez le ``X-SharePointHealthScore`` de la ferme SharePoint pendant la période de
   ralentissement. Un score de 9 ou plus ajoute une attente avant chaque requête
   (environ 2 secondes à 9, environ 4 à 10, en doublant ensuite, sans plafond global),
   ce qui peut transformer un crawl qui devrait prendre des heures en un crawl bien plus
   long
2. Vérifiez la présence de réponses 503 répétées. Une réponse 503 est retentée jusqu'à
   ``retry_limit`` fois, en attendant 2, puis 4, puis 8 secondes (plafonné à 30) avant
   chaque nouvelle tentative
3. Vérifiez si ``number_of_threads`` a été augmenté de façon excessive. Plus de threads
   signifie à peu près proportionnellement plus de requêtes vers SharePoint, ce qui peut
   pousser le score de santé plus haut. Augmentez-le progressivement sur une ferme sur
   site
4. Si ``site.crawl_subsites=true``, gardez à l'esprit que le temps total du crawl croît
   à peu près avec le nombre de sous-sites découverts - envisagez de réduire la portée
   avec ``site.max_depth``

Rien n'est indexé
-----------------

**Symptôme** : le crawl se termine normalement, mais la recherche ne renvoie aucun
résultat

**Points à vérifier** :

1. Vérifiez le journal du crawler pour des erreurs ou avertissements (réglez
   ``org.codelibs.fess.ds`` sur ``DEBUG`` dans
   ``app/WEB-INF/env/crawler/resources/log4j2.xml``)
2. Vérifiez ``url``, ``site.name`` (ou ``site.path``) et ``site.list_name`` pour des
   fautes de frappe - rappelez-vous que ``site.name`` n'est pas nécessaire une fois
   ``site.path`` défini
3. Confirmez que l'authentification réussit effectivement (pas de 401) - une requête qui
   ne s'authentifie jamais est une cause bien plus fréquente qu'un ``role.skip`` ou
   ``default_permissions`` mal configuré
4. Si ``include_pattern`` ou ``exclude_pattern`` est défini, rappelez-vous qu'ils
   correspondent à un chemin relatif au serveur (pour un fichier de bibliothèque de
   documents ou une pièce jointe d'élément de liste) ou au ``FileRef`` (pour un élément
   de liste) - pas à l'URL affichée dans les résultats de recherche. Vérifiez qu'un
   motif n'a pas été écrit pour une URL complète
5. Vérifiez si ``supported_mimetypes`` ou ``max_content_length`` exclut les fichiers que
   vous attendez de voir
6. Vérifiez si ``site.exclude_list`` ou ``site.exclude_folder`` exclut involontairement
   la cible

Informations de référence
=========================

- :doc:`ds-overview` - Aperçu des connecteurs Data Store
- :doc:`ds-microsoft365` - Connecteur Microsoft 365 (pour SharePoint Online)
- :doc:`../../admin/dataconfig-guide` - Guide de configuration Data Store
- :doc:`../../admin/plugin-guide` - Guide de gestion des plugins
