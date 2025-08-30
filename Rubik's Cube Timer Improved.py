#Modules are imported here
from tkinter import *
from tkinter import ttk, messagebox, colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename
import random, time, csv, datetime, os
from datetime import datetime, timedelta
from xml.dom.minidom import Notation

timerRunning = None
filepath = "dummyTimes.csv" #Dummy file for default times

with open(filepath, "w") as file:
    file.write("")

#Constant list of fonts for the scramble text and the timer
FONTS = ["Agency FB", "Algerian", "Arial", "Arial Black", "Arial Narrow", "Arial Narrow Special", "Arial Rounded MT", "Arial Special", "Arial Unicode MS", "Bahnschrift", "Baskerville Old Face", "Bauhaus 93", "Beesknees ITC", "Bell MT", "Berlin Sans FB", "Berlin Sans FB Demi", "Bernard MT Condensed", "Blackadder ITC", "Book Antiqua", "Bradley Hand ITC", "Brush Script MT", "Calibri", "Calisto MT", "Cambria", "Candara", "Century Gothic", "Comic Sans MS", "Consolas", "Constantia", "Cooper Black", "Copperplate Gothic Bold", "Copperplate Gothic Light", "Corbel", "Courier New", "Courier Regular", "Curlz MT", "Edwardian Script ITC", "Elephant", "Engravers MT", "Eras ITC", "EucrosiaUPC", "Euphemia", "Eurostile", "Felix Titling", "Fine Hand", "Fixed Miriam Transparent", "Forte", "Franklin Gothic", "Franklin Gothic Medium", "Freestyle Script", "Gabriola", "Garamond", "Georgia", "Gill Sans", "Gill Sans MT", "Gill Sans MT Condensed", "Gradl Grotesque", "Gulim", "GulimChe", "Hadassah Friedlaender", "Haettenschweiler", "Harlow Solid Italic", "Harrington", "HGGothicE", "HGMinchoE", "HGSoeiKakugothicUB", "High Tower Text", "Holidays MT", "HoloLens MDL2 Assets", "Impact", "Imprint MT Shadow", "Informal Roman", "IrisUPC", "Iskoola Pota", "JasmineUPC", "Javanese Text", "Jokerman", "Juice ITC", "Kalinga", "Kartika", "Khmer UI", "Kino MT", "Kristen ITC", "Lao UI", "Latha", "Leelawadee", "Levenim MT", "Lucida Bright", "Lucida Bright Math", "Lucida Calligraphy", "Lucida Console", "Lucida Fax", "Lucida Handwriting", "Lucida Sans", "Lucida Sans Typewriter", "Lucida Sans Unicode", "Magneto", "Maiandra GD", "Malgun Gothic", "Mangal", "Matura MT Script Capitals", "McZee", "Mead Bold", "Meiryo", "Mercurius Script MT Bold",  "Microsoft Sans Serif", "Mistral", "Modern Love", "Modern No. 20", "Mongolian Baiti", "Monotype.com", "Monotype Corsiva", "Monotype Sorts", "MoolBoran", "MS Gothic", "MS PMincho", "MS Reference", "News Gothic MT", "New Caledonia", "OCR A Extended", "Old English Text MT", "Onyx", "Palatino Linotype", "Papyrus", "Parchment", "Perpetua", "Perpetua Titling MT", "Playbill", "PMingLiU", "PMingLiU-ExtB", "Poor Richard", "Pristina", "Rage Italic", "Ravie", "Rockwell", "Rockwell Extra Bold", "Rod", "Sakkal Majalla", "Script MT Bold", "Segoe MDL2 Assets", "Segoe Print", "Segoe Script", "Segoe UI", "Segoe UI Emoji", "Segoe UI Historic", "Segoe UI Symbol", "Segoe UI Variable", "Shonar Bangla", "Showcard Gothic", "Shruti", "SimHei", "Simplified Arabic", "SimSun", "SimSun-ExtB", "Sitka", "Snap ITC", "Stencil", "Sylfaen", "Tahoma", "Tempus Sans ITC", "Times New Roman", "Trebuchet MS", "Tw Cen MT", "Verdana", "Viner Hand ITC", "Vivaldi", "Vladimir Script", "Wide Latin", "Yu Gothic", "Yu Gothic UI"]

