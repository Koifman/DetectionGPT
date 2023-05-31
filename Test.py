import openai
import requests
import yaml
import json

openai.api_key = "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"

# Function to retrieve SIGMA rule from a YAML file
def get_sigma_rule_from_yaml(yaml_url):
    # Send HTTP GET request to retrieve the YAML file
    response = requests.get(yaml_url)
    
    # Parse the YAML content and extract the SIGMA rule
    sigma_rule = yaml.safe_load(response.text)
    
    return sigma_rule

# Function to generate CMD command from a SIGMA rule
def generate_cmd_command(sigma_rule):
    # Convert the SIGMA rule to a string
    sigma_rule_str = yaml.dump(sigma_rule)
    
    # Send the SIGMA rule as a prompt to the API
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role":"system","content":"provide CMD commands that demonstrate the behavior described in the following sigma rule"+sigma_rule_str}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    # Extract the generated CMD command from the API response
    cmd_command = response.choices[0].message["content"]
    #formatted = json.dumps(cmd_command, indent=4)
    
    return cmd_command

# Main interaction loop
while True:
    # Get YAML URL input from the user
    yaml_url = input("Enter the URL of a SIGMA rule in YAML format (or 'quit' to exit): ")
    
    # Check if user wants to exit
    if yaml_url.lower() == 'quit':
        break
    
    # Retrieve the SIGMA rule from the YAML file
    sigma_rule = get_sigma_rule_from_yaml(yaml_url)
    
    
    # Generate CMD command from the SIGMA rule
    cmd_command = generate_cmd_command(sigma_rule)
    
    # Display the generated CMD command
    print("Generated CMD command:")
    print(cmd_command)
    print()