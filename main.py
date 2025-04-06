    ############################################# IMPORTING ################################################
from functions import *
import tkinter as tk
from tkinter import Menu, ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time
import torch


Video_Index = 1
############################################# FUNCTIONS ################################################
def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

def changeOnHover(button, colorOnHover, colorOnLeave, fontcOnHover, fontcOnLeave):
 
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover,fg=fontcOnHover) if (button['state']!="disabled") else None)
 
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave, fg=fontcOnLeave))

def changeOnHoverClear(text,text2,button, colorOnHover, colorOnLeave, fontcOnHover, fontcOnLeave):
 
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover,fg=fontcOnHover,text=text))
 
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave, fg=fontcOnLeave,text=text2))
def show_gif(after_gif_callback):

    gif_window = tk.Toplevel(window)
    gif_window.title("Tutorial")
    gif_window.geometry("400x400")
    gif_window.configure(bg="white")

    heading = tk.Label(gif_window, text="Tutorial", font=("times", 20, "bold"), bg="white", fg="black")
    heading.pack(pady=10)

    gif_path = "tutorial.gif" 
    gif_image = Image.open(gif_path)
    gif_label = tk.Label(gif_window, bg="white")
    gif_label.pack()


    def animate_gif(count):
        frame = count % gif_image.n_frames 
        gif_image.seek(frame)
        gif_photo = ImageTk.PhotoImage(gif_image)
        gif_label.config(image=gif_photo)
        gif_label.image = gif_photo
        gif_window.after(100, animate_gif, count + 1)
    
    animate_gif(0)


    def close_and_trigger_callback():
        gif_window.destroy()
        after_gif_callback()

    ok_button = tk.Button(
        gif_window, text="OK", command=close_and_trigger_callback, font=("times", 15), bg="#ff8d84", fg="white"
    )
    ok_button.pack(pady=20)

    gif_window.transient(window)
    gif_window.grab_set()
    gif_window.mainloop()

    
def heat(window):

    q = 0
    persons = []


    def blend_color(start_color, end_color, steps, step):
        start_r, start_g, start_b = int(start_color[1:3], 16), int(start_color[3:5], 16), int(start_color[5:7], 16)
        end_r, end_g, end_b = int(end_color[1:3], 16), int(end_color[3:5], 16), int(end_color[5:7], 16)

        new_r = int(start_r + (end_r - start_r) * step / steps)
        new_g = int(start_g + (end_g - start_g) * step / steps)
        new_b = int(start_b + (end_b - start_b) * step / steps)

        return f'#{new_r:02x}{new_g:02x}{new_b:02x}'

    def transition_color(widgets, steps, step=0):
        if step <= steps:
            for widget, attr, start_color, end_color in widgets:
                new_color = blend_color(start_color, end_color, steps, step)
                widget.config(**{attr: new_color})
            widgets[0][0].after(50, transition_color, widgets, steps, step + 1)

    def change(count):

        st = ['#3fde07', '#d6bd1b', '#d6a019', '#eb940e', '#f5650c']
        en = ['#3fde07', '#d6bd1b', '#d6a019', '#eb940e', '#f5650c']

        transition_index = min(int(count/4), len(st) - 1)
        widgets_to_transition = [
            (frame1, 'bg', st[transition_index], en[transition_index])
        ]
        transition_color(widgets_to_transition, 10)


    # window = tk.Tk()
    # window.title("Color Transition")
    # window.geometry("300x200")

    frame1 = tk.Frame(window, bg="#3fde07",highlightbackground="#262523", highlightthickness=2)
    frame1.place(relx=0.7, rely=0.3, width=200, height=200)
    tk.Label(frame1,text="Room 1",font=("Arial", 15)).place(relx=0.1, rely=0)

    def load_model():
        global persons

        model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        cap = cv2.VideoCapture(Video_Index)

        def process_frame():
            nonlocal cap
            ret, frame = cap.read()
            if not ret:
                cap.release()
                cv2.destroyAllWindows()
                return

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(rgb_frame)

            detections = results.pandas().xyxy[0]
            persons = detections[detections['name'] == 'person']


            person_count = len(persons)

            if person_count > 0:
                change(person_count)

            for _, row in persons.iterrows():
                x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.putText(frame, f"Count: {person_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Room Monitoring", frame)

            if cv2.waitKey(1) & 0xFF != ord('q'):
                window.after(10, process_frame)
            else:
                cap.release()
                cv2.destroyAllWindows()

        process_frame()
    load_model()

    # window.mainloop()
    
    
def psw_admin():
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
        admin()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

