# Remarque
Nous avons constaté que la durée a diminué comparé à la version précédente.
Nous avons de meilleur résultat. Mais ces résultats sont pas encore optimaux.
*Par exemple avec un fichier de 1.3Mo nous passons de 12min à 9min pour encoder*

# Problèmes constaté
Lors de l'encodage pour les **30 premiers %, l'encodage ou le décodage est rapide et devient très lent vers 70%**. Ce problème est causé par quoi?
D'après les résultats du profiling, le chunker énormément appelé.
A cette version, nous appellons le **progressbar 10 fois peu importe la taille du fichier**.

# Solutions à implémenter
Comment serait la rapidité si, j'appelais le progressbar que **4 fois**