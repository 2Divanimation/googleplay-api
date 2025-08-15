from flask import Flask, request, jsonify
from google_play_scraper import app as gp_app
import re

app = Flask(__name__)

def extract_package_name(url):
    match = re.search(r"id=([a-zA-Z0-9._]+)", url)
    if match:
        return match.group(1)
    return None

@app.route("/get-app-info", methods=["GET"])
def get_app_info():
    url = request.args.get("url")
    if url:
        package_name = extract_package_name(url)
    else:
        package_name = "com.instagram.android"  # پیش‌فرض

    if not package_name:
        return jsonify({"error": "Invalid URL"}), 400

    try:
        app_details = gp_app(package_name, lang="en", country="us")

        data = {
            "appName": app_details.get("title"),
            "companyName": app_details.get("developer"),
            "downloads": app_details.get("installs"),
            "score": str(app_details.get("score")),
            "ageRating": app_details.get("contentRating"),
            "reviews": str(app_details.get("ratings")),
            "iconUrl": app_details.get("icon"),
            "screenshots": app_details.get("screenshots"),
            "updatedDate": app_details.get("released"),

            "price": str(app_details.get("price")),
            "free": app_details.get("free"),
            "currency": app_details.get("currency"),
            "offersIAP": app_details.get("offersIAP")
        }
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






