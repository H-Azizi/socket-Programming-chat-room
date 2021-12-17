from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox #Tkinter Python Module for GUI
import socket #Sockets for network connection
import threading # for multiple proccess 
import cryptocode


class GUI:
    pass_temp = ""
    client_socket = None
    last_received_message = None
    
    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.initialize_socket()
        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialazing socket with TCP and IPv4
        remote_ip = '127.0.0.1' # IP address 
        remote_port = 10319 #TCP port
        self.client_socket.connect((remote_ip, remote_port)) #connect to the remote server

    def initialize_gui(self): # GUI initializer
        self.root.title("UOK Chat Room")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_name_section()
        self.display_password_section()
        self.display_chat_entry_box()
    
    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,)) # Create a thread for the send and receive in same time
        thread.start()
    #function to recieve msg
    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode('utf-8')
         
            if "joined" in message:
                user = message.split(":")[1]
                message = user + " has joined"
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)
            else:
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)

        so.close()

    def display_name_section(self):
        frame = Frame()
        Label(frame, text='Enter your ID       ',fg='#0059b3', font=("Helvetica 12 bold")).pack(side='left', padx=10)
        self.name_widget = Entry(frame, width=51, borderwidth=2)
        self.name_widget.pack(side='left', anchor='e')
        self.sign_in_button = Button(frame, text="sign up", width=10, fg='#FF0055', bg='#BAEE17',command=self.sigh_up).pack(side='left')
        frame.pack(side='top', anchor='nw')

    def display_password_section(self):
        frame = Frame()
        Label(frame, text='Enter Password ' ,fg='#0059b3', font=("Helvetica 12 bold")).pack(side='left', padx=10)
        self.password_widget = Entry(frame, width=51, borderwidth=2,show='*')
        self.password_widget.pack(side='left', anchor='e')
        self.join_button = Button(frame, text="Join", width=10, fg='#FF0055', bg='#BAEE17', command=self.on_join).pack(side='left')
        frame.pack(side='top', anchor='nw')
        #pass_temp = self.password_widget.get()

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='Chat Box:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter message',fg='#FF8000', font=("Serif 12 bold")).pack(side='top', anchor='c')
        self.enter_text_widget = Text(frame, width=60, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

    def sigh_up(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror(
                "Enter your name", "Enter your name to send a message")
            return
        if len(self.password_widget.get()) == 0:
            messagebox.showerror(
                "Enter your pass", "Enter your password to send a message")
            return
        if  match_user(self.name_widget.get()) == True :
            messagebox.showerror("Invalid Username","This Username has been taken ")
            self.name_widget.config(state='disabled')
        else:
            put_new_client(self.name_widget.get(),self.password_widget.get())
            messagebox.showinfo("You Have Been Inrolled","Success")
    def on_join(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
        if len(self.password_widget.get()) == 0:
            messagebox.showerror(
                "Enter your pass", "Enter your password to send a message")
            return

        # print(encMessage)
        if  match_user_pass(self.name_widget.get(), self.password_widget.get()) == True :
            messagebox.showinfo("Success","Wellcom to UOK Chat Room ")
            self.name_widget.config(state='disable')
            self.client_socket.send(("joined:" + self.name_widget.get()).encode('utf-8'))
        else:
            messagebox.showerror("Password", "Please Enter Correct Password")



    def on_enter_key_pressed(self, event):
      if len(self.name_widget.get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
      self.send_chat()
      self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        senders_name = self.name_widget.get().strip() + ": "
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = (senders_name + data).encode('utf-8')
        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)

def read_file():
    file = open("data.txt", "r")
    lines = file.readlines()
    count_pass = 1
    count_user = 0
    z_f = 0
    for line in lines:
        if count_pass > 110:
            break
        if z_f % 2 == 0:
            line_user[count_user] = line.strip()
            count_user += 1
            z_f += 1
        elif z_f % 2 != 0:
            line_pass[count_pass] = line.strip()
            count_pass += 1
            z_f += 1
def match_user_pass (u , p):

    for i in range(160):
        decoded2 = cryptocode.decrypt(line_user[i], "8585")
        if u == decoded2 :
            decoded = cryptocode.decrypt(line_pass[i+1], "8585")
            if p == decoded:
                return True
def match_user (u):
    for i in range(160):
        if u == line_user[i] :
            return True
def put_new_client (u , p):
    f = open('data.txt', 'a')
    u = cryptocode.encrypt(u, "8585")
    f.write(u+'\n')
    p = cryptocode.encrypt(p , "8585")
    f.write(p+'\n')
    f.close()
#main function
if __name__ == '__main__':
    pass_temp = ""
    user_temp = ""
    line_pass = [""] * 160
    line_user = [""] * 160
    clients_list = [0] * 10
    read_file()
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
