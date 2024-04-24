import customtkinter as ctk

from modulos.classes import User

from modulos.profile import tela_user

import re

from tkinter import *

from tkinter import messagebox

from modulos.register import insert_into_database as insert_database

from modulos.login import login

janela = ctk.CTk()

import tkinter as tk
import customtkinter as ctk

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class Application():
    def __init__(self):
        self.janela = janela
        self.tema()
        self.tela()
        self.tela_login()
        janela.mainloop()

    def tema(self):    
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def tela(self, tamanho = "430x330"):
        janela.geometry(tamanho)
        janela.title("BookPy")
        janela.maxsize(1000, 1000)
        janela.minsize(300, 200)
        janela.resizable(False, False)

    def tela_login(self):
        def limit_entry_size(event, max_length):
            widget = event.widget
            text = widget.get()
            if len(text) > max_length:
                widget.delete(max_length, 'end')

        def remember_function(remember, login, senha, email):
            if remember == True:
                if(login.get() != "" or senha.get() != "" or email.get() != ""):
                    with open("remember.txt", "w") as file:
                        file.write(f"{login.get()} {senha.get()} {email.get()}")
                else:
                    messagebox.showinfo(title= "Estado do Login", message= "Preencha os campos de login para salvar")
            else:
                try:
                    with open("remember.txt", "w") as file:
                        file.write("")
                        login.delete(0, END)
                        senha.delete(0, END)
                        email.delete(0, END)
                except:
                    messagebox.showinfo(title= "Estado do Login", message= "Nenhum dado salvo")
            
        def U_remember(login, email, senha, check_box):
            try:
                with open("remember.txt", "r") as file:
                    data = file.read().split()
                    login.insert(0, data[0])
                    senha.insert(0, data[1])
                    email.insert(0, data[2])
                    check_box.select()
            except:
                pass

        def clique_register():
            def tela_back(frame_forget, frame_pack, tam):
                frame_forget.pack_forget()
                self.tela(tamanho= tam)
                frame_pack.pack(padx= 10, pady= 10)

            def read_terms():
                register_frame.pack_forget()

                terms_frame= ctk.CTkFrame(janela)
                terms_frame.pack(padx= 10, pady= 10)
                self.tela(tamanho= "400x280")

                terms_label= ctk.CTkLabel(terms_frame, text= "Termos e Condições", font= ("Roboto", 15))
                terms_label.pack(padx= 10, pady= 10)

                terms_text= ctk.CTkLabel(terms_frame, text= "1. BookPy é uma rede amigável para todos os grupos sociais, sendo intolerável discursos preconceituosos, ofensivos e quaisquer atitudes consideradas suspeitas.\n2. A divulgação de conteúdos pornográficos e violentos é cabível de banimento da rede.\n3. Ao clicar em 'Aceite os termos e condições para continuar', o usuário concorda em compartilhas seus dados com a empresa BookPy.\n4. A empresa BookPy não se responsabiliza por quaisquer danos causados por terceiros.\n5. A empresa BookPy se reserva o direito de banir usuários que não seguirem as regras estabelecidas.", font= ("Roboto", 10), wraplength= 350, justify= "left")
                terms_text.pack(padx= 10, pady= 10)

                back_button= ctk.CTkButton(terms_frame, text= "Voltar", command= lambda: tela_back(terms_frame, register_frame, tam= "400x410"))
                back_button.pack(padx= 10, pady= 10)

            def save_user():
                if(check_box.get() != True):
                    messagebox.showinfo(title= "Estado do Cadastro", message= "Você precisa aceitar os termos e condições para continuar")

                elif(len(login_entry.get()) > 20 or len(senha_entry.get()) > 20):
                    messagebox.showinfo(title= "Estado do Cadastro", message= "Nome de usuário ou senha muito longos. Por favor, tente novamente")

                elif(senha_entry.get() != confirmar_senha.get()):
                    messagebox.showinfo(title= "Estado do Cadastro", message= "As senhas não coincidem. Por favor, tente novamente")

                elif(len(login_entry.get()) < 4 or len(senha_entry.get()) < 4):
                    messagebox.showinfo(title= "Estado do Cadastro", message= "Nome de usuário ou senha muito curtos. Por favor, tente novamente")
                
                elif not re.search('[a-z]', senha_entry.get()):
                    messagebox.showinfo(title= "Estado do Cadastro", message= "Sua senha deve conter pelo menos um caractere minúsculo")
                
                elif not re.search('[A-Z]', senha_entry.get()):
                    messagebox.showinfo(title= "Estado do Cadastro", message= "Sua senha deve conter pelo menos um caractere maiúsculo")
                
                elif not re.search('[0-9]', senha_entry.get()):
                    messagebox.showinfo(title= "Estado do Cadastro", message= "Sua senha deve conter pelo menos um número")
                
                elif not re.search('[!@#$%^&*(),.?":{}|<>]', senha_entry.get()):
                    messagebox.showinfo(title= "Estado do Cadastro", message= "Sua senha deve conter pelo menos um caractere especial")

                elif not re.search('@', email_entry.get()):
                    messagebox.showinfo(title= "Estado do Cadastro", message= "E-mail inválido. Por favor, tente novamente")

                elif not (len(email_entry.get()) > 10 and len(email_entry.get()) < 40):
                    messagebox.showinfo(title= "Estado do Cadastro", message= "E-mail inválido. Por favor, tente novamente")

                else:
                    result = insert_database(str(login_entry.get()), str(email_entry.get()), str(senha_entry.get()))
                    messagebox.showinfo(title= "Estado do Cadastro", message= result)

            login_frame.pack_forget()

            register_frame= ctk.CTkFrame(janela)
            register_frame.pack(padx= 10, pady= 10)
            self.tela(tamanho= "400x410")

            label= ctk.CTkLabel(register_frame, text= "Preencha corretamente todos os campos abaixos\n com as informações solicitadas ", font= ("Roboto", 15))
            label.pack(padx= 10, pady= 10)
            
            login_entry= ctk.CTkEntry(register_frame, placeholder_text= "Nome de usuário com até 20 caracteres", width= 250)
            login_entry.pack(padx= 10, pady= 7)
            login_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

            email_entry= ctk.CTkEntry(register_frame, placeholder_text= "E-mail", width= 250)
            email_entry.pack(padx= 10, pady= 7)
            email_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 40))

            senha_entry= ctk.CTkEntry(register_frame, placeholder_text= "Senha com até 20 caracteres", show= "*", width= 250)
            senha_entry.pack(padx= 10, pady= 7)
            senha_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

            confirmar_senha= ctk.CTkEntry(register_frame, placeholder_text= "Confirmar senha", show= "*", width= 250)
            confirmar_senha.pack(padx= 10, pady= 7)
            confirmar_senha.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

            check_box= ctk.CTkCheckBox(register_frame, text= "Aceite os termos e condições para continuar")
            check_box.pack(padx= 10, pady= 7)
            
            label_check= ctk.CTkLabel(register_frame, text= "Leia os termos e condições clicando aqui", font= ("Roboto", 10), cursor= "hand2")
            label_check.bind("<Button-1>", lambda event: read_terms())
            label_check.pack(padx= 10, pady= 7)

            save_button= ctk.CTkButton(register_frame, text= "Cadastrar-se", command= save_user)
            save_button.pack(padx= 10, pady= 7)

            back_button= ctk.CTkButton(register_frame, text= "Voltar à área de login", command= lambda: tela_back(register_frame, login_frame, tam= "430x330"))
            back_button.pack(padx= 10, pady= 7)

        def clique_login():
            result = login(login_entry.get(), senha_entry.get(), email_entry.get())
            messagebox.showinfo(title= "Estado de Login", message= result)
            if(result == "Usuário encontrado!"):
                
                usuario= User(login_entry.get(), senha_entry.get(), email_entry.get())

                janela.destroy()

                tela_user(usuario)

        login_frame = ctk.CTkFrame(janela)
        login_frame.pack(padx=10, pady=10)
        login_frame.configure(width= 300, height= 70)
            
        texto = ctk.CTkLabel(login_frame, text= "Entre na sua conta BookPy!", font=("Roboto", 15))
        texto.pack(padx= 10, pady= 10)
        
        login_entry = ctk.CTkEntry(login_frame, placeholder_text= "Login")
        login_entry.pack(padx=10, pady=10)
        login_entry.configure(width= 400, height= 50)
        login_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

        email_entry = ctk.CTkEntry(login_frame, placeholder_text= "E-mail")
        email_entry.pack(padx=10, pady=10)
        email_entry.configure(width= 400, height= 50)
        email_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 40))
        
        senha_entry = ctk.CTkEntry(login_frame, placeholder_text= "Senha", show= "*")
        senha_entry.pack(padx= 10, pady= 10)
        senha_entry.configure(width= 400, height= 50)
        senha_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

        register_button = ctk.CTkButton(login_frame, text= "Cadastre-se", command= clique_register)
        register_button.pack(side="right", padx=10, pady=10)
        register_button.configure(width=100, height=35)

        remember_check = ctk.CTkCheckBox(login_frame, text= "Lembre-se de mim")
        remember_check.pack(side="right", padx=10, pady=10)
        ToolTip(remember_check, "Salve seus dados para não precisar digitá-los novamente. Lembre-se de que seus dados ficarão salvos no seu computador.")

        remember_check.bind("<Button-1>", lambda event: remember_function(remember_check.get(), login_entry, senha_entry, email_entry))
    
        login_button = ctk.CTkButton(login_frame, text= "Login", command= clique_login)
        login_button.pack(side="left", padx=10, pady=10)
        login_button.configure(width=100, height=35)

        U_remember(login_entry, email_entry, senha_entry, remember_check)
        
Application()