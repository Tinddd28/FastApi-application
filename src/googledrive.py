import os.path

from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from src.googleDrive_conf import get_cred
from config.config import folder_id


class File_cl:
    @classmethod
    def load_file(cls, file_path):
        try:
            service = get_cred()
            # Call the Drive v3 API
            id_folder = folder_id
            file_metadata = {"name": os.path.basename(file_path), "parents": [id_folder]}
            media = MediaFileUpload(file_path, resumable=True)
            file_l = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            file_id = file_l.get("id")
            file_url = f"https://drive.google.com/file/d/{file_id}/view"
            print(file_url)

            return {"file_id": file_id, "file_url": file_url}

            #return {"message": "Файл успешно загружен на Google Диск", "file_id": file_l.get("id")}

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f"An error occurred: {error}")

