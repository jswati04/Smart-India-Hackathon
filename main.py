import json
import smtplib
import matplotlib as mpl
import sys
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
from tkinter import *
import tkinter.messagebox
import json
from random import uniform
import numpy as np
import pandas as pd
import os.path
import math
from random import uniform, randint, choices, choice
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
#tkinter modules and related alll
root=Tk()
#intialization of the allthe variables
df=pd.DataFrame()#contains the hydraulic fluid data frame
WELCOME_MSG = '''Welcome to the fire data analysis portal '''
WELCOME_DURATION = 5000
frm= Frame(root)
hydraulic_fluid_data=pd.DataFrame()#contains the data of the data of the hydraulic fluids
hydraulicfluids=0#hydraulicfluids number of rows
coalmines=0#coal mines number of rows
hydraulic_fluid_data=0
l=0
splitratio=0
coal_mine_data=0
coal_mine_dataframe=pd.DataFrame()
text1=Text(frm,width=1000 ,height=700)
text2=Text(frm,width=1000 ,height=700)
b3=Button(frm,text="Show hydraulic fluid")
b4=Button(frm,text="Show coal mines")
k=pd.DataFrame(columns=["FluidID",	"Auto_Ignition_Temp","Heat_of_Combustion","Flame_Propagation_Speed","Flash_Point","Fire_Point","Spray_Flammability","Viscosity_Temp_Properties","Seal_Compatibility","Lubricating_Quality","Relative_Cost"])
#intialization of variables ends here
#code begins for the welcome message
def destroy():#Welcome message destroy code here written
    k.destroy()
    menu = Menu(root)  # main menu
    # gdata=Menu(menu)#Generate data menu
    root.config(menu=menu)
    #menu.add_cascade(label="Generate Data",menu=gdata)
    #gdata.add_command(label="Generate Data",command=generating)
    subgenerate=Menu(menu, tearoff = 0)
    menu.add_cascade(label="Generate Data",menu=subgenerate)
    subgenerate.add_command(label="Random Data", command=generating)
    subgenerate.add_command(label="Select File to Upload",command=select)#Code to be added
    subgenerate.add_command(label="Write to CSV File",command=writecsv)
    
    subtest =Menu(menu, tearoff = 0)#subset of the test menu
    menu.add_cascade(label="Test Data",menu=subtest)
    subtest.add_command(label="Split Data",command=split)
    subtest.add_command(label="Enter test data", command=enterdata)
    menu.add_command(label="View Results",command=result)
    menu.add_command(label="Exit",command=l)
    z=Label(frm,text="FIRE HACKERS WELCOMES YOU",fg="Blue",font = "Helvetica 40 bold")
    z.pack(side=LEFT)
def l():
    root.destroy()
 #Non GUI PART STATRTS
    # Function to parse a JSON Schema
def parse_json(address):
    with open(address) as data_file:    
        data = json.load(data_file)
    return data
    # Function to generate hyraulic fluid data
# Function to generate hyraulic fluid data
def generate_fluid_data(address, num):
    schema = parse_json(address)
    properties = schema['properties']
    
    headers = []
    relations = []
    maximum = []
    minimum = []
    safety_prob_weights = [0.1, 0.05, 0.05, 0.2, 0.3, 0.3]
    usage_prob_weights = [0.27, 0.27, 0.27, 0.19]
    
    for i in list(properties.keys()):
        headers.append(i)
        
        if i == 'FluidID':
            continue
        
        try:
            relations.append(properties[i]['relation'])
            maximum.append(float(properties[i]['max']))
            minimum.append(float(properties[i]['min']))
        except:
            pass
            
    
    dataset = []
    n = len(headers)-2
    c = 6 #no. of factors that affect the safety score
    
    dataset.append(headers)
    
    #Actual Data Generation
    for i in range(num):
        arr = []
        arr.append(i+1);
        safety_sum = 0.0
        usage_sum = 0.0
        
        #Safety Score Calculation
        for j in range(c):
            if headers[j+1]=='Fire_Point':
                val = uniform(val, val+50)
            else:
                val = uniform(minimum[j], maximum[j])
                
            arr.append(round(val, 1))
            
            if relations[j]=='inverse':
                val = minimum[j] / val
                safety_sum += safety_prob_weights[j] * val
            else:
                safety_sum += safety_prob_weights[j] * (val / maximum[j])
            
        safety_sum /= c
    
        #Usability Factor Calculation
        for j in range(n-1-c):
            val = uniform(minimum[n-c+1+j], maximum[n-c+1+j])
            arr.append(round(val, 1))
            if relations[j]=='inverse':
                val = minimum[n-c+1+j] / val
                usage_sum += usage_prob_weights[j] * val
            else:
                usage_sum += usage_prob_weights[j] * (val / maximum[n-c+1+j])
            
        usage_sum /= (n-c-1)       
        #write as percentage of ideal fluid
        arr.append(round((safety_sum*100), 2))
        arr.append(round((usage_sum*100), 2))
        dataset.append(arr)    
    return dataset

