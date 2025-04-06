import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

Video_Index = 1
############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'xxxxxxxxxxxxx@gmail.com' ")

###################################################################################

def check_haarcascadefile(window):
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel/psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw(window,message,message1):
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages(window,message,message1)
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear(txt,message1):
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2(txt2, message1):
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def TakeImages(window,txt,txt2,message,message1,trainImg):
    check_haarcascadefile(window)
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("EmployeeDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("EmployeeDetails/EmployeeDetails.csv")
    if exists:
        with open("EmployeeDetails/EmployeeDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("EmployeeDetails/EmployeeDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(Video_Index)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            faces = detector.detectMultiScale(gray, 1.1, 5,minSize=(100,100))
            for (x, y, w, h) in faces:
                
                face = cv2.resize(gray[y:y + h, x:x + w], (200, 200)) 
                
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage/ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",face)
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(150) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 150:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('EmployeeDetails/EmployeeDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)
    trainImg.config(state=tk.NORMAL)

########################################################################################

def TrainImages(window,message,message1):
    check_haarcascadefile(window)
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

# def TrackImages(window, tv):
#     while True:
#         check_haarcascadefile(window)
#         assure_path_exists("Attendance/")
#         assure_path_exists("EmployeeDetails/")
        
#         for k in tv.get_children():
#             tv.delete(k)
#         msg = ''
#         i = 0
#         j = 0
#         recognizer = cv2.face.LBPHFaceRecognizer_create()
#         exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
#         if exists3:
#             recognizer.read("TrainingImageLabel/Trainner.yml")
#         else:
#             mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
#             return
#         harcascadePath = "haarcascade_frontalface_default.xml"
#         faceCascade = cv2.CascadeClassifier(harcascadePath)
        
#         cam = cv2.VideoCapture(0)
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         col_names = ['Id', '', 'Name', '', 'Date', '', 'Intime', '', 'Outtime']
#         curtime = None
#         exists1 = os.path.isfile("EmployeeDetails/EmployeeDetails.csv")
#         if exists1:
#             df = pd.read_csv("EmployeeDetails/EmployeeDetails.csv")
#         else:
#             mess._show(title='Details Missing', message='Employees details are missing, please check!')
#             cam.release()
#             cv2.destroyAllWindows()
#             window.destroy()
#             return
#         while True:
#             flag=False
#             ret, im = cam.read()
#             gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#             faces = faceCascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
#             for (x, y, w, h) in faces:
#                 cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
#                 face_resized = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
#                 serial, conf = recognizer.predict(face_resized)
#                 if conf < 60:
#                     ts = time.time()
#                     date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
#                     timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
#                     aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
#                     ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
#                     ID = str(ID).strip("[]")
#                     bb = str(aa).strip("[]").strip("'")
#                     curtime = timeStamp
#                     attendance = [str(ID), '', bb, '', str(date), '', str(curtime), str(curtime)]
#                     flag=True
#                     break
#                 else:
#                     bb = 'Unknown'
#                 cv2.putText(im, bb, (x, y + h), font, 1, (255, 255, 255), 2)
#             cv2.imshow('Taking Attendance', im)
#             if flag or cv2.waitKey(1) == ord('q'):
#                 break
#         ts = time.time()
#         date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
#         attendance_file = f"Attendance/Attendance_{date}.csv"

        
#         # Load existing records from the file
#         existing_records = []
#         if os.path.isfile(attendance_file):
#             with open(attendance_file, 'r') as csvFile:
#                 reader = csv.reader(csvFile)
#                 existing_records = list(reader)

#         # Update or add the current attendance
#         updated = False
#         for record in existing_records:
#             if record and record[0] == str(ID):  # Match ID
#                 record[-1] = curtime  # Update outtime
#                 updated = True
#                 break
        
#         if not updated:
#             # Add new record if ID is not found
#             existing_records.append(attendance)

#         # Write back updated records to the file
#         with open(attendance_file, 'w', newline='') as csvFile:
#             writer = csv.writer(csvFile)
#             writer.writerows(existing_records)

#         # Display updated records in the treeview
#         for record in existing_records:
#             if record and record[0] != 'Id':  # Skip header row
#                 j += 1
#                 iidd = str(record[0]) + '   '
#                 ch(j, tv, iidd, record)

#         tv.tag_configure('gray', background="#ebf7bc")
#         tv.tag_configure('green', background="#cfec9a")
#         cam.release()
#         cv2.destroyAllWindows()
#         if cv2.waitKey(3) == ord('q'):
#             break
def TrackImages(window, tv):
    check_haarcascadefile(window)
    assure_path_exists("Attendance/")
    assure_path_exists("EmployeeDetails/")

    for k in tv.get_children():
        tv.delete(k)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not os.path.isfile("TrainingImageLabel/Trainner.yml"):
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    recognizer.read("TrainingImageLabel/Trainner.yml")

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(Video_Index)  # Ensure correct camera index
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Intime', '', 'Outtime']

    if not os.path.isfile("EmployeeDetails/EmployeeDetails.csv"):
        mess._show(title='Details Missing', message='Employees details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        return

    df = pd.read_csv("EmployeeDetails/EmployeeDetails.csv")
    date = datetime.datetime.now().strftime('%d-%m-%Y')
    attendance_file = f"Attendance/Attendance_{date}.csv"

    # Load existing attendance records into memory
    attendance_data = {}
    if os.path.isfile(attendance_file):
        with open(attendance_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if row and row[0] != 'Id':
                    attendance_data[row[0]] = row

    while True:
        ret, im = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            face_resized = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            serial, conf = recognizer.predict(face_resized)

            if conf < 60:
                ts = time.time()
                curtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID).strip("[]")
                bb = str(aa).strip("[]").strip("'")

                if ID in attendance_data:
                    attendance_data[ID][-1] = curtime  # Update outtime
                else:
                    new_record = [str(ID), '', bb, '', date, '', curtime, curtime]
                    attendance_data[ID] = new_record

                cv2.putText(im, f"ID: {ID} Name: {bb}", (x, y + h), font, 1, (255, 255, 255), 2)
            else:
                cv2.putText(im, "Unknown", (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)

        # Update the treeview continuously
        for k in tv.get_children():
            tv.delete(k)
        for record in attendance_data.values():
            j = len(tv.get_children()) + 1
            iidd = str(record[0]) + '   '
            ch(j, tv, iidd, record)

        tv.tag_configure('gray', background="#ebf7bc")
        tv.tag_configure('green', background="#cfec9a")

        # Write attendance data back to the file
        with open(attendance_file, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(col_names)
            writer.writerows(attendance_data.values())

        if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit
            break

    cam.release()
    cv2.destroyAllWindows()




#################################################################################
def att(tv):
    col_names = ['Id', '', 'Name', '', 'Date', '', 'InTime','OutTime']
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance/Attendance_" + date + ".csv")
    attendance_file = f"Attendance/Attendance_{date}.csv"
    # try:
    #     with open("Attendance/Attendance_" + date + ".csv", 'r') as csvFile1:
    #         reader1 = csv.reader(csvFile1)
    #         for lines in reader1:
    #             i = i + 1
    #             if (i > 1):
    #                 if (i % 2 != 0):
    #                     j+=1
    #                     iidd = str(lines[0]) + '   '
    #                     ch(j,tv,iidd,lines)
    #     csvFile1.close()
    # except Exception as e:
    #     mess.showinfo("Oops","No records for today yet")
    existing_records = []
    if os.path.isfile(attendance_file):
        with open(attendance_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            existing_records = list(reader)
    for record in existing_records:
        if record and record[0] != 'Id':  # Skip header row
            j += 1
            iidd = str(record[0]) + '   '
            ch(j, tv, iidd, record)
    tv.tag_configure('gray', background="#ebf7bc")
    tv.tag_configure('green', background="#cfec9a")
#################################################################################
def ch(j,tv,iidd,lines):
    if j % 2==0:
        tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6]),str(lines[7])),tags=['gray'])
    else:
        tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6]),str(lines[7])),tags=['green'])
##################################################################################
def psw_quit(window):
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        window.destroy()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

##################################################################################
######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }