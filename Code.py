import openai
import requests
import yaml
import json
import subprocess
import time


openai.api_key = "ENTER_KEY_HERE"


def get_sigma_rule_from_yaml(yaml_url):
    response = requests.get(yaml_url)
    sigma_rule = yaml.safe_load(response.text)
    return sigma_rule


def generate_cmd_command(sigma_rule):
    sigma_rule_str = yaml.dump(sigma_rule)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role":"system","content":"provide CMD commands that demonstrate the behavior described in the following sigma rule"+sigma_rule_str + ". Please make sure to give me a list of ONLY the commands, without ANY other text. Also, please include commands to REVERT any creations or modifications from the previous commands. Again, list ONLY commands, without any other explanation text whatsoever. Also, please include a number prefix for each command you include, for example: 1. <Command>"}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.3
    )
    

    cmd_command = response.choices[0].message["content"]
    return cmd_command

def run_commands(output):
    output = output.split("\n")
    commands_to_run = [line.split('. ', 1)[1] for line in output if '. ' in line]
    print("Running the following commands:\n")
    for command in commands_to_run:
        print(command + "\n")
    print("\n\n") 
    for command in commands_to_run:
        print("[*] Running: " + command + "\n")
        completed_process = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(completed_process.stdout)
        time.sleep(2)


while True:
    yaml_url = input("Enter the URL of a SIGMA rule in YAML format (or 'quit' to exit): ")
    if yaml_url.lower() == 'quit':
        break
    

    sigma_rule = get_sigma_rule_from_yaml(yaml_url)
    cmd_command = generate_cmd_command(sigma_rule)
    
    print("Generated CMD command:")
    print(cmd_command)
    ifrun = input("Would you like to execute the commands? Y/N\n")
    if ifrun == "Y" or ifrun == "y":
        commands_list = run_commands(cmd_command)
    else:
        break