#Scramble Class defined for setting the scramble based on the puzzle that is used here
class Scramble():
    #defined outside so that can be used with many objects (also used for WCA Puzzles)
    NOTATION = ["F", "L", "U", "D", "B", "R", "F'", "L'", "U'", "D'", "B'", "R'", "F2", "D2", "U2", "B2", "L2", "R2"]
    WIDE_NOTATION = ["Fw", "Uw", "Lw", "Dw", "Rw", "Bw", "Fw'", "Uw'", "Lw'", "Dw'", "Rw'", "Bw'", "Fw2", "Uw2", "Lw2", "Dw2", "Rw2", "Bw2"]
    PYRA_NOTATION = ["U", "B", "R", "L", "U'", "B'", "R'", "L'", "u", "b", "r", "l", "u'", "b'", "r'", "l'"]
    SKEWB_NOTATION = ["U", "B", "R", "L", "U'", "B'", "R'", "L'"]
    RIGHT_HANDED = ["F", "U", "R", "F'", "U'", "R'", "F2", "U2","R2"]
    LEFT_HANDED = ["F", "L", "U", "F'", "L'", "U'", "F2", "U2", "L2"]
    
    #Defined as a dictionary with keys and values (had help with cleaning up the code)
    SCRAMBLE_CONFIGURE_LIST = {
    "3x3": (50, NOTATION), "3x3 One Handed": (50, NOTATION), "3x3 Blindfolded": (50, NOTATION), "2x2_L": (25, LEFT_HANDED), "2x2_R": (25, RIGHT_HANDED), "4x4": (95, (NOTATION, WIDE_NOTATION)), "Pyraminx": (25, PYRA_NOTATION), "Skewb": (25, SKEWB_NOTATION)
    }
    
    def __init__(self):
        self.letter, self.scrambleSet = "", ""
        self.choice = None
        self.lengthValue = 0
    
    def scrambleGenerator(self, length, choice, puzzleType):
        self.scrambleSet, self.letter = "", "" #Used before generating a new Scramble
        scrambleText.config(text = "")
        
        if puzzleType == "4x4":
            #Error Handling for checking puzzles
            try:
                while len(self.scrambleSet) < length: #Needed Assistance for setting the condition for the scramble to prevent repetitions of the same character
                    self.letter = random.choice(random.choices(choice, weights = map(len, choice))[0]) #Used to randomise items working in multi dimensional arrays

                    if not self.scrambleSet or self.letter[0] != self.scrambleSet.split()[-1][0]: #Need to ensure that the notation works perfectly similar to backtracking algorithm (not a perfect demonstration), makes sure that the notation only comes from the scrambleset
                        self.scrambleSet = self.scrambleSet + " " + self.letter
                        scrambleText.config(text = self.scrambleSet, wraplength = 500, justify = CENTER)
            
            except Exception as e:
                messagebox.showerror("Error!", "Error Occured when genereating a scramble: " + e)
        
        else:
            #repeated syntax
            while len(self.scrambleSet) < length: #Needed Assistance for setting the condition for the scramble to prevent repetitions of the same character
                self.letter = random.choice(random.choices(choice, weights = map(len, choice))) #Doesn't use the [0] as only 1 array is used here

                if not self.scrambleSet or self.letter[0] != self.scrambleSet.split()[-1][0]: #Need to ensure that the notation works perfectly similar to backtracking algorithm (not a perfect demonstration), makes sure that the notation only comes from the scrambleset
                    self.scrambleSet = self.scrambleSet + " " + self.letter
                    scrambleText.config(text = self.scrambleSet, wraplength = 500, justify = CENTER)

    #Updates the scramble each time (hopefully change this to run efficiently)
    def updateScramble(self, puzzleType):
        #Created with Assistance for setting keys for dictionaries
        key = puzzleType if puzzleType != "2x2" else f"2x2_{handChoice.get()[0]}" #assigns a key to the dictionary based on the choices
        if key in self.SCRAMBLE_CONFIGURE_LIST:
            self.lengthValue, self.choice = self.SCRAMBLE_CONFIGURE_LIST[key] #Gets the attribute based on the key and uses this key to access the dictionary if stored
            self.scrambleSet = self.scrambleGenerator(self.lengthValue, self.choice, puzzleType)
            scrambleText.config(text = self.scrambleSet)
            timer.resetTime()
        
        else:
            messagebox.showerror("Error!", "You must choose a Puzzle Type from the chosen list!")
            self.scrambleSet = None
            return
        