# function to generate coal mines data
def generate_mines_data(address, num, fluid_data):
    schema = parse_json(address)
    properties = schema['properties']
    
    headers = []
    types = []
    maximum = []
    minimum = []
    relations = []
    
    for i in list(properties.keys()):
        headers.append(i)
        types.append(properties[i]['type'])
        
        try:
            if properties[i]['type'] == 'number':
                maximum.append(float(properties[i]['max']))
                minimum.append(float(properties[i]['min']))
            elif properties[i]['type'] == 'integer':
                maximum.append(int(properties[i]['max']))
                minimum.append(int(properties[i]['min']))
        except:
            pass
        
        try:
            relations.append(properties[i]['relation'])
        except:
            pass    
    dataset = []
    dataset.append(headers)
    num = 200
    mine_types = ['open-cast', 'underground', 'both']
    safety_prob_weights = [0.32, 0.16, 0.16, 0.12, 0.12, 0.12]
    
    for i in range(num):
        arr = []
        
        #Mine ID
        arr.append(i+1)
        
        #Mine Type
        type_of_mine = choices(mine_types, weights = [0.396, 0.534, 0.07])
        arr.append(type_of_mine[0])
        
        #Fluid Score
        total = 0.0
        score = 0.0
        numFluids = randint(3, 7)
        fluids = choices(range(1, 51), k=numFluids)
        for j in range(numFluids):
            total += fluid_data[fluids[j]][-1]
        for j in range(numFluids):
            score += fluid_data[fluids[j]][-2] * (fluid_data[fluids[j]][-1] / total)
        arr.append(round(score, 2))
        
        #Percentage of Inflammable Gas & Rate of Emission
        avg_igas = 0.0
        avg_rate = 0.0
        
        if type_of_mine[0] != 'open-cast':
            no_of_seams = randint(5, 20)
            
            for j in range(no_of_seams):
                degree = choices(['I', 'II', 'III'], weights = [0.72, 0.24, 0.04])
                
                if degree == 'I':
                    igas = uniform(minimum[0], 0.1)
                    rate = uniform(minimum[1], 1)
                    
                elif degree == 'III':
                    igas = uniform(minimum[0], maximum[0])
                    rate = uniform(10, maximum[1])
                    
                else:
                    igas = uniform(minimum[0], maximum[0])
                    rate = uniform(minimum[1], maximum[1])
                    while igas < 0.1 or (rate < 1 or rate > 10):
                        igas = uniform(minimum[0], maximum[0])
                        rate = uniform(minimum[1], maximum[1])
                
                avg_igas += igas
                avg_rate += rate
            
            avg_igas /= no_of_seams
            avg_rate /= no_of_seams
            
        arr.append(round(avg_igas, 2))
        arr.append(round(avg_rate, 2))
            
        #Oxygen Content
        arr.append(round(uniform(minimum[2], maximum[2]), 2))
        
        #Relative Humidity
        arr.append(round(uniform(minimum[3], maximum[3]), 2))
        
        #No. of Workers
        arr.append(randint(minimum[4], maximum[4]))
        
        #Calculation of overall Safety Score
        n = len(maximum)
        total = 0.0
        for j in range(n):
            val = arr[j+2]
            if(relations[j]=='inverse' and val != 0):
                val = minimum[j] / val
                total += safety_prob_weights[j] * val
            else:
                total += safety_prob_weights[j] * (val / maximum[j])
            
        total /= n
        
        #write as percentage
        arr.append(round((total*100), 2))
        
        dataset.append(arr)
    
    return dataset

#NON GUI PART ENDS

