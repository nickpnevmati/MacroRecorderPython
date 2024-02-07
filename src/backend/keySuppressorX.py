import pyxhook

# This function is called every time a key is presssed
def kbevent(event):
    # print key info
    print(event)

    # If you want to prevent a particular key from being propagated
    # set event.Ascii to zero. Here we block the "a" key
    if event.Ascii == 97:  # ASCII for 'a'
        # Suppress event
        return False

# Create hookmanager
hookman = pyxhook.HookManager()
# Define our callback to fire when a key is pressed down
hookman.KeyDown = kbevent
# Hook the keyboard
hookman.HookKeyboard()
# Start our listener
hookman.start()

# Keep the program running
input("Press Enter to terminate...\n")

# Close the listener when we are done
hookman.cancel()