import os.path

from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from src.googleDrive_conf import get_cred



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

class File_cl:
    @classmethod
    def load_file(cls, file_path):
        try:
            service = get_cred()
            # Call the Drive v3 API
            id_folder = "1iNrAuUoXkAHPYN_ZbWqojC-4tHDuBSKT"
            file_metadata = {"name": os.path.basename(file_path), "parents": [id_folder]}
            media = MediaFileUpload(file_path, resumable=True)
            file_l = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return {"message": "Файл успешно загружен на Google Диск", "file_id": file_l.get('id')}

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f"An error occurred: {error}")

