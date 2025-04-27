import sys
import os
import json
import pyaudio
import vosk
import time

# Vérifier si le modèle est déjà chargé pour éviter de le recharger à chaque appel
if not hasattr(sys.modules[__name__], "vosk_model"):
    model_path = "models/vosk-model-fr-0.22"  # Spécifie le modèle à utiliser
    if not os.path.exists(model_path):
        print(f"\u274C Modèle introuvable : {model_path}")
        sys.exit(1)
    sys.modules[__name__].vosk_model = vosk.Model(model_path)

model = sys.modules[__name__].vosk_model

def recognize_audio():
    samplerate = 16000  # Fréquence d'échantillonnage
    p = pyaudio.PyAudio()

    # Vérifier les périphériques audio disponibles
    for i in range(p.get_device_count()):
        print(p.get_device_info_by_index(i))
    
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=samplerate, input=True, frames_per_buffer=4096)
    stream.start_stream()

    print("\U0001F3A4 Parlez maintenant...")
    rec = vosk.KaldiRecognizer(model, samplerate)

    last_speech_time = time.time()
    silence_threshold = 2  # Temps en secondes pour détecter une pause
    transcription = ""

    try:
        with open("resultat_transcription.txt", "a", encoding="utf-8") as f:  # Ouvre le fichier une seule fois
            while True:
                data = stream.read(4096, exception_on_overflow=False)
                if len(data) == 0:
                    break

                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if "text" in result and result["text"]:
                        transcription += result["text"] + " "
                        last_speech_time = time.time()
                else:
                    partial_result = json.loads(rec.PartialResult())
                    print(f"\U0001F50D Tentative de reconnaissance : {partial_result.get('partial', '')}")
                    last_speech_time = time.time()

                # Vérifie si l'utilisateur s'est arrêté de parler
                if time.time() - last_speech_time > silence_threshold and transcription:
                    print(f"\u2705 Texte reconnu : {transcription.strip()}")

                    # Sauvegarde du résultat dans le fichier texte
                    f.write(transcription.strip() + "\n")
                    f.flush()  # Assure que les données sont écrites immédiatement
                    os.fsync(f.fileno())  # Forcer l'écriture sur le disque

                    transcription = ""
                    last_speech_time = time.time()

    except KeyboardInterrupt:
        print("\n\U0001F6D1 Arrêt manuel détecté.")
        if transcription:  # Vérifie s'il y a du texte non enregistré
            print(f"\U0001F4BE Sauvegarde finale : {transcription.strip()}")
            with open("resultat_transcription.txt", "a", encoding="utf-8") as f:
                f.write(transcription.strip() + "\n")
        print("\u2705 Tout a été enregistré avant la fermeture.")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    recognize_audio()
