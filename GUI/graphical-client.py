import socket
import threading
from tkinter import *
from tkinter import ttk

# Constants
FORMAT = 'utf-8'
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# The GUI class
class User_interface:
    # Constructor
    def __init__(self) -> None:
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login To Chat")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=500,
                             height=600)
        # create a Label
        self.pls = Label(self.login,
                         text="Sign in to proceed",
                         justify=CENTER,
                         font=("Courier", 14, "bold"))

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text="Username: ",
                               font=("Courier", 12))

        self.labelName.place(relheight=0.3,
                             relx=0.2,
                             rely=0.2)

        # Input box for the name
        self.entryName = Entry(self.login,
                               font=("Courier", 14))

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.5,
                             rely=0.3)

        # set the focus of the cursor
        self.entryName.focus()

        # Continue Button to go to the chat window
        self.go = Button(self.login,
                         text="PROCEED",
                         font=("Courier", 14, "bold"),
                         command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4,
                      rely=0.55)

        # The mainloop of the program from tkinter
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        # the thread to receive messages
        receiver = threading.Thread(target=self.receive)
        receiver.start()

    # The main chat window layout
    # The main layout of the chat
    def layout(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=600,
                              height=700,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font=("Courier", 13, "bold"),
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font=("Courier", 14),
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font=("Courier", 13))

        # place the given widget approximately in the middle
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font=("Courier", 10, "bold"),
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        # create a Quit Button
        self.buttonQuit = Button(self.labelBottom,
                                 text="Quit",
                                 font=("Courier", 10, "bold"),
                                 width=20,
                                 bg="#ABB2B9",
                                 command=self.quitApplication)

        self.buttonQuit.place(relx=0.6,
                              rely=0.008,
                              relheight=0.06,
                              relwidth=0.15)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the given widget approximately in the middle
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

        # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=NORMAL)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
        self.textCons.config(state=DISABLED)

    # Allow clients to receive messages in chatroom
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)

                # Send the client's name from the server
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message+"\n\n")

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occurred!")
                self.quitApplication()
                break

    # Send the message to the chatroom
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))
            break

    # Quit the application and close the socket connection
    def quitApplication(self):
        client.close()
        self.Window.destroy()

# Set the theme to 'clam' for a modern look
ttk.Style().theme_use('clam')

# Create an instance of the User_interface class
ui = User_interface()
