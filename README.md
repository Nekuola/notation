# Notation automatisée
Fichier de notation produisant un rapport automatique sur les compétences de l'élève.

# How to use
## Fichier notation
Faire une copie du fichier test_notation.
Fixer les questions, le barême, et les thèmes abordées à chaque question en fonction de l'examen, en suivant le format fourni (thème = compétence avec la notation UPSTI).

Pour chaque élève, appliquer la notation suivante : 
- 3 = Question parfaitement réalisée
- 2 = Question presque parfaitement réalisée
- 1 = Début de raisonnement ou de calcul, mais non complètement abouti
- 0 = Réponse fausse / Question non abordée

## Fichier python notation personnalisé
Changer la ligne 32 table = pd.read_excel('test_notation.xlsx') en mettant à la place le nom de votre fichier de notation.

Lancer le programme. Il produira automatiquement :
- Des figures bilans pour chaque élève, enregistré dans le dossier img
- Un document texte compte_rendu.txt, qui une fois compilé donne un document latex complet où, sur chaque feuille, est présentée un bilan détaillé pour chaque élève.
A imprimer, puis à rendre avec la copie.

