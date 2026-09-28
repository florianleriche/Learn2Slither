Learn2Slither
Feuille de route du projet
🎯 Objectif du projet

Le but de Learn2Slither est de créer un Snake capable d'apprendre à jouer tout seul grâce au Q-Learning.

Contrairement à un Snake classique où les déplacements sont contrôlés par le joueur, ici le serpent doit apprendre par lui-même à :

trouver les pommes vertes ;
éviter les pommes rouges ;
éviter les murs ;
éviter son propre corps ;
survivre le plus longtemps possible.

L'idée est qu'au début il joue complètement au hasard, puis qu'il améliore progressivement ses décisions grâce aux récompenses qu'il reçoit.

1. Création du plateau

La première étape a été de créer un plateau.

J'ai choisi un plateau :

Plain Text
10 x 10
Show more lines

avec :

un serpent ;
deux pommes vertes ;
une pomme rouge.

Les pommes apparaissent toujours dans des cases libres.

2. Création du serpent

Le serpent possède :

Python
self.body
Show more lines

qui contient toutes les positions de son corps.

Exemple :

Python
[
(5, 5),
(4, 5),
(3, 5)
]
Show more lines

La première case est toujours la tête.

3. Déplacements

J'ai ensuite ajouté les déplacements :

Plain Text
UP
LEFT
DOWN
RIGHT
Show more lines

Chaque action déplace la tête dans une direction de la carte.

Le reste du corps suit automatiquement.

4. Gestion des pommes

Deux types de pommes existent :

Pomme verte

Quand le serpent mange une pomme verte :

Plain Text
+ taille
+ récompense
Show more lines

Le serpent grandit d'une case.

Pomme rouge

Quand le serpent mange une pomme rouge :

Plain Text
- taille
- récompense
Show more lines

Le serpent perd une case.

5. Détection des collisions

J'ai ajouté les collisions :

Mur
Plain Text
GAME OVER
Show more lines

si la tête sort de la carte.

Corps
Plain Text
GAME OVER
Show more lines

si la tête touche son propre corps.

6. Première version du Q-Learning

J'ai ensuite créé une Q-Table.

La Q-Table stocke :

Plain Text
Etat
+
Action
=
Valeur
Show more lines

Exemple :

Python
Q[state]["UP"]
Show more lines

Plus la valeur est élevée, plus l'action semble intéressante.

7. Les récompenses

Le serpent apprend grâce aux récompenses.

J'ai utilisé un système proche de :

Plain Text
Pomme verte -> récompense positive
 
Pomme rouge -> récompense négative
 
Mort -> grosse récompense négative
 
Déplacement -> légère pénalité
``
Show more lines

Le but est de lui faire comprendre naturellement quels comportements sont bons ou mauvais.

8. Comprendre la vision du serpent

Le sujet impose que le serpent ne connaisse pas toute la carte.

Il ne voit que dans les quatre directions :

Plain Text
UP
LEFT
DOWN
RIGHT
Show more lines

Par exemple :

Plain Text
UP : 0 0 G W
 
LEFT : S W
 
DOWN : 0 W
 
RIGHT : R W
Show more lines

avec :

Plain Text
0 = vide
G = pomme verte
R = pomme rouge
S = serpent
W = mur
Show more lines
9. Construction du State

Une grande partie du projet a consisté à créer un état utilisable par le Q-Learning.

Plusieurs versions ont été testées :

Vision complète
Python
(
('0','0','G','W'),
('S','W'),
('R','W'),
('0','W')
)
Show more lines
Vision compressée

Par exemple :

Python
(
0,1,0,4,
1,0,0,1,
...
)
Show more lines

Après beaucoup de tests, j'ai finalement gardé une version qui permettait d'obtenir les meilleurs résultats.

10. Phase de débogage

C'est probablement la partie qui a pris le plus de temps.

Pendant longtemps, je pensais que :

la croissance ne fonctionnait pas ;
le state était mauvais ;
les récompenses étaient mauvaises ;
le Q-Learning était cassé.