#Creates a class for controlling the timer within the system           
class Timer():
    def __init__(self):
        self.start = self.elapsed = self.defaultTime = self.date = self.hours = self.minutes = self.did_not_finish_counter = 0
        self.currentMean = self.currentAverage = self.seconds = self.millieseconds = self.total = self.standardDeviation = 0.0 #Defined as their specified data types wherever possible
        self.bestMean = self.bestAverage_5 = self.bestAverage_12 = float('inf')
        self.stringTime = "" #Converts the time into string
        self.dateFormat = "%d/%m/%Y %H:%M:%S"
        self.running = False
        self.timerList, self.validTimes = [], []
    
    def startTime(self):
        if not self.running and self.elapsed == 0: #Ensures that the timer is running
            #Starts the timer and runs the stopwatch
            self.start = time.time() - self.elapsed
            self.running = True
            self.updateTime()
        
        else:
            self.running = False
            self.updateTime()

    def resetTime(self):
        #Resets the stopwatch back to 0
        self.running = False
        self.elapsed = 0
        self.updateTime()

    #Used to update the running timer on display
    def updateTime(self):
        global timerRunning
        timerRunning = None   
        if self.running:
            self.defaultTime = self.elapsed = time.time() - self.start
        
        #Used to convert the timer into a specific format (had help with this)
        if self.elapsed != str("DNF"):
            self.minutes, self.seconds = divmod(int(self.elapsed), 60) #Converts the minutes and the seconds ensuring that only 0-60 is allowed
            self.hours, self.minutes = divmod(int(self.minutes), 60) #Converts the hours and the minutes ensuring that only 0-60 is allowed
            self.millieseconds = int((self.elapsed - int(self.elapsed)) * 100) #Converts the millieseconds to only allow 0-99
            
            timer_string = f"{int(self.seconds):02}.{self.millieseconds:02}"
            
            #Separate Conditions Used when the timer starts reaching 1 minute and 1 hour
            if self.minutes >= 1:
                timer_string = f"{int(self.minutes):02}:{int(self.seconds):02}.{self.millieseconds:02}"
            
            if self.hours >= 1:
                timer_string = f"{int(self.hours):02}:{int(self.minutes):02}:{int(self.seconds):02}.{self.millieseconds:02}"
            
            timerText.config(text = timer_string)
            timerRunning = timerWindow.after(10, self.updateTime) #after 10 milliseconds
    
    #Submits the time based on what is shown within the timer and ensures that the timer doesn't run when submitting times
    def submission(self):
        if self.elapsed == str("DNF"):
            self.stringTime = "DNF"
            self.date = str((datetime.now()).strftime(self.dateFormat))
            self.write_times_to_file()
            self.resetTime()
            scramble.updateScramble(puzzleChoice.get())
        
        elif self.elapsed == 0:
            messagebox.showwarning("Warning!", "Cannot submit the time when it hasn't started yet!")
        
        elif self.elapsed > 0 and self.running:
            messagebox.showwarning("Error!", "Do not submit a time whilst the timer is running!")
            
        else:
            self.stringTime = timerText.cget("text") #retrives the text character
            self.date = str((datetime.now()).strftime(self.dateFormat)) #Uses a datetime format to display the contents of the time
            self.write_times_to_file()
            self.resetTime()
            scramble.updateScramble(puzzleChoice.get())
    
    def write_times_to_file(self):
        count = 0
        table.delete(*table.get_children())
        
        try:
            with open(filepath, "a") as file:
                file.write(self.stringTime + "," + scrambleText.cget("text") + "," + self.date + "," + puzzleChoice.get())
                file.write("\n")

            #Inserting items in a table
            with open(filepath, "r") as file:
                reader = csv.reader(file)
                self.timerList = list(reader)
                
                for item in self.timerList:
                    table.insert(parent = '', index = "end", iid = count, text = "", values = item)
                    count += 1

                for column in columns:
                    table.heading(column, text=column, command=lambda c=column: on_sort(c, table)) #Sorts the columns based on the headings that are used to sort the data table
            
            #Used to update the mean
            self.update_mean_time()
            
            #Used to update the average
            self.update_average_time(5)
            self.update_average_time(12)
        
        except FileNotFoundError:
            messagebox.showerror("Error!", "Cannot find file!")
    
    #Created with assistance to convert into specific time format
    def timeData(self, stringTime):
        try:
            part = stringTime.split(":") #splits times more than 1 minute based on its separateor
            total = 0
            
            #Converts the time format whether "HH:MM:SS.MS" or "MM:SS.MS"
            if len(part) == 3:
                hour, mins, seconds = int(part[0]), int(part[1]), float(part[2])
            
            elif len(part) == 2:
                mins, seconds = int(part[0]), float(part[1])
            
            second = int(seconds)
            milliesecond = (seconds - second) * 1000
            total = (hour * 3600) + (mins * 60) + (second + milliesecond / 1000)
            return timedelta(seconds=total) #returns the total time within the specific format
        
        except ValueError:
            return timedelta(seconds = 0) #In case of errors
        
    def plusTwo(self):
        if self.millieseconds > 0 and self.elapsed != str("DNF") and (self.elapsed - self.defaultTime != 2):
            self.elapsed += 2
            self.updateTime()
        
        else:
            messagebox.showwarning("Warning!", "If the timer shows DNF, cannot plus 2 on a DNF \n Only 1 Plus 2 is used unless this is a mistake!")
            
        return self.elapsed
    
    def unSolved(self):
        if self.elapsed != 0 and not self.running:
            self.elapsed = str("DNF")
            timerText.config(text = "DNF")
        
        return self.elapsed
    
    def goodSolve(self):
        self.elapsed = self.defaultTime
        self.updateTime()
        
        return self.elapsed
    
    def calculateMean(self):
        self.total, self.did_not_finish_counter = 0.0, 0
        self.validTimes = []
        
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            self.timerList = list(reader)
            
        for item in self.timerList:
            if item[0] != "DNF" and len(item[0]) >= 8:
                self.total += self.timeData(item[0]).total_seconds()
                self.validTimes.append(item[0])

            elif item[0] != "DNF" and len(item[0]) < 8:
                self.total += float(item[0])
                self.validTimes.append(item[0])
            
            else:
                self.did_not_finish_counter += 1
        
        self.best_and_worst_times()
        validity = (len(self.timerList) - self.did_not_finish_counter)
        
        if validity == 0:
            return 0
        
        else:
            return self.total / validity

    def calcuate_standard_deviation(self, mean):
        self.total = 0.0
        self.validTimes = []
        
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            self.timerList = list(reader)
        
        for item in self.timerList:
            if item[0] != "DNF":
                if ":" in item[0]:
                    seconds = self.timeData(item[0]).total_seconds()
                
                else:
                    seconds = float(item[0])
                
                self.validTimes.append(seconds)
        
        for item in self.validTimes:
            self.total += item ** 2
        
        return ((self.total / len(self.validTimes)) - (mean ** 2)) ** 0.5
    
    #Used for calculating averages whilst extracting best and worst time (used with assistance and works perfectly)
    def calculate_average(self, number):
        self.total = 0.0
        self.validTimes = []

        with open(filepath, "r") as file:
            reader = csv.reader(file)
            self.timerList = list(reader)
            
            selectedItems = self.timerList[-number:] #uses spllicing to identify how many pieces of data is required

            #Assistance in cleaning the program for readability
            for item in selectedItems:
                if item[0] != "DNF":
                    if ":" in item[0]: #Used for any instances of ":" to convert into a specific format or into decimal point
                        seconds = self.timeData(item[0]).total_seconds()
                    
                    else:
                        seconds = float(item[0])
                    
                    self.total += seconds
                    self.validTimes.append(seconds)

            best_worst_times = self.best_and_worst_times()
            
            self.validTimes = [float(time) for time in self.validTimes if time not in best_worst_times] #appends times not included in best or worst time
            self.total = sum(self.validTimes)
            
            validity = len(self.validTimes)

            if validity == 0:
                return 0

            else:
                return self.total / validity
        
    #Created with Assistance for conversion
    def convert_stat_time(self, stat_type):
        minutes, seconds = divmod(int(stat_type), 60)
        hours, minutes = divmod(minutes, 60)
        millieseconds = abs(int((stat_type - int(stat_type)) * 100))

        return hours, minutes, seconds, millieseconds
    
    #Created with assistance for conversion
    def update_display_stat(self, stat, label, type_of_stat, type):
        type = f"{"Average" if type == "average" else "Mean"}"
        hours, minutes, seconds, millieseconds = self.convert_stat_time(stat)
        format_time = ""
        type_of_stat = f"{"Best" if type_of_stat == "best" else "Current"}" + " " + type + ": "
        
        if hours > 0:
            format_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{millieseconds:02}"
            
        elif minutes > 0:
            format_time = f"{int(minutes):02}:{int(seconds):02}.{millieseconds:02}"
        
        else:
            format_time = f"{int(seconds):02}.{millieseconds:02}"
        
        label.config(text = type_of_stat + format_time)
        numSolves.config(text = "Number of solves: " + str(len(self.timerList)))
        numFails.config(text = "Number of DNFs: " + str(self.did_not_finish_counter))
        standard_deviation.config(text = "Standard Deviation: " + str(self.standardDeviation))
    
    #Created with assistance for calcuating and updating the mean time
    def update_mean_time(self):
        self.currentMean = round(self.calculateMean(), 2)
        self.standardDeviation = round(self.calcuate_standard_deviation(self.currentMean), 2)
        
        if self.currentMean <= self.bestMean and self.currentMean != 0.0:
            self.bestMean = self.currentMean
            self.update_display_stat(self.bestMean, bestMean, "best", "mean")
            
        self.update_display_stat(self.currentMean, currentMean, "current", "mean")
    
    def update_average_time(self, number):
        self.currentAverage = round(self.calculate_average(number), 2)
        
        #Created with Assistance (used to update the interface when it reaches the desired number of solves)
        
        #Doesn't update average based on the number set by the parameter "number"
        if len(self.timerList) < number:
            return
        
        currentLabel = current_average_5 if number == 5 else current_average_12
        bestLabel = best_average_5 if number == 5 else best_average_12
        
        #Ensures that the average is updated based on the number of solves within the session
        if number == 5:
            #hasAttr is based on the attribute defined in the class
            if (not hasattr(self, "bestAverage_5")) or (self.currentAverage <= self.bestAverage_5 and self.currentAverage != 0.0):
                self.bestAverage_5 = self.currentAverage
                self.update_display_stat(self.bestAverage_5, bestLabel, "best", "average")
    
        elif number == 12:
            if (not hasattr(self, "bestAverage_12")) or (self.currentAverage <= self.bestAverage_12 and self.currentAverage != 0.0):
                self.bestAverage_12 = self.currentAverage
                self.update_display_stat(self.bestAverage_12, bestLabel, "best", "average")
        
        self.update_display_stat(self.currentAverage, currentLabel, "current", "average")
    
    #Sets the best and worst time for the specified session
    def best_and_worst_times(self):
        if self.validTimes:
            maximum, minimum = max(self.validTimes), min(self.validTimes) #uses keywords max and min to indicate maximum and minimum
            bestTime.config(text = "Best: " + str(minimum))
            worstTime.config(text = "Worst: " + str(maximum))
            return maximum, minimum
        
        if len(self.validTimes) <= 4:
            return None

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

