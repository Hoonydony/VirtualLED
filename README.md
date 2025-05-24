This virtual LED demo visualizes the real-time signal status of a virtual I/O register on an Arm Cortex-A53(AArch64, virt) using QEMU and GDB.
It reads signal values from the emulated hardware registers and displays them as a graph and the LED indicator shows the LED's status through turning on a red light when it receives ON signal.
The system continuously fetches data via GDB remote debugging for live monitoring as per your system performance, while the signal fluctuates between 0 and 1 repeatedly on the virtual device.
This provides an interactive way to observe and analyze the signal behavior of the I/O register, memory-mapped at 0x40010000, during emulation.

![image](https://github.com/user-attachments/assets/f7bbfc3c-9ba0-469d-b7a7-e8a75eb2fe53)


How to run the demo:
1. compile the source: aarch64-none-elf-gcc -g -nostdlib -T linker.ld -march=armv8-a -mcpu=cortex-a53 main.c -o main.elf
2. run the executeable: qemu-system-aarch64 -M virt -cpu cortex-a53 -m 256M -kernel main.elf -nographic -s -S
3. run the python application on the another terminal: python3 app.py

You need 
- the aarch64 cross-compiler to build the code.
- QEMU (qemu-system-aarch64) to run the ARM virtual machine.
- Python 3 with matplotlib and pexpect libraries.

Notes:
It works best on macOS and Linux.
The python app connects to the virtual device through the remote GDB port(localhost:1234) that should be available.
   

When it receives ON signal(==1), the LED indicator becomes red and the graph rises to ON.
![Screenshot 2025-05-24 at 21 15 04](https://github.com/user-attachments/assets/eb17fbf4-89ec-4a54-92d4-8dbb17feef10)

When it receives OFF signal(==0), the LED indicator becomes grey and the graph stays at OFF.
![Screenshot 2025-05-24 at 21 15 33](https://github.com/user-attachments/assets/af77149b-9905-47c1-8cd1-af30b33a3b8c)


