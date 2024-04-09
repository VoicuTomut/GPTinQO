from gpt_sage.assistant import Evaluate
from gpt_sage.config import get_config
import time
import json
from flask import Flask, request, jsonify


GPT_CONFIG = "config/gpt.toml"
REQUEST_STORAGE = "data/request_data/history.json"
config = get_config(GPT_CONFIG)
JUDGE= Evaluate(config)



def extract_gpt(gpt_message: str):
    """
    convert the gpt message to a dictionary to be more friendly to use
    :param gpt_message: gpt message
    :type gpt_message: str
    :return: extract
    :rtype: dict
    """
    # Initialize an empty dictionary to store the extracted data
    extract = {}

    # Split the tagged set string by newline characters
    lines = gpt_message.split('\n')

    # Iterate through each line and extract key-value pairs
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)  # Split only at the first occurrence of ':'
            key = key.strip()  # Remove leading/trailing whitespace
            value = value.strip()  # Remove leading/trailing whitespace
            extract[key] = value
    return extract


def save_dictionary_to_file(dictionary: dict, filename: str):
    """
    Save dictionary to file.
    :param dictionary: dictionary
    :type dictionary: dict
    :param filename: path to the file where the data wil be saved
    :type filename: str
    :return: -
    :rtype: -
    """
    with open(filename, 'a') as file:
        json.dump(dictionary, file)
        file.write('\n')  # Add a newline to separate dictionaries


app = Flask(__name__)

@app.route('/process_answer', methods=['POST'])
def process_answer():

    input_dict = request.json
    u_id = input_dict["user_id"]
    question = input_dict["question"]
    expectation = input_dict["expectation"]
    value = input_dict["value"]

    performance = JUDGE.measure(question, expectation, value)
    extract = extract_gpt(performance["gpt"])

    interaction_info = {"input": {"question": question, "expectation": expectation, "value": value},
                       "performance": performance,
                       "gpt_extract": extract,
                       "time": time.time(),
                       "u_id": u_id,
                       }

    save_dictionary_to_file(interaction_info, REQUEST_STORAGE)

    return  jsonify(interaction_info)


if __name__ == '__main__':
    app.run(debug=True)