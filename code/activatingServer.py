import subprocess
import time
import requests
import json
import urllib.request
import os

# 1. Kill any existing processes
!pkill -f uvicorn 2>/dev/null
!pkill -f ngrok 2>/dev/null
time.sleep(2)

# 2. Start uvicorn in the background
print("🚀 Starting FastAPI server...")
print("⏳ This will take 1-5 minutes because it's loading heavy AI models (TensorFlow, Sentence-BERT, spaCy)...")
print("⏳ Please be patient! Do not stop the cell.\n")

env = os.environ.copy()
env["PYTHONUNBUFFERED"] = "1"

server_process = subprocess.Popen(
    ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env
)

# 3. Poll the server until it's ready (up to 300 seconds / 5 minutes)
server_ready = False
for i in range(60): # 60 * 5 = 300 seconds
    time.sleep(5)
    
    # Check if process died
    if server_process.poll() is not None:
        print("\n❌ Server crashed on startup!")
        stdout, stderr = server_process.communicate()
        print("STDOUT:", stdout.decode() if stdout else "None")
        print("STDERR:", stderr.decode() if stderr else "None")
        break
        
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=2)
        if response.status_code == 200:
            print(f"\n✅ Server is ready! (Took {i*5} seconds to load models)")
            server_ready = True
            break
    except requests.exceptions.ConnectionError:
        print(f"⏳ Still loading models... ({i*5}s)")
        
if not server_ready and server_process.poll() is None:
    print("\n⚠️ Server is still loading after 5 minutes! It's still running in the background.")
    print("Starting ngrok anyway. It might show a 502 error for a few minutes until the server finishes loading.")
    server_ready = True # Force ngrok to start

if server_ready:
    # 4. Start ngrok
    print("\n🌐 Starting ngrok tunnel...")
    
    # 🔴 REPLACE THIS WITH YOUR ACTUAL NGROK TOKEN 🔴
    !ngrok config add-authtoken *********************** 2>/dev/null
    
    # Start ngrok process in background
    ngrok_process = subprocess.Popen(
        ['ngrok', 'http', '8000'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)
    
    # Get the public URL from ngrok API
    try:
        with urllib.request.urlopen('http://localhost:4040/api/tunnels') as response:
            data = json.loads(response.read().decode())
            public_url = data['tunnels'][0]['public_url']
            print(f"\n🎉 SUCCESS! Your app is live at:")
            print(f"👉 {public_url}")
            print("\nClick the link above to open PathFinder AI!")
            print("(If you see a 502 Bad Gateway, just wait 1-2 minutes and refresh. The AI models are still loading!)")
    except Exception as e:
        print(f"⚠️ Ngrok started but couldn't fetch URL automatically. Error: {e}")
