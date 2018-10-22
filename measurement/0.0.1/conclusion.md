# Remarque
Au fur et à mesure que la taille du fichier augmente, le temps d'exécution
augmente aussi considérablement. Par exemple, avec un fichier de **1.3Mo nous sommes déjà à 12min comme temps d'exécution comme 
le montre les statistiques**. En matière de rapidité, le code est buggy.

# Cause
Fuck!!! Putain!! la merde. Le progressbar est appelé autant de fois que j'encode chaque byte et fait près de 30% de l'opération d'encodage/Decodage. 
Merde!!! Par exemple pour un fichier ayant une taille 500ko, il est appelé:
**547742 fois**

# Solution à implémenter
Diminuer la résolution du progressbar i.e incrémenter de 10%