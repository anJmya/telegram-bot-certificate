from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas

class Certificate: 
    def generate(self, name, course, period, cert_num):
        # Генерация PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=landscape(A4))
        w, h = landscape(A4)

        # Рамка
        c.setLineWidth(2)
        c.rect(40, 40, w-80, h-80)
        c.rect(60, 60, w-120, h-120)

        # Лого, имя, дата выдачи и номер
        c.setFont("Times-Bold", 16)
        c.drawString(100, h-100, "Figurin's school")
        c.setFont("Times-Roman", 12)
        c.drawRightString(w-100, h-100, f"{cert_num} от {datetime.now().strftime('%d.%m.%Y')}")

        # Текст
        c.setFont("Times-Bold", 42)
        c.drawCentredText(w/2, h-170, "Сертификат")
        
        c.setFont("Times-Roman", 16)
        c.drawCentredText(w/2, h-210, "Подтверждает, что")
        
        c.setFont("Times-Bold", 26)
        c.drawCentredText(w/2, h-260, name)
        
        c.setFont("Times-Roman", 16)
        c.drawCentredText(w/2, h-300, "прослушал(-а) курс")
        
        c.setFont("Times-Bold", 18)
        c.drawCentredText(w/2, h-330, f'"{course}"')
        
        c.setFont("Times-Roman", 14)
        c.drawCentredText(w/2, h-360, "в количестве 10 часов")
        c.drawCentredText(w/2, h-380, period)
        
        # Подпись и печать
        c.setFont("Times-Roman", 10)
        c.drawString(100, 120, "Профессиональный\nБухгалтер РК, Налоговый\nКонсультант РК")
        c.drawRightString(w-100, 130, "Фигурина Н.Э")
        
        c.circle(w/2, 150, 35, fill=0)
        c.setFont("Times-Roman", 8)
        c.drawCentredText(w/2, 155, "Figurin's")
        c.drawCentredText(w/2, 145, "School")

        c.save()
        buffer.seek(0)
        
        return buffer
