import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def generer_diagramme_sequenciel(time, appareils, data, line_styles=None, title="Diagramme de Séquence"):
    offsets = np.arange(0, len(appareils) * 1.5, 1.5)  # Décalage vertical

    fig, ax = plt.subplots()

    for i, appareil in enumerate(appareils):
        ax.plot(time, data[i] + offsets[i], label=appareil, linestyle=line_styles.get(appareil, '-'))
        ax.axhline(y=offsets[i], color='gray', linestyle='-', linewidth=1)
        ax.axhline(y=offsets[i] + 1, color='gray', linestyle='-', linewidth=0.5)

    for t in time:
        ax.axvline(x=t, color='lightgray', linestyle='-', linewidth=1)

    positions_y = []
    labels_y = []

    for i, offset in enumerate(offsets):
        positions_y.extend([offset, offset + 1])
        labels_y.extend([f'{appareils[i]} [0]', f'{appareils[i]} [1]'])

    ax.set_yticks(positions_y)
    ax.set_yticklabels(labels_y)
    ax.set_ylim(-0.5, max(offsets) + 1.5)
    ax.set_xticks(np.arange(0, max(time) + 1, 1))
    ax.set_xlabel('Step')
    ax.set_title(title, fontsize=20)
    ax.legend()

    st.pyplot(fig)

# Interface Streamlit
st.title('Générateur de Diagramme de Séquence')

# Saisie des paramètres par l'utilisateur
time_max = st.slider('Temps maximum', 0, 12, 12)
time = np.arange(0, time_max + 1)

nombre_appareils = st.number_input('Nombre d\'appareils', min_value=1, max_value=10, value=5)
appareils = [st.text_input(f'Nom de l\'appareil {i+1}', f'Appareil {i+1}') for i in range(nombre_appareils)]

data = []
line_styles = {}
for i in range(nombre_appareils):
    etats = st.text_input(f'États pour {appareils[i]} (séparés par des virgules)', '0,0,0,0,0,1,1,1,0,0,0,0,0')
    data.append(np.array([int(x) for x in etats.split(',')]))
    style = st.selectbox(f'Style de ligne pour {appareils[i]}', ['-', '--'], index=0)
    line_styles[appareils[i]] = style

title = st.text_input('Titre du diagramme', 'Diagramme de Séquence')

# Génération du diagramme
if st.button('Générer le diagramme'):
    generer_diagramme_sequenciel(time, appareils, data, line_styles, title)
