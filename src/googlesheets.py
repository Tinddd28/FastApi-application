import os

from googleapiclient.errors import HttpError

from config.spreadsheetId import st
from src.table_conf import get_sheet
from src.models import request

SPREADSHEET_ID = st


class google_sheets:
    @classmethod
    async def add_request(cls, data: request.RequestAdd) -> int:
        try:
            service = get_sheet()
            
            user_dict = data.model_dump()

            # Call the Sheets API
            sheets = service.spreadsheets()
            range_="Sheet1!A:F"

            result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=range_).execute()

            values = result.get("values", [])
            count = 0
            if len(values) == 1:
                count = 1
            else:
                last = values[len(values) - 1][0]
                count = int(last) + 1
            range_ = "Sheet1"
            list = [[count], [user_dict["fio"]], [user_dict["topic"]], [user_dict["num"]], [user_dict["director"]], [user_dict["user_id"]]]
            resource = {
                "majorDimension": "COLUMNS",
                "values": list
            }

            sheets.values().append(spreadsheetId=SPREADSHEET_ID, range=range_, body=resource, valueInputOption="USER_ENTERED").execute()


            return user_dict["user_id"]

        except HttpError as error:
            print(error)


    @classmethod
    async def get_requests(cls, id: int) -> list:
        try:
            #service = get_sheet()
            sheets = get_sheet().spreadsheets()
            range_="Sheet1!A:F"
            result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=range_).execute()

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
    @classmethod
    async def add_link(cls, id: int, url:str):
        try:
            sheets = get_sheet().spreadsheets()
            range_ = f"Sheet1!G{id + 1}"
            value_input_option = "RAW"
            values = [[url]]
            body = {"values": values}
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=range_,valueInputOption=value_input_option, body=body).execute()

            return {"id": id, "url": url}
        except HttpError as error:
            print(error)

    @classmethod
    async def check_id_and_link(cls, id: int):
        try:
            sheets = get_sheet().spreadsheets()
            range_ = "Sheet1!A:G"
            result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=range_).execute()

            values = result.get("values", [])

            if len(values) - 1 < id: 
                return {"state": -1}
            
            flag = 0                                          # Блок проверки для пустого поля, чтобы не добавлялась ссылкка для несуществующего id

            for row in values:
                if row:
                    if row[0] == str(id):
                        flag = 1
                        break

            if flag:
                for row in values:
                    if len(row) == 6:
                        return {"state": 0}
                    return {"state": 1}
            else: 
                return {"state": -1}
                    
        except HttpError as error:
            print(error)
