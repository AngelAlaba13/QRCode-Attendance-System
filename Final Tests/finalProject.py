import datetime
import os
import logging
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
import qrcode
from threading import Thread
import sqlite3
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import re
from PIL import ImageTk, Image
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AttendanceMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x1100")
        self.root.config(bg="white")
        self.front()
        self.setup_database()
        
    def front(self):
        self.frontFrame = Frame(self.root, width=1200, height=1100)
        self.frontFrame.place(x=0, y=0)
        self.cover_image = Image.open("D:\VS Code Python\TKinter\QRCode Generator\imgs\cover.png")
        self.cover_photo = ImageTk.PhotoImage(self.cover_image)
        
        self.cover_photoLabel = Label(self.frontFrame, image=self.cover_photo, bg="#0F21A3")
        self.cover_photoLabel.place(x=0, y=0)
        
        self.startButton = Button(self.frontFrame, text="OPEN", font=("Arial", 25, "bold"), width=12, bg="white", fg="black", command=self.setup_gui)
        self.startButton.place(x=480, y=790)

    def setup_gui(self):
        self.frontFrame.place_forget()
        
        self.side_panel = Frame(self.root, height=1100, width=200, bg="#0F21A3")
        self.side_panel.place(x=0, y=0)
        self.generate_qr_frame = Frame(self.root, width=1000, height=1100, bg="#8CB7DE")
        self.attendance_record = Frame(self.root, width=1000, height=1100, bg="#8CB7DE")
        self.generate_qr()
       
        self.nemsu_logo_image = Image.open("D:/VS Code Python/TKinter/QRCode Generator/imgs/cite logo1.png")
        self.nemsu_logo_photo = ImageTk.PhotoImage(self.nemsu_logo_image)
        
        self.nemsu_logo = Label(self.side_panel, image=self.nemsu_logo_photo, bg="#0F21A3")
        self.nemsu_logo.place(x=20, y=25)
        
        self.register_bttn = Button(self.side_panel, text="Register", font=("Arial", 15), width=15, bg="#0768E0", fg="white", command=self.generate_qr)
        self.register_bttn.place(x=0, y=300)
        self.attendance_bttn = Button(self.side_panel, text="Attendance", font=("Arial", 15), width=14, bg="#0768E0", fg="white", command=self.display_information)
        self.attendance_bttn.place(x=0, y=400)

    def setup_database(self):
        self.conn = sqlite3.connect('attendance.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                          id INTEGER PRIMARY KEY,
                          user_id INTEGER,
                          name TEXT,
                          year INTEGER,
                          block TEXT,
                          time TEXT,
                          date TEXT
                          )''')
        self.conn.commit()

    # QR Code
    def generate_qr(self):
        self.attendance_record.place_forget()
        self.generate_qr_frame.place(x=200, y=0)
        
        registerLabel = Label(self.generate_qr_frame, text="REGISTER STUDENT", font=("", 40, "bold"),bg="#8CB7DE")
        registerLabel.place(x=180, y=80)
        
        idLabel = Label(self.generate_qr_frame, text="Student ID ", font=("", 20),bg="#8CB7DE")
        idLabel.place(x=95, y=250)
        id_num = Entry(self.generate_qr_frame, width=25, font=("Arial", 20))
        id_num.place(x=280, y=250)

        nameLabel = Label(self.generate_qr_frame, text="Name ", font=("", 20), bg="#8CB7DE")
        nameLabel.place(x=160, y=310)
        display_name = Entry(self.generate_qr_frame, width=25, font=("Arial", 20))
        display_name.place(x=280, y=310)

        yearBlockLabel = Label(self.generate_qr_frame, text="Year and Block ", font=("", 20), bg="#8CB7DE")
        yearBlockLabel.place(x=30, y=370)
        yearBlockEntry = Entry(self.generate_qr_frame, width=25, font=("Arial", 20))
        yearBlockEntry.place(x=280, y=370)
        
        def qr_gen():
            student_id = str(id_num.get())
            name = str(display_name.get())
            year_and_block = str(yearBlockEntry.get())
                
            qr_content = f"ID: {student_id} Name: {name} Year and Block: {year_and_block}"
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            save_dir = "D:\VS Code Python\TKinter\QRCode Generator\qrcodes"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            file_name = f"{name}_QRCode.png"
            img_path = os.path.join(save_dir, file_name)
            img.save(img_path)
            generatedQr = PhotoImage(file=img_path)
            generatedQr_label = Label(self.generate_qr_frame, image=generatedQr)
            generatedQr_label.image = generatedQr 
            generatedQr_label.place(x=270, y=510)
                        
            return img_path

        generate_btn = Button(self.generate_qr_frame, text="Generate", command=qr_gen, padx=10, bg="white")
        generate_btn.place(x=800, y=310)

    def close_conn(self):
        self.conn.close()
        self.root.destroy()
    
    # Database table
    def display_information(self):
        self.generate_qr_frame.place_forget()
        self.attendance_record.place(x=200, y=0)
    
        conn = self.get_database_connection()
        
        registerLabel = Label(self.attendance_record, text="ATTENDANCE", font=("", 40, "bold"),bg="#8CB7DE")
        registerLabel.place(x=300, y=80)
        
        scrollbar = Scrollbar(self.attendance_record)
        scrollbar.place(relx=0.96, rely=0.2, relheight=0.6, anchor='ne')
    
        tree = Treeview(self.attendance_record, columns=('No.', 'Student_ID', 'Name', 'Year', 'Block', 'Time', 'Date'), show="headings", height=33, yscrollcommand=scrollbar.set)
        tree.heading("#1", text="No.")
        tree.column("#1", width=60)
        tree.heading("#2", text="Student_ID")
        tree.column("#2", width=140)
        tree.heading("#3", text="Name")
        tree.column("#3", width=320)  
        tree.heading("#4", text="Year")
        tree.column("#4", width=70) 
        tree.heading("#5", text="Block")
        tree.column("#5", width=70) 
        tree.heading("#6", text="Time")
        tree.column("#6", width=120)  
        tree.heading("#7", text="Date")
        tree.column("#7", width=120) 
        
        scrollbar.config(command=tree.yview)

        c = conn.cursor()
        c.execute("SELECT id, user_id, name, year, block, time, date FROM attendance")
        rows = c.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

        tree.place(x=40, y=220)
        
        self.attendance_record.config(width=1000, height=1100)

    @staticmethod
    def get_database_connection():
        return sqlite3.connect('attendance.db')

def convertedData(data):
    string = str(data)
    conn = AttendanceMonitorApp.get_database_connection()

    # Data separater
    student_id_pattern = r'ID:\s*(\d{2}-\d{5})'
    name_pattern = r'Name:\s*(.*?)\s*Year\s*and\s*Block:'
    year_block_pattern = r'Year\s*and\s*Block:\s*(\d+)[A-Za-z]*([A-Za-z])$'

    student_id_match = re.search(student_id_pattern, string)
    name_match = re.search(name_pattern, string)
    year_block_match = re.search(year_block_pattern, string)

    if student_id_match:
        student_id = student_id_match.group(1)
    else:
        student_id = None

    if name_match:
        name = name_match.group(1).strip()
    else:
        name = None

    if year_block_match:
        year = year_block_match.group(1)
        block = year_block_match.group(2)
    else:
        year = None
        block = None

    philippine_tz = pytz.timezone('Asia/Manila')
    current_datetime = datetime.datetime.now(philippine_tz)
    current_date = current_datetime.date().isoformat()
    current_time = current_datetime.strftime('%I:%M %p')

    # Inserting data into the database
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE user_id = ?", (student_id,))
        result = cursor.fetchone()

        if result[0] > 0:
            messagebox.showinfo("Duplicate Entry", f"Record with Student ID {student_id} already exists.")
        else:
            response = messagebox.askyesno("Confirmation", f"Do you want to record the following QR code?\n\n{data}")
            if response:        
                    print(student_id, name, year, block, current_time, current_date)
                    conn.execute("INSERT INTO attendance (user_id, name, year, block, time, date) VALUES (?, ?, ?, ?, ?, ?)",(student_id, name, year, block, current_time, current_date))  
                    conn.commit()
                    messagebox.showinfo("Success","Recorded")
            else:
                    messagebox.showinfo("Success","Query denied")
                    pass
        
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        conn.close()

def run_gui():
    root = Tk()
    app = AttendanceMonitorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_conn)
    root.mainloop()

def run_scanner():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        if not success:
            break
        for code in decode(img):
            decoded_data = code.data.decode('UTF-8')
            convertedData(decoded_data)
            logging.info(decoded_data)
            rect_pts = code.rect
            if decoded_data:
                pts = np.array([code.polygon], np.int32)
                cv2.polylines(img, [pts], True, (0, 225, 0), 3)
        
        cv2.imshow("Img: ", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    gui_thread = Thread(target=run_gui)
    scanner_thread = Thread(target=run_scanner)

    gui_thread.start()
    scanner_thread.start()
