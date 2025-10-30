from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from controller.app_controller import AppController
import uvicorn
import os

app = FastAPI(title="SmartApp IoT System")

templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

controller = AppController()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

# Speaker
@app.post("/toggle_speaker")
async def toggle_speaker(request: Request):
    _ = controller.toggle_speaker()
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

@app.post("/set_volume")
async def set_volume(request: Request, volume: int = Form(...)):
    controller.set_speaker_volume(volume)
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

# Light
@app.post("/toggle_light")
async def toggle_light(request: Request):
    _ = controller.toggle_light()
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

@app.post("/set_brightness")
async def set_brightness(request: Request, brightness: int = Form(...)):
    controller.set_light_brightness(brightness)
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

# Curtains
@app.post("/toggle_curtains")
async def toggle_curtains(request: Request):
    _ = controller.toggle_curtains()
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

@app.post("/set_curtains_position")
async def set_curtains_position(request: Request, position: int = Form(...)):
    controller.set_curtains_position(position)
    status = controller.get_all_status()
    return templates.TemplateResponse("index.html", {"request": request, "devices": status})

if __name__ == "__main__":
    host = os.getenv("UVICORN_HOST", "0.0.0.0")
    port = int(os.getenv("UVICORN_PORT", "8010"))
    uvicorn.run(app, host=host, port=port)
