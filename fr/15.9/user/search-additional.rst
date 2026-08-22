=============================
Critères de recherche masqués
=============================

Le paramètre ``ex_q`` permet de transmettre un critère de recherche spécifique sans afficher son texte à l'écran. Les critères spécifiés dans ``ex_q`` ne s'affichent pas dans le champ de recherche et sont conservés même lorsque l'écran est actualisé lors de la pagination ou du filtrage par facettes.

Dans ``ex_q``, vous pouvez utiliser la même syntaxe de requête que pour le terme de recherche standard (``q``) : le format ``field:value``, les phrases, les plages, des opérateurs tels que ``OR``, etc. Le critère spécifié est combiné par défaut avec le critère de ``q`` au moyen de AND lors de l'exécution de la recherche. Autrement dit, les documents ne correspondant pas au critère de ``ex_q`` sont exclus des résultats de recherche.

Utilisation
-----------

Lors de l'exécution d'une recherche (par exemple, depuis un formulaire de recherche), ajoutez la valeur de ``ex_q`` sous forme de champ de formulaire masqué ou de paramètre de requête dans l'URL, puis exécutez la recherche. Vous pouvez ainsi effectuer la recherche sans afficher le critère à l'écran.

Vous pouvez spécifier ``ex_q`` plusieurs fois. Comme dans l'exemple ci-dessous, transmettre plusieurs valeurs ``ex_q`` ajoute chacune d'elles comme critère de recherche (les valeurs vides ou en double sont ignorées).

.. code-block:: none

    /search?q=keyword&ex_q=label:manual&ex_q=filetype:pdf

Conservation lors de la pagination
-----------------------------------

Fess ajoute automatiquement la valeur de ``ex_q`` aux liens de pagination (page suivante, page précédente, etc.) et aux liens de filtrage par facettes. Le critère ``ex_q`` est donc conservé même lorsque l'écran est actualisé par ces opérations.

En revanche, si vous saisissez un terme dans le champ de recherche standard (la zone de recherche) et relancez la recherche, ``ex_q`` n'est pas conservé. Si vous souhaitez que le critère soit également conservé via la zone de recherche, prévoyez un champ masqué ``ex_q`` dans votre propre formulaire de recherche et envoyez ``ex_q`` à chaque recherche.

.. note::

    * Si la longueur d'une valeur ``ex_q`` dépasse ``query.max.length`` (valeur par défaut : 1000 caractères), cette valeur est ignorée sans provoquer d'erreur.
    * ``ex_q`` peut être utilisé non seulement pour la recherche depuis l'écran web, mais aussi avec l'API de recherche (``/api/v2``). Dans l'API, le nombre maximal d'éléments ``ex_q`` par requête (``api.v2.param.max.array.size``, valeur par défaut : 100) et la longueur maximale de chaque élément (``api.v2.param.max.length``, valeur par défaut : 1000 caractères) s'appliquent.
