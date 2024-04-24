import customtkinter as ctk

from tkinter import messagebox

from modulos.savePost import savePost

from modulos.load_posts import fetch_posts

from modulos.deletePost import delete_data

from modulos.window_modify import new_window

from modulos.classes import Post

def tema():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

def tela_resolucao(janela, tamanho = "1200x600"):
    janela.geometry(tamanho)
    janela.title("BookPy")
    janela.maxsize(700, 800)
    janela.minsize(300, 200)
    janela.resizable(True, True)   

def tela_user(user):
    
    janela = ctk.CTk()

    tema()

    tela_resolucao(janela)
    
    def limit_size(event, max_length):
        widget = event.widget
        text = widget.get("1.0", "end-1c")
        if len(text) > max_length:
            widget.delete("1.0", "end")
            widget.insert("1.0", text[:max_length])  

    def limit_entry_size(event, max_length):
        widget = event.widget
        text = widget.get()
        if len(text) > max_length:
            widget.delete(max_length, 'end')

    def add_placeholder(widget, placeholder_text):
        if(widget):
            widget.insert('1.0', placeholder_text)
            widget.bind("<FocusIn>", lambda event: widget.delete('1.0', 'end') if widget.get('1.0', 'end-1c') == placeholder_text else None)
            widget.bind("<FocusOut>", lambda event: widget.insert('1.0', placeholder_text) if not widget.get('1.0', 'end-1c') else None)

    def add_more_infos(frame, post_args, more_infos):
        def less_infos():
            title_entry.pack_forget()
            author_entry.pack_forget()
            publisher_entry.pack_forget()

            post_args.title = None
            post_args.author = None
            post_args.publisher = None
            post_args.user_author = None
            
            less_infos_var.pack_forget()

            more_infos.pack(padx= 10, pady= 10)
        global title_entry, author_entry, publisher_entry
        
        title_entry = ctk.CTkEntry(frame, width= 400, placeholder_text="Digite o título do seu livro", font=("Roboto", 15))
        title_entry.pack(padx=10, pady=10)
        title_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

        author_entry = ctk.CTkEntry(frame, width= 400, placeholder_text="Digite o autor do seu livro", font=("Roboto", 15))
        author_entry.pack(padx=10, pady=10)
        author_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

        publisher_entry = ctk.CTkEntry(frame, width= 400, placeholder_text="Digite a editora do seu livro", font=("Roboto", 15))
        publisher_entry.pack(padx=10, pady=10)
        publisher_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

        more_infos.pack_forget()
        less_infos_var = ctk.CTkLabel(frame, text= "\U0001F809", font= ("Roboto", 20), cursor= "hand2")
        less_infos_var.pack(side="bottom", padx= 10, pady= 10)
        less_infos_var.bind("<Button-1>", lambda event: less_infos())

    def delete_post(post, widget, user):
        delete_data(post[0], user.username)
        widget.pack_forget()
        update_posts(all_posts_frame)
        
    def modify_post(post, user):
        new_window(user, post[0])
        all_posts_frame.pack_forget()
        update_posts(all_posts_frame)

    def update_posts(widget):
        for widget in widget.winfo_children():
            widget.destroy()
        
        posts= fetch_posts()

        for post in reversed(posts):
            post_frame= ctk.CTkFrame(all_posts_frame, fg_color="#363636", width= 700, height= 400)
            post_frame.pack(padx= 10, pady= 10)
            post_frame.pack_propagate(False)

            frame= ctk.CTkFrame(post_frame, fg_color="transparent", width= 600)
            frame.place(x= 10, y= 10)

            username_label= ctk.CTkLabel(frame, text=post[1], font= ("Roboto", 20))
            username_label.grid(sticky="w", row= 0, column= 0, padx=5, pady=10)

            title_label= ctk.CTkLabel(frame, text=post[3], font= ("Roboto", 15))
            title_label.grid(sticky="w", row= 1, column= 0, padx=5, pady= 10)

            author_label= ctk.CTkLabel(frame, text=post[4], font= ("Roboto", 15))
            author_label.grid(sticky="w", row= 2, column=0, padx= 5, pady= 10)

            publisher_label= ctk.CTkLabel(frame, text=post[5], font= ("Roboto", 15))
            publisher_label.grid(sticky="w", row= 3, column= 0, padx= 5, pady= 10)

            if(post[1] == user.username):
                buttons_frame= ctk.CTkFrame(post_frame, fg_color="transparent", width= 100)
                buttons_frame.place(x=350, y=10)

                delete_button= ctk.CTkButton(buttons_frame, text= "Apagar", width=30, fg_color= "#363636", hover_color="#4F4F4F", font= ("Roboto", 15), command= lambda post=post: delete_post(post, post_frame, user))
                delete_button.pack(padx= 5, pady= 5)

                modify_button= ctk.CTkButton(buttons_frame, text= "Editar", width=30, font= ("Roboto", 15), fg_color= "#363636", hover_color="#4F4F4F", command= lambda post=post: modify_post(post, user))
                modify_button.pack(padx= 5, pady= 5)

            content_label= ctk.CTkLabel(frame, text=insert_newlines(post[2]), font= ("Roboto", 15))
            content_label.grid(sticky= "w", row= 5, column= 0, padx= 5, pady= 10)

    def insert_newlines(string, every=64):
        lines = []
        for i in range(0, len(string), every):
            line = string[i:i+every]
            if i + every < len(string):
                
                if string[i+every] != ' ':
                    words = line.split(' ')
                    if len(words) > 1:
                        line = ' '.join(words[:-1])
                        string = string[:i+len(line)] + ' ' + words[-1] + string[i+every:]
            lines.append(line)
        return '\n'.join(lines)
    
    def add_post(post, content, user):

        if(content.get("1.0", "end-1c") == "Escreva aqui o que deseja postar..." or content.get("1.0", "end-1c") == ""):
            messagebox.showinfo(title= "Erro ao postar", message= "Você precisa escrever algo para postar")
            return
        
        post.content = insert_newlines(content.get("1.0", "end-1c"))
        post.user_author = user
        post.title = title_entry.get() if 'title_entry' in globals() else None
        post.author = author_entry.get() if 'author_entry' in globals() else None
        post.publisher = publisher_entry.get() if 'publisher_entry' in globals() else None

        retorno= savePost(post)

        if(retorno == 'Post salvo com sucesso!'):
            content.delete("1.0", "end")
            title_entry.delete(0, "end") if 'title_entry' in globals() else None
            author_entry.delete(0, "end") if 'author_entry' in globals() else None
            publisher_entry.delete(0, "end") if 'publisher_entry' in globals() else None

            messagebox.showinfo(title= "Postagem realizada", message= "Postagem feita com sucesso!")

            update_posts(all_posts_frame)
            janela.update()

    def main_window(user):

        user_frame = ctk.CTkFrame(janela, width= 800)
        user_frame.pack(padx= 10, pady= 10)

        side_bar_frame = ctk.CTkFrame(user_frame, width= 100)
        side_bar_frame.pack(side= "left", padx= 10, pady= 10)

        titulo = ctk.CTkLabel(side_bar_frame, text= "BookPy", font= ("Roboto", 20))
        titulo.pack(side= 'top', padx= 10, pady= 10)

        perfil_button = ctk.CTkButton(side_bar_frame, text= "Perfil", font= ("Roboto", 15), fg_color= "#363636")
        perfil_button.pack(padx= 10, pady= 10)
        
        global main_frame, all_posts_frame
        main_frame = ctk.CTkFrame(user_frame, width= 700)
        main_frame.pack(side= "right", padx= 10, pady= 10)

        post_here_frame = ctk.CTkFrame(main_frame, width= 700)
        post_here_frame.pack(side= "top", padx= 10, pady= 10)

        post_here_entry = ctk.CTkTextbox(post_here_frame, width= 420, height= 40, wrap= "word")
        post_here_entry.pack(side="top", padx= 10, pady= 10)
        post_here_entry.bind("<KeyRelease>", lambda event: limit_size(event, 200))

        add_placeholder(post_here_entry, "Escreva aqui o que deseja postar...")

        buttons_frame = ctk.CTkFrame(post_here_frame, fg_color= "transparent")
        buttons_frame.pack(side= "bottom",padx= 10, pady= 10)

        global post_scope

        post_scope = Post()

        post_button = ctk.CTkButton(buttons_frame, text= "Postar", font= ("Roboto", 15), width= 100, fg_color= "#363636", hover_color="#4F4F4F", command= lambda: add_post(post_scope, post_here_entry, user.username))
        post_button.pack(side= "bottom", padx= 10, pady= 10)

        more_infos = ctk.CTkLabel(buttons_frame, text= "\U0001F847", font= ("Roboto", 20), cursor= "hand2")
        more_infos.bind("<Button-1>", lambda event: add_more_infos(post_here_frame, post_scope, more_infos))
        more_infos.pack(side= "bottom", padx= 10, pady= 10)
        
        all_posts_frame = ctk.CTkScrollableFrame(main_frame, width= 1200)
        all_posts_frame.pack(side="bottom", fill="both", expand=True)

        update_posts(all_posts_frame)

    main_window(user)

    janela.mainloop()