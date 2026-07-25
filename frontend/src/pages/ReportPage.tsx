import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { Header } from '../components/Header';
import { ReportStats } from '../components/ReportStats';
import { ComplianceChecklist } from '../components/ComplianceChecklist';
import { reportService } from '../services/upload';
import { Loader } from 'lucide-react';

export const ReportPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const uploadId = searchParams.get('uploadId');
  const [report, setReport] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    const loadReport = async () => {
      if (!uploadId) {
        setError('No upload ID provided');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        // First generate the report
        const generatedReport = await reportService.generateReport(parseInt(uploadId));
        setReport(generatedReport);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to load report');
      } finally {
        setLoading(false);
      }
    };

    loadReport();
  }, [uploadId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="flex items-center justify-center min-h-[calc(100vh-64px)]">
          <div className="text-center">
            <Loader className="animate-spin mx-auto mb-4" size={48} />
            <p className="text-gray-600">Generating compliance report...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="flex items-center justify-center min-h-[calc(100vh-64px)]">
          <div className="text-center">
            <p className="text-red-600 text-lg font-semibold">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!report) {
    return null;
  }

  const warningChecks = report.total_checks - report.passed_checks - report.failed_checks;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Compliance Report</h1>
          <p className="text-gray-600 mt-2">Companies Act 2016 & MFRS Compliance Analysis</p>
        </div>

        {/* Risk Level Badge */}
        <div className="mb-6 p-4 rounded-lg bg-white shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Overall Risk Level</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{report.overall_risk_level.toUpperCase()}</p>
            </div>
            <div className={`px-6 py-3 rounded-lg font-semibold ${
              report.overall_risk_level === 'critical' ? 'bg-red-100 text-red-800' :
              report.overall_risk_level === 'high' ? 'bg-orange-100 text-orange-800' :
              report.overall_risk_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
              'bg-green-100 text-green-800'
            }`}>
              {report.overall_risk_level.toUpperCase()}
            </div>
          </div>
        </div>

        {/* Report Stats */}
        <ReportStats
          complianceScore={report.compliance_score}
          totalChecks={report.total_checks}
          passedChecks={report.passed_checks}
          failedChecks={report.failed_checks}
          warningChecks={warningChecks}
        />

        {/* Summary */}
        {report.summary && (
          <div className="mt-8 bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Report Summary</h2>
            <div className="prose prose-sm max-w-none">
              {report.summary.split('\n').map((line, index) => (
                <p key={index} className="text-gray-700 mb-2">{line}</p>
              ))}
            </div>
          </div>
        )}

        {/* Compliance Checks */}
        {report.check_results && report.check_results.length > 0 && (
          <div className="mt-8 bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Compliance Checks</h2>
            <ComplianceChecklist checks={report.check_results} />
          </div>
        )}

        {/* AI Recommendations */}
        {report.recommendations?.ai_recommendations && (
          <div className="mt-8 bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">AI Recommendations</h2>
            <div className="prose prose-sm max-w-none">
              {report.recommendations.ai_recommendations.split('\n').map((line, index) => (
                <p key={index} className="text-gray-700 mb-2">{line}</p>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
