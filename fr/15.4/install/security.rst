========================
Configuration de la sécurité
========================

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
2. Cliquez sur « Système » → « Utilisateur »
3. Sélectionnez l'utilisateur ``admin``
4. Définissez un mot de passe fort
5. Cliquez sur le bouton « Mettre à jour »

**Politique de mot de passe recommandée :**

- Minimum 12 caractères
- Inclure des majuscules, des minuscules, des chiffres et des symboles
- Éviter les mots du dictionnaire
- Modifier régulièrement (tous les 90 jours recommandés)

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

5. Mise à jour de la configuration de |Fess| pour ajouter les informations d'authentification OpenSearch ::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200
       SEARCH_ENGINE_USERNAME=admin
       SEARCH_ENGINE_PASSWORD=<mot_de_passe_fort>

Pour plus de détails, consultez `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__.

Activation de HTTPS
-------------------

La communication HTTP n'est pas chiffrée, ce qui présente des risques d'écoute et de falsification. Utilisez obligatoirement HTTPS dans les environnements de production.

**Méthode 1 : Utilisation d'un proxy inverse (recommandé)**

Placez Nginx ou Apache devant |Fess| pour terminer HTTPS.

Exemple de configuration Nginx ::

    server {
        listen 443 ssl http2;
        server_name votre-domaine-fess.com;

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

Ajoutez ce qui suit à ``system.properties`` ::

    server.ssl.enabled=true
    server.ssl.key-store=/path/to/keystore.p12
    server.ssl.key-store-password=<mot_de_passe>
    server.ssl.key-store-type=PKCS12

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

Contrôle d'accès basé sur les rôles (RBAC)
-------------------------------------------

|Fess| prend en charge plusieurs rôles d'utilisateur. Conformément au principe du moindre privilège, accordez uniquement les privilèges minimums nécessaires aux utilisateurs.

**Types de rôles :**

- **Administrateur** : Tous les privilèges
- **Utilisateur général** : Recherche uniquement
- **Administrateur explorateur** : Gestion de la configuration d'exploration
- **Éditeur de résultats de recherche** : Modification des résultats de recherche

**Procédure :**

1. Cliquez sur « Système » → « Rôle » dans l'écran d'administration
2. Créez les rôles nécessaires
3. Attribuez des rôles aux utilisateurs dans « Système » → « Utilisateur »

Activation des journaux d'audit
--------------------------------

Les journaux d'audit sont activés par défaut pour enregistrer l'historique des opérations du système.

Activation des journaux d'audit dans le fichier de configuration (``log4j2.xml``) ::

    <Logger name="org.codelibs.fess.audit" level="info" additivity="false">
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

- [ ] Contrôle d'accès basé sur les rôles configuré
- [ ] Comptes utilisateurs inutiles supprimés
- [ ] Politique de mot de passe configurée

Surveillance et journalisation
-------------------------------

- [ ] Journaux d'audit activés
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
