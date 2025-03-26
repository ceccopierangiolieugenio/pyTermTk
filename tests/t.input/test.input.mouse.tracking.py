import sys
import tty
import termios

def enable_mouse_tracking():
    # Enable SGR mouse mode (1006) and extended mouse mode (1015)
    sys.stdout.write("\033[?1003h\033[?1015h\033[?1006h")
    sys.stdout.flush()

def disable_mouse_tracking():
    sys.stdout.write("\033[?1003l\033[?1015l\033[?1006l")
    sys.stdout.flush()

def read_mouse_events():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        event = ""
        while True:
            event += sys.stdin.read(1)
            if event[-1]=='\033':
                mouse_event = event[:-1].replace('\033','<ESC>')
                print(f"Mouse event: {mouse_event}")
                event = '\033'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        disable_mouse_tracking()

if __name__ == "__main__":
    enable_mouse_tracking()
    try:
        read_mouse_events()
    except KeyboardInterrupt:
        disable_mouse_tracking()
        print("\nMouse tracking disabled.")