def validate_and_take_images(txt,txt2,message1,trainImg):
    if not txt.get().strip() or not txt2.get().strip():
        mess.showwarning("Input Error", "Please fill in all required fields.")
    else:
        show_gif(lambda: TakeImages(window, txt, txt2, message, message1, trainImg))

        
def admin():
    root=tk.Tk()
    root.title("Admin")
    root.geometry("485x600")
    frame2 = tk.Frame(root, bg="#262523",highlightbackground="white", highlightthickness=2)
    frame2.place(relx=0, rely=0, width=485, height=600)
    head2 = tk.Label(frame2, text="For New Registrations", padx=124,fg="black",bg="#dfdfdf" ,font=('times', 17, ' bold '), highlightbackground="white", highlightthickness=2, anchor="center")
    head2.grid(row=0,column=0)
    lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg="white"  ,bg="#262523" ,font=('times', 17, ' bold ') )
    lbl.place(x=80, y=55)
    lbl_star = tk.Label(frame2, text="*", fg="red", bg="#262523", font=('times', 17, 'bold'))
    lbl_star.place(x=300, y=55)

    txt = tk.Entry(frame2,width=28 ,fg="black",font=('times', 15, ' bold '))
    txt.place(x=80, y=88)

    lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="white"  ,bg="#262523" ,font=('times', 17, ' bold '))
    lbl2.place(x=80, y=140)
    lbl_star = tk.Label(frame2, text="*", fg="red", bg="#262523", font=('times', 17, 'bold'))
    lbl_star.place(x=300, y=140)

    txt2 = tk.Entry(frame2,width=28 ,fg="black",font=('times', 15, ' bold ')  )
    txt2.place(x=80, y=173)

    message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg="#262523" ,fg="white"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
    message1.place(x=7, y=230)

    clearButton = tk.Button(frame2, text="Clear", command=lambda:clear(txt,message1)  ,fg="black"  ,bg="#ff8d84"  ,width=6 ,activebackground = "white" ,font=('times', 10, ' bold '), borderwidth=6)
    clearButton.place(x=365, y=86)
    clearButton2 = tk.Button(frame2, text="Clear", command=lambda:clear2(txt2,message1)  ,fg="black"  ,bg="#ff8d84"  ,width=6 , activebackground = "white" ,font=('times', 10, ' bold '), borderwidth=6)
    clearButton2.place(x=365, y=172)    
    takeImg = tk.Button(
        frame2, text="Take Images",
        command=lambda:validate_and_take_images(txt,txt2,message1,trainImg),
        fg="white", bg="#262523",
        width=34, height=1, activebackground="white",
        font=("times", 15, "bold"), borderwidth=10
    )
    takeImg.place(x=30, y=300)
    trainImg = tk.Button(frame2, text="Save Profile", command=lambda:psw(window,message,message1) ,fg="white"  ,bg="#262523"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '), borderwidth=10,state="disabled")
    trainImg.place(x=30, y=380)
    changeOnHover(takeImg, "#2df900", "#262523","black","white")
    changeOnHover(trainImg, "#2df900", "#262523","black","white")

    changeOnHover(clearButton,"#ea2a2a","#ff8d84","black","black")
    changeOnHover(clearButton2,"#ea2a2a","#ff8d84","black","black")
        
    bt = tk.Button(root, text="HEAT MAP",command=lambda:heat(root)  ,fg="white"  ,bg="#262523"  ,width=20  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '), borderwidth=10)
    # bt.place(relx=0.7,rely=0.1)
    bt_manual = tk.Button(root, text="Manual Entry",command=lambda:heat()  ,fg="white"  ,bg="#262523"  ,width=20  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '), borderwidth=10)
    # bt_manual.place(relx=0.1,rely=0.85)
    
    # lbl = tk.Label(root, text="Enter ID",width=20  ,height=1  ,fg="white"  ,bg="#262523" ,font=('times', 17, ' bold ') )
    # lbl.place(relx=0.4,rely=0.82)
    # txt = tk.Entry(root,width=28 ,fg="black",font=('times', 15, ' bold '))
    # txt.place(relx=0.4,rely=0.87)
    # root.mainloop()
############################################################################

################################################################################







# ######################################## USED STUFFS ############################################
    

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background='#262523')



frame1 = tk.Frame(window, bg="#262523",highlightbackground="white", highlightthickness=2)
frame1.place(relx=0.11, rely=0.17, relwidth=0.8, relheight=0.80)

# frame2 = tk.Frame(window, bg="#262523",highlightbackground="white", highlightthickness=2)
# frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance System" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)




datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"   |   ", fg="#e58905",bg="#262523" ,width=55 ,height=1,font=('times', 15, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="#e58905",bg="#262523" ,width=55 ,height=1,font=('times', 15, ' bold '), anchor="w")
clock.pack(fill='both',expand=1)
tick()

# head2 = tk.Label(frame2, text="For New Registrations", padx=124,fg="black",bg="#dfdfdf" ,font=('times', 17, ' bold '), highlightbackground="white", highlightthickness=2, anchor="center")
# head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="For Already Registered", padx=400,fg="black",bg="#dfdfdf" ,font=('times', 17, ' bold '), highlightbackground="white", highlightthickness=2)
head1.place(x=0,y=0)

# lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg="white"  ,bg="#262523" ,font=('times', 17, ' bold ') )
# lbl.place(x=80, y=55)

# txt = tk.Entry(frame2,width=28 ,fg="black",font=('times', 15, ' bold '))
# txt.place(x=80, y=88)

# lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="white"  ,bg="#262523" ,font=('times', 17, ' bold '))
# lbl2.place(x=80, y=140)

# txt2 = tk.Entry(frame2,width=28 ,fg="black",font=('times', 15, ' bold ')  )
# txt2.place(x=80, y=173)

# message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg="#262523" ,fg="white"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
# message1.place(x=7, y=230)

message = tk.Label(frame1, text="" ,bg="#00aeff" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
# message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance",width=50  ,fg="white"  ,bg="#262523"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=170, y=43)

res=0
exists = os.path.isfile("EmployeeDetails/EmployeeDetails.csv")
if exists:
    with open("EmployeeDetails/EmployeeDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2)
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################
style=ttk.Style()
style.theme_use('clam')
style.configure("Treeview.Heading", background="#8fc42b")
tv= ttk.Treeview(frame1,height =13,columns = ('name','date','intime','outtime'))

tv.column('#0',width=182)
tv.column('name',width=230)
tv.column('date',width=233)
tv.column('intime',width=185)
tv.column('outtime',width=185)
tv.grid(row=2,column=0,padx=(0,0),pady=(80,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('intime',text ='INTIME')
tv.heading('outtime',text ='OUTTIME')

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(80,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

# clearButton = tk.Button(frame2, text="Clear", command=lambda:clear(txt,message1)  ,fg="black"  ,bg="#ff8d84"  ,width=6 ,activebackground = "white" ,font=('times', 10, ' bold '), borderwidth=6)
# clearButton.place(x=365, y=86)
# clearButton2 = tk.Button(frame2, text="Clear", command=lambda:clear2(txt2,message1)  ,fg="black"  ,bg="#ff8d84"  ,width=6 , activebackground = "white" ,font=('times', 10, ' bold '), borderwidth=6)
# clearButton2.place(x=365, y=172)    
# takeImg = tk.Button(
#     frame2, text="Take Images",
#     command=lambda: show_gif(
#         lambda: TakeImages(window, txt, txt2, message, message1, trainImg)
#     ),
#     fg="white", bg="#262523",
#     width=34, height=1, activebackground="white",
#     font=("times", 15, "bold"), borderwidth=10
# )
# takeImg.place(x=30, y=300)
# trainImg = tk.Button(frame2, text="Save Profile", command=lambda:psw(window,message,message1) ,fg="white"  ,bg="#262523"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '), borderwidth=10,state="disabled")
# trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="Take Attendance", command=lambda:TrackImages(window,tv)  ,fg="white"  ,bg="#262523"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '), borderwidth=10)
trackImg.place(x=30,y=380)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="#ff8d84"  ,width=78 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '),borderwidth=10)
quitWindow.place(x=30, y=500)
Att = tk.Button(window, text="Admin Panel", command=lambda:psw_admin() ,fg="white"  ,bg="#262523"  ,width=11 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '),borderwidth=10)
Att.place(x=1100, y=10)


# changeOnHover(takeImg, "#2df900", "#262523","black","white")
# changeOnHover(trainImg, "#2df900", "#262523","black","white")

# changeOnHover(clearButton,"#ea2a2a","#ff8d84","black","black")
# changeOnHover(clearButton2,"#ea2a2a","#ff8d84","black","black")

changeOnHover(trackImg, "#2df900", "#262523","black","white")
changeOnHover(quitWindow, "#ea2a2a","#ff8d84","black","white")
changeOnHover(Att, "#2df900", "#262523","black","white")

##################### END ######################################
att(tv)
window.configure(menu=menubar)
# window.attributes('-fullscreen', True)
window.mainloop()

####################################################################################################

