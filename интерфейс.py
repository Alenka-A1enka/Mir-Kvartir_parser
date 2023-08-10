import PySimpleGUI as sg
import parser_mirkv
import tkinter.messagebox as mb

layout = [
    [sg.Text('Выберите ценовой диапазон: ')
    ],
    [sg.Text('От'), sg.InputText()
     ],
    [sg.Text('До'), sg.InputText()
     ],
    [
      sg.Checkbox('Однокомнатные'), sg.Checkbox('Двухкомнатные'), sg.Checkbox('Трехкомнатные')
    ],
    [
        sg.Submit('Применить')
    ],
    [sg.Output(size=(88, 20))],
    [sg.Submit('Записать данные в файл')],
]
window = sg.Window('Парсинг сайта Мир квартир', layout)
parser = parser_mirkv.Parser()

while True:                             
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if event == 'Применить':
        parser.parsing_mir_kvartir(price_from=values[0], price_to=values[1], one_room = values[2], 
                                   two_room = values[3], third_room = values[4])
        print(parser.get_last_data())
        
    if event == 'Записать данные в файл':
        parser.write_dct_to_docx()
        mb.showinfo("Информация", 'Данные записаны в файл')
        
