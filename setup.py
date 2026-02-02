from setuptools import setup

setup(
    name="habit-tracker",
    version="1.0.0",
    py_modules=["habit_tracker"],
    install_requires=[
        "typer[all]==0.12.5",
        "rich==13.9.4",
        "schedule==1.2.2",
    ],
    entry_points={
        "console_scripts": [
            "habit-tracker=habit_tracker:app",
        ],
    },
    author="Your Name",
    description="A CLI tool to track daily habits and build streaks",
    python_requires=">=3.7",
)
