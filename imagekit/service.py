import base64
import imghdr
import mimetypes
from typing import Optional

from fastapi import UploadFile, HTTPException
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from imagekitio import ImageKit

# SDK initialization (shared singleton or injected in reality)
imagekit = ImageKit(
    private_key="private_Mu3gJBmvHsU0sAN2AHW7OmHcBYY=",
    public_key="public_GXodnti2JP3WswBsHlzKIyCnkbA=",
    url_endpoint="https://ik.imagekit.io/owlit",
)


def build_file_name(filename: str, content: bytes) -> str:
    detected_ext = imghdr.what(None, h=content)
    file_name_value = filename or "upload"
    if detected_ext:
        ext_for_name = "jpg" if detected_ext == "jpeg" else detected_ext
        base = file_name_value.rsplit(".", 1)[0] if "." in file_name_value else file_name_value
        file_name_value = f"{base}.{ext_for_name}"
    return file_name_value

def get_mime_type(filename: str, content: bytes) -> str:
    detected_ext = imghdr.what(None, h=content)
    if detected_ext:
        mime_map = {
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
            "bmp": "image/bmp",
            "tiff": "image/tiff",
        }
        mime = mime_map.get(detected_ext)
        if mime:
            return mime
    guessed, _ = mimetypes.guess_type(filename or "")
    return guessed or "application/octet-stream"


def upload_image_service(
    file: UploadFile,
    folder: str = "/",
    use_unique_file_name: bool = True,
    is_private_file: bool = False,
    tags: Optional[str] = None,
):
    try:
        # Read file content (sync)
        content = file.file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        # Prepare ImageKit upload options
        options = UploadFileRequestOptions(
            folder=folder if folder else "/",
            use_unique_file_name=use_unique_file_name,
            is_private_file=is_private_file,
            tags=[t.strip() for t in tags.split(",")] if tags else None,
        )

        # Convert file to base64
        b64 = base64.b64encode(content).decode("utf-8")

        # Build proper filename
        file_name_value = build_file_name(file.filename, content)

        # Upload to ImageKit (sync SDK call)
        result = imagekit.upload_file(
            file=b64,
            file_name=file_name_value,
            options=options,
        )

        # Handle ImageKit errors
        if isinstance(result, dict) and result.get("error"):
            err = result["error"]
            status = err.get("status_code", 400) if isinstance(err, dict) else 400
            raise HTTPException(status_code=status, detail=err)

        # Normalize response
        resp = result.get("response", result) if isinstance(result, dict) else result

        # Private file → return signed URL
        if isinstance(resp, dict) and is_private_file:
            try:
                signed = imagekit.url({
                    "src": resp.get("url"),
                    "signed": True,
                    "expireSeconds": 300,
                })
                resp = {**resp, "signed_url": signed}
            except Exception:
                pass

        return resp

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")



def delete_image_service(file_id: str):
    try:
        res = imagekit.delete_file(file_id)
        if isinstance(res, dict) and res.get("error"):
            err = res["error"]
            status = 404 if getattr(err, "http_status_code", None) == 404 else 400
            raise HTTPException(status_code=status, detail=str(err))
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image deletion failed: {str(e)}")
