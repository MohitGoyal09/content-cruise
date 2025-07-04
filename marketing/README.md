# 💰 AI Marketing Automation - COST OPTIMIZED

## 🚀 Performance Metrics (Optimized)

- **Original Cost:** $3.8 | **Optimized Cost:** <$1.00 ⚡ **75% Reduction**
- **Original Time:** 1hr+ | **Optimized Time:** ~15 min ⚡ **85% Faster**
- **Tasks:** 5 essential tasks (down from 8)
- **Voice Calls:** 1 single API call (optimized)

## 💡 Cost Optimization Strategies Applied

### 1. **LLM Model Optimization**

- ✅ `mistral-small-latest` (cheapest Mistral)
- ✅ `gemini-1.5-flash` (fastest/cheapest Gemini)
- ✅ `max_tokens` limits (1000-1200)
- ✅ Lower temperature (0.1-0.5)
- ✅ 30-second timeouts

### 2. **Task Reduction**

- ❌ Removed: `blog_optimization_task` (redundant)
- ❌ Removed: `email_marketing_task` (can be generated later)
- ❌ Removed: `final_analysis_task` (merged into blog_analysis)
- ✅ Kept: Core content creation + analysis

### 3. **Agent Optimization**

- ✅ `max_iterations=1` (single pass)
- ✅ `verbose=False` (minimal output)
- ✅ Essential tools only
- ✅ Execution timeouts (5-10 min max)

### 4. **Voice Generation Efficiency**

- ✅ **ONE** voice API call only
- ✅ Hindi-friendly slogans
- ✅ Pre-optimized examples
- ✅ 5-second rate limiting

### 5. **API Rate Limiting**

- ✅ `max_rpm=120` (faster processing)
- ✅ No artificial delays
- ✅ Parallel processing where possible

## 🎯 Cost Breakdown (Estimated)

| Component | Original | Optimized | Savings |
|-----------|----------|-----------|---------|
| LLM Calls | $2.50 | $0.60 | 76% |
| Voice API | $0.80 | $0.20 | 75% |
| Search API | $0.50 | $0.15 | 70% |
| **Total** | **$3.80** | **$0.95** | **75%** |

## ⚡ Speed Optimizations

### Runtime Breakdown

- **Market Research:** 3 min (was 15 min)
- **Blog Creation:** 5 min (was 20 min)
- **Blog Analysis:** 2 min (was 10 min)
- **Social Media:** 3 min (was 15 min)
- **Audio Slogan:** 2 min (was 10 min)
- **Total:** ~15 min (was 70+ min)

## 🔧 Further Optimization Options

### Ultra-Budget Mode (Cost: <$0.50)

```python
# Switch to even cheaper models
mistral_llm = LLM(model="mistral/mistral-tiny", max_tokens=500)
gemini_llm = LLM(model="gemini-1.5-flash", max_tokens=800)
```

### Lightning Mode (Time: <10 min)

```python
# Reduce to 3 core tasks only
tasks = [market_research, blog_creation, audio_slogan]
```

---

# AI Marketing Automation Crew

This CrewAI-powered marketing automation system creates comprehensive marketing campaigns with AI-generated content, including blog posts, social media content, and voice-generated slogans.

## Features

- **Market Research**: Competitor analysis, keyword research, and audience insights
- **Content Creation**: Blog posts, social media content, and email sequences  
- **Performance Analysis**: SEO optimization and content improvement recommendations
- **Voice Generation**: AI-powered Hindi-friendly slogans with audio output
- **Multi-Agent Workflow**: Specialized agents for different marketing tasks

## Quick Start

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set API Keys**:

   ```bash
   export GOOGLE_API_KEY=your_gemini_key
   export MISTRAL_API_KEY=your_mistral_key  
   export SARVAM_API_KEY=your_sarvam_key
   export SERPER_API_KEY=your_serper_key
   ```

3. **Run Campaign**:

   ```bash
   cd marketing
   python src/marketing/main.py
   ```

## Project Structure

```
marketing/
├── content/                    # Generated campaign content
│   └── {campaign-name}/       # Dynamic campaign folders
│       ├── market_research/   # Competitor & audience analysis
│       ├── blogs/            # Blog posts & optimizations
│       ├── analysis/         # Performance recommendations  
│       ├── social-media/     # Social media posts
│       ├── emails/           # Email marketing sequences
│       └── audio/            # Voice slogans & audio files
├── src/marketing/
│   ├── config/
│   │   ├── agents.yaml       # Agent configurations
│   │   └── tasks.yaml        # Task definitions
│   ├── tools/                # Custom AI tools
│   ├── crew.py              # Main crew orchestration
│   └── main.py              # Entry point
└── knowledge/               # User preferences & context
```

## Configuration

### Campaign Settings

The system uses dynamic inputs for:

- Campaign topic and target audience
- Brand voice and messaging
- Budget and timeline
- Content preferences

### Agent Specialization

- **Campaign Manager**: Strategic oversight and coordination
- **Market Strategist**: Research and competitive analysis  
- **Content Creator**: Blog posts and creative content
- **Performance Analyst**: Optimization and improvement
- **Brand Voice Specialist**: Slogans and audio generation

## Cost Management

Monitor your usage with AgentOps integration:

- Track API costs in real-time
- Optimize model selection for budget
- Monitor task execution times
- Review performance metrics

## Advanced Features

### Voice Generation

- Hindi-language support via SARVAM AI
- Multiple speaker options
- Automatic file management
- Cost-optimized single API calls

### SEO Optimization  

- Keyword density analysis
- Readability scoring
- Meta description generation
- Content improvement suggestions

### Social Media Integration

- Platform-specific content formatting
- Hashtag optimization
- Engagement strategy recommendations
- Cross-platform consistency checks

# Marketing Crew

Welcome to the Marketing Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:

```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/marketing/config/agents.yaml` to define your agents
- Modify `src/marketing/config/tasks.yaml` to define your tasks
- Modify `src/marketing/crew.py` to add your own logic, tools and specific args
- Modify `src/marketing/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the marketing Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The marketing Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Marketing Crew or crewAI.

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
