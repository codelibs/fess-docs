========================================
Intégrer la recherche à un site existant
========================================

Introduction
============

Lorsque vous souhaitez ajouter une recherche à un portail intranet ou à un site produit, il n'est pas réaliste de demander aux utilisateurs de retenir l'URL de Fess.
Ce que l'on attend, c'est une zone de recherche dans l'en-tête des pages qu'ils ouvrent tous les jours, et une page de résultats qui semble faire partie de ce site.

Dans cet article, nous utilisons Fess 15.9 pour essayer tour à tour les trois méthodes suivantes, qui se mettent toutes en place uniquement côté navigateur.

- Placer un formulaire de recherche HTML sur une page existante et afficher les résultats sur la page de recherche de Fess
- Utiliser Fess Site Search (FSS) pour afficher les résultats de recherche à l'intérieur d'une page du site existant
- Modifier l'apparence de la page de recherche de Fess (le thème) pour l'adapter au site existant

Nous configurons également le « mappage de chemin », qui remplace la destination des liens des résultats de recherche par des URL accessibles aux utilisateurs.

La création d'écrans personnalisés en appelant l'API de recherche depuis le serveur d'un système métier est traitée dans :doc:`guide-11`.

Prérequis
=========

- En suivant les étapes de :doc:`guide-02`, Fess 15.9 fonctionne avec Docker Compose à l'adresse ``http://localhost:8080/``, et au moins un contenu a déjà été exploré
- Un fichier HTML local qui tient lieu de site existant

Un site existant se trouve normalement sur une origine (la combinaison du schéma, de l'hôte et du port) différente de celle de Fess.
Pour reproduire cette condition dans cet article, exécutez la commande suivante dans le répertoire qui contient le fichier HTML, puis ouvrez-le à l'adresse ``http://localhost:8000/``.

::

    $ python3 -m http.server 8000

Choisir une méthode
===================

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - Méthode
     - Où les résultats de recherche s'affichent
     - Ce qu'il faut côté Fess
   * - Formulaire de recherche
     - Passage à la page de recherche de Fess (``/search``) et affichage sur celle-ci
     - Rien
   * - Fess Site Search
     - À l'intérieur d'une page du site existant
     - Le plugin ``fess-webapp-v1-api``
   * - Changement de thème
     - La page de recherche de Fess (avec une autre apparence)
     - Un ZIP de thème (ou les paramètres de [Général])

Le formulaire de recherche et le changement de thème peuvent être combinés.
Si la page sur laquelle arrivent les utilisateurs en quittant le site existant doit avoir la même apparence, configurez les deux.

Envoyer la recherche d'un formulaire vers la page de recherche de Fess
======================================================================

Placer le formulaire
--------------------

Écrivez le formulaire suivant à l'endroit de la page existante où vous voulez placer la zone de recherche.

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <button type="submit">Rechercher</button>
    </form>

Les termes de recherche sont envoyés à ``/search`` de Fess dans le paramètre ``q``, et les résultats s'affichent sur la page de recherche de Fess.
``maxlength`` correspond à la longueur maximale des termes de recherche côté Fess, ``query.max.length`` (valeur par défaut ``1000``).
En production, remplacez l'URL de ``action`` par l'URL de Fess à laquelle accèdent les utilisateurs.

Pour ne faire rechercher que les documents portant une étiquette donnée, envoyez aussi la valeur de l'étiquette dans ``fields.label``.

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <input type="hidden" name="fields.label" value="intranet">
      <button type="submit">Rechercher</button>
    </form>

``intranet`` est la valeur d'une étiquette créée dans [Robot d'exploration] > [Étiquette].
Si vous envoyez une valeur qui n'existe pas, vous obtenez 0 résultat.
Pour la création des étiquettes, consultez :doc:`guide-04`.

Vérifier
--------

