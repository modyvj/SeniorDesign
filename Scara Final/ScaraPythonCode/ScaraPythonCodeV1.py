# Scara Gui

###### Vishal Mody 
from tkinter import *  # filedialog, Tk
# from tkinter import filedialog
import sys
import os
import glob
import serial
import time
from tkinter.filedialog import askopenfilename

__author__= 'Vishal Mody'


RightLeftCounter = 94
ActivePin = 0
ActiveJoint = 'X'
color = 1


class App:
    def __init__(self, master, ser):

        

        ##### check boxes
        checka1 = int()
        checka2 = int()
        checka3 = int()
        checka4 = int()
        #    self.
        self.RecordCheck_text = IntVar()
        self.LazerCheck_text = IntVar()

        self.J1_total_label_text = IntVar()
        self.J2_total_label_text = IntVar()
        self.J3_total_label_text = IntVar()

        self.X_total_label_text = IntVar()
        self.Y_total_label_text = IntVar()
        self.Z_total_label_text = IntVar()

        self.ser = ser

        ##### ###############################################################
        ####          SERVO ANGLE/ HEIGHT Values
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
        #   R4 = Radiobutton(master, text="Joint 4", variable=checka4,background="lime green", value=4,
        #                  command= self.activate_J4).grid(row=6)

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
        frame4.grid(row=11, column=3, columnspan=7)

        Label(master, text="", background="lime green", width=3).grid(row=2, column=3)
        Label(master, text="", background="lime green", width=3).grid(row=2, column=9)

        self.SerialReading_label_text = StringVar()
        self.SerialString =""
        self.SerialReading_label_text.set(self.SerialString)#### used to set the
        Label(master, text="Serial Line:", background="lime green", ).grid(row=11, column=0)
        self.SerialReading_Label = Label(frame4, textvariable=self.SerialReading_label_text)
        ###### ###############################################################
        #####               GO SUBMIT  QUIT buttons

        self.Go = Button(frame2,
                         text="Submit", padx=10, highlightbackground="lime green",
                         command=self.write_Go, width=5)
        self.Go.pack(side=LEFT)  # grid(row=7, column=10, padx=0, pady=0, sticky="nw")

        self.Submit = Button(frame1,
                             text="Submit", padx=10, highlightbackground="lime green",
                             command=self.write_Submit)
        self.Submit.pack(side=LEFT)  # .grid(row=7, column=10, padx=0, pady=0, sticky="nw")

        self.Quit = Button(master,
                           text="Quit", highlightbackground="lime green",
                           command=quit)
        self.Quit.grid(row=0, column=0, padx=0, pady=0, sticky="nw")  ##Quit Button Location

        ##### ###############################################################
        #######################  Arrow Keys

        self.Left = Button(master,
                           text="←", padx=10, highlightbackground="lime green",
                           command=self.write_Left)
        self.Left.grid(row=4, column=5, padx=0, pady=0, )  # sticky="nw")

        self.Right = Button(master,
                            text="→", padx=10, highlightbackground="lime green",
                            command=self.write_Right)
        self.Right.grid(row=4, column=7, padx=2, pady=0, )  # sticky="nw")

        self.Up = Button(master,
                         text="↑", padx=10, highlightbackground="lime green",
                         command=self.write_Up)
        self.Up.grid(row=3, column=6, padx=0, pady=0, )  # sticky="nw")

        self.Down = Button(master,
                           text="↓", padx=10, highlightbackground="lime green",
                           command=self.write_Down)
        self.Down.grid(row=5, column=6, padx=2, pady=0, )  # sticky="nw")

        ##### ###############################################################
        #######################X Y Z point entry

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
        ###########        Record, Laser, Read, Kill

        ##    self.FileName_label =  Label(frame4, text="file location11111111111111111111111111111111111111111111111111",background="lime green",)
        ##    self.FileName_label.pack(side=LEFT)#grid(row=2, column=5,columnspan=3,sticky=E)

        self.RecordCheck = Checkbutton(master, text="Record", onvalue="5", offvalue="0",
                                       variable=self.RecordCheck_text, background="lime green",
                                       command=self.write_record).grid(row=2, column=11, sticky=W)

        self.LazerCheck = Checkbutton(master, text="Laser", onvalue="6", offvalue="0",
                                      variable=self.LazerCheck_text, background="lime green",
                                      command=self.write_Laser).grid(row=6, sticky=W)

        self.Open = Button(master,
                           text="Read Txt", highlightbackground="lime green",
                           command=self.open_text)
        self.Open.grid(row=0, column=11, padx=0, pady=0, sticky=E)  ### read txt file

        self.Kill = Button(frame3,
                           text="Kill Motors", padx=10, highlightbackground="lime green",
                           command=self.write_Kill)
        self.Kill.pack(side=LEFT)  # .grid(row=7, column=5, columnspan=3,padx=0, pady=0, sticky="nw")
        #  self.Go.pack(side=LEFT)

        ######## ###############################################################
        #########              Reset Clear

        self.Reset = Button(master,
                            text="Reset", highlightbackground="lime green",
                            command=self.write_reset)
        self.Reset.grid(row=0, column=1, padx=0, pady=0, sticky="nw")

        self.Clear1 = Button(frame1,
                             text="Clear", highlightbackground="lime green",
                             command=self.clear_text1, )
        self.Clear1.pack(side=LEFT)

        self.Clear2 = Button(frame2,
                             text="Clear", highlightbackground="lime green",
                             command=self.clear_text2, )
        self.Clear2.pack(side=LEFT)

        self.sweep = Button(master,
                            text="S", highlightbackground="lime green",
                            command=self.write_sweep)



    ##################################################################################
    ############## ###############################################################
    #############
        
