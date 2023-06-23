"""
To run thiscode please provide a valid openAI API token like so:

API_TOKEN=your_openai_api_token python flask_api.py
"""


from flask import Flask, request
import base64
import PyPDF2
import traceback
import io
import json
import requests
import os
from time import sleep
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)


@app.route("/extract_pdf_content", methods=["POST"])
def extract_pdf_content():
    OPENAI_API_TOKEN = os.getenv("API_TOKEN")

    try:
        # Get the base64 encoded PDF file from the request
        encoded_pdf = request.form["pdf_file"]
        print("PDF encodé en base64 reçu...")

        # Decode the base64 string into bytes
        pdf_bytes = base64.b64decode(encoded_pdf)

        # Create a file-like object from the PDF bytes
        pdf_stream = io.BytesIO(pdf_bytes)

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        print("\n1- Extraction du texte de ce PDF en base64...")

        # Extract the text content from each page
        content = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            decoded_text = page_text
            content.append(decoded_text)

        # Limit content to 4000 chars not to use too much tokens
        content = str(content)[:4000]

        # Format the AI question
        print(
            "\n2- Création de la question à poser à l'IA textuelle à partir du template et du texte extrait..."
        )

        json_template = json.dumps(
            {
                "commande": "",
                "modele": "",
                "date_de_la_facture": "",
                "reference": "{numero facture}",
                "montant_ht": "{montant HT en euros}",
                "montant_devise_ht": "{montant HT dans la devise de la facture}",
                "date_comptable": "",
                "mode_de_reglement": "",
                "type": "{type de facture}",
                "commentaire": "",
                "envoi_demande_bap": "",
                "bap_reçu_le": "",
                "tva": "{pourcentage de TVA}",
                "date_decheance_de_facture": "",
                "date_decheance_facture_reelle": "",
                "societe_de_refactoring": "",
                "date_de_reception_de_facture": "",
            }
        )
        question_text = (
            """A partir de ce texte:\n%s\n\npeux tu formater le JSON suivant:\n%s"""
            % (content, json_template)
        )
        question_text += """\nPrend des initiatives pour arriver à remplir les valeurs associées aux clés de ce JSON"""

        # Call the text AI
        print("\n3- Appel de l'IA textuelle avec la question...")
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_TOKEN}",
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": question_text}],
            "temperature": 0.7,
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.json())
        res = response.json()
        out_json = res["choices"][0]["message"]["content"]

        print(
            "\n4- On retourne le JSON renvoyé par l'IA textuelle, au format demandé par GreenBO"
        )
        out_json = "{" + out_json.split("{")[1]
        print(out_json.encode("utf-8").decode("unicode_escape"))

        return out_json

    except Exception as e:
        print(traceback.print_exc())
        return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run()
