"""
This is the main frontend of the Hackathon
"""

#  Import librairies

import json

import pandas as pd
import requests
import streamlit as st


def main():
    #  Sidebar
    with st.sidebar:
        st.markdown("# Configuration ")
        st.divider()

        ## Upload a PDF file
        st.write("## Déposer le PDF de la facture")

        uploaded_file = st.file_uploader("", type="pdf")
        print(type(uploaded_file))
        if uploaded_file is not None:
            files = {"file": uploaded_file}

    # Main page
    st.title("Outil de Saisie Intelligent")
    st.divider()

    st.info(
        "Cet outil vous aidera à extraire les informations définie dans le template depuis le PDF de la facture"
    )
    st.warning(
        "Une vérification de votre part est nécessaire, comme l'IA n'est pas un outil parfait , elle peu donc faire des erreurs."
    )
    # st.divider()

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

        # Define the API endpoint URL
        url = "https://api.example.com/endpoint"

        # Send a GET request
        # response = requests.post(url, files=files, timeout=30)

        # Check the response status code
        # if response.status_code == 200:
        # Request was successful
        # data = response.json()  # Parse the response JSON data
        data = {
            "commande": "CMD-2023-1234",
            "modele": "ABC123",
            "date_de_la_facture": "2023-06-22",
            "reference": "REF-2023-5678",
            "montant_ht": "1500.00",
            "montant_devise_ht": "1200.00",
            "date_comptable": "2023-06-30",
            "mode_de_reglement": "Virement bancaire",
            "type": "Facture",
            "commentaire": "Merci pour votre commande !",
            "envoi_demande_bap": "Oui",
            "bap_reçu_le": "2023-06-25",
            "tva": "20%",
            "date_decheance_de_facture": "2023-07-22",
            "date_decheance_facture_reelle": "2023-07-25",
            "societe_de_refactoring": "ABC Factoring",
            "date_de_reception_de_facture": "2023-06-23",
        }

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

        # else:
        #     # Request failed
        #     st.write("Request failed with status code:", response.status_code)

    # get config parameters


if __name__ == "__main__":
    main()
