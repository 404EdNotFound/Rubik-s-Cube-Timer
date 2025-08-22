#Imported Modules used to execute such instructions that are existing to the programming language to execute specific instructions written by expert progrmmers
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import time
import random
from datetime import datetime, timedelta
import csv

#Used to clear out data within this temporary session of a file
with open("timesList.csv", "w") as file:
    file.write("")

#Class Defined for scrambling puzzles
class Scramble():
    def __init__(self, notation, wideNotation):
        #Scambles denoted by notation and wide notation for bigger cubes
        self.notation = notation
        self.wideNotation = wideNotation
        self.scrambleSet = ""
        self.choice = None
        self.letter = ""
        self.lengthValue = 0
    
    def scrambleGenerator(self, length, choice):
        self.scrambleSet = "" #Used to set the scramble to blank before generating a new scramble
        self.letter = ""
        scrambleText.config(text = "")

    #Inefficient approach to write the scramble, needed help with this
        if puzzleType.get() == "4x4":
            while len(self.scrambleSet) < length: #Needed help with this, setting the condition for the scramble to prevent repetitions of the same character
                self.letter = random.choice(random.choices(choice, weights = map(len, choice))[0]) #Used to randomise items working in multi dimensional arrays

                if not self.scrambleSet or self.letter[0] != self.scrambleSet.split()[-1][0]: #Need to ensure that the notation works perfectly similar to backtracking algorithm (not a perfect demonstration), makes sure that the notation only comes from the scrambleset
                    self.scrambleSet = self.scrambleSet + " " + self.letter
                    scrambleText.config(text = self.scrambleSet)

        else:
            while len(self.scrambleSet) < length:
                self.letter = random.choice(random.choices(choice, weights = map(len, choice))) #Doesn't use the [0] as it is only using a single array

                if not self.scrambleSet or self.letter[0] != self.scrambleSet.split()[-1][0]:
                    self.scrambleSet = self.scrambleSet + " " + self.letter
                    scrambleText.config(text = self.scrambleSet)

    #Method used for being able to update scrambles based on the puzzle involving parameter passing and changes the length and scramble notation each time
    def updateScramble(self, puzzle_type):
        if puzzle_type == "3x3" or puzzle_type == "3x3 One Handed" or puzzle_type == "3x3 Blindfolded":
            self.lengthValue = 50
            self.choice = self.notation

        elif puzzle_type == "2x2":
            self.lengthValue = 25
            self.choice = self.notation

        elif puzzle_type == "4x4":
            self.lengthValue = 95
            self.choice = self.notation, self.wideNotation
        
        else:
            messagebox.showerror("Error!", "Please select a Puzzle Type in order to generate a scramble.") #Users must ensure that a puzzle type must be set before generating a scramble
        
        self.scrambleSet = self.scrambleGenerator(self.lengthValue, self.choice) #sent to the scramble generator method
        scrambleText.config(text = self.scrambleSet)

