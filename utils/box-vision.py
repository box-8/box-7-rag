import os
import base64
import requests
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Fonction pour encoder une image en base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Fonction pour ouvrir une boîte de dialogue pour sélectionner une image
def get_image_path():
    # Créer une instance de la fenêtre Tkinter
    root = Tk()
    # Cacher la fenêtre principale Tkinter
    root.withdraw()
    # Ouvrir une boîte de dialogue pour choisir un fichier image
    file_path = askopenfilename(
        title="Sélectionner une image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    # Vérifier si un fichier a été sélectionné
    if not file_path:
        raise ValueError("Aucun fichier n'a été sélectionné")
    return file_path

# Question "métier"
question = "Quelles non conformités peut-on voir sur cette photo de chantier ?"

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("La clé API OpenAI n'est pas définie dans les variables d'environnement")

# Obtenir le chemin de l'image sélectionnée par l'utilisateur
image_path = get_image_path()

# Encoder l'image en base64
base64_image = encode_image(image_path)

# On fait appel à OpenAI pour analyser une photo
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Création du payload pour l'appel à l'API
payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": question
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 300  # Paramétrable
}

# Envoyer la requête à l'API OpenAI
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# Afficher la réponse
print(response.json())
