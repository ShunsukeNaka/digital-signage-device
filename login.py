import requests
import tkinter as tk
from tkinter import messagebox

import ds_key


url = "https://be.fukunage-device.fukunova.jp/login"

def check_login():
    userid = entry_user.get()
    password = entry_pass.get()
    deviceid = entry_device.get()
    
    body = {
        "user": {
            "id": userid,
            "pass": password
        },
        "device": {
            "id": deviceid
        }
    }

    response = requests.post(url, json=body)
    data = response.json()

    if data["status"] == "success":
        ds_key.generate_and_save_key()
        ds_key.encrypt_and_save_token(data['token'], outfile="device_token.enc")
        # messagebox.showinfo("Token", f"{data['token']}")
        root.after(100, root.destroy)
    else:
        messagebox.showerror(f"userid: {userid} \npassword: {password} \ndeviceid: {deviceid}")

#    if username in USERS and USERS[username] == password:
#        messagebox.showinfo("Success", f"Welcome {username}!")
#        root.destroy()
#    else:
#        messagebox.showerror("Failed", "Login failed!")

root = tk.Tk()
root.title("Login")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
#root.attributes('-fullscreen', True)

tk.Label(root, text="UserID").pack(pady=(10,0))
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="UserPassword").pack(pady=(10,0))
entry_pass = tk.Entry(root)
entry_pass.pack()

tk.Label(root, text="DeviceID").pack(pady=(10,0))
entry_device = tk.Entry(root)
entry_device.pack()

tk.Button(root, text="Login", command=check_login).pack(pady=10)

root.mainloop()
