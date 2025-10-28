import threading
import traceback

def custom_thread_excepthook(args):
    """
    Args is a named tuple with:
    - exc_type: Exception class
    - exc_value: Exception instance
    - exc_traceback: Traceback object
    - thread: Thread object where exception occurred
    """
    print(f"Thread {args.thread.name} crashed!")
    print(f"Exception: {args.exc_type.__name__}: {args.exc_value}")

    # Print full traceback like default handler
    print("\nFull traceback:")
    traceback.print_exception(args.exc_type, args.exc_value, args.exc_traceback, colorize=True)

    # Or to match default format exactly:
    # ßsys.stderr.write(f"\n\nPIPPO\n\nException in thread {args.thread.name}:\n")
    # traceback.print_exception(args.exc_type, args.exc_value, args.exc_traceback, file=sys.stderr)

# Set custom handler
threading.excepthook = custom_thread_excepthook

# Example thread that will crash
def worker():
    raise ValueError("Something went wrong!")

thread = threading.Thread(name='Pippo', target=worker)
try:
    thread.start()
    thread.join()
except Exception as e:
    print(e)
    print('EUGENIO')
