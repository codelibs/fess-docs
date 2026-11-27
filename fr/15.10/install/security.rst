============================
Configuration de la sécurité
============================

Cette page décrit les configurations de sécurité recommandées pour exploiter |Fess| en toute sécurité dans un environnement de production.

.. danger::

   **La sécurité est extrêmement importante**

   Dans les environnements de production, il est fortement recommandé de mettre en œuvre toutes les configurations de sécurité décrites sur cette page.
   Le non-respect des configurations de sécurité augmente les risques d'accès non autorisé, de fuite de données et de compromission du système.

Configurations de sécurité obligatoires
========================================

Modification du mot de passe administrateur
--------------------------------------------

Veuillez obligatoirement modifier le mot de passe administrateur par défaut (``admin`` / ``admin``).

**Procédure :**

1. Connexion à l'écran d'administration : http://localhost:8080/admin
2. Cliquez sur « Utilisateur » → « Utilisateur »
3. Sélectionnez l'utilisateur ``admin``
4. Définissez un mot de passe fort
5. Cliquez sur le bouton « Mettre à jour »

.. note::

   Une fois le mot de passe modifié à partir de ``admin``, il n'est plus possible de le redéfinir avec une valeur aussi simple que ``admin`` (une liste noire de mots de passe administrateur est configurée via ``password.invalid.admin.passwords``). Vous pouvez également modifier le mot de passe initial de l'utilisateur ``admin`` avant le premier démarrage en définissant ``index.user.initial_password`` dans ``fess_config.properties``. ``bin/fess-setup init`` la définit pour vous ; voir :doc:`fess-setup`.

.. note::

   Si vous vous connectez avec ``admin`` et le mot de passe initial, l'écran de changement de mot de passe s'affiche juste après la connexion. Il s'agit d'une invitation à changer le mot de passe, et non d'une obligation imposée côté serveur (la connexion est déjà établie et vous pouvez ouvrir l'interface d'administration sans changer le mot de passe). Pour garantir le changement du mot de passe, définissez le mot de passe initial avec ``bin/fess-setup init`` ou ``index.user.initial_password`` avant le premier démarrage.

**Politique de mot de passe recommandée :**

|Fess| dispose d'une fonctionnalité intégrée qui impose des exigences de longueur minimale/maximale et de types de caractères pour le mot de passe. Configurez les propriétés suivantes dans ``fess_config.properties`` (les valeurs par défaut sont indiquées entre parenthèses) :

- ``password.min.length`` (par défaut : ``8``) : Longueur minimale. Une valeur de 12 caractères ou plus est recommandée.
- ``password.max.length`` (par défaut : ``100``) : longueur maximale en caractères. Quelle que soit cette valeur, un mot de passe est aussi limité en octets UTF-8 par l'algorithme de hachage des mots de passe (voir ci-dessous).
- ``password.require.uppercase`` (par défaut : ``false``) : Exiger des lettres majuscules.
- ``password.require.lowercase`` (par défaut : ``false``) : Exiger des lettres minuscules.
- ``password.require.digit`` (par défaut : ``false``) : Exiger des chiffres.
- ``password.require.special.char`` (par défaut : ``false``) : Exiger des symboles.

.. note::

   Par défaut, la longueur minimale est de ``8`` caractères et toutes les exigences de type de caractères sont désactivées. Pour renforcer la sécurité des mots de passe, définissez explicitement les propriétés ci-dessus. Notez que |Fess| ne dispose pas de fonctionnalité d'expiration des mots de passe (changement périodique forcé) ; si vous souhaitez imposer un changement périodique du mot de passe comme règle opérationnelle, faites-le manuellement.

**Hachage des mots de passe et limite en octets :**

