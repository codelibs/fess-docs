========================================================
Créer un serveur de recherche basé sur Elasticsearch avec Fess 〜 Édition API
========================================================

Introduction
========

Cette fois, nous allons présenter comment utiliser l'API fournie par Fess pour effectuer des recherches et afficher les résultats côté client (navigateur).
En utilisant l'API, il est également possible d'intégrer Fess comme serveur de recherche dans des systèmes web existants avec seulement des modifications HTML.

Cet article utilise Fess 15.3.0 pour les explications.
Pour la méthode de construction de Fess, veuillez consulter l'\ `édition introduction <https://fess.codelibs.org/ja/articles/article-1.html>`__\.

Public visé
========

-  Personnes souhaitant ajouter une fonctionnalité de recherche à un système web existant

Environnement requis
==========

Le contenu de cet article a été vérifié dans l'environnement suivant.

-  Google Chrome 120 ou ultérieur

API JSON
========

Fess peut répondre aux résultats de recherche au format JSON en plus de l'affichage HTML habituel via une API.
En utilisant l'API, il est facile de construire un serveur Fess et de simplement interroger les résultats de recherche depuis des systèmes existants.
Comme les résultats de recherche peuvent être traités dans un format indépendant du langage de développement, il devrait être facile d'intégrer Fess dans des systèmes autres que Java.

Pour savoir quel type de réponse l'API fournie par Fess retourne, veuillez consulter `Réponse JSON <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__.

Fess utilise OpenSearch comme moteur de recherche interne.
OpenSearch fournit également une API JSON, mais l'API de Fess est différente.
L'avantage d'utiliser l'API de Fess plutôt que l'API d'OpenSearch est que vous pouvez utiliser diverses fonctionnalités spécifiques à Fess telles que la gestion des journaux de recherche et le contrôle des droits de consultation.
Si vous souhaitez développer de zéro votre propre mécanisme d'exploration de documents, il serait préférable d'utiliser OpenSearch, mais si vous souhaitez simplement ajouter facilement une fonctionnalité de recherche, vous pouvez réduire considérablement les coûts de développement en utilisant Fess.

Construction d'un site de recherche utilisant l'API JSON
==================================

Cette fois, nous allons expliquer comment construire un site utilisant l'API de Fess.
Pour l'échange avec le serveur Fess, nous utiliserons la réponse JSON.
Le serveur Fess utilisé cette fois est le serveur Fess publiquement accessible en démonstration par le projet Fess.
Si vous souhaitez utiliser votre propre serveur Fess, veuillez installer Fess 15.3.0 ou ultérieur.

JSON et CORS
-----------

Lors de l'accès en JSON, il faut faire attention à la politique Same-Origin.
Ainsi, si le serveur qui génère le HTML à afficher dans le navigateur et le serveur Fess sont sur le même domaine, JSON peut être utilisé, mais s'ils sont différents, il faut utiliser CORS (Cross-Origin Resource Sharing).
Cette fois, nous allons procéder en supposant que le serveur hébergeant le HTML et le serveur Fess sont sur des domaines différents.
Fess prend en charge CORS, et les valeurs de configuration peuvent être définies dans app/WEB-INF/classes/fess_config.properties. Par défaut, les paramètres suivants sont définis.

::

    api.cors.allow.origin=*
    api.cors.allow.methods=GET, POST, OPTIONS, DELETE, PUT
    api.cors.max.age=3600
    api.cors.allow.headers=Origin, Content-Type, Accept, Authorization, X-Requested-With
    api.cors.allow.credentials=true

Cette fois, nous utiliserons la configuration par défaut, mais si vous modifiez la configuration, veuillez redémarrer Fess.


Fichiers à créer
----------------

Cette fois, nous allons implémenter le processus de recherche en utilisant JavaScript dans le HTML.
Nous utilisons jQuery comme bibliothèque JavaScript.
Les fichiers à créer sont les suivants.

-  Fichier HTML « index.html » qui affiche le formulaire de recherche et les résultats de recherche

- Fichier JS « fess.js » qui communique avec le serveur Fess

Dans cet exemple de construction, nous avons implémenté les fonctionnalités suivantes.

-  Envoi de requête de recherche avec le bouton de recherche

-  Liste des résultats de recherche

-  Traitement de pagination des résultats de recherche

Création du fichier HTML
------------------

