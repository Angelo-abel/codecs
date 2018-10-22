# Remarque
Pas vraiment d'amélioration. Il y en a qui ont connu quelques améliorations
mais les stats pour  certaines tailles de fichier se sont dégradées. 
Autre chose sur les premier 25% sont vites parcouru et les 75% restants deviennent vraiment lent.
Mon PC commence par fumer même dès que la taille augmente ce qui veut dire qu'il stocke trop de chose dans le buffer.

# Cause
Pour avoir la chaîne encryptée, nous utilisons une variable qui stocke ces informations. Mais merde imaginons que j'ai un fichier de 1GB à encoder, putain la taille de cette variable va atteindre les 1GB(manière de parlé) dans le buffer en plus et cette espace est inutilisable pour run le programme. Donc mon programme va ralentir au fur et mesure que j'encode/je décode le fichier. 

# solution 
Ecrire au fur et à mesure dans le fichier de destination tout en essayant de vider le buffer si c'est possible et supprimer la barre de progression. 