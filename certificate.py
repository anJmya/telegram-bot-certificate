from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os

# путь до пнг и шрифтов
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCES_PATH = os.path.join(BASE_PATH, 'resources')
FONTS_PATH = os.path.join(RESOURCES_PATH, 'fonts')
IMAGES_PATH = os.path.join(RESOURCES_PATH, 'img')

# регистрация шрифтов
try:
    pdfmetrics.registerFont(TTFont('Montserrat-Regular', os.path.join(FONTS_PATH, 'Montserrat-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('Montserrat-Bold', os.path.join(FONTS_PATH, 'Montserrat-Bold.ttf')))
    print("Шрифты Montserrat успешно зарегистрированы.")
except Exception as e:
    print(f"Ошибка при регистрации шрифтов: {e}. Убедитесь, что файлы шрифтов находятся в папке resources/fonts/")
    print(f"Ожидаемый путь к шрифтам: {FONTS_PATH}")


class Certificate: 
    def generate(self, name, course, period, cert_num):
        # Генерация PDF
        try:
            print(f"Начинаю генерацию PDF для {name}")
            
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=landscape(A4))
            w, h = landscape(A4)
            
            # Рамки
            from reportlab.lib.colors import Color

            start_color = Color(80/255, 146/255, 169/255)  #5092A9
            end_color = Color(143/255, 234/255, 212/255)   #8FEAD4
            
            # Внешняя рамка с градиентом 
            gradient_steps = 50  
            for i in range(gradient_steps):
                ratio = i / gradient_steps
                r = start_color.red + (end_color.red - start_color.red) * ratio
                g = start_color.green + (end_color.green - start_color.green) * ratio
                b = start_color.blue + (end_color.blue - start_color.blue) * ratio
                
                current_color = Color(r, g, b)
                c.setStrokeColor(current_color)
                c.setLineWidth(0.4)  # толщина линии 
                
                # смещаем каждую линию на толщину предидущей
                offset = i * 0.4
                c.rect(40 + offset, 40 + offset, w-80 - 2*offset, h-80 - 2*offset, fill=0)
            

            
            # Лого Школы
            try:
                logo_path = os.path.join(IMAGES_PATH, 'logo.png')
                if os.path.exists(logo_path):
                    c.drawImage(logo_path, 100, h-120, width=40, height=40, mask='auto')
                    c.setFont("Montserrat-Bold", 16)
                    c.drawString(150, h-105, "Figurin's school")
                else:
                    print("Логотип школы не найден в resources/img/")
                    c.setFont("Montserrat-Bold", 16)
                    c.drawString(100, h-150, "Figurin's school")
            except Exception as e:
                print(f"Ошибка при добавлении логотипа школы: {e}")
                c.setFont("Montserrat-Bold", 16)
                c.drawString(100, h-100, "Figurin's school")
            
            # лого ПСБ
            try:
                psb_logo_path = os.path.join(IMAGES_PATH, 'psb.png')
                if os.path.exists(psb_logo_path):
                    c.drawImage(psb_logo_path, w-250, h-105, width=170, height=30, mask='auto')
                    c.setFont("Montserrat-Regular", 12)
                    c.drawRightString(w-100, h-130, f"{cert_num} от {datetime.now().strftime('%d.%m.%Y')}")
                else:
                    print("Логотип ИПБ не найден в resources/img/")
                    c.setFont("Montserrat-Regular", 12)
                    c.drawRightString(w-100, h-100, f"{cert_num} от {datetime.now().strftime('%d.%m.%Y')}")
            except Exception as e:
                print(f"Ошибка при добавлении логотипа ИПБ: {e}")
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
            
            # Текст с квалификацией (разбит на несколько строк)
            c.setFont("Montserrat-Regular", 10)
            c.drawString(100, 140, "Профессиональный")
            c.drawString(100, 128, "Бухгалтер РК")
            c.drawString(100, 116, "Налоговый консультант РК")
            
            c.drawRightString(w-100, 130, "Фигурина Н.Э")
            
            # stamp and sign stack together
            signature_center_x = w/2
            
            # Подпись
            try:
                sign_path = os.path.join(IMAGES_PATH, 'sign.png')
                if os.path.exists(sign_path):
                    c.drawImage(sign_path, signature_center_x-50, 100, width=100, height=50, preserveAspectRatio=True, mask='auto')
                    print("Подпись добавлена")
                else:
                    print("Файл подписи не найден в resources/img/")
            except Exception as e:
                print(f"Ошибка при добавлении подписи: {e}")
            
            # Печать
            try:
                stamp_path = os.path.join(IMAGES_PATH, 'stamp.png')
                if os.path.exists(stamp_path):
                    # Размещаем печать чуть правее и выше подписи
                    c.drawImage(stamp_path, signature_center_x+20, 110, width=90, height=90, preserveAspectRatio=True, mask='auto')
                    print("Печать добавлена")
                else:
                    print("Файл печати не найден в resources/img/, используется стандартный круг")
                    # Если файл печати не найден, рисуем стандартный круг
                    c.circle(signature_center_x+55, 185, 35, fill=0)
                    c.setFont("Montserrat-Regular", 8)
                    c.drawCentredString(signature_center_x+55, 190, "Figurin's")
                    c.drawCentredString(signature_center_x+55, 180, "School")
            except Exception as e:
                print(f"Ошибка при добавлении печати: {e}")
                # В случае ошибки рисуем стандартный круг
                c.circle(signature_center_x+55, 185, 35, fill=0)
                c.setFont("Montserrat-Regular", 8)
                c.drawCentredString(signature_center_x+55, 190, "Figurin's")
                c.drawCentredString(signature_center_x+55, 180, "School")
            
            c.save()
            buffer.seek(0)
            
            print(f"PDF успешно сгенерирован для {name}")
            return buffer
            
        except Exception as e:
            print(f"Ошибка в генерации PDF: {e}")
            import traceback
            traceback.print_exc()
            raise