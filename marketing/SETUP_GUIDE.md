# 🚀 Complete Setup Guide - AI Marketing Automation Platform

## 📋 Quick Start Checklist

✅ **Prerequisites Installation**  
✅ **API Keys Configuration**  
✅ **Project Dependencies**  
✅ **Environment Setup**  
✅ **First Campaign Run**  
✅ **Troubleshooting & Optimization**

---

## 🔧 Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: Stable connection for API calls

### Development Tools (Optional)

```bash
# Git for version control
git --version

# Virtual environment support
python -m venv --help

# Package manager (if using poetry)
poetry --version
```

---

## 🔑 API Keys Setup

### Required API Keys

#### 1. Google Gemini API

```bash
# Get your key from: https://aistudio.google.com/app/apikey
export GOOGLE_API_KEY="your_gemini_api_key_here"
```

#### 2. Mistral AI API

```bash
# Get your key from: https://console.mistral.ai/
export MISTRAL_API_KEY="your_mistral_api_key_here"
```

#### 3. SARVAM AI API (Voice Generation)

```bash
# Get your key from: https://www.sarvam.ai/
export SARVAM_API_KEY="your_sarvam_api_key_here"
```

#### 4. Serper API (Search)

```bash
# Get your key from: https://serper.dev/
export SERPER_API_KEY="your_serper_api_key_here"
```

#### 5. AgentOps API (Optional - Monitoring)

```bash
# Get your key from: https://agentops.ai/
export AGENTOPS_API_KEY="your_agentops_api_key_here"
```

### Environment File Setup

Create a `.env` file in the `marketing/` directory:

```env
# Core LLM APIs
GOOGLE_API_KEY=your_gemini_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here

# Voice Generation
SARVAM_API_KEY=your_sarvam_api_key_here

# Search and Research
SERPER_API_KEY=your_serper_api_key_here

# Monitoring (Optional)
AGENTOPS_API_KEY=your_agentops_api_key_here

# Campaign Configuration
CAMPAIGN_NAME=auto-generated
DEFAULT_BUDGET=75000
DEFAULT_DURATION_DAYS=45
```

---

## 📦 Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the project
git clone <repository-url>
cd deep-dive

# Verify project structure
ls -la
```

### Step 2: Navigate to Marketing Directory

```bash
cd marketing
ls -la
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv marketing-env

# Activate virtual environment
# On Windows:
marketing-env\Scripts\activate
# On macOS/Linux:
source marketing-env/bin/activate

# Verify activation
which python
```

### Step 4: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(crewai|streamlit|mistral|google)"
```

### Step 5: Verify API Keys

```bash
# Test API key setup
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Gemini API:', '✅' if os.getenv('GOOGLE_API_KEY') else '❌')
print('Mistral API:', '✅' if os.getenv('MISTRAL_API_KEY') else '❌')
print('SARVAM API:', '✅' if os.getenv('SARVAM_API_KEY') else '❌')
print('Serper API:', '✅' if os.getenv('SERPER_API_KEY') else '❌')
"
```

---

## 🎮 Usage Options

### Option 1: Command Line Interface (Recommended for Demos)

```bash
# Run complete marketing campaign
python src/marketing/main.py

# Expected output:
# ⚡ AI Marketing Content Creation - SPEED-OPTIMIZED WORKFLOW
# 🚀 Direct Execution → 📊 Research → 📝 Create → 🔍 Analyze
# ⚡ Target: <$0.95, ~15 min | 🧠 Mistral + Gemini
```

### Option 2: Streamlit Web Interface (Interactive)

```bash
# Launch web interface
streamlit run src/marketing/app_streamlit.py

# Access at: http://localhost:8501
# Features:
# - Interactive campaign configuration
# - Real-time progress monitoring
# - Download generated content
# - Campaign history management
```

### Option 3: Custom Integration

```python
# Direct Python integration
from src.marketing.crew import Marketing

# Initialize campaign
marketing_crew = Marketing()

# Configure campaign
inputs = {
    'topic': 'AI-powered marketing automation',
    'target_audience': 'small business owners aged 30-45',
    'brand_voice': 'professional yet approachable',
    'budget': '75000',
    'campaign_name': 'my-campaign-2025'
}

# Run campaign
result = marketing_crew.crew().kickoff(inputs=inputs)
```

---

## 📁 Project Structure Understanding

```
marketing/
├── src/marketing/
│   ├── config/
│   │   ├── agents.yaml         # Agent configurations
│   │   └── tasks.yaml          # Task definitions
│   ├── tools/                  # Custom AI tools
│   │   ├── analytics_tool.py
│   │   ├── voice_generation.py
│   │   └── ...
│   ├── crew.py                 # Main orchestration
│   ├── main.py                 # CLI entry point
│   └── app_streamlit.py        # Web interface
├── content/                    # Generated campaigns
│   └── {campaign-name}/
│       ├── market_research/
│       ├── blogs/
│       ├── social-media/
│       ├── emails/
│       └── audio/
├── requirements.txt            # Dependencies
├── .env                        # API keys (create this)
└── README.md                   # Documentation
```

---

## 🔧 Configuration Options

### Agent Configuration (Advanced)

Edit `src/marketing/config/agents.yaml`:

```yaml
# Customize agent behavior
campaign_manager:
  role: "Your Custom Campaign Director Role"
  max_iterations: 5          # Reduce for speed
  max_execution_time: 1200   # 20 minutes max

content_creator:
  role: "Your Custom Content Creator Role"
  max_iterations: 3          # Balance quality vs speed
  max_execution_time: 2400   # 40 minutes max
```

### Task Configuration (Advanced)

Edit `src/marketing/config/tasks.yaml`:

