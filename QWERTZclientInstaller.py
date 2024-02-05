import os,json,time,wget
from datetime import datetime
import tkinter as tk
from io import BytesIO
import minecraft_launcher_lib
from PIL import Image, ImageTk
import requests
import tempfile,sys
from tkinter import ttk, PhotoImage
from tkinter import filedialog
from zipfile import ZipFile
from tkinter import DISABLED,NORMAL
from tkinter import ttk,font,messagebox
from ttkbootstrap import Style
def get_latest_version(project_id):
    response = requests.get(f'https://api.modrinth.com/api/v1/mod/{project_id}/version')
    versions = json.loads(response.text)
    latest_version = versions[0]  # Assuming the first version in the list is the latest
    return latest_version['files'][0]['url']  # Assuming the first file is the one you want


def download_file_with_progress(url, save_path, progress_bar, root):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    total_downloaded = 0  # Initialize the total downloaded variable
    with open(save_path, 'wb') as file:
        for data in response.iter_content(block_size):
            file.write(data)
            total_downloaded += len(data)  # Update the running total of bytes downloaded
            progress = (total_downloaded / total_size) * 100
            progress_bar['value'] = progress
            root.update_idletasks()  # Update the GUI to reflect the progress
            
if os.name=="nt":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)





def startinstall():
    global button2, label3, label4,label2
    root.geometry("1000x600")
    button.destroy()
    style = ttk.Style()
    style.configure("Red.TLabel", foreground="red")
    label["text"] = "QWERTZclient 1/6"
    label2 = ttk.Label(root, text="Welcome to the QWERTZclient installer!", style='info.TLabel',font=("Courier", 20))
    label2.pack(pady=10)
    label3 = ttk.Label(root, text="Install QWERTZclient in just a few clicks!", style='white',font=("Consolas", 15))
    label3.pack(pady=10)
    label4 = ttk.Label(root, text="NEXT: Create QWERTZclient folder", style='style2',font=("Consolas", 12))
    label4.pack(pady=10)
    label4.configure(style="Red.TLabel")
    button2 = ttk.Button(root, text="NEXT")
    button2.config(command=createfolder)
    button2.pack(pady=10)

def createfolder():
    global path2,text_var,entry,label4,browse_button
    def change_width(*args):
        entry.config(width=len(text_var.get()))  # Adding some extra space
    global label4, button2,s
    s3 = ttk.Style()
    fontb = font.Font(root , family = 'Ubuntu',  size = 30 , weight = font.BOLD)
    s3.configure('TButton2.TButton',font=fontb)
    label["text"] = "QWERTZclient 2/6"
    label2.destroy()
    label3["text"] = "Please specify the QWERTZclient path"
    label3.pack(pady=10)

    text_var = tk.StringVar()
    text_var.trace("w", change_width)
    entry = ttk.Entry(root, width=50,textvariable=text_var, justify="center")
    a=os.getenv('APPDATA').replace("\\","/")
    entry.insert(0,f"{a}/.minecraft/QWERTZclient")
    entry.pack(pady=10)

    s.configure('TButton2.TButton', font=('Arial', 15))
    def browse_file():
        dirname = filedialog.askdirectory(initialdir=f"{os.getenv('APPDATA')}/.minecraft", title="Select a Folder")
        entry.delete(0, tk.END)  # Clear the entry widget
        entry.insert(0, dirname)  # Insert the selected file path
    browse_button = ttk.Button(root, text="BROWSE", command=browse_file)
    browse_button.configure(style="TButton2.TButton")
    browse_button.pack(pady=10)
    
    label4["text"]="NEXT: Download Vanilla 1.8.9"
    label4.pack_forget()
    label4.pack(pady=10)
    button2.config(command=validatepath)
    button2.pack_forget()
    button2.pack(pady=10)
def is_valid_directory_path(path):
    if os.path.isabs(path):  # Check if it's an absolute path
        if not os.path.exists(path):  # Check if the path exists
            return True,True  # It's a valid directory path that doesn't exist
        else:
            return True,False
    return False,1  # It's not a valid directory path
