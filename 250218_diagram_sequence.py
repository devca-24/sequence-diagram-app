import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Dernière version du code pour générer le diagramme de séquence "Filtration"
# ---------------------------------------------------------

# 1) Définition des paliers (steps) : de 0 à 14
steps = np.arange(0, 15)

# 2) Définition des signaux (chaque liste doit avoir la même longueur que 'steps')
#    Les valeurs correspondent aux niveaux (0 = fermé/à l'arrêt, >0 = ouvert/en marche).
#    Vous pouvez ajuster ces valeurs si vous souhaitez refléter plus précisément vos consignes.

# --- Filtration titres ---
filtration_basse = [
    0, 0,  # step 0 à 1
    1, 1, 1, 1, 1, 1, 1, 1,  # step 2 à 9
    1,     # step 10
    0, 0, 0, 0  # step 11 à 14
]

filtration_haute = [
    0, 0,
    2, 2, 2, 2, 2, 2, 2, 2,
    2,
    0, 0, 0, 0
]

# Si besoin d’une troisième courbe pour “filtration très haute” (exemple) :
# filtration_tres_haute = [
#     0, 0,
#     3, 3, 3, 3, 3, 3, 3, 3,
#     3,
#     0, 0, 0, 0
# ]

# --- Vannes / Pompes ---
vanne_cuve_permeat = [
    0, 0,
    5, 4, 5, 5, 5, 5, 5, 5,
    5,
    0, 0, 0, 0
]

vanne_entree_uf = [
    0, 0,
    4, 4, 4, 4, 4, 4, 4, 4,
    4,
    0, 0, 0, 0
]

vanne_eau_brute = [
    0, 0,
    3, 3, 3, 3, 3, 3, 3, 3,
    3,
    0, 0, 0, 0
]

pompe_eau_brute = [
    0, 0,
    2, 2, 2, 2, 2, 2, 2, 2,
    2,
    0, 0, 0, 0
]

# ---------------------------------------------------------
# 3) Création de la figure et des tracés
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

# Filtration
plt.step(steps, filtration_basse, where='post',
         label='Filtration titre basse', color='green')
plt.step(steps, filtration_haute, where='post',
         label='Filtration titre haute', color='red', linewidth=2)

# Exemple si vous aviez une filtration "très haute" en pointillé
# plt.step(steps, filtration_tres_haute, where='post',
#          label='Filtration titre très haute', color='red', linestyle='--')

# Vannes et pompe
plt.step(steps, vanne_cuve_permeat, where='post',
         label='Vanne cuve perméat E8.ST.2.01', color='purple')
plt.step(steps, vanne_entree_uf, where='post',
         label='Vanne entrée UF E8.S2.02', color='red', linestyle='--')
plt.step(steps, vanne_eau_brute, where='post',
         label='Vanne eau brute E8.S1.01', color='orange')
plt.step(steps, pompe_eau_brute, where='post',
         label='Pompe eau brute E8.P1.01', color='teal')

# ---------------------------------------------------------
# 4) Mise en forme du diagramme
# ---------------------------------------------------------
plt.title('Diagramme de séquence : Filtration\nDate : 03/09/2024', fontsize=14)
plt.xlabel('Step')
plt.ylabel('Valeur (ouverture / consigne)')

# Affichage des légendes, grille, limites
plt.grid(True)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
plt.xlim(0, 14)
plt.ylim(0, 6)

# Ajout d’un texte explicatif (facultatif) : QF et CL
plt.text(
    0.02, 1.03,
    'QF = Régulation du débit de filtration\n'
    'CL = Critères de lavage\n'
    'tR = Durée de filtration max\n'
    'Vfil max = Volume de filtration max\n'
    'FRam = Perméabilité min',
    transform=plt.gca().transAxes,
    fontsize=9,
    va='bottom'
)

# ---------------------------------------------------------
# 5) Affichage du graphique
# ---------------------------------------------------------
plt.tight_layout()
plt.show()

