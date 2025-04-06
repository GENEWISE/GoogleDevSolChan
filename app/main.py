import os
import subprocess
import sys
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_route import router as auth_router
from routes.doctor_route import router as doctor_router
from routes.access_route import router as access_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(doctor_router, prefix="/doctor", tags=["Doctors"])
app.include_router(access_router, prefix="/access", tags=["Access Requests"])

react_build_path = os.path.join(os.path.dirname(__file__), "..", "FrontEnd", "dist")

assets_path = os.path.join(react_build_path, "assets")
if not os.path.exists(assets_path):
    raise RuntimeError(f"⚠️ React build not found at {assets_path}. Run 'npm run build' in the FrontEnd folder.")

app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

@app.get("/")
def serve_react():
    index_path = os.path.join(react_build_path, "index.html")
    return FileResponse(index_path)

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    index_path = os.path.join(react_build_path, "index.html")
    return FileResponse(index_path)

def run_streamlit_app(script_name, port):
    script_path = os.path.join(os.path.dirname(__file__), "streamlit", script_name)
    if not os.path.exists(script_path):
        print(f"Streamlit script {script_path} not found!")
        return
    command = [
        sys.executable, "-m", "streamlit", "run", script_path,
        "--server.port", str(port),
        "--server.headless", "true"
    ]
    try:
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Started Streamlit app: {script_name} on port {port}")
    except Exception as e:
        print(f"Failed to start {script_name}: {e}")

run_streamlit_app("chat.py", 8501)
run_streamlit_app("classify.py", 8502)
run_streamlit_app("geneseq.py", 8503)
run_streamlit_app("protein.py", 8504)