|Fess| stocke le mot de passe d'un utilisateur local sous forme de hachage. ``app.password.algorithm`` (par défaut : ``bcrypt``) sélectionne l'algorithme des mots de passe nouveaux et modifiés, et ``app.password.bcrypt.cost`` (par défaut : ``10``) définit le coût de BCrypt. Tant que ``app.password.upgrade.enabled`` vaut ``true`` (par défaut), un utilisateur dont le hachage stocké est plus ancien (un ancien hachage sans préfixe ``{id}``, le hachage d'un autre algorithme ou un hachage BCrypt de coût inférieur) reçoit un nouveau hachage à sa prochaine connexion réussie. L'algorithme est un composant : un plugin peut donc en fournir un autre (voir :ref:`webapp-plugin-password-encoder`).

La limite en octets appartient à l'algorithme. BCrypt ne lit que les 72 premiers octets d'un mot de passe en UTF-8 ; depuis 15.10, un mot de passe de plus de 72 octets est donc refusé lorsqu'on le définit (écran de gestion des utilisateurs, changement de mot de passe forcé du formulaire de connexion, ``/api/v2/auth/password`` et API d'administration) avec « Le mot de passe ne doit pas dépasser 72 octets. », quelle que soit la valeur que ``password.max.length`` (100 caractères par défaut) autorise. Un caractère non ASCII occupe plus d'un octet (3 octets pour la plupart des caractères japonais, chinois et coréens). Un compte dont le mot de passe a été défini auparavant avec plus de 72 octets continue de se connecter, car la vérification d'un mot de passe n'applique aucune limite de longueur. Toutefois, seuls ses 72 premiers octets sont comparés : n'importe quelle fin après le 72e octet est donc acceptée. Définir un nouveau mot de passe (72 octets au maximum) supprime ce défaut.

**Sessions après un changement de mot de passe :**

Lorsque le mot de passe d'un utilisateur local est modifié, que ce soit par l'utilisateur lui-même ou par un administrateur sur l'écran de gestion des utilisateurs ou via l'API REST d'administration, les autres sessions de connexion de cet utilisateur prennent fin à leur prochaine vérification (voir ci-dessous). Chaque session de connexion lit l'heure du dernier changement de mot de passe dans l'index des utilisateurs au plus une fois par ``password.changed.check.interval`` de ``fess_config.properties`` (par défaut : ``60`` secondes ; avec ``0`` ou moins, la vérification a lieu à chaque requête), de sorte que les autres sessions prennent fin dans ce délai, sur n'importe quel nœud. Les utilisateurs authentifiés par LDAP ou SSO ne sont pas concernés, car leurs mots de passe sont gérés en dehors de |Fess|.

**Sessions après une modification des rôles ou des groupes :**