#Class used for creating the timer within the cube when running and resetting the time
class cubingTimer():
    def __init__(self):
        self.elapsedTime = 0
        self.stringTime = ""
        self.startTime = 0
        self.hours = 0.0
        self.minutes = 0.0
        self.seconds = 0.0
        self.millieseconds = 0.0
        self.running = False
        self.dateFormat = "%d/%m/%Y %H:%M:%S"
        self.date = 0
        self.dateObj = ""
        self.timeFile = "timesList.csv"
        self.tempList = [] #Used as a temporary list to append all times as 1D arrays
        self.times = [] #Used for List of Times to be Stored and appending 2D arrays
        self.maximum = ""
        self.minimum = ""
        # self.current_average_of_5 = ""
        # self.current_average_of_12 = ""
        # self.best_average_of_5 = ""
        # self.best_average_of_12 = ""
    
    def runningTimer(self):
        if not self.running and self.elapsedTime == 0:
            self.startTime = time.time() - self.elapsedTime #Ensures that the timer is running and switches boolean condition to hint whether or not the timer is running
            self.running = True
            self.updateTime()
        
        else:
            self.running = False
            self.updateTime()
    
    #Resets the time to 0
    def resetTime(self):
        self.running = False
        self.elapsedTime = 0
        self.updateTime()
    
    #Updates the timer during each iteration of time, Needed help with this
    def updateTime(self):
        if self.running:
            self.elapsedTime = time.time() - self.startTime
         
        if self.elapsedTime != str("DNF"): #Used to check if the timer is running without error
            self.minutes, self.seconds = divmod(int(self.elapsedTime), 60) #Converts minutes and seconds into a model that only accepts 0-60
            self.hours, self.minutes = divmod(self.minutes, 60) #Only used for when the hour is greater than 1
            self.millieseconds = int((self.elapsedTime - int(self.elapsedTime)) * 100) #Integer value used for being able to write milliseconds
            timer.config(text = f"{int(self.seconds):02}.{self.millieseconds:02}") #Displays the time in text

        #Saving unwanted spaces unless these conditions are true
            if self.minutes >= 1:
                timer.config(text = f"{int(self.minutes):02}:{int(self.seconds):02}.{self.millieseconds:02}")

            if self.hours >= 1:
                timer.config(text = f"{int(self.hours):02}:{int(self.minutes):02}:{int(self.seconds):02}.{self.millieseconds:02}")
            cubingWindow.after(10, self.updateTime) #Updates after every 10 milliseconds

    def listStorage(self):
            self.tempList.append(scrambleText.cget("text")) #cget retrieves the characters within the label
            self.tempList.append(self.dateObj)
            self.tempList.append(puzzleType.get())
            self.times.append(self.tempList)

            self.times.sort(key=lambda x:x[2], reverse=True)
            self.tempList = []
    
    #Writes inputted data into the CSV file with append mode exception handling for finding file
    def write_to_file(self):
        try:
            file = open(self.timeFile, "a")
        
        except FileNotFoundError:
            messagebox.showerror("Error!", "File cannot open")
        
        else:
            #Appends all data whilst separating each field with ","
            file.write(self.stringTime + "," + scrambleText.cget("text") + "," + self.dateObj + "," + puzzleType.get())
            file.write("\n")
            file.close()

    #Reads the file storing data as CSV file with exception handling for finding file
    def read_from_file(self):
        try:
            file = open(self.timeFile, "r")
            
        except FileNotFoundError:
            messagebox.showerror("Error!", "File cannot open")
        
        else:
            #Attempting to reverse sort the data within a particular index (needed help with this)
            csv.reader(file)
            file.close()

    #Both functions defined to identify any penalties for the solve 
    def plusTwo(self):
        if self.millieseconds > 0 and self.elapsedTime != str("DNF"):
            self.elapsedTime +=  2
            self.updateTime()
        
        elif self.elapsedTime == str("DNF"):
            messagebox.showerror("Error!", "Cannot plus 2 a DNF solve.")
        
        return self.elapsedTime #Returns this back to the program

    def unSolved(self):
        if self.elapsedTime != 0 and not self.running:
            self.elapsedTime = str("DNF")
            timer.config(text = "DNF")
        
        return self.elapsedTime #Returns this back to the program

    #Appends the data within File
    def submission(self):
        if self.elapsedTime == str("DNF"):
            self.stringTime = "DNF"
            self.tempList.append(self.stringTime)
            self.listStorage()
            self.write_to_file()
            self.resetTime()
            scramble.updateScramble(puzzleType.get())
        
        #Timer cannot be 0 and after solve
        elif self.elapsedTime == 0:
            messagebox.showwarning("Warning", "Cannot append the timer without starting it")

        else: 
            if self.hours >= 1:
                self.stringTime = str(f"{int(self.hours):02}:{int(self.minutes):02}:{int(self.seconds):02}.{self.millieseconds:02}")
            
            elif self.minutes >= 1:
                self.stringTime = str(f"{int(self.minutes):02}:{int(self.seconds):02}.{self.millieseconds:02}")
            
            else:
                self.stringTime = str(f"{int(self.seconds):02}.{self.millieseconds:02}")
            self.tempList.append(self.stringTime)

            self.date = datetime.now()
            self.dateObj = str(self.date.strftime(self.dateFormat))
            
            self.listStorage()
            self.write_to_file()
            self.read_from_file()
            self.resetTime()
            scramble.updateScramble(puzzleType.get())

        return self.elapsedTime #Returns this back to the program

#This is a sort example that will subject to change or stay the same, this makes use of the lambda function that is used to sort such relevant data, this uses a complex algorithm that is like Insertion Sort but also incorperates the idea of sorting into different fields that are chosen by the user in Ascending and Descending Order, needed help with this
def sortFunction(tree, column, descending):
    data = [(tree.set(item, column), item) for item in tree.get_children("")]
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)

def on_sort(column, table):
    sort_column = table.heading(column)["text"]
    if "↑" in sort_column:
        sortFunction(table, column, False)
        table.heading(column, text=(column + " ↓"))
    else:
        sortFunction(table, column, True)
        table.heading(column, text=(column + " ↑"))

