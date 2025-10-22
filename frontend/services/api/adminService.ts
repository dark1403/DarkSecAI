import apiClient from './apiClient';

export interface AdminStats {
  users_total: number;
  admins_total: number;
  reports_total: number;
  vulnerabilities_total: number;
  headers_reports_total: number;
  domxss_results_total: number;
  payload_results_total: number;
  xss_payload_results_total: number;
  file_upload_results_total: number;
  conversations_total: number;
  api_keys_configured: number;
  api_keys: Record<string, boolean>;
  last_event: string | null;
  audit_events: number;
  severity_breakdown: Record<string, number>;
}

const adminService = {
  getStats: async (): Promise<AdminStats> => {
    const response = await apiClient.get('/admin/stats/');
    return response.data as AdminStats;
  }
};

export default adminService;
