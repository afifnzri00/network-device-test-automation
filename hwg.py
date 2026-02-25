import tkinter as tk
import time
import threading
import pygame
from tkinter import *
from tkinter import simpledialog
from tkinter import PhotoImage
from tkinter import font

from checkip import check_ips_init
from checkip import check_ips
from hws import hws_trigger
from hws import hws_init
from hws import HW_SEND_2

from changeip import change_first_ip

from datetime import timedelta,datetime


class TimerApp:
    def __init__(self, root,):
        self.root = root
        self.time_var = tk.StringVar()
        self.time_var.set("00:00:00:00")
        self.label_timer = tk.Label(
            root,
            textvariable=self.time_var,
            font=("Helvetica", 24),
            bg = '#dee6ef',
            )
        self.label_timer.grid(
            row=3,
            column=0,
            columnspan=11,
            rowspan=2,
            )
        self.label_timer_format = tk.Label(
            root,
            text = "Day:Hour:Minute:Second",
            font=("Helvetica", 14),
            bg = '#dee6ef',
            )
        self.label_timer_format.grid(
            row=5,
            column=0,
            columnspan=11,
            rowspan=2,

            )
 
        self.elapsed_time = timedelta()
        self.stop_flag = threading.Event()

        
        # self.update_time()
        # self.update_timer()

    def update_time(self):

        if not self.stop_flag.is_set():
            formatted_time = datetime(1, 1, 1) + self.elapsed_time
            days = formatted_time.day - 1  # Subtracting 1 to get the correct day count
            time_str = " {:02}:{:02}:{:02}:{:02}".format(days, formatted_time.hour, formatted_time.minute, formatted_time.second)
            self.time_var.set(time_str)
            self.root.after(1000, self.update_time)

    def update_timer(self):

        if not self.stop_flag.is_set():
            self.elapsed_time += timedelta(seconds=1)
            self.root.after(1000, self.update_timer)



    def timer_stop(self):
        self.stop_flag.set()
    
    def timer_resume(self):
        if self.stop_flag.is_set():
            self.stop_flag.clear()
            self.update_time()
            self.update_timer()
        else:
            self.update_time()
            self.update_timer()

    
    def timer_forget(self):
        self.label_timer.destroy()
        self.label_timer_format.destroy()

class changeip_devicelabel:
    # def __init__(self, root,x1, y1, text):
    def __init__(self, root,row, column, text):
        self.label = tk.Label(
            root,
            text=text,
            bg="white",
            height=1,
            width=15,
            font=("Helvetica",24,"normal"),
            relief="solid",
            borderwidth=3,
            anchor="center",  # or "w", "e", "s", "se", etc.
            justify="center",  # or "left", "right"
            # wraplength=200  
            )
        self.label.grid(
            row=row,
            column=column,
            columnspan=2,
            )
        # self.label.config(pady=8)  
        # self.label.grid(row=row,column=column,sticky = "ew")

    def changeip_change_color(self, new_color):
        self.label.configure(bg=new_color)
  
    def changeip_forget_label(self):
        self.label.destroy()

class burntest_devicelabel:
    # def __init__(self, root,x1, y1, text):
    def __init__(self, root,row, column, sub_text):
        # self.label = tk.Label(root, text="192.168.0."+text, bg="light grey",width=15,font=("Helvetica", 24),relief="solid", borderwidth=2)
        fail_text="Fail:  "
        space_text = "     "
        
        self.mainlabel = tk.Label(
            root,
            text= fail_text+space_text,
            bg="White",
            height=2,
            width=20,
            font=("Helvetica", 12,"bold"),
            relief="solid",
            anchor="e",  # or "w", "e", "s", "se", etc.
            # justify="right",  # or "left", "right"

            borderwidth=2)
        # self.mainlabel.config(
        #     pady=8
        #     )  
        self.mainlabel.grid(
            row=row,
            column=column,
            columnspan = 1,
            sticky = "ew",
            )
        
        self.sublabel = tk.Label(
            root,
            text=sub_text,
            # bg="light grey",
            bg = "white",
            height=2,
            width=25,
            font=("Helvetica", 12,"bold"),
            relief="solid",
            borderwidth=2
            )
        
        self.sublabel.grid(
            row=row,
            column=column,
            columnspan = 1,
            sticky = "w"
            )

        self.failcount = 0  # Initialize failcount to 0 for each instance
        # self.fail_status = False

    # def burntest_change_color(self, new_color,fail_text,failcount):
    def burntest_change_color(self, new_color,failcount):
        # if self.fail_status:
        #     text += " Fail"
        # else:
        #     text += " PASS"
        # text = fail_text
        # text += str(failcount)
        text = f"Fail: {str(failcount)}    "
        # self.label.configure(bg=new_color,text = text)
        self.sublabel.configure(bg=new_color)
        self.mainlabel.configure(text = text)
        

    def burntest_forget_label(self):
        self.mainlabel.destroy()
        self.sublabel.destroy()

