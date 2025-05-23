This virtual LED demo visualizes the real-time signal status of a virtual GPIO on an Arm Cortex-A53(virt) using QEMU and GDB.
It reads signal values from the emulated hardware registers and displays them as a graph and the LED indicator shows the LED's status through turning on a red light when it receives ON signal.
The system continuously fetches data via GDB remote debugging for live monitoring as per your system performance, while the signal fluctuates repeatedly on the virtual device.
This provides an interactive way to observe and analyze GPIO signal behavior during emulation.

How to run the demo:
1. compile the source: aarch64-none-elf-gcc -g -nostdlib -T linker.ld -march=armv8-a -mcpu=cortex-a53 main.c -o main.elf
2. run the executeable: qemu-system-aarch64 -M virt -cpu cortex-a53 -m 256M -kernel main.elf -nographic -s -S
3. run the python application on the another terminal: python3 app.py

You need 
- the aarch64 cross-compiler to build the code.
- QEMU (qemu-system-aarch64) to run the ARM virtual machine.
- Python 3 with matplotlib and pexpect libraries.

Notes:
Works best on macOS and Linux.
The python app connects to the virtual device through the remote GDB port(localhost:1234) that should be available.
   

When it receives ON signal(==1), the LED indicator becomes red and the graph rises to ON.
![Screenshot 2025-05-23 at 23 16 19](https://github.com/user-attachments/assets/e33aa1cd-8e7c-450c-8812-05ef92efd8b3)

When it receives OFF signal(==0), the LED indicator becomes grey and the graph stays at OFF.
![Screenshot 2025-05-23 at 23 09 22](https://github.com/user-attachments/assets/083a7ace-169a-417b-877d-3aa61f389564)
