import os

from googleapiclient.errors import HttpError

from config.spreadsheetId import st
from src.table_conf import get_sheet
from src.models import user

SPREADSHEET_ID = st


class User:
    @classmethod
    async def add_user(cls, data: user.UserAdd) -> int:
        try:
            service = get_sheet()
            
            user_dict = data.model_dump()

            # Call the Sheets API
            sheets = service.spreadsheets()
            range="Sheet1!A:F"

            result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute()

            values = result.get("values", [])
            count = 0
            if len(values) == 1:
                count = 1
            else:
                last = values[len(values) - 1][0]
                count = int(last) + 1
            range = "Sheet1"
            list = [[count], [user_dict["fio"]], [user_dict["topic"]], [user_dict["num"]], [user_dict["director"]], [user_dict["user_id"]]]
            resource = {
                "majorDimension": "COLUMNS",
                "values": list
            }

            sheets.values().append(spreadsheetId=SPREADSHEET_ID, range=range, body=resource, valueInputOption="USER_ENTERED").execute()


            return user_dict["user_id"]

        except HttpError as error:
            print(error)



    async def get_requests(id: str) -> list:
        try:
            service = get_sheet()
            sheets = service.spreadsheets()
            range="Sheet1!A:F"
            result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute()

            values = result.get("values", [])
            a = []
            for row in values:
                if row:
                    if row[5] == id:
                        x = {"count": row[0], "fio": row[1], "topic": row[2], "num": row[3], "director": row[4], "user_id": row[5] }
                        a.append(x)

            return a
        except HttpError as error:
            print(error)

