# example.py
import debugpy

# Start the debug server
debugpy.listen(("localhost", 64321))
print("Waiting for debugger to attach...")
debugpy.wait_for_client()
print("Attached!!!")

def add(a, b):
    return a + b

def main():
    x = 10
    y = 20
    result = add(x, y)
    print(f"The result is {result}")

if __name__ == "__main__":
    main()
