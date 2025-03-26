from flask import Flask, render_template
import requests

app = Flask(__name__)

# Replace with your Multichain node's actual RPC credentials and URL
RPC_USER = 'multichainrpc'
RPC_PASSWORD = 'password'
RPC_PORT = '8000'
RPC_HOST = 'multichain_node'  # this should match the service name in docker-compose
RPC_URL = f'http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}'

def get_logs():
    payload = {
        "method": "liststreamitems",
        "params": ["data"],
        "id": 1,
        "jsonrpc": "2.0"
    }
    try:
        response = requests.post(RPC_URL, json=payload)
        response.raise_for_status()
        return response.json().get("result", [])
    except Exception as e:
        return [{"key": "error", "data": str(e)}]

@app.route("/")
def index():
    logs = get_logs()
    return render_template("index.html", logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)