#Triggers any key presses based on the event driven paradigm
def keyFunctions(event):
    if puzzleChoice.get() == "":
        messagebox.showerror("Error!", "You must select a puzzle type before running!")
        
    elif event.keysym == "space" and scrambleText.cget("text") != "":
        timer.startTime()
    
    elif event.keysym in ["R", "r", "Escape"]:
        timer.resetTime()
    
    elif event.keysym == "Return" and not timer.running: #Different to not timer.running which affects if the timer is running
        scramble.updateScramble(puzzleChoice.get())

#Used to ask which colour is required here
def colourChooser(type, window):
    colour = colorchooser.askcolor() #Asks for the colour and returns a tuple containing an RGB integer Tuple and in Hexadecimal
    
    #Ensured that the colour gets picked without closing or cancelling the screen
    if type == "foreground" and colour[1] is not None:
        for item in window:
            item.config(foreground = colour[1].upper())
            
    elif type == "background" and colour[1] is not None:
        for item in window:
            item.config(background = colour[1].upper())
    
#Function provided to transfer between 2 different screens and to cancel the after once the timer is running  
def transferScreen(currentWindow, newWindow):
    if "dummyTimes.csv" in filepath: 
        with open(filepath, "w") as file:
            file.write("")
        
    global timerRunning
    if timerRunning is not None:
        currentWindow.after_cancel(timerRunning)
        timerRunning = None
    currentWindow.destroy()
    newWindow()
 