1. Ouvrez le fichier HTML depuis ``http://localhost:8000/`` et recherchez un mot contenu dans un document exploré
2. Si le navigateur passe à ``http://localhost:8080/search?q=...`` et que les résultats s'affichent sur la page de recherche de Fess, c'est terminé

Si vous obtenez 0 résultat, recherchez le même mot dans la zone de recherche de ``http://localhost:8080/`` et comparez.
Si vous obtenez là aussi 0 résultat, le problème ne vient pas du formulaire, mais de l'exploration ou des permissions.

À propos des suggestions
------------------------

La page `Placement du formulaire de recherche <https://fess.codelibs.org/fr/stable/config/search-form-integration.html>`__ contient un exemple qui ajoute des suggestions au formulaire.
Cependant, ``/js/suggestor.js`` et ``/js/jquery-3.7.1.min.js``, que charge cet exemple, ne sont pas inclus dans Fess 15.9 ; l'exemple ne fonctionne donc pas tel quel en 15.9.
La partie formulaire (envoi de ``q`` à ``/search``) peut être utilisée telle quelle.

Pour afficher des suggestions dans la zone de recherche du site existant, utilisez l'une des solutions suivantes.

- Activer les suggestions dans Fess Site Search, présenté dans la section suivante
- Appeler ``/api/v2/suggest-words`` depuis votre propre script (pour l'utilisation de l'API, voir :doc:`guide-11`)

Une fois sur la page de recherche de Fess, le thème fourni avec Fess affiche les suggestions.

Afficher les résultats dans la page avec Fess Site Search
=========================================================

Fess Site Search (FSS) est un JavaScript qui affiche un formulaire de recherche et des résultats de recherche sur une page du site existant.
Les utilisateurs peuvent rechercher sans quitter le site existant.

Le JavaScript de FSS n'est pas distribué par Fess.
Téléchargez le fichier généré avec FSS JS Generator (https://fss-generator.codelibs.org/) et placez-le sur le serveur du site existant.

Installer le plugin de l'API v1
-------------------------------

FSS appelle ``/api/v1`` de Fess.
Fess 15.9 lui-même ne fournit que ``/api/v2`` ; ``/api/v1`` est fourni par le plugin ``fess-webapp-v1-api``.
Ce plugin n'est pas inclus dans l'image Docker.

Avec Docker Compose, ajoutez la ligne suivante dans ``environment`` de ``fess01`` dans ``compose.yaml``.

.. code-block:: yaml

    - "FESS_PLUGINS=fess-webapp-v1-api:15.9.0"

Si vous indiquez déjà d'autres plugins, ajoutez-les dans la même valeur, séparés par des espaces.
Après l'enregistrement, exécutez ``up -d`` en indiquant les deux fichiers Compose.
``fess01`` est recréé et le plugin est installé au démarrage.
Comme le conteneur est recréé, les paramètres modifiés dans [Système] > [Général] sont réinitialisés, comme lors d'un ``down`` (voir la section sur l'arrêt et le redémarrage dans :doc:`guide-02`).

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Vous pouvez aussi l'installer depuis [Système] > [Plugin] > [Installer] dans l'interface d'administration (un redémarrage de Fess est nécessaire après l'installation).
Avec Docker, toutefois, le plugin est placé dans le conteneur ; il disparaît donc lorsque le conteneur est recréé par ``down``.
Si vous l'indiquez dans ``FESS_PLUGINS``, il est réinstallé à chaque recréation.

Lorsque ``fess01`` est healthy, vérifiez que l'API répond.

::

    $ curl 'http://localhost:8080/api/v1/documents?q=fess'

Si un JSON contenant ``"record_count"`` est renvoyé, tout est prêt.
Si une erreur 404 est renvoyée, le plugin n'est pas installé.
Dans ce cas, un WARN commençant par ``No plugin serves the legacy API`` est écrit une seule fois dans ``fess.log``.
Si le plugin est installé mais qu'aucun JSON n'est renvoyé, vérifiez que « Réponse JSON » n'est pas désactivé dans [Système] > [Général].
Désactiver « Réponse JSON » empêche de répondre non seulement ``/api/v1``, mais aussi ``/api/v2``, ce qui rend inutilisable la page de recherche de Fess elle-même.

