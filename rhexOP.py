import ctypes
import os
import sys
import tkinter as tk
import psutil
import gc

kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

def optimize_ram():
    initial_ram = psutil.virtual_memory().percent
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pid = proc.info['pid']
            if pid <= 4:
                continue
            
            handle = kernel32.OpenProcess(0x1F0FFF, False, pid)
            if handle:
                kernel32.SetProcessWorkingSetSize(handle, -1, -1)
                psapi.EmptyWorkingSet(handle)
                kernel32.CloseHandle(handle)
        except Exception:
            continue

    gc.collect()
    final_ram = psutil.virtual_memory().percent
    
    btn_rhexo.config(
        text=f"%{initial_ram} -> %{final_ram}", 
        bg="#27ae60", 
        fg="#ffffff"
    )
    root.after(2000, lambda: btn_rhexo.config(text="RHEXO", bg="#1f1f1f", fg="#00e676"))

root = tk.Tk()
root.title("RHEXO OPTIMIZER")
root.geometry("200x90")
root.configure(bg="#121212")

root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0.95)

def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

header = tk.Frame(root, bg="#0d0d0d", height=22)
header.pack(fill="x", side="top")

lbl_title = tk.Label(header, text=" RHEXO OPTIMIZER", fg="#888888", bg="#0d0d0d", font=("Segoe UI", 8, "bold"))
lbl_title.pack(side="left", padx=2)

btn_close = tk.Button(header, text="✕", fg="#ffffff", bg="#0d0d0d", bd=0, activebackground="#e74c3c", command=root.destroy, width=3)
btn_close.pack(side="right")

header.bind("<Button-1>", start_move)
header.bind("<B1-Motion>", do_move)
lbl_title.bind("<Button-1>", start_move)
lbl_title.bind("<B1-Motion>", do_move)

btn_rhexo = tk.Button(
    root, 
    text="RHEXO", 
    font=("Impact", 18), 
    fg="#00e676", 
    bg="#1f1f1f", 
    activeforeground="#ffffff", 
    activebackground="#2a2a2a", 
    bd=1, 
    relief="solid", 
    cursor="hand2", 
    command=optimize_ram
)
btn_rhexo.pack(expand=True, fill="both", padx=8, pady=(4, 8))

root.mainloop()