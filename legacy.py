import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os 
import schedule

class MyHandler(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logs = []
        self.update = []
    
    def on_modified(self, event):
        print("update")
        self.update.append(event.src_path.split('\\')[2])

    def on_created(self, event):
        cmd = event.src_path
        if(len(cmd.split('\\')) == 3):
            print("create remote dir")
            dir_name = event.src_path.split('\\')[2]
            os.system(f"gh repo create {dir_name} --private")
        else:
            print("update")
            self.update.append(event.src_path.split('\\')[2])
            

    def on_deleted(self, event):
        print("update")
        self.update.append(event.src_path.split('\\')[2])
        

    def on_moved(self, event):
        print("update")
        self.update.append(event.src_path.split('\\')[2])
      

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, "D:\codes", recursive=True)
    observer.start()
   
    def update():
        elem = event_handler.update
        elem = list(set(elem))
        print(elem)
  
    schedule.every(10).seconds.do(update)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