Générer et placer le JavaScript
-------------------------------

1. Ouvrez https://fss-generator.codelibs.org/, indiquez les couleurs, les polices, etc. dans le générateur, puis cliquez sur [Generate]
2. Téléchargez le fichier JavaScript avec [Download JS]
3. Renommez le fichier en ``fess-ss.js`` et placez-le dans le même répertoire que le fichier HTML

Sur la page qui affiche les résultats de recherche (par exemple ``result.html``), écrivez le code suivant.

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form
        language="fr"
        :enable-suggest="true"
        suggest-url="http://localhost:8080"
      ></fess-search-form>
      <fess-search-result
        fess-url="http://localhost:8080"
        language="fr"
      ></fess-search-result>
    </div>

``fess-url`` est l'URL de Fess utilisée pour la recherche, et ``suggest-url`` celle utilisée pour les suggestions.
En production, indiquez une URL de Fess accessible depuis le navigateur des utilisateurs.

Dans l'en-tête des autres pages, placez uniquement le formulaire de recherche.

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form result-page="result.html"></fess-search-form>
    </div>

Le formulaire place les termes de recherche dans le paramètre ``fss.query`` et passe à ``result.html`` ; FSS sur ``result.html`` exécute alors la recherche.
Depuis une page qui ne charge pas FSS, un formulaire qui passe à ``result.html?fss.query=termes`` fonctionne de la même manière.

Pour les autres attributs (nombre de résultats par page ``:page-size``, filtrage par étiquette ``:enable-label``, ouverture des liens dans un nouvel onglet ``link-target="_blank"``, etc.), consultez le manuel de FSS JS Generator.

Vérifier
--------

1. Ouvrez ``http://localhost:8000/result.html`` et lancez une recherche avec le formulaire
2. Si les résultats de recherche s'affichent dans la page, c'est terminé
3. S'ils ne s'affichent pas, examinez la requête vers ``/api/v1/documents`` dans l'onglet Réseau des outils de développement du navigateur. En cas de 404, vérifiez le plugin ; en cas d'erreur CORS, consultez la section suivante

Points d'attention
------------------

Du point de vue du navigateur, appeler l'API sur ``localhost:8080`` depuis une page sur ``localhost:8000`` est une communication cross-origin.
Par défaut, Fess est configuré avec ``api.cors.allow.origin=*`` et accepte les appels de n'importe quelle origine.
La façon de limiter les appelants au site existant est traitée dans :doc:`guide-11`.

Les recherches que FSS envoie depuis une autre origine sont traitées comme celles d'un utilisateur non connecté (invité), même si l'utilisateur est connecté à Fess.
En effet, FSS appelle l'API sans cookies, et la valeur par défaut ``api.cors.allow.origin=*`` n'autorise pas non plus la communication cross-origin avec identifiants.
Par conséquent, seuls les documents dont les permissions contiennent ``{role}guest`` apparaissent dans les résultats.
Pour montrer des documents différents selon le service, demandez aux utilisateurs de se connecter sur la page de recherche de Fess (voir :doc:`guide-05`).

Modifier l'apparence de la page de recherche de Fess
====================================================

En 15.9, la page de recherche est affichée par un « thème » qui regroupe HTML, CSS et JavaScript.
L'écran [Conception de la page] et la modification des JSP des versions précédentes n'existent plus.
Si rien n'est configuré, le thème fourni ``bootstrap`` est utilisé.

Ce que l'on peut changer sans créer de ZIP
------------------------------------------

Le contenu saisi dans « Page d'accueil de la recherche », sous « Avis » dans [Système] > [Général], s'affiche sur la page d'accueil de la recherche et sur la page des résultats du thème fourni.
Vous pouvez aussi écrire du HTML, mais les éléments tels que ``<script>`` et ``<style>`` sont supprimés.
Si vous voulez seulement afficher une ligne d'information pour les utilisateurs internes, il n'est pas nécessaire de créer un thème.

