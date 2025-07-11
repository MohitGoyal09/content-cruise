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
    "total_tasks": 12, 
    "start_time": 0,
    "last_update": 0,
    "estimated_completion": 0
}

@CrewBase
class Marketing():
    """
    SOPHISTICATED MULTI-STAGE MARKETING CAMPAIGN CREW with ITERATIVE QUALITY CONTROL
    🧠 INTELLIGENT WORKFLOW: Multi-stage Create → Validate → Analyze → Optimize loops across ALL content
    📝 COMPREHENSIVE CAMPAIGN: Full marketing automation content suite with quality assurance
    💰 COST: ~$4-7 for complete publication-ready campaign with optimization loops
    ⏱️ TIME: 60-90 minutes for complete 12-stage sophisticated campaign generation
    🔄 RETRY STRATEGY:
       - LLM Level: 3x API retries with exponential backoff  
       - Agent Level: 5x iterations with extended timeouts (20-30 min each)
       - Crew Level: 3-hour total execution window for quality optimization
    
    💎 SOPHISTICATED CAMPAIGN WORKFLOW:
       Stage 1: Foundational Research (market intelligence)
       Stage 2: Research Validation (placeholder content elimination)
       Stage 3: Core Content Iteration (blog: create → validate → analyze → optimize)
       Stage 4: Distribution Content Iteration (social+email: create → analyze → optimize)
       Stage 5: Brand Content Iteration (audio: create → analyze)
       Stage 6: Executive Assembly (comprehensive final report)
    
    🎯 PREMIUM CAMPAIGN FEATURES:
       - Strategic market research with competitor & keyword analysis
       - Automated validation to eliminate placeholder content and incomplete blogs
       - Iteratively optimized 2000+ word blog posts with SEO excellence
       - Multi-platform social media strategy (LinkedIn, Twitter, Instagram, Facebook)
       - Customer journey email sequence (5 strategic emails)
       - Culturally-resonant audio slogans with voice generation (single best slogan)
       - Comprehensive performance analysis and optimization across ALL content
       - Executive-ready campaign assembly with implementation roadmap
    
    🚀 ADVANCED INTELLIGENCE: Quality control loops, content validation, strategic optimization, comprehensive analysis
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    # Task and Agent friendly names for UI display
    task_descriptions = {
        'market_research_task': 'Market Research & Intelligence',
        'market_research_validation_task': 'Market Research Validation',
        'blog_creation_task': 'Blog Content Creation',
        'blog_validation_task': 'Blog Content Validation',
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
            tools=[SerperDevTool(), FixedFileWriterTool(), FixedFileReadTool()],
            llm=mistral_llm,
            verbose=True,
            max_iterations=10,
            max_execution_time=2400,
            allow_delegation=False,
            max_retry_limit=5,
            system_message="""You are a Senior Market Intelligence Director. Your primary responsibility is conducting thorough market research using ONLY real, verified data.

CRITICAL RULES - TASK FAILS IF VIOLATED:
🚫 NEVER use placeholder content like "Company A", "Keyword 1", "Segment 1", "Description of", etc.
🚫 NEVER create generic templates or example content
🚫 NEVER use vague demographic data like "Age: 25-45", "Gender: all", "Location: global"

✅ REQUIRED APPROACH:
1. SEARCH FIRST: Use Search tool to find real competitors, keywords, and demographic data
2. VERIFY: Ensure all company names, keywords, and data points are real and current
3. DETAILED ANALYSIS: Provide specific market positioning, pricing, and competitive advantages
4. REAL DATA ONLY: Include actual demographic numbers, income ranges, job titles, pain points

EXAMPLES OF REQUIRED QUALITY:
- Competitors: "HubSpot Marketing Hub", "Mailchimp", "ActiveCampaign" with real pricing and features
- Keywords: "AI marketing automation", "small business CRM", "email marketing tools" with search volumes
- Demographics: "Small business owners aged 28-52, average revenue $250K-2M, primarily in retail/services"

🔍 VALIDATION PROCESS:
- All your work will be validated for placeholder content
- If placeholders are found, you'll be asked to research and fix them
- Use web search extensively to gather real market intelligence
- Focus on actionable business data that stakeholders can use immediately

