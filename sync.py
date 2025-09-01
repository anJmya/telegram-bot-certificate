from datetime import datetime, timedelta

class Sync:
    def __init__(self, sheets):
        self.sheets = sheets
        self.start_sync_row = 2597 
    
    def sync(self):
        # Получаем данные, начиная с определенной строки
        source_data, target_data = self.sheets.get_data(start_row=self.start_sync_row)
        
        # Существующие записи  
        existing = {f"{r['name'].lower()}-{r['course'].lower()}" for r in target_data}
        
        # Период прохождения
        today = datetime.now()
        monday = today - timedelta(days=today.weekday() + 7)
        friday = monday + timedelta(days=4)
        
        # Форматируем даты
        start_date = monday.strftime('%d.%m.%Y')  
        end_date = friday.strftime('%d.%m.%Y')    
        period_text = f"с {start_date} по {end_date}"  
        
        # Next cert number
        max_num = 1548  # Start with this nubmer(Этот номер был последним до введения бота)
        for r in target_data:
            try:
                num = int(r['num'].replace('№', '') or 0)
                max_num = max(max_num, num)
            except ValueError:
                continue
        
        # Новые записи
        new_records = []
        for s in source_data:
            key = f"{s['name'].lower()}-{s['course'].lower()}"
            if key not in existing and s['name'].strip() and s['course'].strip():
                max_num += 1
                new_records.append([
                    f"№{max_num}",      
                    today.strftime('%d.%m.%Y'),  
                    s['name'],
                    '',
                    s['phone'],
                    s['course'],                
                    start_date,
                    end_date,
                    period_text,
                    '', '', ''
                ])
        
        if new_records:
            self.sheets.add_records(new_records)
        
        return len(new_records), [r[2] for r in new_records]
