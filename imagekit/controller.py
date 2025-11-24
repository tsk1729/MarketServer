from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, Query

from imagekit.service import upload_image_service, delete_image_service

imagekit_controller = APIRouter(tags=["ImageKit"])


@imagekit_controller.post("/image/upload")
def upload_image(
    file: UploadFile = File(..., description="Image file to upload"),
    folder: str = Form(default="/", description="Destination folder in ImageKit"),
    use_unique_file_name: bool = Form(default=True, description="Generate unique name at ImageKit"),
    is_private_file: bool = Form(default=False, description="Upload as private file"),
    tags: Optional[str] = Form(default=None, description="Comma separated tags"),
):
    """REST endpoint for testing and manual uploads. Delegates to service."""
    return  upload_image_service(
        file=file,
        folder=folder,
        use_unique_file_name=use_unique_file_name,
        is_private_file=is_private_file,
        tags=tags,
    )


@imagekit_controller.delete("/image/delete")
def delete_image(file_id: str = Query(..., description="file_id from upload response")):
    """REST endpoint for deleting image. Delegates to service."""
    return delete_image_service(file_id)
