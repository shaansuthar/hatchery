from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from agents.tools.search import SearchTools
from langchain_ollama import ChatOllama
from langchain_cohere import ChatCohere
from datetime import datetime

# Llama3_2 = ChatOllama(model="llama3.2")

llm = ChatCohere(temperature=0.3)
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Uncomment the following line to use an example of a custom tool
# from Agents.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


@CrewBase
class AgentsCrew:
    """Agents crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["marketing_director"],
            allow_delegation=True,
            verbose=True,
            max_iter=5,
            llm=llm,
        )

    @agent
    def market_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["market_researcher"],
            tools=[
              SearchTools.open_page,
            ],
            verbose=True,
            llm=llm,
        )

    # @agent
    # def content_strategist(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["content_strategist"],
    #         verbose=True
    #     )

    @agent
    def creative_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["creative_designer"],
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )

    @agent
    def copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config["copywriter"],
            verbose=True,
            llm=llm,
        )
        

    @task
    def market_research(self) -> Task:
        return Task(
            config=self.tasks_config["market_research"],
            agent=self.market_researcher(),
            output_file=f"src/agents/simulations/{now}/market_research.md",
        )

    # @task
    # def content_strategy_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["content_strategy"],
    #         agent=self.content_strategist(),
    #     )

    @task
    def creative_design_task(self) -> Task:
        return Task(
            config=self.tasks_config["creative_design"],
            agent=self.creative_designer(),
            output_file=f"src/agents/simulations/{now}/visual-content.md",
        )

    @task
    def copywriting_task(self) -> Task:
        return Task(
            config=self.tasks_config["copywriting"],
            agent=self.copywriter(),
            output_file=f"src/agents/simulations/{now}/copywriting.json",
        )
    
    @task
    def move_character_task(self) -> Task:
        return Task(
            config=self.tasks_config["move_character"],
            agent=self.manager(),
            output_file=f"src/agents/simulations/{now}/movement.json",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Agents crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.hierarchical,
            verbose=1,
            # manager_llm=Llama3_2
            manager_agent=self.manager()
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