class burntest_faillabel:
    # def __init__(self, root,x1, y1, text):
    def __init__(self, root,row, column, text):
        self.label = tk.Label(
            root,
            text=text,
            bg="light grey",
            width=10,
            font=("Helvetica", 12,"bold"),
            relief="solid", borderwidth=2
            )
        self.label.config(
            # pady=8
            )  
        self.label.grid(
            row=row,
            column=column,
            # sticky ="w"
            )
        # self.fail_status = False
        self.failcount = 0  # Initialize failcount to 0 for each instance

class GUI:
    def __init__(self, root):
        self.sound_trigger = threading.Event()
        self.sound_trigger.set()
        self.stop_trigger = True
        self.disconnect_found = False
        self.root = root
        self.root.title("IPX5455 TEST")
        self.root.iconbitmap(r"C:\for IPX5455 test program\amperes_logo.ico")  
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        background_colour = "#dee6ef"
        self.root.configure(bg=background_colour)  # Change 'lightblue' to your desired color

        # self.timer = None
        # self.previous_connect_status = [None] * 40
        self.main_win()

    def main_win(self):

        # empty_label_left = tk.Label(self.root, text="")
        # empty_label_right = tk.Label(self.root, text="")

        image_path = r"C:\for IPX5455 test program\amperes_logo_main.png"  
        self.img = PhotoImage(file=image_path)
        self.photo_label_main = tk.Label(
            self.root,
            image=self.img,
            bg = '#dee6ef'
            )
        self.photo_label_main.grid(
            row=0,
            column=0,
            columnspan=11
            )
 
        text = "IPX5455 TESTING"
        bold_font = font.Font(
            family="Arial",
            size=38,
            weight="bold"
            )
        self.text_label = tk.Label(
            self.root,
            text=text,
            font=bold_font,bg = '#dee6ef'
            )
        self.text_label.grid(
            row=1,
            column=0,
            columnspan=11
            )

        self.button1 = tk.Button(
            self.root,
            width = 15,
            # height = 2,
            text="CHANGE IP",
            font=("Arial", 14, "bold"),
            fg = 'white',
            bg = '#0c4da2',
            relief= "flat",
            command=self.change_ip
            )
        self.button1.grid(
            row=10,
            column=3,
            columnspan=2,
            sticky="ns"
            )

        self.button2 = tk.Button(
            self.root,
            width = 15,
            # height = 2,
            text="BURN TEST",
            font=("Arial", 14, "bold"),
            fg = 'white',
            bg = '#0c4da2',
            relief= "flat",
            command=self.burn_test
            )
        self.button2.grid(
            row=10,
            column=6,
            columnspan=2,
            sticky="ns"
            )
    
        for col in [0,2,4,6,8,10]:
            self.root.columnconfigure(col,weight=2)
        for col in [1,3,5,7,9,]:
            self.root.columnconfigure(col, weight=1)



        for row in [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]:
            self.root.rowconfigure(row, minsize=2)
        
    def change_ip(self):
        self.photo_label_main.destroy()
        self.text_label.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.run_changeip()

    def burn_test(self):
        self.photo_label_main.destroy()
        self.text_label.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.run_burntest()

    def changeip_label_init(self):
        self.label1  = changeip_devicelabel(self.root,  3, 0,"192.168.0.101")
        self.label2  = changeip_devicelabel(self.root,  3, 3,"192.168.0.102")
        self.label3  = changeip_devicelabel(self.root,  3, 6,"192.168.0.103")
        self.label4  = changeip_devicelabel(self.root,  3, 9,"192.168.0.104")

        self.label5  = changeip_devicelabel(self.root,  5, 0,"192.168.0.105")
        self.label6  = changeip_devicelabel(self.root,  5, 3,"192.168.0.106")
        self.label7  = changeip_devicelabel(self.root,  5, 6,"192.168.0.107")
        self.label8  = changeip_devicelabel(self.root,  5, 9,"192.168.0.108")

        self.label9  = changeip_devicelabel(self.root,  7, 0,"192.168.0.109")
        self.label10 = changeip_devicelabel(self.root,  7, 3,"192.168.0.110")
        self.label11 = changeip_devicelabel(self.root,  7, 6,"192.168.0.111")
        self.label12 = changeip_devicelabel(self.root,  7, 9,"192.168.0.112")

        self.label13 = changeip_devicelabel(self.root,  9, 0,"192.168.0.113")
        self.label14 = changeip_devicelabel(self.root,  9, 3,"192.168.0.114")
        self.label15 = changeip_devicelabel(self.root,  9, 6,"192.168.0.115")
        self.label16 = changeip_devicelabel(self.root,  9, 9,"192.168.0.116")

        self.label17 = changeip_devicelabel(self.root, 11, 0,"192.168.0.117")
        self.label18 = changeip_devicelabel(self.root, 11, 3,"192.168.0.118")
        self.label19 = changeip_devicelabel(self.root, 11, 6,"192.168.0.119")
        self.label20 = changeip_devicelabel(self.root, 11, 9,"192.168.0.120")

        self.label21 = changeip_devicelabel(self.root, 13, 0,"192.168.0.121")
        self.label22 = changeip_devicelabel(self.root, 13, 3,"192.168.0.122")
        self.label23 = changeip_devicelabel(self.root, 13, 6,"192.168.0.123")
        self.label24 = changeip_devicelabel(self.root, 13, 9,"192.168.0.124")

        self.label25 = changeip_devicelabel(self.root, 15, 0,"192.168.0.125")
        self.label26 = changeip_devicelabel(self.root, 15, 3,"192.168.0.126")
        self.label27 = changeip_devicelabel(self.root, 15, 6,"192.168.0.127")
        self.label28 = changeip_devicelabel(self.root, 15, 9,"192.168.0.128")

        self.label29 = changeip_devicelabel(self.root, 17, 0,"192.168.0.129")
        self.label30 = changeip_devicelabel(self.root, 17, 3,"192.168.0.130")
        self.label31 = changeip_devicelabel(self.root, 17, 6,"192.168.0.131")
        self.label32 = changeip_devicelabel(self.root, 17, 9,"192.168.0.132")

        self.label33 = changeip_devicelabel(self.root, 19, 0,"192.168.0.133")
        self.label34 = changeip_devicelabel(self.root, 19, 3,"192.168.0.134")
        self.label35 = changeip_devicelabel(self.root, 19, 6,"192.168.0.135")
        self.label36 = changeip_devicelabel(self.root, 19, 9,"192.168.0.136")

        self.label37 = changeip_devicelabel(self.root, 21, 0,"192.168.0.137")
        self.label38 = changeip_devicelabel(self.root, 21, 3,"192.168.0.138")
        self.label39 = changeip_devicelabel(self.root, 21, 6,"192.168.0.139")
        self.label40 = changeip_devicelabel(self.root, 21, 9,"192.168.0.140")

    def burntest_label_init(self):
        self.label1  = burntest_devicelabel(self.root,  7, 2, "192.168.0.101")
        self.label2  = burntest_devicelabel(self.root,  7, 4, "192.168.0.102")
        self.label3  = burntest_devicelabel(self.root,  7, 6, "192.168.0.103")
        self.label4  = burntest_devicelabel(self.root,  7, 8, "192.168.0.104")

        self.label5  = burntest_devicelabel(self.root,  9, 2, "192.168.0.105")
        self.label6  = burntest_devicelabel(self.root,  9, 4, "192.168.0.106")
        self.label7  = burntest_devicelabel(self.root,  9, 6, "192.168.0.107")
        self.label8  = burntest_devicelabel(self.root,  9, 8, "192.168.0.108")

        self.label9  = burntest_devicelabel(self.root,  11, 2, "192.168.0.109")
        self.label10 = burntest_devicelabel(self.root,  11, 4, "192.168.0.110")
        self.label11 = burntest_devicelabel(self.root,  11, 6, "192.168.0.111")
        self.label12 = burntest_devicelabel(self.root,  11, 8, "192.168.0.112")

        self.label13 = burntest_devicelabel(self.root,  13, 2,"192.168.0.113")
        self.label14 = burntest_devicelabel(self.root,  13, 4,"192.168.0.114")
        self.label15 = burntest_devicelabel(self.root,  13, 6,"192.168.0.115")
        self.label16 = burntest_devicelabel(self.root,  13, 8,"192.168.0.116")

        self.label17 = burntest_devicelabel(self.root,  15, 2, "192.168.0.117")
        self.label18 = burntest_devicelabel(self.root,  15, 4, "192.168.0.118")
        self.label19 = burntest_devicelabel(self.root,  15, 6, "192.168.0.119")
        self.label20 = burntest_devicelabel(self.root,  15, 8, "192.168.0.120")

        self.label21 = burntest_devicelabel(self.root,  17, 2, "192.168.0.121")
        self.label22 = burntest_devicelabel(self.root,  17, 4, "192.168.0.122")
        self.label23 = burntest_devicelabel(self.root,  17, 6, "192.168.0.123")
        self.label24 = burntest_devicelabel(self.root,  17, 8, "192.168.0.124")

        self.label25 = burntest_devicelabel(self.root,  19, 2, "192.168.0.125")
        self.label26 = burntest_devicelabel(self.root,  19, 4, "192.168.0.126")
        self.label27 = burntest_devicelabel(self.root,  19, 6, "192.168.0.127")
        self.label28 = burntest_devicelabel(self.root,  19, 8, "192.168.0.128")

        self.label29 = burntest_devicelabel(self.root,  21, 2, "192.168.0.129")
        self.label30 = burntest_devicelabel(self.root,  21, 4, "192.168.0.130")
        self.label31 = burntest_devicelabel(self.root,  21, 6, "192.168.0.131")
        self.label32 = burntest_devicelabel(self.root,  21, 8, "192.168.0.132")

        self.label33 = burntest_devicelabel(self.root, 23, 2, "192.168.0.133")
        self.label34 = burntest_devicelabel(self.root, 23, 4, "192.168.0.134")
        self.label35 = burntest_devicelabel(self.root, 23, 6, "192.168.0.135")
        self.label36 = burntest_devicelabel(self.root, 23, 8, "192.168.0.136")

        self.label37 = burntest_devicelabel(self.root, 25, 2, "192.168.0.137")
        self.label38 = burntest_devicelabel(self.root, 25, 4, "192.168.0.138")
        self.label39 = burntest_devicelabel(self.root, 25, 6, "192.168.0.139")
        self.label40 = burntest_devicelabel(self.root, 25, 8, "192.168.0.140")



