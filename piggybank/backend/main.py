from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os

import models
from database import engine
from api import router as api_router

# Create DB tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Piggybank API", description="API for TASCHENGELD Tracker")

# -------------------------------------------------------------
# HA INGRESS MIDDLEWARE
# -------------------------------------------------------------
# Home Assistant Supervisor forwards requests via Ingress.
# It sets the X-Ingress-Path header (e.g., /api/hassio_ingress/xyz123).
# We intercept this and strip it dynamically using middleware, so the Vue App 
# and FastAPI endpoints can use relative paths without breaking.

@app.middleware("http")
async def ingress_middleware(request: Request, call_next):
    ingress_path = request.headers.get("x-ingress-path", "")
    
    # FastAPIs root_path scope handles the prefixing for docs and routing dynamically if we inject it.
    if ingress_path:
        request.scope["root_path"] = ingress_path
        
    response = await call_next(request)
    return response

# Mount API
app.include_router(api_router, prefix="/api")

# -------------------------------------------------------------
# STATIC FRONTEND MOUNTING
# -------------------------------------------------------------
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Ensure static dir exists so FastAPI doesn't crash if frontend isn't built yet
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Provide a catch-all for Vue Router History mode, and serve index.html
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # Check if the requested file exists in the static dir (e.g., assets, js, css)
    file_path = os.path.join(STATIC_DIR, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Otherwise, return index.html for Vue Router to handle (SPA fallback)
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.isfile(index_path):
        # We read the index.html and inject a meta tag or window.dynamic_base variable
        # so Vue Router knows its base URL dynamically without hardcoding it at build.
        with open(index_path, "r") as f:
            html = f.read()
        return HTMLResponse(html)
    
    return HTMLResponse("<h1>Frontend not built yet.</h1><p>Run npm run build in frontend.</p>", status_code=404)
