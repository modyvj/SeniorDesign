
"""
The basis of the code used the generate the ASYNCHRONOUS I/o was taken from...
 http://code.activestate.com/recipes/82965-threads-tkinter-and-asynchronous-io/...
 Created by Jacob Hallén, AB Strakt, Sweden. 2001-10-17n
"""


import tkinter
from tkinter import *
import time
import threading
import random
import queue
import serial
from serial import threaded
import os
import sys
import numpy as np
from tkinter.filedialog import askopenfilename


__author__= 'Vishal Mody'

global fileName

ActiveJoint = 'X' # no joint is Active
Joint_A= "A"
Joint_B="B"
Joint_C="C"
color = 1 ### not sure
LinkLength1 = 30.5
LinkLength2 = 30.5
currxpos = int
currypos = int
currzpos = int

currapos = int
currbpos = int
currcpos = int


class App:
    def __init__(self, master, ser, queue, endCommand, ):
        self.queue = queue

        Qbutton = Button(master, text='Quit', command=endCommand,highlightbackground="lime green").grid(row=0)
        msg = StringVar()


        ####### THe min and Max for each stepper motors rotary encoder
        JaRotMax = 24
        JaRotMin = 0
        JbRotMax = 180
        JbRotMin = 0
        JcRotMax = 315
        JcRotMin = 0
        LinkLength3 =30.5
        LinkLength4 =30.5

        ####### Checkbox Variable for Radiobutton
        checka1 = int()
        checka2 = int()
        checka3 = int()
        checka4 = int()


        self.RecordCheck_text = IntVar()
        self.LazerCheck_text = IntVar()

        ####### IntVariable for steppers and X,Y,Z
        self.J1_total_label_text = IntVar()
        self.J2_total_label_text = IntVar()
        self.J3_total_label_text = IntVar()

        self.X_total_label_text = IntVar()
        self.Y_total_label_text = IntVar()
        self.Z_total_label_text = IntVar()

        self.ser = ser

        ##### ###############################################################
        ####          Stepper ANGLE/ RadioButton HEIGHT Variables Placement and Def

        self.J1_total = 0
        self.J2_total = 0
        self.J3_total = 0

        self.J1_total_label_text.set(self.J1_total)
        self.J2_total_label_text.set(self.J2_total)
        self.J3_total_label_text.set(self.J3_total)

        self.J1_total_label = Label(master, textvariable=self.J1_total_label_text, background="pale green")
        self.J2_total_label = Label(master, textvariable=self.J2_total_label_text, background="pale green")
        self.J3_total_label = Label(master, textvariable=self.J3_total_label_text, background="pale green")

        self.J1_Value = Entry(master, highlightbackground="lime green", width=12)
        self.J2_Value = Entry(master, highlightbackground="lime green", width=12)
        self.J3_Value = Entry(master, highlightbackground="lime green", width=12)

        self.J1_Value.grid(row=3, column=1)
        self.J2_Value.grid(row=4, column=1)
        self.J3_Value.grid(row=5, column=1)

        self.R1 = Radiobutton(master, text="Joint 1 (Cm)", variable=checka1, background="lime green", value=1,
                              command=self.activate_J1).grid(row=3)
        self.R2 = Radiobutton(master, text="Joint 2 (Deg)", variable=checka2, background="lime green", value=2,
                              command=self.activate_J2).grid(row=4)
        self.R3 = Radiobutton(master, text="Joint 3 (Deg)", variable=checka3, background="lime green", value=3,
                              command=self.activate_J3).grid(row=5)

        #### Joint values location
        self.J1_total_label.grid(row=3, column=3, sticky=W)
        self.J2_total_label.grid(row=4, column=3, sticky=W)
        self.J3_total_label.grid(row=5, column=3, sticky=W)

        ###### ###############################################################
        #####           Frames and Labels

        frame1 = Frame(master, bg="lime green")
        frame2 = Frame(master, bg="lime green")
        frame1.grid(row=7, column=1)
        frame2.grid(row=7, column=10)
        frame3 = Frame(master, bg="lime green")  # frame for Kill
        frame3.grid(row=7, column=5, columnspan=3)
        frame4 = Frame(master, bg="lime green")  # frame for reading serial label
        frame4.grid(row=13, column=2 )  # , columnspan=7)

        Label(master, text="", background="lime green", width=3).grid(row=2, column=3)
        Label(master, text="", background="lime green", width=3).grid(row=2, column=9)

        self.SerialReading_label_text = StringVar()

        self.SerialString = "No Current Serial Input"
        self.SerialReading_label_text.set(self.SerialString)  #### used to set the
        Label(master, text="Serial Line:", background="lime green", ).grid(row=11, column=0)
        self.SerialReading_Label = Label(master, textvariable=self.SerialReading_label_text,background="pale green").grid(row =12 , column = 2, columnspan = 6)



        ###### ###############################################################
        #####               GO SUBMIT buttons

        self.Enter = Button(frame2,
                         text="Enter", padx=10, highlightbackground="lime green",
                         command=self.button_Enter, width=5)
        self.Enter.pack(side=LEFT)  # grid(row=7, column=10, padx=0, pady=0, sticky="nw")

        self.Submit = Button(frame1,
                             text="Submit", padx=10, highlightbackground="lime green",
                             command=self.button_Submit)
        self.Submit.pack(side=LEFT)  # .grid(row=7, column=10, padx=0, pady=0, sticky="nw")

        # self.Quit = Button(master,
        #                    text="Quit", highlightbackground="lime green",
        #                    command=quit)
        # self.Quit.grid(row=0, column=0, padx=0, pady=0, sticky="nw")  ##Quit Button Location

        ##### ###############################################################
        #######################  Arrow Keys LEFT RIGHT UP DOWN LOCATION

        self.Left = Button(master,
                           text="←", padx=10, highlightbackground="lime green",
                           command=self.button_Left)
        self.Left.grid(row=4, column=5, padx=0, pady=0, )  # sticky="nw")

        self.Right = Button(master,
                            text="→", padx=10, highlightbackground="lime green",
                            command=self.button_Right)
        self.Right.grid(row=4, column=7, padx=2, pady=0, )  # sticky="nw")

        self.Up = Button(master,
                         text="↑", padx=10, highlightbackground="lime green",
                         command=self.button_Up)
        self.Up.grid(row=3, column=6, padx=0, pady=0, )  # sticky="nw")

        self.Down = Button(master,
                           text="↓", padx=10, highlightbackground="lime green",
                           command=self.button_Down)
        self.Down.grid(row=5, column=6, padx=2, pady=0, )

        ##### ###############################################################
        #######################X Y Z point entry & Grid Placement

        # XYZ True position
        self.X_total = 0
        self.Y_total = 0
        self.Z_total = 0

        self.X_total_label_text.set(self.X_total)
        self.Y_total_label_text.set(self.Y_total)
        self.Z_total_label_text.set(self.Z_total)

        self.X_total_label = Label(master, textvariable=self.X_total_label_text, background="pale green")
        self.Y_total_label = Label(master, textvariable=self.Y_total_label_text, background="pale green")
        self.Z_total_label = Label(master, textvariable=self.Z_total_label_text, background="pale green")

        # XYZ labels/position
        Label(master, text="X (Cm)", background="lime green").grid(row=3, column=9, )
        Label(master, text="Y (Cm)", background="lime green").grid(row=4, column=9)
        Label(master, text="Z (Cm)", background="lime green").grid(row=5, column=9)

        self.X_total_label.grid(row=3, column=11, sticky=W)
        self.Y_total_label.grid(row=4, column=11, sticky=W)
        self.Z_total_label.grid(row=5, column=11, sticky=W)

        # XYZ entry values
        self.X_Value = Entry(master, highlightbackground="lime green", width=12)
        self.Y_Value = Entry(master, highlightbackground="lime green", width=12)
        self.Z_Value = Entry(master, highlightbackground="lime green", width=12)
        self.X_Value.grid(row=3, column=10)
        self.Y_Value.grid(row=4, column=10)
        self.Z_Value.grid(row=5, column=10)

        ####### ###############################################################
        ###########        Record, Laser, Read/Open, Kill LOCATION

        self.RecordCheck = Checkbutton(master, text="Record", onvalue="5", offvalue="0",
                                       variable=self.RecordCheck_text, background="lime green",
                                       command=self.start_Recording).grid(row=2, column=11, sticky=W)

        self.LazerCheck = Checkbutton(master, text="Laser", onvalue="6", offvalue="0",
                                      variable=self.LazerCheck_text, background="lime green",
                                      command=self.button_Laser).grid(row=6, sticky=W)

        self.Open = Button(master,
                           text="Read Txt", highlightbackground="lime green",
                           command=self.open_Text)
        self.Open.grid(row=0, column=11, padx=0, pady=0, sticky=E)  ### read txt file

        self.Kill = Button(frame3,
                           text="Start Motors", padx=10, highlightbackground="lime green",
                           command=self.button_Kill)
        self.Kill.pack(side=LEFT)

        ######## ###############################################################
        #########              Reset Clear1 CLear 2 Sweep

        self.Reset = Button(master,
                            text="Reset", highlightbackground="lime green",
                            command=self.button_Reset)
        self.Reset.grid(row=0, column=1, padx=0, pady=0, sticky="nw")

        self.Clear1 = Button(frame1,
                             text="Clear", highlightbackground="lime green",
                             command=self.clear_Text1, )
        self.Clear1.pack(side=LEFT)

        self.Clear2 = Button(frame2,
                             text="Clear", highlightbackground="lime green",
                             command=self.clear_Text2, )
        self.Clear2.pack(side=LEFT)

        # self.sweep = Button(master,
        #                     text="S", highlightbackground="lime green",
        #                     command=self.button_Sweep)

    ##################################################################################
    ############## ###############################################################
    #############

    #        self.get_SerialInput()

    #   self.sweep.grid(row=0, column=9, padx=0, pady=0, sticky="nw")

    ##################################################################################
    ############## ###############################################################
    #############         DEF  Functions

    ## Clear Text1 Angles
    def clear_Text1(self): # Clear Joint entry Boxes
        self.J1_Value.delete(0, END)
        self.J2_Value.delete(0, END)
        self.J3_Value.delete(0, END)


    def clear_Text2(self): # Clear XYZ entry Boxes
        self.X_Value.delete(0, END)
        self.Y_Value.delete(0, END)
        self.Z_Value.delete(0, END)

    ## Active Joints "_"XXX
    def activate_J1(self):  # Activate joint 1
        global ActiveJoint
        ActivePin = 9
        ActiveJoint = 'A'
        return ActiveJoint

    def activate_J2(self):  # Activate joint 2
        global ActiveJoint
        ActiveJoint = 'B'
        ActivePin = 10
        return ActiveJoint

    def activate_J3(self):  # Activate joint 3
        global ActiveJoint
        ActivePin = 11
        ActiveJoint = 'C'
        return ActiveJoint

    def activate_J4(self):  # Activate joint 4
        global ActiveJoint
        ActivePin = 12
        ActiveJoint = 'D'
        return ActiveJoint

    # def deselect_all(self):
    #     global ActivatePin
    #     ActivatePin = 0
    def encodeoutput(self,x):
        setTemp0 = ActiveJoint + str(x)
        setTemp1 = str(setTemp0)
        setTemp1 = str(App.check_SerialLength(self, setTemp1))
        print("encoded to:",setTemp1)
        return setTemp1

    def start_motors(self):
        self.ser.write("S000".encode())
        self.ser.flush()


    ########## Arrows Right Left Up Down
    def button_Left(self):  # Move Left Deg =Deg-1
        if (ActiveJoint == "B"):
            x = self.J2_total
        elif (ActiveJoint == "C"):
            x = self.J3_total
        else:
            print("Error: Incorrect Joint for OP")
            return
        #### subtract 1 degree to go left
        x = str(int(x)-1)   #####  incrementing x by -1
        setTemp1=App.encodeoutput(self,x)
        # setTemp0 = ActiveJoint + str(x)
        # setTemp1 = str(setTemp0)
        # setTemp1 = str(App.check_SerialLength(self, setTemp1))  ### make sure 4 chars
        self.ser.write(setTemp1.encode()) #### WRITE Serial code to Arduino
        print('Sending: ', setTemp1)
        # self.ser.flush()
        # App.start_motors(self)
        # self.ser.flush()
        # self.ser.write("S000".encode())


        # print(str(self.ser.readline().decode()))

    #    x = str(self.ser.readline())#.decode()) ########### this gets XXXX not b XXXX
    #    print ('this is ' + x)
    # print (self.ser.readline())#.rstrip())

    def button_Right(self):  # Move Right
        ### Delete RightLeftCOunter
        if (ActiveJoint == "B"):
            x = self.J2_total
        elif (ActiveJoint == "C"):
            x = self.J3_total
        else:
            print("Error: Incorrect Joint for OP")
            return
        #### subtract 1 degree to go left

        x = str(int(x) + 1)  #####  incrementing x by -1
        setTemp1 = App.encodeoutput(self, x)
        # setTemp0 = ActiveJoint + str(x)
        # setTemp1 = str(setTemp0)
        # setTemp1 = str(App.check_SerialLength(self, setTemp1))  ### make sure 4 chars
        self.ser.write(setTemp1.encode())  #### WRITE Serial code to Arduino
        print('Sending: ', setTemp1)
        # self.ser.flush()
        # self.ser.write("S000".encode())

    def button_Up(self):  # Move Up only available for A
        ### Delete RightLeftCOunter
        if (ActiveJoint == "A"):
            x = self.J1_total
        else:
            print("Error: Incorrect Joint for OP")
            return
        x = str(int(x) + 1)
        setTemp0 = ActiveJoint + str(x) #increment Z by +1
        setTemp1 = str(setTemp0)
        print('Writing: ' , setTemp1,len(setTemp1))
        self.ser.write(setTemp1.encode())

        print(self.ser.readline().rstrip())

    def button_Down(self):  # Move Down only available for A
        ### Delete RightLeftCOunter
        if (ActiveJoint == "A"):
            x = self.J1_total
            setTemp0 = ActiveJoint + str(x) #increment Z by -1
            setTemp1 = str(setTemp0)
            print('Writing: ' + setTemp1)
            self.ser.write(setTemp1.encode())

            print(self.ser.readline().rstrip())

    # def write_SerialCalc(self):  ### the kinematic calculations
    #
    #     print(self.ser.readline())

    # def update_angles(self):
    #     print(self.ser.readline())
    #
    # def update_XYZ(self):
    #     print(self.ser.readline())

    ############################################################################
    #######################  Go Submit
    def button_Enter(self):
        if (self.RecordCheck_text.get() == 5):
            print(str(fileName))
            print(self.X_total)
            print(self.ser.readline())
            fileName.write(Joint_C)
            fileName.write(str(self.X_total))
            fileName.write(Joint_B)
            fileName.write(str(self.Y_total))
            fileName.write(Joint_A)
            fileName.write(str(self.Z_total))
            fileName.write("\n")

        # #####Convert and Send
        # cradpos = np.arccos((((x * x) + (y * y))) / (2 * LinkLength1 * LinkLength1))
        # cdegpos = np.round(np.degrees(cradpos), 0)
        # bdegpos = np.round(np.degrees(np.arctan(y / x)) + np.degrees(
        #     ((LinkLength1 * LinkLength1) * np.sin(cdegpos)) / (2 * LinkLength1 * LinkLength1)), 0)
        if (len(self.X_Value.get()) > 0):
            self.X_total = self.X_Value.get()
            self.X_total_label_text.set(self.X_total)

            setTemp0 = Joint_C + str(self.X_total)
            setTemp1 = str(setTemp0)
            setTemp1 = str(App.check_SerialLength(self, setTemp1))
            # self.ser.write(setTemp1.encode())
            print("sending:", setTemp1)

            # self.ser.flush()
        if (len(self.J2_Value.get()) > 0):
            self.Y_total = self.Y_Value.get()
            self.Y_total_label_text.set(self.Y_total)
            setTemp0 = Joint_B + str(self.Y_total)
            setTemp1 = str(setTemp0)
            setTemp1 = str(App.check_SerialLength(self, setTemp1))
            # self.ser.write(setTemp1.encode())
            # print(self.ser.write(setTemp1.encode()))
            print("sending:", setTemp1)

            # self.ser.flush()

        if (len(self.Z_Value.get()) > 0):
            self.Z_total = self.Z_total.get()
            self.J3_total_label_text.set(self.Z_total)
            setTemp0 = Joint_A + str(self.Z_total)
            setTemp1 = str(setTemp0)
            setTemp1 = str(App.check_SerialLength(self, setTemp1))
            # setTemp0 =  setTemp2+setTemp1
            # setTemp1=str(setTemp0)
            # self.ser.write(setTemp1.encode())
            print("sending:", setTemp1)
        #App.get_XYZEntryText()
        # if (len(self.X_Value.get()) > 0):
        #     self.X_total = self.X_Value.get()
        # if (len(self.Y_Value.get()) > 0):
        #     self.Y_total = self.Y_Value.get()
        # if (len(self.Z_Value.get()) > 0):
        #     self.Z_total = self.Z_Value.get()
        #
        # self.X_total_label_text.set(self.X_total)
        # self.Y_total_label_text.set(self.Y_total)
        # self.Z_total_label_text.set(self.Z_total)

        # Outputlist = list(self.X_total,self.Y_total,self.Z_total)
        App.calc_deg(self,int(self.X_total),int(self.Y_total),0)#int(self.Z_total))




    def calc_deg(self,x,y,z): #### calculate degrees and Serial Write
        x=int(x)
        y=int(y)
        z=int(z)

        # x= 10
        # y= 15
        # LinkLength1=(30.5)
        # x=c,y=b , z = height but not coded due to hardware issue
        cradpos = np.arccos((((x * x) + (y * y))) /(2 *LinkLength1 * LinkLength1))
        cdegpos=np.round(np.degrees(cradpos),0)
        bdegpos = np.round(np.degrees(np.arctan(y/x)) + np.degrees(((LinkLength1 * LinkLength1)*np.sin(cdegpos))/(2 *LinkLength1 * LinkLength1)),0)

        adegpos=int(0)
        cdegpos=int(cdegpos)
        bdegpos=int(bdegpos)
        App.serial_Write(self,adegpos,bdegpos,cdegpos)

    def serial_Write(self,adegpos,bdegpos,cdegpos):
        # c=str(c)
        # b=str(b)
        # a=str(a)
        # self.ser.write((str(cradpos)).encode())
        # print("sent C:" cradpos )
        setTemp2=""
        setTemp3=""
        setTemp4=""
        if (adegpos>0):
            setTemp0 = Joint_A + str(adegpos)
            setTemp1 = str(setTemp0)
            setTemp2 = str(App.check_SerialLength(self, setTemp1))
            # self.ser.write(str(set).encode())
            # print("sent A(z):", adegpos)
            # self.ser.flush()
        if (bdegpos>0):
            setTemp0 = Joint_B + str(bdegpos)
            setTemp1 = str(setTemp0)
            setTemp3 = str(App.check_SerialLength(self, setTemp1))
            # self.ser.write(str(bdegpos).encode())
            # print("sent B(y):", bdegpos)
            # self.ser.flush()
        if (cdegpos>0):
            setTemp0 = Joint_C + str(cdegpos)
            setTemp1 = str(setTemp0)
            setTemp4 = str(App.check_SerialLength(self, setTemp1))
            # self.ser.write(str(cdegpos).encode())
            # print("sent C(x): ", cdegpos)
            # self.ser.flush()


            setTempf= setTemp2+setTemp3+setTemp4
            setTempf =str(setTempf)
            self.ser.write(setTempf.encode())
            print("values sent")


    # def calc_cm(self,):









            ####### need to write algorithem for position locatoin


        # print(self.ser.readline())

    def button_Submit(self):  #### for angles only
        # write code for angle generatoin
        ### check what needs to be sent
        # App.get_JJJentryText()
        if (len(self.J1_Value.get()) > 0):
            self.J1_total = self.J1_Value.get()
            self.J1_total_label_text.set(self.J1_total)
            setTemp0 = Joint_A + str(self.J1_total)
            setTemp1 = str(setTemp0)
            setTemp1 = str(App.check_SerialLength(self, setTemp1))
            print("sending:", setTemp1)

            self.ser.flush()
        if (len(self.J2_Value.get()) > 0):
            self.J2_total = self.J2_Value.get()
            self.J2_total_label_text.set(self.J2_total)
            setTemp0 = Joint_B + str(self.J2_total)
            setTemp1 = str(setTemp0)
            setTemp1 = str(App.check_SerialLength(self, setTemp1))
            self.ser.write(setTemp1.encode())
            # print(self.ser.write(setTemp1.encode()))
            print("sending:", setTemp1)

            # self.ser.flush()

        if (len(self.J3_Value.get()) > 0):
            self.J3_total = self.J3_Value.get()
            self.J3_total_label_text.set(self.J3_total)
            setTemp0 = Joint_C + str(self.J3_total)
            setTemp1 = str(setTemp0)
            setTemp1 = str(App.check_SerialLength(self, setTemp1))
            # setTemp0 =  setTemp2+setTemp1
            # setTemp1=str(setTemp0)
            self.ser.write(setTemp1.encode())
            print("sending:", setTemp1)

            # self.ser.flush()

        # App.start_motors(self)

    #########################################################################
    #######################  Reset Sweep
    def button_Reset(self):  # Reset Servo aka Call reset
        setTemp1 = "R000"
        print('Sending: Reset Command')
        self.ser.write(setTemp1.encode()) #### WRITE RESET to Arduino
        ser.flush()

        self.J1_total = 0
        self.J2_total = 0
        self.J3_total = 0
        self.X_total = 0
        self.Y_total = 0
        self.Z_total = 0
        self.X_total_label_text.set(self.X_total)
        self.Y_total_label_text.set(self.Y_total)
        self.Z_total_label_text.set(self.Z_total)
        self.J1_total_label_text.set(self.J1_total)
        self.J2_total_label_text.set(self.J2_total)
        self.J3_total_label_text.set(self.J3_total)
        App.clear_Text1(self)
        App.clear_Text2(self)
        f = ""

    # def button_Sweep(self):  # Continuous rotation
    #     ### Delete RightLeftCOunter
    #
    #     for RightLeftCounter in range(0, 180):
    #         print(RightLeftCounter)
    #         self.ser.write(chr(RightLeftCounter))
    #         print(self.ser.readline())
    #         time.sleep(0.01)  # delays for 1 seconds
    #     RightLeftCounter = 90
    #     self.ser.write(chr(RightLeftCounter))

    ######### ###############################################################
    ######          Record Read Laser Kill
    def start_Recording(self):  # record points
        global fileName
        #   print('the value is ',self.RecordCheck_text.get(),'\n')
        if (self.RecordCheck_text.get() == 5):  # if recording
            ### start recording movement
            fileName = open(os.path.expanduser("~/Desktop/somefile.txt"), "w+")
            return fileName

        else:
            fileName.close()  # values written to txt file aren't saved till it's closed
            print("No longer Recording")

    def open_Text(self):  # Read Txt file
        global fileName

        if (self.RecordCheck_text.get() == 5):
            self.RecordCheck_text.value == 0
            fileName.close()

        path = askopenfilename()
        if (path != ""):
            f = open(path, 'r')
            fileName = os.path.basename(path)
            return f

    def button_Laser(self):
        if (self.LazerCheck_text.get() == 6):
            print("Laser is on")
            self.ser.write("L000".encode())
        else:
            print("Laser is off")
            self.ser.write("L100".encode())

    def button_Kill(self):  # Kill
        self.ser.write("S000".encode())
        self.ser.flush()
        # setTemp1 = "K000"
        # print('Sending: Kill Command')
        # self.ser.write(setTemp1.encode())


        self.ser.flush()


    def ActiveServo(self):
        print(ActivePin)

    ##############################################################################
    #############   Update
    def get_XYZEntryText(self):
        if (len(self.X_Value.get()) > 0):
            self.X_total = self.X_Value.get()
        if (len(self.Y_Value.get()) > 0):
            y=self.Y_total = self.Y_Value.get()
        if (len(self.Z_Value.get()) > 0):
            self.Z_total = self.Z_Value.get()
        App.calc_deg(self.X_total,self.Y_total,self.Z_total)

    def get_JJJentryText(self):

        if (len(self.J1_Value.get()) > 0):
            self.J1_total = self.J1_Value.get()
        if (len(self.J2_Value.get()) > 0):
            self.J2_total = self.J2_Value.get()
        if (len(self.J3_Value.get()) > 0):
            self.J3_total = self.J3_Value.get()

        self.X_total_label_text.set(self.X_total)
        self.Y_total_label_text.set(self.Y_total)
        self.Z_total_label_text.set(self.Z_total)
        self.J1_total_label_text.set(self.J1_total)
        self.J2_total_label_text.set(self.J2_total)
        self.J3_total_label_text.set(self.J3_total)