def validatepath():
    global clientdir,text_var
    clientdir = text_var.get()
    if is_valid_directory_path(clientdir)[0]:
        os.makedirs(clientdir,exist_ok=True)
        downloadvanilla()
    else:
        messagebox.showerror("NOT A VALID DIRECTORY!",f"The path you specified is not a valid directory path!")
def downloadvanilla():
    global path2,text_var,download_button,label2
    global label4, button2,s
    s3 = ttk.Style()
    fontb = font.Font(root , family = 'Ubuntu',  size = 30 , weight = font.BOLD)
    s3.configure('TButton2.TButton',font=fontb)
    label["text"] = "QWERTZclient 3/6"
    label3["text"] = "Please download Vanilla 1.8.9"
    label3.pack(pady=10)
    entry.destroy()
    download_button = ttk.Button(root, text="DOWNLOAD", command=downloadvanillanow)
    download_button.configure(style="TButton2.TButton")
    download_button.pack(pady=10)
    browse_button.pack_forget()
    label4["text"]="NEXT: Download Java"
    label4.pack_forget()
    label4.pack(pady=30)
    label2 = ttk.Label(root, text="NOTE: since 1.8.9 is already installed you can skip this step!", style='info.TLabel',font=("Courier", 10))
    if os.path.exists(f"{os.getenv('APPDATA')}/.minecraft/versions/1.8.9/1.8.9.jar"):
        label2.pack(pady=10)
    button2.config(command=downloadjava)
    button2["style"] = "TButtonDisabled.TButton"
    button2.pack_forget()
    button2.pack(pady=10)
    button2.config(state=DISABLED)
    if os.path.exists(f"{os.getenv('APPDATA')}/.minecraft/versions/1.8.9/1.8.9.jar"):
        button2.config(state=NORMAL)
        download_button.config(state=DISABLED)
def downloadjava():
    global path2,text_var,download_button,label2
    global label4, button2,s
    s3 = ttk.Style()
    fontb = font.Font(root , family = 'Ubuntu',  size = 30 , weight = font.BOLD)
    s3.configure('TButton2.TButton',font=fontb)
    label["text"] = "QWERTZclient 4/6"
    label3["text"] = "Please download QWERTZclient's Java"
    label3.pack(pady=10)
    entry.destroy()
    download_button.destroy()
    download_button = ttk.Button(root, text="DOWNLOAD", command=downloadjavanow)
    download_button.configure(style="TButton2.TButton")
    download_button.pack(pady=10)
    browse_button.pack_forget()
    label4["text"]="NEXT: Download QWERTZclient"
    label4.pack_forget()
    label4.pack(pady=30)
    label2.pack_forget()
    label2 = ttk.Label(root, text="NOTE: since QWERTZ client's java is already installed you can skip this step!", style='info.TLabel',font=("Courier", 10))
    if os.path.exists(f"{clientdir}/java/bin/javaw.exe"):
        label2.pack(pady=10)

    button2.config(command=downloadforge)
    button2["style"] = "TButtonDisabled.TButton"
    button2.pack_forget()
    button2.pack(pady=10)
    button2.config(state=DISABLED)
    if os.path.exists(f"{clientdir}/java/bin/javaw.exe"):
        button2.config(state=NORMAL)
        download_button.config(state=DISABLED)
def downloadforge():
    global path2,text_var,download_button,label2
    global label4, button2,s
    s3 = ttk.Style()
    fontb = font.Font(root , family = 'Ubuntu',  size = 30 , weight = font.BOLD)
    s3.configure('TButton2.TButton',font=fontb)
    label["text"] = "QWERTZclient 5/6"
    label3["text"] = "Please download QWERTZclient"
    label3.pack(pady=10)
    entry.destroy()
    download_button.destroy()
    download_button = ttk.Button(root, text="DOWNLOAD", command=downloadforgenow)
    download_button.configure(style="TButton2.TButton")
    download_button.pack(pady=10)
    browse_button.pack_forget()
    label4["text"]="NEXT: Java Arguments"
    label4.pack_forget()
    label4.pack(pady=30)
    label2.pack_forget()
    label2 = ttk.Label(root, text="NOTE: since QWERTZclient is already installed you can skip this step!", style='info.TLabel',font=("Courier", 10))
    if os.path.exists(f"{os.getenv('APPDATA')}/.minecraft/versions/1.8.9-qwertzclient-1.0/1.8.9-qwertzclient-1.0.jar"):
        label2.pack(pady=10)

    button2.config(command=setjavaargs)
    button2["style"] = "TButtonDisabled.TButton"
    button2.pack_forget()
    button2.pack(pady=10)
    button2.config(state=DISABLED)
    if os.path.exists(f"{os.getenv('APPDATA')}/.minecraft/versions/1.8.9-qwertzclient-1.0/1.8.9-qwertzclient-1.0.jar"):
        button2.config(state=NORMAL)
        download_button.config(state=DISABLED)
