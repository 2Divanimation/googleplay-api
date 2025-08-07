from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/get-app-info")
def get_app_info():
    url = request.args.get("url")

    if not url or "play.google.com" not in url:
        return jsonify({"error": "Invalid or missing URL."}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find("h1").text.strip()
        description = soup.find("meta", {"name": "description"})['content']
        icon_url = soup.find("img")["src"]

        return jsonify({
            "title": title,
            "description": description,
            "icon_url": icon_url,
            "source_url": url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
