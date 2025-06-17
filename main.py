from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

PROMO_PAGE = "https://discoverhub.tv/promos"  # Replace if needed

def find_codes_from_page():
    try:
        response = requests.get(PROMO_PAGE)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        codes = re.findall(r'\b[A-Z0-9]{6,10}\b', text)
        unique_codes = list(set(c for c in codes if "CODE" in text or "promo" in text.lower()))
        return unique_codes
    except Exception as e:
        return [f"Error: {str(e)}"]

@app.route("/")
def index():
    codes = find_codes_from_page()
    return render_template("index.html", codes=codes)

if __name__ == "__main__":
    app.run(debug=True)
