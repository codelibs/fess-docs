==============================
Recherche par champ spécifique
==============================

Recherche par champ spécifique
===============================

Les résultats de l'exploration par |Fess| sont enregistrés pour chaque champ tel que le titre ou le contenu. Vous pouvez effectuer une recherche en spécifiant ces champs. En spécifiant un champ, vous pouvez définir des critères de recherche détaillés tels que le type de document ou la taille.

Champs disponibles
------------------

Par défaut, vous pouvez effectuer une recherche en spécifiant les champs suivants.

.. list-table::
   :header-rows: 1

   * - Nom du champ
     - Description
     - Type de données
   * - url
     - URL explorée
     - Mot-clé
   * - host
     - Nom d'hôte contenu dans l'URL explorée
     - Mot-clé
   * - site
     - Chaîne obtenue en retirant de l'URL le schéma et la chaîne de requête (nom d'hôte et chemin). La recherche s'effectue par correspondance de préfixe
     - Mot-clé
   * - title
     - Titre
     - Texte
   * - content
     - Contenu
     - Texte
   * - content_length
     - Taille du document (en octets)
     - Numérique
   * - last_modified
     - Date de dernière modification du document
     - Date
   * - timestamp
     - Date et heure d'indexation du document (heure d'exécution du crawl si la date de dernière modification n'est pas disponible)
     - Date
   * - mimetype
     - Type MIME du document (exemple : ``text/html``)
     - Mot-clé
   * - filetype
     - Type de fichier déterminé à partir du type MIME (exemple : ``html``, ``word``, ``pdf``. ``others`` si aucun ne correspond)
     - Mot-clé
   * - filename
     - Nom de fichier situé à la fin du chemin de l'URL
     - Mot-clé
   * - label
     - Valeur de l'étiquette attribuée au document
     - Mot-clé
   * - lang
     - Code de langue du document (exemple : ``ja``, ``en``)
     - Mot-clé
   * - anchor
     - URL de destination des liens extraits d'une page HTML (crawl Web uniquement)
     - Mot-clé
   * - click_count
     - Nombre de clics sur le document
     - Numérique
   * - favorite_count
     - Nombre de fois où le document a été ajouté aux favoris
     - Numérique

Table : Liste des champs disponibles

« Type de données » indique la différence de mode de recherche propre à chaque champ.

* Mot-clé : recherche par correspondance exacte sur la valeur entière. Peut être combinée avec une recherche par caractères génériques ou par préfixe.
* Texte : recherche en texte intégral sur les termes obtenus par découpage (notamment par analyse morphologique). C'est le cas des champs title et content.
* Numérique / Date : vous pouvez utiliser la :doc:`Recherche par plage <search-range>`.

Si aucun champ n'est spécifié, la recherche porte sur les champs title et content. Selon la configuration, il est également possible d'ajouter des champs supplémentaires à cibler pour la recherche.

.. note::
    Selon la cible du crawl, certains champs peuvent ne pas être renseignés. Par exemple, anchor n'est enregistré que lors d'un crawl Web, et lang uniquement lorsque le document HTML possède un attribut de langue. Par ailleurs, des champs tels que segment (identifiant de session représentant une exécution de crawl) ou doc_id (identifiant interne attribué par le système) peuvent également être spécifiés, mais ils ne sont pas utilisés dans le cadre d'une recherche normale.

Lorsque des fichiers HTML sont ciblés par la recherche, le contenu de la balise title est enregistré dans le champ title, et le texte situé sous la balise body est enregistré dans le champ content.

Utilisation
-----------

Pour effectuer une recherche par champ spécifique, saisissez dans le formulaire de recherche au format « nom_champ:terme_recherche », en séparant le nom du champ et le terme de recherche par deux-points (:).

Pour effectuer une recherche avec fess comme terme de recherche dans le champ title, saisissez ce qui suit :

::

    title:fess

Cette recherche affichera les documents dont le champ title contient fess dans les résultats de recherche.

Pour effectuer une recherche sur le champ url, saisissez ce qui suit :

::

   url:https\:\/\/fess.codelibs.org\/ja\/15.8\/*
   url:"https://fess.codelibs.org/ja/15.8/*"

La première méthode permet d'utiliser des requêtes avec caractères génériques, vous pouvez donc également écrire par exemple ``url:*\/\/fess.codelibs.org\/*``. Les caractères « : » et « / » contenus dans l'URL sont des caractères spéciaux de la syntaxe de requête ; veuillez les échapper avec ``\`` (voir :doc:`special-char`). La seconde méthode ne permet pas d'utiliser des requêtes avec caractères génériques, mais un terme se terminant par ``*`` est traité comme une recherche par préfixe (correspondance en début de chaîne).

.. tip::
    Si vous souhaitez rechercher une partie de l'URL, vous pouvez utiliser ``inurl:`` pour effectuer une recherche par correspondance partielle sur l'URL. Par exemple, ``inurl:15.8`` recherche les documents dont l'URL contient ``15.8``.

Pour les champs dont la valeur contient « / », comme mimetype, filetype ou site, entourez la valeur de guillemets comme dans ``mimetype:"text/html"``, ou échappez-la comme dans ``mimetype:text\/html``.

Pour la syntaxe de recherche associée, consultez également :doc:`Recherche avec caractères génériques <search-wildcard>`, :doc:`Recherche par plage <search-range>`, :doc:`Recherche avec tri <search-sort>` et :doc:`Caractères spéciaux <special-char>`.
