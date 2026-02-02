#!/usr/bin/env python3
"""
CLI Habit Tracker - Track your daily habits and build streaks
"""
import json
import typer
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import schedule
import time
import threading

app = typer.Typer(help="Track your daily habits and build streaks")
console = Console(force_terminal=True, legacy_windows=False)

DATA_FILE = Path.home() / ".habit_tracker_data.json"


class HabitTracker:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self) -> dict:
        """Load habit data from JSON file"""
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {"habits": {}, "reminders": {}}

    def save_data(self):
        """Save habit data to JSON file"""
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_habit(self, name: str, description: str = ""):
        """Add a new habit"""
        if name in self.data["habits"]:
            return False, "Habit already exists"

        self.data["habits"][name] = {
            "description": description,
            "created_date": datetime.now().isoformat(),
            "completions": [],
            "current_streak": 0,
            "longest_streak": 0
        }
        self.save_data()
        return True, f"Habit '{name}' added successfully"

    def remove_habit(self, name: str):
        """Remove a habit"""
        if name not in self.data["habits"]:
            return False, "Habit not found"

        del self.data["habits"][name]
        if name in self.data["reminders"]:
            del self.data["reminders"][name]
        self.save_data()
        return True, f"Habit '{name}' removed successfully"

    def mark_done(self, name: str, date: Optional[str] = None):
        """Mark a habit as done for a specific date"""
        if name not in self.data["habits"]:
            return False, "Habit not found"

        if date is None:
            date = datetime.now().date().isoformat()

        habit = self.data["habits"][name]

        if date in habit["completions"]:
            return False, "Habit already marked as done for this date"

        habit["completions"].append(date)
        habit["completions"].sort()
        self._update_streaks(name)
        self.save_data()
        return True, f"Habit '{name}' marked as done for {date}"

    def unmark_done(self, name: str, date: Optional[str] = None):
        """Unmark a habit for a specific date"""
        if name not in self.data["habits"]:
            return False, "Habit not found"

        if date is None:
            date = datetime.now().date().isoformat()

        habit = self.data["habits"][name]

        if date not in habit["completions"]:
            return False, "Habit was not marked as done for this date"

        habit["completions"].remove(date)
        self._update_streaks(name)
        self.save_data()
        return True, f"Habit '{name}' unmarked for {date}"

    def _update_streaks(self, name: str):
        """Calculate and update current and longest streaks"""
        habit = self.data["habits"][name]
        completions = [datetime.fromisoformat(d).date() for d in habit["completions"]]

        if not completions:
            habit["current_streak"] = 0
            habit["longest_streak"] = 0
            return

        completions.sort(reverse=True)
        today = datetime.now().date()

        # Calculate current streak
        current_streak = 0
        expected_date = today

        for completion_date in completions:
            if completion_date == expected_date:
                current_streak += 1
                expected_date -= timedelta(days=1)
            elif completion_date == expected_date + timedelta(days=1):
                # Allow for yesterday if today isn't done yet
                current_streak += 1
                expected_date -= timedelta(days=1)
            else:
                break

        # Calculate longest streak
        longest_streak = 0
        temp_streak = 1

        completions.sort()
        for i in range(1, len(completions)):
            diff = (completions[i] - completions[i-1]).days
            if diff == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1

        longest_streak = max(longest_streak, temp_streak)

        habit["current_streak"] = current_streak
        habit["longest_streak"] = longest_streak

    def get_habits(self) -> dict:
        """Get all habits"""
        return self.data["habits"]

    def get_habit_stats(self, name: str) -> Optional[dict]:
        """Get statistics for a specific habit"""
        if name not in self.data["habits"]:
            return None

        habit = self.data["habits"][name]
        completions = habit["completions"]

        if not completions:
            return {
                "name": name,
                "total_completions": 0,
                "current_streak": 0,
                "longest_streak": 0,
                "success_rate_7d": 0,
                "success_rate_30d": 0,
                "last_completed": None
            }

        today = datetime.now().date()
        last_7_days = [(today - timedelta(days=i)).isoformat() for i in range(7)]
        last_30_days = [(today - timedelta(days=i)).isoformat() for i in range(30)]

        completed_7d = sum(1 for d in last_7_days if d in completions)
        completed_30d = sum(1 for d in last_30_days if d in completions)

        return {
            "name": name,
            "description": habit["description"],
            "total_completions": len(completions),
            "current_streak": habit["current_streak"],
            "longest_streak": habit["longest_streak"],
            "success_rate_7d": round((completed_7d / 7) * 100, 1),
            "success_rate_30d": round((completed_30d / 30) * 100, 1),
            "last_completed": completions[-1] if completions else None
        }

    def set_reminder(self, name: str, time_str: str):
        """Set a reminder time for a habit"""
        if name not in self.data["habits"]:
            return False, "Habit not found"

        try:
            datetime.strptime(time_str, "%H:%M")
        except ValueError:
            return False, "Invalid time format. Use HH:MM (e.g., 09:00)"

        self.data["reminders"][name] = time_str
        self.save_data()
        return True, f"Reminder set for '{name}' at {time_str}"

    def get_reminders(self) -> dict:
        """Get all reminders"""
        return self.data["reminders"]


tracker = HabitTracker()


@app.command()
def add(
    name: str,
    description: str = typer.Option("", "--description", "-d", help="Description of the habit")
):
    """Add a new habit to track"""
    success, message = tracker.add_habit(name, description)
    if success:
        console.print(f"[green]+[/green] {message}")
    else:
        console.print(f"[red]x[/red] {message}")


