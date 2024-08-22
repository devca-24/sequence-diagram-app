import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

# Dictionnaires de traduction
translations = {
    'fr': {
        'title': 'Générateur de Diagramme de Séquence',
        'time_max': 'Temps maximum',
        'num_devices': 'Nombre d\'appareils',
        'device_name': 'Nom de l\'appareil',
        'states': 'États pour',
        'line_style': 'Style de ligne pour',
        'durations': 'Durée (en secondes) pour chaque appareil (sous la courbe)',
        'generate': 'Générer le diagramme',
        'download': 'Télécharger le diagramme en PDF',
        'step': 'Étape',
        'sequence_diagram': 'Diagramme de Séquence',
    },
    'de': {
        'title': 'Sequenzdiagramm-Generator',
        'time_max': 'Maximale Zeit',
        'num_devices': 'Anzahl der Geräte',
        'device_name': 'Name des Geräts',
        'states': 'Zustände für',
        'line_style': 'Linienstil für',
        'durations': 'Dauer (in Sekunden) für jedes Gerät (unter der Kurve)',
        'generate': 'Diagramm erzeugen',
        'download': 'Diagramm als PDF herunterladen',
        'step': 'Schritt',
        'sequence_diagram': 'Sequenzdiagramm',
    },
    'it': {
        'title': 'Generatore di Diagrammi di Sequenza',
        'time_max': 'Tempo massimo',
        'num_devices': 'Numero di dispositivi',
        'device_name': 'Nome del dispositivo',
        'states': 'Stati per',
        'line_style': 'Stile di linea per',
        'durations': 'Durata (in secondi) per ogni dispositivo (sotto la curva)',
        'generate': 'Genera il diagramma',
        'download': 'Scarica il diagramma in PDF',
        'step': 'Passo',
        'sequence_diagram': 'Diagramma di Sequenza',
    }
}

def generer_diagramme_sequenciel(time, appareils, data, line_styles=None, durations=None, title="Diagramme de Séquence"):
    try:
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
        ax.set_xlabel(translations[lang]['step'])
        ax.set_title(title, fontsize=20)
        ax.legend()

        # Ajout des durées sous la courbe concernée
        if durations:
            for i, duration_info in enumerate(durations):
                appareil_index = appareils.index(duration_info['appareil'])
                for step, duration in zip(duration_info['steps'], duration_info['durations']):
                    ax.text(step, offsets[appareil_index] - 0.3, f'{duration}s', ha='center', va='center', fontsize=12, color='black')

        st.pyplot(fig)
        return fig

    except Exception as e:
        st.error(f"Erreur lors de la génération du diagramme : {e}")

# Interface Streamlit
lang = st.selectbox('Choisissez la langue', ['fr', 'de', 'it'])
st.title(translations[lang]['title'])

# Saisie des paramètres par l'utilisateur
time_max = st.slider(translations[lang]['time_max'], 0, 12, 12)
time = np.arange(0, time_max + 1)

nombre_appareils = st.number_input(translations[lang]['num_devices'], min_value=1, max_value=10, value=5)
appareils = [st.text_input(f"{translations[lang]['device_name']} {i+1}", f'Appareil {i+1}') for i in range(nombre_appareils)]

data = []
line_styles = {}
for i in range(nombre_appareils):
    etats = st.text_input(f"{translations[lang]['states']} {appareils[i]} (séparés par des virgules)", '0,0,0,0,0,1,1,1,0,0,0,0,0')
    data.append(np.array([float(x) for x in etats.split(',')]))  # Accepte les demi-états
    style = st.selectbox(f"{translations[lang]['line_style']} {appareils[i]}", ['-', '--'], index=0)
    line_styles[appareils[i]] = style

durations = []
if st.checkbox('Ajouter des durées spécifiques sous les courbes'):
    for appareil in appareils:
        steps = st.text_input(f"Étapes pour afficher la durée sous {appareil} (séparées par des virgules)", '5,10')
        dur_values = st.text_input(f"Durées correspondantes (en secondes) pour {appareil} (séparées par des virgules)", '5,3')
        durations.append({
            'appareil': appareil,
            'steps': [int(x) for x in steps.split(',')],
            'durations': [int(x) for x in dur_values.split(',')]
        })

title = st.text_input(translations[lang]['sequence_diagram'], translations[lang]['sequence_diagram'])

# Génération du diagramme
if st.button(translations[lang]['generate']):
    fig = generer_diagramme_sequenciel(time, appareils, data, line_styles, durations, title)
    
    # Option de téléchargement en PDF
    buf = io.BytesIO()
    if fig:
        fig.savefig(buf, format="pdf")
        st.download_button(
            label=translations[lang]['download'],
            data=buf,
            file_name="sequence_diagram.pdf",
            mime="application/pdf"
        )
