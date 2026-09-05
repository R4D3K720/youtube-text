from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


app = FastAPI()


# Pozwala frontendowi komunikować się z backendem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoRequest(BaseModel):
    url: str


def get_video_id(url: str):

    parsed = urlparse(url)

    # youtube.com/watch?v=XXXX
    if "youtube.com" in parsed.netloc:

        query = parse_qs(parsed.query)

        if "v" in query:
            return query["v"][0]

    # youtu.be/XXXX
    if "youtu.be" in parsed.netloc:

        return parsed.path.strip("/")

    return None


@app.get("/")
def home():

    return {
        "status": "TubeScript backend działa!"
    }


@app.post("/transcribe")
def transcribe(video: VideoRequest):

    video_id = get_video_id(video.url)

    if not video_id:

        raise HTTPException(
            status_code=400,
            detail="Nieprawidłowy link YouTube."
        )

    try:

        api = YouTubeTranscriptApi()

        fetched = api.fetch(video_id)

        transcript = "\n".join(
            snippet.text
            for snippet in fetched
        )

        return {
            "video_id": video_id,
            "transcript": transcript
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Nie udało się pobrać transkrypcji: {str(e)}"
        )