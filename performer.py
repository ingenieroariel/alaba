#!/usr/bin/env python
import sys
import os
from Tkinter import *


def play(song_name):
    """
    Paragraphs are separated by a blank line
    This function takes a path to file in the following format:
    Two line breaks 
    """
    song_file = open(song_name, "r")
    # We assume the file is small enough that loading it fully into
    # the RAM is not an issue. TODO: Revisit in the future to avoid
    # having it blow up if the file is too big.
    lines = song_file.readlines()
    song_file.close()

    nlines = len(lines)
    global i
    i = 0

    # creates a "root window" and name it.
    root = Tk()
    root.title("Performer")

    # getting screen dimentions
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    # configuring the screen size
    root.geometry("%dx%d+0+0" % (w, h))
    # Setup sensible defaults for the text
    text = Text(root, state=DISABLED)       
    text.config(background = "#%02x%02x%02x" % (0, 0, 0) )
    text.config(foreground = "#%02x%02x%02x" % (255, 255, 255) )
    text.config(font = "Sans %d" % (h * 0.037))
    text.config(wrap = WORD)

    # TODO make a canvas_text widget, looks like it is need fori
    # centering the text this one SHOULD have worked according 
    # to the TCL spec ... maybe I found a bug ? 
    # http://www.tcl.tk/man/tcl8.5/TkCmd/text.htm#M50
    #text.config(justify = CENTER)

    # sends the widget to the window, expanding its size to the max
    text.pack(fill=BOTH, expand=1)          


    #TODO find out how to put the text on the middle of the screen
    # already tried, can't find this one, need external help

    # no-go, the text widget doesn't work when I do this
    #text.place(anchor=CENTER)

    # I get WEIRD resuts :/
    #text.grid(row=0)
    #e1 = Entry(root)
    #e1.grid(row=0, column=0)

    def write_previous(event):
        """
        writes previous paragraph on the screen
        """
        global i
        i -= 1
        if i < 0:
                i += nlines 
        text.config(state=NORMAL)       
        text.delete(1.0, END)
        text.insert(END, lines[i])
        text.config(state=DISABLED)        


    def write_next(event):
        """
        writes the next paragraph on the screen
        """
        global i
        text.config(state=NORMAL)       
        text.delete(1.0, END)
        i = ( i + 1 ) % nlines
        text.insert(END, lines[i])
        text.config(state=DISABLED)        
        
    def esc_pressed(event):
        """
        quits the mainloop()
        """
        root.quit()

    # Bind the key handlers to the application
    root.bind("<Escape>", esc_pressed )
    root.bind("q", esc_pressed )
    root.bind("<Left>", write_previous)
    root.bind("<Down>", write_previous)
    root.bind("<Right>", write_next)
    root.bind("<Up>", write_next)



    #TODO remove the top/botton and everything else from the screen
    # search why this isn't woking, maybe I have to tkraise() it somehow
    # ignoring system bars
    #root.overrideredirect(1) 
    root.focus_set() 

    #start reading the first line
    write_next(0)

    # processes events to the window, letting user interact with it
    root.mainloop()        

if __name__ == "__main__":
    # This library is being run as a script, look
    # for the song's path in the argument
    try:
        if not os.path.isfile(sys.argv[1]):
           print "The file %s doesn't exist." % sys.argv[1]
           sys.exit()          
        song_name = sys.argv[1]
        play(sys.argv[1])

    except IndexError:
        print "Usage : performer.py <lyrics.txt>"
        sys.exit()

    except IOError:
        print "Can't open file %s" % sys.argv[1]
        sys.exit()