#Refreshing the same screen each time the user wants to refresh the screen   
def refreshScreen(currentWindow, sameWindow):
    if "dummyTimes.csv" in filepath: 
        with open(filepath, "w") as file:
            file.write("")

    global timerRunning
    if timerRunning is not None:
        currentWindow.after_cancel(timerRunning)
        timerRunning = None
    scramble.scrambleSet = None
    currentWindow.destroy()
    sameWindow()
    
    #Created with assistance
    with open(filepath, "r") as file:
        reader = csv.reader(file)
        timer.timerList = list(reader)

#Displays the font if the user is interested to know the kind of font that the user is currently using
def showFont(scramble, timer, stat):
    messagebox.showinfo("Fonts used!", "Scramble Font: " + scramble + "\n" + "Timer Font: " + timer + "\n" + "Stats Font: " + stat)

#Used to save a session into a file for later use
def saveSession():
    global filepath
    filepath = asksaveasfilename(defaultextension="csv", filetypes=[("CSV Files", ".csv"), ("All Files", "*.*")])
    
    if not filepath:
        return
    
    else:
        with open(filepath, "w", newline="") as file:
            writer = csv.writer(file)
            
            # Iterate over each row in the Treeview
            for item in table.get_children():  # Get each row (item) ID
                value = table.item(item, "values")  # Retrieve the row's values
                writer.writerow(value)  # Write values to the CSV file

