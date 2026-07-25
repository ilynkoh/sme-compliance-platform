import pytest
from app.services.compliance_checker import ComplianceChecker
from app.models.trial_balance import TrialBalanceEntry, AccountType

def test_balance_check_pass(test_db):
    """Test balanced trial balance check"""
    # Create balanced entries
    entries = [
        TrialBalanceEntry(upload_id=1, account_code='1000', account_name='Cash', account_type=AccountType.ASSET, debit_amount=1000),
        TrialBalanceEntry(upload_id=1, account_code='2000', account_name='Liability', account_type=AccountType.LIABILITY, credit_amount=1000),
    ]
    
    checker = ComplianceChecker(entries)
    checks = checker.run_checks()
    
    # Find the balance check
    balance_check = next((c for c in checks if c['check_name'] == 'Trial Balance Totals'), None)
    assert balance_check is not None
    assert balance_check['status'] == 'pass'

def test_balance_check_fail(test_db):
    """Test unbalanced trial balance check"""
    entries = [
        TrialBalanceEntry(upload_id=1, account_code='1000', account_name='Cash', account_type=AccountType.ASSET, debit_amount=1000),
        TrialBalanceEntry(upload_id=1, account_code='2000', account_name='Liability', account_type=AccountType.LIABILITY, credit_amount=500),
    ]
    
    checker = ComplianceChecker(entries)
    checks = checker.run_checks()
    
    balance_check = next((c for c in checks if c['check_name'] == 'Trial Balance Totals'), None)
    assert balance_check is not None
    assert balance_check['status'] == 'fail'
