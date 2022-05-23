import gspread
from django.conf import settings


class SheetClient:

    def __init__(self):
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        self.client = gspread.service_account_from_dict(settings.GOOGLE_SHEETS_CREDENTIALS, scope)

    def get_values(self, spread_sheet_name, sheet_name):
        spread = self.client.open(spread_sheet_name)
        worksheet = spread.worksheet(sheet_name)
        list_of_lists = worksheet.get_all_values()
        return list_of_lists