###############################################################################
################################################
    def decode_SerialInput(self, x):

        if x[:1] == "a":
            self.J1_total = int(x[1:])
            self.J1_total_label_text.set(self.J1_total)


        elif x[:1] == "b":
            self.J2_total = int(x[1:])
            self.J2_total_label_text.set(self.J2_total)

        elif x[:1] == "c":
            self.J3_total = int(x[1:])
            self.J3_total_label_text.set(self.J3_total)

        elif x[:1] == "x":
            self.X_total = int(x[1:])
            self.X_total_label_text.set(self.X_total)

        elif x[:1] == "y":
            self.Y_total = int(x[1:])
            self.Y_total_label_text.set(self.Y_total)

        elif x[:1] == "z":
            self.Z_total = int(x[1:])
            self.Z_total_label_text.set(self.Z_total)

        else: return

    def check_SerialLength(self, setTemp1):  ### used to make sure serial output len = 4
        if (len(setTemp1) == 4):
            return setTemp1
        elif (len(setTemp1) < 4):
            setTemp1 = setTemp1[:1] + '0' + setTemp1[1:]
            return App.check_SerialLength(self, setTemp1)
        elif (len(setTemp1) > 4):
            setTemp1 = setTemp1[:-1]
            print("Error: To Long, changed to",setTemp1)
            return App.check_SerialLength(self, setTemp1)


    ################### Below is the code to contantly update the Serial Label and
    #call serial decode function
    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # print('length msg :',len(str(msg)),msg)
                ################ Update Label Total values if needed
                print('Pincom msg Length:', msg) # debugging
                if (len(str(msg))>3):
                    self.SerialReading_label_text.set(msg)  #### used to set the Serial label
                    App.decode_SerialInput(self,msg)
                    # if msg[:1] == "a":
                    #     self.J1_total = int(msg[1:])
                    #     self.J1_total_label_text.set(self.J1_total)
                    #
                    # elif msg[:1] == "b":
                    #     self.J2_total = int(msg[1:])
                    #     self.J2_total_label_text.set(self.J2_total)
                    #
                    # elif msg[:1] == "c":
                    #     self.J3_total = int(msg[1:])
                    #     self.J3_total_label_text.set(self.J3_total)


                #root.update()
                # print("Print:", self.SerialString)
            except queue.Empty:
                self.SerialReading_label_text.set("Error Que Empty")
                pass


class SerialThreadClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """

    def __init__(self, master):
        self.master = master
        self.queue = queue.Queue() # Create queue

        self.gui = App(master, ser, self.queue, self.endApplication) # set up Gui

        # Set up the thread to do asynchronous I/O
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        #####
        self.thread2= serial
        #####
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()   # Check if queue for gui needs anything

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            import sys  # system stop
            sys.exit(1)
        self.master.after(100, self.periodicCall) #check every 100ms for queue

    ############# Reading Serial'
    def workerThread1(self): #where asynchronous I/O is handled
        # ser = serial.Serial('/dev/cu.usbmodem1421')
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            time.sleep(rand.random() * 0.3)
            # time.sleep(.1) #is delay needed?
            msg = str(self.gui.ser.readline().decode().rstrip()) ##### rstrip gets rid of blank or lines the str for len
            #print("msg =: ",msg,len(msg),len(str(msg)),str(msg))
            # msg=msg.

            if (len(msg)>(0)):
                print(msg)
            if (len(msg)  ==4):     ##### is char due to
                print('wtreading : ', msg)
                self.queue.put(msg)
            elif (len(msg)  >4):
                print(msg)

            # elif(len(str(msg))  !=4):
            #      print('Sread len !=4')



    def endApplication(self):
        # ser = serial.Serial('/dev/cu.usbmodem1421')
        # self.gui.ser.write("Q000".encode())
        # self.ser.flush()
        self.running=0
        # ser.write("Stop Program".encode())
        # ser.close()

ser = serial.Serial('/dev/cu.usbmodem1421') # My serial port... modify for yours
# ser.port = '/dev/cu.usbmodem1421 '
ser.baudrate = 9600
ser.timeout = 0

if ser.isOpen() == False: # open port if !open
    ser.open()




rand = random.Random()
root = tkinter.Tk()
root.title("Scara GUI Controller")
root.configure(background='lime green')

client = SerialThreadClient(root)
root.mainloop()

