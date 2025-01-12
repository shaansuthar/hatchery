import getpass
import os
from dotenv import load_dotenv
load_dotenv()

from typing import Annotated, List
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
import google.generativeai as genai
from openai import ChatCompletion
import os

# Set your OpenAI API key
# openai.api_key = "your_openai_api_key"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define agent behavior using OpenAI API calls
def agent_response(role, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text



from typing import List, Optional, Literal
from langchain_core.language_models.chat_models import BaseChatModel

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from langchain_core.messages import HumanMessage, trim_messages

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Optional

from langchain_experimental.utilities import PythonREPL
from typing_extensions import TypedDict

from typing import Annotated, List

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool


def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> str:
    options = ["FINISH"] + members
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When finished,"
        " respond with FINISH."
    )

    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""

        next: Literal[*options]

    def supervisor_node(state: MessagesState) -> Command[Literal[*members, "__end__"]]:
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto)

    return supervisor_node





# Define nodes for each agent class
class ProductManager(Node):
    def process(self, data):
        user_idea = data.get("startup_idea", "")
        refined_idea = agent_response("Product Manager", f"Refine this startup idea: {user_idea}")
        return {"refined_idea": refined_idea}

class MarketingDirector(Node):
    def process(self, data):
        refined_idea = data.get("refined_idea", "")
        market_research = agent_response("Market Researcher", f"Conduct market research for: {refined_idea}")
        design_mockups = agent_response("Visual Designer", f"Create visual assets for: {refined_idea}")
        campaign_plan = agent_response("Social Media Strategist", f"Develop a social media strategy for: {refined_idea}")
        return {
            "market_research": market_research,
            "design_mockups": design_mockups,
            "campaign_plan": campaign_plan
        }

class SoftwareDirector(Node):
    def process(self, data):
        refined_idea = data.get("refined_idea", "")
        frontend_code = agent_response("Frontend Developer", f"Develop the user interface for: {refined_idea}")
        backend_code = agent_response("Backend Developer", f"Implement backend logic for: {refined_idea}")
        test_report = agent_response("QA Engineer", f"Test the software for: {refined_idea}")
        return {
            "frontend_code": frontend_code,
            "backend_code": backend_code,
            "test_report": test_report
        }

# Create the LangGraph
class StartupSimulation(Graph):
    def __init__(self):
        super().__init__()
        # Add nodes to the graph
        self.add_node("product_manager", ProductManager())
        self.add_node("marketing_director", MarketingDirector())
        self.add_node("software_director", SoftwareDirector())

        # Define edges between nodes
        self.add_edge("product_manager", "marketing_director")
        self.add_edge("product_manager", "software_director")

# Run the simulation
def main():
    # Initialize the simulation graph
    simulation = StartupSimulation()

    # User input
    startup_idea = input("Share your startup idea: ")

    # Start the graph processing
    results = simulation.run({"startup_idea": startup_idea})

    # Display results
    print("\nSimulation Results:")
    print(f"Refined Idea: {results['product_manager']['refined_idea']}")
    print(f"Market Research: {results['marketing_director']['market_research']}")
    print(f"Design Mockups: {results['marketing_director']['design_mockups']}")
    print(f"Social Media Campaign: {results['marketing_director']['campaign_plan']}")
    print(f"Frontend Code: {results['software_director']['frontend_code']}")
    print(f"Backend Code: {results['software_director']['backend_code']}")
    print(f"Test Report: {results['software_director']['test_report']}")

if __name__ == "__main__":
    main()
