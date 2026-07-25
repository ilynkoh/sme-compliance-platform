import React from 'react';
import { Upload as UploadIcon, AlertCircle, CheckCircle } from 'lucide-react';
import { useDropzone } from 'react-dropzone';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  isLoading?: boolean;
  error?: string | null;
  success?: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  isLoading,
  error,
  success,
}) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0]);
      }
    },
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv'],
    },
    disabled: isLoading,
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition ${
        isDragActive
          ? 'border-primary-500 bg-primary-50'
          : 'border-gray-300 hover:border-gray-400'
      } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center gap-4">
        {success ? (
          <CheckCircle size={48} className="text-green-500" />
        ) : error ? (
          <AlertCircle size={48} className="text-red-500" />
        ) : (
          <UploadIcon size={48} className="text-gray-400" />
        )}

        {success && (
          <div>
            <p className="text-green-600 font-semibold">File uploaded successfully!</p>
          </div>
        )}
        {error && (
          <div>
            <p className="text-red-600 font-semibold">Upload failed</p>
            <p className="text-red-500 text-sm">{error}</p>
          </div>
        )}
        {!success && !error && (
          <div>
            <p className="text-gray-700 font-semibold">
              {isDragActive
                ? 'Drop your Excel file here'
                : 'Drag and drop your trial balance Excel file here'}
            </p>
            <p className="text-gray-500 text-sm mt-2">
              or click to select (XLSX, XLS, CSV)
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