Lorsque les rôles ou les groupes d'un utilisateur local sont modifiés après l'ouverture d'une session, la session de connexion de cet utilisateur prend fin. Cela couvre la modification de l'utilisateur (sur l'écran de gestion des utilisateurs ou via l'API REST d'administration) ainsi que la suppression d'un rôle ou d'un groupe que l'utilisateur possédait. L'intervalle de vérification est le même ``password.changed.check.interval`` (par défaut : ``60`` secondes) que pour un changement de mot de passe. Contrairement à un changement de mot de passe, la session qui a effectué la modification n'est pas une exception : par exemple, lorsqu'un administrateur modifie ses propres rôles, la session de l'administrateur prend fin elle aussi et il doit se reconnecter. Une session terminée est enregistrée dans le journal d'audit sous ``SESSION_END`` avec ``reason`` ``permissions_changed``. Les utilisateurs authentifiés par LDAP ou SSO ne sont pas concernés, car leurs rôles et groupes sont obtenus auprès du fournisseur d'identité à chaque connexion.

Modifier la clé de chiffrement
------------------------------

``app.cipher.key`` dans ``fess_config.properties`` est la clé qui chiffre les mots de passe enregistrés dans les configurations de crawl et de magasin de données. La valeur fournie (``___change__me___``) est publique. Si la clé conserve la valeur fournie, |Fess| écrit un avertissement dans ``fess.log`` au démarrage. Si la clé est vide, |Fess| interrompt le démarrage (voir :ref:`upgrade-1510-cipher-key`). |Fess| ne modifie pas la clé automatiquement.

Définissez-la avant le premier démarrage, avec le mot de passe initial de l'utilisateur ``admin`` ::

    $ bin/fess-setup init

Pour les packages RPM et DEB, exécutez ``/usr/share/fess/bin/fess-setup init``. La commande génère une clé aléatoire, ou prend celle donnée avec ``--cipher-key`` ; voir :doc:`fess-setup`. Pour la définir à la main, modifiez ``app.cipher.key`` dans ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` pour le package ZIP, ``/etc/fess/fess_config.properties`` pour les packages RPM et DEB). Avec la valeur par défaut de ``app.cipher.algorithm`` (``aes``), la clé doit comporter 16, 24 ou 32 caractères.

.. warning::

   Modifier la clé après l'enregistrement de mots de passe dans des configurations de crawl ou de magasin de données rend ces valeurs impossibles à déchiffrer. Conservez la clé avec vos sauvegardes de ``fess_config.properties`` et utilisez la même clé lorsque vous passez à une autre installation.

Activation du plugin de sécurité OpenSearch
--------------------------------------------

**Procédure :**

1. Supprimez ou commentez la ligne suivante dans ``opensearch.yml`` ::

       # plugins.security.disabled: true

2. Configuration du plugin de sécurité ::

       plugins.security.allow_default_init_securityindex: true
       plugins.security.authcz.admin_dn:
         - CN=admin,OU=SSL,O=Test,L=Test,C=DE

3. Configuration des certificats TLS/SSL

4. Redémarrage d'OpenSearch

5. Configurez la connexion à OpenSearch du côté |Fess|.

   Spécifiez l'URL de connexion via la variable d'environnement ``SEARCH_ENGINE_HTTP_URL`` (modifiez ``bin/fess.in.sh`` ou le fichier d'environnement du service ; la valeur par défaut provient de ``search_engine.http.url`` dans ``fess_config.properties``) ::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200

   Spécifiez les informations d'authentification via les propriétés suivantes dans ``fess_config.properties`` (les paquets ZIP, RPM et DEB n'ont pas les variables d'environnement ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD`` ; les images docker-fess les prennent en charge) ::

       search_engine.username=admin
       search_engine.password=<strong_password>

Pour plus de détails, consultez `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__.

Activation de HTTPS
-------------------

La communication HTTP n'est pas chiffrée, ce qui présente des risques d'écoute et de falsification. Utilisez obligatoirement HTTPS dans les environnements de production.

**Méthode 1 : Utilisation d'un proxy inverse (recommandé)**

Placez Nginx ou Apache devant |Fess| pour terminer HTTPS.

Exemple de configuration Nginx ::

    server {
        listen 443 ssl http2;
        server_name your-fess-domain.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

Lorsque TLS est terminé au niveau du proxy inverse, ajoutez également ce qui suit dans ``fess_config.properties`` afin que le cookie de session reçoive l'attribut ``Secure``. Redémarrez |Fess| après la modification. Ne le définissez pas si des utilisateurs accèdent aussi à |Fess| en HTTP simple, car la session ne peut alors plus être établie en HTTP ::

    session.cookie.secure=true

**Méthode 2 : Configuration HTTPS directement dans Fess**

Ajoutez ce qui suit à ``tomcat_config.properties`` ::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.SSLEnabled=true
    tomcat.certificateKeystoreFile=[chemin vers le fichier keystore]
    tomcat.certificateKeystorePassword=[mot de passe spécifié lors de la création du fichier keystore]
    tomcat.certificateKeyAlias=[alias du certificat]
    tomcat.sslProtocol=[protocole SSL (ex. TLS)]
    tomcat.enabledProtocols=liste des protocoles activés (séparés par des virgules) (ex. TLSv1.2,TLSv1.3)

Configurations de sécurité recommandées
========================================

Configuration du pare-feu
-------------------------

Ouvrez uniquement les ports nécessaires et fermez les ports inutiles.

**Ports à ouvrir :**

- **8080** (ou 443 pour HTTPS) : Interface Web |Fess| (si un accès externe est nécessaire)
- **22** : SSH (pour l'administration, uniquement depuis des adresses IP de confiance)

**Ports à fermer :**

- **9200, 9300** : OpenSearch (communication interne uniquement, bloquer l'accès externe)

Exemple de configuration Linux (firewalld) ::

    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --add-port=8080/tcp  # uniquement en cas d'accès direct à Fess sur le port 8080
    $ sudo firewall-cmd --reload

Restriction d'adresse IP ::

    $ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="8080" protocol="tcp" accept'

Configuration du contrôle d'accès
----------------------------------

Envisagez de restreindre l'accès à l'écran d'administration à des adresses IP spécifiques.

Exemple de restriction d'accès avec Nginx ::

    location /admin {
        allow 192.168.1.0/24;
        deny all;

        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
    }

Rôles et contrôle d'accès
--------------------------

|Fess| fournit deux rôles intégrés :

- ``admin`` : Rôle administrateur pouvant effectuer toutes les opérations, y compris sur l'écran d'administration.
- ``guest`` : Rôle attribué aux utilisateurs non authentifiés (anonymes).

Tous les autres rôles peuvent être librement créés depuis l'écran d'administration. Dans |Fess|, un rôle est une étiquette ne comportant qu'un nom, principalement utilisée pour le contrôle d'accès aux résultats de recherche (quels documents un utilisateur peut consulter). L'exception est un rôle nommé ``admin-`` suivi du nom d'un écran d'administration, tel que ``admin-user`` ou ``admin-scheduler`` : il permet à un utilisateur d'ouvrir cet écran, et la forme ``-view``, telle que ``admin-user-view``, donne un accès en lecture seule.

.. warning::

   Les rôles ``admin-*`` permettent de répartir les écrans d'administration courants entre plusieurs opérateurs, mais ils ne constituent pas une frontière de privilèges. Un utilisateur disposant de ``admin-user`` peut attribuer n'importe quel rôle existant, y compris le rôle administrateur, à n'importe quel utilisateur ; ``admin-accesstoken`` peut émettre un jeton d'accès avec la permission ``Radmin-api``, qui donne accès à l'ensemble de l'API Admin ; ``admin-scheduler`` peut exécuter des tâches de script sur le serveur, et ``admin-plugin`` peut installer des plugins. Traitez chaque rôle ``admin-*`` comme équivalent au rôle administrateur (``authentication.admin.roles``, valeur par défaut ``admin``) et accordez-le uniquement à des opérateurs de confiance.

Conformément au principe du moindre privilège, accordez le rôle administrateur (``admin``) uniquement aux utilisateurs effectuant des tâches d'administration, et ne l'accordez pas aux utilisateurs de recherche généraux.

**Procédure :**

1. Cliquez sur « Utilisateur » → « Rôle » dans l'écran d'administration
2. Créez les rôles nécessaires
3. Attribuez des rôles aux utilisateurs dans « Utilisateur » → « Utilisateur »

Journalisation d'audit
------------------------

L'historique des opérations du système, telles que l'authentification et les opérations d'administration, est enregistré par défaut sous forme de journal d'audit. Le journal d'audit est généré par le logger ``fess.log.audit`` défini dans ``log4j2.xml``, et sa destination de sortie par défaut est ``audit.log``.

Étant activé par défaut, aucune configuration supplémentaire n'est nécessaire. Pour personnaliser la destination de sortie ou le niveau de journalisation, modifiez la définition suivante dans ``log4j2.xml`` ::

    <Logger name="fess.log.audit" additivity="false" level="info">
        <AppenderRef ref="AuditFile"/>
    </Logger>

Chaque enregistrement d'audit est une ligne de champs ``key:value`` séparés par des tabulations (LTSV). Un enregistrement commence par ``action`` et se termine par ``ip`` (l'adresse IP du client) et ``time`` (UTC, ISO 8601). Lorsque ``app.audit.log.format`` vaut ``ecs``, ou qu'il est vide et que la variable d'environnement ``FESS_APP_TYPE`` vaut ``docker``, les enregistrements sont écrits en JSON ECS, avec les champs sous la forme ``labels.<key>``.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Action
     - Champs
     - Écrit lorsque
   * - ``LOGIN``
     - ``user``, ``permissions``
     - un utilisateur se connecte.
   * - ``LOGOUT``
     - ``user``, ``permissions``
     - un utilisateur se déconnecte.
   * - ``SESSION_END``
     - ``user``, ``reason``
     - |Fess| met fin de lui-même à une session de connexion, par opposition à une déconnexion demandée par l'utilisateur (c'est ``LOGOUT``). Un enregistrement est écrit pour chaque session terminée.
   * - ``LOGIN_FAILURE``
     - ``class``, ``user``
     - une connexion est refusée, sur le formulaire de connexion, dans l'API de connexion ou par SSO. Une connexion qu'un authentificateur SSO refuse par une exception est également enregistrée.
   * - ``ACCESS``
     - ``user``, ``path``, ``execute``, ``method``, ``id``
     - une requête atteint un écran d'administration ou l'API REST d'administration, avant l'exécution de l'action. Pour l'API REST d'administration, c'est après l'acceptation du jeton d'accès.
   * - ``ACCESS_DENIED``
     - ``user``, ``path``
     - une requête vers un écran d'administration est refusée en raison des rôles de l'utilisateur, ou une requête vers l'API REST d'administration est refusée par la vérification du jeton d'accès (l'API répond HTTP 401).
   * - ``UPDATE_PASSWORD``
     - ``user``, ``target``
     - un mot de passe est modifié : par un utilisateur depuis l'écran de connexion ou ``/api/v2/auth/password``, ou par un administrateur qui définit un nouveau mot de passe pour un utilisateur sur l'écran de gestion des utilisateurs ou via l'API REST d'administration.
   * - ``UPDATE_PERMISSION``
     - ``user``, ``permissions``
     - les permissions d'un utilisateur LDAP sont mises à jour.
   * - ``REGISTER_PASSKEY``
     - ``user``, ``target``, ``credentialId``
     - une clé d'accès est enregistrée.
   * - ``DELETE_PASSKEY``
     - ``user``, ``target``, ``credentialId``
     - une clé d'accès est supprimée : par l'utilisateur, ou par un administrateur sur l'écran de gestion des utilisateurs. Lorsqu'un administrateur définit un nouveau mot de passe pour un utilisateur, toutes les clés d'accès de cet utilisateur sont supprimées, et un enregistrement est écrit pour chaque clé d'accès.
   * - ``SCRIPT_EXECUTION``
     - ``scriptType``, ``source``, ``user``, ``result``, ``script``
     - un script est exécuté. Voir :doc:`../config/scripting-overview`.

- ``LOGIN_FAILURE`` : ``user`` est le nom d'utilisateur saisi et ``class`` le type des identifiants. Lorsqu'un authentificateur SSO refuse une connexion par une exception, aucun identifiant n'a été établi : l'enregistrement ne contient alors ni ``user`` ni ``class``, et rien de l'exception n'est écrit.
- ``ACCESS`` : ``user`` est l'utilisateur connecté lorsque la requête porte une session. Lorsque l'API REST d'administration est appelée avec un simple jeton d'accès et sans session, c'est le nom du jeton d'accès (le jeton lui-même n'est jamais écrit ; ``-`` lorsque le nom ne peut pas être obtenu). ``user`` de ``ACCESS_DENIED`` suit la même règle. ``method`` est la méthode HTTP. ``id`` est la valeur du paramètre de requête ``id``, écrit uniquement si la requête en comporte un (il n'est pas lu dans une requête de téléversement). Aucun autre paramètre de requête n'est écrit, car les formulaires d'administration contiennent des mots de passe et des clés.
- ``ACCESS_DENIED`` : pour une requête refusée vers l'API REST d'administration, seul le chemin de la requête est écrit. Ni le jeton d'accès ni le paramètre qui le transportait ne sont enregistrés.
- ``REGISTER_PASSKEY`` et ``DELETE_PASSKEY`` : ``user`` est l'utilisateur qui a effectué l'opération et ``target`` le nom de l'utilisateur propriétaire de la clé d'accès. ``credentialId`` correspond aux 8 premiers caractères de l'identifiant d'identification, suivis de ``...`` s'il est plus long. La clé de la clé d'accès n'est jamais écrite.
- ``UPDATE_PASSWORD`` : ``user`` est l'utilisateur qui a modifié le mot de passe et ``target`` le nom de l'utilisateur dont le mot de passe a été modifié. Le mot de passe et son empreinte ne sont jamais écrits, et une modification refusée n'écrit rien.
- ``SESSION_END`` : ``user`` est l'utilisateur dont la session a pris fin et ``reason`` en est la raison. ``password_changed`` : le mot de passe de l'utilisateur a été modifié après l'ouverture de la session. ``permissions_changed`` : les rôles ou les groupes de l'utilisateur local ont été modifiés après l'ouverture de la session (par la modification de l'utilisateur, ou par la suppression d'un rôle ou d'un groupe que l'utilisateur possédait). ``user_not_found`` : le document de l'utilisateur local n'existe plus, par exemple parce que l'utilisateur a été supprimé ou renommé. ``idp_session_ended`` : le fournisseur d'identité (IdP) a mis fin à sa session (le ``SessionNotOnOrAfter`` de SAML, voir :doc:`../config/sso-saml`, ou le back-channel logout d'OpenID Connect, voir :doc:`../config/sso-oidc`).

