# app.py
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your chain's JSON-RPC endpoint
RPC_URL = "http://multichain_node:1234"  # Example: container name is `multichain_node`, port 1234

@app.route("/")
def index():
    try:
        # Minimal JSON-RPC example:
        # This "liststreamitems" call is specific to MultiChain, but adapt as you like.
        # For other blockchains, change method/params accordingly.
        payload = {
            "jsonrpc": "1.0",
            "id": "curltest",
            "method": "liststreamitems",
            "params": ["YOUR_STREAM_NAME"]  # Replace with the stream name you want
        }
        headers = {"content-type": "application/json"}

        response = requests.post(RPC_URL, json=payload, headers=headers, timeout=5, auth=('multichainrpc','YOUR_RPC_PASSWORD'))
        data = response.json()

        if "result" in data:
            chain_data = data["result"]
        else:
            chain_data = ["No 'result' found in JSON-RPC response. Check your node configuration."]

    except Exception as e:
        chain_data = [f"Error connecting to chain: {e}"]

    # Render a simple HTML table or list
    return """
    <html>
    <head><title>Chain Logs</title></head>
    <body>
      <h1>Blockchain Logs</h1>
      <p>Below are raw items from the chain:</p>
      <ul>
        {}
      </ul>
      <a href="/">Refresh</a>
    </body>
    </html>
    """.format("".join(f"<li>{item}</li>" for item in chain_data))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)