import csv
import PySimpleGUI as sg
trimestre = -1
P200_2 = [0, 0, 0, 0]
P200_4 = [0, 0, 0, 0]
P200_6 = [0, 0, 0, 0]
P200_8 = [0, 0, 0, 0]
P200_9 = [0, 0, 0, 0]
P300_16 = [0, 0, 0, 0]
totalP200 = [0, 0, 0, 0]
P150_301010101 = [0, 0, 0, 0]
P150_30101010201 = [0, 0, 0, 0]
P150_30101010202 = [0, 0, 0, 0]
sg.theme('DefaultNoMoreNagging')
layout = [
    [sg.Text('Arquivo SPED ECF:'), sg.Input(key='file_path'), sg.FileBrowse()],
    [sg.Button('Calcular'), sg.Button('Sair')],
    [sg.Output(size=(60, 15))]
]
window = sg.Window('Cálculo de Receita', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Sair':
        break

    try:
        with open(values['file_path'], 'r', encoding='iso-8859-1') as file:
            reader = csv.reader(file, delimiter='|')
            data = [row for row in reader]
        for line in data:
            if line[1] == "P030":
                trimestre += 1
            elif line[1] == "P200":
                valor = line[4].strip().replace(",", ".")
                if valor:
                    valor_float = float(valor)
                    if line[2] == "2":
                        P200_2[trimestre] = valor_float
                    elif line[2] == "4":
                        P200_4[trimestre] = valor_float
                    elif line[2] == "6":
                        P200_6[trimestre] = valor_float
                    elif line[2] == "8":
                        P200_8[trimestre] = valor_float
                    elif line[2] == "9":
                        P200_9[trimestre] = valor_float
            elif line[1] == "P300":
                valor = line[4].strip().replace(",", ".")
                if valor:
                    P300_16[trimestre] = float(valor)

            elif line[1] == "P150":
                valor = line[8].strip().replace(",", ".")
                if line[2] == "3.01.01.01.01":
                    if valor:
                        P150_301010101[trimestre] = float(valor)
                elif line[2] == "3.01.01.01.02.01":
                    if valor:
                        P150_30101010201[trimestre] = float(valor)
                elif line[2] == "3.01.01.01.02.02":
                    if valor:
                        P150_30101010202[trimestre] = float(valor)

        receita_informada = []
        receita_calculada = []
        

        
        
        sg.popup('Receita calculada com sucesso!')
        
        for i in range(4):
            receita_informada.append(
                P200_2[i]+P200_4[i]+P200_6[i]+P200_8[i]+P200_9[i]+P300_16[i])
            receita_calculada.append(
                P150_301010101[i]-P150_30101010202[i]-P150_30101010201[i])
            if receita_calculada[i] != receita_informada[i]:
                print(
                    f'No {i+1} trimestre: {round(receita_calculada[i] - receita_informada[i],2)}')
        
    except Exception as e:
        sg.popup_error(f'Ocorreu um erro: {e}')
        print(f'Ocorreu um erro: {e}')
window.close()