def generating():# Data is being generated for the  randomly for the menu genrate data
    global hydraulicfluids#hydraulicfluids number of rows
    global coalmines#coal mines number of rows
    global hydraulic_fluid_data#hydraulic fluids data contain
    global df
    print("Data is being generated")    
    for widget in frm.winfo_children():# frame childrens whatever before will be automaticaly destroyed
            widget.destroy()   
    z=Label(frm,text="FIRE HACKERS PORTAL",fg="Blue",font = "Helvetica 20 bold")
    z.pack(side=TOP)
    l1=Label(frm,text="Number of data-points to be generated -->",font = "Helvetica 10")
    #l1.grid(row=15,column=3,)
    l1.pack(side=TOP)
    l2=Label(frm,text="Hydraulic Fluids",font = "Helvetica 10")
    #l2.grid(row=16,column=3)
    l2.pack()
    e1=Entry(frm,font = "Helvetica 10")
    e1.insert(END,'100')
    #e1.grid(row=16,column=4H
    e1.pack()
    l3=Label(frm,text="Coal Mines",font = "Helvetica 10")
    #l3.grid(row=17,column=3)
    l3.pack()
    e2=Entry(frm,font = "Helvetica 10")
    e2.insert(END,'100')
    #e2.grid(row=17,column=4)    
    e2.pack()
    def sub():
        global hydraulicfluids
        global coalminesshydraulicfluid_data
        global hydraulic_fluid_data
        global df
        global coal_mine_dataframe
        global coal_mine_data
        global text1
        global text2
        global b3
        global b4
        b3.destroy()
        b4.destroy()
        text1.destroy()
        text2.destroy()
        #hydraulic fluids         
        hydraulicfluids=int(e1.get())
        print(hydraulicfluids)
        #coal mines
        coalmines=int(e2.get())
        #NON GUI PART
        print(coalmines)
        print("aaa")
        hydraulic_fluid_schema = 'Schema/hydraulic_fluid.json'
        coal_mine_schema = 'Schema/coal_mines.json'
        print('Hydraulic Fluid Data')
        # number of data points for hydraulic fluids dataset
        # n_hydraulic_fluids = int(input('Enter number of data points for hydraulic fluids'))
        n_hydraulic_fluids = hydraulicfluids
        n_coal_mines =coalmines
        print(n_hydraulic_fluids)
        hydraulic_fluid_data = generate_fluid_data(hydraulic_fluid_schema, n_hydraulic_fluids)
        coal_mine_data = generate_mines_data(coal_mine_schema, n_coal_mines, hydraulic_fluid_data)
        """   for i in hydraulic_fluid_data:
            for j in i:
                print(j)"""
        
        #print(hydraulic_fluid_data)
        #button to print the data in a tabular format
        df = pd.DataFrame(hydraulic_fluid_data)
        coal_mine_dataframe = pd.DataFrame(coal_mine_data)
        

        #hydraulic fluids data to be printed the functions defination starts here
        def putthehydraulicfluid():
                    global df
                    global text1
                    global text2
                    text2.destroy()
                    text1 = Text(frm,width=1000 ,height=700,font = "Helvetica 10")                   
                    text1.insert(END, str(df.iloc[:,:]))
                    #text.grid(row=19,column=0)
                    text1.pack()
        b3=Button(frm,text="Show hydraulic fluid",command=  putthehydraulicfluid)
        #b3.grid(row=30)
        b3.pack()
        def putthecoalmines():
                global  coal_mine_dataframe
                global text1
                global text2
                text1.destroy()
                text2 = Text(frm,width=1000 ,height=700,font = "Helvetica 10")                   
                text2.insert(END, str(coal_mine_dataframe.iloc[:,:]))
                #text.grid(row=19,column=0)
                text2.pack()

        b4=Button(frm,text="Show coal mines",command= putthecoalmines,font = "Helvetica 10")
        b4.pack()
        #print(df)
        #NON GUI 
    gen = Button(frm,text="Generate",command=sub)
    gen.pack()
    print("Working")
    #nON GUI PART SOUMIK 
        
