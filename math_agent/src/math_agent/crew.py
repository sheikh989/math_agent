from crewai import Crew, Process
from pathlib import Path
import yaml
from crewai import Agent, Task
from .tools.question_to_json_tool import question_auto_extractor_tool,json_structuring_tool,generic_math_solver_tool,visual_formatter_tool

class MathCrew:
    def __init__(self):
        base = Path(__file__).parent

        with open(base / "config" / "agents.yaml") as f:
            agents_config = yaml.safe_load(f)

        with open(base / "config" / "tasks.yaml") as f:
            tasks_config = yaml.safe_load(f)

        

        agents = {}
        for name, cfg in agents_config.items():
            tools = {
                "question_auto_extractor_tool": question_auto_extractor_tool,
                "json_structuring_tool": json_structuring_tool,
                "generic_math_solver_tool": generic_math_solver_tool,
                "visual_formatter_tool": visual_formatter_tool,
            }
            agent_tools = [tools[t] for t in cfg.get("tools", [])]

            agents[name] = Agent(
                **{
                    "role": cfg["role"],
                    "goal": cfg["goal"],
                    "backstory": cfg["backstory"],
                    "verbose": cfg["verbose"],
                    "memory": cfg["memory"],
                    "allow_delegation": cfg["allow_delegation"],
                    "llm": cfg["llm"],
                    "tools": agent_tools
                }
            )

        tasks = []
        for task_name, cfg in tasks_config.items():
            tasks.append(
                Task(
                    description=cfg["description"],
                    expected_output=cfg["expected_output"],
                    agent=agents[cfg["agent"]],
                    tools=[],
                )
            )

        self.crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
        )

    def kickoff(self, question: str):
        return self.crew.kickoff({"question": question})
