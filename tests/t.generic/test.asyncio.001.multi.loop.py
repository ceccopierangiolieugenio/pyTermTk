#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio

# Define the first endless loop
async def loop_one():
    while True:
        print("Running loop one...")
        await asyncio.sleep(1)  # Non-blocking sleep

# Define the second endless loop
async def loop_two():
    while True:
        print("Running loop two...")
        await asyncio.sleep(2)  # Non-blocking sleep

# Main entry point
async def main():
    # Create and run tasks for the loops
    task1 = asyncio.create_task(loop_one())
    task2 = asyncio.create_task(loop_two())
    
    # Keep the program running indefinitely
    await asyncio.gather(task1, task2)

# Run the event loop
asyncio.run(main())