#Uses event handling to identify which key is pressed while the window is running to trigger the event specified
def presses(event):
    if puzzleType.get() == "":
        messagebox.showerror("Error!", "You must select a puzzle type before running!")
    
    elif event.keysym == "space" and scrambleText.cget("text") != "":
        stackmatTimer.runningTimer()
    
    elif event.keysym in ["R", "r", "Escape"]:
        stackmatTimer.resetTime()
    
    elif event.keysym == "Return" and stackmatTimer.elapsedTime == 0:
        stackmatTimer.resetTime()
        scramble.updateScramble(puzzleType.get())

#Transfer between screens
def transferScreen(currentWindow, newWindow):
    cubingTimer()
    currentWindow.destroy()
    newWindow()

#Communicates with the directory to save and load files under specific file names
def save_file():
    stackmatTimer.timeFile = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]) #asksaveasfilename is a dialog from the tkinter.filedialog module which displays a file open dialog and stores the file path to the variable for the user to save their file
    if not stackmatTimer.timeFile:
        stackmatTimer.timeFile = "timesList.csv"
        return
    
    with open(stackmatTimer.timeFile, mode="w", encoding="utf-8", newline = "") as output_file: #UTF-8 is a standard encoding tool
        writer = csv.writer(output_file)

        for item_id in table.get_children():
            value = table.item(item_id, 'values')
            writer.writerow(value)

def open_file():
    stackmatTimer.timeFile = askopenfilename(filetypes = [("CSV Files", "*.csv"), ("All Files", "*.*")]) #askopenfilename is a dialog from the tkinter.filedialog module which displays a file open dialog and stores the file path to the variable
    if not stackmatTimer.timeFile: #Used to check if the button pressed isn't open meaning that the filepath doesn't contain any data and returns without executing any code
        stackmatTimer.timeFile = "timesList.csv"
        return
    table.delete(*table.get_children())

    with open(stackmatTimer.timeFile, mode="r", encoding="utf-8") as input_file: #UTF-8 is a standard encoding tool
        reader = csv.reader(input_file)

        for item in reader:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1

#Views the list of times recorded in a table in a separate window
def viewTimes():
    global table
    list_of_times = Tk()
    list_of_times.title("List of times")
    table = ttk.Treeview(list_of_times)
    table["column"] = ("Time", "Scramble", "Date and Time", "Puzzle Type")
    columns = ("Time", "Scramble", "Date and Time", "Puzzle Type")
    
    tableFrame = Frame(list_of_times, background = "white")
    
    #Button Frames for saving, loading and deleting such sessions
    tableButtonFrame = Frame(list_of_times, background = "White")
    saveButton = Button(tableButtonFrame, text = "Save Session", command = save_file)
    loadButton = Button(tableButtonFrame, text = "Load Session", command = open_file)
    clearButton = Button(tableButtonFrame, text = "Clear Session")
    timerButton = Button(tableButtonFrame, text = "Return to timer window", command = lambda: transferScreen(list_of_times, mainPage))

    #Inserts the columns position by position
    table.column("#0", width = 0, stretch = NO)
    table.column("Time", anchor = CENTER, width = 300, minwidth = 25)
    table.column("Scramble", anchor = CENTER, width = 300, minwidth = 25)
    table.column("Date and Time", anchor = CENTER, width = 300, minwidth = 25)
    table.column("Puzzle Type", anchor = CENTER , width = 300, minwidth = 25)

    #Inserts the heading based on the columns
    table.heading("#0", text = "Label", anchor = W)
    table.heading("Time", text = "Time")
    table.heading("Scramble", text = "Scramble")
    table.heading("Date and Time", text = "Date and Time")
    table.heading("Puzzle Type", text = "Puzzle Type")
    
    #Inserts the data within the file
    with open("timesList.csv", "r") as file:
        count = 0
        reader = csv.reader(file) # reads the data within the file
        for item in reader:
            table.insert(parent = '', index = "end", iid = count, text = "", values = item)
            count += 1

        for column in columns:
            table.heading(column, text=column, command=lambda c=column: on_sort(c, table)) #Sorts the columns based on the headings that are used to sort the data table

    tableFrame.pack(fill = BOTH)
    table.pack()
    tableButtonFrame.pack(fill = BOTH)
    saveButton.pack(padx = 5, pady = 5)
    loadButton.pack(padx = 5, pady = 5)
    clearButton.pack(padx = 5, pady = 5)
    timerButton.pack(padx = 5, pady = 5)
    return list_of_times

