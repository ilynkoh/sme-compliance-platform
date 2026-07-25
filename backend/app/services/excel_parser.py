import openpyxl
import pandas as pd
import logging
from typing import List, Dict, Any
from app.utils.errors import FileProcessingException

logger = logging.getLogger(__name__)

class ExcelParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.account_type_mapping = {
            'asset': 'asset',
            'liability': 'liability',
            'equity': 'equity',
            'revenue': 'revenue',
            'expense': 'expense',
            'current asset': 'asset',
            'non-current asset': 'asset',
            'current liability': 'liability',
            'non-current liability': 'liability',
        }
    
    def parse(self) -> List[Dict[str, Any]]:
        try:
            df = pd.read_excel(self.file_path)
            
            required_columns = ['Account Code', 'Account Name', 'Account Type', 'Debit', 'Credit']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise FileProcessingException(
                    f"Missing required columns: {', '.join(missing_columns)}"
                )
            
            entries = []
            for _, row in df.iterrows():
                try:
                    account_type = self._normalize_account_type(row['Account Type'])
                    
                    entry = {
                        'account_code': str(row['Account Code']).strip(),
                        'account_name': str(row['Account Name']).strip(),
                        'account_type': account_type,
                        'debit_amount': float(row['Debit']) if row['Debit'] else 0.0,
                        'credit_amount': float(row['Credit']) if row['Credit'] else 0.0,
                    }
                    entries.append(entry)
                except Exception as e:
                    logger.warning(f"Skipping row due to error: {e}")
                    continue
            
            if not entries:
                raise FileProcessingException("No valid entries found in Excel file")
            
            logger.info(f"Successfully parsed {len(entries)} trial balance entries")
            return entries
            
        except FileProcessingException:
            raise
        except Exception as e:
            logger.error(f"Error parsing Excel file: {e}")
            raise FileProcessingException(f"Failed to parse Excel file: {str(e)}")
    
    def _normalize_account_type(self, account_type: str) -> str:
        normalized = account_type.lower().strip()
        return self.account_type_mapping.get(normalized, 'other')