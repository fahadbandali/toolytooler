import cmd, sys
import subprocess
import os
from openai import OpenAI

class ToolyTooler(cmd.Cmd):
    intro = "This is a special terminal powered by AI to use custom scripts and CLI comments navigate the terminal in plain language"
    prompt = "(tooly)"
    open_ai_client = None
    system_instruction = None

    def do_setup(self, arg):
        "function that asks the user to provide their open ai key to store it as an env variable"
        args = arg.split()
        
        force_flag = '--force' in args
        
        if force_flag:
            os.environ.pop('OPENAI_API_KEY', None) 
            print("Cleared existing environment variable OPENAI_API_KEY.")

        open_ai_key = os.getenv("OPENAI_API_KEY")
        if open_ai_key is None or open_ai_key == '':
            input_api_key = input("OpenAI Api key is not defined, lets store it as a system variable. Please enter it: ")
            print(f"Run the following command in your terminal to set the API key:")
            command = f'export OPENAI_API_KEY="{input_api_key}" && python3 tooly-tooler.py'
            print(command)
            sys.exit()
        else:
            file_path = 'system-prompt.txt'
            process_results = subprocess.run("pwd", capture_output=True, text=True)
            with open(file_path, 'r') as file:
                self.system_instruction = file.read()
            self.system_instruction += f"You are operating from {process_results.stdout} and you wont have access to all directories so only provide commands that you will not get a permission issue."
            self.open_ai_client = OpenAI()
            print("You're all set, use the command 'ask' to start going through your terminal")

    def do_ask(self, arg):
        "function that sends prompts to an AI model and gets the desired response"
        try:
            context = arg
            if self.open_ai_client is None:
                print("use the 'setup' command to add your open ai key")
                return

            while True:
                result = self._prompt_open_ai(context)
                if result["command"] is not None:

                    if result["command"] == "Be more specific.":
                        feedback = input("Lets revise your ask ")
                        context += f"Context from previous ask {arg}, Results from previous ask: {result["command"]}. New ask {feedback}"
                        print("Generating a new command based on your feedback...")
                        continue
                    else:
                        print(f"Command to execute: {result["command"]}")
                        user_input = input(f"Do you want to execute this command? (y/n): ")
                    if user_input.lower() == 'y':
                        process_results = subprocess.run(result["command"], shell=True, capture_output=True, text=True)
                        print("Command executed. Here is the output:")
                        print(process_results.stdout)
                        print(process_results.stderr)
                        feedback = input("Want to continue? y/n ")
                        if feedback.lower() == "n":
                            print("exiting the ask prompt flow")
                            break
                        else:
                            feedback = input("Lets continue, what should we do next? ")
                            context += f"Context from previous ask {arg}, Results from previous ask: {result["command"]}. New ask {feedback}"
                    elif user_input.lower() == 'n':
                        feedback = input("How can I do better? Please provide your feedback: ")
                        context += f"Context from previous ask {arg}, Results from previous ask: {result["command"]}. New ask {feedback}"
                        print("Generating a new command based on your feedback...")
                    elif user_input.lower() == 'q':
                        print("exiting the ask prompt flow")
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
        except KeyboardInterrupt:
            print("Exiting the ask function gracefully")

    def do_exit(self, arg):
        "function that closes the terminal"
        return True

    def _prompt_open_ai(self, arg):
        response = self.open_ai_client.responses.create(
            model="gpt-4o-mini",
            instructions=self.system_instruction,
            input=arg,
            tools=[]
        )

        return { "command": response.output_text }

if __name__ == '__main__':
    try:
        ToolyTooler().cmdloop() 
    except KeyboardInterrupt:
        print("thanks for trying tooly!")