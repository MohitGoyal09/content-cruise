from crewai.tools import BaseTool
from typing import Dict, List, Any
import re
from urllib.parse import urlparse
import requests


class SEOAnalysisTool(BaseTool):
    name: str = "SEO Analysis Tool"
    description: str = (
        "Analyzes content for SEO optimization including keyword density, "
        "readability score, meta descriptions, and provides actionable recommendations."
    )

    def _run(self, content: str, target_keywords: List[str] = None) -> Dict[str, Any]:
        """
        Analyze content for SEO optimization
        
        Args:
            content: The content to analyze
            target_keywords: List of target keywords to optimize for
        
        Returns:
            Dictionary with SEO analysis results and recommendations
        """
        try:
            if target_keywords is None:
                target_keywords = []
            
            analysis = {
                "word_count": self._count_words(content),
                "readability_score": self._calculate_readability(content),
                "keyword_density": self._analyze_keyword_density(content, target_keywords),
                "heading_structure": self._analyze_headings(content),
                "meta_recommendations": self._generate_meta_recommendations(content),
                "seo_score": 0,
                "recommendations": []
            }
            
            # Calculate overall SEO score and generate recommendations
            analysis["seo_score"] = self._calculate_seo_score(analysis)
            analysis["recommendations"] = self._generate_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            return {"error": f"SEO analysis failed: {str(e)}"}
    
    def _count_words(self, content: str) -> int:
        """Count words in content"""
        words = re.findall(r'\b\w+\b', content.lower())
        return len(words)
    
    def _calculate_readability(self, content: str) -> Dict[str, Any]:
        """Calculate readability metrics"""
        sentences = re.split(r'[.!?]+', content)
        words = re.findall(r'\b\w+\b', content)
        
        avg_sentence_length = len(words) / max(len([s for s in sentences if s.strip()]), 1)
        
        # Simple readability score (lower is better)
        readability_score = min(avg_sentence_length / 15 * 100, 100)
        
        return {
            "avg_sentence_length": round(avg_sentence_length, 2),
            "readability_score": round(readability_score, 2),
            "grade_level": "Easy" if readability_score < 50 else "Medium" if readability_score < 80 else "Difficult"
        }
    
    def _analyze_keyword_density(self, content: str, keywords: List[str]) -> Dict[str, float]:
        """Analyze keyword density"""
        total_words = len(re.findall(r'\b\w+\b', content.lower()))
        keyword_density = {}
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = len(re.findall(rf'\b{re.escape(keyword_lower)}\b', content.lower()))
            density = (count / total_words) * 100 if total_words > 0 else 0
            keyword_density[keyword] = round(density, 2)
        
        return keyword_density
    
    def _analyze_headings(self, content: str) -> Dict[str, Any]:
        """Analyze heading structure"""
        h1_count = len(re.findall(r'^# .+', content, re.MULTILINE))
        h2_count = len(re.findall(r'^## .+', content, re.MULTILINE))
        h3_count = len(re.findall(r'^### .+', content, re.MULTILINE))
        
        return {
            "h1_count": h1_count,
            "h2_count": h2_count,
            "h3_count": h3_count,
            "has_proper_structure": h1_count == 1 and h2_count >= 2
        }
    
    def _generate_meta_recommendations(self, content: str) -> Dict[str, str]:
        """Generate meta description and title recommendations"""
        # Extract first paragraph as potential meta description
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        first_paragraph = paragraphs[0] if paragraphs else ""
        
        # Extract title (first H1)
        title_match = re.search(r'^# (.+)', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Content Title"
        
        return {
            "suggested_title": title[:60] + "..." if len(title) > 60 else title,
            "suggested_meta_description": first_paragraph[:155] + "..." if len(first_paragraph) > 155 else first_paragraph
        }
    
    def _calculate_seo_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate overall SEO score"""
        score = 0
        
        # Word count (ideal: 700-2000 words)
        word_count = analysis["word_count"]
        if 700 <= word_count <= 2000:
            score += 25
        elif 500 <= word_count < 700 or 2000 < word_count <= 3000:
            score += 15
        else:
            score += 5
        
        # Readability
        readability = analysis["readability_score"]["readability_score"]
        if readability < 60:
            score += 25
        elif readability < 80:
            score += 15
        else:
            score += 5
        
        # Heading structure
        if analysis["heading_structure"]["has_proper_structure"]:
            score += 25
        else:
            score += 10
        
        # Keyword density (ideal: 1-3% for main keywords)
        keyword_densities = analysis["keyword_density"]
        ideal_density_count = sum(1 for density in keyword_densities.values() if 1 <= density <= 3)
        if ideal_density_count > 0:
            score += 25
        else:
            score += 10
        
        return score
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable SEO recommendations"""
        recommendations = []
        
        # Word count recommendations
        word_count = analysis["word_count"]
        if word_count < 700:
            recommendations.append("Consider expanding content to at least 700 words for better SEO performance")
        elif word_count > 2000:
            recommendations.append("Content is quite long. Consider breaking into multiple pieces or adding subheadings")
        
        # Readability recommendations
        readability_score = analysis["readability_score"]["readability_score"]
        if readability_score > 80:
            recommendations.append("Consider shortening sentences and using simpler words to improve readability")
        
        # Heading structure recommendations
        heading_structure = analysis["heading_structure"]
        if heading_structure["h1_count"] == 0:
            recommendations.append("Add an H1 heading (main title) to your content")
        elif heading_structure["h1_count"] > 1:
            recommendations.append("Use only one H1 heading per page. Convert extra H1s to H2 or H3")
        
        if heading_structure["h2_count"] < 2:
            recommendations.append("Add more H2 subheadings to improve content structure and readability")
        
        # Keyword density recommendations
        keyword_densities = analysis["keyword_density"]
        for keyword, density in keyword_densities.items():
            if density < 1:
                recommendations.append(f"Increase usage of keyword '{keyword}' (current density: {density}%)")
            elif density > 3:
                recommendations.append(f"Reduce usage of keyword '{keyword}' to avoid over-optimization (current density: {density}%)")
        
        return recommendations 