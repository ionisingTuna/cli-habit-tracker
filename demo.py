#!/usr/bin/env python3
"""
Demo script to showcase the habit tracker features
Run this to see all the commands in action
"""
import subprocess
import time
import os
from pathlib import Path

def run_cmd(cmd, description):
    """Run a command and display its output"""
    print(f"\n{'='*70}")
    print(f">>> {description}")
    print(f"$ python habit_tracker.py {cmd}")
    print(f"{'-'*70}")
    result = subprocess.run(f"python habit_tracker.py {cmd}", shell=True, capture_output=False)
    time.sleep(1)
    return result.returncode == 0

def main():
    # Clean up any existing data
    data_file = Path.home() / ".habit_tracker_data.json"
    if data_file.exists():
        response = input(f"\nExisting data found at {data_file}. Delete it for demo? (y/n): ")
        if response.lower() == 'y':
            data_file.unlink()
            print("Data file deleted.\n")

    print("\n" + "="*70)
    print("CLI HABIT TRACKER DEMO")
    print("="*70)

    # Add habits
    run_cmd('add Exercise -d "30 minutes of cardio"', "1. Add a habit with description")
    run_cmd('add Reading', "2. Add a habit without description")
    run_cmd('add Meditation -d "10 minutes mindfulness"', "3. Add another habit")

    # List habits
    run_cmd('list', "4. List all habits")

    # Mark habits as done
    run_cmd('done Exercise', "5. Mark Exercise as done")
    run_cmd('done Reading', "6. Mark Reading as done")

    # Show today's summary
    run_cmd('today', "7. Show today's summary")

    # List updated status
    run_cmd('list', "8. List updated habits")

    # Show statistics
    run_cmd('stats Exercise', "9. Show detailed statistics for Exercise")

    # Show history
    run_cmd('history Exercise', "10. Show completion history for Exercise")

    # Set reminder
    run_cmd('remind Meditation 08:00', "11. Set a reminder for Meditation")

    # List with reminders
    run_cmd('list', "12. List habits with reminders")

    print("\n" + "="*70)
    print("DEMO COMPLETE!")
    print("="*70)
    print("\nYour data is saved in:", data_file)
    print("Try exploring more commands and building your habits!")
    print("\nRun 'python habit_tracker.py --help' to see all available commands")

if __name__ == "__main__":
    main()
