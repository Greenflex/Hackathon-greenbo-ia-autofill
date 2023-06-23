"""
This is the main frontend of the Hackathon
"""

#  Import librairies

import pandas as pd
import requests
import streamlit as st
import base64
import json


def encode_pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as file:
        encoded_pdf = base64.b64encode(file.read()).decode("utf-8")
    return encoded_pdf


def send_post_request(url, payload):
    response = requests.post(url, data=payload)
    return response


def main():
    #  Sidebar
    with st.sidebar:
        st.markdown("# Configuration ")
        st.divider()

        ## Upload a PDF file
        st.write("## Déposer le PDF de la facture")

        uploaded_file = st.file_uploader("", type="pdf")
        if uploaded_file is not None:
            pdf_contents = uploaded_file.read()
            encoded_pdf = base64.b64encode(pdf_contents).decode("utf-8")

    # Main page
    st.title("Outil de Saisie Intelligent")
    st.divider()

    st.info(
        "Cet outil vous aidera à extraire les informations définie dans le template depuis le PDF de la facture"
    )
    st.warning(
        "Une vérification de votre part est nécessaire, comme l'IA n'est pas un outil parfait , elle peu donc faire des erreurs."
    )

    ## Add a button to send the request to the backend
    st.write("## Saisir votre demande à l'IA")

    st.text_input(
        "",
        value="Bonjour, je veux extraire les informations définies dans le template de saisie depuis le PDF",
    )
    if st.checkbox("Visualiser le template de saisie"):
        # Load the JSON data from a file
        with open("template_saisie.json", "r") as file:
            json_data = json.load(file)

        # Display the JSON object
        st.json(json_data)

    button_status = st.button("Envoyer")

    if button_status:
        # Backend API call
        st.success("Envoi de la requête à l'API ...")

        # Send a Post request
        endpoint_url = "http://localhost:5000/extract_pdf_content"
        payload = {"pdf_file": encoded_pdf}
        response = send_post_request(endpoint_url, payload)

        if response.status_code == 200:
            resp = response.text.encode("utf-8").decode("unicode_escape")
            data = json.loads(resp)
            print(resp)
            print(data)
            # Access the values in the JSON object

            commande = data["commande"]
            modele = data["modele"]
            date_de_la_facture = data["date_de_la_facture"]
            reference = data["reference"]
            montant_ht = data["montant_ht"]
            montant_devise_ht = data["montant_devise_ht"]
            date_comptable = data["date_comptable"]
            mode_de_reglement = data["mode_de_reglement"]
            type_facture = data["type"]
            commentaire = data["commentaire"]
            envoi_demande_bap = data["envoi_demande_bap"]
            bap_recu_le = data["bap_reçu_le"]
            tva = data["tva"]
            date_decheance_facture = data["date_decheance_de_facture"]
            date_decheance_facture_reelle = data["date_decheance_facture_reelle"]
            societe_de_refactoring = data["societe_de_refactoring"]
            date_reception_facture = data["date_de_reception_de_facture"]
            # and so on...

            st.write("## Information extraite par l'IA")

            # Display the values in the Streamlit app
            st.write("Commande:", commande)
            st.write("Modèle:", modele)
            st.write("Date de la facture:", date_de_la_facture)
            st.write("Référence:", reference)
            st.write("Montant HT:", montant_ht)
            st.write("Montant devise HT:", montant_devise_ht)
            st.write("Date comptable:", date_comptable)
            st.write("Mode de règlement:", mode_de_reglement)
            st.write("Type de facture:", type_facture)
            st.write("Commentaire:", commentaire)
            st.write("Envoi demande BAP:", envoi_demande_bap)
            st.write("BAP reçu le:", bap_recu_le)
            st.write("TVA:", tva)
            st.write("Date d'échéance de facture:", date_decheance_facture)
            st.write("Date d'échéance facture réelle:", date_decheance_facture_reelle)
            st.write("Société de refactoring:", societe_de_refactoring)
            st.write("Date de réception de facture:", date_reception_facture)

        else:
            print("PDF content extraction failed.")

    # get config parameters


if __name__ == "__main__":
    main()
