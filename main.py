from tkinter import *
from tkinter import ttk
from tktile import safetile,Tile,colors
import random
import time
def getkey(dict:dict,index:int):
    try:
        return list(dict.keys())[index]
    except IndexError:
        pass
x:int = 0
y:int = 0
flags:int = 0
elapsed:float = 0
tilegrid:dict[Tile:tuple] = {}
tileindices:list[safetile] = []
minegrid:list[bool] = []
def generateboard(coords:tuple):
    global x,y,elapsed,tilegrid,tileindices,minegrid,flags
    try:
        for tile,position in tilegrid.items():
            tile.body.destroy()
    except AttributeError:
        pass
    startfound:bool = False
    starttiles:list[Tile] = []
    while not(startfound):
        tilegrid = {}
        tileindices = []
        minegrid = []
        (y,x) = coords
        minegrid = [not(i%2==0 or i%3==0 or i%5==0 or i%7==0 or i%9==0) for i in range(x*y)]
        random.shuffle(minegrid)
        start:float = time.time_ns()
        for ypointer in range(y):
            for xpointer in range(x):
                index:int = getindex((xpointer,ypointer))
                tileindices.append(safetile((xpointer,ypointer)))
                tilegrid[Tile(
                    master=tileframe,
                    value=sumadjacentmines(tileindices[index]),
                    mine=minegrid[index],
                    width=2,
                    height=1,
                    data=tileindices[index]
                )] = (xpointer,ypointer)
        for tile,position in tilegrid.items():
            for adjacent in tile.data.adjacents:
                if not((adjacent[0]>-1 and adjacent[0]<x) and (adjacent[1]>-1 and adjacent[1]<y)):
                    continue
                adtile:Tile = getkey(tilegrid,getindex(adjacent))
                if adtile.value==0 and not(adtile.mine):
                    zerocounter:int = 0
                    starttiles = [adtile]
                    for adadjacent in adtile.data.adjacents:
                        if not((adadjacent[0]>-1 and adadjacent[0]<x) and (adadjacent[1]>-1 and adadjacent[1]<y)):
                            continue
                        adadtile:Tile = getkey(tilegrid,getindex(adadjacent))
                        if adadtile.value==0 and not(adadtile.mine):
                            starttiles.append(adadtile)
                            zerocounter+=1
                    if zerocounter>3:
                        startfound = True
                        break
            if startfound:
                break
    for tile in tileindices:
        adjacent:int = sumadjacentmines(tile)
        getkey(tilegrid,getindex(tile.position)).setvalue(adjacent,False)
    for tile,position in tilegrid.items():
        tile.grid(row=position[0],column=position[1])
    def ENDALL():
        for tile,position in tilegrid.items():
            tile.body.unbind("<Button-3>")
            tile.body.config(command=None)
            tile.hidden = False
    def reveal(tile:Tile):
        try:
            if tile.hidden and not(tile.flagged):
                tile.hidden = False
                tile.setvalue(tile.value,False)
                if tile.mine:
                    ENDALL()
                if tile.value==0 and not(tile.mine):
                    for position in tile.data.adjacents:
                        if (position[0]>-1 and position[0]<x) and (position[1]>-1 and position[1]<y):
                            reveal(getkey(tilegrid,getindex(position)))
        except AttributeError:
            pass
    for tile in starttiles:
        reveal(tile)
    def flag(tile:Tile):
        global flags
        if tile.hidden:
            tile.flagged=not(tile.flagged)
            if tile.flagged:
                flags-=1
                getkey(headerwidgets,4).config(text=f"flags: {flags}")
                tile.body.config(
                    text="",
                    background=colors["flag"],
                    activebackground=colors["flag"]
                )
            elif not(tile.hidden):
                tile.setvalue(tile.value,True)
            else:
                flags+=1
                getkey(headerwidgets,4).config(text=f"flags: {flags}")
                tile.body.config(
                    text="",
                    background=colors["unrevealed"],
                    activebackground=colors["highlighted"]
                )
    for tile,position in tilegrid.items():
        tile.body.config(command=lambda t=tile: reveal(t))
        tile.body.bind("<Button-3>",lambda event,t=tile: flag(t))
    elapsed = (time.time_ns()-start)/10**8
def getindex(pos:tuple):
    global x,y,elapsed,tilegrid,tileindices,minegrid,flags
    return (x*pos[1])+pos[0]
def sumadjacentmines(tile:safetile):
    totalmines:int = 0
    global x,y,elapsed,tilegrid,tileindices,minegrid,flags
    for position in tile.adjacents:
        if (position[0]>-1 and position[0]<x) and (position[1]>-1 and position[1]<y):
            try:
                if minegrid[getindex(position)]:
                    totalmines+=1
            except IndexError:
                pass
    return totalmines

root:Tk = Tk()
style = ttk.Style()
style.theme_use("classic")
root.resizable(False,False)
mainframe:Frame = ttk.Frame(
    root,
    padding=5
)
mainframe.grid()
title:Label = ttk.Label(
    mainframe,
    text="caiamitai's minesweeper in tk!!",
    anchor="center",
    width=50
)
title.grid(row=0,column=0)
header:Frame = ttk.Frame(mainframe)
header.grid(row=1,column=0)
tileframe:Frame = ttk.Frame(mainframe)
tileframe.grid(row=2,column=0)
xinput:StringVar = StringVar()
yinput:StringVar = StringVar()
headerwidgets:dict[:tuple] = {
    Entry(
        header,
        textvariable=xinput,
        width=18
    ) : (1,0),
    Entry(
        header,
        textvariable=yinput,
        width=18
    ) : (1,1),
    Button(
        header,
        text="generate new board",
        width=18
    ) : (1,2),
    ttk.Label(
        header,
        text="",
        anchor="center",
        width=20,
        wraplength=100
    ) : (2,1),
    ttk.Label(
        header,
        text=f"flags: {0}",
        anchor="e",
        width=20
    ) : (3,0),
    ttk.Label(
        header,
        text=f"mines left: {0}",
        anchor="w",
        width=20
    ) : (3,2)
}
for widget,position in headerwidgets.items():
    widget.grid(row=position[0],column=position[1])

def managegeneration():
    global flags
    try:
        generateboard((int(xinput.get()),int(yinput.get())))
        getkey(headerwidgets,3).config(text=f"generated in {elapsed} seconds!")
    except ValueError:
        getkey(headerwidgets,3).config(text="invalid inputs. please stop having alzheimers")
    flags = minegrid.count(True)
    getkey(headerwidgets,4).config(text=f"flags: {flags}")
    getkey(headerwidgets,5).config(text=f"mines: {flags}")
getkey(headerwidgets,2).config(command=managegeneration)
root.mainloop()