const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");

const app = express();
const PORT = 3000;

app.use(cors()); // Autoriser les requêtes cross-origin

// ✅ Nouvelle route POST pour la reconnaissance vocale
app.post("/speech-to-text", (req, res) => {
  console.log("🟡 Requête reçue à /speech-to-text");

  const python = spawn("python", ["-u", "total_vosk.py"]);

  let finalText = "";

  python.stdout.on("data", (data) => {
    const lines = data.toString().split("\n");
    for (let line of lines) {
      try {
        const parsed = JSON.parse(line);
        if (parsed.text) {
          finalText = parsed.text;
        }
      } catch (err) {
        // Ligne non-JSON → log seulement
        console.log("📥 Log:", line);
      }
    }
  });

  python.stderr.on("data", (err) => {
    console.error("🔴 Erreur Python :", err.toString());
  });

  python.on("close", (code) => {
    console.log(`✅ Script terminé (code ${code})`);
    res.json({ text: finalText });
  });
});

// Démarrer le serveur
app.listen(PORT, () => {
  console.log(`🚀 Serveur Node.js démarré sur http://localhost:${PORT}`);
});