def select():
    #global df
    print("Select is working")
    for widget in frm.winfo_children():
        widget.destroy()
    z=Label(frm,text="FIRE HACKERS PORTAL",fg="Blue",font = "Helvetica 20 bold")
    z.grid(row=0,column=6,columnspan=2)
    l1=Label(frm,text="Enter the name of the file for hydralic fluid",font = "Helvetica 10 ")
    l1.grid(row=7,column=6)
    e1=Entry(frm,font = "Helvetica 10")
    e1.insert(END,'m.csv')
    e1.grid(row=7,column=7)
    e2=Entry(frm,font = "Helvetica 10")
    e2.insert(END,'q.csv')
    e2.grid(row=9,column=7)
    l2=Label(frm,text="Enter the name of the file for coal mine",font = "Helvetica 10")
    l2.grid(row=9,column=6)
    def cmd():
         s=e1.get()
         l=e2.get()
         if os.path.isfile(s) and os.path.isfile(l):
             df=pd.read_csv(s)
             coal_mine_dataframe=pd.read_csv(l)  
             tkinter.messagebox.showinfo("OK","Data has been succesfully uploaded")
             if df == None or coal_mine_dataframe == None:
                tkinter.messagebox.showinfo("Error","Data frame has no value ")               
         else:
            tkinter.messagebox.showinfo("Error","Path of the files don't exist ")               
    bt=Button(frm,text="Submit",command=cmd,font = "Helvetica 10")
    bt.grid(rows=11,column=6,columnspan=2)
    print(hydraulic_fluid_data)
    #print(df)
    print("GOOOD WORK DONE")

def writedata():
        print("Writing data")
        
    
def writecsv():
    global df
    global coal_mine_dataframe
    print("Writing data to csv")
    for widget in frm.winfo_children():# frame childrens whatever before will be automaticaly destroyed
            widget.destroy()
    z=Label(frm,text="FIRE HACKERS PORTAL",fg="Blue",font = "Helvetica 20 bold")
    z.grid(row=0,column=6,columnspan=2)
    s=Label(frm,text="Enter the name of the file in which you want to write data for")
    l = Label(frm,text="Hydraulic fluid",font = "Helvetica 10")
    l.grid(row= 8,column=6)
    j = Entry(frm,font = "Helvetica 10")
    j.insert(END,'hydraulicfluid.csv')
    j.grid(row=8,column=7,columnspan=2)
    q = Label(frm,text="Coal mines",font = "Helvetica 10")
    q.grid(row= 9,column=6)
    m = Entry(frm)
    m.insert(END,'coalminedatarel.csv')
    m.grid(row=9,column=7,columnspan=2)
    
    def s():
        global df
        ze=j.get()
        qe=m.get()
        print(j) 
        if df.empty and  coal_mine_dataframe.empty :
            print("appp")
            tkinter.messagebox.showinfo("Error",'There is no value to be writen in the csv file for hydraulic fluid and coal mine. So please generate the data')
        else :
            def write_data_to_csv(address, dataset):
                dataset.to_csv(address, sep=',', header=True)
            write_data_to_csv(ze,df)
            write_data_to_csv(qe,coal_mine_dataframe)
            tkinter.messagebox.showinfo("OK","Data has been succesfully written")
    k=Button(frm,text="Write",command=s,font = "Helvetica 10")
    k.grid(row=13,column=6,columnspan=2)
def subtest():
    print("Data is being generated")

'''def result():
    print("Data is being generated")'''

def split():
    global splitratio
    global df
    global coal_mine_dataframe
    # generate the feature matrix
    for widget in frm.winfo_children():# frame childrens whatever before will be automaticaly destroyed
            widget.destroy()
    z=Label(frm,text="FIRE HACKERS PORTAL",fg="Blue",font = "Helvetica 20 bold")
    z.grid(row=0,column=6,columnspan=2)
    #print("Data is being split")
    print("Data is being split ")
    l1=Label(frm,text="Enter the data the test datasets's ratio in percentage",font = "Helvetica 10")
    l1.grid(row=6,column=6)
    e1 = Entry(frm,font = "Helvetica 10")
    e1.insert(END,'20')
    e1.grid(row=6,column=7)
   
    # print(s)
    def cd():
        global splitratio
        if df.empty or coal_mine_dataframe.empty :
             tkinter.messagebox.showinfo("Error",'There is no dataset to split on ')
        else:    
           splitratio=float(float(e1.get())/100)
           if(splitratio>.50):
                tkinter.messagebox.showinfo("Error",'The splir ratio should be less than 50% ')
           else:
             print(splitratio)
             X = coal_mine_dataframe.iloc[:, 1:-1].values
             y = coal_mine_dataframe.iloc[:, 1].values
             X = list(X)
             X.pop(0)
             X = np.array(X)
             y = list(y)
             y.pop(0)
             y = np.array(y)
             # Encoding categorical variable in feature matrix
             labelencoder_X = LabelEncoder()
             X[:, 0] = labelencoder_X.fit_transform(X[:, 0])
             onehotencoder = OneHotEncoder(categorical_features = [0])
             X = onehotencoder.fit_transform(X).toarray()
             # Avoiding dummy variable trap
             X = X[:, 1:]
             # Encoding the Dependent Variable
             labelencoder_y = LabelEncoder()
             y = labelencoder_y.fit_transform(y)
             # Splitting dataset in train and test
             from sklearn.model_selection import train_test_split
             X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = splitratio, random_state = 0)
             clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
             clf.fit(X_train, y_train)
             # Prediction on test set
             y_pred = clf.predict(np.array(X_test))
             # Confusion matrix
             cm=confusion_matrix(y_test, y_pred)
             correct_predictions = 0
             for i in range(len(cm)):
                   correct_predictions += cm[i][i]
             false_predictions = len(y_test) - correct_predictions
             accuracy = (correct_predictions - false_predictions) * 100 / len(y_test)
             print('Accuracy:', accuracy, '%')
             l=Label(frm,text="The percentage accuracy is "+str(accuracy)+"%")
             l.grid(row=15,column=6,columnspan=2)
             #print(splitratio)             
    b=Button(frm,text="Split the data",command=cd)
    b.grid(row=9,column=6,columnspan=2)
    
