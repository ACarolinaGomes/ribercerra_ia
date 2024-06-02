import PySimpleGUI as sg
import webbrowser
import os
import io
import json
import psycopg2
import requests
from io import BytesIO
from PIL import Image
from pprint import pprint

working_directory = os.getcwd()

API_KEY = "2b10Xq0KJm9iGzfiEiSUf6qf6"
PROJECT = "all"
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}&lang=pt&include-related-images=true"
data = { 'organs': ['auto'] }

username = ''
password = ''
email = ''
usuarios = ''
VERDE = '#033814'
HIPERTEXTO = '#633414'
LINEBREAK = '#138046'

usuarioLogado = ''
json_result = ''

conexao = psycopg2.connect(database = "Ribercerra",
                           host = "localhost",
                           user = "postgres",
                           password = "03142131",
                           port = "5432")

banco = conexao.cursor()

def alterar_senha(novaSenha):
    global usuarioLogado
    try: 
        banco.execute(f''' UPDATE tb_user SET senha_user = '{novaSenha}' WHERE id_user = {usuarioLogado[0]}; ''')
        conexao.commit()
        sg.Popup("Senha Atualizada!", font=("Roboto", 12))
        banco.execute(f''' SELECT * FROM tb_user WHERE id_user = {usuarioLogado[0]} ''')
        usuarioLogado = banco.fetchone()
    except:
        sg.Popup("Um erro ocorreu!", font=("Roboto", 12))

def alterar_email(novoEmail):
    global usuarioLogado
    try: 
        banco.execute(f''' UPDATE tb_user SET email = '{novoEmail}' WHERE id_user = {usuarioLogado[0]}; ''')
        conexao.commit()
        sg.Popup("Email atualizado!", font=("Roboto", 12))
        banco.execute(f''' SELECT * FROM tb_user WHERE id_user = {usuarioLogado[0]} ''')
        usuarioLogado = banco.fetchone()
    except:
        sg.Popup("Email em utilização, favor digitar outro.", font=("Roboto", 12))

def config():
    sg.theme('LightGreen10')
    layout_column=[[sg.Push(), sg.Text("Alterar senha", size=(28,1), font=("Inder", 14, "italic")), sg.Push()],
              [sg.Push(), sg.Text("Insira a senha antiga:", size=(28,1), font=("Inder", 12)), sg.InputText(key='-passwordold-', font=("Inder", 12), password_char='*'), sg.Push()],
              [sg.Push(), sg.Text("Insira a nova senha:", size=(28,1), font=("Inder",12)), sg.InputText(key='-password-', font=("Inder", 12), password_char='*'), sg.Push()],
              [sg.Push(), sg.Text("Confirme a nova senha:", size=(28,1), font=("Inder", 12)), sg.InputText(key='-repassword-', font=("Inder", 12), password_char='*'), sg.Push()],
              [sg.Button("Alterar senha", font=("Roboto", 12, "bold"))],
              [sg.Push(), sg.Text("__________",  size=(28,2), font=("Inder", 10), text_color=LINEBREAK), sg.Push()],
              [sg.Push(), sg.Text("Alterar o e-mail",  size=(28,1), font=("Inder", 14, "italic")), sg.Push()],
              [sg.Push(), sg.Text("Insira o novo e-mail:", size=(28,1), font=("Inder",12)), sg.InputText(key='-email-', font=("Inder",12)), sg.Push()],
              [sg.Button("Alterar e-mail", font=("Roboto", 12, "bold"))]
              ]
    menu_def=[['Menu',['Início', 'Perfil', 'Identificar', 'Mapa', 'Enciclopedia', 'Sobre', 'Sair']]]
    layout = [[sg.Menu(menu_def)],
              [sg.Column(layout_column, element_justification='center')],
              [sg.Text("<< Voltar", text_color=HIPERTEXTO, font=("Inder", 10, "italic", "underline"), enable_events=True)]
              ]
    window = sg.Window("Configurações", layout)

    while True:
        event, values = window.read()
        if event == 'Sair':
            window.close()
            menu_inicial()
            break
        else:
            if event == sg.WIN_CLOSED:
                break
            else:
                if event == "Sobre":
                    window.close()
                    sobre()
                    break
                else:
                    if event == "Identificar":
                        window.close()
                        identificacao()
                        break
                    else:
                        if event == "Mapa":
                            window.close()
                            mapa()
                            break
                        else:
                            if event == "Enciclopedia":
                                window.close()
                                enciclopedia()
                                break
                            else:
                                if event == "Início":
                                    window.close()
                                    menu_pos_login()
                                    break
                                else:
                                    if event == "Perfil":
                                        window.close()
                                        perfil()
                                        break
                                    else:
                                        if event == "Alterar senha":
                                            if values['-passwordold-'] == usuarioLogado[3]:
                                                if values['-password-'] == values['-repassword-']:
                                                    alterar_senha(values['-password-'])
                                                continue
                                            else:
                                                sg.popup("Senha Incorreta.")
                                        else:
                                            if event == "<< Voltar":
                                                window.close()
                                                perfil()
                                                break
                                            else:
                                                if event == "Alterar e-mail":
                                                    alterar_email(values['-email-'])
                                                continue

    window.close()

