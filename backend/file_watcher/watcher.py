import time
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pipelines import unstructured_v2

class UploadHandler(FileSystemEventHandler):
    def __init__(self, loop, tags):
        self.loop = loop
        self.tags = tags

    def on_created(self, event):
        if not event.is_directory:
            print(f" New file detected: {event.src_path}")
            # We use the event loop to run the async pipeline from a sync thread
            asyncio.run_coroutine_threadsafe(
                unstructured_v2.run_pipeline(event.src_path, self.tags), 
                self.loop
            )

async def start_watching(path_to_watch: str):
    """Initializes the observer to monitor the directory."""
    # For automation, we can define a default set of tags to extract
    default_tags = ["name", "email", "total_amount"] 
    
    loop = asyncio.get_running_loop()
    event_handler = UploadHandler(loop, default_tags)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    
    print(f" Folder Watcher started on: {path_to_watch}")
    observer.start()
    try:
        while True:
            await asyncio.sleep(1) # Keep the coroutine alive
    except Exception as e:
        observer.stop()
        print(f"Watcher stopped: {e}")
    observer.join()