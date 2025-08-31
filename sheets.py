import gspread
import json
import base64
from google.oauth2.service_account import Credentials
from fuzzywuzzy import fuzz
from config import GOOGLE_CREDS, SOURCE_SHEET_ID, TARGET_SHEET_ID

class Sheets:
    def __init__(self):
        creds = json.loads(base64.b64decode(GOOGLE_CREDS).decode())
        credentials = Credentials.from_service_account_info(
            creds, scopes=['https://spreadsheets.google.com/feeds',
                          'https://www.googleapis.com/auth/drive']
        )
        self.client = gspread.authorize(credentials)
    
    def get_data(self):
        """Получить данные из таблиц"""
        source = self.client.open_by_key(SOURCE_SHEET_ID).sheet1.get('B:E')
        target = self.client.open_by_key(TARGET_SHEET_ID).sheet1.get_all_values()
        
        # Преобразуем в словари
        source_data = []
        if len(source) > 1:
            for row in source[1:]:
                if len(row) >= 4 and row[0].strip():
                    source_data.append({
                        'name': row[0], 'email': row[1], 
                        'phone': row[2], 'course': row[3]
                    })
        
        target_data = []
        if len(target) > 1:
            for row in target[1:]:
                while len(row) < 12: row.append('')
                if row[2].strip():  # Если есть ФИО
                    target_data.append({
                        'num': row[0], 'date': row[1], 'name': row[2], 
                        'phone': row[3], 'course': row[4], 'period': row[7]
                    })
        
        return source_data, target_data
    
    def search_student(self, query):
        """Поиск студента"""
        _, target_data = self.get_data()
        matches = []
        
        for record in target_data:
            score = fuzz.token_set_ratio(query.lower(), record['name'].lower())
            if score >= 70:
                record['score'] = score
                matches.append(record)
        
        return sorted(matches, key=lambda x: x['score'], reverse=True)
    
    def add_records(self, records):
        """Добавить записи"""
        if records:
            sheet = self.client.open_by_key(TARGET_SHEET_ID).sheet1
            sheet.append_rows(records)