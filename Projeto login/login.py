import customtkinter
from tkinter import *
import sqlite3
from datetime import datetime

# Criar banco de dados e tabelas se não existirem
def criar_bd():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para abrir a janela de cadastro
def abrir_tela_cadastro():
    def capturar_dados():
        nome = nome_entry.get()
        email = email_entry.get()
        senha = senha_entry.get()
        confirmar_senha = confirmar_senha_entry.get()

        if senha == confirmar_senha:
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nome, email, senha)
                VALUES (?, ?, ?)
            ''', (nome, email, senha))
            conn.commit()
            conn.close()
            tela_cadastro.destroy()
        else:
            erro_label.config(text="As senhas não coincidem!", text_color="red")

    def toggle_password_visibility():
        if senha_entry.cget('show') == '*':
            senha_entry.config(show='')
            confirmar_senha_entry.config(show='')
            tela_cadastro.after(2000, lambda: senha_entry.config(show='*'))
            tela_cadastro.after(2000, lambda: confirmar_senha_entry.config(show='*'))
        else:
            senha_entry.config(show='*')
            confirmar_senha_entry.config(show='*')

    tela_cadastro = customtkinter.CTk()
    tela_cadastro.geometry("400x500")  # Aumentando a altura da janela de cadastro
    tela_cadastro.title("Tela de Cadastro")

    # Adicionar widgets de cadastro aqui
    cadastro_label = customtkinter.CTkLabel(master=tela_cadastro, text="Cadastro de Usuário", font=("Roboto", 20), text_color="white")
    cadastro_label.pack(pady=20)

    nome_entry = customtkinter.CTkEntry(master=tela_cadastro, placeholder_text="Nome completo", width=250, height=40)
    nome_entry.pack(pady=10)

    email_entry = customtkinter.CTkEntry(master=tela_cadastro, placeholder_text="Email", width=250, height=40)
    email_entry.pack(pady=10)

    senha_entry = customtkinter.CTkEntry(master=tela_cadastro, placeholder_text="Senha", show="*", width=250, height=40)
    senha_entry.pack(pady=10)

    confirmar_senha_entry = customtkinter.CTkEntry(master=tela_cadastro, placeholder_text="Confirmar senha", show="*", width=250, height=40)
    confirmar_senha_entry.pack(pady=10)

    # Adicionar botão para alternar a visibilidade da senha
    toggle_button = customtkinter.CTkButton(master=tela_cadastro, text="Mostrar/Ocultar Senha", command=toggle_password_visibility)
    toggle_button.pack(pady=10)

    # Adicionar rótulo para mensagens de erro
    erro_label = customtkinter.CTkLabel(master=tela_cadastro, text="", font=("Roboto", 10), text_color="red")
    erro_label.pack(pady=10)

    # Adicionar botão de cadastro na cor verde
    cadastrar_button = customtkinter.CTkButton(master=tela_cadastro, text="Cadastre-se", fg_color="green", command=capturar_dados, width=250, height=40)
    cadastrar_button.pack(pady=20)

    tela_cadastro.mainloop()

# Criar banco de dados e tabelas ao iniciar o programa
criar_bd()

# Mostrar janela com ícone
janela = customtkinter.CTk()
janela.geometry("800x500")  # Alterando o tamanho da janela para 800x500
janela.title("Sistema de login")
janela.iconbitmap("icon.ico")

# Impedir o ajuste de tela
janela.resizable(False, False)

# Trabalhando com as imagens
img = PhotoImage(file="log.png")
label_img = customtkinter.CTkLabel(master=janela, image=img)
label_img.place(x=350, y=50)  # Ajuste a posição conforme necessário

# Frame
frame = customtkinter.CTkFrame(master=janela, width=300, height=450)  # Aumentando a altura do frame
frame.place(x=25, y=50)  # Ajuste a posição conforme necessário

# Frame widgets
label = customtkinter.CTkLabel(master=frame, text="Sistema de Login", font=("Roboto", 30), text_color="white")
label.place(x=25, y=5)

# Determinando a largura máxima dos campos de entrada e botão de login
max_width = 250

# Função para capturar o que é digitado nos campos de entrada
def get_input():
    username = username_entry.get()
    password = password_entry.get()
    
    # Verificar se o usuário está no banco de dados
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM usuarios WHERE nome = ? AND senha = ?
    ''', (username, password))
    result = cursor.fetchone()
    
    if result:
        print("Login bem-sucedido!")
        # Registrar login bem-sucedido no banco de dados
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO logins (nome, data_hora)
            VALUES (?, ?)
        ''', (username, data_hora))
        conn.commit()
    else:
        print("Nome de usuário ou senha incorretos.")
    
    conn.close()

# Função para alternar a visibilidade da senha com temporizador de 2 segundos
def toggle_password_visibility():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        janela.after(2000, lambda: password_entry.config(show='*'))
    else:
        password_entry.config(show='*')

# Adicionar campos de entrada para o login
username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Nome de usuário", width=max_width, height=40)
username_entry.place(x=25, y=80)

password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Senha", show="*", width=max_width, height=40)
password_entry.place(x=25, y=160)

# Adicionar botão para alternar a visibilidade da senha
toggle_button = customtkinter.CTkButton(master=frame, text="Mostrar/Ocultar Senha", command=toggle_password_visibility)
toggle_button.place(x=25, y=200)

# Adicionar texto indicando campos obrigatórios abaixo dos campos de usuário e senha
required_label_user = customtkinter.CTkLabel(master=frame, text="* Campo obrigatório", text_color="green", font=("Roboto", 10))
required_label_user.place(x=25 + (max_width - required_label_user.winfo_reqwidth()) // 2, y=120)  # Centralizar abaixo do campo de usuário

required_label_password = customtkinter.CTkLabel(master=frame, text="* Campo obrigatório", text_color="green", font=("Roboto", 10))
required_label_password.place(x=25 + (max_width - required_label_password.winfo_reqwidth()) // 2, y=240)  # Centralizar abaixo do campo de senha

# Adicionar botão "Lembrar-se de mim"
remember_me_button = Checkbutton(master=frame, text="Lembrar-se de mim", fg="green", font=("Roboto", 10))
remember_me_button.place(x=25, y=280)  # Ajuste a posição conforme necessário

# Adicionar botão de login
login_button = customtkinter.CTkButton(master=frame, text="Entrar", command=get_input, width=max_width, height=40)
login_button.place(x=25, y=320)

# Adicionar botão de cadastro
register_button = customtkinter.CTkButton(master=frame, text="Cadastre-se", fg_color="green", command=abrir_tela_cadastro, width=max_width, height=40)
register_button.place(x=25, y=380)

# Adicionar texto "Se não tem conta" abaixo do botão de cadastro
if_not_registered_label = customtkinter.CTkLabel(master=frame, text="Se não tem conta", text_color="blue", font=("Roboto", 14))
if_not_registered_label.place(x=25 + (max_width - if_not_registered_label.winfo_reqwidth()) // 2, y=430)  # Ajuste a posição conforme necessário

janela.mainloop()
