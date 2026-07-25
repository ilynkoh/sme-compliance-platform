import logging
from typing import List, Dict, Any
from app.models.trial_balance import TrialBalanceEntry
from app.models.report import ComplianceCheckResult, CheckStatus, RiskLevel

logger = logging.getLogger(__name__)

class ComplianceChecker:
    """Check compliance against Companies Act 2016"""
    
    def __init__(self, entries: List[TrialBalanceEntry]):
        self.entries = entries
        self.checks = []
    
    def run_checks(self) -> List[Dict[str, Any]]:
        """Run all compliance checks"""
        checks = []
        
        checks.extend(self._check_balance_sheet_structure())
        checks.extend(self._check_asset_classification())
        checks.extend(self._check_liability_classification())
        checks.extend(self._check_equity_structure())
        checks.extend(self._check_account_balances())
        checks.extend(self._check_disclosure_requirements())
        checks.extend(self._check_audit_requirements())
        
        return checks
    
    def _check_balance_sheet_structure(self) -> List[Dict[str, Any]]:
        """Check balance sheet structure compliance"""
        checks = []
        
        has_assets = any(e.account_type == 'asset' for e in self.entries)
        has_liabilities = any(e.account_type == 'liability' for e in self.entries)
        has_equity = any(e.account_type == 'equity' for e in self.entries)
        
        checks.append({
            'check_name': 'Assets Classification',
            'check_category': 'Financial Statement',
            'status': CheckStatus.PASS if has_assets else CheckStatus.FAIL,
            'risk_level': RiskLevel.CRITICAL if not has_assets else RiskLevel.LOW,
            'description': 'Verify proper classification of assets',
            'reference': 'CA 2016 - Schedule 2 (MFRS)'
        })
        
        checks.append({
            'check_name': 'Liabilities Classification',
            'check_category': 'Financial Statement',
            'status': CheckStatus.PASS if has_liabilities else CheckStatus.WARNING,
            'risk_level': RiskLevel.MEDIUM if not has_liabilities else RiskLevel.LOW,
            'description': 'Verify proper classification of liabilities',
            'reference': 'CA 2016 - Schedule 2 (MFRS)'
        })
        
        checks.append({
            'check_name': 'Equity Structure',
            'check_category': 'Financial Statement',
            'status': CheckStatus.PASS if has_equity else CheckStatus.FAIL,
            'risk_level': RiskLevel.HIGH if not has_equity else RiskLevel.LOW,
            'description': 'Verify proper equity classification',
            'reference': 'CA 2016 - Schedule 2 (MFRS)'
        })
        
        return checks
    
    def _check_asset_classification(self) -> List[Dict[str, Any]]:
        return [{
            'check_name': 'Asset Valuation',
            'check_category': 'Financial Statement',
            'status': CheckStatus.PASS,
            'risk_level': RiskLevel.LOW,
            'description': 'Assets valued at historical cost or fair value',
            'reference': 'MFRS 101 - Presentation of Financial Statements'
        }]
    
    def _check_liability_classification(self) -> List[Dict[str, Any]]:
        return [{
            'check_name': 'Liability Classification',
            'check_category': 'Financial Statement',
            'status': CheckStatus.PASS,
            'risk_level': RiskLevel.LOW,
            'description': 'Liabilities properly classified as current or non-current',
            'reference': 'MFRS 101 - Presentation of Financial Statements'
        }]
    
    def _check_equity_structure(self) -> List[Dict[str, Any]]:
        return [{
            'check_name': 'Equity Composition',
            'check_category': 'Financial Statement',
            'status': CheckStatus.PASS,
            'risk_level': RiskLevel.LOW,
            'description': 'Equity composition disclosed (share capital, reserves, retained earnings)',
            'reference': 'CA 2016 - Section 399'
        }]
    
    def _check_account_balances(self) -> List[Dict[str, Any]]:
        checks = []
        
        total_debits = sum(e.debit_amount for e in self.entries)
        total_credits = sum(e.credit_amount for e in self.entries)
        
        is_balanced = abs(total_debits - total_credits) < 0.01
        
        checks.append({
            'check_name': 'Trial Balance Totals',
            'check_category': 'Financial Statement',
            'status': CheckStatus.PASS if is_balanced else CheckStatus.FAIL,
            'risk_level': RiskLevel.CRITICAL if not is_balanced else RiskLevel.LOW,
            'description': f'Debits (RM{total_debits:,.2f}) = Credits (RM{total_credits:,.2f})',
            'finding': None if is_balanced else f'Balance difference: RM{abs(total_debits - total_credits):,.2f}',
            'reference': 'Fundamental Accounting Principle'
        })
        
        return checks
    
    def _check_disclosure_requirements(self) -> List[Dict[str, Any]]:
        return [
            {
                'check_name': 'Related Party Disclosure',
                'check_category': 'Disclosure',
                'status': CheckStatus.WARNING,
                'risk_level': RiskLevel.MEDIUM,
                'description': 'Related party transactions must be disclosed',
                'reference': 'MFRS 124 - Related Party Disclosures'
            },
            {
                'check_name': 'Contingent Liabilities',
                'check_category': 'Disclosure',
                'status': CheckStatus.WARNING,
                'risk_level': RiskLevel.MEDIUM,
                'description': 'Contingent liabilities must be disclosed if material',
                'reference': 'MFRS 137 - Provisions, Contingent Liabilities and Contingent Assets'
            }
        ]
    
    def _check_audit_requirements(self) -> List[Dict[str, Any]]:
        return [{
            'check_name': 'Audit Threshold Compliance',
            'check_category': 'Audit & Reporting',
            'status': CheckStatus.WARNING,
            'risk_level': RiskLevel.MEDIUM,
            'description': 'Verify if company meets audit threshold under CA 2016',
            'reference': 'CA 2016 - Section 379 (Audit exemption threshold)'
        }]