from tkinter import *
from tkinter import ttk
import pyqrcode
import calendar
from translate import Translator
from datetime import datetime, timedelta


def update_clocks():
    # Обновление текущего времени
    current_time = datetime.now().strftime('%H:%M:%S')
    moscow_time_label.config(text=f"Московское время: {current_time}")
    current_time_label.config(text=f"Часы: {current_time[:2]} Минуты: {current_time[3:5]} Секунды: {current_time[6:]}")

    # Оставшееся время до нового дня
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=0, minute=0, second=0)
    time_until_midnight = midnight - datetime.now()
    left_time_label.config(text=f"Время до наступления нового дня: {time_until_midnight}")

    root.after(1000, update_clocks)


def show_calendar():
    year = int(year_entry.get())
    month = int(month_entry.get())
    cal = calendar.monthcalendar(year, month)
    calendar_text.delete(1.0, END)
    calendar_text.insert(END, calendar.month_name[month] + ' ' + str(year) + '\n\n')
    calendar_text.insert(END, 'MonTueWedThuFriSatSun\n')
    for week in cal:
        for day in week:
            if day == 0:
                calendar_text.insert(END, '   ')
            else:
                calendar_text.insert(END, f'{day:2} ')
        calendar_text.insert(END, '\n')


def calculate():
    expression = calc_entry.get()
    try:
        result = eval(expression)
        calc_result.config(text="Результат: " + str(result))
    except Exception as e:
        calc_result.config(text="Ошибка: " + str(e))


def translate():
    translator = Translator(from_lang=lan1.get(), to_lang=lan2.get())
    translation = translator.translate(var.get())
    var1.set(translation)


def generate_qr_code():
    qr_text = qr_entry.get()
    qr = pyqrcode.create(qr_text)
    qr_image = qr.xbm(scale=10)
    qr_code = BitmapImage(data=qr_image)
    qr_label.config(image=qr_code)
    qr_label.photo = qr_code


root = Tk()
root.title("Многофункциональный ассистент")
root.geometry('1024x512')
root.resizable(width=False, height=False)


# Создаем вкладки
tab_control = ttk.Notebook(root)

# Электронные часы

clock_tab = Frame(tab_control)
tab_control.add(clock_tab, text='Часы')

bg_w = PhotoImage(file="watch.png")
label1 = Label(clock_tab, image=bg_w)
label1.place(x=0, y=0)

moscow_time_frame = LabelFrame(clock_tab, text='Московское время', padx=10, pady=10)
moscow_time_frame.pack(padx=10, pady=10)
moscow_time_label = Label(moscow_time_frame, font=('Arial', 20))
moscow_time_label.pack()

current_time_frame = LabelFrame(clock_tab, text='Текущее время', padx=10, pady=10)
current_time_frame.pack(padx=10, pady=10)
current_time_label = Label(current_time_frame, font=('Arial', 20))
current_time_label.pack()

left_time_frame = LabelFrame(clock_tab, text='Время до наступления нового дня', padx=10, pady=10)
left_time_frame.pack(padx=10, pady=10)
left_time_label = Label(left_time_frame, font=('Arial', 20))
left_time_label.pack()

update_clocks()


# Календарь
calendar_tab = ttk.Frame(tab_control)
tab_control.add(calendar_tab, text='Календарь')

bg_k = PhotoImage(file="calendar.png")
label_c = Label(calendar_tab, image=bg_k)
label_c.place(x=0, y=0)

year_label = Label(calendar_tab, text='Введите год:', font='Arial 15')
year_label.pack(pady=20)
year_entry = Entry(calendar_tab, width=30)
year_entry.pack(pady=10)

month_label = Label(calendar_tab, text='Введите месяц (числом 1-12):', font='Arial 15')
month_label.pack(pady=10)
month_entry = Entry(calendar_tab)
month_entry.pack(pady=10)

show_calendar_button = Button(calendar_tab, text=' Показать \nкалендарь', font='Arial 15',
                              width=10, height=2, command=show_calendar)
show_calendar_button.pack(pady=10)

calendar_text = Text(calendar_tab, height=10, width=25)
calendar_text.pack(pady=20)


# Калькулятор

calculator_tab = Frame(tab_control, bg='#10FD5A')
tab_control.add(calculator_tab, text='Калькулятор')

bg_c = PhotoImage(file="calculator.png")
label_cal = Label(calculator_tab, image=bg_c)
label_cal.place(x=0, y=0)


calc_label = Label(calculator_tab, text="Введите выражение:")
calc_label.pack(pady=10)

calc_entry = Entry(calculator_tab)
calc_entry.pack(pady=10)

calc_button = Button(calculator_tab, text="Вычислить", command=calculate)
calc_button.pack(pady=10)

calc_result = Label(calculator_tab)
calc_result.pack(pady=10)


# Переводчик

mainframe = ttk.Frame(tab_control)
tab_control.add(mainframe, text='Переводчик')

bg_t = PhotoImage(file="translator.png")
label_tr = Label(mainframe, image=bg_t)
label_tr.place(x=0, y=0)

lan1 = StringVar(root)
lan2 = StringVar(root)

choices = {'English', 'Hindi', 'Gujarati', 'Spanish', 'German', 'Russian'}

lan1.set('Russian')
lan2.set('English')

lan1menu = OptionMenu(mainframe, lan1, *choices)
Label(mainframe, text="Выберите язык для ввода:", font='Arial 15').pack(pady=10)
lan1menu.pack()

lan2menu = OptionMenu(mainframe, lan2, *choices)
Label(mainframe, text="Выберите язык для перевода:", font='Arial 15').pack(pady=10)
lan2menu.pack()

Label(mainframe, text="Введите текст:", font='Arial 15').pack(pady=10)
var = StringVar()

textbox = ttk.Entry(mainframe, textvariable=var, width=30)
textbox.pack(pady=10)

b = Button(mainframe, text='Нажмите для перевода', command=translate, font='Arial 12', height=2)
b.pack(pady=10)

Label(mainframe, text="Ваш перевод:", font='Arial 15').pack(pady=10)
var1 = StringVar()

text_box = Entry(mainframe, textvariable=var1, width=30)
text_box.pack(pady=10)


# Создание QR-кода

qr_tab = Frame(tab_control, bg='#D7EA7D')
tab_control.add(qr_tab, text='QR-код')
qr_label = Label(qr_tab)
qr_label.pack(pady=20)
qr_entry = Entry(qr_tab)
qr_entry.pack(pady=10)
generate_button = Button(qr_tab, text="Создать QR-код", command=generate_qr_code)
generate_button.pack(pady=10)


tab_control.pack(expand=1, fill="both")


root.mainloop()
