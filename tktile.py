from tkinter import *
from graphics import color
from dataclasses import dataclass
colors:dict[str:color] = {
    "unrevealed" : color.rgbtohex((200,200,200)),
    "highlighted" : color.rgbtohex((210,210,210)),
    "mine" : color.rgbtohex((200,50,50)),
    "flag" : color.rgbtohex((50,50,200)),

    "0" : color.rgbtohex((0,0,0)),
    "1" : color.rgbtohex((50,50,200)),
    "2" : color.rgbtohex((50,150,50)),
    "3" : color.rgbtohex((200,50,50)),
    "4" : color.rgbtohex((125,50,125)),
    "5" : color.rgbtohex((125,125,50)),
    "6" : color.rgbtohex((50,125,125)),
    "7" : color.rgbtohex((175,100,25)),
    "8" : color.rgbtohex((100,100,100))
}

@dataclass
class safetile:
    position:tuple
    def __post_init__(self):
        self.topleft:tuple = (self.position[0]-1,self.position[1]-1)
        self.top:tuple = (self.position[0],self.position[1]-1)
        self.topright:tuple = (self.position[0]+1,self.position[1]-1)
        self.left:tuple = (self.position[0]-1,self.position[1])
        self.right:tuple = (self.position[0]+1,self.position[1])
        self.bottomleft:tuple = (self.position[0]-1,self.position[1]+1)
        self.bottom:tuple = (self.position[0],self.position[1]+1)
        self.bottomright:tuple = (self.position[0]+1,self.position[1]+1)
        self.adjacents:list[tuple] = [
            self.topleft,
            self.top,
            self.topright,
            self.left,
            self.right,
            self.bottomleft,
            self.bottom,
            self.bottomright
        ]

class Tile:
    def __init__(self,master:Widget=None,value:int=None,mine:bool=None,width:int=None,height:int=None,data:safetile=None):
        self.width:int = width
        self.height:int = height
        self.value:int = value
        self.mine:bool = mine
        self.hidden:bool = True
        self.flagged:bool = False
        self.data:safetile = data
        self.body:Button = Button(
            master,
            text="",
            font=("Kanit",12,"bold"),
            width=width,
            height=height,
            foreground=colors["unrevealed"],
            background=colors["unrevealed"],
            activebackground=colors["highlighted"]
        )
    def grid(self,row:int=None,column:int=None):
        self.body.grid(row=row,column=column)
    def setvalue(self,newval:int,override:bool):
        self.value = newval
        if not(self.hidden) or override:
            if self.mine:
                self.body.config(
                    background=colors["mine"],
                    activebackground=colors["mine"]
                )
            else:
                self.body.config(
                    background=colors["unrevealed"],
                    activebackground=colors["highlighted"],
                    text=str(newval),
                    foreground=colors[str(newval)]
                )