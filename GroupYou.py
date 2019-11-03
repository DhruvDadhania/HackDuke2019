import Tkinter as tk
import tkMessageBox
from Tkinter import StringVar
from Tkinter import *
from PIL import ImageTk, Image
import HackDukeBackend


main = tk.Tk()
main.title("GroupYou")
main.geometry("600x400")
#main.resizable(0, 0)


    
def groupYou():
    if not checkURL():
        tkMessageBox.showinfo("Error", "Please enter a valid URL")
        
    if not checkGroupSize():
        tkMessageBox.showinfo("Error", "Please enter a valid number of groups")
        
    code = url.get().split("/d/")[1]
    code = code.split("/")[0]
    print(int(groupSize.get()))
    # Execute Dhruv
    groups = HackDukeBackend.make_groups(code, int(groupSize.get()))
    label1.grid_remove();
    label2.grid_remove();
    go.grid_remove();
    urlEntry.grid_remove();
    groupSizeEntry.grid_remove();
    
    main.geometry("1000x1500")
    logolabel.grid_remove()
    logolabel.grid(row=0, column = 0)
    
    
    canvas_frame = Frame(main, width=1500, height = 800)
    canvas_frame.grid(row = 1, column = 0)
    
    # Make results canvas
    results = Canvas(canvas_frame, width = 1500, height = 800)
    

    # group is list of lists 
      
    results.grid(row = 1, column=0)
    
    
    numStudents = sum(len(x) for x in groups)
    labelFrames = [tk.LabelFrame() for j in xrange(len(groups))]
    studentLabels = [tk.Label() for j in xrange(numStudents)]
    frame_label = tk.Frame(results, bg="blue")
    results.create_window((0,0), window=frame_label, anchor = "nw")
    for group in range(0,len(groups)):
        labelFrames[group] = tk.LabelFrame(results, text=("Group "+str(group+1)))
        labelFrames[group].grid(row = group/6, column=group%6, padx=10, pady=10)
        labelFrames[group].config(font = ("Helvetica", 30))
        for student in range (0, len(groups[group])):
            studentLabels[group+student] = Label(labelFrames[group], text= groups[group][student])
            studentLabels[group+student].grid(row = student, column = 0)
            studentLabels[group+student].config(font = ("Helvetica", 20))
            
     
    
def checkURL():
    #if "sheets" not in url.get() or "https://" not in url.get():
    #    return False;
    #else:
        return True;
    
def checkGroupSize():
    if not groupSize.get().isdigit():
        return False
    elif int(groupSize.get()) < 2:
        return False
    else:
        return True

logo = Image.open("groupYouLogo.gif")
logo2 = ImageTk.PhotoImage(logo)
logolabel = Label(main,image=logo2)
logolabel.grid(row=0, column = 1)

label1 = tk.Label(main, text="Google Form URL:")
label1.grid(row=1, column=0)

url = StringVar()
urlEntry = tk.Entry(main, textvariable=url)
urlEntry.grid(row=1, column=1)
url.get()


label2 = tk.Label(main, text="Number of groups:")
label2.grid(row=2, column=0, sticky=W)

groupSize = StringVar()
groupSizeEntry = tk.Entry(main, textvariable=groupSize)
groupSizeEntry.grid(row=2, column=1)
groupSize.get()


go = tk.Button(main, text ="Go!", command = groupYou)
go.grid(row = 3, column = 1)




main.mainloop()