def exportar_dados():
    sg.theme('LightGreen10')
    menu_def=[['Menu',['Início', 'Perfil', 'Identificar', 'Mapa', 'Enciclopedia', 'Sobre', 'Sair']]]
    layout = [[sg.Menu(menu_def)],]
    window = sg.Window("RiberCerra", layout)

    while True:
        event, values = window.read()
        if event == 'Sair':
            window.close()
            menu_inicial()
            break
        else:
            if event == sg.WIN_CLOSED:
                break
            else:
                if event == "Sobre":
                    window.close()
                    sobre()
                    break
                else:
                    if event == "Identificar":
                        window.close()
                        identificacao()
                        break
                    else:
                        if event == "Mapa":
                            window.close()
                            mapa()
                            break
                        else:
                            if event == "Enciclopedia":
                                window.close()
                                enciclopedia()
                                break
                            else:
                                if event == "Início":
                                    window.close()
                                    menu_pos_login()
                                    break
                                else:
                                    if event == "Perfil":
                                        window.close()
                                        perfil()
                                        break
    window.close()

def popupIdentificacao(planta):
    sg.theme('LightGreen10')

    response = requests.get(planta['images'][0]['url']['o'])
    imagem = Image.open(BytesIO(response.content))
    png_bio = io.BytesIO()
    imagem.save(png_bio, format='PNG')
    pngData = png_bio.getvalue()


    layout_column = [[sg.Text("Provável identificação", justification='center', font=("Roboto", 20, "bold"), size=(50,1))],
              [sg.Text("_______________", justification='center', text_color=LINEBREAK)],
              [sg.Text("Nomes comuns: ", justification='center', font=("Roboto", 17, "bold"))],
              [sg.Text(nomeComum, font=("Roboto", 14)) for nomeComum in planta['species']['commonNames']],
              [sg.Image(data=pngData)] ]
    
    layout = [[sg.Column(layout_column, element_justification='center')]]
    
    window = sg.Window("Identificação", layout, element_justification='center')
    
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            window.close()
            identificacao()
            break
    window.close()

def post(files):
    global json_result
    req = requests.Request('POST', url=api_endpoint, files=files, data=data)
    prepared = req.prepare()

    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)

    pprint(response.status_code)
    pprint(json_result)

    if json_result['results'][0]['score'] > 0.05:
        popupIdentificacao(json_result['results'][0])
    else:
        sg.popup("Planta não identificada")

def identificacao():
    sg.theme('LightGreen10')
    menu_def=[['Menu',['Início', 'Perfil', '!&Identificar', 'Mapa', 'Enciclopedia', 'Sobre', 'Sair']]]
    layout = [[sg.Menu(menu_def)],
                [sg.Text("Choose a PNG file:")],
                [sg.InputText(key="-FILE_PATH-"), 
                sg.FileBrowse(initial_folder=working_directory, file_types=[("JPEG Files", "*.jpeg")])],
                [sg.Button('Submit'), sg.Exit()]]
    
    window = sg.Window("Identifique uma planta", layout)

    while True:
        event, values = window.read()
        if event == 'Sair':
            window.close()
            menu_inicial()
            break
        else:
            if event == sg.WIN_CLOSED:
                break
            else:
                if event == "Sobre":
                    window.close()
                    sobre()
                    break
                else:
                    if event == "Perfil":
                        window.close()
                        perfil()
                        break
                    else:
                        if event == "Mapa":
                            window.close()
                            mapa()
                            break
                        else:
                            if event == "Enciclopedia":
                                window.close()
                                enciclopedia()
                                break
                            else:
                                if event == "Início":
                                    window.close()
                                    menu_pos_login()
                                    break
                                elif event == "Submit":
                                    address = values["-FILE_PATH-"]
                                    files = [
                                        ('images', (address, open(address, 'rb')))
                                    ]
                                    print(files)   
                                    post(files)
                                    break
                                    
    window.close()