Utiliser un thème publié
------------------------

Le projet Fess publie des thèmes comme ``docsearch``, destiné à la recherche de documents.

1. Ouvrez [Système] > [Thème]
2. Sous « Installer le thème », choisissez un thème dans « Nom » et cliquez sur [Sélectionner]
3. Dans « Version », choisissez la version pour 15.9 (``15.9.x``) et cliquez sur [Installer]
4. Dans « Thème par défaut », au-dessus de la liste, choisissez le thème installé et cliquez sur [Définir]

Lorsque vous rouvrez ``http://localhost:8080/``, la page s'affiche avec le nouveau thème.
Choisir « (aucun par défaut) » et cliquer sur [Définir] permet de revenir au thème fourni ``bootstrap``.

Dupliquer le thème fourni et changer le logo et les couleurs
------------------------------------------------------------

Le thème fourni ne peut pas être modifié directement, et un thème nommé ``bootstrap`` ne peut pas non plus être remplacé par téléversement.
Dupliquez-le sous un autre nom et modifiez la copie.
Ici, nous utilisons ``mytheme``.

1. Copiez le thème fourni hors du conteneur

   ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml cp fess01:/usr/share/fess/app/themes/bootstrap ./mytheme

2. Dans ``mytheme/theme.yml``, remplacez ``name`` par ``mytheme`` et ``displayName`` par ``My Theme``, par exemple
3. Modifiez les fichiers suivants

   - Couleurs et mise en page : ``assets/styles.css``
   - Logo : ``assets/logo-head.png`` (en-tête) et ``assets/logo.png`` (page d'accueil de la recherche)
   - Nom de l'organisation dans le pied de page : ``footer.copyright_org`` dans ``i18n/messages.fr.json`` (``messages.en.json`` pour l'interface en anglais)

4. Regroupez les fichiers de façon que ``theme.yml`` se trouve à la racine du ZIP

   ::

       $ cd mytheme && zip -r ../mytheme.zip . && cd ..

5. Téléversez ``mytheme.zip`` avec [Téléverser] dans [Système] > [Thème]
6. Dans « Thème par défaut », choisissez ``mytheme`` et cliquez sur [Définir]

Ne modifiez pas ``index.html``.
Le fichier ``index.html`` fourni fait référence aux fichiers du thème sous la forme ``{{themePath}}/assets/...``.
Comme Fess remplace ``{{themePath}}`` par ``themes/mytheme`` au moment de servir la page, il suffit de changer le nom pour que les fichiers du thème dupliqué soient chargés.

Vérifier
--------

Rouvrez ``http://localhost:8080/`` et vérifiez que le logo et les couleurs ont changé.
Si ce n'est pas le cas, vérifiez dans l'onglet Réseau des outils de développement que la feuille de style est chargée depuis ``/themes/mytheme/assets/styles.css``.
Si elle est chargée depuis ``/themes/bootstrap/``, le paramètre du thème par défaut n'a pas été pris en compte.

Points d'attention concernant les thèmes
----------------------------------------

- La page de recherche reçoit un en-tête ``Content-Security-Policy`` qui limite la provenance des scripts, des styles et des images à Fess lui-même. Les polices et scripts de CDN externes ne sont pas chargés ; incluez-les dans le ZIP du thème
- La page de recherche ne s'affiche pas dans un ``iframe`` d'une autre page (car la valeur par défaut de ``theme.index.frame.ancestors`` est ``'none'``). Pour afficher des résultats de recherche à l'intérieur d'un portail, utilisez FSS
- ``fess01`` sous Docker n'a pas de volume. Les thèmes téléversés sont placés dans le conteneur et le paramètre du thème par défaut est enregistré dans ``system.properties`` ; les deux disparaissent donc lorsque le conteneur est recréé par ``down``. Utilisez habituellement ``stop``/``start`` et, après une recréation, refaites le téléversement et le paramétrage
- Le thème fourni est conçu pour l'API ``/api/v2`` de la même version de Fess. Après une mise à niveau de Fess, dupliquez à nouveau le nouveau thème fourni et réappliquez vos modifications

