from fastapi import FastAPI, Query
from fastapi.responses import Response, HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template
import base64
import uvicorn
from simulation import draw_knitting_pattern
from stitch import Stitch


app = FastAPI()

# Mount static files (if needed later)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load HTML template for the homepage
with open("templates/index.html", "r") as f:
    template = Template(f.read())

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main HTML page."""
    return template.render()

@app.get("/simulate")
async def simulate(
    rows: int = Query(30, ge=10, le=50), 
    columns: int = Query(30, ge=15, le=60),
    time: int = Query(None)  # Forces a unique request to prevent caching
):
    """Returns the knitting pattern as a PNG image."""
    print(f"DEBUG: Received request with rows={rows}, columns={columns}, time={time}")  # Log every request

    try:
        img_data = draw_knitting_pattern(rows, columns)

        if not img_data or len(img_data) < 50:
            print("ERROR: Invalid image data!")
            return Response(content="ERROR: Image generation failed", media_type="text/plain")

        img_bytes = base64.b64decode(img_data)
        print(f"DEBUG: Successfully decoded image, size={len(img_bytes)} bytes")  # Log valid images
        return Response(content=img_bytes, media_type="image/png")

    except Exception as e:
        print(f"ERROR: FastAPI crashed: {e}")
        return Response(content="ERROR: Server issue", media_type="text/plain")

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