def enciclopedia():
    sg.theme('LightGreen10')
    menu_def=[['Menu',['Início', 'Perfil', 'Identificar', 'Mapa', '!&Enciclopedia', 'Sobre', 'Sair']]]
    layout = [[sg.Menu(menu_def)],]
    window = sg.Window("RiberCerra", layout)

    while True:
        event, values = window.read()
        if event == 'Sair':
            window.close()
            menu_inicial()
            break
        else:
            if event == sg.WIN_CLOSED:
                break
            else:
                if event == "Sobre":
                    window.close()
                    sobre()
                    break
                else:
                    if event == "Perfil":
                        window.close()
                        perfil()
                        break
                    else:
                        if event == "Mapa":
                            window.close()
                            mapa()
                            break
                        else:
                            if event == "Identificar":
                                window.close()
                                identificacao()
                                break
                            else:
                                if event == "Início":
                                    window.close()
                                    menu_pos_login()
                                    break
    window.close()

def mapa():
    sg.theme('LightGreen10')
    menu_def=[['Menu',['Início', 'Perfil', 'Identificar', '!&Mapa', 'Enciclopedia', 'Sobre', 'Sair']]]
    layout = [[sg.Menu(menu_def)],
              [sg.Push(), sg.Text("Mapa da região", font=("Inder", 14, "bold")), sg.Push()],
              [sg.Image(filename='D:/fatec/6o semestre/python/ribercerra_ia/mock_map.PNG')],
              [sg.Push(), sg.Button("Identifique uma planta", font=("Roboto", 14)), sg.Push()]]
    
    window = sg.Window("RiberCerra - Mapa", layout)

    while True:
        event, values = window.read()
        if event == 'Sair':
            window.close()
            menu_inicial()
            break
        else:
            if event == sg.WIN_CLOSED:
                break
            else:
                if event == "Sobre":
                    window.close()
                    sobre()
                    break
                else:
                    if event == "Perfil":
                        window.close()
                        perfil()
                        break
                    else:
                        if event == "Identificar" or event =="Identifique uma planta":
                            window.close()
                            identificacao()
                            break
                        else:
                            if event == "Enciclopedia":
                                window.close()
                                enciclopedia()
                                break
                            else:
                                if event == "Início":
                                    window.close()
                                    menu_pos_login()
                                    break
    window.close()

def perfil():
    sg.theme('LightGreen10')
    menu_def=[['Menu',['Início', '!&Perfil', 'Identificar', 'Mapa', 'Enciclopedia', 'Sobre', 'Sair']]]
    layout_column=[[sg.Push(), sg.Text("Meu Perfil", font=("Inder", 14, "bold")), sg.Push()],
                   [sg.Push(), sg.Text("________________", font=("Inder", 10), text_color=LINEBREAK), sg.Push()],
                   [sg.Push(), sg.Text(usuarioLogado[1], font=("Roboto", 12, "bold")), sg.Push()],
                   [sg.Push(), sg.Text(usuarioLogado[2], font=("Roboto", 10)), sg.Push()],
                   [sg.Button("Configurações", font=("Inder", 12)), sg.Button("Exportar dados", font=("Inder", 12))]]
    layout=[[sg.Menu(menu_def)],
            [sg.Column(layout_column, element_justification='center')]
            ]
    window = sg.Window("RiberCerra - Perfil", layout)

    while True:
        event, values = window.read()
        if event == 'Sair':
            window.close()
            menu_inicial()
            break
        else:
            if event == sg.WIN_CLOSED:
                break
            else:
                if event == "Sobre":
                    window.close()
                    sobre()
                    break
                else:
                    if event == "Identificar":
                        window.close()
                        identificacao()
                        break
                    else:
                        if event == "Mapa":
                            window.close()
                            mapa()
                            break
                        else:
                            if event == "Enciclopedia":
                                window.close()
                                enciclopedia()
                                break
                            else:
                                if event == "Início":
                                    window.close()
                                    menu_pos_login()
                                    break
                                else:
                                    if event == "Configurações":
                                        window.close()
                                        config()
                                        break
                                    else:
                                        if event == "Exportar dados":
                                            window.close()
                                            exportar_dados()
                                            break
    window.close()