J'ai ajouté énormément de logs :

Python
Q VALUES
Show more lines

pour voir exactement ce que le serpent pensait.

Exemple :

Plain Text
UP : -2.3
LEFT : 0.5
DOWN : -1.2
RIGHT : 3.4
Show more lines

Cela m'a permis de comprendre ses choix.

11. Le constat qui a tout changé

Après des heures de debug, j'ai réalisé quelque chose de beaucoup plus simple :

Plain Text
Le Q-Learning fonctionnait déjà.
Show more lines

Le vrai problème était le nombre de sessions d'entraînement.

Au début j'utilisais :

Plain Text
1000 sessions
Show more lines

et je pensais que c'était énorme.

En réalité ce n'était pas assez.

12. Plus d'entraînement

J'ai ensuite augmenté progressivement :

Plain Text
5000 sessions
 
10000 sessions
 
20000 sessions
Show more lines

Et les performances ont complètement changé.

Au lieu de :

Plain Text
Length 3
Length 4
Length 5
Show more lines

j'ai commencé à obtenir :

Plain Text
Length 16
Show more lines

puis :

Plain Text
Length 38
Show more lines

et finalement :

Plain Text
Length 45
Show more lines

sur certains entraînements.

C'est à ce moment-là que j'ai compris que le modèle apprenait réellement.

13. Sauvegarde du modèle

Pour éviter de réentraîner l'IA à chaque fois, j'ai ajouté :

Python
pickle
Show more lines

afin de sauvegarder la Q-Table.

Exemple :

Plain Text
models/
├── 1sess.pkl
├── 10sess.pkl
├── 100sess.pkl
├── 20000sess.pkl
└── best.pkl
Show more lines
14. Chargement du modèle

J'ai ensuite ajouté :

Shell
--load
Show more lines

pour pouvoir réutiliser un modèle déjà entraîné.

Exemple :

Shell
python3 main.py --load models/best.pkl
Show more lines
15. Mode évaluation

Ajout également de :

Shell
--dontlearn
Show more lines

Dans ce mode :

Plain Text
Le serpent n'apprend plus.
Show more lines

Il utilise uniquement les connaissances déjà présentes dans la Q-Table.

J'ai aussi découvert qu'il fallait mettre :

Python
epsilon = 0
Show more lines

ou très proche de zéro pour éviter qu'il continue à faire des actions aléatoires.

16. Spawn aléatoire

Au départ le serpent apparaissait toujours au même endroit.

J'ai modifié le système pour que :

Plain Text
position
+
orientation
Show more lines

soient choisies aléatoirement au début de chaque partie.

Le serpent peut maintenant apparaître :

Plain Text
UP
DOWN
LEFT
RIGHT
Show more lines

conformément au sujet.

17. Interface graphique

Le projet utilisait initialement uniquement :

Plain Text
Terminal
Show more lines

J'ai ensuite développé une interface graphique avec :

Python
pygame
Show more lines

L'interface affiche :

le serpent ;
les pommes vertes ;
la pomme rouge ;
le plateau.
18. Vision du serpent

J'ai ajouté un mode spécial :

Plain Text
Vision Mode
Show more lines

Dans ce mode, on ne voit que ce que le serpent est autorisé à voir.

Tout le reste de la carte est masqué.

Cela permet de visualiser exactement les informations utilisées par l'agent pour prendre ses décisions.

19. Taille de carte configurable

Ajout de paramètres :

Shell
--width
--height
Show more lines

Exemple :

Shell
python3 main.py --width 20 --height 20
Show more lines

Le même modèle peut donc être utilisé sur différentes tailles de cartes.

✅ Résultat final

Le projet contient aujourd'hui :

Q-Learning complet
Q-Table sauvegardable
Chargement de modèles
Mode évaluation
Spawn aléatoire
Interface graphique pygame
Mode vision du serpent
Taille de plateau configurable
Modèles entraînés

Le serpent est capable d'obtenir régulièrement des scores largement supérieurs à l'objectif demandé par le sujet.