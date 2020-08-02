# imports
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# const
revenues_particuliers = [[2428431, 13000],
                         [1921550, 38000],
                         [909528, 60000],
                         [657661, 85000],
                         [445529, 300000],
                         [10595, 750000],
                         [3587, 2000000]]


# defs
def calculerDataTaux(sal, imp):
    data_list = []

    for salaire in sal:
        data = 0

        for impot in imp:
            if salaire >= impot[1]:
                data = impot[0]

        data_list.append(data)

    return data_list


def calculerDataSalaire(sal, imp):
    data_list = []
    impot_ajout_tranche = calculImpotTranche(imp)

    for salaire in sal:
        data = calculUnSalaire(imp, impot_ajout_tranche, salaire)
        data_list.append(data)

    return data_list


def calculUnSalaire(imp, tranche, salaire):
    data = 0
    montant_restant = salaire

    for i in range(len(imp)):
        if tranche[i] == 0:
            data += montant_restant * (1 - imp[i][0])
        elif montant_restant >= tranche[i]:
            montant_restant -= tranche[i]
            data += tranche[i] * (1 - imp[i][0])
        elif montant_restant < tranche[i]:
            data += montant_restant * (1 - imp[i][0])
            montant_restant = 0

    return data


def calculImpotTranche(imp):
    impot_ajout_tranche = []
    for i in range(len(imp)):
        try:
            impot_ajout_tranche.append(imp[i+1][1] - imp[i][1])
        except IndexError:
            impot_ajout_tranche.append(0)

    return impot_ajout_tranche


def afficherFigure(sal, data_t, data_s):
    fig, ax1 = plt.subplots()

    color = "tab:blue"
    ax1.set_xlabel("Salaire avant impôt ($)")
    ax1.set_ylabel("Salaire après impôt ($)")
    ax1.plot(sal, data_s, color=color)
    ax1.plot(sal, sal, color="tab:green")
    ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()

    color = "tab:red"
    ax2.set_ylabel("Taux d'imposition")
    ax2.plot(sal, data_t, color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    fig.tight_layout()

    root = tk.Tk()

    bar = FigureCanvasTkAgg(fig, root)
    bar.get_tk_widget().pack()

    root.mainloop()


def afficherRevenue(sal, data_t, data_s, rev, imp):
    rev_apres_imp = []
    tranche = calculImpotTranche(imp)
    for r in rev:
        apres_imp = calculUnSalaire(imp, tranche, r[1])
        rev_apres_imp.append(r[1] - apres_imp)

    total = 0
    for i in range(len(rev)):
        total += rev[i][0] * rev_apres_imp[i]

    print(f"Le gouvernement reçoit {total} en impôt!")


######################
# Debut du main loop #
######################

imposition = []

print("Bienvenue au visualisateur d'imposition Québécois!")
type_impot = input("Voulez vous visualiser \
l'imposition a.ctuelle ou en créer un n.ouvelle?[a/n] ")

if type_impot == 'a':
    imposition = [[0.15, 0], [0.20, 44545], [0.24, 89080], [0.2575, 108390]]

elif type_impot == 'n':
    try:
        nbre_pallier = int(input("Combien \
de pallier d'imposition voulez-vous créer? "))

        for pallier in range(nbre_pallier):
            print(f"Pallier #{pallier + 1}")
            taux = float(input("Taux?[0-1] "))
            montant = int(input("Montant minimum? (Le premier à zéro) "))
            imposition.append([taux, montant])
    except ValueError:
        print("Mauvaise option! Je quitte!")
        exit()

else:
    print("Mauvaise option! Je quitte!")
    exit()

max_sal = int(input("Jusqu'à combien de dollars \
voulez-vous afficher les taux d'impositions? "))

salaire = range(0, max_sal, 1000)
data_taux = calculerDataTaux(salaire, imposition)
data_salaire = calculerDataSalaire(salaire, imposition)

afficherRevenue(salaire, data_taux, data_salaire,
                revenues_particuliers, imposition)
afficherFigure(salaire, data_taux, data_salaire)

