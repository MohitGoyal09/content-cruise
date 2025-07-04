from crewai.tools import BaseTool
from typing import Dict, List, Any, Optional
import json
from datetime import datetime, timedelta
import re


class SocialMediaTool(BaseTool):
    name: str = "Social Media Management Tool"
    description: str = (
        "Manages social media content creation, scheduling, and optimization for multiple platforms. "
        "Creates platform-specific content variations and suggests optimal posting times."
    )

    def _run(self, content: str, platforms: List[str] = None, action: str = "create_posts") -> Dict[str, Any]:
        """
        Manage social media content and scheduling
        
        Args:
            content: The original content to adapt for social media
            platforms: List of platforms (twitter, linkedin, facebook, instagram)
            action: Action to perform (create_posts, schedule, analyze_performance)
        
        Returns:
            Dictionary with social media content and scheduling recommendations
        """
        try:
            if platforms is None:
                platforms = ["twitter", "linkedin", "facebook"]
            
            if action == "create_posts":
                return self._create_platform_posts(content, platforms)
            elif action == "schedule":
                return self._generate_schedule_recommendations(platforms)
            elif action == "analyze_performance":
                return self._analyze_social_performance()
            else:
                return {"error": f"Unknown action: {action}"}
                
        except Exception as e:
            return {"error": f"Social media management failed: {str(e)}"}
    
    def _create_platform_posts(self, content: str, platforms: List[str]) -> Dict[str, Any]:
        """Create platform-specific social media posts"""
        # Extract key information from content
        title = self._extract_title(content)
        key_points = self._extract_key_points(content)
        hashtags = self._generate_hashtags(content)
        
        posts = {}
        
        for platform in platforms:
            if platform.lower() == "twitter":
                posts["twitter"] = self._create_twitter_posts(title, key_points, hashtags)
            elif platform.lower() == "linkedin":
                posts["linkedin"] = self._create_linkedin_post(title, key_points, hashtags, content)
            elif platform.lower() == "facebook":
                posts["facebook"] = self._create_facebook_post(title, key_points, hashtags, content)
            elif platform.lower() == "instagram":
                posts["instagram"] = self._create_instagram_post(title, key_points, hashtags)
        
        return {
            "posts": posts,
            "hashtags": hashtags,
            "engagement_tips": self._get_engagement_tips(),
            "posting_schedule": self._generate_schedule_recommendations(platforms)
        }
    
    def _extract_title(self, content: str) -> str:
        """Extract title from content"""
        title_match = re.search(r'^# (.+)', content, re.MULTILINE)
        return title_match.group(1) if title_match else "Check out our latest content!"
    
    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from content"""
        # Look for bullet points or numbered lists
        bullet_points = re.findall(r'^[-*•] (.+)', content, re.MULTILINE)
        numbered_points = re.findall(r'^\d+\. (.+)', content, re.MULTILINE)
        
        # Combine and limit to top 5 points
        key_points = (bullet_points + numbered_points)[:5]
        
        # If no bullet points found, extract from headings
        if not key_points:
            headings = re.findall(r'^## (.+)', content, re.MULTILINE)
            key_points = headings[:5]
        
        return key_points
    
    def _generate_hashtags(self, content: str) -> List[str]:
        """Generate relevant hashtags based on content"""
        # Common marketing hashtags
        base_hashtags = ["#DigitalMarketing", "#ContentMarketing", "#MarketingTips", "#BusinessGrowth"]
        
        # Extract keywords for specific hashtags
        words = re.findall(r'\b[A-Z][a-z]+\b', content)
        keyword_hashtags = [f"#{word}" for word in set(words[:3])]
        
        return base_hashtags + keyword_hashtags
    
    def _create_twitter_posts(self, title: str, key_points: List[str], hashtags: List[str]) -> List[Dict[str, str]]:
        """Create Twitter thread posts"""
        posts = []
        
        # Main tweet
        main_tweet = f"{title[:200]}... 🧵\n\n{' '.join(hashtags[:3])}"
        posts.append({
            "type": "main_tweet",
            "content": main_tweet,
            "character_count": len(main_tweet)
        })
        
        # Thread tweets for key points
        for i, point in enumerate(key_points[:4], 1):
            thread_tweet = f"{i}/{len(key_points[:4])} {point[:250]}"
            posts.append({
                "type": "thread_tweet",
                "content": thread_tweet,
                "character_count": len(thread_tweet)
            })
        
        return posts
    
    def _create_linkedin_post(self, title: str, key_points: List[str], hashtags: List[str], content: str) -> Dict[str, str]:
        """Create LinkedIn post"""
        # LinkedIn allows longer content
        post_content = f"🚀 {title}\n\n"
        
        if key_points:
            post_content += "Key insights:\n"
            for point in key_points[:3]:
                post_content += f"• {point}\n"
        
        post_content += f"\n{' '.join(hashtags[:5])}\n\n"
        post_content += "What are your thoughts? Share in the comments! 👇"
        
        return {
            "content": post_content,
            "character_count": len(post_content),
            "call_to_action": "engagement_focused"
        }
    
    def _create_facebook_post(self, title: str, key_points: List[str], hashtags: List[str], content: str) -> Dict[str, str]:
        """Create Facebook post"""
        post_content = f"{title}\n\n"
        
        if key_points:
            post_content += "📈 Here's what you need to know:\n\n"
            for point in key_points[:3]:
                post_content += f"✅ {point}\n"
        
        post_content += f"\n{' '.join(hashtags[:3])}"
        
        return {
            "content": post_content,
            "character_count": len(post_content),
            "recommended_image": "infographic or carousel",
            "call_to_action": "Learn more or share your experience!"
        }
    
    def _create_instagram_post(self, title: str, key_points: List[str], hashtags: List[str]) -> Dict[str, str]:
        """Create Instagram post"""
        post_content = f"✨ {title}\n\n"
        
        if key_points:
            for i, point in enumerate(key_points[:3], 1):
                post_content += f"{i}. {point}\n"
        
        post_content += f"\n{' '.join(hashtags[:10])}"  
        
        return {
            "content": post_content,
            "character_count": len(post_content),
            "recommended_format": "carousel or reel",
            "visual_suggestions": ["infographic", "behind_the_scenes", "testimonial"]
        }
    
    def _generate_schedule_recommendations(self, platforms: List[str]) -> Dict[str, Any]:
        """Generate optimal posting schedule recommendations"""
        schedule = {
            "twitter": {
                "best_times": ["9:00 AM", "1:00 PM", "3:00 PM"],
                "best_days": ["Tuesday", "Wednesday", "Thursday"],
                "frequency": "1-3 times per day",
                "optimal_interval": "4 hours"
            },
            "linkedin": {
                "best_times": ["8:00 AM", "12:00 PM", "5:00 PM"],
                "best_days": ["Tuesday", "Wednesday", "Thursday"],
                "frequency": "1 time per day",
                "optimal_interval": "24 hours"
            },
            "facebook": {
                "best_times": ["9:00 AM", "1:00 PM", "7:00 PM"],
                "best_days": ["Wednesday", "Thursday", "Friday"],
                "frequency": "1-2 times per day",
                "optimal_interval": "6 hours"
            },
            "instagram": {
                "best_times": ["11:00 AM", "2:00 PM", "7:00 PM"],
                "best_days": ["Wednesday", "Thursday", "Friday"],
                "frequency": "1 time per day",
                "optimal_interval": "24 hours"
            }
        }
        
        filtered_schedule = {platform: schedule[platform] for platform in platforms if platform in schedule}
        
        return {
            "platform_schedules": filtered_schedule,
            "general_tips": [
                "Post consistently at the same times",
                "Test different times and measure engagement",
                "Consider your audience's time zone",
                "Monitor competitors' posting patterns"
            ]
        }
    
    def _get_engagement_tips(self) -> List[str]:
        """Get engagement optimization tips"""
        return [
            "Ask questions to encourage comments",
            "Use emojis to make posts more visually appealing",
            "Share behind-the-scenes content",
            "Respond to comments within 1-2 hours",
            "Use polls and interactive features",
            "Share user-generated content",
            "Post industry news and trending topics",
            "Include clear calls-to-action"
        ]
    
    def _analyze_social_performance(self) -> Dict[str, Any]:
        """Analyze social media performance (mock data for demonstration)"""
        return {
            "engagement_rates": {
                "twitter": "2.5%",
                "linkedin": "4.2%",
                "facebook": "3.1%",
                "instagram": "5.8%"
            },
            "best_performing_content": "Educational posts with infographics",
            "optimal_posting_time": "Wednesday 1:00 PM",
            "recommendations": [
                "Increase visual content on Instagram",
                "Use more industry hashtags on LinkedIn",
                "Create more thread content on Twitter",
                "Focus on community building on Facebook"
            ]
        } 