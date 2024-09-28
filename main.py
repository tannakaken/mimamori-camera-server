from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import os
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

app = FastAPI()


dir_path = "images"
JST = timezone(timedelta(hours=+9), 'JST')


@app.get("/")
def read_root() -> FileResponse:
    p = Path(dir_path)
    files = list(p.glob("*"))
    file_updates = {file_path: os.stat(file_path).st_mtime for file_path in files}

    newest_file_path = max(file_updates, key=file_updates.get)

    return FileResponse(newest_file_path)


@app.post("/")
async def read_item(upload_file: UploadFile):
    """最大でも１秒に一回のリクエストしかさばかない。
    """
    now = datetime.now(JST)
    filename = now.strftime('%Y%m%dT%H%M%S.jpg')
    fullpath = f"{dir_path}/{filename}"
    with open(fullpath, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return {"ok": True}