Your research must pass this test: Could someone immediately use this data to make business decisions? If not, research deeper until you have actionable intelligence."""
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
        )

    @task
    def market_research_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_research_validation_task'],
            agent=self.market_strategist(),
            expected_output="Validated and corrected market research files with 100% real data - zero placeholder content",
            description="VALIDATION ONLY: Check and fix market research files for placeholder content. Use web search to replace with real data."
        )

    @task
    def blog_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_creation_task'],
            agent=self.content_creator(),
            expected_output="Complete 2000+ word blog post with all required sections ready for publishing. NO market research content included.",
            description="BLOG CONTENT ONLY: Create ONE complete blog post file with introduction, main body, recommendations, and conclusion."
        )

    @task
    def blog_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_validation_task'],
            agent=self.performance_analyst(),
            expected_output="Validation report confirming blog content completeness or flagging specific deficiencies.",
            description="CRITICAL VALIDATION: Verify blog content completeness - ensure all required sections exist and content is substantial."
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

    def _extract_task_and_agent_info(self, task_or_output):
        """Simple, reliable method to extract task and agent names"""
        task_name = "Unknown task"
        agent_name = "Unknown agent"
        
        # Get the actual task object
        if hasattr(task_or_output, 'task'):
            task = task_or_output.task
        else:
            task = task_or_output
            
        try:
            # Extract task name - prioritize manually set name
            if hasattr(task, 'name') and task.name:
                task_name = task.name
            elif hasattr(task, 'description'):
                # Simple keyword matching for task identification
                desc_lower = str(task.description).lower()
                if "market research" in desc_lower:
                    task_name = "market_research_task"
                elif "blog" in desc_lower and "create" in desc_lower:
                    task_name = "blog_creation_task"
                elif "blog" in desc_lower and "validation" in desc_lower:
                    task_name = "blog_validation_task"
                elif "blog" in desc_lower and "analysis" in desc_lower:
                    task_name = "blog_analysis_task"
                elif "blog" in desc_lower and "optimization" in desc_lower:
                    task_name = "blog_optimization_task"
                elif "distribution" in desc_lower and "creation" in desc_lower:
                    task_name = "distribution_content_creation_task"
                elif "distribution" in desc_lower and "analysis" in desc_lower:
                    task_name = "distribution_content_analysis_task"
                elif "distribution" in desc_lower and "optimization" in desc_lower:
                    task_name = "distribution_content_optimization_task"
                elif "audio" in desc_lower and "slogan" in desc_lower and "analysis" not in desc_lower:
                    task_name = "audio_slogan_task"
                elif "audio" in desc_lower and "analysis" in desc_lower:
                    task_name = "audio_slogan_analysis_task"
                elif "final" in desc_lower and "report" in desc_lower:
                    task_name = "final_report_assembly_task"
                    
            # Extract agent name from agent config
            if hasattr(task, 'agent') and task.agent:
                agent = task.agent
                if hasattr(agent, 'config') and isinstance(agent.config, dict) and 'role' in agent.config:
                    agent_name = agent.config['role']
                elif hasattr(agent, 'role') and agent.role:
                    agent_name = agent.role
                    
        except Exception as e:
            print(f"Debug: Error extracting task/agent info: {e}")
            
        return task_name, agent_name

    def _task_callback(self, task_output):
        """Simplified task completion callback"""
        global CAMPAIGN_STATUS
        
        task_name, agent_name = self._extract_task_and_agent_info(task_output)
        
        # Get user-friendly names
        friendly_task_name = self.task_descriptions.get(task_name, task_name.replace('_', ' ').title())
        friendly_agent_name = self.agent_descriptions.get(agent_name, "Agent")
        
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
        
        # Save status to file
        try:
            with open("campaign_status.json", "w") as f:
                json.dump(CAMPAIGN_STATUS, f)
        except Exception:
            pass
        
        # Clean status update
        print(f"✅ Task completed: {friendly_task_name} by {friendly_agent_name}")
        print(f"📊 Progress: {CAMPAIGN_STATUS['progress']}% complete")
        
        # Validate task completion
        campaign_name = os.getenv("CAMPAIGN_NAME", "default-campaign")
        validation_passed = self._validate_task_completion(task_name, campaign_name)
        
        if not validation_passed:
            print(f"❌ ERROR: Task {friendly_task_name} did not create required files!")
        
        return task_output

    def _step_callback(self, step_output):
        """Simplified step callback with proper agent name"""
        global CAMPAIGN_STATUS
        
        try:
            current_time = time.time()
            last_update = CAMPAIGN_STATUS.get("last_update", 0)
            
            # Throttle updates - only update every 15 seconds to reduce spam
            if current_time - last_update < 15:
                return step_output
                
            # Update timestamp
            CAMPAIGN_STATUS["last_update"] = current_time
            
            # Get agent info from current status
            agent_role = CAMPAIGN_STATUS.get("current_agent", "Working Agent")
            action = "Processing..."
            
            # Try to get more specific action info
            if hasattr(step_output, 'tool') and step_output.tool:
                action = f"Using {step_output.tool}"
            elif hasattr(step_output, 'tool_input') and isinstance(step_output.tool_input, dict):
                if 'file_path' in step_output.tool_input:
                    action = "Writing file"
                elif 'query' in step_output.tool_input:
                    action = "Researching"
            
            # Clean status update
            print(f"🔄 {agent_role}: {action}")
            
        except Exception:
            # Silent error handling
            pass
            
        return step_output

    def _validate_task_completion(self, task_name, campaign_name):
        """Validate that required files were created for each task"""
        validation_rules = {
            "market_research_task": {
                "files": ["competitors.md", "keywords.md", "audience.md"],
                "path": f"content/{campaign_name}/market_research/",
                "content_validation": self._validate_market_research_content
            },
            "market_research_validation_task": {
                "files": ["competitors.md", "keywords.md", "audience.md"],
                "path": f"content/{campaign_name}/market_research/",
                "content_validation": self._validate_market_research_content
            },
            "blog_creation_task": {
                "files": ["ai-marketing-guide.md"],
                "path": f"content/{campaign_name}/blogs/",
                "content_validation": self._validate_blog_file_creation
            },
            "blog_validation_task": {
                "files": ["ai-marketing-guide.md"], 
                "path": f"content/{campaign_name}/blogs/",
                "content_validation": self._validate_blog_content_completeness
            },
            "blog_analysis_task": {
                "files": ["strategic-optimization.md"],
                "path": f"content/{campaign_name}/analysis/"
            },
            "blog_optimization_task": {
                "files": ["optimized-ai-marketing-guide.md"],
                "path": f"content/{campaign_name}/blogs/"
            },
            "distribution_content_creation_task": {
                "files": ["posts_v1.md", "email-sequence_v1.md"],
                "path": [f"content/{campaign_name}/social-media/", f"content/{campaign_name}/emails/"],
                "content_validation": self._validate_social_media_content
            },
            "distribution_content_analysis_task": {
                "files": ["distribution_feedback.md"],
                "path": f"content/{campaign_name}/analysis/"
            },
            "distribution_content_optimization_task": {
                "files": ["posts_final.md", "email-sequence_final.md"],
                "path": [f"content/{campaign_name}/social-media/", f"content/{campaign_name}/emails/"],
                "content_validation": self._validate_social_media_content
            },
            "audio_slogan_task": {
                "files": ["slogans.md"],
                "path": f"content/{campaign_name}/audio/",
                "content_validation": self._validate_hindi_slogans
            },
            "audio_slogan_analysis_task": {
                "files": ["audio_slogan_feedback.md"],
                "path": f"content/{campaign_name}/analysis/"
            },
            "final_report_assembly_task": {
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
                            
                            # Additional content validation if specified
                            if "content_validation" in rule:
                                validation_func = rule["content_validation"]
                                if not validation_func(full_path):
                                    print(f"⚠️ CONTENT VALIDATION FAILED: {full_path}")
                                    return False
                
                return True
        
        return True  # No specific validation rule found

    def _validate_market_research_content(self, file_path):
        """Enhanced validation to prevent placeholder content and ensure real research data"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                content_lower = content.lower()
                
            # Basic content length check
            if len(content) < 200:
                print(f"❌ CONTENT VALIDATION FAILED: Content too short in {file_path} ({len(content)} chars)")
                print("   Market research files should be comprehensive with real data")
                return False
            
            # Strict placeholder detection - these patterns indicate lazy/fake research
            forbidden_patterns = [
                "company a", "company b", "company c", "company d", "company e",
                "competitor a", "competitor b", "competitor c", "competitor d",
                "keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5",
                "segment 1", "segment 2", "segment 3", "primary segment",
                "description of", "example company", "sample keyword",
                "age: 25-45", "gender: all", "location: global", "location: worldwide",
                "demographics:", "psychographics:", "placeholder", "to be determined",
                "tbd", "coming soon", "research pending", "data not available"
            ]
            
            # Check for ANY forbidden placeholder patterns
            for pattern in forbidden_patterns:
                if pattern in content_lower:
                    print(f"❌ PLACEHOLDER CONTENT DETECTED: '{pattern}' found in {file_path}")
                    print(f"   This indicates insufficient research. Real company/keyword names required.")
                    return False
            
            # File-specific validation
            filename = os.path.basename(file_path).lower()
            
            if "competitors" in filename:
                # Check for real company names (proper nouns with context)
                import re
                # Look for patterns like "HubSpot", "Mailchimp", "ActiveCampaign"
                company_patterns = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]*)*\b', content)
                # Filter out common words that aren't company names
                excluded_words = {'Marketing', 'Company', 'Competitor', 'Business', 'Platform', 'Solution', 'Tool', 'Features', 'Pricing', 'Market', 'Position', 'Analysis', 'Direct', 'Indirect', 'Key', 'Strengths', 'Target'}
                real_companies = [word for word in company_patterns if word not in excluded_words and len(word) > 3]
                
                if len(real_companies) < 5:
                    print(f"❌ INSUFFICIENT REAL COMPANIES: Only {len(real_companies)} found in {file_path}")
                    print(f"   Found: {real_companies[:3]}... Need actual company names like 'HubSpot', 'Mailchimp'")
                    return False
                    
            elif "keywords" in filename:
                # Check for specific, quoted keywords or multi-word phrases
                import re
                quoted_keywords = len(re.findall(r'"[^"]+"|\'[^\']+\'', content))
                multi_word_phrases = len(re.findall(r'\b\w+\s+\w+\s+\w+\b', content_lower))
                
                if quoted_keywords < 3 and multi_word_phrases < 8:
                    print(f"❌ INSUFFICIENT SPECIFIC KEYWORDS: Only {quoted_keywords} quoted terms and {multi_word_phrases} phrases in {file_path}")
                    print("   Need specific keywords like 'AI marketing automation', 'small business CRM'")
                    return False
                    
            elif "audience" in filename:
                # Check for specific demographic data (numbers, ranges, specifics)
                import re
                has_age_ranges = bool(re.search(r'\b\d{2}-\d{2}\b', content))
                has_income_data = bool(re.search(r'\$[\d,]+', content))
                has_specific_titles = bool(re.search(r'(owner|manager|director|ceo|founder)', content_lower))
                
                if not (has_age_ranges or has_income_data or has_specific_titles):
                    print(f"❌ INSUFFICIENT DEMOGRAPHIC SPECIFICITY in {file_path}")
                    print("   Need specific data: age ranges, income levels, job titles, etc.")
                    return False
            
            print(f"✅ CONTENT VALIDATION PASSED: {file_path} contains real research data")
            return True
            
        except Exception as e:
            print(f"❌ Error validating content for {file_path}: {e}")
            return False

    def _validate_social_media_content(self, file_path):
        """Validate social media files contain platform-specific content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                content_lower = content.lower()
            
            # Check if posts file contains platform-specific sections
            if "posts_" in file_path:
                required_platforms = ["linkedin", "twitter", "instagram", "facebook"]
                missing_platforms = []
                
                for platform in required_platforms:
                    if platform not in content_lower:
                        missing_platforms.append(platform)
                
                if missing_platforms:
                    print(f"❌ SOCIAL MEDIA VALIDATION FAILED: Missing platforms in {file_path}: {missing_platforms}")
                    print(f"   Social media files must include sections for: LinkedIn, Twitter, Instagram, Facebook")
                    return False
                
                # Check if it's not just blog content
                blog_indicators = ["the night sky has captivated", "ai to the rescue", "conclusion:", "## ai"]
                for indicator in blog_indicators:
                    if indicator in content_lower:
                        print(f"❌ SOCIAL MEDIA VALIDATION FAILED: Blog content found in social media file: {file_path}")
                        print(f"   Social media files should contain platform-specific posts, not blog content")
                        return False
                        
            print(f"✅ SOCIAL MEDIA VALIDATION PASSED: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error validating social media content for {file_path}: {e}")
            return False

    def _validate_hindi_slogans(self, file_path):
        """Validate that slogans are in Hindi language"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                content_lower = content.lower()
            
            # Check for Hindi indicators
            hindi_indicators = ["hindi:", "transliteration:", "english translation:"]
            has_hindi_structure = all(indicator in content_lower for indicator in hindi_indicators)
            
            if not has_hindi_structure:
                print(f"❌ HINDI SLOGAN VALIDATION FAILED: Missing Hindi structure in {file_path}")
                print(f"   Slogans must include: Hindi text, Transliteration, and English Translation")
                return False
            
            # Check for common English-only patterns that shouldn't be there
            english_only_patterns = [
                "slogan 1:", "slogan 2:", "slogan 3:", "slogan 4:", "slogan 5:",
                "your brand", "smart solutions", "ai powered", "marketing made easy"
            ]
            
            for pattern in english_only_patterns:
                if pattern in content_lower and "hindi:" not in content_lower:
                    print(f"❌ HINDI SLOGAN VALIDATION FAILED: English-only content detected in {file_path}")
                    print(f"   All slogans must be in Hindi with transliteration and translation")
                    return False
                    
            print(f"✅ HINDI SLOGAN VALIDATION PASSED: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error validating Hindi slogans for {file_path}: {e}")
            return False

    def _validate_blog_file_creation(self, file_path):
        """Validate that blog file was created with correct name and location"""
        try:
            # Check if file has correct name
            if not file_path.endswith("ai-marketing-guide.md"):
                print(f"❌ BLOG FILE VALIDATION FAILED: Incorrect filename in {file_path}")
                print(f"   Blog file MUST be named 'ai-marketing-guide.md', not other names like 'blog_post.md'")
                return False
            
            # Check if file is in correct subdirectory
            if "/blogs/" not in file_path:
                print(f"❌ BLOG FILE VALIDATION FAILED: Blog file not in blogs subdirectory: {file_path}")
                print(f"   Blog file MUST be placed in 'blogs' subdirectory")
                return False
            
            # Check if file is the wrong location (like root campaign directory)
            if file_path.count("/") < 3:  # Should have content/campaign/blogs/filename structure
                print(f"❌ BLOG FILE VALIDATION FAILED: Blog file in wrong directory structure: {file_path}")
                print(f"   Expected structure: content/campaign-name/blogs/ai-marketing-guide.md")
                return False
                
            # Check content length (basic validation)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if len(content) < 1000:  # Should be 1500-2000 words, so at least 1000 chars
                print(f"❌ BLOG CONTENT VALIDATION FAILED: Content too short in {file_path} ({len(content)} chars)")
                print(f"   Blog post should be 1500-2000 words")
                return False
                
            print(f"✅ BLOG FILE VALIDATION PASSED: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error validating blog file for {file_path}: {e}")
            return False

    def _validate_blog_content_completeness(self, file_path):
        """Validate that blog contains complete content, not just supplementary sections"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                content_lower = content.lower()
            
            # Check total word count
            word_count = len(content.split())
            if word_count < 2000:
                print(f"❌ BLOG COMPLETENESS VALIDATION FAILED: Content too short ({word_count} words in {file_path})")
                print("   Blog post must be at least 2000 words")
                return False
            
            # Check for required main content sections
            required_sections = [
                ("introduction", ["## introduction", "# introduction", "## intro", "## overview"]),
                ("main content", ["## benefits", "## advantages", "## technical", "## implementation", "## roi", "## business case"]),
                ("recommendations", ["## recommendation", "## strategic", "## next step", "## action"]),
                ("conclusion", ["## conclusion", "## summary", "## final"])
            ]
            
            missing_sections = []
            for section_name, patterns in required_sections:
                section_found = any(pattern in content_lower for pattern in patterns)
                if not section_found:
                    missing_sections.append(section_name)
            
            if missing_sections:
                print(f"❌ BLOG COMPLETENESS VALIDATION FAILED: Missing required sections in {file_path}: {missing_sections}")
                print("   Blog must include: Introduction, Main Content, Strategic Recommendations, Conclusion")
                return False
            
            # Check if it's only supplementary sections (footer content)
            main_content_indicators = [
                "cloud computing", "ai marketing", "automation", "e-commerce", "technical", "implementation",
                "benefits", "advantages", "roi", "business case", "cto", "decision-makers"
            ]
            
            footer_only_indicators = [
                "additional resources", "glossary", "about the author", "final thoughts"
            ]
            
            main_content_found = any(indicator in content_lower for indicator in main_content_indicators)
            mostly_footer = sum(1 for indicator in footer_only_indicators if indicator in content_lower) >= 3
            
            if mostly_footer and not main_content_found:
                print(f"❌ BLOG COMPLETENESS VALIDATION FAILED: Content appears to be only supplementary sections in {file_path}")
                print("   Blog must contain substantial main content about the topic, not just footer sections")
                return False
            
            # Check for substantial technical content for CTO audience
            technical_indicators = [
                "scalability", "integration", "security", "infrastructure", "api", "data", "system",
                "platform", "technology", "software", "architecture", "performance"
            ]
            
            technical_content_found = sum(1 for indicator in technical_indicators if indicator in content_lower)
            if technical_content_found < 5:
                print(f"❌ BLOG COMPLETENESS VALIDATION FAILED: Insufficient technical content for CTO audience in {file_path}")
                print("   Blog must include substantial technical insights for technical decision-makers")
                return False
            
            print(f"✅ BLOG COMPLETENESS VALIDATION PASSED: {file_path} ({word_count} words)")
            return True
            
        except Exception as e:
            print(f"❌ Error validating blog content completeness for {file_path}: {e}")
            return False

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
        
        print("🧠 SOPHISTICATED MULTI-STAGE CAMPAIGN: 12-task iterative quality control workflow")
        print("📝 INTELLIGENT CAMPAIGN: Research → Validation → Blog Loop → Distribution Loop → Audio Loop → Assembly")
        print("🔄 QUALITY-OPTIMIZED: Create → Validate → Analyze → Optimize loops across ALL content types")
        print("💎 Target: Premium campaign with comprehensive optimization, ~60-90 min runtime")
        # Create tasks with explicit names for better tracking
        market_task = self.market_research_task()
        market_task.name = "market_research_task"
        
        market_validation_task = self.market_research_validation_task()
        market_validation_task.name = "market_research_validation_task"
        
        blog_create_task = self.blog_creation_task()
        blog_create_task.name = "blog_creation_task"
        
        blog_validation_task = self.blog_validation_task()
        blog_validation_task.name = "blog_validation_task"
        
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
                market_validation_task,
                
                # Stage 2: Core Content Iteration (Blog) - MUST CREATE 1 BLOG + VALIDATE + 1 ANALYSIS + 1 OPTIMIZED BLOG
                blog_create_task,
                blog_validation_task,
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
            verbose=False,  # Reduced verbosity to minimize terminal spam
            max_rpm=10,  # Reduced rate limit to prevent API issues
            full_output=True,
            max_execution_time=14400,
            share_crew=False,
            output_log_file="crew_execution.log",
            task_callback=self._task_callback,
            step_callback=self._step_callback
        )