Mises à jour de sécurité régulières
------------------------------------

Veuillez appliquer régulièrement les mises à jour de sécurité de |Fess| et OpenSearch.

**Procédure recommandée :**

1. Vérifier régulièrement les informations de sécurité

   - `Informations sur les versions de Fess <https://github.com/codelibs/fess/releases>`__
   - `Avis de sécurité OpenSearch <https://github.com/opensearch-project/OpenSearch/security/advisories>`__

2. Valider les mises à jour dans un environnement de test
3. Appliquer les mises à jour dans l'environnement de production

Protection des données
=======================

Chiffrement des sauvegardes
----------------------------

Les données de sauvegarde peuvent contenir des informations confidentielles. Veuillez chiffrer et stocker les fichiers de sauvegarde.

Exemple de sauvegarde chiffrée ::

    $ tar czf fess-backup.tar.gz /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

Le répertoire de données d'un OpenSearch en cours d'exécution (``/var/lib/opensearch``) ne peut pas être sauvegardé de façon cohérente par simple copie de fichiers. Pour les données d'index, utilisez la `fonction d'instantanés d'OpenSearch <https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`__. Les données de configuration de |Fess| peuvent être téléchargées depuis la page de sauvegarde de l'interface d'administration (voir :doc:`../admin/backup-guide`).

