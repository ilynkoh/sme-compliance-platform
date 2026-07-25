import api from './api';
import { API_ENDPOINTS } from '../config/api';

export interface UploadResponse {
  id: number;
  company_id: number;
  filename: string;
  status: string;
  file_size: number;
  fiscal_year: string;
  error_message: string | null;
  created_at: string;
}

export interface ReportResponse {
  id: number;
  upload_id: number;
  overall_risk_level: string;
  compliance_score: number;
  total_checks: number;
  passed_checks: number;
  failed_checks: number;
  summary: string;
  recommendations: any;
  created_at: string;
}

export const uploadService = {
  uploadTrialBalance: async (companyId: number, file: File, fiscalYear?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('company_id', companyId.toString());
    if (fiscalYear) {
      formData.append('fiscal_year', fiscalYear);
    }

    const response = await api.post(API_ENDPOINTS.UPLOADS.TRIAL_BALANCE, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data as UploadResponse;
  },

  getUpload: async (uploadId: number) => {
    const response = await api.get(API_ENDPOINTS.UPLOADS.GET(uploadId));
    return response.data as UploadResponse;
  },
};

export const reportService = {
  generateReport: async (uploadId: number, includeAiAnalysis: boolean = true) => {
    const response = await api.post(API_ENDPOINTS.REPORTS.GENERATE, {
      upload_id: uploadId,
      include_ai_analysis: includeAiAnalysis,
    });
    return response.data as ReportResponse;
  },

  getReport: async (reportId: number) => {
    const response = await api.get(API_ENDPOINTS.REPORTS.GET(reportId));
    return response.data as ReportResponse;
  },

  getReportsByUpload: async (uploadId: number) => {
    const response = await api.get(API_ENDPOINTS.REPORTS.BY_UPLOAD(uploadId));
    return response.data as ReportResponse[];
  },
};