Tout d'abord, créez le HTML pour afficher le formulaire de recherche et les résultats de recherche.
Cette fois, pour faciliter la compréhension, nous avons utilisé une structure de balises simple sans ajuster le design avec CSS.
Le fichier HTML utilisé est le suivant.

Contenu d'index.html
::

    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Site de recherche</title>
    </head>
    <body>
    <div id="header">
      <form id="searchForm">
        <input id="searchQuery" type="text" name="query" size="30"/>
        <input id="searchButton" type="submit" value="Rechercher"/>
        <input id="searchStart" type="hidden" name="start" value="0"/>
        <input id="searchNum" type="hidden" name="num" value="20"/>
      </form>
    </div>
    <div id="subheader"></div>
    <div id="result"></div>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script type="text/javascript" src="fess.js"></script>
    </body>
    </html>

En regardant sous la balise body, tout d'abord dans la partie de la balise div avec l'attribut id header, le champ de saisie de recherche et le bouton de recherche sont placés.
De plus, les formulaires hidden conservent la position de début d'affichage (start) et le nombre d'éléments à afficher (num).
Les valeurs de start et num sont mises à jour par JavaScript après l'envoi de la requête de recherche.
Cependant, le nombre d'éléments à afficher est le nombre d'éléments par page, et dans cet exemple de code, comme il n'y a pas de fonctionnalité pour changer le nombre d'éléments à afficher, la valeur de num n'est pas modifiée.

Dans la partie de la balise div subheader suivante, des informations telles que le nombre de résultats trouvés sont affichées.
Dans la balise div result, les résultats de recherche et les liens de pagination sont affichés.

Enfin, le fichier JS de jQuery et le JavaScript « fess.js » que nous avons créé sont chargés.
Vous pouvez également enregistrer le fichier JS de jQuery dans le même répertoire que « index.html », mais cette fois nous l'obtenons via le CDN de Google.

Création du fichier JS
----------------

Ensuite, créez le fichier JS « fess.js » qui communique avec le serveur Fess et affiche les résultats de recherche.
Créez « fess.js » avec le contenu suivant et placez-le dans le même répertoire que « index.html ».