####################################################################################
############################### CHANGE IP FUNCTION #################################
####################################################################################

    def run_changeip(self):

        image_path = r"C:\for IPX5455 test program\amperes_logo_changeip.png"  
        self.img = PhotoImage(file=image_path)
        self.photo_label_changeip = tk.Label(
            self.root,
            image=self.img,
            bg = '#dee6ef'
            )
        self.photo_label_changeip.grid(
            row=1,
            column=0,
            columnspan= 11
            )

        self.changeip_label_init()

        self.button5 = tk.Button(
            self.root,
            width=15,
            height=2,
            text="CHANGE IP",
            font=("Arial",10,"bold"),
            fg = 'white',
            bg = '#0c4da2',
            relief= "flat",
            command=self.trigger_change_ip_fisrt
            )
        self.button5.grid(
            row=23, 
            column=3,
            columnspan = 2,
            )
    
        self.button6 = tk.Button(
            self.root,
            width=15,
            height=2,
            text="HOME",
            font=("Arial",10,"bold"),
            fg = 'white',
            bg = '#0c4da2',
            relief= "flat",
            command=self.run_changeip_returnhome,
            )
        self.button6.grid(
            row=23,
            column=6,
            columnspan = 2,
            )


    def ask_begin_ip(self):
        try:
            user_input_2 = simpledialog.askinteger("Change IP Adress", "Enter the first new ip adress \n E.g: 101,102,103,..140",parent=self.root)
            if  user_input_2 is not None and user_input_2 in range (101,141):
                return user_input_2
            else:
                print("Error: No input provided. Please enter a valid value.")
        except ValueError as e:
            print(f"Error: {e}")

    def trigger_change_ip_fisrt(self):
        first_ip = self.ask_begin_ip()
        self.trigger_changeip(first_ip)

    def trigger_changeip(self,first_ip):
        self.trigger_change_ip_begin(first_ip)

    def trigger_change_ip_begin(self,first_ip):
        t2 = threading.Thread(target=self.change_ip_thread, args=(first_ip,))
        t2.start()

    def change_ip_thread(self,first_ip):
        change_ip_result =  change_first_ip(first_ip)
        self.trigger_change_ip_update_colour(first_ip,change_ip_result)

    def trigger_change_ip_update_colour(self,first_ip,change_ip_result):
        if change_ip_result:
            new_color = "light green"
        else:
            new_color = "red"
        label = getattr(self, f"label{first_ip - int (100)}")
        label.changeip_change_color(new_color)
        self.trigger_change_ip_continue(first_ip)

    def trigger_change_ip_continue(self,first_ip):
        loop_changeip = tk.messagebox.askquestion("Change IP adress", "Do you want to continue change IP address on next DUT?")
        if loop_changeip == 'yes':
            first_ip = first_ip + int(1)
            self.trigger_change_ip_begin(first_ip)
        else:
            pass

    def run_changeip_returnhome(self):
        for i in range (1,41):
            label = getattr(self, f"label{i}")
            label.changeip_forget_label()
        self.photo_label_changeip.destroy()
        self.button5.destroy()
        self.button6.destroy()
        self.main_win()

