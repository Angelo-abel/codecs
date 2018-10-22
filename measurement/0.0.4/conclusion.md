# Conclusion
On constate une nette amélioration et je peux encoder/décoder des fichiers ayant une taille de 20Mo en un temps moyen de **16s**

# Remarque
Avec cette méthode d'écriture directement dans le fichier de destination,
il fait appel plus aux fonctions **read** et **write**.

# Solution a implémenter
Bon maintenant comment minimiser le nombre d'appel de ses fonctions?
 1. Traiter plus d'un bytes à la fois, i.e allez au WORD_SIZE de machine.
 Mon ordinateur étant un 64bit alors mon **WORD_SIZE=8bytes**

