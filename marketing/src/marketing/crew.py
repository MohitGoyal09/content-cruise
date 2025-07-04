import os
import time
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileWriterTool, DirectoryReadTool, ScrapeWebsiteTool
from crewai import LLM
import logging
import time
import random

logging.basicConfig(level=logging.WARNING)

from src.marketing.tools.voice_generation import VoiceGenerationTool
from src.marketing.tools.analytics_tool import AnalyticsTool
from src.marketing.tools.competitor_analysis_tool import CompetitorAnalysisTool
from src.marketing.tools.seo_tool import SEOAnalysisTool
from src.marketing.tools.social_media_tool import SocialMediaTool
from src.marketing.tools.fixed_file_read_tool import FixedFileReadTool
from src.marketing.tools.fixed_file_writer_tool import FixedFileWriterTool

mistral_llm = LLM(
    model="mistral/mistral-small-latest",
    temperature=0.1,
    max_tokens=3000,
    timeout=180,
    top_p=1.0,
    max_retries=3,
    num_retries=3
)

gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
    max_tokens=4000,
    timeout=300,
    top_p=0.9,
    max_retries=5,
    num_retries=5,
    retry_delay=60,
    fallback_models=["gemini/gemini-1.5-flash-001"]
)

@CrewBase
class Marketing():
    """
    COMPLETE CONTENT MARKETING CAMPAIGN CREW with ROBUST RETRY LOGIC
    📝 COMPREHENSIVE CAMPAIGN: Full marketing automation content suite
    💰 COST: ~$3-5 for complete publication-ready campaign
    ⏱️ TIME: 45-60 minutes for complete 6-task campaign generation
    🔄 RETRY STRATEGY:
       - LLM Level: 3x API retries with exponential backoff  
       - Agent Level: 5x iterations with extended timeouts (20-30 min each)
       - Crew Level: 2-hour total execution window for quality
    💎 COMPLETE CAMPAIGN FEATURES:
       - Market research with competitor & keyword analysis
       - Full 1200+ word blog posts with SEO optimization
       - Social media content (LinkedIn, Twitter, Instagram)
       - Email marketing sequence (3 complete emails)
       - Professional audio slogans with voice generation
       - Performance analysis and optimization recommendations
    🚀 RELIABILITY: Verbose logging, auto-recovery, comprehensive error handling
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def campaign_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['campaign_manager'],
            tools=[FixedFileWriterTool(), FixedFileReadTool()],
            llm=mistral_llm,
            verbose=True,
            max_iterations=5,
            max_execution_time=1200,
            max_retry_limit=3
        )

    @agent
    def market_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['market_strategist'],
            tools=[SerperDevTool(), FixedFileWriterTool()],
            llm=mistral_llm,
            verbose=True,
            max_iterations=8,
            max_execution_time=1800,
            allow_delegation=False,
            max_retry_limit=5
        )

    @agent
    def content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creator'],
            tools=[FixedFileReadTool(), FixedFileWriterTool()],
            llm=gemini_llm,
            verbose=True,
            max_iterations=3,
            max_execution_time=2400,
            allow_delegation=False,
            max_retry_limit=5
        )

    @agent
    def performance_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['performance_analyst'],
            tools=[FixedFileReadTool(), FixedFileWriterTool()],
            llm=mistral_llm,
            verbose=True,
            max_iterations=5,
            max_execution_time=1200,
            allow_delegation=False,
            max_retry_limit=3
        )

    @agent
    def brand_voice_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['brand_voice_specialist'],
            tools=[FixedFileWriterTool(), VoiceGenerationTool()],
            llm=gemini_llm,
            verbose=True,
            max_iterations=3,
            max_execution_time=1800,
            allow_delegation=False,
            max_retry_limit=5
        )

    @task
    def market_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_research_task'],
            agent=self.market_strategist(),
            expected_output="3 concise markdown files with essential research data completed in under 3 minutes.",
            description="CRITICAL TASK: Create market research files for competitors, keywords, and audience analysis."
        )

    @task
    def blog_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_creation_task'],
            agent=self.content_creator(),
            expected_output="Complete 1200-word blog post ready for publishing in under 5 minutes."
        )

    @task
    def blog_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_analysis_task'],
            agent=self.performance_analyst(),
            expected_output="Brief improvement recommendations completed in under 2 minutes."
        )

    @task
    def social_media_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['social_media_creation_task'],
            agent=self.content_creator(),
            expected_output="A professionally formatted markdown file with 3 high-quality, engaging social media posts."
        )

    @task
    def email_marketing_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_marketing_task'],
            agent=self.content_creator(),
            expected_output="3 ready-to-send marketing emails with subject lines and full content."
        )

    @task
    def audio_slogan_task(self) -> Task:
        return Task(
            config=self.tasks_config['audio_slogan_task'],
            agent=self.brand_voice_specialist(),
            expected_output="A text file with 2 high-quality slogan options and an audio file."
        )

    def _handle_gemini_rate_limit(self, retry_count=0, max_retries=5):
        if retry_count >= max_retries:
            print(f"❌ Max retries ({max_retries}) reached for Gemini API")
            return False
        base_delay = 60
        delay = base_delay * (2 ** retry_count) + random.uniform(0, 10)
        print(f"⏳ Gemini API rate limit hit. Waiting {delay:.0f} seconds before retry {retry_count + 1}/{max_retries}...")
        time.sleep(delay)
        return True

    def _task_callback(self, task_output):
        task_name = task_output.task.name if hasattr(task_output, 'task') and hasattr(task_output.task, 'name') else "Unknown task"
        print(f"✅ Task completed: {task_name}")
        time.sleep(5)
        if "market_research" in task_name.lower():
            campaign_name = os.getenv("CAMPAIGN_NAME")
            if not campaign_name or campaign_name.strip() in ["", "None", "null"]:
                from datetime import datetime
                current_year = datetime.now().year
                campaign_name = f"fallback-campaign-{current_year}-{int(time.time())}"
                os.environ["CAMPAIGN_NAME"] = campaign_name
                print(f"⚠️ Using fallback campaign name: {campaign_name}")
            research_dir = f"content/{campaign_name}/market_research"
            if not os.path.exists(research_dir):
                os.makedirs(research_dir, exist_ok=True)
                print(f"⚠️ Created missing directory: {research_dir}")
            expected_files = ["competitors.md", "keywords.md", "audience.md"]
            missing_files = []
            for file in expected_files:
                file_path = os.path.join(research_dir, file)
                if not os.path.exists(file_path):
                    missing_files.append(file)
            if missing_files:
                print(f"⚠️ Missing market research files: {', '.join(missing_files)}")
                print("⚠️ Creating placeholder files to be regenerated...")
                for file in missing_files:
                    file_path = os.path.join(research_dir, file)
                    with open(file_path, "w") as f:
                        f.write(f"# {file.replace('.md', '').title()} Research\n\n")
                        f.write("This file needs to be regenerated.\n")
        return task_output

    @crew
    def crew(self) -> Crew:
        print("🚀 COMPLETE MARKETING CAMPAIGN: 6-task comprehensive content generation")
        print("📝 FULL CAMPAIGN: Market research + Blog + Social + Email + Audio + Analysis")
        print("🔄 RETRY-ENABLED: Auto-recovery on API failures, 5x iterations per agent")
        print("💎 Target: Complete marketing campaign, ~45-60 min runtime")
        return Crew(
            agents=[
                self.market_strategist(),
                self.content_creator(),
                self.performance_analyst(),
                self.brand_voice_specialist()
            ],
            tasks=[
                self.market_research_task(),
                self.blog_creation_task(),
                self.blog_analysis_task(),
                self.social_media_creation_task(),
                self.email_marketing_task(),
                self.audio_slogan_task()
            ],
            process=Process.sequential,
            verbose=True,
            max_rpm=30,
            full_output=True,
            step_callback=self._task_callback,
            max_execution_time=10800,
            share_crew=False,
            output_log_file="crew_execution.log"
        )
