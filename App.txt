import tkinter as tk

# For a string to store alphabet.
import string

# Help with importing images.
import os

# Help with importing speak audio.
import pyttsx3 # pip install pyttsx3

# Help with implementing of PIL and images into GUI.
from PIL import Image, ImageTk 

# Help with importing thread.
from threading import Thread

# Help with importing message box.
from tkinter import messagebox

# For board dimensions.
DIMENSION=8

# For size screen.
SIZE=100

# For center screen.
LEFT=400
UP=5

# For colors squares.
LIGHT="burlywood1"
DARK="tan4"

# For color highlight background.
WHITE='#fff'

# Help with importing playsound.
from playsound import playsound # pip install playsound 

# Speak function when the game starts.
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
Thread(target=speak("welcome!")).start()

# Sounds when are captured a piece or moved a piece.
def capture_sound(): 
    playsound('capture.wav')

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

        # Stores squares with position as key and button as value.
        self.square_color=None
        self.squares={} 
        self.ranks=string.ascii_lowercase

        # Stores images of pieces.
        self.white_images={} 
        self.black_images={}

        # For convenience when calling all white pieces.
        self.white_pieces=["pyimage1","pyimage3","pyimage4","pyimage5","pyimage6","pyimage7"]
        self.black_pieces=["pyimage8","pyimage10","pyimage11","pyimage12","pyimage13","pyimage14"]

        # Button associated with used to pressed.
        self.buttons_pressed=False

        # Associated with square clicked.
        self.turns=False

        # First square clicked.
        self.sq1=None 
        self.sq2=None 

        # Button associated with the square clicked.
        self.sq1_button=None 
        self.sq2_button=None

        # Button associated with the squares light and dark.
        self.piece_color=None

        # For castling.
        self.castled=False

    # For call some functions.
    def __call__(self):
        self.set_squares()
        self.import_pieces()
        self.set_pieces()
        self.mainloop()

    # Called when a square button is pressed, consists of majority of the movement code.
    def select_piece(self,button): 
        # Checks color of first pieces.
        if button["image"] in self.white_pieces and self.buttons_pressed==False:
            self.piece_color="white"
        # Checks color of second pieces.
        elif button["image"] in self.black_pieces and self.buttons_pressed==False:
            self.piece_color="black"      

        # Prevents people from moving their pieces when it's not their turn.
        if (self.piece_color=="white" and self.turns%2==0) or (self.piece_color=="black" and self.turns%2==1) or self.buttons_pressed==True:
            # Stores square and button of first square selected.
            if self.buttons_pressed==False: 
                # Retrieves position of piece.
                self.sq1=list(self.squares.keys())[list(self.squares.values()).index(button)] 
                self.sq1_button=button
                self.buttons_pressed+=1

            # Stores square and button of second square selected.
            elif self.buttons_pressed==True: 
                # Retrieves position of piece.
                self.sq2=list(self.squares.keys())[list(self.squares.values()).index(button)]
                self.sq2_button=button
                self.buttons_pressed-=1

                # Prevents self destruction and allows the user to choose a new piece.
                if self.sq2==self.sq1:
                    self.buttons_pressed=False
                    return

                # Makes sure the move is legal.
                if self.allowed_piece_move() and self.friendly_fire()==False:
                    previous_sq1=self.sq1
                    previous_sq1_button_piece=self.sq1_button["image"]
                
                    previous_sq2=self.sq2
                    previous_sq2_button_piece=self.sq2_button["image"]

                    # Moves piece in sq1 to sq2
                    self.squares[self.sq2].config(image=self.sq1_button["image"]) 
                    self.squares[self.sq2].image=self.sq1_button["image"]

                    # Clears sq1
                    self.squares[self.sq1].config(image=self.white_images["blank.png"]) 
                    self.squares[self.sq1].image=self.white_images["blank.png"]

                    # For some reason it says king is in check after a castle - 
                    # so I set up a variable here that would prevent this code from running.
                    if self.in_check()==True and self.castled==False:
                        # Reverts movement since king is or would be put into check because of move.
                        self.squares[previous_sq2].config(image=previous_sq2_button_piece) 
                        self.squares[previous_sq2].image=previous_sq2_button_piece
                        
                        self.squares[previous_sq1].config(image=previous_sq1_button_piece)
                        self.squares[previous_sq1].image=previous_sq1_button_piece
                    else:
                        self.turns+=1  
                        # For one possible white pawn promotion in Queen.           
                        if (button["image"]=="pyimage5" and previous_sq2.count("8")==1):
                            self.squares[self.sq2].config(image="pyimage6")
                            self.squares[self.sq2].image="pyimage6"

                        # For one possible black pawn promotion in Queen. 
                        if (button["image"]=="pyimage12" and previous_sq2.count("1")==1):
                            self.squares[self.sq2].config(image="pyimage13")
                            self.squares[self.sq2].image="pyimage13"
                        else:
                            capture_sound()
        else:
            return True

    # Prevents capturing your own pieces.    
    def friendly_fire(self): 
        piece_2_color=self.sq2_button["image"]
        if self.piece_color=="white" and piece_2_color in self.white_pieces:
            return True
        if self.piece_color=="black" and piece_2_color in self.black_pieces:
            return True
        else:
            return False

    # Makes sure that the squares in between sq1 and sq2 aren't occupied.
    def clear_path(self,piece): 
        if piece=="rook" or piece=="queen":  
            # For vertical movement. 
            if self.sq1[0]==self.sq2[0]: 
                position1=min(int(self.sq1[1]),int(self.sq2[1]))
                position2=max(int(self.sq1[1]),int(self.sq2[1]))
                for i in range(position1+1,position2):
                    square_on_path=self.squares[self.sq1[0]+str(i)].cget("image")
                    if square_on_path!="pyimage2":
                        return False

            # For horizontal movement.       
            elif self.sq1[1]==self.sq2[1]: 
                position1=min(self.ranks.find(self.sq1[0]),self.ranks.find(self.sq2[0]))
                position2=max(self.ranks.find(self.sq1[0]),self.ranks.find(self.sq2[0]))

                for i in range(position1+1,position2):
                    square_on_path=self.squares[self.ranks[i]+self.sq1[1]].cget("image")
                    if square_on_path!="pyimage2":
                        return False

        # For diagonal movement.        
        if piece=="bishop" or piece=="queen": 
            x1=self.ranks.find(self.sq1[0])
            x2=self.ranks.find(self.sq2[0])
            y1=int(self.sq1[1])
            y2=int(self.sq2[1])
            if y1<y2:
                # NE direction.
                if x1<x2:
                    for x in range(x1+1,x2):
                        y1+=1
                        square_on_path=self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path!="pyimage2":
                            return False
                # NW direction.
                elif x1>x2:
                    for x in range(x1-1,x2,-1):
                        y1+=1
                        square_on_path=self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path!="pyimage2":
                            return False
            elif y1>y2:
                # SE direction.
                if x1<x2:
                    for x in range(x1+1,x2):
                        y1-=1
                        square_on_path=self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path!="pyimage2":
                            return False
                # SW direction.
                if x1>x2:
                    for x in range(x1-1,x2,-1):
                        y1-=1
                        square_on_path=self.squares[self.ranks[x]+str(y1)].cget("image")
                        if square_on_path!="pyimage2":
                            return False
        return True
                
    # Checks whether the piece can move to square 2 with respect to their movement capabilities.
    def allowed_piece_move(self): 
        # Redefining pyimage for readability.
        wb,wk,wn,wp,wq,wr="pyimage1","pyimage3","pyimage4","pyimage5","pyimage6","pyimage7" 
        bb,bk,bn,bp,bq,br="pyimage8","pyimage10","pyimage11","pyimage12","pyimage13","pyimage14"

        # For when this function is called for check.
        if self.sq1_button["image"]=="pyimage2" or self.sq1_button["image"]=="pyimage9":
            return False

        # King movement.
        if self.sq1_button["image"]==wk or self.sq1_button["image"]==bk:
            # Allows 1 square when move.
            if (abs(int(self.sq1[1])-int(self.sq2[1]))<2) and (abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])))<2:
                return True

        # Castle movement to white in long form.
        if self.sq1_button["image"]==wk and self.sq2=="c1": 
            # Checks to see if squares in between rook and king 
            # are empty and are not a possible move for opponent.
            for x in range(1,4): 
                square_button=self.squares[self.ranks[x]+str(1)]
                if square_button["image"]!="pyimage2":
                    return False
                self.squares["a1"].config(image="pyimage2")
                self.squares["a1"].image="pyimage2"
                self.squares["d1"].config(image="pyimage7")
                self.squares["d1"].image=("pyimage7")
                self.castled=False
                return True

        # Castle movement to white in short form.
        if self.sq1_button["image"]==wk and self.sq2=="g1":
            # Checks to see if squares in between rook and king 
            # are empty and are not a possible move for opponent.
            for x in range(5,7):
                square_button=self.squares[self.ranks[x]+str(1)]
                if square_button["image"]!="pyimage2":
                    return False
                self.squares["h1"].config(image="pyimage2")
                self.squares["h1"].image="pyimage2"
                self.squares["f1"].config(image="pyimage7")
                self.squares["f1"].image=("pyimage7")
                self.castled=False
                return True

        # Castle movement to black in long form.
        if self.sq1_button["image"]==bk and self.sq2=="c8":
            # Checks to see if squares in between rook and king 
            # are empty and are not a possible move for opponent.
            for x in range(1,3):
                square_button=self.squares[self.ranks[x]+str(8)]
                if square_button["image"]!="pyimage2":
                    return False
                self.squares["a8"].config(image="pyimage2")
                self.squares["a8"].image="pyimage2"
                self.squares["d8"].config(image="pyimage14")
                self.squares["d8"].image=("pyimage14")
                self.castled=False
                return True

        # Castle movement to black in short form.
        if self.sq1_button["image"]==bk and self.sq2=="g8":
            # Checks to see if squares in between rook and king 
            # are empty and are not a possible move for opponent.
            for x in range(5,7): 
                square_button=self.squares[self.ranks[x]+str(8)]
                if square_button["image"]!="pyimage2":
                    return False
                self.squares["h8"].config(image="pyimage2")
                self.squares["h8"].image="pyimage2"
                self.squares["f8"].config(image="pyimage14")
                self.squares["f8"].image=("pyimage14")
                self.castled=False
                return True

        # Queen movement.
        if (self.sq1_button["image"]==wq or self.sq1_button["image"]==bq) and self.clear_path("queen"):
            # Allows the moving and the capturing of pieces as rook.
            if int(self.sq1[1])==int(self.sq2[1]) or self.sq1[0]==self.sq2[0]: 
                return True

            # Allows the moving and the capturing of pieces as bishop.
            if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])):
                return True

        # Bishop movement.     
        if (self.sq1_button["image"]==wb or self.sq1_button["image"]==bb) and self.clear_path("bishop"):
            # Allows the moving and the capturing of pieces as bishop.
            if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])): 
                return True

        # Knight movement.
        if self.sq1_button["image"]==wn or self.sq1_button["image"]==bn:
            # Allows tall L moves if there is not an opponent piece there.
            if (abs(int(self.sq1[1])-int(self.sq2[1]))==2) and (abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0]))==1):
                return True

            # Allows wide L moves if there is not an opponent piece there.
            if (abs(int(self.sq1[1])-int(self.sq2[1]))==1) and (abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0]))==2): 
                return True

        # Rook movement.
        if (self.sq1_button["image"]==wr or self.sq1_button["image"]==br) and self.clear_path("rook"): 
            # Allows the moving and the capturing of pieces as rook.
            if int(self.sq1[1])==int(self.sq2[1]) or self.sq1[0]==self.sq2[0]:
                return True

        # White pawn movement.
        if self.sq1_button["image"]==wp:
            # allows for 2 space jump from starting position.
            if "2" in self.sq1: 
                # allows 2 sq movement.
                if int(self.sq1[1])+1==int(self.sq2[1]) or int(self.sq1[1])+2==int(self.sq2[1]) and self.sq1[0]==self.sq2[0] and self.sq2_button["image"]=="pyimage2":
                    # Makes sure that there is no piece blocking path.
                    in_front=self.squares[self.sq1[0]+str(int(self.sq1[1])+1)]
                    if in_front["image"]=="pyimage2": 
                        return True

            # Allows 1 sq movement.           
            if int(self.sq1[1])+1==int(self.sq2[1]) and self.sq1[0]==self.sq2[0] and self.sq2_button["image"]=="pyimage2":
                return True

            # Allows the capturing of diagonal pieces if there is an opponent piece there.
            if int(self.sq1[1])+1==int(self.sq2[1]) and abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0]))==1 and self.sq2_button["image"]!="pyimage2":
                return True
    
            # Allows the moving of en passant from a5 to b5.
            if "a5" in self.sq1=="a5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["b5"].config(image="pyimage2")
                    self.squares["b5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from b5 to a5.
            if "b5" in self.sq1=="b5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["a5"].config(image="pyimage2")
                    self.squares["a5"].image="pyimage2"
                    self.squares["c5"].config(image="pyimage2")
                    self.squares["c5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from b5 to c5.
            if "b5" in self.sq1=="b5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["c5"].config(image="pyimage2")
                    self.squares["c5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from c5 to b5.
            if "c5" in self.sq1=="c5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["d5"].config(image="pyimage2")
                    self.squares["d5"].image="pyimage2"
                    self.squares["b5"].config(image="pyimage2")
                    self.squares["b5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from c5 to d5.
            if "c5" in self.sq1=="c5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["b5"].config(image="pyimage2")
                    self.squares["b5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from d5 to c5.
            if "d5" in self.sq1=="d5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["c5"].config(image="pyimage2")
                    self.squares["c5"].image="pyimage2"
                    self.squares["e5"].config(image="pyimage2")
                    self.squares["e5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from d5 to c5.
            if "d5" in self.sq1=="d5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["e5"].config(image="pyimage2")
                    self.squares["e5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from e5 to f5.
            if "e5" in self.sq1=="e5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["d5"].config(image="pyimage2")
                    self.squares["d5"].image="pyimage2"
                    self.squares["f5"].config(image="pyimage2")
                    self.squares["f5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from e5 to f5.
            if "e5" in self.sq1=="e5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["f5"].config(image="pyimage2")
                    self.squares["f5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from f5 to e5.
            if "f5" in self.sq1=="f5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["e5"].config(image="pyimage2")
                    self.squares["e5"].image="pyimage2"
                    self.squares["g5"].config(image="pyimage2")
                    self.squares["g5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from f5 to g5.
            if "f5" in self.sq1=="f5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["g5"].config(image="pyimage2")
                    self.squares["g5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from g5 to f5.
            if "g5" in self.sq1=="g5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["f5"].config(image="pyimage2")
                    self.squares["f5"].image="pyimage2"
                    self.squares["h5"].config(image="pyimage2")
                    self.squares["h5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from f5 to g5.
            if "g5" in self.sq1=="g5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["h5"].config(image="pyimage2")
                    self.squares["h5"].image="pyimage2"
                    return True

            # Allows the moving of en passant from h5 to g5.
            if "h5" in self.sq1=="h5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["g5"].config(image="pyimage2")
                    self.squares["g5"].image="pyimage2"
                    return True

        # black pawn movement.
        if self.sq1_button["image"]==bp: 
            # Allows for 2 space jump from starting position.
            if "7" in self.sq1: 
                # Only allows it to move straight 1 or 2 sql.
                if int(self.sq1[1])==int(self.sq2[1])+1 or int(self.sq1[1])==int(self.sq2[1])+2 and self.sq1[0]==self.sq2[0] and self.sq2_button["image"]=="pyimage2":
                    # Makes sure that there is no piece blocking path.
                    in_front=self.squares[self.sq1[0]+str(int(self.sq1[1])+1)]
                    if in_front["image"]!="pyimage2": 
                        return True
            
            # Allows 1 sq movement.
            if int(self.sq1[1])==int(self.sq2[1])+1 and self.sq1[0]==self.sq2[0] and self.sq2_button["image"]=="pyimage2":
                return True

            # Allows the capturing of diagonal pieces if there is an opponent piece there.
            if int(self.sq1[1])==int(self.sq2[1])+1 and abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0]))==1 and self.sq2_button["image"]!="pyimage2":
                return True

            # Allows the moving of en passant from a4 to b4.
            if "a4" in self.sq1!="a5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["b4"].config(image="pyimage2")
                    self.squares["b4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from b4 to a4.
            if "b4" in self.sq1!="b5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["a4"].config(image="pyimage2")
                    self.squares["a4"].image="pyimage2"
                    self.squares["c4"].config(image="pyimage2")
                    self.squares["c4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from b4 to c4.
            if "b4" in self.sq1!="b5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["c4"].config(image="pyimage2")
                    self.squares["c4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from c4 to d4.
            if "c4" in self.sq1!="c5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["d4"].config(image="pyimage2")
                    self.squares["d4"].image="pyimage2"
                    self.squares["b4"].config(image="pyimage2")
                    self.squares["b4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from c4 to b4.
            if "c4" in self.sq1!="c5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["b4"].config(image="pyimage2")
                    self.squares["b4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from d4 to c4.
            if "d4" in self.sq1!="d5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["c4"].config(image="pyimage2")
                    self.squares["c4"].image="pyimage2"
                    self.squares["e4"].config(image="pyimage2")
                    self.squares["e4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from d4 to e4.
            if "d4" in self.sq1!="d5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["e4"].config(image="pyimage2")
                    self.squares["e4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from e4 to f4.
            if "e4" in self.sq1!="e5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["d4"].config(image="pyimage2")
                    self.squares["d4"].image="pyimage2"
                    self.squares["f4"].config(image="pyimage2")
                    self.squares["f4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from e4 to f4.
            if "e4" in self.sq1!="e5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["f4"].config(image="pyimage2")
                    self.squares["f4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from f4 to e4.
            if "f4" in self.sq1!="f5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["e4"].config(image="pyimage2")
                    self.squares["e4"].image="pyimage2"
                    self.squares["g4"].config(image="pyimage2")
                    self.squares["g4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from f4 to g4.
            if "f4" in self.sq1!="f5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["g4"].config(image="pyimage2")
                    self.squares["g4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from g4 to f4.
            if "g4" in self.sq1!="g5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["f4"].config(image="pyimage2")
                    self.squares["f4"].image="pyimage2"
                    self.squares["h4"].config(image="pyimage2")
                    self.squares["h4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from g4 to h4.
            if "g4" in self.sq1!="g5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["h4"].config(image="pyimage2")
                    self.squares["h4"].image="pyimage2"
                    return True

            # Allows the moving of en passant from h4 to g4.
            if "h4" in self.sq1!="h5":
                if abs(int(self.sq1[1])-int(self.sq2[1]))==abs(self.ranks.find(self.sq1[0])-self.ranks.find(self.sq2[0])) and self.sq2_button["image"]=="pyimage2":
                    self.squares["g4"].config(image="pyimage2")
                    self.squares["g4"].image="pyimage2"
                    return True

    # Show a message in the screen when is in check.
    def invalid_move(self):
        messagebox.showerror('Error','Something went wrong with your movement!')

    # Prevents a move if king is under attack.
    def in_check(self): 
        # Stores current values assigned to values.
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
            # Calls find king function to find position of king.
            self.sq2=self.find_king("pyimage3") 
            # Iterates through each square.
            for key in self.squares: 
                self.sq1=key
                self.sq1_button=self.squares[self.sq1]
                if self.sq1_button["image"] in self.black_pieces:
                    # Checks to see if the king's current position 
                    # is a possible move for the piece.
                    if self.allowed_piece_move():
                        self.invalid_move()
                        return True

        if self.piece_color=="black":
            # Calls find king function to find position of king.
            self.sq2=self.find_king("pyimage10")
            # Iterates through each square.
            for key in self.squares:
                self.sq1=key
                self.sq1_button=self.squares[self.sq1] 
                if self.sq1_button["image"] in self.white_pieces:
                    # Checks to see if the king's current position 
                    # is a possible move for the piece.
                    if self.allowed_piece_move():
                        self.invalid_move()
                        return True

        return_previous_values()
        return False
    
    # Finds the square where the king is currently on.
    def find_king(self,king):
        for square in self.squares:
            button=self.squares[square]
            if button["image"]==king:
                return square

    # Fills frame with buttons representing squares.
    def set_squares(self): 
        for x in range(DIMENSION):
            for y in range(DIMENSION):
                # Alternates between dark/light tiles.
                if x%2==0 and y%2==0: 
                    self.square_color=DARK
                elif x%2==1 and y%2==1:
                    self.square_color=DARK
                else:
                    self.square_color=LIGHT

                buttons=tk.Button(
                                    self, 
                                    bg=self.square_color,
                                    bd=False, 
                                    width=94,
                                    height=94,
                                    activebackground=self.square_color,
                                )
                buttons.grid(row=DIMENSION-x,column=y)
                position=self.ranks[y]+str(x+1)
                self.squares.setdefault(position,buttons) 

                # Creates list of square positions.
                self.squares[position].config(
                                            command=lambda 
                                            key=self.squares[position]: 
                                            self.select_piece(key)
                                        )
        self.set_alpha_colors()

    # Letters and numbers above of the buttons.
    def set_alpha_colors(self):
        font_size=7
        # Letters above of the buttons.
        letters=[
                    ['a','b','c','d','e','f','g','h']
                ]
        for x, rows in enumerate(letters):
            for y, letters in enumerate(rows):
                self.letters_row=tk.Label(
                                        self, 
                                        text=letters, 
                                        font=('monospace',font_size,'bold')
                                    )
                # Alternates between dark/light tiles
                if x%2==0 and y%2==0: 
                    self.letters_row.config(foreground=LIGHT,background=DARK)
                elif x%2==1 and y%2==1:
                    self.letters_row.config(foreground=LIGHT,background=DARK)
                else:
                    self.letters_row.config(foreground=DARK,background=LIGHT)

                self.letters_row.grid(row=DIMENSION-x,column=y,sticky='ws')
                position=self.ranks[y]+str(x+1)
                self.squares.setdefault(position,letters)

        # Numbers above of the buttons.
        numbers={
                    '1':0, 
                    '2':1, 
                    '3':2, 
                    '4':3, 
                    '5':4, 
                    '6':5, 
                    '7':6, 
                    '8':7,
                }
        for x, col in enumerate(numbers):
            for y, numbers in enumerate(col):
                self.numbers_col=tk.Label(
                                            self, 
                                            text=numbers, 
                                            font=('monospace',font_size,'bold')
                                        )
                # Alternates between dark/light tiles.
                if x%2==0 and y%2==0: 
                    self.numbers_col.config(foreground=DARK,background=LIGHT)
                elif x%2==1 and y%2==1:
                    self.numbers_col.config(foreground=DARK,background=LIGHT)
                else:
                    self.numbers_col.config(foreground=LIGHT,background=DARK)   

                self.numbers_col.grid(row=x+1,column=y,sticky='ne')
                position=self.ranks[y]+str(x+1)
                self.squares.setdefault(position,numbers)            
        
    # Opens and stores images of pieces and prepares
    # the pieces for the game for both sides.
    def import_pieces(self):
        # Stores white pieces images into dicts.
        path=os.path.join(os.path.dirname(__file__),"white") 
        w_dirs=os.listdir(path)
        for file in w_dirs:
            img=Image.open(path+"\\"+file)
            img=img.resize((80,80))
            img=ImageTk.PhotoImage(image=img)
            self.white_images.setdefault(file,img)

        # Stores black pieces images into dicts.
        path=os.path.join(os.path.dirname(__file__),"black") 
        b_dirs=os.listdir(path)
        for file in b_dirs:
            img=Image.open(path+"\\"+file)
            img=img.resize((80,80))
            img=ImageTk.PhotoImage(image=img)
            self.black_images.setdefault(file,img)

    # Places pieces in starting positions.
    def set_pieces(self): 
        # Assigning positions with their default pieces.
        rank1_pieces={
                        "a1":"r.png", 
                        "b1":"n.png", 
                        "c1":"b.png", 
                        "d1":"q.png", 
                        "e1":"k.png", 
                        "f1":"b.png", 
                        "g1":"n.png", 
                        "h1":"r.png",
                    }

        rank2_pieces={
                        "a2":"p.png", 
                        "b2":"p.png", 
                        "c2":"p.png", 
                        "d2":"p.png", 
                        "e2":"p.png", 
                        "f2":"p.png", 
                        "g2":"p.png", 
                        "h2":"p.png",
                    }    

        rank7_pieces={
                        "a7":"p.png", 
                        "b7":"p.png", 
                        "c7":"p.png", 
                        "d7":"p.png", 
                        "e7":"p.png", 
                        "f7":"p.png", 
                        "g7":"p.png", 
                        "h7":"p.png",
                    }

        rank8_pieces={
                        "a8":"r.png", 
                        "b8":"n.png", 
                        "c8":"b.png", 
                        "d8":"q.png", 
                        "e8":"k.png", 
                        "f8":"b.png", 
                        "g8":"n.png", 
                        "h8":"r.png",
                    }

        # Inserts images into buttons.
        for key in rank1_pieces:
            starting_piece=rank1_pieces[key]
            self.squares[key].config(image=self.white_images[starting_piece])
            self.squares[key].image=self.white_images[starting_piece]
            
        for key in rank2_pieces:
            starting_piece=rank2_pieces[key]
            self.squares[key].config(image=self.white_images[starting_piece])
            self.squares[key].image=self.white_images[starting_piece]

        for key in rank7_pieces:
            starting_piece=rank7_pieces[key]
            self.squares[key].config(image=self.black_images[starting_piece])
            self.squares[key].image=self.black_images[starting_piece]
            
        for key in rank8_pieces:
            starting_piece=rank8_pieces[key]
            self.squares[key].config(image=self.black_images[starting_piece])
            self.squares[key].image=self.black_images[starting_piece]

        # Fill rest with blank pieces.
        for rank in range(3,7): 
            for file in range(DIMENSION):
                starting_piece="blank.png"
                position=self.ranks[file]+str(rank)
                self.squares[position].config(image=self.white_images[starting_piece])
                self.squares[position].image=self.white_images[starting_piece]

# Creates main window with the board objects.
root=tk.Tk()
root=App(root,DIMENSION,DIMENSION)
if __name__ == "__main__":
    root()