def setjavaargs():
    global javaargs
    global path2,text_var,download_button,label2,java_args_label
    global label4, button2,s,java_args_entry
    def change_width(*args):
        java_args_entry.config(width=len(text_var.get()))  # Adding some extra space
    s3 = ttk.Style()
    fontb = font.Font(root , family = 'Ubuntu',  size = 30 , weight = font.BOLD)
    s3.configure('TButton2.TButton',font=fontb)
    label["text"] = "QWERTZclient 6/6"
    label3["text"] = "Please set your Java args"
    label3.pack(pady=10)
    download_button.destroy()
    browse_button.pack_forget()
    java_args_label = ttk.Label(root, text="Java Arguments:")
    java_args_label.pack(pady=10)
    text_var = tk.StringVar()
    text_var.trace("w", change_width)
    java_args_entry = ttk.Entry(root, width=50,textvariable=text_var, justify="center")
    ram = 4
    java_args_entry.insert(0,f"-Xmx{ram}G -Ddg.safe=true -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M")
    java_args_entry.pack(pady=10)
    label4["text"]="NEXT: Inject Launcher Profile"
    label4.pack_forget()
    label4.pack(pady=30)
    label2.pack_forget()
    button2.config(command=injectprofile)
    button2["style"] = "TButtonDisabled.TButton"
    button2.pack_forget()
    button2.pack(pady=10)
    button2.config(state=NORMAL)
def injectprofile():
    global javaargs,java_args_entry
    javaargs = java_args_entry.get()
    path = f"{os.getenv('APPDATA')}/.minecraft/launcher_profiles.json"
    datern = datetime.now()
    rightnow = datern.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    dicti = {
        "created" : rightnow,
        "gameDir" : clientdir,
        "icon" : "Lectern_Book",
        "lastUsed" : rightnow,
        "javaArgs": javaargs,
        "javaDir" : f"{clientdir}/java/bin/javaw.exe",
        "lastVersionId" : "1.8.9-qwertzclient-1.0",
        "name" : "QWERTZclient",
        "type" : "custom"
        }
    with open(path,"r") as f:
        a = json.load(f)
    a["profiles"]["qwertzclient"] = dicti
    with open(path,"w") as f:
        json.dump(a,f)
    messagebox.showinfo("SUCCESS!","QWERTZclient is successfully injected into the Launcher!\nNEXT: Select Mods")
    tweakclient()
