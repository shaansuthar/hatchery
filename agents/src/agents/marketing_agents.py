from crewai import Agent
from crewai.project import CrewBase

@CrewBase
class MarketingAgents():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["marketing_director"],
            allow_delegation=True,
            verbose=True,
            max_iter=5,
            # llm=llm,
        )

    # def market_researcher(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["market_researcher"],
    #         # tools=[
    #         #   SearchTools.open_page,
    #         # ],
    #         verbose=True,
    #         # llm=llm,
    #         allow_delegation=False,
    #     )

    # def creative_designer(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["creative_designer"],
    #         verbose=True,
    #         allow_delegation=False,
    #         # llm=llm,
    #     )

    def caption_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["caption_writer"],
            verbose=True,
            # llm=llm,
            allow_delegation=False,
        )
    
    def requirements_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["requirements_engineer"],
            verbose=True,
            # llm=llm,
            allow_delegation=False,
        )