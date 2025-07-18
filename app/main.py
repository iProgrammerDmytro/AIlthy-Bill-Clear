from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.bill.router import router as bill_router
from app.contact.router import router as contact_router
from app.core.config import get_settings

settings = get_settings()


app = FastAPI(title=settings.project_name)

# Static + templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def home(request: Request):
    """
    Serve the one-page MVP UI.
    """
    return templates.TemplateResponse("index.html", {"request": request})


# API routes
app.include_router(bill_router, prefix=settings.api_prefix)
app.include_router(contact_router, prefix=settings.api_prefix)
