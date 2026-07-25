import React from 'react';
import { Header } from '../components/Header';

export const DashboardPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Welcome to SME Compliance Platform</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload Files</h3>
            <p className="text-gray-600 mb-4">Upload your trial balance for analysis</p>
            <a href="/uploads" className="text-primary-600 hover:text-primary-700 font-semibold">
              Go to Uploads →
            </a>
          </div>

          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">View Reports</h3>
            <p className="text-gray-600 mb-4">Check your compliance reports</p>
            <a href="/reports" className="text-primary-600 hover:text-primary-700 font-semibold">
              View Reports →
            </a>
          </div>

          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Documentation</h3>
            <p className="text-gray-600 mb-4">Learn about Companies Act 2016</p>
            <a href="#" className="text-primary-600 hover:text-primary-700 font-semibold">
              Read Docs →
            </a>
          </div>
        </div>
      </main>
    </div>
  );
};
