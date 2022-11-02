import os

with open('test.txt', 'wb') as f:
    f.write("!!!!!!!!!!@@@@@@@@@@##########$$$$$$$$$$%%%%%%".encode())
    f.write((1).to_bytes(4, 'big', signed=True))

print(os.path.getsize("./test.txt"))
