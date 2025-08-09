import pyperclip
import tkinter as tk
import threading
import time
import keyboard
import re

def fix_accented_characters(text):
    """Convert backtick+vowel patterns to accented characters"""
    original = text
    
    # Dictionary mapping vowels to their grave accent versions
    accent_map = {
        'a': 'à', 'e': 'è', 'i': 'ì', 'o': 'ò', 'u': 'ù',
        'A': 'À', 'E': 'È', 'I': 'Ì', 'O': 'Ò', 'U': 'Ù'
    }
    
    # Use regex to find backtick followed by vowel and replace
    def replace_accent(match):
        vowel = match.group(1)
        return accent_map.get(vowel, match.group(0))
    
    # Pattern: backtick followed by any vowel
    pattern = r'`([aeiouAEIOU])'
    matches = re.findall(pattern, text)
    result = re.sub(pattern, replace_accent, text)
    
    if result != original and matches:
        print(f"Fixed {len(matches)} wrong characters")
    
    return result

# This function removes EOL characters and fixes accented characters from clipboard text
def eol_remover(stop_flag):
    global last_copied
    print("EOLRemover started")
    while not stop_flag.is_set():
        current_copied = pyperclip.paste()
        if str(current_copied) != '': # do nothing if content copied to clipboard is not a text
            
            # Remove line breaks
            cleaned_text = current_copied.replace("\r", "").replace("\n", " ")
            
            # Fix accented characters (backtick + vowel -> accented vowel)
            cleaned_text = fix_accented_characters(cleaned_text)
            
            if cleaned_text != last_copied:
                last_copied = cleaned_text
                pyperclip.copy(last_copied)
        time.sleep(0.1)
    print("EOLRemover stopped")

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
    window.title("EOL & Accent Fixer")
    window.geometry("320x150")
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
    button_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    
    # Create a button widget and add it to the button frame
    button1 = tk.Button(button_frame, text="ACTIVATE", command=enable_eol_remover)
    button1.pack(side=tk.LEFT, padx=10)
    
    # Create another button widget and add it to the button frame
    button2 = tk.Button(button_frame, text="DEACTIVATE", command=disable_eol_remover)
    button2.pack(side=tk.LEFT, padx=10)
    
    # Run the event loop
    window.mainloop()