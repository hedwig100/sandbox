import { useQuery } from '@tanstack/react-query';

interface HealthResponse {
  status: string;
  timestamp: string;
}

export const useHealthQuery = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: async (): Promise<HealthResponse> => {
      const response = await fetch('/api/health');
      if (!response.ok) {
        throw new Error('Failed to fetch health status');
      }
      return response.json();
    },
  });
};
