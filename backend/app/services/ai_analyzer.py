import logging
from typing import Dict, Any, Optional

from app.config import settings
from app.models.trial_balance import TrialBalanceEntry

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """AI-powered analysis using OpenAI"""
    
    def __init__(self):
        if settings.OPENAI_API_KEY:
            try:
                import openai
                openai.api_key = settings.OPENAI_API_KEY
            except ImportError:
                logger.warning("OpenAI not installed")
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
    
    def analyze_compliance_risks(self, entries: list, checks: list) -> Optional[str]:
        """Generate AI-powered compliance analysis"""
        try:
            if not settings.OPENAI_API_KEY:
                logger.warning("OpenAI API key not configured")
                return None
            
            import openai
            
            total_assets = sum(e.debit_amount for e in entries if e.account_type == 'asset')
            total_liabilities = sum(e.credit_amount for e in entries if e.account_type == 'liability')
            
            prompt = f"""
            As a Malaysian financial compliance expert, analyze this company's financial position:
            
            Trial Balance Summary:
            - Total Assets: RM{total_assets:,.2f}
            - Total Liabilities: RM{total_liabilities:,.2f}
            - Number of Accounts: {len(entries)}
            
            Compliance Checks Status:
            {self._format_checks(checks)}
            
            Provide:
            1. Risk assessment summary
            2. Key compliance concerns under Companies Act 2016
            3. Recommended remediation steps
            4. Timeline for addressing issues
            
            Format as clear, actionable recommendations for SME management.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Malaysian financial compliance expert specializing in Companies Act 2016."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"AI Analysis error: {e}")
            return None
    
    def generate_recommendations(self, findings: Dict[str, Any]) -> Optional[str]:
        """Generate AI-powered recommendations"""
        try:
            if not settings.OPENAI_API_KEY:
                return None
            
            import openai
            
            prompt = f"""
            Based on these compliance findings for a Malaysian SME:
            
            {findings}
            
            Provide specific, actionable remediation recommendations aligned with:
            - Companies Act 2016
            - Malaysian Financial Reporting Standards (MFRS)
            - Best practices for SMEs
            
            Format as a prioritized action plan.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Malaysian financial compliance expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Recommendation generation error: {e}")
            return None
    
    @staticmethod
    def _format_checks(checks: list) -> str:
        """Format checks for prompt"""
        formatted = []
        for check in checks[:5]:
            status = check.get('status', 'UNKNOWN')
            name = check.get('check_name', 'Unknown Check')
            formatted.append(f"- {name}: {status}")
        return "\n".join(formatted)