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

# Global campaign status tracking
CAMPAIGN_STATUS = {
    "current_task": "Initializing",
    "current_agent": "System",
    "task_status": "pending",
    "completed_tasks": [],
    "progress": 0,
    "total_tasks": 10, 
    "start_time": 0,
    "last_update": 0,
    "estimated_completion": 0
}

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
    
    # Task and Agent friendly names for UI display
    task_descriptions = {
        'market_research_task': 'Market Research & Intelligence',
        'blog_creation_task': 'Blog Content Creation',
        'blog_analysis_task': 'Blog Performance Analysis',
        'blog_optimization_task': 'Blog Content Optimization',
        'distribution_content_creation_task': 'Distribution Content Creation',
        'distribution_content_analysis_task': 'Distribution Content Analysis',
        'distribution_content_optimization_task': 'Distribution Content Optimization',
        'audio_slogan_task': 'Audio Slogan Creation',
        'audio_slogan_analysis_task': 'Audio Slogan Analysis',
        'final_report_assembly_task': 'Final Campaign Assembly'
    }
    
    agent_descriptions = {
        'Senior Market Intelligence Director & Competitive Strategy Expert': 'Market Strategist',
        'Expert Content Strategist & Performance-Driven Creative Director': 'Content Creator',
        'Senior Performance Intelligence Director & Growth Optimization Expert': 'Performance Analyst',
        'Brand Psychology Expert & Creative Innovation Director': 'Brand Voice Specialist',
        'Senior Campaign Director & Strategic Content Orchestrator': 'Campaign Manager'
    }
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
            max_iterations=10,
            max_execution_time=2400,
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
            expected_output="MANDATORY: 3 separate markdown files MUST be created: competitors.md, keywords.md, audience.md in market_research folder",
            description="CRITICAL: Create exactly 3 files using File Writer Tool. Task fails if any file missing. Do NOT create blog content."
        )

    @task
    def blog_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_creation_task'],
            agent=self.content_creator(),
            expected_output="Complete 1500-2000 word blog post ready for publishing. NO market research content included.",
            description="BLOG CONTENT ONLY: Create ONE blog post file. Do NOT create market research content. Do NOT mix blog with research."
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
            expected_output="MANDATORY: 2 files MUST be created: posts_v1.md in social-media folder AND email-sequence_v1.md in emails folder",
            description="CRITICAL: Create exactly 2 files using File Writer Tool. Task fails if any file missing."
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
            expected_output="MANDATORY: 1 file MUST be created: slogans.md in audio folder AND audio file generated",
            description="CRITICAL: Create slogans.md file using File Writer Tool AND generate audio using Voice Generation Tool"
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

    def _task_start_callback(self, task):
        """Callback when a task starts"""
        global CAMPAIGN_STATUS
        
        print(f"🚀 TASK STARTED DEBUG:")
        print(f"   Task object: {task}")
        print(f"   Task type: {type(task)}")
        print(f"   Task dir: {dir(task)}")
        
        task_name = "Unknown task"
        agent_name = "Unknown agent"
        
        try:
            # Get task method name from the stack trace or attributes
            import inspect
            frame = inspect.currentframe()
            caller_frame = frame.f_back
            caller_name = caller_frame.f_code.co_name
            print(f"   Caller: {caller_name}")
            
            # Try to get task ID or description
            if hasattr(task, 'id'):
                print(f"   Task ID: {task.id}")
            if hasattr(task, 'description'):
                desc = str(task.description)
                print(f"   Task Description: {desc[:100]}...")
                
                # Map based on description content
                if "market research" in desc.lower() or "competitors" in desc.lower():
                    task_name = "market_research_task"
                elif "blog_creation" in desc.lower() and "create" in desc.lower():
                    task_name = "blog_creation_task"
                elif "blog_analysis" in desc.lower() or "blog" in desc.lower() and "analysis" in desc.lower():
                    task_name = "blog_analysis_task"
                elif "blog_optimization" in desc.lower() or "blog" in desc.lower() and "optimization" in desc.lower():
                    task_name = "blog_optimization_task"
                elif "distribution_content_creation" in desc.lower() or ("distribution" in desc.lower() and "creation" in desc.lower()):
                    task_name = "distribution_content_creation_task"
                elif "distribution_content_analysis" in desc.lower() or ("distribution" in desc.lower() and "analysis" in desc.lower()):
                    task_name = "distribution_content_analysis_task"
                elif "distribution_content_optimization" in desc.lower() or ("distribution" in desc.lower() and "optimization" in desc.lower()):
                    task_name = "distribution_content_optimization_task"
                elif "audio" in desc.lower() and "slogan" in desc.lower() and "analysis" not in desc.lower():
                    task_name = "audio_slogan_task"
                elif "audio" in desc.lower() and "analysis" in desc.lower():
                    task_name = "audio_slogan_analysis_task"
                elif "final_report" in desc.lower() or "campaign report" in desc.lower():
                    task_name = "final_report_assembly_task"
                    
            # Try to get agent info
            if hasattr(task, 'agent'):
                if hasattr(task.agent, 'role'):
                    agent_name = task.agent.role
                elif hasattr(task.agent, 'name'):
                    agent_name = task.agent.name
                elif hasattr(task.agent, '_name'):
                    agent_name = task.agent._name
                print(f"   Agent: {agent_name}")
                
        except Exception as e:
            print(f"   Error in task start callback: {str(e)}")
            
        # Get user-friendly names
        friendly_task_name = self.task_descriptions.get(task_name, task_name)
        friendly_agent_name = self.agent_descriptions.get(agent_name, agent_name)
        
        print(f"   Final mapping: {task_name} -> {friendly_task_name}")
        print(f"   Agent mapping: {agent_name} -> {friendly_agent_name}")
        
        # Update status with task starting
        CAMPAIGN_STATUS["current_task"] = friendly_task_name
        CAMPAIGN_STATUS["current_agent"] = friendly_agent_name
        CAMPAIGN_STATUS["task_status"] = "in_progress"
        CAMPAIGN_STATUS["last_update"] = time.time()
        
        print(f"🚀 Task started: {friendly_task_name} by {friendly_agent_name}")
        
    def _task_callback(self, task_output):
        global CAMPAIGN_STATUS
        
        print(f"✅ TASK COMPLETED DEBUG:")
        print(f"   Task output: {task_output}")
        print(f"   Task output type: {type(task_output)}")
        print(f"   Task output dir: {dir(task_output)}")
        
        # Get task and agent information with better error handling
        task_name = "Unknown task"
        agent_name = "Unknown agent"
        
        try:
            # Try multiple ways to get the task name
            if hasattr(task_output, 'task'):
                print(f"   Has task: {task_output.task}")
                if hasattr(task_output.task, 'name'):
                    task_name = task_output.task.name
                    print(f"   Task name: {task_name}")
                elif hasattr(task_output.task, 'description'):
                    # Extract task name from description if available
                    desc = str(task_output.task.description)
                    print(f"   Task description: {desc[:100]}...")
                    
                    if "market research" in desc.lower() or "competitors" in desc.lower():
                        task_name = "market_research_task"
                    elif "blog_creation" in desc.lower() and "create" in desc.lower():
                        task_name = "blog_creation_task"
                    elif "blog_analysis" in desc.lower() or "blog" in desc.lower() and "analysis" in desc.lower():
                        task_name = "blog_analysis_task"
                    elif "blog_optimization" in desc.lower() or "blog" in desc.lower() and "optimization" in desc.lower():
                        task_name = "blog_optimization_task"
                    elif "distribution_content_creation" in desc.lower() or ("distribution" in desc.lower() and "creation" in desc.lower()):
                        task_name = "distribution_content_creation_task"
                    elif "distribution_content_analysis" in desc.lower() or ("distribution" in desc.lower() and "analysis" in desc.lower()):
                        task_name = "distribution_content_analysis_task"
                    elif "distribution_content_optimization" in desc.lower() or ("distribution" in desc.lower() and "optimization" in desc.lower()):
                        task_name = "distribution_content_optimization_task"
                    elif "audio" in desc.lower() and "slogan" in desc.lower() and "analysis" not in desc.lower():
                        task_name = "audio_slogan_task"
                    elif "audio" in desc.lower() and "analysis" in desc.lower():
                        task_name = "audio_slogan_analysis_task"
                    elif "final_report" in desc.lower() or "campaign report" in desc.lower():
                        task_name = "final_report_assembly_task"
                        
                # Try to get agent name
                if hasattr(task_output.task, 'agent'):
                    print(f"   Has agent: {task_output.task.agent}")
                    if hasattr(task_output.task.agent, 'role'):
                        agent_name = task_output.task.agent.role
                        print(f"   Agent role: {agent_name}")
                    elif hasattr(task_output.task.agent, 'name'):
                        agent_name = task_output.task.agent.name
                        print(f"   Agent name: {agent_name}")
                        
        except Exception as e:
            print(f"   Error getting task/agent info: {str(e)}")
            
        print(f"   Raw task name: {task_name}")
        print(f"   Raw agent name: {agent_name}")
        
        # Get user-friendly names
        friendly_task_name = self.task_descriptions.get(task_name, task_name)
        friendly_agent_name = self.agent_descriptions.get(agent_name, agent_name)
        
        print(f"   Friendly task: {friendly_task_name}")
        print(f"   Friendly agent: {friendly_agent_name}")
        
        # Update status
        CAMPAIGN_STATUS["current_task"] = friendly_task_name
        CAMPAIGN_STATUS["current_agent"] = friendly_agent_name
        CAMPAIGN_STATUS["task_status"] = "completed"
        CAMPAIGN_STATUS["completed_tasks"].append(friendly_task_name)
        CAMPAIGN_STATUS["progress"] = min(100, int((len(CAMPAIGN_STATUS["completed_tasks"]) / CAMPAIGN_STATUS["total_tasks"]) * 100))
        CAMPAIGN_STATUS["last_update"] = time.time()
        
        print(f"   Updated CAMPAIGN_STATUS: {CAMPAIGN_STATUS}")
        
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
        
        # Validate task completion
        campaign_name = os.getenv("CAMPAIGN_NAME", "default-campaign")
        validation_passed = self._validate_task_completion(task_name, campaign_name)
        
        if not validation_passed:
            print(f"❌ CRITICAL ERROR: Task {friendly_task_name} did not create required files!")
            print(f"🔄 This may cause subsequent tasks to fail!")
        
        time.sleep(5)
        
        return task_output

    def _step_callback(self, step_output):
        """Callback for individual steps within tasks"""
        global CAMPAIGN_STATUS
        
        print(f"📞 STEP CALLBACK TRIGGERED!")
        print(f"   Step output type: {type(step_output)}")
        print(f"   Current CAMPAIGN_STATUS before update: {CAMPAIGN_STATUS}")
        
        try:
            current_time = time.time()
            
            # Only update timestamp and keep existing task/agent values from task callbacks
            # Don't override the current_task and current_agent set by task callbacks
            CAMPAIGN_STATUS["last_update"] = current_time
            if CAMPAIGN_STATUS.get("task_status") != "completed":
                CAMPAIGN_STATUS["task_status"] = "in_progress"
            
            # Increment progress slightly for activity indication (but don't exceed task callback values)
            current_progress = CAMPAIGN_STATUS.get("progress", 0)
            if current_progress < 95:  # Don't exceed 95% until tasks complete
                CAMPAIGN_STATUS["progress"] = min(current_progress + 1, 95)
            
            print(f"   STEP UPDATE - Task: {CAMPAIGN_STATUS.get('current_task', 'Unknown task')}")
            print(f"   STEP UPDATE - Agent: {CAMPAIGN_STATUS.get('current_agent', 'Unknown agent')}")
            print(f"   STEP UPDATE - Progress: {CAMPAIGN_STATUS['progress']}%")
            
            # Save to JSON file immediately for backup
            try:
                with open("campaign_status.json", "w") as f:
                    json.dump(CAMPAIGN_STATUS, f)
                print(f"   ✅ Saved status to JSON file")
            except Exception as json_error:
                print(f"   ❌ Error saving JSON: {str(json_error)}")
            
            # Use current CAMPAIGN_STATUS for display instead of trying to extract from step_output
            agent_role = CAMPAIGN_STATUS.get("current_agent", "Unknown agent")
            action = "Working..."
            
            # Try to get action/description from step_output
            if hasattr(step_output, 'action'):
                action = str(step_output.action)
            elif hasattr(step_output, 'description'):
                action = str(step_output.description)
            elif hasattr(step_output, 'tool'):
                action = f"Using {step_output.tool}"
            elif hasattr(step_output, 'log'):
                action = str(step_output.log)[:50] + "..."
            
            # Enhanced debug info about step_output structure
            print(f"   Step output attributes: {[attr for attr in dir(step_output) if not attr.startswith('_')]}")
            
            # Try to extract more meaningful action information
            if hasattr(step_output, 'tool_input'):
                tool_input = step_output.tool_input
                if isinstance(tool_input, dict):
                    if 'tool_name' in tool_input:
                        action = f"Using {tool_input['tool_name']}"
                    elif 'file_path' in tool_input:
                        action = f"Writing to {tool_input['file_path']}"
                    elif 'query' in tool_input:
                        action = f"Researching: {tool_input['query'][:30]}..."
            
            print(f"🔄 Step: {agent_role} - {action}")
            
        except Exception as e:
            print(f"Error in step callback: {str(e)}")
            
        return step_output

    def _validate_task_completion(self, task_name, campaign_name):
        """Validate that required files were created for each task"""
        validation_rules = {
            "market_research": {
                "files": ["competitors.md", "keywords.md", "audience.md"],
                "path": f"content/{campaign_name}/market_research/"
            },
            "blog_creation": {
                "files": ["ai-marketing-guide.md"],
                "path": f"content/{campaign_name}/blogs/"
            },
            "blog_analysis": {
                "files": ["strategic-optimization.md"],
                "path": f"content/{campaign_name}/analysis/"
            },
            "blog_optimization": {
                "files": ["optimized-ai-marketing-guide.md"],
                "path": f"content/{campaign_name}/blogs/"
            },
            "distribution_content_creation": {
                "files": ["posts_v1.md", "email-sequence_v1.md"],
                "path": [f"content/{campaign_name}/social-media/", f"content/{campaign_name}/emails/"]
            },
            "distribution_content_analysis": {
                "files": ["distribution_feedback.md"],
                "path": f"content/{campaign_name}/analysis/"
            },
            "distribution_content_optimization": {
                "files": ["posts_final.md", "email-sequence_final.md"],
                "path": [f"content/{campaign_name}/social-media/", f"content/{campaign_name}/emails/"]
            },
            "audio_slogan": {
                "files": ["slogans.md"],
                "path": f"content/{campaign_name}/audio/"
            },
            "audio_slogan_analysis": {
                "files": ["audio_slogan_feedback.md"],
                "path": f"content/{campaign_name}/analysis/"
            },
            "final_report_assembly": {
                "files": ["FINAL_CAMPAIGN_REPORT.md"],
                "path": f"content/{campaign_name}/"
            }
        }
        
        for rule_name, rule in validation_rules.items():
            if rule_name in task_name.lower():
                files = rule["files"]
                paths = rule["path"] if isinstance(rule["path"], list) else [rule["path"]]
                
                for i, file_name in enumerate(files):
                    path = paths[i] if i < len(paths) else paths[0]
                    full_path = os.path.join(path, file_name)
                    
                    if not os.path.exists(full_path):
                        print(f"⚠️ VALIDATION FAILED: Missing file {full_path}")
                        return False
                    else:
                        file_size = os.path.getsize(full_path)
                        if file_size < 100:  # Minimum file size check
                            print(f"⚠️ VALIDATION FAILED: File too small {full_path} ({file_size} bytes)")
                            return False
                        else:
                            print(f"✅ VALIDATION PASSED: {full_path} ({file_size} bytes)")
                
                return True
        
        return True  # No specific validation rule found

    @crew
    def crew(self) -> Crew:
        global CAMPAIGN_STATUS
        
        # Initialize campaign status
        CAMPAIGN_STATUS["start_time"] = time.time()
        CAMPAIGN_STATUS["last_update"] = time.time()
        CAMPAIGN_STATUS["completed_tasks"] = []
        CAMPAIGN_STATUS["progress"] = 0
        CAMPAIGN_STATUS["current_task"] = "Initializing"
        CAMPAIGN_STATUS["current_agent"] = "System"
        CAMPAIGN_STATUS["task_status"] = "pending"
        
        print("🧠 SOPHISTICATED MULTI-STAGE CAMPAIGN: 10-task iterative quality control workflow")
        print("📝 INTELLIGENT CAMPAIGN: Research → Blog Loop → Distribution Loop → Audio Loop → Assembly")
        print("🔄 QUALITY-OPTIMIZED: Create → Analyze → Optimize loops across ALL content types")
        print("💎 Target: Premium campaign with comprehensive optimization, ~60-90 min runtime")
        # Create tasks with explicit names for better tracking
        market_task = self.market_research_task()
        market_task.name = "market_research_task"
        
        blog_create_task = self.blog_creation_task()
        blog_create_task.name = "blog_creation_task"
        
        blog_analysis_task = self.blog_analysis_task()
        blog_analysis_task.name = "blog_analysis_task"
        
        blog_opt_task = self.blog_optimization_task()
        blog_opt_task.name = "blog_optimization_task"
        
        dist_create_task = self.distribution_content_creation_task()
        dist_create_task.name = "distribution_content_creation_task"
        
        dist_analysis_task = self.distribution_content_analysis_task()
        dist_analysis_task.name = "distribution_content_analysis_task"
        
        dist_opt_task = self.distribution_content_optimization_task()
        dist_opt_task.name = "distribution_content_optimization_task"
        
        audio_task = self.audio_slogan_task()
        audio_task.name = "audio_slogan_task"
        
        audio_analysis_task = self.audio_slogan_analysis_task()
        audio_analysis_task.name = "audio_slogan_analysis_task"
        
        final_task = self.final_report_assembly_task()
        final_task.name = "final_report_assembly_task"
        
        return Crew(
            agents=[
                self.market_strategist(),
                self.content_creator(),
                self.performance_analyst(),
                self.brand_voice_specialist(),
                self.campaign_manager()
            ],
            tasks=[
                # Stage 1: Foundational Research - MUST CREATE 3 FILES
                market_task,
                
                # Stage 2: Core Content Iteration (Blog) - MUST CREATE 1 BLOG + 1 ANALYSIS + 1 OPTIMIZED BLOG
                blog_create_task,
                blog_analysis_task,
                blog_opt_task,
                
                # Stage 3: Distribution Content Creation & Iteration - MUST CREATE 2 FILES + 1 ANALYSIS + 2 OPTIMIZED FILES
                dist_create_task,
                dist_analysis_task,
                dist_opt_task,
                
                # Stage 4: Brand Content Creation & Iteration - MUST CREATE 1 AUDIO + 1 ANALYSIS
                audio_task,
                audio_analysis_task,
                
                # Stage 5: Final Assembly & Review - MUST CREATE 1 FINAL REPORT
                final_task
            ],
            process=Process.sequential,
            verbose=True,
            max_rpm=20,
            full_output=True,
            max_execution_time=14400,
            share_crew=False,
            output_log_file="crew_execution.log",
            task_callback=self._task_callback,
            step_callback=self._step_callback
        )
