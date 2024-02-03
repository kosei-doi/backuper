import tkinter
from tkinter import *
from tkinter import ttk
import os 
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os 
import time 

def writeToLog(msg): 
    numlines = int(log.index('end - 1 line').split('.')[0]) 
    log['state'] = 'normal' 
    #if numlines==24: 
    # #log.delete(1.0, 2.0) 
    if log.index('end-1c')!='1.0': 
        log.insert('1.0', '\n') 
    log.insert('1.0', msg) 
    log['state'] = 'disabled' 
    

class MyHandler(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update = []
    
    def on_modified(self, event):
        path = event.src_path.split('\\')[2]
        writeToLog(f"{path} updated")
        self.update.append(path)

    def on_created(self, event):
        cmd = event.src_path
        if(len(cmd.split('\\')) == 3):
            writeToLog("created remote dir")
            dir_name = event.src_path.split('\\')[2]
            os.system(f"gh repo create {dir_name} --private")
            os.chdir("D:\\codes\\"+dir_name)
            os.system(f"echo {dir_name} > README.md")
            os.system("git init")
            os.system("git add .")
            os.system('git commit -m "auto-commit"')
            os.system("git branch -M main")
            os.system(f"git remote add origin https://github.com/kosei-doi/{dir_name}.git")
            os.system("git push -u origin main")
        else:
            path = event.src_path.split('\\')[2]
            writeToLog(f"{path} updated")
            self.update.append(path)
            

    def on_deleted(self, event):
        path = event.src_path.split('\\')[2]
        writeToLog(f"{path} updated")
        self.update.append(path)
        

    def on_moved(self, event):
        path = event.src_path.split('\\')[2]
        writeToLog(f"{path} updated")
        self.update.append(path)
      




if __name__ == '__main__': 
    

    # ウィンドウを作成 
    root = tkinter.Tk() 
    root.title("BACKUPER")
    # アプリの名前 
    root.geometry("200x200") # アプリの画面サイズ
     # Frame1の作成
    frame1 = ttk.Frame(root, padding=10)
    
   
    log = Text(root, state='disabled',borderwidth=5, width=20, height=10, wrap='none', padx=10,pady=10) 
    ys = ttk.Scrollbar(root, orient = 'vertical', command = log.yview) 
    log['yscrollcommand'] = ys.set 
    log.insert('end', "Lorem ipsum...\n...\n...") 
    log.grid(row=1, column=0) 
    ys.grid(column = 1, row = 1, sticky = 'ns')
    frame1.grid()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, "D:\codes", recursive=True)
    observer.start()
    
    def update():
        elems = event_handler.update
        event_handler.update = []
        elems = list(set(elems))
        result = ', '.join(elems)
        writeToLog(result+"\nwill be updated")
        for elem in elems:
            os.chdir("D:\\codes\\"+elem)
            os.system("git add .")
            os.system('git commit -m "auto-commit"')
            os.system("git push -u origin main")

    def sleep():
        elems = event_handler.update
        event_handler.update = []
        elems = list(set(elems))
        result = ', '.join(elems)
        writeToLog(result+"\nwill be updated")
        for elem in elems:
            os.chdir("D:\\codes\\"+elem)
            os.system("git add .")
            os.system('git commit -m "auto-commit"')
            os.system("git push -u origin main")
        
        time.sleep(2)
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        
    
    
    refer_button = ttk.Button(frame1, text=u'UPDATE', command=update) 
    refer_button.grid(row=3, column=0)
    
    refer_button = ttk.Button(frame1, text=u'SLEEP', command=sleep) 
    refer_button.grid(row=3, column=2)
    # ウィンドウを動かす
    root.mainloop()
    
    # observer.join()
    