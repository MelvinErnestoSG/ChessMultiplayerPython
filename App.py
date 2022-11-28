import tkinter as tk

# for a string to store alphabet.
import string as st

# help with importing images.
import os

# help with importing speak audio.
# pip install pyttsx3.
import pyttsx3

# help with implementing of PIL and images into GUI.
from PIL import Image, ImageTk 

# help with importing thread.
from threading import Thread

# help with importing messagebox.
from tkinter import messagebox

# import dimensions and castling.
from Const import DIMENSION,SIZE,LEFT,UP,LIGHT,DARK,WHITE

# help with importing playsound.
# pip install playsound 
from playsound import playsound 
#--------------------------------------#
# speak function.
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
# speak when the game starts.
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
Thread(target=speak("welcome!")).start()
#--------------------------------------#
# sound when are moved pieces.
def move_sound(): 
    playsound('move.wav')
#--------------------------------------#
# sound when is moved pieces.
def capture_sound(): 
    playsound('capture.wav')
#--------------------------------------#
# call sound when is moved pieces.
def play_sound_move(moved=False):
    if moved:
        move_sound()
    else:
        capture_sound()
#--------------------------------------#
# call sound when is captured pieces.
def play_sound_capture(captured=False):
    if captured:
        capture_sound()
    else:
        move_sound()

