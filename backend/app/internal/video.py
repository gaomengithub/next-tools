import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

video_path = os.path.abspath('.') +'//video//ahp.mp4'

router = APIRouter()


@router.get('/ahp_readme_video/')
async def ahp_readme_video():
    return FileResponse(video_path)
