from datetime import datetime, timedelta

class Sync: 
    def __init__(self, sheets):
        self.sheets = sheets
    
    def sync(self):
        """Синхронизация"""
        source_data, target_data = self.sheets.get_data()
        
        # Существующие записи
        existing = {f"{r['name'].lower()}-{r['course'].lower()}" for r in target_data}
        
        # Период прохождения (предыдущая неделя)
        today = datetime.now()
        monday = today - timedelta(days=today.weekday() + 7)
        friday = monday + timedelta(days=4)
        
        # Форматируем даты
        start_date = monday.strftime('%d.%m.%Y')  # Столбец G
        end_date = friday.strftime('%d.%m.%Y')    # Столбец H
        period_text = f"с {start_date} по {end_date}"  # Столбец I


        # Next cert Number
        max_num = 1548
        for r in target_data:
            try:
                num = int(r['num'].replace('№', '') or 0)
                max_num = max(max_num, num)
            except ValueError:
                continue


        # New records
        new_records = []
        for s in source_data:
            key = f"{s['name'].lower()}-{s['course'].lower()}"
            if key not in existing and s['name'].strip() and s['course'].strip():
                max_num += 1
                new_records.append([
                    f"№{max_num}",      
                    today.strftime('%d.%m.%Y'),  
                    s['name'],          
                    s['phone'],         
                    s['course'],        
                    '',                 
                    start_date,         
                    end_date,           
                    period_text,        
                    '', '', ''          
                ])


            if new_records: 
                self.sheets.add_records(new_records)

            return len(new_records), [r[2] for r in new_records]