def result():
    #print("Results is being displayed")
    def draw_figure(canvas, figure, loc=(0, 0)):
        """ Draw a matplotlib figure onto a Tk canvas
    
        loc: location of top-left corner of figure on canvas in pixels.
        Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
        """
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = PhotoImage(master=canvas, width=figure_w, height=figure_h)
    
        # Position: convert from top-left anchor to center anchor
        canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)
    
        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        
    
        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return photo
    w, h = 300, 200
    window = Tk()
    window.title("A figure in a canvas")
    canvas = Canvas(window, width=w, height=h)
    canvas.pack()
    
    # Generate some example data
    X = np.linspace(0, 2 * np.pi, 50)
    Y = np.sin(X)
    
    # Create the figure we desire to add to an existing canvas
    fig = mpl.figure.Figure(figsize=(2, 1))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.plot(X, Y)
    
    # Keep this handle alive, or else figure will disappear
    fig_x, fig_y = 100, 100
    fig_photo = draw_figure(canvas, fig, loc=(fig_x, fig_y))
    fig_w, fig_h = fig_photo.width(), fig_photo.height()
    
    # Add more elements to the canvas, potentially on top of the figure
    canvas.create_line(200, 50, fig_x + fig_w / 2, fig_y + fig_h / 2)
    canvas.create_text(200, 50, text="Zero-crossing", anchor="s")
    
    # Let Tk take over
    mainloop()
def sendmail():
    #print("abc")
    content = 'Fire Hazard Alert!!!'
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('debanjan.banerjee98@gmail.com', '9933545223')
    mail.sendmail('debanjan.banerjee98@gmail.com', 'anish.pathak5@gmail.com', content)
    mail.close()

