import os
import time
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai import LLM
import logging
import time
import random
import json

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
    SOPHISTICATED MULTI-STAGE MARKETING CAMPAIGN CREW with ITERATIVE QUALITY CONTROL
    🧠 INTELLIGENT WORKFLOW: Multi-stage Create → Analyze → Optimize loops across ALL content
    📝 COMPREHENSIVE CAMPAIGN: Full marketing automation content suite with quality assurance
    💰 COST: ~$4-7 for complete publication-ready campaign with optimization loops
    ⏱️ TIME: 60-90 minutes for complete 10-stage sophisticated campaign generation
    🔄 RETRY STRATEGY:
       - LLM Level: 3x API retries with exponential backoff  
       - Agent Level: 5x iterations with extended timeouts (20-30 min each)
       - Crew Level: 3-hour total execution window for quality optimization
    
    💎 SOPHISTICATED CAMPAIGN WORKFLOW:
       Stage 1: Foundational Research (market intelligence)
       Stage 2: Core Content Iteration (blog: create → analyze → optimize)
       Stage 3: Distribution Content Iteration (social+email: create → analyze → optimize)
       Stage 4: Brand Content Iteration (audio: create → analyze)
       Stage 5: Executive Assembly (comprehensive final report)
    
    🎯 PREMIUM CAMPAIGN FEATURES:
       - Strategic market research with competitor & keyword analysis
       - Iteratively optimized 1500+ word blog posts with SEO excellence
       - Multi-platform social media strategy (LinkedIn, Twitter, Instagram, Facebook)
       - Customer journey email sequence (5 strategic emails)
       - Culturally-resonant audio slogans with voice generation
       - Comprehensive performance analysis and optimization across ALL content
       - Executive-ready campaign assembly with implementation roadmap
    
    🚀 ADVANCED INTELLIGENCE: Quality control loops, strategic optimization, comprehensive analysis
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
    def blog_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_optimization_task'],
            agent=self.content_creator(),
            expected_output="Fully optimized blog post implementing all strategic recommendations."
        )

    @task
    def distribution_content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['distribution_content_creation_task'],
            agent=self.content_creator(),
            expected_output="Two comprehensive files: posts_v1.md with 4 platform-optimized social media posts and email-sequence_v1.md with complete 5-email customer journey sequence."
        )

    @task
    def distribution_content_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['distribution_content_analysis_task'],
            agent=self.performance_analyst(),
            expected_output="Comprehensive strategic analysis with prioritized optimization recommendations for distribution content improvement."
        )

    @task
    def distribution_content_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['distribution_content_optimization_task'],
            agent=self.content_creator(),
            expected_output="Two fully optimized files implementing all strategic recommendations: posts_final.md and email-sequence_final.md."
        )

    @task
    def audio_slogan_task(self) -> Task:
        return Task(
            config=self.tasks_config['audio_slogan_task'],
            agent=self.brand_voice_specialist(),
            expected_output="5 culturally-resonant Hindi slogans with professional audio generation of the most impactful slogan."
        )

    @task
    def audio_slogan_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['audio_slogan_analysis_task'],
            agent=self.performance_analyst(),
            expected_output="Detailed analysis of slogan effectiveness with strategic recommendations for optimization and market deployment."
        )

    @task
    def final_report_assembly_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_report_assembly_task'],
            agent=self.campaign_manager(),
            expected_output="A comprehensive, executive-ready campaign report showcasing the complete optimized marketing campaign."
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
        global CAMPAIGN_STATUS
        
        # Get task and agent information
        task_name = task_output.task.name if hasattr(task_output, 'task') and hasattr(task_output.task, 'name') else "Unknown task"
        agent_name = task_output.task.agent.role if (hasattr(task_output, 'task') and 
                                                    hasattr(task_output.task, 'agent') and 
                                                    hasattr(task_output.task.agent, 'role')) else "Unknown agent"
        
        # Get user-friendly names
        friendly_task_name = self.task_descriptions.get(task_name, task_name)
        friendly_agent_name = self.agent_descriptions.get(agent_name, agent_name)
        
        # Update status
        CAMPAIGN_STATUS["current_task"] = friendly_task_name
        CAMPAIGN_STATUS["current_agent"] = friendly_agent_name
        CAMPAIGN_STATUS["task_status"] = "completed"
        CAMPAIGN_STATUS["completed_tasks"].append(friendly_task_name)
        CAMPAIGN_STATUS["progress"] = min(100, int((len(CAMPAIGN_STATUS["completed_tasks"]) / CAMPAIGN_STATUS["total_tasks"]) * 100))
        CAMPAIGN_STATUS["last_update"] = time.time()
        
        # Calculate estimated completion time
        elapsed_time = CAMPAIGN_STATUS["last_update"] - CAMPAIGN_STATUS["start_time"]
        if CAMPAIGN_STATUS["progress"] > 0:
            total_estimated_time = (elapsed_time / CAMPAIGN_STATUS["progress"]) * 100
            remaining_time = total_estimated_time - elapsed_time
            CAMPAIGN_STATUS["estimated_completion"] = remaining_time
        
        # Save status to file for potential recovery
        try:
            with open("campaign_status.json", "w") as f:
                json.dump(CAMPAIGN_STATUS, f)
        except Exception as e:
            print(f"Error saving campaign status: {str(e)}")
        
        print(f"✅ Task completed: {friendly_task_name} by {friendly_agent_name}")
        print(f"📊 Progress: {CAMPAIGN_STATUS['progress']}% complete")
        
        time.sleep(5)
        
        # Handle market research task specific logic
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
        print("🧠 SOPHISTICATED MULTI-STAGE CAMPAIGN: 10-task iterative quality control workflow")
        print("📝 INTELLIGENT CAMPAIGN: Research → Blog Loop → Distribution Loop → Audio Loop → Assembly")
        print("🔄 QUALITY-OPTIMIZED: Create → Analyze → Optimize loops across ALL content types")
        print("💎 Target: Premium campaign with comprehensive optimization, ~60-90 min runtime")
        return Crew(
            agents=[
                self.market_strategist(),
                self.content_creator(),
                self.performance_analyst(),
                self.brand_voice_specialist(),
                self.campaign_manager()
            ],
            tasks=[
                # Stage 1: Foundational Research
                self.market_research_task(),
                
                # Stage 2: Core Content Iteration (Blog)
                self.blog_creation_task(),
                self.blog_analysis_task(),
                self.blog_optimization_task(),
                
                # Stage 3: Distribution Content Creation & Iteration
                self.distribution_content_creation_task(),
                self.distribution_content_analysis_task(),
                self.distribution_content_optimization_task(),
                
                # Stage 4: Brand Content Creation & Iteration
                self.audio_slogan_task(),
                self.audio_slogan_analysis_task(),
                
                # Stage 5: Final Assembly & Review
                self.final_report_assembly_task()
            ],
            process=Process.sequential,
            verbose=True,
            max_rpm=30,
            full_output=True,
            max_execution_time=10800,
            share_crew=False,
            output_log_file="crew_execution.log"
        )
