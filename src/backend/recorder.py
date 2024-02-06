from pynput import keyboard, mouse

def on_press(key):
    try:
        print(f'Alphanumeric key pressed: {key.char}')
    except AttributeError:
        print(f'Special key pressed: {key}')

def on_release(key):
    print(f'Key released: {key}')
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def on_click(x, y, button, pressed):
    if pressed:
        print(f'Mouse clicked at ({x}, {y}) with {button}')

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()