Pour la structure des thèmes et les éléments de ``theme.yml``, consultez le `Guide de développement des thèmes <https://fess.codelibs.org/fr/stable/dev/theme-development.html>`__.

Faire pointer les liens des résultats vers les URL des utilisateurs
===================================================================

Il arrive que l'on veuille explorer avec un nom d'hôte interne tout en faisant ouvrir les documents aux utilisateurs par l'URL du portail.
Par exemple, vous explorez ``http://intranet-web01:8080/docs/`` et voulez que les résultats de recherche ouvrent ``https://portal.example.com/docs/``.
Dans ce cas, le mappage de chemin permet de remplacer l'URL uniquement à l'affichage.

1. Ouvrez [Robot d'exploration] > [Mappage de chemin] et cliquez sur [Créer nouveau]
2. Saisissez les valeurs suivantes et cliquez sur [Créer]

   .. list-table::
      :header-rows: 1
      :widths: 25 75

      * - Champ
        - Valeur
      * - Expression régulière
        - ``^http://intranet-web01:8080/docs/``
      * - Remplacement
        - ``https://portal.example.com/docs/``
      * - Type de processus
        - Affichage
      * - Ordre de tri
        - ``0``

« Affichage » ne remplace que l'URL affichée dans les résultats de recherche et la destination du lien.
L'URL enregistrée dans l'index ne change pas : aucune nouvelle exploration n'est nécessaire, et la modification s'applique aux résultats de recherche dès l'enregistrement.
Si vous choisissez « Exploration » ou « Exploration/Affichage », l'URL remplacée est enregistrée dans l'index.
Attention : choisir l'une de ces options alors que vous voulez seulement changer l'affichage modifie aussi les URL des explorations suivantes.

Pour vérifier, recherchez un mot qui fait apparaître le document concerné, et vérifiez que l'URL et la destination du lien dans les résultats sont ``https://portal.example.com/docs/...``.
Si vous recevez les résultats par l'API, l'URL remplacée se trouve dans ``url_link``, et non dans ``url`` (voir :doc:`guide-11`).

Pour un exemple qui transforme les chemins d'un serveur de fichiers en URL d'un serveur web, consultez `Mappage de chemin <https://fess.codelibs.org/fr/stable/admin/pathmap-guide.html>`__.

Articles à lire ensuite
=======================

- Appeler l'API de recherche depuis le serveur d'un système métier : :doc:`guide-11`
- Changer les documents affichés dans le portail selon le service : :doc:`guide-05`
- Rechercher ensemble des sites web et des serveurs de fichiers et les séparer par étiquettes : :doc:`guide-04`
- Montrer un thème ou des cibles de recherche différents à chaque organisation : :doc:`guide-13`
- Exiger une connexion pour la page de recherche : :doc:`guide-15`

Références
==========

- `Placement du formulaire de recherche <https://fess.codelibs.org/fr/stable/config/search-form-integration.html>`__
- `Thème <https://fess.codelibs.org/fr/stable/admin/theme-guide.html>`__
- `Guide de développement des thèmes <https://fess.codelibs.org/fr/stable/dev/theme-development.html>`__
- `Mappage de chemin <https://fess.codelibs.org/fr/stable/admin/pathmap-guide.html>`__
- `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__
- `FSS JS Generator <https://fss-generator.codelibs.org/>`__
- `fess-site-search (GitHub) <https://github.com/codelibs/fess-site-search>`__
- `fess-webapp-v1-api (GitHub) <https://github.com/codelibs/fess-webapp-v1-api>`__