####################################################################################
############################## burn test function ##################################
####################################################################################
    def run_burntest(self):
        self.timer = TimerApp(self.root)     

        image_path = r"C:\for IPX5455 test program\amperes_logo_burntest.png"  
        self.img = PhotoImage(file=image_path)
        self.photo_label_burntest = tk.Label(
            self.root,
            image=self.img,
            bg = '#dee6ef',
            )
        self.photo_label_burntest.grid(
            row = 0,
            column = 0,
            columnspan = 11
            )
        
        pygame.mixer.init()
        file_path = r"C:\for IPX5455 test program\beep.wav"
        pygame.mixer.music.load(file_path)

        self.disconnect_found = False
        self.keep_running = True
        self.previous_connect_status = [None] * 40
        self.pagingcount = 0

        self.burntest_label_init()

        self.button5 = tk.Button(
            self.root,
            width=15,
            height=2,
            relief= "flat",
            text="REFRESH ",
            font=("Arial",10,"bold"),
            fg = 'white',
            bg = '#0c4da2',
            # command=lambda:self.toggle_trigger(paging_auth_token)
            )
        self.button5.config(
            width=15,
            height=2,
            relief= "flat",
            font=("Arial",10,"bold"),
            fg = 'white',
            bg = '#0c4da2',
            )
        self.button5.grid(
            row=27,
            column=2,
            columnspan=2,
            )

        self.button3 = tk.Button(
            self.root,
            width=15,
            height=2,
            relief= "flat",
            text="TRIGGER PAGING\nPaging count: 0",
            font=("Arial",10,"bold"),
            fg = 'white',
            bg = '#0c4da2',
            command=lambda:self.toggle_trigger(paging_auth_token)
            # command=lambda:self.toggle_trigger(selected_com = clicked.get())
            )
        self.button3.grid(
            row=27,
            column=4,
            columnspan=3
            )
        self.button4 = tk.Button(
            self.root,
            width=15,
            height=2,
            relief= "flat",
            text="HOME",
            font=("Arial",10,"bold"),
            fg = 'white',
            bg = '#0c4da2',
            command=self.run_burntest_returnhome
            )
        self.button4.grid(
            row=27,
            column=7,
            columnspan=2,
            )

        unit_test = self.ask_check_unit()

        server_init = check_ips_init()
        if server_init == False:
            print("Server disconnect")
            self.disconnect_server()
        else:
            server_auth_token = server_init
            print(f"Server auth token:{server_auth_token}")
            self.update_colors(unit_test,server_auth_token)


        paging_init = hws_init()
        if paging_init == False:
            print("Paging device disconnected")
        else:
            paging_auth_token = paging_init
            print(f"Paging auth token:{paging_auth_token}")

        # self.update_colors(unit_test,server_auth_token)
        
        self.sound_trigger.clear()
        t1 = threading.Thread(target=self.play_song)
        t1.start()
 
    def run_burntest_returnhome(self):
        if not self.stop_trigger: # to terminate trigger paging
            self.stop_trigger = not self.stop_trigger
        self.keep_running = False
        self.disconnect_found = False
        for i in range (1,41):
            label = getattr(self, f"label{i}")
            label.burntest_forget_label()
        # self.drop.destroy()
        self.photo_label_burntest.destroy()
        self.button3.destroy()
        self.button4.destroy()
        self.button5.destroy()
        self.main_win()
        self.sound_trigger.set()
        if self.timer:  #stop timer
            self.timer.timer_stop() 
            self.timer.timer_forget()

    def run_burntest_triggerpaging(self,paging_auth_token):
        if not self.stop_trigger:
            if hws_trigger(paging_auth_token):
                self.button3.flash()
                self.pagingcount += 1
                pagingcount = str(self.pagingcount)
                self.button3.config(text= f"TRIGGER PAGING\nPaging count: {pagingcount}")
                self.root.after(60000,self.run_burntest_triggerpaging,paging_auth_token)
            else:
                self.timer.timer_stop() 
                self.button3.config(bg = "red")
                self.stop_trigger = not self.stop_trigger
                tk.messagebox.showinfo("Paging server error", "Cannot access paging server")
                return 
  
    # def toggle_trigger(self,selected_com):
    def toggle_trigger(self,paging_auth_token):
        paging_reset = HW_SEND_2(paging_auth_token)
        try:
            self.stop_trigger = not self.stop_trigger
            if not self.stop_trigger:
                self.timer.timer_resume()
                self.button3.config(
                    fg = "black",
                    bg="light green",
                    # bg = "#0c4da2",
                    )
                # paging_reset = HW_SEND_2(paging_auth_token)
                if paging_reset == True:
                    self.run_burntest_triggerpaging(paging_auth_token)
                # self.run_burntest_triggerpaging(selected_com)
            else:
                self.timer.timer_stop() 
                self.button3.config(
                    # bg = "SystemButtonFace"
                    fg = "white",
                    bg = "#0c4da2",
                    )
        except Exception as e:
                print(f"Error: {e}")     
   
    def ask_check_unit(self):
        try:
            user_input_1 = simpledialog.askinteger("Total DUT Tested", "Enter device total unit:",parent=self.root)
            if  user_input_1 is not None and user_input_1 in range (1,11):
                user_input_1 = (4*(int(user_input_1)))+1
                return user_input_1
            else:
                print("Error: No input provided. Please enter a valid value.")
        except ValueError as e:
            print(f"Error: {e}")

    def update_colors(self,unit_test,server_auth_token):
        if not self.keep_running: 
            return
        connect_status = check_ips(server_auth_token)
        if connect_status == False:     #just added,checks if server disconnected
            self.disconnect_server()    #just added,checks if server disconnected
        all_true = all(connect_status[0:unit_test-1])
        if all_true:
            self.disconnect_found = False
        else:
            self.disconnect_found = True

        for i in range (1,unit_test):
            label = getattr(self, f"label{i}")
            if self.previous_connect_status[i-1] is None:
                # print("ayam")
                if connect_status [i-1]:
                    new_color = "light green"
                    failcount = label.failcount
                else:
                    new_color = "red"
                    label.failcount += 1
                    failcount = label.failcount
                label.burntest_change_color(new_color,failcount)
            
            elif connect_status[i-1] != self.previous_connect_status[i-1]:
                # print("kambing")
                if connect_status [i-1]:
                    new_color = "light green"
                    failcount = label.failcount
                else:
                    new_color = "red"
                    label.failcount += 1
                    failcount = label.failcount
                label.burntest_change_color(new_color,failcount)

            self.previous_connect_status[i-1] = connect_status[i-1]

        self.root.after(500, self.update_colors,unit_test,server_auth_token)  

    def play_song(self):
        while not self.sound_trigger.is_set():
            self.play_song_trigger()

    def play_song_trigger(self):
        if self.disconnect_found:
            pygame.mixer.music.play()
            time.sleep(3)
            pygame.mixer.music.stop()

    def disconnect_server(self):
        self.timer.timer_stop() 
        # self.timer = None 
        tk.messagebox.showinfo("Server disconnect", "Check the IPX5101 server")
        return

def hwg_main():
    root = tk.Tk()
    GUI(root)
    root.mainloop()

if __name__ == "__main__":
    hwg_main()