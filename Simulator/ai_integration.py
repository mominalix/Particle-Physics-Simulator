import openai

# Set your OpenAI API key here
api_path="C:/Users/FRENZY/Desktop/Github/apikey.txt"
with open(api_path, 'r') as file:
    # Read the first line
    openai.api_key = file.readline()

def extract_scenario(prompt):
    # Call the OpenAI API to generate scenario information from the prompt
    customized_prompt="Here is the prompt for a scenario of a phyics simulation: \n'"+prompt+ "'\nI want you to only return values in following format which will be fed as initial conditions (position, velocity and weight) to the simulator. You can add or remove number of particles, set their weights, their velocities(vx,vy,vx) and their positions(x,y,z) in a 3d space to best define scenario. It is better to keep a little distance between particles too and set their approach through velocity. Use the following format and do changes as mentioned: \n'particles': [ {'x': 0.0, 'y': 0.0, 'z': 0.0, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0, 'weight': 1.0}, {'x': 0.0, 'y': 0.0, 'z': 0.0, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0, 'weight': 1.0}]"
    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=customized_prompt,
        max_tokens=500,
        stop=None,
        temperature=0.7,
    )
    print(response.choices[0].text)
    # Extract relevant information from the API response\
    parsed_scenario = parse_response(response.choices[0].text)
    return parsed_scenario



def parse_response(response_text):
    # Implement your logic to parse the generated text and extract scenario data
    # Return the extracted scenario data as a dictionary
    # Example:
    print (response_text)
    return response_text
