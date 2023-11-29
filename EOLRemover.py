import pyperclip
import tkinter as tk
import threading
import time
import keyboard

# This function is the actual EOL character remover and it is run by a separated thread.
# It takes as argument the stop flag, used to know whenever to continue looping or not
# The idea is pretty simple, copy the last saved element in clipboard, check if the saved element contains text,
# remove EOL characters, check if it's a new content or not, if it's new then just remove EOL characters 
# and paste it on the clipboard. loop until the stop flag is set -> aka the thread has been killed by the disable_eol_remover function.
def eol_remover(stop_flag):
    global last_copied
    print("EOLRemover started")
    while not stop_flag.is_set():
        #print("running")
        current_copied = pyperclip.paste()
        if str(current_copied) != '': # do nothing if content copied to clipboard is not a text
            
            current_copied = current_copied.replace("\r", "").replace("\n", " ")
            if current_copied != last_copied:
                last_copied = current_copied

                modified_last = last_copied.replace("\r", "").replace("\n", " ")
                last_copied = modified_last

                pyperclip.copy(last_copied)
        time.sleep(0.1)
    print("EOLRemover stopped")


# This function creates and starts a new thread to remove EOL characters from the clipboard text
# It first checks if a thread is already running, and if not, creates a new thread and clears the stop flag
# The stop flag is used to control the loop in the separate thread that listens for clipboard changes
# The thread is started as a daemon thread so it will terminate when the main program exits
# The function also updates the status label in the GUI to indicate that the EOL remover is activated
def enable_eol_remover():
    global thread
    global thread_stop_flag
    global enable
    
    if not thread.is_alive():
        thread = threading.Thread(target=eol_remover, args=(thread_stop_flag,), daemon=True)
        thread_stop_flag.clear()
        thread.start()
        label2.config(text="ACTIVATED", fg='#31b710', font=("TkDefaultFont", 12, "bold"))
        if not enable:
            enable = True

# This function stops the EOL remover by setting the stop flag in the thread and waiting for it to finish
# It first checks if a thread is running, and if so, sets the stop flag to terminate the loop in the separate thread
# It then creates a new thread to wait for the EOL remover thread to finish and joins it
# The function also updates the status label in the GUI to indicate that the EOL remover is deactivated
# The original thread is not stopped directly, as this could cause the program to hang or crash
def disable_eol_remover():
    global thread
    global thread_stop_flag
    global last_copied
    global enable
 
    if thread != None:
        if thread.is_alive():
            last_copied = None
            thread_stop_flag.set()
            jointhread = threading.Thread(target=thread.join, daemon=True)
            jointhread.start()
            label2.config(text="DEACTIVATED", fg='#bf1715', font=("TkDefaultFont", 12, "bold"))
            if enable:
                enable = False

def switch_activation():
    global enable

    if enable:
        disable_eol_remover()
    else:
        enable_eol_remover()


thread_stop_flag = threading.Event()
thread_stop_flag.set()
thread = threading.Thread(target=eol_remover, args=(thread_stop_flag,), daemon=True)
jointhread = None
last_copied = None
enable = False

keyboard.add_hotkey("alt_gr", switch_activation)

# Simple main, it creates the GUI with tkinter
if __name__ == '__main__':
    window = tk.Tk()
    window.title("EOLRemover")
    window.geometry("300x120")
    window.resizable(False, False)

    # Create a frame to hold the labels and center it
    label_frame = tk.Frame(window)
    label_frame.pack()
    label_frame.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    # Create the first label widget and center it
    label1 = tk.Label(label_frame, text="Status: ")
    label1.pack(side=tk.LEFT)

    # Create the second label widget and add it to the label frame
    label2 = tk.Label(label_frame, text="DEACTIVATED", fg='#bf1715', font=("TkDefaultFont", 12, "bold"))
    label2.pack(side=tk.LEFT, padx=10)

    # Create a frame to hold the buttons and center it
    button_frame = tk.Frame(window)
    button_frame.pack()
    button_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    # Create a button widget and add it to the button frame
    button1 = tk.Button(button_frame, text="ACTIVATE", command=enable_eol_remover)
    button1.pack(side=tk.LEFT, padx=10)

    # Create another button widget and add it to the button frame
    button2 = tk.Button(button_frame, text="DEACTIVATE", command=disable_eol_remover)
    button2.pack(side=tk.LEFT, padx=10)

    # Run the event loop
    window.mainloop()
