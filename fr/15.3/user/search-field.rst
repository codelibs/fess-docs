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
   * - url
     - URL explorée
   * - host
     - Nom d'hôte contenu dans l'URL explorée
   * - title
     - Titre
   * - content
     - Contenu
   * - content_length
     - Taille du document exploré
   * - last_modified
     - Date de dernière modification du document exploré
   * - mimetype
     - Type MIME du document

Table : Liste des champs disponibles


Si aucun champ n'est spécifié, la recherche cible les champs title et content.
Il est également possible d'ajouter des champs et de les inclure dans la recherche.

Lors de la recherche de fichiers HTML, la balise title est enregistrée dans le champ title et la chaîne de caractères sous la balise body est enregistrée dans le champ content.

Utilisation
-----------

Pour effectuer une recherche par champ spécifique, saisissez dans le formulaire de recherche au format « nom_champ:terme_recherche », en séparant le nom du champ et le terme de recherche par deux-points (:).

Pour rechercher fess dans le champ title, saisissez ce qui suit :

::

    title:fess

Cette recherche affichera les documents dont le champ title contient fess dans les résultats de recherche.

Pour effectuer une recherche sur le champ url, saisissez ce qui suit :

::

   url:https\:\/\/fess.codelibs.org\/fr\/15.3\/*
   url:"https://fess.codelibs.org/fr/15.3/*"

La première méthode permet d'utiliser des requêtes avec caractères génériques, vous pouvez donc écrire par exemple ``url:*\/\/fess.codelibs.org\/*``. Les caractères « : » et « / » dans l'URL sont des caractères réservés et doivent être échappés. La seconde méthode ne permet pas d'utiliser des requêtes avec caractères génériques, mais permet d'utiliser des requêtes de préfixe.
