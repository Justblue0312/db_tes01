import uvicorn
from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from config import create_app

app = create_app()


# Test route
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, tags=["Index"])
async def index(request: Request):
    """
    Home page

    Args:
        request (Request): Request object

    Returns:
        HTMLResponse: HTML response
    """
    return templates.TemplateResponse("index.html", context={"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