```yaml
# Customize task behavior
market_research_task:
  description: "Your custom research requirements"
  expected_output: "Specific deliverables you need"

blog_creation_task:
  description: "Your custom blog requirements"
  expected_output: "Specific blog format and length"
```

### Cost Optimization Settings

```python
# Ultra-Budget Mode (Edit in crew.py)
mistral_llm = LLM(
    model="mistral/mistral-tiny",     # Cheapest option
    max_tokens=500,                   # Reduced tokens
    temperature=0.1                   # Lower creativity
)

# Speed Mode
gemini_llm = LLM(
    model="gemini-1.5-flash",         # Faster model
    max_tokens=800,                   # Reduced tokens
    timeout=120                       # Faster timeout
)
```

---

## 🧪 Testing Your Setup

### Basic Functionality Test

```bash
# Quick test run (should complete in ~15 minutes)
python src/marketing/main.py

# Expected directory structure after completion:
content/
└── ai-powered-marketing-automation-small-2025/
    ├── market_research/
    │   ├── competitors.md
    │   ├── keywords.md
    │   └── audience.md
    ├── blogs/
    │   └── ai-marketing-guide.md
    ├── analysis/
    │   └── quick-improvements.md
    ├── social-media/
    │   └── posts.md
    ├── emails/
    │   └── email-sequence.md
    └── audio/
        ├── slogans.md
        └── audio_*.wav
```

### Performance Validation

```bash
# Check generated content quality
ls -la content/*/blogs/
wc -w content/*/blogs/*.md           # Should be 1500+ words
ls -la content/*/audio/*.wav         # Should have audio file

# Verify all required files exist
find content/ -name "*.md" | wc -l   # Should be 6+ markdown files
```

### Cost Tracking Test

```python
# Monitor API costs (if AgentOps configured)
import agentops
agentops.init()

# Run campaign with monitoring
# Check costs at: https://agentops.ai/
```

---

## 🚨 Troubleshooting

### Common Issues & Solutions

#### API Key Issues

```bash
# Issue: "API key not found"
# Solution: Verify environment variables
echo $GOOGLE_API_KEY
echo $MISTRAL_API_KEY

# Issue: "Invalid API key"
# Solution: Check key format and permissions
# Gemini keys start with: AI...
# Mistral keys start with: API...
```

#### Rate Limiting

```bash
# Issue: "Rate limit exceeded"
# Solution: Check API quotas and implement delays

# Temporary fix: Add delays in crew.py
import time
time.sleep(60)  # Wait 1 minute between calls
```

#### File Generation Issues

```bash
# Issue: Missing output files
# Solution: Check directory permissions
mkdir -p content/test-campaign
touch content/test-campaign/test.md

# Issue: Empty files
# Solution: Check agent execution logs
tail -f crew_execution.log
```

#### Memory Issues

```bash
# Issue: Out of memory errors
# Solution: Reduce max_tokens in LLM config

# Edit crew.py
mistral_llm = LLM(max_tokens=1000)  # Reduce from 3000
gemini_llm = LLM(max_tokens=2000)   # Reduce from 4000
```

### Performance Optimization

#### Speed Optimization

```python
# Reduce agent iterations for faster execution
max_iterations = 1  # Single pass only

# Use faster models
model = "gemini-1.5-flash"     # Instead of gemini-2.5-flash
model = "mistral/mistral-tiny" # Instead of mistral-small
```

#### Cost Optimization

```python
# Monitor token usage
max_tokens = 500    # Minimum viable tokens
temperature = 0.1   # Reduce creativity for consistency

# Skip optional tasks
tasks = [market_research, blog_creation, audio_slogan]  # Essential only
```

---

## 📊 Expected Output & Quality Metrics

### Successful Campaign Indicators

✅ **Completion Time**: 10-20 minutes  
✅ **Total Cost**: $0.50 - $1.50  
✅ **Files Generated**: 6+ markdown files + 1 audio file  
✅ **Blog Length**: 1500+ words  
✅ **SEO Score**: 85+ points  
✅ **Brand Consistency**: Aligned across all content

### Quality Checkpoints

1. **Market Research**: 3 comprehensive analysis files
2. **Blog Content**: Publication-ready, SEO-optimized
3. **Social Media**: Platform-specific, engaging content
4. **Email Sequence**: 5-email customer journey
5. **Audio Content**: Professional Hindi voice generation
6. **Overall Quality**: Professional presentation ready

---

## 🎯 Next Steps After Setup

### Immediate Actions

1. **Run First Campaign**: Test with default settings
2. **Review Output**: Check content quality and completeness
3. **Customize Settings**: Adjust for your specific needs
4. **Monitor Performance**: Track costs and execution time

### Advanced Usage

1. **Custom Agents**: Create specialized agents for your industry
2. **Integration**: Connect with your existing marketing tools
3. **Automation**: Set up scheduled campaign generation
4. **Scaling**: Configure for enterprise-level usage

### Deployment

1. **Production Setup**: Configure for production environment
2. **Security**: Implement proper API key management
3. **Monitoring**: Set up comprehensive logging and analytics
4. **Maintenance**: Regular updates and optimization

---

## 📞 Support & Resources

### Documentation

- **Main README**: Comprehensive project overview
- **ARCHITECTURE.md**: Technical implementation details
- **API Documentation**: Tool and integration guides

### Community & Support

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Community Q&A and best practices
- **Wiki**: Additional tutorials and examples

### Performance Monitoring

- **AgentOps Dashboard**: Real-time cost and performance tracking
- **Logs**: Detailed execution logs for troubleshooting
- **Metrics**: Success rates and quality scores

---

**🎉 Congratulations! Your AI Marketing Automation Platform is ready to create professional marketing campaigns in minutes instead of hours!**
