import React from 'react';
import { Doughnut, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

interface ReportStatsProps {
  complianceScore: number;
  totalChecks: number;
  passedChecks: number;
  failedChecks: number;
  warningChecks: number;
}

export const ReportStats: React.FC<ReportStatsProps> = ({
  complianceScore,
  totalChecks,
  passedChecks,
  failedChecks,
  warningChecks,
}) => {
  const complianceData = {
    labels: ['Passed', 'Failed', 'Warnings'],
    datasets: [
      {
        data: [passedChecks, failedChecks, warningChecks],
        backgroundColor: ['#22c55e', '#ef4444', '#eab308'],
        borderColor: ['#16a34a', '#dc2626', '#ca8a04'],
        borderWidth: 2,
      },
    ],
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Compliance Score</h3>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="text-5xl font-bold text-primary-600 mb-2">
              {complianceScore.toFixed(1)}%
            </div>
            <p className="text-gray-600">Overall Compliance</p>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Check Results</h3>
        <div className="flex items-center justify-center h-64">
          <Doughnut data={complianceData} />
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Summary</h3>
        <div className="space-y-3 h-64 flex flex-col justify-center">
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Total Checks:</span>
            <span className="font-semibold text-gray-900">{totalChecks}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Passed:</span>
            <span className="font-semibold text-green-600">{passedChecks}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Failed:</span>
            <span className="font-semibold text-red-600">{failedChecks}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Warnings:</span>
            <span className="font-semibold text-yellow-600">{warningChecks}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