def tweakclient():
    global path2,text_var,download_button,label2,checkboxes,scrollable_frame
    global label4, button2,s,java_args_entry
    global java_args_entry,canvas,scrollbar,frame
    java_args_label.destroy()
    java_args_entry.destroy()
    root.geometry("1000x800")
    s3 = ttk.Style()
    fontb = font.Font(root , family = 'Ubuntu',  size = 30 , weight = font.BOLD)
    s3.configure('TButton2.TButton',font=fontb)
    label["text"] = "QWERTZclient 1/2"
    label3["text"] = "Please select the mods you want to use"
    label3.pack(pady=10)
    download_button.destroy()
    browse_button.pack_forget()
    label4["text"]="NEXT: Select Texturepacks"
    label4.pack_forget()
    label2.pack_forget()
    button2.config(command=tweakclientnow)
    button2.pack_forget()
    button2.config(state=NORMAL)
    mod_urls=requests.get("https://raw.githubusercontent.com/QWERTZexe/QWERTZclient/main/mod_urls.json").json()
    # Create a scrollable frame
    scrollable_frame = ttk.Frame(root)
    scrollable_frame.pack(pady=10)

    canvas = tk.Canvas(scrollable_frame)
    scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    frame = ttk.Frame(canvas)

    frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # For each mod, create a label with an icon and a checkbox
    i=0
    checkboxes = {}
    for mod_name, mod_url in mod_urls.items():
        # Download the latest release
        # This is a simplified example, you may need to modify it based on the actual URL of the latest release

        # Save the mod file

        # Create an icon
        # This is a placeholder, replace 'icon_url' with the actual URL of the icon
        response = requests.get(mod_url[1])
        img_data = response.content
        img = PhotoImage(data=img_data)
        img = img.subsample(8, 8) 
        # Create a label with the icon
        label6 = ttk.Label(frame, image=img)
        label6.image = img  # Keep a reference to the image to prevent it from being garbage collected
        label6.grid(row=i, column=0, padx=10)
    
        # Create a checkbox
        checkbox_var = tk.BooleanVar(value=True)
        s3.configure("TCheckbutton",font=("Courier", 14))
        checkbox = ttk.Checkbutton(frame, text=mod_name, variable=checkbox_var)
        checkbox.grid(row=i, column=1, padx=10)
        i+=1
        checkboxes[mod_name] = {}
        checkboxes[mod_name]["var"] = checkbox_var
        checkboxes[mod_name]["url"] = mod_url
        checkboxes[mod_name]["checkbox"] = checkbox
        checkboxes[mod_name]["label"] = label6

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    label4.pack(pady=30)
    button2.pack(pady=10)
    
def tweakclientnow():
    os.makedirs(f"{clientdir}/mods",exist_ok=True)
    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
    label4.pack_forget()
    button2.pack_forget()
    progress_bar.pack(pady=10)
    a=0
    for key in list(checkboxes.keys()):
        if checkboxes[key]["var"].get() == True:
            a+=1
            url=checkboxes[key]["url"][0]
            if url.startswith("https://api.github.com"):
                url = f"{url}/releases/latest"
                response = requests.get(url)
                data = response.json()
                # Extract the download URL for the JAR file from the API response
                try:
                    jar_download_url = data['assets'][0]['browser_download_url']
                    filename = jar_download_url.split("/")[-1]
                    if os.path.exists(f"{clientdir}/mods/{filename}"):
                        os.remove(f"{clientdir}/mods/{filename}") # if exist, remove it directly
                    wget.download(jar_download_url, f"{clientdir}/mods/{filename}")
                    progress = (a / len(list(checkboxes.keys()))) * 100
                    progress_bar['value'] = progress
                except:
                    pass
                root.update_idletasks()  # Update the GUI to reflect the progress
            else:
                try:
                    jar_download_url = url
                    filename = jar_download_url.split("/")[-1]
                    if os.path.exists(f"{clientdir}/mods/{filename}"):
                        os.remove(f"{clientdir}/mods/{filename}") # if exist, remove it directly
                    wget.download(jar_download_url, f"{clientdir}/mods/{filename}")
                    progress = (a / len(list(checkboxes.keys()))) * 100
                    progress_bar['value'] = progress
                except:
                    pass
                root.update_idletasks()  # Update the GUI to reflect the progress
    time.sleep(0.2)
    progress_bar.destroy()
    label4.pack(pady=30)
    button2.pack(pady=10)
    tweaktexturepack()