def sobre():
    sg.theme('LightGreen10')
    menu_def=[['Menu',['Início', 'Perfil', 'Identificar', 'Mapa', 'Enciclopedia', '!&Sobre', 'Sair']]]
    layout_column = [[sg.Push(), sg.Text("Sobre o RiberCerra", font=("Roboto", 18, "bold")), sg.Push()],
                     [sg.Push(), sg.Text("______________________________", font=("Inder", 10), text_color=LINEBREAK), sg.Push()],
                     [sg.Push(), sg.Text("Código fonte", justification='center', font=("Inder", 10, "italic"), enable_events=True, text_color=HIPERTEXTO), sg.Push()],
                     [sg.Text("Aplicativo desenvolvido por Gabriel Leandro de Araujo Pilato e Ana Carolina da Silva Gomes", font=("Inder", 10))],
                     [sg.Push(), sg.Text("______________________________", font=("Inder", 10), text_color=LINEBREAK), sg.Push()],
                     [sg.Text("O Projeto RiberCerra é um aplicativo com o intuito de catalogar e disseminar\n o conhecimento de espécies de flora nativa do Cerrado.", font=("Inder", 12))],
                     [sg.Text("Nesta versão, pretendemos demonstrar a capacidade de reconhecimento de\nflora por meio da API Pl@ntNet e suas limitações.", font=("Inder", 12))],
                     [sg.Push(), sg.Text("______________________________", font=("Inder", 10), text_color=LINEBREAK), sg.Push()],
                     [sg.Text("Sobre o Pl@ntNet", font=("Roboto", 14, "bold"), text_color=HIPERTEXTO, enable_events=True)],
                     [sg.Image(filename="D:/fatec/6o semestre/python/ribercerra_ia/Plantnet_logo.png")],
                     [sg.Text("Pl@ntNet é um projeto de ciências com foco na disseminação de conhecimento civil.", font=("Inder", 10), text_color=HIPERTEXTO)]
                     ]
    layout=[[sg.Menu(menu_def)],
            [sg.Column(layout_column, element_justification='center')]
            ]
    window = sg.Window("RiberCerra - Sobre", layout)

    while True:
        event, values = window.read()
        if event == 'Sair':
            window.close()
            menu_inicial()
            break
        else:
            if event == sg.WIN_CLOSED:
                break
            else:
                if event == "Perfil":
                    window.close()
                    perfil()
                    break
                else:
                    if event == "Identificar":
                        window.close()
                        identificacao()
                        break
                    else:
                        if event == "Mapa":
                            window.close()
                            mapa()
                            break
                        else:
                            if event == "Enciclopedia":
                                window.close()
                                enciclopedia()
                                break
                            else:
                                if event == "Início":
                                    window.close()
                                    menu_pos_login()
                                    break
                                else:
                                    if event == "Código fonte":
                                        webbrowser.open("https://github.com/GabrielPilato/RiberCerra")
                                        break
                                    else:
                                        if event == "Sobre o Pl@ntNet":
                                            webbrowser.open("https://my.plantnet.org/")
    window.close()

def menu_pos_login():
    sg.theme('LightGreen10')
    layout_column = [[sg.Text("ÚLTIMAS DESCOBERTAS", justification='center', font=("Roboto", 20, "bold"))],
                     [sg.Image(filename=f'{working_directory}\mock_map.PNG')],
                     [sg.Text("_______________", justification='center', text_color=LINEBREAK)],
                     [sg.Text("Angelim-do-Cerrado", font=("Inder", 16), justification='center')],
                     [sg.Image(filename=f'{working_directory}\\angelim.png')],
                     [sg.Text("Espécie florestal comum no Cerrado.", size=(20,2), justification='center', font=("Inder", 12)), 
                      sg.Text("Leia mais na enciclopédia>>", enable_events=True, font=("Inder", 12, "bold"), text_color=HIPERTEXTO)]]
    menu_def=[['Menu',['!&Início', 'Perfil', 'Identificar', 'Mapa', 'Enciclopedia', 'Sobre', 'Sair']]]
    layout = [[sg.Menu(menu_def)],
              [sg.Column(layout_column, scrollable=True, vertical_scroll_only=True, element_justification='center')]
              ]
    window = sg.Window("RiberCerra", layout)

    while True:
        event, values = window.read()
        if event == 'Sair':
            window.close()
            menu_inicial()
            break
        else:
            if event == sg.WIN_CLOSED:
                break
            else:
                if event == "Perfil":
                    window.close()
                    perfil()
                    break
                else:
                    if event == "Identificar":
                        window.close()
                        identificacao()
                        break
                    else:
                        if event == "Mapa":
                            window.close()
                            mapa()
                            break
                        else:
                            if event == "Enciclopedia" or event == "Leia mais na enciclopédia>>":
                                window.close()
                                enciclopedia()
                                break
                            else:
                                if event == "Sobre":
                                    window.close()
                                    sobre()
                                    break
    window.close()

