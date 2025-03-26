from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Use the bridging node for RPC
RPC_URL = "http://bridge_node:7041"

@app.route("/")
def index():
    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "liststreamitems",
        "params": ["YOUR_STREAM_NAME"]  # Replace with the stream name you want
    }
    headers = {"content-type": "application/json"}

    try:
        # Replace with correct Multichain RPC credentials
        response = requests.post(
            RPC_URL,
            json=payload,
            headers=headers,
            timeout=5,
            auth=('multichainrpc', 'YOUR_RPC_PASSWORD')  
        )
        data = response.json()
        chain_data = data.get("result", [])
    except Exception as e:
        chain_data = [f"Error connecting to chain: {e}"]

    # Render a simple list
    html_list = "".join(f"<li>{item}</li>" for item in chain_data)
    return f"""
    <html>
    <head><title>Bridge Node Logs</title></head>
    <body>
      <h1>Bridge Node Logs</h1>
      <p>Below are raw items from the chain (via bridging node):</p>
      <ul>
        {html_list}
      </ul>
      <a href="/">Refresh</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)