def tweaktexturepack():
    global path2,text_var,download_button,label2,checkboxes,scrollable_frame
    global label4, button2,s,java_args_entry
    global java_args_entry,canvas,scrollbar,frame
    canvas.destroy()
    scrollbar.destroy()
    scrollable_frame.destroy()
    frame.destroy()
    for checkbox in checkboxes.values():
        checkbox["checkbox"].destroy()
        checkbox["label"].destroy()
    s3 = ttk.Style()
    fontb = font.Font(root , family = 'Ubuntu',  size = 30 , weight = font.BOLD)
    s3.configure('TButton2.TButton',font=fontb)
    label["text"] = "QWERTZclient 2/2"
    label3["text"] = "Please select the texturepacks you want to use"
    label3.pack(pady=10)
    label4["text"]="NEXT: Finishing up"
    label4.pack_forget()
    label2.pack_forget()
    button2.config(command=tweaktexturepacknow)
    button2.pack_forget()
    button2.config(state=NORMAL)
    tp_urls=requests.get("https://raw.githubusercontent.com/QWERTZexe/QWERTZclient/main/texturepack_urls.json").json()
    # Create a scrollable frame
    scrollable_frame = ttk.Frame(root)
    scrollable_frame.pack(pady=10)

    canvas = tk.Canvas(scrollable_frame)
    scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    frame = ttk.Frame(canvas)

    frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # For each mod, create a label with an icon and a checkbox
    i=0
    checkboxes = {}
    for tp_name, tp_url in tp_urls.items():
        # Download the latest release
        # This is a simplified example, you may need to modify it based on the actual URL of the latest release

        # Save the mod file

        # Create an icon
        # This is a placeholder, replace 'icon_url' with the actual URL of the icon
        response = requests.get(tp_url[1])
        img_data = response.content
        img = PhotoImage(data=img_data)
        img = img.subsample(8, 8) 
        # Create a label with the icon
        label6 = ttk.Label(frame, image=img)
        label6.image = img  # Keep a reference to the image to prevent it from being garbage collected
        label6.grid(row=i, column=0, padx=10)
    
        # Create a checkbox
        checkbox_var = tk.BooleanVar(value=True)
        s3.configure("TCheckbutton",font=("Courier", 14))
        checkbox = ttk.Checkbutton(frame, text=tp_name, variable=checkbox_var)
        checkbox.grid(row=i, column=1, padx=10)
        i+=1
        checkboxes[tp_name] = {}
        checkboxes[tp_name]["var"] = checkbox_var
        checkboxes[tp_name]["url"] = tp_url
        checkboxes[tp_name]["checkbox"] = checkbox
        checkboxes[tp_name]["label"] = label6
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    label4.pack(pady=30)
    button2.pack(pady=10)
def tweaktexturepacknow():
    os.makedirs(f"{clientdir}/resourcepacks",exist_ok=True)
    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
    label4.pack_forget()
    button2.pack_forget()
    progress_bar.pack(pady=10)
    a=0
    for key in list(checkboxes.keys()):
        if checkboxes[key]["var"].get() == True:
            a+=1
            url=checkboxes[key]["url"][0]
            url = f"{url}/releases/latest"
            response = requests.get(url)
            data = response.json()
            try:
                zip_download_url = data['assets'][0]['browser_download_url']
                filename = zip_download_url.split("/")[-1]
                if os.path.exists(f"{clientdir}/resourcepacks/{filename}"):
                    os.remove(f"{clientdir}/resourcepacks/{filename}") # if exist, remove it directly
                wget.download(zip_download_url, f"{clientdir}/resourcepacks/{filename}")
                progress = (a / len(list(checkboxes.keys()))) * 100
                progress_bar['value'] = progress
            except:
                pass
            root.update_idletasks()  # Update the GUI to reflect the progress
        
    time.sleep(0.2)
    progress_bar.destroy()
    label4.pack(pady=30)
    button2.pack(pady=10)
    finishup()
def downloadforgenow():
    global progress_bar
    label4.pack_forget()
    button2.pack_forget()
    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
    progress_bar.pack(pady=10)
    pathh = tempfile.mktemp()
    download_file_with_progress("https://raw.githubusercontent.com/QWERTZexe/QWERTZclient/main/qwertzclient.zip",pathh,progress_bar,root)
    extract_zip_with_progress(pathh,f"{os.getenv('APPDATA')}/.minecraft",progress_bar)
    progress_bar.destroy()
    label4.pack(pady=5)
    button2.pack(pady=10)
    if os.path.exists(f"{os.getenv('APPDATA')}/.minecraft/versions/1.8.9-qwertzclient-1.0/1.8.9-qwertzclient-1.0.jar"):
        button2.config(state=NORMAL)
        download_button.config(state=DISABLED)
