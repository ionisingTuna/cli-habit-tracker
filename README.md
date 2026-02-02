# CLI Habit Tracker

A beautiful and powerful command-line habit tracker to help you build and maintain daily habits with streak tracking, statistics, and reminders.

## Features

- **Basic Tracking**: Add/remove habits and mark them as done
- **Streak Tracking**: Track current and longest streaks for each habit
- **History & Statistics**: View completion history and success rates
- **Reminders**: Set reminder times for your habits
- **Beautiful Interface**: Rich terminal UI with colors and tables

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd cli-habit-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install as a command:
```bash
pip install -e .
```

Now you can use `habit-tracker` from anywhere!

## Usage

### Add a new habit
```bash
python habit_tracker.py add "Exercise" --description "30 minutes of exercise"
# or if installed: habit-tracker add "Exercise" -d "30 minutes of exercise"
```

### List all habits
```bash
python habit_tracker.py list
```

### Mark a habit as done
```bash
python habit_tracker.py done "Exercise"
```

### View today's summary
```bash
python habit_tracker.py today
```

### View detailed statistics
```bash
python habit_tracker.py stats "Exercise"
```

### View completion history
```bash
# Shows last 30 days by default
python habit_tracker.py history "Exercise"
```

### Set a reminder
```bash
python habit_tracker.py remind "Exercise" "07:00"
```

### Unmark a habit (if marked by mistake)
```bash
python habit_tracker.py undone "Exercise"
```

### Remove a habit
```bash
python habit_tracker.py remove "Exercise"
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `add <name>` | Add a new habit to track |
| `remove <name>` | Remove a habit |
| `done <name>` | Mark a habit as done for today |
| `undone <name>` | Unmark a habit |
| `list` | List all habits with today's status |
| `today` | Show quick summary for today |
| `stats <name>` | Show detailed statistics for a habit |
| `history <name>` | Show completion history |
| `remind <name> <time>` | Set a reminder (HH:MM format) |

## Data Storage

Habit data is stored in `~/.habit_tracker_data.json` in your home directory.

## Examples

```bash
# Morning routine
habit-tracker add "Meditation" -d "10 minutes of meditation"
habit-tracker add "Exercise" -d "30 minutes workout"
habit-tracker add "Reading" -d "Read 20 pages"

# Set reminders
habit-tracker remind "Meditation" "07:00"
habit-tracker remind "Exercise" "07:30"
habit-tracker remind "Reading" "21:00"

# Mark habits as done
habit-tracker done "Meditation"
habit-tracker done "Exercise"

# Check progress
habit-tracker today
habit-tracker list

# View detailed stats
habit-tracker stats "Exercise"
```

## License

MIT License