Contenu de fess.js
::

    $(function(){
        // (1) URL de Fess
        var baseUrl = "http://SERVERNAME:8080/api/v1/documents?q=";
        // (2) Objet jQuery du bouton de recherche
        var $searchButton = $('#searchButton');

        // (3) Fonction de processus de recherche
        var doSearch = function(event){
          // (4) Obtention de la position de début d'affichage et du nombre d'éléments à afficher
          var start = parseInt($('#searchStart').val()),
              num = parseInt($('#searchNum').val());
          // Vérification de la position de début d'affichage
          if(start < 0) {
            start = 0;
          }
          // Vérification du nombre d'éléments à afficher
          if(num < 1 || num > 100) {
            num = 20;
          }
          // (5) Obtention des informations de page à afficher
          switch(event.data.navi) {
            case -1:
              // Cas de la page précédente
              start -= num;
              break;
            case 1:
              // Cas de la page suivante
              start += num;
              break;
            default:
            case 0:
              start = 0;
              break;
          }
          // Trim et stockage de la valeur du champ de recherche
          var searchQuery = $.trim($('#searchQuery').val());
          // (6) Vérification que le formulaire de recherche n'est pas vide
          if(searchQuery.length != 0) {
            var urlBuf = [];
            // (7) Désactivation du bouton de recherche
            $searchButton.attr('disabled', true);
            // (8) Construction de l'URL
            urlBuf.push(baseUrl, encodeURIComponent(searchQuery),
              '&start=', start, '&num=', num);
            // (9) Envoi de la requête de recherche
            $.ajax({
              url: urlBuf.join(""),
              dataType: 'json',
            }).done(function(data) {
              // Traitement des résultats de recherche
              var dataResponse = data.response;
              // (10) Vérification du statut
              if(dataResponse.status != 0) {
                alert("Un problème est survenu lors de la recherche. Veuillez contacter l'administrateur.");
                return;
              }

              var $subheader = $('#subheader'),
                  $result = $('#result'),
                  record_count = dataResponse.record_count,
                  offset = 0,
                  buf = [];
              if(record_count == 0) { // (11) Cas où il n'y a pas de résultat de recherche
                // Sortie dans la zone de sous-en-tête
                $subheader[0].innerHTML = "";
                // Sortie dans la zone de résultat
                buf.push("<b>", dataResponse.q, "</b> : Aucune information correspondante trouvée.");
                $result[0].innerHTML = buf.join("");
              } else { // (12) Cas où la recherche a trouvé des résultats
                var page_number = dataResponse.page_number,
                    startRange = dataResponse.start_record_number,
                    endRange = dataResponse.end_record_number,
                    i = 0,
                    max;
                offset = startRange - 1;
                // (13) Sortie dans le sous-en-tête
                buf.push("<b>", dataResponse.q, "</b> : Résultats de recherche ",
                  record_count, " éléments trouvés, affichage de ", startRange, " à ",
                  endRange, " (", dataResponse.exec_time,
                    " secondes)");
                $subheader[0].innerHTML = buf.join("");

                // Effacement de la zone de résultats de recherche
                $result.empty();

                // (14) Affichage des résultats de recherche
                var $resultBody = $("<ol/>");
                var results = dataResponse.result;
                for(i = 0, max = results.length; i < max; i++) {
                  buf = [];
                  buf.push('<li><h3 class="title">', '<a href="',
                    results[i].url_link, '">', results[i].title,
                    '</a></h3><div class="body">', results[i].content_description,
                    '<br/><cite>', results[i].site, '</cite></div></li>');
                  $(buf.join("")).appendTo($resultBody);
                }
                $resultBody.appendTo($result);

                // (15) Affichage des informations de numéro de page
                buf = [];
                buf.push('<div id="pageInfo">Page ', page_number, '<br/>');
                if(dataResponse.prev_page) {
                  // Lien vers la page précédente
                  buf.push('<a id="prevPageLink" href="#">&lt;&lt;Page précédente</a> ');
                }
                if(dataResponse.next_page) {
                  // Lien vers la page suivante
                  buf.push('<a id="nextPageLink" href="#">Page suivante&gt;&gt;</a>');
                }
                buf.push('</div>');
                $(buf.join("")).appendTo($result);
              }
              // (16) Mise à jour des informations de page
              $('#searchStart').val(offset);
              $('#searchNum').val(num);
              // (17) Déplacement de l'affichage de la page vers le haut
              $(document).scrollTop(0);
            }).always(function() {
              // (18) Activation du bouton de recherche
              $searchButton.attr('disabled', false);
            });
          }
          // (19) Retour de false pour ne pas soumettre
          return false;
        };

        // (20) Traitement lorsque la touche Enter est pressée dans le champ de recherche
        $('#searchForm').submit({navi:0}, doSearch);
        // (21) Traitement lorsque le lien de page précédente est cliqué
        $('#result').on("click", "#prevPageLink", {navi:-1}, doSearch)
        // (22) Traitement lorsque le lien de page suivante est cliqué
          .on("click", "#nextPageLink", {navi:1}, doSearch);
      });

Le traitement de « fess.js » est exécuté après la construction du DOM du fichier HTML.
Tout d'abord, en 1, spécifiez l'URL du serveur Fess construit.

2 enregistre l'objet jQuery du bouton de recherche.
Comme l'objet jQuery du bouton de recherche est utilisé plusieurs fois, il est conservé dans une variable pour être réutilisé.

3 définit la fonction de processus de recherche. Le contenu de cette fonction sera expliqué dans la section suivante.

20 enregistre l'événement lorsque le formulaire de recherche est soumis.
Lorsque le bouton de recherche est cliqué ou que la touche Enter est pressée dans le champ de recherche, le traitement enregistré en 20 est exécuté.
Lors de l'événement, la fonction de processus de recherche doSearch est appelée.
La valeur de navi est transmise lors de l'appel de la fonction de processus de recherche et cette valeur est utilisée pour le traitement de pagination.

21 et 22 enregistrent les événements lorsque les liens ajoutés par le traitement de pagination sont cliqués.
Comme ces liens sont ajoutés dynamiquement, il est nécessaire d'enregistrer les événements avec delegate.
Dans ces événements également, comme en 20, la fonction de processus de recherche est appelée.

Fonction de processus de recherche doSearch
--------------------

Nous allons expliquer la fonction de processus de recherche doSearch en 3.

