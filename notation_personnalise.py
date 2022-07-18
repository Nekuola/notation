# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 16:09:07 2022

@author: kevin
"""



#
##########
#
# IMPORT
#
##########
#

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#
##########
#
# Import de l'excel de notation
#      Calcul des notes
#
##########
#

table = pd.read_excel('test_notation.xlsx')
# NB : SI FICHIER XLSX, INSTALLER LA VERSION
# 1.20 DE XLRD : pip install xlrd==1.2.0

#print(table)
n_question = len(table)
bareme_total = table.Bareme.sum()
liste_eleves = table.columns[3:]
liste_theme = []
dict_theme = {}
dict_reussite_theme = {}

# Construction du dictionnaire theme
for themes in table.Theme:
    for theme in themes.replace(' ','').split(','):
        if theme not in liste_theme:
            liste_theme.append(theme)
            i = [1 if theme in x else 0 for x in table.Theme]
            i = [j/sum(i) for j in i]
            dict_theme[theme] = i
dict_theme['Total'] = [1]*n_question

# Construction du dictionnaire de note pour
# chaque eleve
for eleve in liste_eleves:
    d = {}
    for theme in dict_theme.keys():
        note = (table.Bareme * table[eleve] *
               dict_theme[theme]).sum() / (3 *
               (table.Bareme * dict_theme[theme]).sum())
        d[theme] = note
    dict_reussite_theme[eleve] = d

print(dict_reussite_theme)

# Construction de la moyenne
d = {}
for theme in dict_theme.keys():
    d[theme] = np.mean([dict_reussite_theme[i][theme] for i in liste_eleves])
dict_reussite_theme['Moyenne'] = d

#
##########
#
# Plot des histogrammes personnalisés
#
##########
#

# Parameters
barWidth = 0.25
couleurEleve = '#229954'
couleurMoyenne = '#73c6b6'
font = {'family':'serif','color':'darkgreen','size':15}

# Bar position
r1 = np.arange(len(liste_theme)+1)
r2 = [x + barWidth for x in r1]

# Plot
for eleve in liste_eleves:
    fig, ax = plt.subplots(figsize=(8,4))
    # Barre notes élève
    graph1 = ax.bar(r1, dict_reussite_theme[eleve].values(),
           width=barWidth, color=couleurEleve,
           label=eleve)

    # Score au dessus des barres
    i = 0
    for p in graph1:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        plt.text(x+width/2,
                 y+height*1.01,
                 '{:.1f}%'.format(list(dict_reussite_theme[eleve].values())[i]*100),
                 ha='center',
                 weight='bold')
        i+=1

    # Barre note moyenne
    ax.bar(r2, dict_reussite_theme['Moyenne'].values(),
           width=barWidth, color=couleurMoyenne,
           label='Moyenne de la classe')

    # Axe X
    plt.xticks([r+barWidth for r in range(len(liste_theme)+1)],
                dict_reussite_theme[eleve])


    plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=2)

    plt.subplots_adjust(bottom=0.15)
    ax.set_ylim([0, 1.1])
    plt.xlabel('Compétences', fontdict=font)
    plt.ylabel('Réussite (%)', fontdict=font)
#    plt.xticks(rotation=90)

    plt.savefig('img/bilan_{}.pdf'.format(eleve), format='pdf')



#
##########
#
# Production des rapports
#
##########
#


with open('compte_rendu_format.txt', encoding='utf8') as f:
    report = f.readlines()

for eleve in liste_eleves:

    report.append("\\section*{Résultat de l'examen de SI} \n \n")
    report.append("Note obtenue au dernier examen : {:.1f}/20 \n \n".format(dict_reussite_theme[eleve]['Total']*20))
    report.append("Classement : {}e sur {} élèves.\n\n".format(len([i for i in liste_eleves if dict_reussite_theme[i]['Total']> dict_reussite_theme[eleve]['Total']])+1, len(liste_eleves)))

    report.append("Tu trouveras ci-dessous un bilan détaillé de l'examen, avec ta réussite pour chaque compétence abordée. \n \n")
    report.append("Une brève description de ces compétences est donnée juste après, afin que tu saches quoi revoir.\n\n")

    report.append("\\begin{figure}[htbp] \n\\centering \n\\includegraphics[width=\\textwidth]{img/bilan_" +
                 eleve + ".pdf} \n\\end{figure} \n\n")

    report.append("\\UPSTIcompetences \n")
    report.append("\\UPSTItableauCompetences{ \n")
    for theme in liste_theme:
        report.append("\\UPSTIligneTableauCompetence{")
        report.append("{}".format(theme))
        report.append("} \n")
    report.append("} \n")
    report.append('\\clearpage \n')

report.append('\\end{document}')



with open('compte_rendu.txt', 'w', encoding='utf8') as f:
    f.write(''.join(report))



