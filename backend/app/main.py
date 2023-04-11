import uvicorn
from fastapi import FastAPI
from app.internal import auth, video
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ahp, fce, dir, mark, set, websocket ,cnki ,citation

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["file_name", "file_type", 'filename'],
)

app.include_router(auth.router, prefix='/tools-next/api')
app.include_router(ahp.router, prefix='/tools-next/api')
app.include_router(fce.router, prefix='/tools-next/api')
app.include_router(dir.router, prefix='/tools-next/api')
app.include_router(mark.router, prefix='/tools-next/api')
app.include_router(set.router, prefix='/tools-next/api')
app.include_router(websocket.router, prefix='/tools-next/api')
app.include_router(video.router, prefix='/tools-next/api')
app.include_router(cnki.router,prefix='/tools-next/api')
app.include_router(citation.router,prefix='/tools-next/api')

if __name__ == "__main__":
    # uvicorn.run(app="app.main:app", host="192.168.31.59", port=8000, reload=True, debug=True)
    # uvicorn.run(app="app.main:app", host="10.1.58.187", port=8000, workers=4)
    uvicorn.run(app="app.main:app", host="localhost", port=8000, reload=True, debug=True)

# uvicorn app.main:app --host '10.10.10.66' --port 8000 --workers 4 --reload
# uvicorn app.main:app --host '124.221.93.232' --port 8000
# uvicorn app.main:app --host '192.168.31.57' --port 8000
# uvicorn app.main:app --host '192.168.50.9' --port 8000 --reload --workers 4
# daphne app.main:app -b 10.0.16.6 -p 8000
# daphne app.main:app -b 192.168.50.9 -p 8000
# uvicorn app.main:app --host '172.20.10.2' --port 8000 --reload
