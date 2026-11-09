============
URL en échec
============

Présentation
============

Cette section explique les URL en échec.
Les URL qui n'ont pas pu être obtenues lors du crawl sont enregistrées et peuvent être vérifiées comme URL en échec.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste pour vérifier les URL en échec, cliquez sur [Informations système > URL en échec] dans le menu de gauche.

|image0|

En cliquant sur le lien de vérification de l'URL en échec, les détails s'affichent.

Éléments de la liste
--------------------

La liste affiche l'URL, le type, le type MIME, le statut HTTP, la taille (octets) et l'heure du dernier accès.

Le type MIME, le statut HTTP et la taille ne sont enregistrés que si le crawler les connaissait ; sinon ils restent vides.

- Enregistrés lorsque : le traitement a échoué après la récupération du document (par exemple dépassement d'une limite de taille), ou le serveur a renvoyé un statut HTTP figurant dans ``crawler.failure.url.status.codes``. Lorsqu'un document est refusé parce qu'il dépasse une limite de taille avant d'être récupéré, seule la taille est enregistrée.
- Non enregistrés lorsque : aucune réponse n'a été obtenue (délai dépassé, erreur de connexion, etc.), et pour les échecs des explorations de magasins de données. Un échec de l'extraction du texte (par exemple un PDF illisible) n'est pas non plus enregistré avec la valeur par défaut ``crawler.ignore.content.exception=true`` : le document est indexé sans corps. Il n'est enregistré que lorsque cette clé vaut ``false``. Toutefois, un document rejeté comme bombe zip suspectée est enregistré comme URL en échec et n'est pas indexé, même lorsque cette clé vaut ``true``.
- Le statut HTTP n'est enregistré que pour les URL ``http`` / ``https``. Il reste vide pour les fichiers, SMB et les autres protocoles.
- Pour une URL en échec enregistrée avant |Fess| 15.10, ces éléments restent vides jusqu'à ce que l'URL échoue à nouveau.

Téléchargement CSV
------------------

Le bouton [Télécharger le CSV] de la liste télécharge au format CSV les URL en échec correspondant aux conditions saisies dans le formulaire de recherche (URL, nombre d'erreurs et type). Le nom du fichier est ``failureurl_yyyyMMddHHmmss.csv``.

- La première ligne contient les noms de colonnes, dans cet ordre : ``url``, ``errorName``, ``errorCount``, ``lastAccessTime``, ``httpStatusCode``, ``mimeType`` et ``contentLength``. Le journal (trace de pile) n'est pas inclus.
- Toutes les lignes correspondantes sont écrites, la plus récente d'abord selon le dernier accès. La pagination ne s'applique pas et le nombre de lignes n'est pas limité.
- ``lastAccessTime`` est au format ISO 8601 en UTC (par exemple ``2026-01-01T00:00:00.000Z``).
- L'encodage des caractères suit « Encodage du fichier CSV » dans [Système > Général] ; un fichier UTF-8 commence par une marque d'ordre des octets.
- Pour qu'un tableur n'exécute pas une valeur comme une formule, une valeur qui commence par ``=``, ``+``, ``-``, ``@``, une tabulation ou un retour chariot est précédée d'un ``'``.

Détails de l'URL en échec
=========================

Les détails de l'URL en échec enregistrent les exceptions survenues lors du crawl.

|image1|

Contenu des détails
-------------------

URL
::::

URL où l'exception s'est produite.

Nom du thread
:::::::::::::

Nom du thread qui exécutait le crawl.
Peut être utilisé lors de la vérification des fichiers journaux.

Type
::::

Type d'exception.

Statut HTTP
:::::::::::

Statut HTTP de la réponse pour le document. Enregistré uniquement pour les URL ``http`` / ``https``, et seulement si le crawler le connaissait.

Type MIME
:::::::::

Type MIME du document. Enregistré uniquement si le crawler le connaissait.

Taille (octets)
:::::::::::::::

Taille du document. Enregistrée uniquement si le crawler la connaissait.

Journal
:::::::

Contenu de l'exception.

Nombre d'erreurs
::::::::::::::::

Nombre de fois où cette exception s'est produite.

Heure du dernier accès
::::::::::::::::::::::

Heure à laquelle cette exception s'est produite.


.. |image0| image:: ../../../resources/images/en/15.10/admin/failureurl-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/failureurl-2.png
