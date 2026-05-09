#!/usr/bin/env python3
"""
Tower of Hanoi — animated ASCII demo.

Coding challenge: Broadening the RISC-V High Precision Code Base and Reach.

A short, self-contained script that solves Tower of Hanoi and animates the
solution in the terminal. No external dependencies — runs on any Python 3
install, including the standard Python interpreter on RISC-V Linux distros.

Usage:
    python3 hanoi.py            # default: 5 disks
    python3 hanoi.py 7          # custom disk count (1–10 sensible)
"""

import os
import sys
import time

# ---------- Config -----------------------------------------------------------
NUM_DISKS = int(sys.argv[1]) if len(sys.argv) > 1 else 5
DELAY     = 0.35                      # seconds between frames
DISK_CH   = "█"
POLE_CH   = "│"
BASE_CH   = "═"

if not 1 <= NUM_DISKS <= 10:
    sys.exit("Please choose between 1 and 10 disks.")

# ---------- State ------------------------------------------------------------
# Each tower is a stack: index 0 is the bottom, the top of the list is the top
# of the physical pile. Disks are stored as integers representing their size.
towers = [[], [], []]
moves  = 0

# ---------- Rendering --------------------------------------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def draw():
    """Print one frame: three towers side by side, plus a status line."""
    clear()
    width = 2 * NUM_DISKS + 1         # widest disk = widest column
    gap   = "    "

    print(f"\n  Tower of Hanoi  •  {NUM_DISKS} disks  •  move {moves:>3}\n")

    # Render rows from top of tower down to the base.
    for level in range(NUM_DISKS - 1, -1, -1):
        line = "  "
        for tower in towers:
            if level < len(tower):
                disk_w = 2 * tower[level] + 1
                pad    = (width - disk_w) // 2
                line  += " " * pad + DISK_CH * disk_w + " " * pad
            else:
                pad = width // 2
                line += " " * pad + POLE_CH + " " * pad
            line += gap
        print(line)

    print("  " + (BASE_CH * width + gap) * 3)
    print("  " + "".join(f"{label:^{width}}{gap}" for label in "ABC"))

    time.sleep(DELAY)

def step(src, dst):
    """Pop a disk off `src`, push onto `dst`, and redraw."""
    global moves
    towers[dst].append(towers[src].pop())
    moves += 1
    draw()

# ============================================================================
# RECURSION  —  the elegant heart of Tower of Hanoi
# ----------------------------------------------------------------------------
# To move n disks from `src` to `dst` using `aux` as scratch space:
#
#     1. Recursively move the top (n-1) disks    src -> aux
#     2. Move the single largest remaining disk  src -> dst
#     3. Recursively move those (n-1) disks      aux -> dst
#
# Each call shrinks the problem by exactly one disk and terminates at n == 0.
# The optimal move count is 2^n - 1, which falls out of the recurrence
# T(n) = 2·T(n-1) + 1 with T(0) = 0.
# ============================================================================
def hanoi(n, src, dst, aux):
    if n == 0:
        return                              # base case: nothing to move
    hanoi(n - 1, src, aux, dst)             # recursive call #1
    step(src, dst)                          # the real work
    hanoi(n - 1, aux, dst, src)             # recursive call #2

# ---------- Driver -----------------------------------------------------------
def main():
    # ---- ITERATION ----------------------------------------------------------
    # Build the initial stack on tower A by iterating from largest to smallest.
    # A simple `for` loop is the natural fit here; recursion would be overkill.
    for size in range(NUM_DISKS, 0, -1):
        towers[0].append(size)

    draw()
    time.sleep(0.8)

    # ---- RECURSION ----------------------------------------------------------
    # Hand off to the recursive solver. Source = A (0), target = C (2).
    hanoi(NUM_DISKS, 0, 2, 1)

    optimal = 2 ** NUM_DISKS - 1
    print(f"\n  Solved in {moves} moves  (optimal: {optimal})\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\n  Interrupted.\n")
        sys.exit(130)
