from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import random
from datetime import datetime


class AnalyticsToolInput(BaseModel):
    """Input schema for AnalyticsTool."""
    content_id: str = Field(..., description="The ID or title of the content to analyze.")
    metrics: str = Field(..., description="Comma-separated list of metrics to analyze (e.g., 'views,engagement,conversion,shares').")

class AnalyticsTool(BaseTool):
    name: str = "Analytics Tool"
    description: str = (
        "Analyzes the performance of content based on specified metrics. "
        "Provides engagement data, conversion rates, and audience insights. "
        "Use this tool to evaluate content performance and identify optimization opportunities."
    )
    args_schema: Type[BaseModel] = AnalyticsToolInput

    def _run(self, content_id: str, metrics: str) -> str:
        """
        Generates realistic analytics data for the specified content.
        Uses current date and provides contextual recommendations.
        """
        # Get current date for realistic reporting
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Parse requested metrics
        requested_metrics = [m.strip().lower() for m in metrics.split(',')]
        
        # Generate realistic analytics data based on content type and industry benchmarks
        views = random.randint(1500, 8000)  
        engagement_rate = round(random.uniform(2.5, 6.5), 2)  
        conversion_rate = round(random.uniform(1.2, 4.5), 2)  
        avg_time_on_page = round(random.uniform(120, 480), 1)  
        bounce_rate = round(random.uniform(35, 65), 1)  
        shares = random.randint(25, 150)  
        lead_generation = random.randint(15, 85)  
        
        # Industry benchmarks for comparison
        benchmark_engagement = 4.0
        benchmark_conversion = 2.5
        benchmark_bounce = 50.0
        
        # Determine performance level
        performance_score = 0
        if engagement_rate > benchmark_engagement: performance_score += 1
        if conversion_rate > benchmark_conversion: performance_score += 1  
        if bounce_rate < benchmark_bounce: performance_score += 1
        
        performance_level = "high" if performance_score >= 2 else "medium" if performance_score == 1 else "needs_improvement"
        
        # Build response with current date
        response = f"## Performance Analytics Report\n"
        response += f"**Content:** {content_id}\n"
        response += f"**Analysis Date:** {current_date}\n\n"
        response += f"### Key Metrics\n\n"
        
        if 'views' in requested_metrics or 'all' in requested_metrics:
            response += f"- **Total Views:** {views:,}\n"
        
        if 'engagement' in requested_metrics or 'all' in requested_metrics:
            trend = "📈" if engagement_rate > benchmark_engagement else "📉"
            response += f"- **Engagement Rate:** {engagement_rate}% {trend} (Industry avg: {benchmark_engagement}%)\n"
            response += f"- **Average Time on Page:** {avg_time_on_page} seconds\n"
            response += f"- **Bounce Rate:** {bounce_rate}% {'✅' if bounce_rate < benchmark_bounce else '⚠️'}\n"
        
        if 'conversion' in requested_metrics or 'all' in requested_metrics:
            trend = "📈" if conversion_rate > benchmark_conversion else "📉"
            response += f"- **Conversion Rate:** {conversion_rate}% {trend} (Industry avg: {benchmark_conversion}%)\n"
            response += f"- **Lead Generation:** {lead_generation} qualified leads\n"
        
        if 'shares' in requested_metrics or 'all' in requested_metrics:
            response += f"- **Social Shares:** {shares}\n"
        
        # Performance assessment
        response += f"\n### Performance Assessment: **{performance_level.upper()}**\n\n"
        
        # Targeted recommendations based on performance
        response += "### Optimization Recommendations\n\n"
        
        if performance_level == "high":
            response += "**Status: Exceeding Benchmarks** ✅\n\n"
            response += "- **Scale Success:** Create similar content on related topics\n"
            response += "- **Amplify Distribution:** Increase budget allocation to top-performing channels\n"
            response += "- **A/B Test:** Experiment with headlines and CTAs to push performance higher\n"
            response += "- **Repurpose:** Convert into video, infographic, or webinar content\n"
        elif performance_level == "medium":
            response += "**Status: Meeting Some Benchmarks** ⚠️\n\n"
            response += "- **Content Enhancement:** Add more interactive elements (calculators, quizzes)\n"
            response += "- **SEO Optimization:** Review and optimize for better search visibility\n"
            response += "- **CTA Improvement:** Test different call-to-action placements and wording\n"
            response += "- **Audience Targeting:** Refine targeting to reach more qualified prospects\n"
        else:
            response += "**Status: Below Benchmarks** 🔄\n\n"
            response += "- **Content Audit:** Review topic relevance and audience alignment\n"
            response += "- **Technical Review:** Check page load speed and mobile optimization\n"
            response += "- **Distribution Strategy:** Explore new channels and promotion tactics\n"
            response += "- **Content Refresh:** Update with current data and trending keywords\n"
        
        response += f"\n**Recommendation:** {'Continue current strategy with minor optimizations' if performance_level == 'high' else 'Implement suggested improvements and monitor closely' if performance_level == 'medium' else 'Requires significant optimization - consider content revision'}\n"
        
        return response 