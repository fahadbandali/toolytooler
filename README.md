# Tooly Tooler

A Python script that helps with navigating the terminal.
It uses ChatGpt 4o mini with a system instruction to get the commands you need and iterate on them

In the future, I'd like to:
- add tools to the prompt. The tools should contain custom shell scripts located in the custom-scripts folder which take in multiple arguments and do some longer processes
- Adjust this program so it's a dedicated cli prompt so instead of running the program you could do `tooly ask where is the pdf of my latest resume`

Installation:
1. create your virtual environment and activate `python3.13 -m venv .venv && source .venv/bin/activate`
2. install the cmd, os and openai libraries using `pip install lib-name`
3. start tooly `python3 tooly-tooler.py`
4. add your open ai api key by running `setup`
5. start navigating the terminal in your language by using the ask command `ask give me the last 5 files that were recently modified in my downloads folder`
