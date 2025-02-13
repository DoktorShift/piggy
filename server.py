import json
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your frontend

CONFIG_FILE = "config.json"

# Ensure config file exists or create default with the proper structure
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        default_config = [
            {"name": "config_wifi_ssid_1", "value": ""},
            {"name": "config_wifi_password_1", "value": ""},
            {"name": "config_lnbits_host", "value": ""},
            {"name": "config_lnbits_https_port", "value": ""},
            {"name": "config_lnbits_invoice_key", "value": ""},
            {"name": "config_static_receive_code", "value": ""},
            {"name": "config_fiat_currency", "value": ""},
            {"name": "config_balance_bias", "value": ""},
            {"name": "config_thousands_separator", "value": ""},
            {"name": "config_decimal_separator", "value": ""},
            {"name": "config_show_boot_wisdom", "value": ""},
            {"name": "config_boot_salutation", "value": ""},
            {"name": "config_locale", "value": ""},
            {"name": "config_time_zone", "value": ""},
            {"name": "config_always_run_webserver", "value": ""},
            {"name": "config_update_host", "value": ""},
            {"name": "config_time_server", "value": ""},
            {"name": "config_time_server_path", "value": ""}
        ]
        json.dump(default_config, f, indent=4)
        logging.info("Created default config file with proper structure.")

@app.route("/config.json", methods=["GET"])
def get_config():
    """Serve config.json contents."""
    try:
        with open(CONFIG_FILE, "r") as f:
            config_data = json.load(f)
        logging.info("Served config.json successfully.")
        return jsonify(config_data), 200
    except Exception as e:
        logging.error(f"Error reading config.json: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/config.json", methods=["POST"])
def save_config():
    """Save posted JSON to config.json."""
    try:
        new_config = request.get_json()  # Expect a JSON body
        with open(CONFIG_FILE, "w") as f:
            json.dump(new_config, f, indent=4)
        logging.info(f"Updated config.json: {new_config}")
        return jsonify({"status": "success", "message": "Configuration saved!"}), 200
    except Exception as e:
        logging.error(f"Error saving config.json: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logging.info("Starting Flask server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)