#Loads any existing file within the specified filepath
def loadSession():
    global filepath
    count = 0
    filepath = askopenfilename(filetypes=[("CSV Files", ".csv"), ("All Files", "*.*")])
    
    if not filepath:
        return
    
    table.delete(*table.get_children())

    filepath = os.path.basename(filepath) #finds the base of the file
    
    with open(filepath, "r", newline = "") as file:
        reader = csv.reader(file)

        for item in reader:
            item = [element.strip() for element in item]
            
            if any(item):
                table.insert("", END, values = item)
                count += 1

    timer.update_mean_time()
        
#Creates the Rules and Regulation Pages for using the timer and how to use the system, uses a list of text and adding a new line per rule with a confirmation button
def rule_page():
    ruleWindow = Tk()
    ruleWindow.title("Rules Page")
    
    ruleFrame = Frame(ruleWindow, background = "white")
    
    ruleHeading = Label(ruleFrame, background = "white", foreground = "black", text = "Rules to Follow for the Rubiks Cube Timer!!!", font = ("Arial", 40, "bold", "underline"))
    ruleText = Label(ruleFrame, background = "white", foreground = "black", text = "Please read all rules below before using the timer! \n When generating a scramble, press either the 'Generate Scramble' button or the Enter Key \n Hand Options are available only for 2x2, this is your preference whether you want to use either RUF or LUF moves in your scrambles! \n The Scrambles are all Computer-Generated Sequences to scramble the cube, please scramble with White on Top and Green facing you! \n Start the timer by pressing the spacebar when you are ready to solve, DO NOT hold the spacebar as pressing and holding can cause confusion! \n Reset the timer with the R or Escape key. \n The System includes Penalties including the Plus 2 and DNFs. \n Please input them accordingly and ensure that you do it safely as this is irreversible like most diagnoses and prescription medicines!!! \n Be Careful, once you set it, you cannot set it back to the original time! \n Only 1 plus 2 is used (instead of stacking it up) \n Try not to intentionally get a bad solve all the time! \n Currently this Software is written in Python with the Tkinter Module and is still in development! \n Have Fun Timing and Solving! \n This is just a developing and improving version, there is an old version which doesn't have all features but still fun to use as a basic interface \n Thank You! press the 'OK' Button when you're ready to time solves!", font = ("Comic Sans Ms", 15, "bold"))
    
    buttonFrame = Frame(ruleWindow)
    timerButton = Button(buttonFrame, text = "Ok", command = lambda: transferScreen(ruleWindow, timer_page))
    foregroundButton = Button(buttonFrame, text = "Choose Foreground", command = lambda: colourChooser("foreground", [ruleHeading, ruleText, timerButton, foregroundButton, backgroundButton]))
    backgroundButton = Button(buttonFrame, text = "Choose Background", command = lambda: colourChooser("background", [ruleWindow, ruleFrame, buttonFrame, ruleHeading, ruleText, timerButton, foregroundButton, backgroundButton]))
    
    #Places and adds all labels, frames and buttons within the GUI interface
    ruleFrame.pack(fill = BOTH)
    ruleHeading.pack()
    ruleText.pack()
    buttonFrame.pack()
    foregroundButton.pack()
    backgroundButton.pack()
    timerButton.pack()
    
    return ruleWindow

