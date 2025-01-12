from datetime import datetime
from crewai import Task
from crewai.project import CrewBase
from crewai_tools import DallETool

# now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
now = "prod"

@CrewBase
class MarketingTasks():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # def market_research(self, agent, context) -> Task:
    #     return Task(
    #         config=self.tasks_config["market_research"],
    #         agent=agent,
    #         context=context,
    #         output_file=f"src/agents/simulations/{now}/market_research.md",
    #     )

    # def creative_design_task(self, agent, context) -> Task:
    #     return Task(
    #         config=self.tasks_config["creative_design"],
    #         agent=agent,
    #         context=context,
    #         output_file=f"src/agents/simulations/{now}/visual-content.md",
    #         tools=[DallETool()],
    #     )

    # def generate_post_task(self, agent, context) -> Task:
    #     return Task(
    #         config=self.tasks_config["generate_post"],
    #         agent=agent,
    #         context=context,
    #         # tools=[DallETool()],
    #         output_file=f"src/agents/simulations/{now}/caption.md",
    #     )
    
    # def move_character_task(self, agent, context) -> Task:
    #     return Task(
    #         config=self.tasks_config["move_character"],
    #         agent=agent,
    #         context=context,
    #         output_file=f"src/agents/simulations/{now}/movement.json",
    #     )
    
    # def generate_requirements_task(self, agent) -> Task:
    #     return Task(
    #         config=self.tasks_config["product_requirements"],
    #         agent=agent,
    #         output_file=f"src/agents/simulations/{now}/requirements.md",
    #     )
    


    def move_character_task(self, agent, context) -> Task:
        return Task(
            config=self.tasks_config["move_character"],
            agent=agent,
            context=context,
            output_file=f"src/agents/simulations/{now}/movement.json",
        )

    def generate_post_task(self, agent, context, callback_function) -> Task:
        return Task(
            config=self.tasks_config["generate_post"],
            agent=agent,
            context=context,
            output_file=f"src/agents/simulations/{now}/generate_post.md",
            callback=callback_function
        )

    def marketing_requirements_task(self, agent, context) -> Task:
        return Task(
            config=self.tasks_config["marketing_requirements"],
            agent=agent,
            context=context,
            output_file=f"src/agents/simulations/{now}/marketing_requirements.md",
        )

    def software_requirements_task(self, agent, context) -> Task:
        return Task(
            config=self.tasks_config["software_requirements"],
            agent=agent,
            context=context,
            output_file=f"src/agents/simulations/{now}/marketing_requirements.md",
        )

    def coding_task(self, agent, context) -> Task:
        return Task(
            config=self.tasks_config["coding"],
            agent=agent,
            context=context,
            output_file=f"src/agents/simulations/{now}/coding_plan.py",
        )