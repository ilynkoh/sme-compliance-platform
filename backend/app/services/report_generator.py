import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models.upload import Upload
from app.models.report import ComplianceReport, ComplianceCheckResult, RiskLevel
from app.models.trial_balance import TrialBalanceEntry
from app.services.compliance_checker import ComplianceChecker
from app.services.risk_analyzer import RiskAnalyzer
from app.services.ai_analyzer import AIAnalyzer

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate compliance reports"""
    
    def __init__(self, upload: Upload, db: Session):
        self.upload = upload
        self.db = db
        self.entries = db.query(TrialBalanceEntry).filter(
            TrialBalanceEntry.upload_id == upload.id
        ).all()
    
    def generate(self, include_ai_analysis: bool = True) -> ComplianceReport:
        """Generate complete compliance report"""
        try:
            checker = ComplianceChecker(self.entries)
            compliance_checks = checker.run_checks()
            
            analyzer = RiskAnalyzer(self.entries)
            risk_analysis = analyzer.analyze()
            
            compliance_score = self._calculate_compliance_score(compliance_checks)
            overall_risk = self._determine_overall_risk(compliance_checks)
            
            report = ComplianceReport(
                upload_id=self.upload.id,
                report_type="compliance",
                overall_risk_level=overall_risk,
                total_checks=len(compliance_checks),
                passed_checks=len([c for c in compliance_checks if c['status'] == 'pass']),
                failed_checks=len([c for c in compliance_checks if c['status'] == 'fail']),
                compliance_score=compliance_score,
                summary=self._generate_summary(compliance_checks, risk_analysis)
            )
            
            for check in compliance_checks:
                result = ComplianceCheckResult(
                    check_name=check['check_name'],
                    check_category=check['check_category'],
                    status=check['status'],
                    risk_level=check.get('risk_level', RiskLevel.LOW),
                    description=check.get('description'),
                    finding=check.get('finding'),
                    reference=check.get('reference')
                )
                report.check_results.append(result)
            
            if include_ai_analysis:
                ai_analyzer = AIAnalyzer()
                ai_summary = ai_analyzer.analyze_compliance_risks(self.entries, compliance_checks)
                ai_recommendations = ai_analyzer.generate_recommendations({
                    'findings': compliance_checks,
                    'risks': risk_analysis
                })
                
                if ai_summary:
                    report.summary = f"{report.summary}\n\n**AI Analysis:**\n{ai_summary}"
                
                report.recommendations = {
                    'ai_recommendations': ai_recommendations,
                    'risks': risk_analysis
                }
            
            self.db.add(report)
            self.db.commit()
            self.db.refresh(report)
            
            logger.info(f"Generated compliance report {report.id} for upload {self.upload.id}")
            return report
        
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise
    
    def _calculate_compliance_score(self, checks: List[Dict[str, Any]]) -> float:
        """Calculate compliance score 0-100"""
        if not checks:
            return 0.0
        
        passed = len([c for c in checks if c['status'] == 'pass'])
        return (passed / len(checks)) * 100
    
    def _determine_overall_risk(self, checks: List[Dict[str, Any]]) -> RiskLevel:
        """Determine overall risk level"""
        risk_counts = {}
        for check in checks:
            risk = check.get('risk_level', RiskLevel.LOW)
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        if RiskLevel.CRITICAL in risk_counts and risk_counts[RiskLevel.CRITICAL] > 0:
            return RiskLevel.CRITICAL
        if RiskLevel.HIGH in risk_counts and risk_counts[RiskLevel.HIGH] > 0:
            return RiskLevel.HIGH
        if RiskLevel.MEDIUM in risk_counts and risk_counts[RiskLevel.MEDIUM] > 0:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
    
    def _generate_summary(self, checks: List[Dict[str, Any]], risks: List[Dict[str, Any]]) -> str:
        """Generate report summary"""
        passed = len([c for c in checks if c['status'] == 'pass'])
        failed = len([c for c in checks if c['status'] == 'fail'])
        warnings = len([c for c in checks if c['status'] == 'warning'])
        
        summary = f"""
        **Compliance Report Summary**
        
        - Total Compliance Checks: {len(checks)}
        - Passed: {passed}
        - Failed: {failed}
        - Warnings: {warnings}
        
        - Financial Risks Identified: {len(risks)}
        
        This report evaluates the trial balance against Malaysian Companies Act 2016 requirements
        and Malaysian Financial Reporting Standards (MFRS).
        """
        
        return summary.strip()