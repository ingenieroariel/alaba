# Just one song in a song.txt file, one line per paragraph (screen),
#  when you run "perform.py song.txt" it goes full screen and starts showing the
# first paragraph it then allows you to go forward or backward (in a loop)
# until you press Esc to leave the program.

import sys
import os
from Tkinter import *           # TK is python's default GUI module


#TODO make a more memory-efficient way to read the file.
# maybe with a first pass to store the locations of each new line into a array
# probably this isn't worth unless the file is larger than 1MB ( ? research on it ) 

try:
        if os.path.isfile(sys.argv[1]) :
                pfile = open( sys.argv[1], "r") 
                lines = pfile.readlines()                
                pfile.close()                
        else:
                print "The file %s doesn't exist." % sys.argv[1]
                sys.exit()          

except IndexError:
        print "Usage : performer.py <lyrics.txt>"
        sys.exit()

except IOError:
        print "Can't open file %s" % sys.argv[1]
        sys.exit()


nlines = len(lines)
i = 0



root = Tk()                     # creates a "root window" and name it.
root.title("Performer")



w, h = root.winfo_screenwidth(), root.winfo_screenheight()      # getting screen dimentions
root.geometry("%dx%d+0+0" % (w, h))                             # configuring the screen size

text = Text(root, state=DISABLED)       
text.config(background = "#%02x%02x%02x" % (0, 0, 0) )
text.config(foreground = "#%02x%02x%02x" % (255, 255, 255) )
text.config(font = "Sans %d" % (h * 0.037))
text.config(wrap = WORD)

#TODO make a canvas_text widget, looks like it is need for centering the text
# this one SHOULD have worked according to the TCL spec ... maybe I found a bug ? http://www.tcl.tk/man/tcl8.5/TkCmd/text.htm#M50
#text.config(justify = CENTER)

text.pack(fill=BOTH, expand=1)          # sends the widget to the window, expanding its size to the max


#TODO find out how to put the text on the middle of the screen
# already tried, can't find this one, need external help

# no-go, the text widget doesn't work when I do this
#text.place(anchor=CENTER)

# I get WEIRD resuts :/
#text.grid(row=0)
#e1 = Entry(root)
#e1.grid(row=0, column=0)





def WritePrevious(event):               #  writes previous paragraph on the screen
        global i
        i -= 1
        if i < 0:
                i += nlines 
        text.config(state=NORMAL)       
        text.delete(1.0, END)
        text.insert(END, lines[i])
        text.config(state=DISABLED)        


def WriteNext(event):                   # writes the next paragraph on the screen
        global i
        text.config(state=NORMAL)       
        text.delete(1.0, END)
        i = ( i + 1 ) % nlines
        text.insert(END, lines[i])
        text.config(state=DISABLED)        
        
def EscPressed(event):                  # quits the mainloop() 
        root.quit()


root.bind("<Escape>", EscPressed )
root.bind("q", EscPressed )
root.bind("<Left>", WritePrevious)
root.bind("<Down>", WritePrevious)
root.bind("<Right>", WriteNext)
root.bind("<Up>", WriteNext)



#TODO remove the top/botton and everything else from the screen
# search why this isn't woking, maybe I have to tkraise() it somehow
#root.overrideredirect(1)                                        # ignoring system bars
root.focus_set() 
#start reading the first line
WriteNext(0);

root.mainloop()                                                 # processes events to the window, letting user interact with it

