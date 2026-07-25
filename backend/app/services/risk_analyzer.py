import logging
from typing import List, Dict, Any
from app.models.trial_balance import TrialBalanceEntry
from app.models.report import RiskLevel

logger = logging.getLogger(__name__)

class RiskAnalyzer:
    """Analyze financial risks in trial balance"""
    
    def __init__(self, entries: List[TrialBalanceEntry]):
        self.entries = entries
        self.risks = []
    
    def analyze(self) -> List[Dict[str, Any]]:
        """Run risk analysis"""
        risks = []
        
        risks.extend(self._check_zero_balances())
        risks.extend(self._check_unusual_patterns())
        risks.extend(self._check_missing_accounts())
        
        return risks
    
    def _check_zero_balances(self) -> List[Dict[str, Any]]:
        """Check for accounts with zero balances"""
        risks = []
        zero_balance_accounts = [
            e for e in self.entries 
            if e.debit_amount == 0 and e.credit_amount == 0
        ]
        
        if zero_balance_accounts:
            risks.append({
                'risk_type': 'Zero Balance Accounts',
                'risk_level': RiskLevel.LOW,
                'affected_accounts': [e.account_name for e in zero_balance_accounts],
                'description': f'{len(zero_balance_accounts)} accounts have zero balance',
                'recommendation': 'Review if accounts should be closed or eliminated'
            })
        
        return risks
    
    def _check_unusual_patterns(self) -> List[Dict[str, Any]]:
        """Check for unusual account patterns"""
        risks = []
        
        unusual_entries = [
            e for e in self.entries 
            if e.debit_amount > 0 and e.credit_amount > 0
        ]
        
        if unusual_entries:
            risks.append({
                'risk_type': 'Unusual Account Pattern',
                'risk_level': RiskLevel.MEDIUM,
                'affected_accounts': [e.account_name for e in unusual_entries],
                'description': f'{len(unusual_entries)} accounts have both debit and credit',
                'recommendation': 'Review account entries - typically accounts should be either debit or credit'
            })
        
        return risks
    
    def _check_missing_accounts(self) -> List[Dict[str, Any]]:
        """Check for potentially missing accounts"""
        required_accounts = {
            'cash': 'asset',
            'accounts payable': 'liability',
            'accounts receivable': 'asset',
            'revenue': 'revenue',
            'expense': 'expense',
        }
        
        present_accounts = {e.account_name.lower() for e in self.entries}
        
        missing = [
            acc for acc in required_accounts.keys() 
            if acc not in present_accounts
        ]
        
        if missing:
            return [{
                'risk_type': 'Potentially Missing Accounts',
                'risk_level': RiskLevel.LOW,
                'missing_accounts': missing,
                'description': f'Potentially missing: {', '.join(missing)}',
                'recommendation': 'Verify if these accounts exist in chart of accounts'
            }]
        
        return []