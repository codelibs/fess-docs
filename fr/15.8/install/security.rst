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

   Une fois le mot de passe modifié à partir de ``admin``, il n'est plus possible de le redéfinir avec une valeur aussi simple que ``admin`` (une liste noire de mots de passe administrateur est configurée via ``password.invalid.admin.passwords``). Vous pouvez également modifier le mot de passe initial de l'utilisateur ``admin`` avant le premier démarrage en définissant ``index.user.initial_password`` dans ``fess_config.properties``.

**Politique de mot de passe recommandée :**

|Fess| dispose d'une fonctionnalité intégrée qui impose des exigences de longueur minimale/maximale et de types de caractères pour le mot de passe. Configurez les propriétés suivantes dans ``fess_config.properties`` (les valeurs par défaut sont indiquées entre parenthèses) :

- ``password.min.length`` (par défaut : ``8``) : Longueur minimale. Une valeur de 12 caractères ou plus est recommandée.
- ``password.max.length`` (par défaut : ``100``) : Longueur maximale.
- ``password.require.uppercase`` (par défaut : ``false``) : Exiger des lettres majuscules.
- ``password.require.lowercase`` (par défaut : ``false``) : Exiger des lettres minuscules.
- ``password.require.digit`` (par défaut : ``false``) : Exiger des chiffres.
- ``password.require.special.char`` (par défaut : ``false``) : Exiger des symboles.

.. note::

   Par défaut, la longueur minimale est de ``8`` caractères et toutes les exigences de type de caractères sont désactivées. Pour renforcer la sécurité des mots de passe, définissez explicitement les propriétés ci-dessus. Notez que |Fess| ne dispose pas de fonctionnalité d'expiration des mots de passe (changement périodique forcé) ; si vous souhaitez imposer un changement périodique du mot de passe comme règle opérationnelle, faites-le manuellement.

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

   Spécifiez les informations d'authentification via les propriétés suivantes dans ``fess_config.properties`` (il n'existe pas de variables d'environnement ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``) ::

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

**Méthode 2 : Configuration HTTPS directement dans Fess**

Ajoutez ce qui suit à ``tomcat_config.properties`` ::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.SSLEnabled=true
    tomcat.certificateKeystoreFile=[chemin vers le fichier keystore]
    tomcat.certificateKeystorePassword=[mot de passe spécifié lors de la création du fichier keystore]
    tomcat.certificateKeyAlias=[alias du certificat]
    tomcat.sslProtocol=[protocole SSL (ex. TLS)]
    tomcat.enabledProtocols=liste des protocoles activés (séparés par des virgules) (ex. TLSv1.2,TLSv1.1,TLSv1)

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

    $ sudo firewall-cmd --permanent --add-service=http
    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --remove-service=opensearch  # En cas de service personnalisé
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

Tous les autres rôles peuvent être librement créés depuis l'écran d'administration. Dans |Fess|, un rôle est une étiquette ne comportant qu'un nom, principalement utilisée pour le contrôle d'accès aux résultats de recherche (quels documents un utilisateur peut consulter). Un rôle en lui-même n'est pas lié à des permissions administratives spécifiques telles que « gérer les configurations d'exploration » ou « modifier les résultats de recherche ».

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

Mises à jour de sécurité régulières
------------------------------------

Veuillez appliquer régulièrement les mises à jour de sécurité de |Fess| et OpenSearch.

**Procédure recommandée :**

1. Vérifier régulièrement les informations de sécurité

   - `Informations sur les versions de Fess <https://github.com/codelibs/fess/releases>`__
   - `Avis de sécurité OpenSearch <https://opensearch.org/security.html>`__

2. Valider les mises à jour dans un environnement de test
3. Appliquer les mises à jour dans l'environnement de production

Protection des données
=======================

Chiffrement des sauvegardes
----------------------------

Les données de sauvegarde peuvent contenir des informations confidentielles. Veuillez chiffrer et stocker les fichiers de sauvegarde.

Exemple de sauvegarde chiffrée ::

    $ tar czf fess-backup.tar.gz /var/lib/opensearch /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

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

Si nécessaire, configurez les en-têtes de sécurité dans Nginx ou Apache ::

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'" always;

Liste de vérification de sécurité
==================================

Avant de déployer en environnement de production, veuillez vérifier la liste de contrôle suivante :

Configuration de base
---------------------

- [ ] Mot de passe administrateur modifié
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
