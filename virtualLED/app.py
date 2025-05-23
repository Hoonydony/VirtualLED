import pexpect
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import os
import sys
import re
import numpy as np

gdb_path = "/Applications/ArmGNUToolchain/14.2.rel1/aarch64-none-elf/bin/aarch64-none-elf-gdb"
gdb_prompt = "(gdb)"

env = os.environ.copy()
env["TERM"] = "dumb"

child = pexpect.spawn(f"{gdb_path} --nx -q main.elf", encoding="utf-8", timeout=15, env=env)
child.logfile = sys.stdout

try:
    child.expect_exact(gdb_prompt)
except pexpect.exceptions.TIMEOUT:
    print("Failed to get initial GDB prompt")
    sys.exit(1)

child.sendline("target remote localhost:1234")
child.expect_exact(gdb_prompt)

child.sendline("break main")
child.expect_exact(gdb_prompt)

child.sendline("continue")
child.expect_exact(gdb_prompt, timeout=15)

times = []
levels = []

start_time = time.time()

def read_signal_level():
    child.sendcontrol('c')
    try:
        child.expect_exact(gdb_prompt, timeout=15)
    except pexpect.exceptions.TIMEOUT:
        print("Timeout on interrupt, retrying...")
        child.sendcontrol('c')
        child.expect_exact(gdb_prompt, timeout=15)

    child.sendline("x/1xw 0x40010000")
    child.expect_exact(gdb_prompt)
    output = child.before
    print(f"GDB Output (SIGNAL_REG): {output}")

    signal_value = 0
    for line in output.splitlines():
        if "0x40010000" in line:
            match = re.search(r"0x[0-9a-fA-F]+:\s*(0x[0-9a-fA-F]+)", line)
            if match:
                try:
                    signal_value = int(match.group(1), 16) & 0x1
                except:
                    return 0, 0, 0

    child.sendline("x/1xw 0x40010004")
    child.expect_exact(gdb_prompt)
    debug_output = child.before

    debug_value = 0
    for line in debug_output.splitlines():
        if "0x40010004" in line:
            match = re.search(r"0x[0-9a-fA-F]+:\s*(0x[0-9a-fA-F]+)", line)
            if match:
                try:
                    debug_value = int(match.group(1), 16)
                except:
                    pass

    child.sendline("x/1xw 0x40010008")
    child.expect_exact(gdb_prompt)
    counter_output = child.before

    counter_value = 0
    for line in counter_output.splitlines():
        if "0x40010008" in line:
            match = re.search(r"0x[0-9a-fA-F]+:\s*(0x[0-9a-fA-F]+)", line)
            if match:
                try:
                    counter_value = int(match.group(1), 16)
                except:
                    pass

    return signal_value, debug_value, counter_value

# Setup figure and histogram
fig = plt.figure("Virtual GPIO Toggle Visualization")
ax = fig.add_subplot(111)

# Set y-axis with ON/OFF labels
ax.set_ylim(-0.1, 1.1)
ax.set_yticks([0, 1])
ax.set_yticklabels(['OFF', 'ON'])

ax.set_xlim(0, 100)
ax.set_xticks(range(0, 101, 10))
ax.set_xlabel('Time (s)')
ax.set_ylabel('Virtual LED Signal')
ax.set_title('Virtual LED I/O on Virtual Arm Cortex-A53')
ax.grid(True)

# LED indicator (top-right corner)
led_ax = fig.add_axes([0.8, 0.86, 0.1, 0.1])
led_ax.axis('off')
led_circle = patches.Circle((0.5, 0.5), 0.25, color='gray')
led_ax.add_patch(led_circle)

def update(frame):
    current_time = time.time() - start_time
    signal_value, debug_value, counter_value = read_signal_level()
    print(f"{current_time:.2f}s: Signal = {signal_value}, Debug = 0x{debug_value:04X}, Counter = {counter_value}")

    # Append all signal values (0 or 1)
    times.append(current_time)
    levels.append(signal_value)

    # Clear previous histogram
    ax.clear()
    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['OFF', 'ON'])
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Virtual LED Signal')
    ax.set_title('Virtual LED I/O on Virtual Arm Cortex-A53')
    ax.grid(True)

    # Update x-axis limits
    if current_time > 100:
        ax.set_xlim(current_time - 100, current_time)
        ax.set_xticks([current_time - 100 + i * 10 for i in range(11)])
    else:
        ax.set_xlim(0, 100)
        ax.set_xticks(range(0, 101, 10))

    # Plot histogram for high signals only
    if times and levels:
        # Filter for signal_value == 1 for histogram
        high_times = [t for t, l in zip(times, levels) if l == 1]
        high_levels = [l for l in levels if l == 1]
        if high_times and high_levels:
            bar_width = 1
            ax.bar(high_times, high_levels, width=bar_width, color='blue', alpha=0.5, align='center')
        
        # Plot line for y=0 up to the current time
        x_start, x_end = ax.get_xlim()
        ax.plot([x_start, current_time], [0, 0], 'b-', linewidth=2, color='blue')

    # LED update
    led_circle.set_color('red' if signal_value else 'gray')

    # Resume program
    child.sendline("continue")
    try:
        child.expect_exact(gdb_prompt, timeout=15)
    except pexpect.exceptions.TIMEOUT:
        print("Warning: Timeout on continue, retrying...")
        child.sendcontrol('c')
        child.expect_exact(gdb_prompt, timeout=15)

    return led_circle,

# animation
ani = animation.FuncAnimation(fig, update, interval=100, cache_frame_data=False)
plt.show()