Meilleures pratiques de sécurité
=================================

Principe du moindre privilège
------------------------------

- Ne pas exécuter Fess et OpenSearch en tant qu'utilisateur root
- Exécuter avec un compte utilisateur dédié
- Accorder les permissions minimales nécessaires sur le système de fichiers

Isolation réseau
----------------

- Placer OpenSearch sur un réseau privé
- Utiliser un VPN ou un réseau privé pour les communications internes
- Placer uniquement l'interface Web |Fess| dans la DMZ

Audit de sécurité régulier
---------------------------

- Vérifier régulièrement les journaux d'accès
- Détecter les modèles d'accès anormaux
- Effectuer régulièrement des analyses de vulnérabilité

Configuration des en-têtes de sécurité
---------------------------------------

|Fess| ajoute par défaut ``X-Frame-Options: SAMEORIGIN`` aux réponses HTML (``response.headers`` dans ``fess_config.properties``) ; il n'est donc pas nécessaire de l'ajouter dans le proxy.

Si nécessaire, configurez les en-têtes de sécurité dans Nginx ou Apache ::

    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

Liste de vérification de sécurité
==================================

Avant de déployer en environnement de production, veuillez vérifier la liste de contrôle suivante :

Configuration de base
---------------------

- [ ] Mot de passe administrateur modifié
- [ ] Clé de chiffrement (``app.cipher.key``) modifiée par rapport à la valeur fournie
- [ ] HTTPS activé
- [ ] Numéro de port par défaut modifié (optionnel)

