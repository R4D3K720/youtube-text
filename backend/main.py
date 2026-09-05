from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

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
        response = requests.get(
            "https://api.freetranscriptapi.com/v1/transcript",
            params={"video_url": video.url},
            timeout=30
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"FreeTranscriptAPI: {response.text}"
            )

        data = response.json()

        transcript = "\n".join(
            item["text"]
            for item in data["transcript"]
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