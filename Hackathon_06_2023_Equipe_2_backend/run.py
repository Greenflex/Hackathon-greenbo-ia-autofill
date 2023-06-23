import base64
import json
import requests
import curlify


def encode_pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as file:
        encoded_pdf = base64.b64encode(file.read()).decode("utf-8")
    return encoded_pdf


def send_post_request(url, payload):
    response = requests.post(url, data=payload)
    return response


# Main function
def main():
    pdf_path = "./facture.pdf"
    endpoint_url = "http://localhost:5000/extract_pdf_content"

    encoded_pdf = encode_pdf_to_base64(pdf_path)
    print(encoded_pdf)

    payload = {"pdf_file": encoded_pdf}

    response = send_post_request(endpoint_url, payload)

    if response.status_code == 200:
        resp = response.text.encode("utf-8").decode("unicode_escape")
        print(resp)
        print(json.loads(resp))
    else:
        print("PDF content extraction failed.")


if __name__ == "__main__":
    main()