def insert_account(username, email, password):
    try:
        banco.execute(f''' INSERT INTO tb_user (nome_user, email, senha_user) VALUES ('{username}','{email}','{password}'); ''')
        conexao.commit()
        sg.Popup("Usuário cadastrado!", font=("Roboto", 12))
    except:
        sg.Popup("Um erro ocorreu", font=("Roboto", 12))


def verifica_login(email, password):
    global usuarioLogado
    for usuario in usuarios:
        print(usuario)
        if usuario[2] == email:
            if usuario[3] == password: 
                usuarioLogado = usuario
                return True
            else:
                return False
    return False

            

def create_account():
    global username, password, email
    sg.theme('LightGreen10')
    layout = [[sg.Text("Cadastro", size =(28, 1), justification='center', font=("Inder", 16, "bold"))],
             [sg.Text("E-mail", size =(14, 1),font=("Inder", 12)), sg.InputText(key='-email-', font=("Inder", 12))],
             [sg.Text("Reinsira o E-mail", size =(14, 1), font=("Inder", 12)), sg.InputText(key='-remail-', font=("Inder", 12))],
             [sg.Text("Nome de usuário", size =(14, 1), font=("Inder", 12)), sg.InputText(key='-username-', font=("Inder", 12))],
             [sg.Text("Senha", size =(14, 1), font=("Inder", 12)), sg.InputText(key='-password-', font=("Inder", 12), password_char='*')],
             [sg.Button("Registre-se", font=("Roboto", 14, "bold")), sg.Button("Cancelar", font=("Roboto", 14))]]

    window = sg.Window("Cadastro de Usuário", layout)

    print(conexao.status)

    while True:
        event,values = window.read()
        if event == 'Cancelar':
            window.close()
            menu_inicial()
            break
        else:
            if event == "Registre-se":
                password = values['-password-']
                username = values['-username-']
                if values['-email-'] != values['-remail-']:
                    sg.popup_error("Valores inválidos. Por favor, tente novamente", font=("Roboto", 12))
                    continue
                elif values['-email-'] == values['-remail-']:
                    email = values['-email-']
                    insert_account(username, email, password)
                    window.close()
                    menu_inicial()
                    break
            else:
                if sg.WIN_CLOSED:
                    break
    window.close()

def login():
    global username,password,usuarios
    sg.theme("LightGreen10")
    layout = [[sg.Text("Log In", size =(28, 1), font=("Inder", 16, "bold"))],
            [sg.Text("Email", size =(14, 1), font=("Inder", 12)),sg.InputText(key='-email-', font=("Inder", 12))],
            [sg.Text("Senha", size =(14, 1), font=("Inder", 12)),sg.InputText(key='-pwd-', password_char='*', font=12)],
            [sg.Button('Ok'),sg.Button('Cancelar')]]

    window = sg.Window("Log In", layout)

    banco.execute(''' SELECT * FROM tb_user ''')
    usuarios = banco.fetchall()
    print(usuarios)

    while True:
        event,values = window.read()
        if event =="Cancelar":
            window.close()
            menu_inicial()
            break
        else:
            if event == sg.WIN_CLOSED:
                break
            else:
                if event == "Ok":
                    if verifica_login(values['-email-'], values['-pwd-']):
                        sg.popup("Bem vindo ao RiberCerra!")
                        window.close()
                        menu_pos_login()
                        break
                    else:
                        sg.popup("Login inválido. Tente novamente.")
    window.close()

def menu_inicial():
    sg.theme('LightGreen10')
    layout_column = [[sg.Text("RiberCerra", justification='center', size = (28,1), font=("Inder", 28, "bold"))],
        [sg.Text("Bem vindo ao RiberCerra.", justification='center', font=("Inder", 12))],
        [sg.Text("Nosso projeto original", justification='center', enable_events=True, font=("Inder", 10, "bold", "underline"), text_color=HIPERTEXTO)],
        [sg.Button("Registre-se", font=("Roboto", 14, "bold")), sg.Button("Login", font=("Roboto", 14)), sg.Button("Sair", font=("Roboto", 14))]]
    layout = [[sg.Titlebar("RiberCerra")],
        [sg.Column(layout_column, element_justification='center')]]
    window = sg.Window("RiberCerra", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Sair":
            break
        else:
            if event =="Registre-se":
                window.close()
                create_account()
                break
            else:
                if event == "Login":
                    window.close()
                    login()
                    break
                else:
                    if event=="Nosso projeto original":
                        webbrowser.open("https://github.com/GabrielPilato/RiberCerra")
    window.close()

menu_inicial()
