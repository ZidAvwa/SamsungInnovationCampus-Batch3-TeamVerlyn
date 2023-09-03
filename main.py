import tkinter as tk
from tkinter import font
import cv2
from PIL import Image, ImageTk
import subprocess
from gpiozero import DistanceSensor
from time import sleep
import RPi.GPIO as GPIO

filename = 'detect.py' 
sensor = DistanceSensor(23, 24)
led = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
warna = 'white'


# Membuat window
window = tk.Tk()
window.title("Tatib Auto")
#window.attributes('-fullscreen', True)
window.geometry('1024x600')
window.configure(background= warna)
tek = font.Font(family="Terminal", size=20)
# Membuat frame untuk webcam
frame_webcam = tk.Frame(window, bg=warna)
frame_webcam.grid(column=3, pady=10, row=0, sticky="ne")

# Membuat label untuk menampilkan webcam
label_webcam = tk.Label(frame_webcam)
label_webcam.pack()

frame3 = tk.Frame(container=False)
frame3.configure(
    background="black",
    borderwidth=6.5,
    height=180,
    width=480)
frame3.grid(column=3, row=1, sticky="se")

frame_depesi = tk.Frame(container=False)
frame_depesi.configure(background="black", height=170, width=515)
frame_depesi.grid(column=0, padx=10, pady=10, row=0, sticky="nw")

depesi = Image.open("depesilogo.png")
depesi = depesi.resize((515, 170))
depesi = ImageTk.PhotoImage(depesi)
label_depesi = tk.Label(frame_depesi, image=depesi, bg=warna)
label_depesi.pack()

frame5 = tk.Frame(container=False)
frame5.configure(height=370, width=515)
frame5.grid(column=0, padx=10, row=0, rowspan=2, sticky="sw")

# Membuat frame untuk logo dan nama
frame_logo = tk.Frame(window, bg= warna)
frame_logo.grid(column=0, padx=10, row=0, rowspan=2, sticky="sw")

# Membaca logo
logo = Image.open("logologo.png")
logo = logo.resize((515, 370))
logo = ImageTk.PhotoImage(logo)

# Membuat label untuk menampilkan logo
label_logo = tk.Label(frame_logo, image=logo, bg=warna)
label_logo.pack()

# Fungsi untuk mengambil gambar dari webcam
def ambil_gambar():
    ret, frame = cap.read()
    
    text1 = tk.Label(frame3, text="Silahkan Scan...")
    text1.configure(background="white", font=tek, height=5, width=29)
    text1.grid(column=3, row=1, sticky="se")
    
    if ret:
        frame2 = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame2 = cv2.resize(frame2, (480, 360))
        img = Image.fromarray(frame2)
        imgtk = ImageTk.PhotoImage(image=img)
        label_webcam.imgtk = imgtk
        label_webcam.configure(image=imgtk)
        GPIO.output(led, GPIO.HIGH)
        
        sensorcm = sensor.distance * 100
        print(round(sensorcm, 1))
        cv2.waitKey(1) & 0xFF == ord('s')
        
        if sensorcm < 4.0:
            text1 = tk.Label(frame3, text="Tunggu Sebentar...")
            text1.configure(background="white", font=tek, height=5, width=27)
            text1.grid(column=3, row=1, sticky="se")
            if sensorcm < 3.0 :
                print("Tunggu Sebentar..")
                GPIO.output(led, GPIO.LOW)
                cv2.imwrite('foto1.jpg', frame)
                subprocess.run(['python3', filename])
    label_webcam.after(10, ambil_gambar)
# Menginisialisasi webcam
cap = cv2.VideoCapture(0)

# Memanggil fungsi untuk mengambil gambar dari webcam
ambil_gambar()

# Menjalankan aplikasi
window.mainloop()

# Menghentikan webcam
cap.release()