def extract_zip_with_progress(zip_file, extract_folder, progress_bar):
    with ZipFile(zip_file, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        for i, file in enumerate(file_list):
            zip_ref.extract(file, extract_folder)
            progress = (i + 1) * 100 // len(file_list)  # Calculate the progress percentage
            progress_bar['value'] = progress  # Update the progress bar value
            root.update_idletasks()  # Update the GUI to reflect the progress
def downloadjavanow():
    global progress_bar
    label4.pack_forget()
    button2.pack_forget()
    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
    progress_bar.pack(pady=10)
    pathh = tempfile.mktemp()
    download_file_with_progress("https://cdn.glitch.me/d204ee01-249d-4fd8-8b05-bea32f8a9bfa/qwertzclientjava.zip",pathh,progress_bar,root)
    extract_zip_with_progress(pathh,f"{clientdir}/java",progress_bar)
    progress_bar.destroy()
    label4.pack(pady=5)
    button2.pack(pady=10)
    if os.path.exists(f"{clientdir}/java/bin/javaw.exe"):
        button2.config(state=NORMAL)
        download_button.config(state=DISABLED)
def downloadvanillanow():
    global current_max, progress_bar,download_button
    label4.pack_forget()
    button2.pack_forget()
    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
    progress_bar.pack(pady=10)
    time.sleep(0.5)
    def set_status(status: str):
        if status == "Installation complete":
            progress_bar.destroy()
            if os.path.exists(f"{os.getenv('APPDATA')}/.minecraft/versions/1.8.9/1.8.9.jar"):
                button2.config(state=NORMAL)
                download_button.config(state=DISABLED)

    def set_progress(progress: int):
        if current_max != 0:
            progress_bar['value'] = progress
            root.update_idletasks()  # Update the GUI to reflect the progress

    def set_max(new_max: int):
        global current_max
        current_max = new_max
        progress_bar['maximum'] = current_max
    callback = {
        "setStatus": set_status,
        "setProgress": set_progress,
        "setMax": set_max
    }
    root.update_idletasks()  # Update the GUI to reflect the progress
    minecraft_launcher_lib.install.install_minecraft_version("1.8.9", f"{os.getenv('APPDATA')}/.minecraft", callback=callback)
    label4.pack(pady=5)
    button2.pack(pady=10)
def finishup():
    global path2,text_var,download_button,label2,checkboxes,scrollable_frame
    global label4, button2,s,java_args_entry
    global java_args_entry,canvas,scrollbar,frame
    canvas.destroy()
    scrollbar.destroy()
    scrollable_frame.destroy()
    frame.destroy()
    for checkbox in checkboxes.values():
        checkbox["checkbox"].destroy()
        checkbox["label"].destroy()
    root.geometry("1000x500")
    s3 = ttk.Style()
    fontb = font.Font(root , family = 'Ubuntu',  size = 30 , weight = font.BOLD)
    s3.configure('TButton2.TButton',font=fontb)
    label["text"] = "QWERTZclient"
    label3["text"] = "Done!\nYou can now launch QWERTZclient from the Minecraft Launcher!"
    label3.pack(pady=10)
    label4.pack_forget()
    label4.pack_forget()
    label2.pack_forget()
    button2["text"] = "EXIT"
    button2.config(command=sys.exit)
    button2.config(state=NORMAL)
root = tk.Tk()
width = 1000
height = 300
scrwdth = root.winfo_screenwidth()
scrhgt = root.winfo_screenheight()
xLeft = (scrwdth/2) - (width/2)
yTop = (scrhgt/2) - (height/2)-300
root.geometry(str(width) + "x" + str(height) + "+" + str(int(xLeft)) + "+" + str(int(yTop)))
style = Style(theme='vapor')

label = ttk.Label(root, text="QWERTZclient 0/6", style='info.TLabel',font=("Courier", 44))
label.pack(pady=10)
fontz = font.Font(root , family = 'Ubuntu',  size = 30 , weight = font.BOLD)

s = ttk.Style()

s.configure('.', font=fontz)
button = ttk.Button(root, text="INSTALL")
style.map('TButton',
          background=[('active', 'black')],
          foreground=[('active', 'white')])
style.map('TButton',
          foreground=[('disabled', 'gray')])
button.config(command=startinstall)
button.pack(pady=10)

root.mainloop()