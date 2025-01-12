from crewai import Agent
from crewai.project import CrewBase
# from langchain_cohere import ChatCohere


# llm = ChatCohere(temperature=0.3)

@CrewBase
class MarketingAgents():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    iterations = 2

    # def manager(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["marketing_director"],
    #         allow_delegation=True,
    #         verbose=True,
    #         max_iter=self.iterations,
    #         # llm=llm,
    #     )

    # def caption_writer(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["caption_writer"],
    #         verbose=True,
    #         # llm=llm,
    #         allow_delegation=False,
    #         max_iter=self.iterations,
    #     )
    
    # def requirements_engineer(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["requirements_engineer"],
    #         verbose=True,
    #         # llm=llm,
    #         allow_delegation=False,
    #         max_iter=self.iterations,
    #     )

    def marketing_director(self) -> Agent:
        return Agent(
            config=self.agents_config["marketing_director"],
            allow_delegation=True,
            verbose=True,
            max_iter=self.iterations,
            # llm=llm,
        )

    def software_director(self) -> Agent:
        return Agent(
            config=self.agents_config["software_director"],
            allow_delegation=True,
            verbose=True,
            max_iter=self.iterations,
        )

    def product_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["product_manager"],
            allow_delegation=True,
            verbose=True,
            max_iter=self.iterations,
        )

    def caption_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["caption_writer"],
            allow_delegation=False,
            verbose=True,
            max_iter=self.iterations,
        )

    def software_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["software_developer"],
            allow_delegation=False,
            verbose=True,
            max_iter=self.iterations,
            allow_code_execution=True,
        )
    
    def requirements_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["requirements_engineer"],
            allow_delegation=False,
            verbose=True,
            max_iter=self.iterations,
            # llm=llm,
        )