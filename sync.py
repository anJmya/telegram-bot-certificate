from datetime import datetime, timedelta

class Sync: 
    def __init__(self, sheets):
        self.sheets = sheets

    def sync(self):
        """Синхронизация таблиц"""
        source_data, target_data = self.sheets.get_data()

        existing = {f"{r['name'].lower()}-{r['course'].lower()}" for r in target_data}

        # Даты
        today = datetime.now()
        last_monday = today - timedelta(days=today.weekday() + 7)
        last_friday = last_monday + timedelta(days=4) 
        period = f"с {last_monday.strftime('%d.%m.%Y')} по {last_friday.strftime('%d.%m.%Y')}"

        # Next cert Number
        max_num = max([int(r['num'].replace('№', '') or 0) for r in target_data] + [0])

        # New records
        new_records = []
        for s in source_data: 
            key = f"{s['name'].lower()}-{s['course'].lower()}"
            if key not in existing: 
                max_num += 1 
                new_records.append([
                    f"№{max_num}", today.strftime('%d.%m.%Y'), s['name'], s['phone'], 
                    s['course'], last_monday.strftime('%d.%m.%Y'), last_friday.strftime('%d.%m.%Y'),
                    period, '', '', '', ''
                ])

            if new_records: 
                self.sheets.add_records(new_records)

            return len(new_records), [r[2] for r in new_records]