#Main window for the cubing timer
def mainPage():
    global scrambleText, timer, cubingWindow, puzzleType, tableFrame

    cubingWindow = Tk()
    cubingWindow.title("Rubik's Cube Timer")
    frame = Frame(cubingWindow, background="white")

    cubingWindow.bind("<Key>", presses) #Only affects key presses involved in the window
    scrambleText = Label(frame, background="white", foreground="black", font=("Arial", 20, "bold"))
    timer = Label(frame, background = "White", foreground = "Black", text = "00.00", font=("Verdana", 40, "bold"))
    plus_2_button = Button(frame, text = "+2", command = stackmatTimer.plusTwo)
    DNF_button = Button(frame, text = "DNF", command = stackmatTimer.unSolved)
    submit_button = Button(frame, text = "Submit", command = stackmatTimer.submission)

    buttonFrame = Frame(cubingWindow, background = "white")
    puzzleType = StringVar()
    puzzles = OptionMenu(frame, puzzleType, "2x2", "3x3", "3x3 One Handed", "3x3 Blindfolded", "4x4") #Choices of puzzle for the user to choose from
    generator = Button(buttonFrame, background="blue", foreground="lime", width="50", text="Generate Scramble", command= lambda: scramble.updateScramble(puzzleType.get())) #Scramble button which updates
    ruleButton = Button(buttonFrame, background = "black", foreground = "red", text = "Return to Rules page", command = lambda: transferScreen(cubingWindow, rulePage)) #Switches screen to the rules page
    times_list = Button(buttonFrame, text = "See time session and list", command = lambda: transferScreen(cubingWindow, viewTimes))
    
    #Places all widgets into the interface with the pack method
    frame.pack(fill = BOTH)
    scrambleText.pack()
    timer.pack()
    plus_2_button.pack(padx = 5, pady = 5)
    DNF_button.pack(padx = 5, pady = 5)
    submit_button.pack(padx = 5, pady = 5)
    buttonFrame.pack(fill = BOTH)
    generator.pack(padx = 5, pady = 5)
    puzzles.pack(padx = 5, pady = 5)
    ruleButton.pack(padx = 5, pady = 5)
    times_list.pack(padx = 5, pady = 5)
    return cubingWindow

#Creating the Rule Based window that the user needs to know
def rulePage():
    global ruleWindow
    ruleWindow = Tk()
    ruleWindow.title("Rules Page!")
    ruleFrame = Frame(ruleWindow, background = "White")
    ruleLabel = Label(ruleFrame, background = "White", text = "Please read all rules below before using the timer! \n When generating a scramble, press either the 'Generate Scramble' button or the Enter Key \n The Scrambles are all Computer-Generated Sequences to scramble the cube, please scramble with White on Top and Green facing you! \n Start the timer by pressing the spacebar when you are ready to solve, DO NOT hold the spacebar as pressing and holding can cause confusion! \n Reset the timer with the R or Escape key. \n 2x2 is currently used with all notations and will be changed to use either RUF or LUF moves \n Currently this Software is written in Python with the Tkinter Module and is still in development! \n Have Fun Timing and Solving! \n Thank You! press the 'OK' Button when you're ready to time Solves!", font = ("Times New Roman", 15, "bold"))
    button_confirmation = Button(ruleFrame, text = "OK", command = lambda : transferScreen(ruleWindow, mainPage))

    ruleFrame.pack()
    ruleLabel.pack()
    button_confirmation.pack()
    return ruleWindow

#Defines the list of notations depending on the puzzle, more if needed
notation = ["F", "L", "U", "D", "B", "R", "F'", "L'", "U'", "D'", "B'", "R'", "F2", "D2", "U2", "B2", "L2", "R2"]
wideNotation = ["Fw", "Uw", "Lw", "Dw", "Rw", "Bw", "Fw'", "Uw'", "Lw'", "Dw'", "Rw'", "Bw'", "Fw2", "Uw2", "Lw2", "Dw2", "Rw2", "Bw2"]

#Classes are called with objects created
stackmatTimer = cubingTimer()
scramble = Scramble(notation, wideNotation)

#First window running under main loop
ruleWindow = rulePage()
ruleWindow.mainloop()

#Commented sections of code:

    #Used to allow the user to choose between different scrambles for 2x2 based on their preferences
''' if puzzleType.get() == "2x2":
        handText = StringVar()
        handOption = OptionMenu(frame, handText, "Left", "Right")
        handOption.pack()
        scramble.updateScramble(puzzleType.get()) '''