@app.command()
def remove(name: str):
    """Remove a habit"""
    success, message = tracker.remove_habit(name)
    if success:
        console.print(f"[green]+[/green] {message}")
    else:
        console.print(f"[red]x[/red] {message}")


@app.command()
def done(
    name: str,
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Date (YYYY-MM-DD), defaults to today")
):
    """Mark a habit as done"""
    success, message = tracker.mark_done(name, date)
    if success:
        console.print(f"[green]+[/green] {message}")

        # Show updated streak
        habit = tracker.data["habits"][name]
        streak = habit["current_streak"]
        if streak > 0:
            console.print(f"[yellow]>> Current streak: {streak} days![/yellow]")
    else:
        console.print(f"[red]x[/red] {message}")


@app.command()
def undone(
    name: str,
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Date (YYYY-MM-DD), defaults to today")
):
    """Unmark a habit"""
    success, message = tracker.unmark_done(name, date)
    if success:
        console.print(f"[green]+[/green] {message}")
    else:
        console.print(f"[red]x[/red] {message}")


@app.command()
def list():
    """List all habits with today's status"""
    habits = tracker.get_habits()

    if not habits:
        console.print("[yellow]No habits tracked yet. Add one with 'habit-tracker add <name>'[/yellow]")
        return

    today = datetime.now().date().isoformat()

    table = Table(title="Your Habits", box=box.ROUNDED)
    table.add_column("Habit", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Streak", justify="center", style="yellow")
    table.add_column("Best", justify="center", style="green")
    table.add_column("Description", style="dim")

    for name, habit in habits.items():
        done_today = "+" if today in habit["completions"] else "o"
        status_style = "green" if today in habit["completions"] else "dim"

        table.add_row(
            name,
            f"[{status_style}]{done_today}[/{status_style}]",
            f"{habit['current_streak']}d",
            f"Best: {habit['longest_streak']}d",
            habit["description"]
        )

    console.print(table)

    # Show reminders if any
    reminders = tracker.get_reminders()
    if reminders:
        console.print("\n[bold]Reminders:[/bold]")
        for habit_name, time_str in reminders.items():
            console.print(f"  - {habit_name}: {time_str}")


@app.command()
def stats(name: str):
    """Show detailed statistics for a habit"""
    stats = tracker.get_habit_stats(name)

    if stats is None:
        console.print(f"[red]x[/red] Habit '{name}' not found")
        return

    panel_content = f"""[bold cyan]{stats['name']}[/bold cyan]
{stats['description']}

[bold]Total Completions:[/bold] {stats['total_completions']}
[bold]Current Streak:[/bold] {stats['current_streak']} days
[bold]Longest Streak:[/bold] {stats['longest_streak']} days

[bold]Success Rates:[/bold]
  Last 7 days:  {stats['success_rate_7d']}%
  Last 30 days: {stats['success_rate_30d']}%

[bold]Last Completed:[/bold] {stats['last_completed'] or 'Never'}
"""

    console.print(Panel(panel_content, title="Habit Statistics", border_style="green"))


@app.command()
def history(
    name: str,
    days: int = typer.Option(30, "--days", "-n", help="Number of days to show")
):
    """Show completion history for a habit"""
    if name not in tracker.data["habits"]:
        console.print(f"[red]x[/red] Habit '{name}' not found")
        return

    habit = tracker.data["habits"][name]
    completions = set(habit["completions"])

    console.print(f"\n[bold]History for '{name}' (last {days} days)[/bold]\n")

    today = datetime.now().date()
    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.isoformat()

        if date_str in completions:
            symbol = "+"
            style = "green"
        else:
            symbol = "x"
            style = "red"

        day_name = date.strftime("%A")
        console.print(f"[{style}]{symbol}[/{style}] {date_str} ({day_name})")


@app.command()
def remind(
    name: str,
    time: str
):
    """Set a reminder for a habit (time in HH:MM format, e.g., 09:00)"""
    success, message = tracker.set_reminder(name, time)
    if success:
        console.print(f"[green]+[/green] {message}")
        console.print("[dim]Note: Reminders are shown when you run the 'list' command[/dim]")
    else:
        console.print(f"[red]x[/red] {message}")


@app.command()
def today():
    """Show quick summary for today"""
    habits = tracker.get_habits()

    if not habits:
        console.print("[yellow]No habits tracked yet.[/yellow]")
        return

    today = datetime.now().date().isoformat()
    completed = sum(1 for h in habits.values() if today in h["completions"])
    total = len(habits)

    percentage = (completed / total * 100) if total > 0 else 0

    if percentage == 100:
        symbol = "***"
        color = "green"
        message = "Perfect day!"
    elif percentage >= 75:
        symbol = "**"
        color = "green"
        message = "Great job!"
    elif percentage >= 50:
        symbol = "*"
        color = "yellow"
        message = "Keep going!"
    else:
        symbol = ">"
        color = "yellow"
        message = "You can do it!"

    console.print(Panel(
        f"[{color}]{symbol} {completed}/{total} habits completed ({percentage:.0f}%)\n{message}[/{color}]",
        title=f"Today - {datetime.now().strftime('%B %d, %Y')}",
        border_style=color
    ))

    # Show incomplete habits
    incomplete = [name for name, habit in habits.items() if today not in habit["completions"]]
    if incomplete:
        console.print("\n[bold]Still to do:[/bold]")
        for habit_name in incomplete:
            console.print(f"  - {habit_name}")


if __name__ == "__main__":
    app()
