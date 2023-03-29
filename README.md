# EOLRemover
This code is a Python script that removes End of Line (EOL) characters from the text in the clipboard. It provides a simple Graphical User Interface (GUI) that allows the user to enable or disable the EOL remover.

# How it works
The script uses the pyperclip library to access the clipboard content. The EOL remover function runs in a separate thread, which listens for changes in the clipboard content. Whenever new text is copied to the clipboard, the function removes any EOL characters from the text and updates the clipboard with the modified text.

The GUI provides two buttons to enable or disable the EOL remover. When the "ACTIVATE" button is clicked, a new thread is created to run the EOL remover function. When the "DEACTIVATE" button is clicked, the thread is stopped by setting a stop flag, and the GUI is updated to reflect that the EOL remover is deactivated.

Alternatively, you can also use the keyboard shortcut "alt_gr" to toggle between activating and deactivating the EOL remover.