class App(tk.Frame):
    def __init__(self, parent, height, width): 
        parent.iconbitmap(os.path.join('./icon/ChessPieces.ico'))
        parent.title('Play Chess')
        parent.geometry(f'{str(SIZE*DIMENSION)}x{str(SIZE*DIMENSION)}+{LEFT}+{UP}')
        parent.resizable(False, False)
        parent.maxsize(height=780,width=780)
        parent.minsize(height=780,width=780)

        tk.Frame.__init__(self, parent) 
        self.height=height
        self.width=width
        self.config(height=100*self.height)
        self.config(width=100*self.width)
        self.config(highlightbackground=WHITE)
        self.config(highlightthickness=6)
        self.pack()
        
        # stores squares with pos as key and button as value.
        self.square_color=None
        self.squares={} 
        self.ranks=st.ascii_lowercase

        # stores images of pieces.
        self.white_images={} 
        self.black_images={}

        # for convenience when calling all white pieces.
        self.white_pieces=["pyimage1","pyimage3","pyimage4","pyimage5","pyimage6","pyimage7"]
        self.black_pieces=["pyimage8","pyimage10","pyimage11","pyimage12","pyimage13","pyimage14"]

        # button associated with used to pressed.
        self.buttons_pressed=False

        # associated with square clicked.
        self.turns=False

        # first square clicked.
        self.sq1=None 
        self.sq2=None 

        # button associated with the square clicked.
        self.sq1_button=None 
        self.sq2_button=None

        # button associated with the square light and dark
        self.piece_color=None

    # call other functions.
    def __call__(self):
        self.set_squares()
        self.set_alpha_color()
        self.set_import_pieces()
        self.set_pieces()
        self.mainloop()

    # letters and numbers above the buttons.
    def set_alpha_color(self):
        font_size=7
        letters=[
                    [' h ',' g ',' f ',' e ',' d ',' c ',' b ',' a '],
                    ['   ','   ','   ','   ','   ','   ','   ','   '],
                    ['   ','   ','   ','   ','   ','   ','   ','   '],
                    ['   ','   ','   ','   ','   ','   ','   ','   '],
                    ['   ','   ','   ','   ','   ','   ','   ','   '],
                    ['   ','   ','   ','   ','   ','   ','   ','   '],
                    ['   ','   ','   ','   ','   ','   ','   ','   '],
                    [' a ',' b ',' c ',' d ',' e ',' f ',' g ',' h '],
                ]
        for x, rows in enumerate(letters):
            for y, letters in enumerate(rows):
                self.label= tk.Label(
                                        self, 
                                        text=letters, 
                                        font=('monospace',font_size,'bold')
                                    )
                # alternates between dark/light tiles.
                if x%2==0 and y%2==0: 
                    self.label.config(foreground=DARK, background=LIGHT)
                    self.label.grid(row=x+1, column=y, sticky='ws')
                elif x%2==1 and y%2==1:
                    self.label.config(foreground=DARK, background=LIGHT)
                    self.label.grid(row=x+1, column=y, sticky='ws')
                else:
                    self.label.config(foreground=LIGHT, background=DARK)
                    self.label.grid(row=x+1, column=y, sticky='ws')

        numbers={
                    '1      8':0, 
                    '2      7':1, 
                    '3      6':2, 
                    '4      5':3, 
                    '5      4':4, 
                    '6      3':5, 
                    '7      2':6, 
                    '8      1':7,
                }
        for x, cols in enumerate(numbers):
            for y, numbers in enumerate(cols):
                self.label= tk.Label(
                                        self, 
                                        text=numbers, 
                                        font=('monospace',font_size,'bold')
                                    )
                # alternates between dark/light tiles.
                if x%2==0 and y%2==0: 
                    self.label.config(foreground=DARK, background=LIGHT)
                    self.label.grid(row=x+1, column=y, sticky='ne')
                elif x%2==1 and y%2==1:
                    self.label.config(foreground=DARK, background=LIGHT)
                    self.label.grid(row=x+1, column=y, sticky='ne')
                else:
                    self.label.config(foreground=LIGHT, background=DARK)
                    self.label.grid(row=x+1, column=y, sticky='ne')

    # called when a square button is pressed, consists of majority of the movement code.
    def select_piece(self,button): 
        #checks color of first piece
        if button["image"] in self.white_pieces and self.buttons_pressed==False: 
            self.piece_color="white"
        
        elif button["image"] in self.black_pieces and self.buttons_pressed==False:
            self.piece_color="black" 
        
        # prevents people from moving their pieces when it's not heir turn.
        if (self.piece_color=="white" and self.turns%2==0) or (self.piece_color=="black" and self.turns%2==1) or self.buttons_pressed==True:
            # stores square and button of first square selected.
            if self.buttons_pressed==False: 
                # retrieves position of piece
                self.sq1=list(self.squares.keys())[list(self.squares.values()).index(button)] 
                self.sq1_button=button
                self.buttons_pressed+=1

            # stores square and button of second square selected.
            elif self.buttons_pressed==True: 
                # retrieves position of piece
                self.sq2=list(self.squares.keys())[list(self.squares.values()).index(button)]
                self.sq2_button=button
                self.buttons_pressed-=1
                
                # prevents self-destruction and allows the user to choose a new piece.
                if self.sq2==self.sq1:
                    self.buttons_pressed=True
                    return

                # makes sure the move is legal.
                if self.allowed_piece_move() and self.friendly_fire()==False:
                    previous_sq1=self.sq1
                    previous_sq1_button_piece=self.sq1_button["image"]
                
                    previous_sq2=self.sq2
                    previous_sq2_button_piece=self.sq2_button["image"]

                    # moves piece in sq1 to sq2
                    self.squares[self.sq2].config(image=self.sq1_button["image"]) 
                    self.squares[self.sq2].image=self.sq1_button["image"]

                    # clears sq1
                    self.squares[self.sq1].config(image=self.white_images["blank.png"]) 
                    self.squares[self.sq1].image=self.white_images["blank.png"]

                    # for some reason it says king is in check after a castle - 
                    # so I set up a variable here that would prevent this code from running.
                    if self.in_check()==True and self.castled==False:
                        # reverts movement since king is 
                        # or would be put into check because of move
                        self.squares[previous_sq2].config(image=previous_sq2_button_piece) 
                        self.squares[previous_sq2].image=previous_sq2_button_piece
                        
                        self.squares[previous_sq1].config(image=previous_sq1_button_piece)
                        self.squares[previous_sq1].image=previous_sq1_button_piece
                    else:
                        self.turns+=1  
                        # checks for possible pawn promotion.                 
                        if (button["image"]=="pyimage5" and previous_sq2.count("8")==1) or (button["image"]=="pyimage12" and previous_sq2.count("1")==1):
                            self.promotion_menu(self.piece_color)
        else:
            self.buttons_pressed=True

    # creates menu to choose what piece to change the pawn to.
    def promotion_menu(self,color): 
        # function called by buttons to make the change and destroy window.
        def return_piece(piece): 
            self.squares[self.sq2].config(image=piece)
            self.squares[self.sq2].image=piece
            promoted.destroy()

        # creates a new menu with buttons depending on pawn color.
        promoted = tk.Tk() 
        promoted.title("Play Chess")
        promoted.iconbitmap(os.path.join("./icon/ChessPieces.ico"))
        promoted.geometry("+600+300")
        promoted.config(width=500, height=135, background="#000")
        promoted.resizable(0, 0)

        #https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode
        #white_figures = { 'king': '♔', 'queen': '♕', 'rook': '♖', 'bishop': '♗', 'knight': '♘', 'pawn': '♙'}
        #black_figures = { 'king': '♚', 'queen': '♛', 'rook': '♜', 'bishop': '♝', 'knight': '♞', 'pawn': '♟'}

        if color == "white":
            # triggers return_piece function when selected.
            promoted_queen = tk.Button (
                                        promoted, 
                                        text="♕",
                                        font=("monospace",45,"bold"),
                                        bg=DARK,
                                        fg="#fff",
                                        activebackground="lawn green",
                                        command=lambda: 
                                        return_piece("pyimage6")
                                    )
            promoted_queen.grid(row=0, column=0, padx=1, pady=1)

            promoted_rook = tk.Button  (
                                        promoted, 
                                        text="♖", 
                                        font=("monospace",45,"bold"),
                                        bg=DARK,
                                        fg="#fff",
                                        activebackground="lawn green",
                                        command=lambda: 
                                        return_piece("pyimage7")
                                    )
            promoted_rook.grid(row=0, column=1, padx=1, pady=1)

            promoted_bishop = tk.Button(
                                        promoted, 
                                        text="♗", 
                                        font=("monospace",45,"bold"),
                                        bg=DARK,
                                        fg="#fff",
                                        activebackground="lawn green",
                                        command=lambda: 
                                        return_piece("pyimage1")
                                    )
            promoted_bishop.grid(row=0, column=2, padx=1, pady=1)

            promoted_knight = tk.Button(
                                        promoted, 
                                        text="♘", 
                                        font=("monospace",45,"bold"),
                                        bg=DARK,
                                        fg="#fff",
                                        activebackground="lawn green",
                                        command=lambda: 
                                        return_piece("pyimage4")
                                    ) 
            promoted_knight.grid(row=0, column=3, padx=1, pady=1)

        elif color == "black":
            # triggers return piece function when selected.
            promoted_queen = tk.Button(
                                        promoted, 
                                        text="♛", 
                                        font=("monospace",45,"bold"),
                                        bg=LIGHT,
                                        fg="#000",
                                        activebackground="lawn green",
                                        command=lambda: 
                                        return_piece("pyimage13")
                                    )
            promoted_queen.grid(row=0, column=0, padx=1, pady=1)

            promoted_rook = tk.Button  (
                                        promoted, 
                                        text="♜", 
                                        font=("monospace",45,"bold"),
                                        bg=LIGHT,
                                        fg="#000",
                                        activebackground="lawn green",
                                        command=lambda: 
                                        return_piece("pyimage14")
                                    )
            promoted_rook.grid(row=0, column=1, padx=1, pady=1)

            promoted_bishop = tk.Button(
                                        promoted, 
                                        text="♝", 
                                        font=("monospace",45,"bold"),
                                        bg=LIGHT,
                                        fg="#000",
                                        activebackground="lawn green",
                                        command=lambda: 
                                        return_piece("pyimage8")
                                    )
            promoted_bishop.grid(row=0, column=2, padx=1, pady=1)

            promoted_knight = tk.Button(
                                        promoted, 
                                        text="♞", 
                                        font=("monospace",45,"bold"),
                                        bg=LIGHT,
                                        fg="#000",
                                        activebackground="lawn green",
                                        command=lambda: 
                                        return_piece("pyimage11")
                                    )
            promoted_knight.grid(row=0, column=3, padx=1, pady=1)
            promoted.mainloop()

    # show message box in the screen.
    def show_message(self):
        messagebox.showerror('Error', 'Something went wrong with your movement!')

    # prevents capturing your own pieces.    
    def friendly_fire(self): 
        piece_2_color=self.sq2_button["image"]
        if self.piece_color=="white" and piece_2_color in self.white_pieces:
            self.show_message()
            return True
        if self.piece_color=="black" and piece_2_color in self.black_pieces:
            self.show_message()
            return True
        else:
            return False

    # makes sure that the squares in between sq1 and sq2 are not occupied.
    def clear_path(self, piece): 
        if piece=="rook" or piece=="queen": 
            # for vertical movement  
            if self.sq1[0]==self.sq2[0]: 
                position1=min(int(self.sq1[1]),int(self.sq2[1]))
                position2=max(int(self.sq1[1]),int(self.sq2[1]))

                for i in range(position1+1,position2):
                    square_on_path=self.squares[self.sq1[0]+str(i)].cget("image")
                    if square_on_path!="pyimage2":
                        return False

            # for horizontal movement.      
            elif self.sq1[1]==self.sq2[1]: 
                position1=min(self.ranks.find(self.sq1[0]),self.ranks.find(self.sq2[0]))
                position2=max(self.ranks.find(self.sq1[0]),self.ranks.find(self.sq2[0]))

                for i in range(position1+1,position2):
                    square_on_path=self.squares[self.ranks[i]+self.sq1[1]].cget("image")
                    if square_on_path!="pyimage2":
                        return False

        # for diagonal movement.    
        if piece=="bishop" or piece=="queen":
            x1=self.ranks.find(self.sq1[0])
            x2=self.ranks.find(self.sq2[0])
            y1=int(self.sq1[1])
            y2=int(self.sq2[1])
            
            if y1<y2:
                if x1<x2:# NE direction.
                    for x in range(x1+1,x2):
                        y1+=1
                        square_on_path=self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path!="pyimage2":
                            return False

                if x1>x2:# NW direction.
                    for x in range(x1-1,x2,-1):
                        y1+=1
                        square_on_path=self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path!="pyimage2":
                            return False

            elif y1>y2:
                if x1<x2:# SE direction.
                    for x in range(x1+1,x2):
                        y1-=1
                        square_on_path=self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path!="pyimage2":
                            return False

                if x1>x2:# SW direction
                    for x in range(x1-1,x2,-1):
                        y1-=1
                        square_on_path=self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path!="pyimage2":
                            return False   
        return True

    # checks whether the piece can move to square 2 with respect to their movement capabilities.
    def allowed_piece_move(self): 
        # redefining pyimage for readability
        wb,wk,wn,wp,wq,wr="pyimage1","pyimage3","pyimage4","pyimage5","pyimage6","pyimage7" 
        bb,bk,bn,bp,bq,br="pyimage8","pyimage10","pyimage11","pyimage12","pyimage13","pyimage14"

        # for when this function is called for check.
        if self.sq1_button["image"]=="pyimage2" or self.sq1_button["image"]=="pyimage9":
            return False

        # king movement.
        if self.sq1_button["image"]==wk or self.sq1_button["image"]==bk:
            # allows 1 square when move.
            if (abs(int(self.sq1[1])-int(self.sq2[1]))<2) and (abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])))<2 and self.sq2_button["image"]=="pyimage2":
                play_sound_move(self)
                return True

            # allows 1 square when capture.
            if (abs(int(self.sq1[1])-int(self.sq2[1]))<2) and (abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])))<2 and self.sq2_button["image"]!="pyimage2":
                play_sound_capture(self)
                return True

        # movement of the castle to white in long shape.
            if self.sq1_button["image"]==wk and self.sq2=="c1": 
                play_sound_move(self)
                # checks to see if squares in between rook and king 
                # are empty and are not a possible move for opponent.
                for x in range(1,4): 
                    square_button = self.squares[self.ranks[x]+str(1)]
                    if square_button["image"]!="pyimage2":
                        return False
                    self.squares["a1"].config(image="pyimage2")
                    self.squares["a1"].image="pyimage2"
                    self.squares["d1"].config(image="pyimage7")
                    self.squares["d1"].image=("pyimage7")
                    return True

        # movement of the castle to white in short form.
            if self.sq1_button["image"]==wk and self.sq2=="g1":
                play_sound_move(self)
                # checks to see if squares in between rook and king 
                # are empty and are not a possible move for opponent.
                for x in range(5,7):
                    square_button = self.squares[self.ranks[x]+str(1)]
                    if square_button["image"]!="pyimage2":
                        return False
                    self.squares["h1"].config(image="pyimage2")
                    self.squares["h1"].image="pyimage2"
                    self.squares["f1"].config(image="pyimage7")
                    self.squares["f1"].image=("pyimage7")
                    return True

        # movement of the castle to black in long form.
            if self.sq1_button["image"]==bk and self.sq2=="c8":
                play_sound_move(self)
                # checks to see if squares in between rook and king 
                # are empty and are not a possible move for opponent.
                for x in range(1,3):
                    square_button = self.squares[self.ranks[x]+str(8)]
                    if square_button["image"] != "pyimage2":
                        return False
                    self.squares["a8"].config(image="pyimage2")
                    self.squares["a8"].image="pyimage2"
                    self.squares["d8"].config(image="pyimage14")
                    self.squares["d8"].image=("pyimage14")
                    return True

        # movement of the castle to black in short form.
            if self.sq1_button["image"]==bk and self.sq2=="g8":
                play_sound_move(self)
                # checks to see if squares in between rook and king 
                # are empty and are not a possible move for opponent.
                for x in range(5,7): 
                    square_button = self.squares[self.ranks[x]+str(8)]
                    if square_button["image"]!="pyimage2":
                        return False
                    self.squares["h8"].config(image="pyimage2")
                    self.squares["h8"].image="pyimage2"
                    self.squares["f8"].config(image="pyimage14")
                    self.squares["f8"].image=("pyimage14")
                    return True

        # queen movement.
        if (self.sq1_button["image"]==wq or self.sq1_button["image"]==bq) and self.clear_path("queen"):
            # makes sure there is equal change between file and rank movement.
            # allows the moving of pieces as rook.
            if int(self.sq1[1])==int(self.sq2[1]) and self.sq2_button["image"]=="pyimage2" or self.sq1[0]==self.sq2[0] and self.sq2_button["image"]=="pyimage2": 
                play_sound_move(self)
                return True

            # allows the capturing of pieces as rook.
            if int(self.sq1[1])==int(self.sq2[1]) and self.sq2_button["image"]!="pyimage2" or self.sq1[0]==self.sq2[0] and self.sq2_button["image"]!="pyimage2": 
                play_sound_capture(self)
                return True

            # allows the moving of pieces as bishop.
            if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                play_sound_move(self)
                return True

            # allows the capturing of pieces as bishop.
            if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])):
                play_sound_capture(self)
                return True

        # bishop movement.     
        if (self.sq1_button["image"]==wb or self.sq1_button["image"]==bb) and self.clear_path("bishop"):
            # makes sure there is equal change between file and rank movement.
            # allows the moving of pieces as bishop.
            if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2": 
                play_sound_move(self)
                return True

            # allows the capturing of pieces as bishop.
            if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])): 
                play_sound_capture(self)
                return True

        # knight movement.
        if self.sq1_button["image"]==wn or self.sq1_button["image"]==bn:
            # allows tall L moves if there is not an opponent piece there.
            if (abs(int(self.sq1[1])-int(self.sq2[1]))==2) and (abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0]))==1) and self.sq2_button["image"]=="pyimage2":
                play_sound_move(self)
                return True

            # allows tall L moves if there is an opponent piece there can make the capture.
            if (abs(int(self.sq1[1])-int(self.sq2[1]))==2) and (abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0]))==1) and self.sq2_button["image"]!="pyimage2":
                play_sound_capture(self)
                return True

            # allows wide L moves if there is not an opponent piece there.
            if (abs(int(self.sq1[1])-int(self.sq2[1]))==1) and (abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0]))==2) and self.sq2_button["image"]=="pyimage2": 
                play_sound_move(self)
                return True

            # allows wide L moves if there is not an opponent piece there can make the capture.
            if (abs(int(self.sq1[1])-int(self.sq2[1]))==1) and (abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0]))==2) and self.sq2_button["image"]!="pyimage2": 
                play_sound_capture(self)
                return True

        # rook movement.
        if (self.sq1_button["image"]==wr or self.sq1_button["image"]==br) and self.clear_path("rook"): 
            # only allows movement within same rank or file.
            # allows the moving of pieces as rook.
            if int(self.sq1[1])==int(self.sq2[1]) and self.sq2_button["image"]=="pyimage2" or self.sq1[0]==self.sq2[0] and self.sq2_button["image"]=="pyimage2":
                play_sound_move(self)
                return True
            
            # allows the capturing of pieces as rook.
            if int(self.sq1[1])==int(self.sq2[1]) and self.sq2_button["image"]!="pyimage2" or self.sq1[0]==self.sq2[0] and self.sq2_button["image"]!="pyimage2":
                play_sound_capture(self)
                return True

        # white pawn movement.
        if self.sq1_button["image"]==wp:
            # allows for 2 space jump from starting position.
            if "2" in self.sq1: 
                # allows 2 sq movement.
                if int(self.sq1[1])+1==int(self.sq2[1]) or int(self.sq1[1])+2==int(self.sq2[1]) and self.sq1[0]==self.sq2[0] and self.sq2_button["image"]=="pyimage2":
                    # makes sure that there is no piece blocking path.
                    in_front=self.squares[self.sq1[0]+str(int(self.sq1[1])+1)]
                    if in_front["image"]=="pyimage2": 
                        play_sound_move(self)
                        return True

            # allows 1 sq movement.           
            if int(self.sq1[1])+1==int(self.sq2[1]) and self.sq1[0]==self.sq2[0] and self.sq2_button["image"]=="pyimage2":
                play_sound_move(self)
                return True

            # allows the capturing of diagonal pieces if there is an opponent piece there.
            if int(self.sq1[1])+1==int(self.sq2[1]) and abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0]))==1 and self.sq2_button["image"]!="pyimage2":
                play_sound_capture(self)
                return True

        # black pawn movement.
        if self.sq1_button["image"]==bp: 
            # allows for 2 space jump from starting position.
            if "7" in self.sq1: 
                # only allows it to move straight 1 or 2 sql.
                if int(self.sq1[1])==int(self.sq2[1])+1 or int(self.sq1[1])==int(self.sq2[1])+2 and self.sq1[0]==self.sq2[0] and self.sq2_button["image"]=="pyimage2":
                    # makes sure that there is no piece blocking path.
                    in_front=self.squares[self.sq1[0]+str(int(self.sq1[1])+1)]
                    if in_front["image"]!="pyimage2": 
                        play_sound_move(self)
                        return True
            
            # allows 1 sq movement.
            if int(self.sq1[1])==int(self.sq2[1])+1 and self.sq1[0]==self.sq2[0] and self.sq2_button["image"]=="pyimage2":
                play_sound_move(self)
                return True

            # allows the capturing of diagonal pieces if there is an opponent piece there.
            if int(self.sq1[1])==int(self.sq2[1])+1 and abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0]))==1 and self.sq2_button["image"]!="pyimage2":
                play_sound_capture(self)
                return True

    # prevents a move if king is under attack.
    def in_check(self): 
        # stores current values assigned to values.
        previous_sq1=self.sq1 
        previous_sq1_button=self.sq1_button

        previous_sq2=self.sq2
        previous_sq2_button=self.sq2_button
        
        def return_previous_values():
            self.sq1=previous_sq1
            self.sq1_button=previous_sq1_button

            self.sq2=previous_sq2
            self.sq2_button=previous_sq2_button
            
        if self.piece_color=="white":
            # calls find_king function to find position of king.
            self.sq2=self.find_king("pyimage3")
            # iterates through each square.
            for key in self.squares: 
                self.sq1=key
                self.sq1_button=self.squares[self.sq1]
                if self.sq1_button["image"] in self.black_pieces:
                    # checks to see if the king's current position is a possible move for the piece.
                    if self.allowed_piece_move(): 
                        speak("invalid move")
                        return True

        if self.piece_color=="black":
            # calls find_king function to find position of king.
            self.sq2=self.find_king("pyimage10")
            # iterates through each square
            for key in self.squares:
                self.sq1=key
                self.sq1_button=self.squares[self.sq1] 
                if self.sq1_button["image"] in self.white_pieces:
                    # checks to see if the king's current position is a possible move for the piece.
                    if self.allowed_piece_move():
                        speak("invalid move")
                        return True

        return_previous_values()
        return False

    # finds the square where the king is currently on.
    def find_king(self,king):
        for square in self.squares:
            button=self.squares[square]
            if button["image"]==king:
                return square

    # fills frame with buttons representing squares.
    def set_squares(self): 
        for x in range(DIMENSION):
            for y in range(DIMENSION):
                # alternates between dark/light tiles.
                if x%2==0 and y%2==0: 
                    self.square_color=DARK
                elif x%2==1 and y%2==1:
                    self.square_color=DARK
                else:
                    self.square_color=LIGHT

                buttons = tk.Button(
                                        self,  
                                        bg=self.square_color, 
                                        bd=False, 
                                        width=94,
                                        height=94,
                                        activebackground=self.square_color,
                                    )
                buttons.grid(row=8-x, column=y)
                position=self.ranks[y]+str(x+1)
                self.squares.setdefault(position,buttons) 

                # creates list of square positions.
                self.squares[position].config(
                                            command=lambda 
                                            key=self.squares[position]: 
                                            self.select_piece(key)
                                        )

    # opens and stores images of pieces and prepares
    # the pieces for the game for both sides.
    def set_import_pieces(self):
        # stores white pieces images into dicts.
        path=os.path.join(os.path.dirname(__file__),"white") 
        w_dirs=os.listdir(path)
        for file in w_dirs:
            img=Image.open(path+"\\"+file)
            img=img.resize((80,80))
            img=ImageTk.PhotoImage(image=img)
            self.white_images.setdefault(file,img)

        # stores black pieces images into dicts.
        path=os.path.join(os.path.dirname(__file__),"black") 
        b_dirs=os.listdir(path)
        for file in b_dirs:
            img=Image.open(path+"\\"+file)
            img=img.resize((80,80))
            img=ImageTk.PhotoImage(image=img)
            self.black_images.setdefault(file,img)

    # places pieces in starting positions.
    def set_pieces(self): 
        # assigning positions with their default pieces.
        dict_rank1_pieces = {
                                "a1":"r.png", 
                                "b1":"n.png", 
                                "c1":"b.png", 
                                "d1":"q.png", 
                                "e1":"k.png", 
                                "f1":"b.png", 
                                "g1":"n.png", 
                                "h1":"r.png",
                            }

        dict_rank2_pieces = {
                                "a2":"p.png", 
                                "b2":"p.png", 
                                "c2":"p.png", 
                                "d2":"p.png", 
                                "e2":"p.png", 
                                "f2":"p.png", 
                                "g2":"p.png", 
                                "h2":"p.png",
                            }    

        dict_rank7_pieces = {
                                "a7":"p.png", 
                                "b7":"p.png", 
                                "c7":"p.png", 
                                "d7":"p.png", 
                                "e7":"p.png", 
                                "f7":"p.png", 
                                "g7":"p.png", 
                                "h7":"p.png",
                            }

        dict_rank8_pieces = {
                                "a8":"r.png", 
                                "b8":"n.png", 
                                "c8":"b.png", 
                                "d8":"q.png", 
                                "e8":"k.png", 
                                "f8":"b.png", 
                                "g8":"n.png", 
                                "h8":"r.png",
                            }

        # inserts images into buttons.
        for key in dict_rank1_pieces:
            starting_piece=dict_rank1_pieces[key]
            self.squares[key].config(image=self.white_images[starting_piece])
            self.squares[key].image=self.white_images[starting_piece]
            
        for key in dict_rank2_pieces:
            starting_piece=dict_rank2_pieces[key]
            self.squares[key].config(image=self.white_images[starting_piece])
            self.squares[key].image=self.white_images[starting_piece]

        for key in dict_rank7_pieces:
            starting_piece=dict_rank7_pieces[key]
            self.squares[key].config(image=self.black_images[starting_piece])
            self.squares[key].image=self.black_images[starting_piece]
            
        for key in dict_rank8_pieces:
            starting_piece=dict_rank8_pieces[key]
            self.squares[key].config(image=self.black_images[starting_piece])
            self.squares[key].image=self.black_images[starting_piece]

        # fill rest with blank pieces.
        for rank in range(3,7): 
            for file in range(DIMENSION):
                starting_piece="blank.png"
                position=self.ranks[file]+str(rank)
                self.squares[position].config(image=self.white_images[starting_piece])
                self.squares[position].image=self.white_images[starting_piece]

# creates main window with the board and creates board object.
root=tk.Tk()
root=App(root,DIMENSION,DIMENSION)
root()