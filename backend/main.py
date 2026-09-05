from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import urllib.request
import urllib.parse
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://r4d3k720.github.io"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {"status": "TubeScript backend działa!"}


@app.post("/transcribe")
def transcribe(video: VideoRequest):

    try:
        encoded_url = urllib.parse.quote(video.url, safe="")

        api_url = (
            "https://api.freetranscriptapi.com/v1/transcript"
            f"?video_url={encoded_url}"
        )

        with urllib.request.urlopen(api_url, timeout=30) as response:
            data = json.loads(response.read().decode())

        transcript_data = data.get("transcript")

        if not transcript_data:
            raise HTTPException(
                status_code=404,
                detail="Nie znaleziono transkrypcji dla tego filmu."
            )

        # API zwraca fragmenty tekstu, więc łączymy je
        # w jeden normalny tekst.
        transcript = "\n".join(
            item["text"] for item in transcript_data
            if item.get("text")
        )

        return {
            "title": data.get("title"),
            "language": data.get("language"),
            "transcript": transcript
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Nie udało się pobrać transkrypcji: {str(e)}"
        )