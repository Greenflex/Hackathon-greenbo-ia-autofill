"""
To run this code please provide a valid openAI API token like so:

API_TOKEN=your_openai_api_token python flask_api.py
"""


import base64
import io
import json
import os
import traceback

import PyPDF2
import requests
from dotenv import load_dotenv
from flask import Flask, request

app = Flask(__name__)


# Load environment variables from .env
load_dotenv()


@app.route("/extract_pdf_content", methods=["POST"])
def extract_pdf_content():
    OPENAI_API_TOKEN = os.getenv("API_TOKEN")
    print(OPENAI_API_TOKEN)

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
        print("1- Extraction du texte de ce PDF...")
        print(
            "2- Création de la question à poser à l'IA textuelle à partir du template et du texte extrait..."
        )
        print("3- Appel de l'IA textuelle avec la question...")
        print(
            "4- On retourne le JSON renvoyé par l'IA textuelle, au format demandé par GreenBO"
        )

        # Extract the text content from each page
        content = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            decoded_text = page_text
            content.append(decoded_text)

        # Limit content to 4000 chars not to use too much tokens
        content = str(content)[:4000]
        print(content[:1000])

        # Format the AI question
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
            """A partir de ce texte:\n%s\n\npeux tu extraire le JSON suivant:\n%s"""
            % (content, json_template)
        )
        print(question_text)

        # Call the text AI OpenAI
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

        response_data = requests.post(url, headers=headers, data=json.dumps(data))
        if "choices" in response_data:
            # Access the data within the "choices" key
            out_json = response_data["choices"][0]["message"]["content"]
            # Process the data as needed
            res = response_data.json()
            print("\n [INFO] Response", res)
            return out_json
        else:
            # Handle the case when the "choices" key is not present in the response
            raise ValueError("Unexpected response structure")

    except Exception as e:
        print(traceback.print_exc())
        return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run()