#Main timer page
def timer_page():
    #Globalising the variables
    global scrambleText, timerText, puzzleChoice, timerWindow, handChoice, table, columns, numFails, numSolves, currentMean, bestMean, bestTime, worstTime, standard_deviation, current_average_5, current_average_12, best_average_5, best_average_12
    
    #Creating the windows and the title
    timerWindow = Tk()
    timerWindow.title("Rubik's Cube Timer Page")
    
    #Randomising fonts each time
    scrambleFont, timerFont, statFont = random.choice(FONTS), random.choice(FONTS), random.choice(FONTS)
    
    timerFrame = Frame(timerWindow)
    timerWindow.bind("<Key>", keyFunctions)
    scrambleText = Label(timerFrame, text = "", font = (scrambleFont, 20, "bold"))
    timerText = Label(timerFrame, text = "00.00", font = (timerFont, 40, "bold"))
    
    frame = Frame(timerWindow)
    originalButton = Button(frame, text = "Original Time (Click only if your timer currently shows Penalties)", command = timer.goodSolve)
    plus2Button = Button(frame, text = "+2", command = timer.plusTwo)
    did_not_finish_button = Button(frame, text = "DNF (Did Not Finish)", command = timer.unSolved)
    generateScramble = Button(frame, text = "Generate Scramble", command = lambda: scramble.updateScramble(puzzleChoice.get()))
    submitButton = Button(frame, text = "Submit Time", command = timer.submission)
    
    optionFrame = Frame(timerWindow)
    puzzleChoice = StringVar()
    option = OptionMenu(optionFrame, puzzleChoice, "2x2", "3x3", "3x3 One Handed", "3x3 Blindfolded", "4x4", "Pyraminx", "Skewb")
    
    handChoice = StringVar()
    handOption = OptionMenu(optionFrame, handChoice, "Left Handed", "Right Handed")
    
    buttonFrame = Frame(timerWindow, highlightbackground = "black", highlightthickness = 2)
    ruleButton = Button(buttonFrame, text = "View Rules", command = lambda: transferScreen(timerWindow, rule_page))
    refreshButton = Button(buttonFrame, text = "Refresh Screen", command = lambda: refreshScreen(timerWindow, timer_page))
    showFonts = Button(buttonFrame, text = "Show Fonts", command = lambda: showFont(scrambleFont, timerFont, statFont))
    foregroundButton = Button(buttonFrame, text = "Choose Foreground", command = lambda: colourChooser("foreground", [scrambleText, standard_deviation, timerText, numSolves, numFails, currentMean, bestMean, bestTime, worstTime, current_average_5, current_average_12, best_average_5, best_average_12, originalButton, plus2Button, did_not_finish_button, generateScramble, ruleButton, refreshButton, submitButton, showFonts, foregroundButton, backgroundButton, saveButton, loadButton]))
    backgroundButton = Button(buttonFrame, text = "Choose Background", command = lambda: colourChooser("background", [timerWindow, timerFrame, buttonFrame, optionFrame, frame, tableFrame, statsFrame, scrambleText, timerText, standard_deviation, numSolves, numFails, currentMean, bestMean, bestTime, worstTime, current_average_5, current_average_12, best_average_5, best_average_12, originalButton, plus2Button, did_not_finish_button, generateScramble, ruleButton, refreshButton, submitButton, showFonts, foregroundButton, backgroundButton, saveButton, loadButton]))
    saveButton = Button(buttonFrame, text = "Save Times", command = saveSession)
    loadButton = Button(buttonFrame, text = "Load Times", command = loadSession)
    
    tableFrame = Frame(timerWindow, highlightbackground = "black", highlightthickness = 2)
    table = ttk.Treeview(tableFrame)
    table["columns"] = columns = ("Time", "Scramble", "Date and Time", "Puzzle Type")
    
    statsFrame = Frame(timerWindow)
    numSolves = Label(statsFrame, text = "Number of Solves: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    numFails = Label(statsFrame, text = "Number of DNFs: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    currentMean = Label(statsFrame, text = "Current Mean: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    bestMean = Label(statsFrame, text = "Best Mean: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    current_average_5 = Label(statsFrame, text = "Current Average of 5: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    best_average_5 = Label(statsFrame, text = "Best Average of 5: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    current_average_12 = Label(statsFrame, text = "Current Average of 12: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    best_average_12 = Label(statsFrame, text = "Best Average of 12: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    bestTime = Label(statsFrame, text = "Best Time: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    worstTime = Label(statsFrame, text = "Worst Time: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    standard_deviation = Label(statsFrame, text = "Standard Deviation: ", font = (statFont, 10, "bold"), highlightbackground = "black", highlightthickness = 2)
    
    table.column("#0", width = 0, stretch = NO)
    table.column("Time", width = 75, minwidth = 25, anchor = N)
    table.column("Scramble", width = 300, minwidth = 25, anchor = N)
    table.column("Date and Time", width = 150, minwidth = 25, anchor = N)
    table.column("Puzzle Type", width = 150, minwidth = 25, anchor = N)
    
    table.heading("Time", text = "Time")
    table.heading("Scramble", text = "Scramble")
    table.heading("Date and Time", text = "Date and Time")
    table.heading("Puzzle Type", text = "Puzzle Type")
    
    timerFrame.grid(row = 0, column = 0)
    scrambleText.grid(row = 1, column = 0, padx = 5, pady = 5)
    timerText.grid(row = 2, column = 0, padx = 5, pady = 5)
    
    optionFrame.grid(row = 3, column = 0)
    option.grid(row = 3, column = 0, padx = 5, pady = 5)
    handOption.grid(row = 3, column = 1, padx = 5, pady = 5)
    
    frame.grid(row = 4, column = 0)
    originalButton.grid(row = 4, column = 0, padx = 5, pady = 5)
    plus2Button.grid(row = 4, column = 1, padx = 5, pady = 5)
    did_not_finish_button.grid(row = 4, column = 2, padx = 5, pady = 5)
    generateScramble.grid(row = 4, column = 3, padx = 5, pady = 5)
    submitButton.grid(row = 4, column = 4, padx = 5, pady = 5)
    
    tableFrame.grid(row = 5, column = 0, padx = 5, pady = 5)
    table.grid(row = 5, column = 0, padx = 5, pady = 5)
    
    statsFrame.grid(row = 6, column = 0, padx = 5, pady = 5)
    numSolves.grid(row = 6, column = 0, padx = 5, pady = 5)
    numFails.grid(row = 6, column = 1, padx = 5, pady = 5)
    currentMean.grid(row = 6, column = 2, padx = 5, pady = 5)
    bestMean.grid(row = 6, column = 3, padx = 5, pady = 5)
    current_average_5.grid(row = 6, column = 4, padx = 5, pady = 5)
    best_average_5.grid(row = 6, column = 5, padx = 5, pady = 5)
    current_average_12.grid(row = 6, column = 6, padx = 5, pady = 5)
    best_average_12.grid(row = 6, column = 7, padx = 5, pady = 5)
    bestTime.grid(row = 6, column = 8, padx = 5, pady = 5)
    worstTime.grid(row = 6, column = 9, padx = 5, pady = 5)
    standard_deviation.grid(row = 7, column = 0, padx = 5, pady = 5)
    
    buttonFrame.grid(row = 8, column = 0)
    showFonts.grid(row = 8, column = 1, padx = 5, pady = 5)
    ruleButton.grid(row = 8, column = 2, padx = 5, pady = 5)
    refreshButton.grid(row = 8, column = 3, padx = 5, pady = 5)
    foregroundButton.grid(row = 8, column = 4, padx = 5, pady = 5)
    backgroundButton.grid(row = 8, column = 5, padx = 5, pady = 5)
    saveButton.grid(row = 8, column = 6, padx = 5, pady = 5)
    loadButton.grid(row = 8, column = 7, padx = 5, pady = 5)

    return timerWindow

scramble, timer = Scramble(), Timer()

timerWindow = timer_page()
timerWindow.mainloop()