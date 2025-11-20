import tkinter as tk
import pyttsx3
import webbrowser
import datetime
import wikipedia
import pywhatkit
import threading
import time
#KHỞI TẠO
engine = pyttsx3.init()
wikipedia.set_lang("vi")
#NÓI
def speak(text):
    engine.say(text)
    engine.runAndWait()
#HẸN GIỜ
def start_timer(seconds):
    def countdown():
        time.sleep(seconds)
        response = "Hết giờ rồi!"
        show_chat("Assistant", response)
        speak("Hết giờ rồi!")
    threading.Thread(target=countdown, daemon=True).start()

def parse_timer(cmd):
    # Giây
    if "giây" in cmd:
        num = int(cmd.split("hẹn giờ")[1].split("giây")[0].strip())
        return num
    # Phút
    if "phút" in cmd:
        num = int(cmd.split("hẹn giờ")[1].split("phút")[0].strip())
        return num * 60

# HÀM XỬ LÝ
def process_command(command):
    cmd = command.lower()

    #HIỂN THỊ TRÊN CHAT
    chat_box.insert(tk.END, f"Bạn: {command}\n")

    if "xin chào" in cmd:
        response = "Xin chào, tao là trợ lý của mi"
    elif "hẹn giờ" in cmd:
        seconds = parse_timer(cmd)
        if seconds:
            start_timer(seconds)
            response = f"Đã hẹn giờ {seconds} giây."
        show_chat("Bạn", command)

    elif "mấy giờ" in cmd:
        now = datetime.datetime.now().strftime("%H:%M")
        response = f"Giờ là {now}"

    elif "hôm nay ngày mấy" in cmd or "ngày mấy" in cmd:
        today = datetime.datetime.now().strftime("%d/%m/%Y")
        response = f"Hôm nay là  {today}"

    elif "mở youtube" in cmd:
        webbrowser.open("https://youtube.com")
        response = "Mở YouTube."

    elif "facebook" in cmd:
        webbrowser.open("https://facebook.com")
        response = "Mở Facebook."

    elif "tìm kiếm" in cmd:
        query = cmd.replace("tìm kiếm", "")
        pywhatkit.search(query)
        response = f"Đang tìm kiếm {query} trên Google."

    elif "phát nhạc" in cmd:
        song = cmd.replace("phát nhạc", "")
        pywhatkit.playonyt(song)
        response = f"Đang phát bài {song}."

    elif "wikipedia" in cmd:
        try:
            keyword = cmd.replace("wikipedia", "")
            info = wikipedia.summary(keyword, sentences=2)
            response = info
        except:
            response = "Tôi không tìm thấy thông tin."

    elif "tạm biệt" in cmd or "thoát" in cmd:
        speak("GOODBYE, HOPE TO SEE YOU AGAIN")
        root.destroy()
        return

    else:
        response = "Tôi chưa hiểu lệnh này, bạn có thể thử lệnh khác."

    # In ra giao diện + nói
    chat_box.insert(tk.END, f"Assistant: {response}\n\n")


#GỬI TEXT
def send_text():
    text = entry.get()
    entry.delete(0, tk.END)
    process_command(text)
def show_chat(who, text):
    if who == "Bạn":
        chat_box.insert(tk.END, f"Bạn đã {text}\n", "user")
    chat_box.yview_moveto(1)

# GIAO DIỆN TKINTER
root = tk.Tk()
root.title("Trợ Lý Ảo bản low quality edition")
root.geometry("1000x900")

title = tk.Label(root, text="TRỢ LÝ ẢO", font=("Arial", 20, "bold"))
title.pack(pady=10)

chat_box = tk.Text(root, font=("Arial", 12), width=60, height=25)
chat_box.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=40)
entry.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

btn_send = tk.Button(btn_frame, text="Gửi", width=10, command=send_text)
btn_send.grid(row=0, column=0, padx=10)
root.mainloop()

