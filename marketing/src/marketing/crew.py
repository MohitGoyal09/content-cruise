from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import (
    SerperDevTool,
    ScrapeWebsiteTool, 
    FileReadTool,
    FileWriterTool
)
from .tools.analytics_tool import AnalyticsTool
from crewai.tools import BaseTool
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini LLM
gemini_llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

@CrewBase
class Marketing():
    """Marketing crew for content creation and optimization workflow"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def campaign_manager(self) -> Agent:
        """Campaign Manager agent that coordinates the entire workflow"""
        return Agent(
            config=self.agents_config['campaign_manager'],
            llm=gemini_llm,
            verbose=True
        )

    @agent
    def market_strategist(self) -> Agent:
        """Market Strategist agent with research tools"""
        return Agent(
            config=self.agents_config['market_strategist'],
            tools=[
                SerperDevTool(),  # For web search
                ScrapeWebsiteTool()  # For scraping website content
            ],
            llm=gemini_llm,
            verbose=True
        )

    @agent
    def content_creator(self) -> Agent:
        """Content Creator agent with writing and SEO tools"""
        return Agent(
            config=self.agents_config['content_creator'],
            tools=[
                SerperDevTool(),  # For fact-checking and research during content creation
                FileReadTool(),   # To read research findings and strategic brief
                FileWriterTool()   # To save draft content
            ],
            llm=gemini_llm,
            verbose=True
        )

    @agent
    def review_agent(self) -> Agent:
        """Review and Polish agent with quality checking tools"""
        return Agent(
            config=self.agents_config['review_agent'],
            tools=[
                FileReadTool(),  # To read content for review
                FileWriterTool()  # To save reviewed content
            ],
            llm=gemini_llm,
            verbose=True
        )

    @agent
    def content_director(self) -> Agent:
        """Content Director agent for formatting and distribution"""
        return Agent(
            config=self.agents_config['content_director'],
            tools=[
                FileReadTool(),  # To read final content
                FileWriterTool(),  # To save formatted report
                ScrapeWebsiteTool()  # To check formatting standards on target platforms
            ],
            llm=gemini_llm,
            verbose=True
        )

    @agent
    def performance_agent(self) -> Agent:
        """Performance Analysis agent with analytics tools"""
        return Agent(
            config=self.agents_config['performance_agent'],
            tools=[
                FileReadTool(),   # To read published content
                FileWriterTool(),  # To save performance reports
                SerperDevTool(),   # To research industry benchmarks
                AnalyticsTool()    # To generate performance analytics
            ],
            llm=gemini_llm,
            verbose=True
        )

    @task
    def campaign_management_task(self) -> Task:
        """Overall campaign management task"""
        return Task(
            config=self.tasks_config['campaign_management_task']
        )

    @task
    def market_research_task(self) -> Task:
        """Market research and strategy task"""
        return Task(
            config=self.tasks_config['market_research_task']
        )

    @task
    def content_creation_task(self) -> Task:
        """Content creation task"""
        return Task(
            config=self.tasks_config['content_creation_task']
        )

    @task
    def content_review_task(self) -> Task:
        """Content review and polish task"""
        return Task(
            config=self.tasks_config['content_review_task']
        )

    @task
    def report_formatting_task(self) -> Task:
        """Report formatting and distribution task"""
        return Task(
            config=self.tasks_config['report_formatting_task']
        )

    @task
    def performance_analysis_task(self) -> Task:
        """Performance analysis and optimization task"""
        return Task(
            config=self.tasks_config['performance_analysis_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Marketing workflow crew"""
        return Crew(
            agents=[self.market_strategist(), self.content_creator(), 
                   self.review_agent(), self.content_director(), self.performance_agent()],
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=self.campaign_manager()
        )
