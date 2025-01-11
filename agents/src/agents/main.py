#!/usr/bin/env python
import sys
import warnings

from agents.crew import AgentsCrew
import datetime
import json


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

from dotenv import load_dotenv
load_dotenv()

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    with open('map_example.json', 'r') as file:
        office_map = json.load(file)

    office_map_string = json.dumps(office_map, indent=2)

    inputs = {
        # 'current_date': datetime.datetime.now().strftime("%Y-%m-%d"),
        # 'instagram_description': "Trudeau resigned", # input('Enter the page description here: '),
        # 'topic_of_the_week': "Canadian politics", # input('Enter the topic of the week here: '),
        # "idea": "Launch a 'Green Pledge' campaign encouraging customers to share their own eco-friendly habits using the hashtag #MyGreenPledge. The campaign will include social media challenges, user-generated content, and a partnership with a well-known environmental non-profit to plant trees for every pledge shared. The goal is to boost brand awareness while aligning with the current sustainability trend.",
        # "current_market_context": "The market is currently seeing a shift toward eco-conscious products and services. Consumers are prioritizing brands that emphasize sustainability, transparency, and ethical practices. Social media engagement is higher for content that highlights authentic environmental initiatives, with hashtags like #SustainableLiving and #EcoFriendly trending. Competitor brands have launched campaigns showcasing their commitment to reducing carbon footprints, which have gained significant traction."
        # "topic": "AI LLMs"
        "map_data": office_map_string
    }
    AgentsCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AgentsCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgentsCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AgentsCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