En 4, obtenez la position de début d'affichage et le nombre d'éléments à afficher.
Ces valeurs sont conservées comme valeurs hidden dans le formulaire de recherche de la zone header.
Comme la position de début d'affichage doit être 0 ou plus et le nombre d'éléments à afficher entre 1 et 100, si des valeurs en dehors de ces plages sont obtenues, des valeurs par défaut sont définies.

En 5, en jugeant la valeur du paramètre navi transmis lors de l'enregistrement de l'événement doSearch, corrigez la position de début d'affichage.
Ici, -1 représente le déplacement vers la page précédente, 1 représente le déplacement vers la page suivante, et les autres valeurs représentent le déplacement vers la première page.

6 juge si la valeur du champ de recherche a été saisie pour exécuter la recherche, et si elle est vide, termine le traitement sans rien faire.

En 7, pour éviter le double submit, désactivez le bouton de recherche pendant l'interrogation du serveur Fess.

En 8, assemblez l'URL pour envoyer la requête Ajax.
Combinez l'URL de 1 avec le terme de recherche, la position de début d'affichage et le nombre d'éléments à afficher.

En 9, envoyez la requête Ajax.
Lorsque la requête est retournée normalement, la fonction success est exécutée.
L'argument de success reçoit l'objet des résultats de recherche retourné par le serveur Fess.

Tout d'abord, en 10, vérifiez le contenu du statut de la réponse.
Lorsque la requête de recherche est traitée normalement, 0 est défini.
Pour les détails de la réponse JSON de Fess, veuillez consulter le\ `site Fess <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__\.

Si la requête de recherche est traitée normalement et qu'aucun résultat de recherche n'a été trouvé, dans la condition 11, videz le contenu de la zone subheader et affichez un message dans la zone result indiquant qu'aucun résultat de recherche n'a été trouvé.

Si des résultats de recherche ont été trouvés, dans la condition 12, traitez les résultats de recherche.
En 13, définissez le message du nombre de résultats et du temps d'exécution dans la zone subheader.
14 ajoute les résultats de recherche à la zone result.
Les résultats de recherche sont stockés sous forme de tableau dans data.response.result.
Vous pouvez obtenir les valeurs de champ des documents de résultats de recherche en accédant à results[i].〜.

En 15, ajoutez le numéro de page actuellement affiché et les liens vers la page précédente et la page suivante à la zone result.
16 enregistre la position de début d'affichage et le nombre d'éléments à afficher actuels dans les champs hidden du formulaire de recherche.
La position de début d'affichage et le nombre d'éléments à afficher seront réutilisés lors de la prochaine requête de recherche.

Ensuite, en 17, changez la position d'affichage de la page.
Lorsqu'un lien vers la page suivante est cliqué, comme la page elle-même n'est pas mise à jour, déplacez vers le haut de la page avec scrollTop.

En 18, après la fin du processus de recherche, activez le bouton de recherche.
Pour que cela soit exécuté que la requête réussisse ou échoue, appelez-le avec complete.

19 retourne false pour empêcher l'envoi du formulaire et du lien après l'appel de la fonction de processus de recherche.
Cela empêche la transition de page.

Exécution
----

Accédez à « index.html » avec un navigateur.
Le formulaire de recherche suivant s'affiche.

Formulaire de recherche
|image1|

Entrez un terme de recherche approprié et cliquez sur le bouton de recherche pour afficher les résultats de recherche.
Le nombre d'éléments à afficher par défaut est de 20, mais si le nombre de résultats trouvés est important, un lien vers la page suivante est affiché sous la liste des résultats de recherche.

Résultats de recherche
|image2|

Conclusion
======

Nous avons construit un site de recherche client basé sur jQuery en utilisant l'API JSON de Fess.
En utilisant l'API JSON, il est possible de construire des systèmes utilisant Fess non seulement pour des applications basées sur navigateur, mais aussi en l'appelant depuis d'autres applications.

Notez que bien que l'exemple de code de cet article montre le format d'endpoint API traditionnel, dans Fess 15.3, l'utilisation de l'endpoint ``/api/v1/documents`` est recommandée.
Pour plus de détails, veuillez consulter les `Spécifications API <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__.

Références
========

-  `Fess <https://fess.codelibs.org/ja/>`__

-  `jQuery <http://jquery.com/>`__

.. |image0| image:: ../../resources/images/en/article/4/sameorigin.png
.. |image1| image:: ../../resources/images/en/article/4/searchform.png
.. |image2| image:: ../../resources/images/en/article/4/searchresult.png
