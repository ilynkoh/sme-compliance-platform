import pytest
import pandas as pd
from app.services.excel_parser import ExcelParser
from app.utils.errors import FileProcessingException

@pytest.fixture
def sample_excel_file(tmp_path):
    """Create sample Excel file for testing"""
    data = {
        'Account Code': ['1000', '1100', '2000', '3000', '4000', '5000'],
        'Account Name': ['Cash', 'Accounts Receivable', 'Accounts Payable', 'Share Capital', 'Revenue', 'Expense'],
        'Account Type': ['asset', 'asset', 'liability', 'equity', 'revenue', 'expense'],
        'Debit': [50000, 30000, 0, 0, 0, 20000],
        'Credit': [0, 0, 40000, 60000, 50000, 0]
    }
    
    df = pd.DataFrame(data)
    file_path = tmp_path / "test_trial_balance.xlsx"
    df.to_excel(file_path, index=False)
    
    return str(file_path)

def test_parse_excel_success(sample_excel_file):
    """Test successful Excel parsing"""
    parser = ExcelParser(sample_excel_file)
    entries = parser.parse()
    
    assert len(entries) == 6
    assert entries[0]['account_code'] == '1000'
    assert entries[0]['account_name'] == 'Cash'
    assert entries[0]['account_type'] == 'asset'
    assert entries[0]['debit_amount'] == 50000
    assert entries[0]['credit_amount'] == 0

def test_parse_excel_invalid_file():
    """Test parsing with invalid file"""
    parser = ExcelParser("/nonexistent/file.xlsx")
    with pytest.raises(FileProcessingException):
        parser.parse()