def enterdata():
    sendmail()
    print("The data is being entered")
    for widget in  frm.winfo_children():# frame childrens whatever before will be automaticaly destroyed
            widget.destroy()   
    z=Label(frm,text="FIRE HACKERS PORTAL",fg="Blue",font = "Helvetica 20 bold")
    z.grid(row=0,column=6,columnspan=2)
    l1=Label(frm,text="If you want to enter data in")
    l1.grid(row=3,column=6,columnspan=2)
    def hydralic():
        global k
        l3=Label(frm,text="Enter the number of sample you want to insert")
        l3.grid(row=6,column=6,columnspan=3)
        l=Entry(frm)
        l.grid(row=6,column=9)
        
        def q():
            s=int(l.get())
            if s>=3:
                i=0
                print("Ok")
                r=7
                c=9
                if df.empty:  
                    tkinter.messagebox.showinfo("Error","The data frame is empty first insert the data")
                else:
                  global k
                  #d=["FluidID",	"Auto_Ignition_Temp","Heat_of_Combustion","Flame_Propagation_Speed","Flash_Point","Fire_Point","Spray_Flammability","Viscosity_Temp_Properties","Seal_Compatibility","Lubricating_Quality","Relative_Cost"]
                  #k=pd.DataFrame(d)
                  i=0
                  for i in range(s):
                        r=7
                        print("Apple")
                        f1=Label(frm,text="Enter the fluid id")
                        f1.grid(row=r,column=c)
                        e1=Entry(frm)
                        e1.grid(row=r,column=c+1)
                        r=r+1
                        f2=Label(frm,text="Enter the Auto Ignition Temp")
                        f2.grid(row=r,column=c)
                        e2=Entry(frm)
                        e2.grid(row=r,column=c+1)
                        r=r+1
                        f3=Label(frm,text="Enter the Heat of Combustion")
                        f3.grid(row=r,column=c)
                        e3=Entry(frm)
                        e3.grid(row=r,column=c+1)
                        r=r+1
                        f4=Label(frm,text="Enter the Flame Propagation Speed")
                        f4.grid(row=r,column=c)
                        e4=Entry(frm)
                        e4.grid(row=r,column=c+1)
                        r=r+1
                        f5=Label(frm,text="Enter the Flash_Point")
                        f5.grid(row=r,column=c)
                        e5=Entry(frm)
                        e5.grid(row=r,column=c+1)
                        r=r+1
                        f6=Label(frm,text="Enter the Fire_Point")
                        f6.grid(row=r,column=c)
                        e6=Entry(frm)
                        e6.grid(row=r,column=c+1)
                        r=r+1
                        f7=Label(frm,text="Enter the Spray Flammability")
                        f7.grid(row=r,column=c)
                        e7=Entry(frm)
                        e7.grid(row=r,column=c+1)
                        r=r+1
                        f8=Label(frm,text="Enter the Viscosity Temp Properties")
                        f8.grid(row=r,column=c)
                        e8=Entry(frm)
                        e8.grid(row=r,column=c+1)
                        r=r+1
                        f9=Label(frm,text="Enter the Seal Compatibility")
                        f9.grid(row=r,column=c)
                        e9=Entry(frm)
                        e9.grid(row=r,column=c+1)
                        r=r+1
                        f10=Label(frm,text="Enter the Lubricating Quality")
                        f10.grid(row=r,column=c)
                        e10=Entry(frm)
                        e10.grid(row=r,column=c+1)
                        r=r+1
                        f11=Label(frm,text="Enter the Relative_Cost")
                        f11.grid(row=r,column=c)
                        e11=Entry(frm)
                        e11.grid(row=r,column=c+1)
                        r=r+1
                        
                        def des():
                            #sendmail()
                            global k
                            k=pd.DataFrame()
                            print("Apple2")
                            g1=int(e1.get())
                            print(g1)
                            g2=float(e2.get())
                            g3=float(e3.get())
                            g4=float(e4.get())
                            g5=float(e5.get())
                            g6=float(e6.get())
                            g7=float(e7.get())
                            g8=float(e8.get())
                            g9=float(e9.get())
                            g10=float(e10.get())
                            g11=float(e11.get())
                            print(str(g10))
                            print("c")
                            d3=[g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11]
                            k.append(d3,ignore_index=True)
                            print(k)
                            f1.forget()
                            f2.forget()
                            f3.forget()
                            f4.forget()
                            f5.forget()
                            f6.forget()
                            f7.forget()
                            f8.forget()
                            f9.forget()
                            f10.forget()
                            f11.forget()
                            e1.forget()
                            e2.forget()
                            e3.forget()
                            e4.forget()
                            e5.forget()
                            e6.forget()
                            e7.forget()
                            e8.forget()
                            e9.forget()
                            e10.forget()
                            e11.forget()
                        sub.grid(row=r,column=c,columnspan=2)
                        b3=Button(frm,text="Submit",command=q)
            else:
                tkinter.messagebox.showinfo("Error","Less than three values have been inserted")
        b3=Button(frm,text="Submit",command=q)
        b3.grid(row=7,column=6,columnspan=2)
    b1=Button(frm,text="Hydralic fluid",command=hydralic)
    b1.grid(row=5,column=6)
    b2=Button(frm,text="Coal mine")
    b2.grid(row=5,column=7)
#root title and all
root.title("Fire data analysis")#Last part of the code
root.wm_attributes("-fullscreen", True)
#root.configure(bg='blue')

k=Label(root,text="Fire Hazards Analysis Portal",fg = "light green",bg = "dark green",font = "Helvetica 50 bold")
#k.pack(anchor=CENTER,fill=X)
k.place(relx=0.5, rely=0.5, anchor=CENTER)
frm=Frame(root)
k.after(2000,destroy)
frm.pack()
root.bind("<Escape>",quit)
root.mainloop()