Sécurité réseau
---------------

- [ ] Ports inutiles fermés par le pare-feu
- [ ] Accès à l'écran d'administration restreint par IP (si possible)
- [ ] Accès à OpenSearch restreint au réseau interne uniquement

Contrôle d'accès
----------------

- [ ] Rôles et permissions d'accès configurés de manière appropriée (rôle administrateur accordé uniquement aux utilisateurs nécessaires)
- [ ] Comptes utilisateurs inutiles supprimés
- [ ] Politique de mot de passe configurée

Surveillance et journalisation
-------------------------------

- [ ] Vérifié que les journaux d'audit sont activés
- [ ] Période de conservation des journaux configurée
- [ ] Mécanisme de surveillance des journaux établi (si possible)

Sauvegarde et récupération
---------------------------

- [ ] Planification de sauvegarde régulière configurée
- [ ] Données de sauvegarde chiffrées
- [ ] Procédure de restauration validée

Gestion des mises à jour et des correctifs
-------------------------------------------

- [ ] Mécanisme de réception des notifications de mises à jour de sécurité établi
- [ ] Procédure de mise à jour documentée
- [ ] Système de validation des mises à jour en environnement de test établi

Réponse aux incidents de sécurité
==================================

Procédure de réponse en cas d'incident de sécurité :

1. **Détection de l'incident**

   - Vérification des journaux
   - Détection de modèles d'accès anormaux
   - Vérification du comportement anormal du système

2. **Réponse initiale**

   - Identification de l'étendue de l'impact
   - Prévention de l'expansion des dommages (arrêt du service concerné, etc.)
   - Préservation des preuves

3. **Enquête et analyse**

   - Analyse détaillée des journaux
   - Identification du chemin d'intrusion
   - Identification des données potentiellement divulguées

4. **Récupération**

   - Correction des vulnérabilités
   - Restauration du système
   - Renforcement de la surveillance

5. **Suivi**

   - Création d'un rapport d'incident
   - Mise en œuvre de mesures préventives
   - Rapport aux parties prenantes

Informations de référence
==========================

- `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__
- `OWASP Top 10 <https://owasp.org/www-project-top-ten/>`__
- `CIS Benchmarks <https://www.cisecurity.org/cis-benchmarks/>`__

Pour toute question ou problème de sécurité, veuillez nous contacter :

- Issues : https://github.com/codelibs/fess/issues
- Assistance commerciale : https://www.n2sm.net/
