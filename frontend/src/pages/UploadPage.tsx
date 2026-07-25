import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Header } from '../components/Header';
import { FileUpload } from '../components/FileUpload';
import { uploadService } from '../services/upload';
import { Upload, MoreVertical } from 'lucide-react';

export const UploadPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
  const [companyId, setCompanyId] = React.useState<number>(1);
  const [fiscalYear, setFiscalYear] = React.useState(new Date().getFullYear().toString());
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [success, setSuccess] = React.useState(false);
  const navigate = useNavigate();

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setError(null);
    setSuccess(false);
  };

  const handleSubmit = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      const response = await uploadService.uploadTrialBalance(
        companyId,
        selectedFile,
        fiscalYear
      );
      setSuccess(true);
      setTimeout(() => {
        navigate(`/reports?uploadId=${response.id}`);
      }, 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Upload Trial Balance</h1>
          <p className="text-gray-600 mt-2">
            Upload your trial balance Excel file for compliance analysis
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow p-8">
              <FileUpload
                onFileSelect={handleFileSelect}
                isLoading={loading}
                error={error}
                success={success}
              />

              {selectedFile && (
                <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <p className="text-sm font-semibold text-blue-900 mb-2">Selected File:</p>
                  <p className="text-blue-800">{selectedFile.name}</p>
                </div>
              )}

              <div className="mt-8 flex gap-4">
                <button
                  onClick={handleSubmit}
                  disabled={!selectedFile || loading}
                  className="flex-1 bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  <Upload size={18} />
                  {loading ? 'Uploading...' : 'Upload File'}
                </button>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Upload Details</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Fiscal Year
                </label>
                <input
                  type="number"
                  value={fiscalYear}
                  onChange={(e) => setFiscalYear(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>

            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-900">
                <strong>Supported formats:</strong> XLSX, XLS, CSV
              </p>
              <p className="text-sm text-blue-900 mt-2">
                <strong>Max file size:</strong> 50 MB
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
