import customtkinter as ctk

from tkinter import messagebox

from modulos.classes import Post

from modulos.modifyPost import modify_data

def limit_entry_size(event, max_length):
    widget = event.widget
    text = widget.get()
    if len(text) > max_length:
        widget.delete(max_length, 'end')

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
    title_entry.pack(side="top", padx=10, pady=10)
    title_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

    author_entry = ctk.CTkEntry(frame, width= 400, placeholder_text="Digite o autor do seu livro", font=("Roboto", 15))
    author_entry.pack(side="top", padx=10, pady=10)
    author_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

    publisher_entry = ctk.CTkEntry(frame, width= 400, placeholder_text="Digite a editora do seu livro", font=("Roboto", 15))
    publisher_entry.pack(side="top", padx=10, pady=10)
    publisher_entry.bind("<KeyRelease>", lambda event: limit_entry_size(event, 20))

    more_infos.pack_forget()
    less_infos_var = ctk.CTkLabel(frame, text= "\U0001F809", font= ("Roboto", 20), cursor= "hand2")
    less_infos_var.pack(side="bottom", padx= 10, pady= 10)
    less_infos_var.bind("<Button-1>", lambda event: less_infos())

def add_placeholder(widget, placeholder_text):
    if(widget):
        widget.insert('1.0', placeholder_text)
        widget.bind("<FocusIn>", lambda event: widget.delete('1.0', 'end') if widget.get('1.0', 'end-1c') == placeholder_text else None)
        widget.bind("<FocusOut>", lambda event: widget.insert('1.0', placeholder_text) if not widget.get('1.0', 'end-1c') else None)

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

def modify(post, content, user, window, id):
    post.content = insert_newlines(content.get('1.0', 'end-1c')) if content.get('1.0', 'end-1c').strip() != "Escreva aqui o que deseja postar..." else post.content
    post.user_author = user
    post.title = title_entry.get() if 'title_entry' in globals() else post.title
    post.author = author_entry.get() if 'author_entry' in globals() else post.author
    post.publisher = publisher_entry.get() if 'publisher_entry' in globals() else post.publisher

    result = modify_data(post, user, id)
    if(result == "Post modificado com sucesso!"):
        window.destroy()
        
    else:
        messagebox.showerror(title= "Erro ao modificar post", message= result)
        content.delete('1.0', 'end-1c')  if content.get('1.0', 'end-1c').strip() != "Escreva aqui o que deseja postar..." or content.get('1.0', 'end-1c') else None
        title_entry.delete(0, 'end')  if 'title_entry' in globals() else post.title
        author_entry.delete(0, 'end')  if 'author_entry' in globals() else post.author
        publisher_entry.delete(0, 'end')  if 'publisher_entry' in globals() else post.publisher
        
def new_window(user, id):

    new= ctk.CTk()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    new.geometry("430x330")

    new.title("BookPy")

    new.minsize(400, 300)

    new.resizable(False, False)
    
    post_here_frame = ctk.CTkFrame(new, width= 700)
    post_here_frame.pack(side= "top", padx= 10, pady= 10)
    
    label = ctk.CTkLabel(new, text= "Editar Post", font= ("Roboto", 15))
    label.pack(padx= 10, pady= 10)

    post_here_entry = ctk.CTkTextbox(post_here_frame, width= 420, height= 40, wrap= "word")
    post_here_entry.pack(side="top", padx= 10, pady= 10)

    add_placeholder(post_here_entry, "Escreva aqui o que deseja postar...")

    global post_scope

    post_scope = Post()

    post_button = ctk.CTkButton(post_here_frame, text= "Postar", font= ("Roboto", 15), width= 100, fg_color= "#363636", hover_color="#4F4F4F", command= lambda: modify(post_scope, post_here_entry, user.username, new, id))
    post_button.pack(side="bottom", padx= 10, pady= 10)

    more_infos = ctk.CTkLabel(post_here_frame, text= "\U0001F847", font= ("Roboto", 20), cursor= "hand2")
    more_infos.bind("<Button-1>", lambda event: add_more_infos(post_here_frame, post_scope, more_infos))
    more_infos.pack(side= "bottom", padx= 10, pady= 10)
    new.mainloop()