# Speech Recognition Module - Vosk (Français)

Ce projet inclut un module de reconnaissance vocale basé sur l'API Vosk pour le traitement de la langue française.

## 📥 Installation

### 1. Télécharger le modèle Vosk pour le français

Téléchargez le modèle `vosk-model-fr-0.22` depuis le [site officiel de Vosk](https://alphacephei.com/vosk/models).

### 2. Extraire les fichiers du modèle

Une fois téléchargé, extrayez le contenu de l'archive `.tar.gz` ou `.zip`.

### 3. Placer le modèle dans votre répertoire de projet

Déplacez le dossier extrait `vosk-model-fr-0.22` dans le répertoire `models/` de votre projet. La structure de votre projet doit ressembler à ceci :

your-project-folder/ ├── models/ │ └── vosk-model-fr-0.22/ │ ├── am │ ├── conf │ ├── ... (fichiers du modèle) ├── your_speech_recognition_module.py ├── README.md └── ...

shell
Copy
Edit

### 4. Installer les dépendances

Assurez-vous d'avoir installé les dépendances nécessaires. Vous pouvez installer la bibliothèque Vosk avec la commande suivante :

'''bash
pip install vosk
5. Utiliser le module de reconnaissance vocale
Dans votre fichier Python your_speech_recognition_module.py, vous pouvez utiliser le modèle comme suit :

python
Copy
Edit
import vosk
import sys
import os
from vosk import Model, KaldiRecognizer
import wave

# Spécifiez le chemin du modèle
model_path = "models/vosk-model-fr-0.22"  # Assurez-vous que ce chemin est correct

# Vérifiez que le modèle est présent
if not os.path.exists(model_path):
    print(f"Le chemin du modèle {model_path} est introuvable !")
    sys.exit(1)

# Charger le modèle Vosk
model = Model(model_path)

# Utilisation du modèle pour la reconnaissance vocale
# Exemple de code pour une reconnaissance simple avec un fichier audio
wf = wave.open("votre_fichier_audio.wav", "rb")
recognizer = KaldiRecognizer(model, wf.getframerate())

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        print(result)

# Vous pouvez également ajouter des traitements supplémentaires selon vos besoins
🚀 Lancer le module
Une fois que vous avez configuré le modèle et installé les dépendances, vous pouvez exécuter votre module de reconnaissance vocale avec la commande suivante :

bash
Copy
Edit
python your_speech_recognition_module.py
Assurez-vous que votre fichier audio (votre_fichier_audio.wav) est au bon format (par exemple, WAV) et qu'il est placé dans le répertoire approprié.

📋 Notes importantes
Le modèle vosk-model-fr-0.22 est utilisé ici pour la reconnaissance vocale en français.

Vérifiez que le chemin vers le modèle est correct dans votre code avant de l'exécuter.

Vous pouvez ajouter d'autres fichiers audio et adapter le code pour la reconnaissance en temps réel si nécessaire.

🔧 Dépannage
Si vous rencontrez une erreur liée au modèle, assurez-vous que le dossier vosk-model-fr-0.22 est correctement extrait et placé dans le répertoire models/.

Si le fichier audio n'est pas lu correctement, vérifiez qu'il est dans un format compatible et qu'il n'est pas corrompu.

N'hésitez pas à ouvrir une issue si vous rencontrez



