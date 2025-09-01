from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

FONT_PATH = os.path.dirname(os.path.abspath(__file__))

try:
    pdfmetrics.registerFont(TTFont('Montserrat-Regular', os.path.join(FONT_PATH, 'Montserrat-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('Montserrat-Bold', os.path.join(FONT_PATH, 'Montserrat-Bold.ttf')))
    print("Шрифты Montserrat успешно зарегистрированы.")
except Exception as e:
    print(f"Ошибка при регистрации шрифтов: {e}. Убедитесь, что файлы шрифтов находятся в папке со скриптом.")


class Certificate: 
    def generate(self, name, course, period, cert_num):
        # Генерация PDF
        try:
            print(f"Начинаю генерацию PDF для {name}")
            
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=landscape(A4))
            w, h = landscape(A4)
            
            # Рамки
            c.setLineWidth(2)
            c.rect(40, 40, w-80, h-80)
            c.rect(60, 60, w-120, h-120)
            
            # Шапка
            c.setFont("Montserrat-Bold", 16)
            c.drawString(100, h-100, "Figurin's school")
            c.setFont("Montserrat-Regular", 12)
            c.drawRightString(w-100, h-100, f"{cert_num} от {datetime.now().strftime('%d.%m.%Y')}")
            
            # Основной текст
            c.setFont("Montserrat-Bold", 42)
            c.drawCentredString(w/2, h-170, "Сертификат")
            
            c.setFont("Montserrat-Regular", 16)
            c.drawCentredString(w/2, h-210, "Подтверждает, что")
            
            c.setFont("Montserrat-Bold", 26)
            c.drawCentredString(w/2, h-260, str(name))
            
            c.setFont("Montserrat-Regular", 16)
            c.drawCentredString(w/2, h-300, "прослушал(-а) курс")
            
            c.setFont("Montserrat-Bold", 18)
            c.drawCentredString(w/2, h-330, f'"{str(course)}"')
            
            c.setFont("Montserrat-Regular", 14)
            c.drawCentredString(w/2, h-360, "в количестве 10 часов")
            c.drawCentredString(w/2, h-380, str(period))
            
            # Подпись и печать
            c.setFont("Montserrat-Regular", 10)
            c.drawString(100, 120, "Профессиональный\nБухгалтер РК, Налоговый\nКонсультант РК")
            c.drawRightString(w-100, 130, "Фигурина Н.Э")
            
            c.circle(w/2, 150, 35, fill=0)
            c.setFont("Montserrat-Regular", 8)
            c.drawCentredString(w/2, 155, "Figurin's")
            c.drawCentredString(w/2, 145, "School")
            
            c.save()
            buffer.seek(0)
            
            print(f"PDF успешно сгенерирован для {name}")
            return buffer
            
        except Exception as e:
            print(f"Ошибка в генерации PDF: {e}")
            import traceback
            traceback.print_exc()
            raise
