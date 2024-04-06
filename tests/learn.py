import sys

# Writing to sys.stdout
# ok = sys.stdout.write("Hello, world!\n")
# print(ok)
#
#
# Redirecting sys.stdout to a file
with open("output.txt", "w") as f:
    sys.stdout = f
    print("This will be written to output.txt")
    print("everything over here would be written to file")
    # Remember to restore sys.stdout to its original value
    sys.stdout = sys.__stdout__

print('ov')



