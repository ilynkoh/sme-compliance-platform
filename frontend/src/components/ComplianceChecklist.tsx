import React from 'react';
import { AlertCircle, CheckCircle, AlertTriangle, Info } from 'lucide-react';

export interface ComplianceCheckItem {
  check_name: string;
  check_category: string;
  status: 'pass' | 'fail' | 'warning' | 'not_applicable';
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  finding?: string;
  remediation?: string;
  reference?: string;
}

interface ComplianceChecklistProps {
  checks: ComplianceCheckItem[];
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'pass':
      return <CheckCircle className="text-green-500" size={20} />;
    case 'fail':
      return <AlertCircle className="text-red-500" size={20} />;
    case 'warning':
      return <AlertTriangle className="text-warning-500" size={20} />;
    default:
      return <Info className="text-gray-500" size={20} />;
  }
};

const getRiskBadgeColor = (risk: string) => {
  switch (risk) {
    case 'critical':
      return 'bg-red-100 text-red-800';
    case 'high':
      return 'bg-orange-100 text-orange-800';
    case 'medium':
      return 'bg-yellow-100 text-yellow-800';
    default:
      return 'bg-green-100 text-green-800';
  }
};

export const ComplianceChecklist: React.FC<ComplianceChecklistProps> = ({ checks }) => {
  const [expandedId, setExpandedId] = React.useState<number | null>(null);

  return (
    <div className="space-y-3">
      {checks.map((check, index) => (
        <div key={index} className="border rounded-lg hover:shadow-md transition">
          <button
            onClick={() => setExpandedId(expandedId === index ? null : index)}
            className="w-full flex items-center justify-between p-4 hover:bg-gray-50"
          >
            <div className="flex items-center gap-3 text-left flex-1">
              {getStatusIcon(check.status)}
              <div>
                <p className="font-semibold text-gray-900">{check.check_name}</p>
                <p className="text-sm text-gray-500">{check.check_category}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${getRiskBadgeColor(check.risk_level)}`}>
                {check.risk_level.toUpperCase()}
              </span>
              <span className="text-gray-400">{expandedId === index ? '▼' : '▶'}</span>
            </div>
          </button>

          {expandedId === index && (
            <div className="border-t bg-gray-50 p-4 space-y-3">
              {check.description && (
                <div>
                  <p className="text-sm font-semibold text-gray-700">Description</p>
                  <p className="text-sm text-gray-600">{check.description}</p>
                </div>
              )}
              {check.finding && (
                <div>
                  <p className="text-sm font-semibold text-gray-700">Finding</p>
                  <p className="text-sm text-gray-600">{check.finding}</p>
                </div>
              )}
              {check.remediation && (
                <div>
                  <p className="text-sm font-semibold text-gray-700">Remediation</p>
                  <p className="text-sm text-gray-600">{check.remediation}</p>
                </div>
              )}
              {check.reference && (
                <div>
                  <p className="text-sm font-semibold text-gray-700">Reference</p>
                  <p className="text-sm text-primary-600 font-mono">{check.reference}</p>
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