#        self.get_SerialInput()



        

    #   self.sweep.grid(row=0, column=9, padx=0, pady=0, sticky="nw")

    ##################################################################################
    ############## ###############################################################
    #############         DEF  Functions

    ## Clear Text
    def clear_text1(self):
        self.J1_Value.delete(0, END)
        self.J2_Value.delete(0, END)
        self.J3_Value.delete(0, END)

    #   self.J4_Value.delete(0, END)
    #   App.clear_text2(self)

    def clear_text2(self):
        self.X_Value.delete(0, END)
        self.Y_Value.delete(0, END)
        self.Z_Value.delete(0, END)

    ## Active Joints
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

    def deselect_all(self):
        global ActivatePin
        ActivatePin = 0
        print(ActivePin)

    ########## Arrows Right Left Up Down
    def write_Left(self):  # Move Left
        if (ActiveJoint == "B"):
            x = self.J2_total
        elif (ActiveJoint == "C"):
            x = self.J3_total
        else:
            print("Error: Incorrect Joint for OP")
            return
        #   x=x-1  #### subtract 1 degree to go left

        setTemp0 = ActiveJoint + str(x)
        setTemp1 = str(setTemp0)
        setTemp1 = str(App.check_SerialLength(self, setTemp1))  ### make sure 4 chars
        #    print('Writing: '+setTemp1)
        self.ser.write(setTemp1.encode())

        time.sleep(.1)

        print(str(self.ser.readline().decode()))

    #    x = str(self.ser.readline())#.decode()) ########### this gets XXXX not b XXXX
    #    print ('this is ' + x)
    # print (self.ser.readline())#.rstrip())

    def write_Right(self):  # Move Right
        global RightLeftCounter
        if (ActiveJoint == "B"):
            x = self.J2_total
        elif (ActiveJoint == "C"):
            x = self.J3_total
        else:
            print("Error: Incorrect Joint for OP")
            return

        setTemp0 = ActiveJoint + str(x)
        setTemp1 = str(setTemp0)
        print('Writing: ' + setTemp1)
        self.ser.write(setTemp1.encode())

        print (self.ser.readline().rstrip())

    def write_Up(self):  # Move Up only available for A
        global RightLeftCounter
        if (ActiveJoint == "A"):
            x = self.J1_total
        else:
            print("Error: Incorrect Joint for OP")
            return
        setTemp0 = ActiveJoint + str(x)
        setTemp1 = str(setTemp0)
        print('Writing: ' + setTemp1)
        self.ser.write(setTemp1.encode())

        print (self.ser.readline().rstrip())

    def write_Down(self):  # Move Down only available for A
        global RightLeftCounter
        if (ActiveJoint == "A"):
            x = self.J1_total
            setTemp0 = ActiveJoint + str(x)
            setTemp1 = str(setTemp0)
            print('Writing: ' + setTemp1)
            self.ser.write(setTemp1.encode())

            print (self.ser.readline().rstrip())

    def write_SerialCalc(self):  ### the kinematic calculations

        print (self.ser.readline())

    def update_angles(self):
        print (self.ser.readline())

    def update_XYZ(self):
        print (self.ser.readline())

    ############################################################################
    #######################  Go Submit
    def write_Go(self):
        if (self.RecordCheck_text.get() == 5):
            print(str(f))
            print(self.X_total)
            print (self.ser.readline())
            f.write(ActiveJoint)
            f.write(",")
            f.write(str(self.X_total))
            f.write(",")
            f.write(str(self.Y_total));
            f.write(",")
            f.write(str(self.Z_total))
            f.write("\n")

            ####### need to write algorithem for position locatoin

        print (self.ser.readline())

    def write_Submit(self):  #### for angles only
        # write code for angle generatoin
        print (self.J1_Value.get())
        App.labels_Update(self)
        print (self.ser.readline())

    #########################################################################
    #######################  Reset Sweep
    def write_reset(self):  # Reset Servo aka Call reset
        setTemp1 = "R000"
        print('Writing: Reset Command')
        self.ser.write(setTemp1.encode())

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
        App.clear_text1(self)
        App.clear_text2(self)
        f = ""

    def write_sweep(self):  # Continuous rotation
        global RightLeftCounter
        for RightLeftCounter in range(0, 180):
            print(RightLeftCounter)
            self.ser.write(chr(RightLeftCounter))
            print (self.ser.readline())
            time.sleep(0.01)  # delays for 1 seconds
        RightLeftCounter = 90
        self.ser.write(chr(RightLeftCounter))

    ######### ###############################################################
    ######          Record Read Laser Kill
    def write_record(self):  # record points
        global f
        #   print('the value is ',self.RecordCheck_text.get(),'\n')
        if (self.RecordCheck_text.get() == 5):  # if recording
            ### start recording movement
            f = open(os.path.expanduser("~/Desktop/somefile.txt"), "w+")
            return f

        else:
            f.close()  # values written to txt file aren't saved till it's closed
            print("No longer Recording")

    def open_text(self):  # Read Txt file
        if (self.RecordCheck_text.get() == 5):
            self.RecordCheck_text.value == 0
            f.close()

        path = askopenfilename()
        if (path != ""):
            f = open(path, 'r')
            fileName = os.path.basename(path)
            return f

    def write_Laser(self):
        if (self.LazerCheck_text.get() == 6):
            print("Laser is on")
            self.ser.write("G100".encode())
        else:
            print("Laser is off")
            self.ser.write("G000".encode())

    def write_Kill(self):  # Kill

        setTemp1 = "K000"
        print('Writing: Kill Command')
        self.ser.write(setTemp1.encode())

    def ActiveServo(self):
        print(ActivePin)

    ##############################################################################
    #############   Update

    def labels_Update(self):

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

    def get_Angles(self):

        if x[:1] == "a":
            self.J1_total = int(x[1:])
            self.J1_total_label_text.set(self.J1_total)



        elif x[:1] == "b":
            self.J2_total = int(x[1:])
            self.J2_total_label_text.set(self.J2_total)


        elif x[:1] == "c":
            self.J3_total = int(x[1:])
            self.J3_total_label_text.set(self.J3_total)

    def get_XYZ(self):
        if x[:1] == "x":
            self.X_total = int(x[1:])
            self.X_total_label_text.set(self.X_total)



        elif x[:1] == "y":
            self.Y_total = int(x[1:])
            self.Y_total_label_text.set(self.Y_total)


        elif x[:1] == "z":
            self.Z_total = int(x[1:])
            self.Z_total_label_text.set(self.Z_total)

    def check_SerialLength(self, setTemp1):  ### used to make sure serial output len = 4
        if (len(setTemp1) == 4):
            return setTemp1
        elif (len(setTemp1) < 4):
            setTemp1 = setTemp1[:1] + '0' + setTemp1[1:]
            return App.check_SerialLength(self, setTemp1)
        elif (len(setTemp1) > 4):
            print("Error: value can only be 3 char long")

    ###### ###############################################################
    #####             Reading serial


    



def main():
    
  
    ser = serial.Serial('/dev/cu.usbmodem1421')
    # ser.port = '/dev/cu.usbmodem1421 '
    ser.baudrate = 9600
    ser.timeout = 0
    # open port if not already open
    if ser.isOpen() == False:
      ser.open()

    root = Tk()
    root.title("Scara GUI Controller")
    root.configure(background='lime green')
    # root.geometry("300x50+500+300")
    app = App(root, ser)
    def get_SerialInput(ser):
        while 1:
            
            print((str(ser.readline().decode())))
            root.update()
            time.sleep(1) 




    root.after(1,get_SerialInput(ser) )
    root.mainloop()


if __name__ == '__main__':
    main()
