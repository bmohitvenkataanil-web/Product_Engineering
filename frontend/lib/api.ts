import {
  Feedback, FeedbackCreate, FeedbackAnalyzeResponse,
  ProductDecision, ProductDecisionCreate,
  EngineeringDecision, EngineeringDecisionCreate,
  ArchitectureDecision, ArchitectureDecisionCreate,
  Experiment, ExperimentCreate,
  Outcome, OutcomeCreate,
  AdviceResponse, CompareAdviceResponse,
  MemoryEvent, TimelineEvent, HindsightStatus, DashboardData
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`API Error (${res.status}): ${errorText || res.statusText}`);
  }

  return res.json();
}

export const api = {
  // Hindsight Status
  getHindsightStatus: () => fetchJson<HindsightStatus>('/api/memory/status'),

  // Dashboard
  getDashboardData: () => fetchJson<DashboardData>('/api/demo/dashboard'),

  // Feedback
  getFeedbacks: (params?: { product_area?: string; status?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return fetchJson<Feedback[]>(`/api/feedback${query ? `?${query}` : ''}`);
  },
  getFeedbackDetail: (id: string) => fetchJson<Feedback>(`/api/feedback/${id}`),
  createFeedback: (data: FeedbackCreate) => fetchJson<Feedback>('/api/feedback', { method: 'POST', body: JSON.stringify(data) }),
  analyzeFeedback: (id: string, memoryMode: string = 'ON') =>
    fetchJson<FeedbackAnalyzeResponse>(`/api/feedback/${id}/analyze?memory_mode=${memoryMode}`, { method: 'POST' }),

  // Product Decisions
  getProductDecisions: (params?: { product_area?: string; status?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return fetchJson<ProductDecision[]>(`/api/product-decisions${query ? `?${query}` : ''}`);
  },
  getProductDecisionDetail: (id: string) => fetchJson<ProductDecision>(`/api/product-decisions/${id}`),
  createProductDecision: (data: ProductDecisionCreate) =>
    fetchJson<ProductDecision>('/api/product-decisions', { method: 'POST', body: JSON.stringify(data) }),

  // Engineering Decisions
  getEngineeringDecisions: (params?: { technology?: string; architecture_area?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return fetchJson<EngineeringDecision[]>(`/api/engineering-decisions${query ? `?${query}` : ''}`);
  },
  getEngineeringDecisionDetail: (id: string) => fetchJson<EngineeringDecision>(`/api/engineering-decisions/${id}`),
  createEngineeringDecision: (data: EngineeringDecisionCreate) =>
    fetchJson<EngineeringDecision>('/api/engineering-decisions', { method: 'POST', body: JSON.stringify(data) }),

  // Architecture Decisions
  getArchitectureDecisions: (params?: { technology?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return fetchJson<ArchitectureDecision[]>(`/api/architecture-decisions${query ? `?${query}` : ''}`);
  },
  getArchitectureDecisionDetail: (id: string) => fetchJson<ArchitectureDecision>(`/api/architecture-decisions/${id}`),
  createArchitectureDecision: (data: ArchitectureDecisionCreate) =>
    fetchJson<ArchitectureDecision>('/api/architecture-decisions', { method: 'POST', body: JSON.stringify(data) }),

  // Experiments
  getExperiments: (params?: { product_area?: string; status?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return fetchJson<Experiment[]>(`/api/experiments${query ? `?${query}` : ''}`);
  },
  createExperiment: (data: ExperimentCreate) =>
    fetchJson<Experiment>('/api/experiments', { method: 'POST', body: JSON.stringify(data) }),
  completeExperiment: (id: string, data: { end_date: string; result: string; conclusion: string; status?: string }) =>
    fetchJson<Experiment>(`/api/experiments/${id}/complete`, { method: 'POST', body: JSON.stringify(data) }),

  // Outcomes
  getOutcomes: (category?: string) =>
    fetchJson<Outcome[]>(`/api/outcomes${category ? `?category=${category}` : ''}`),
  createOutcome: (data: OutcomeCreate) =>
    fetchJson<Outcome>('/api/outcomes', { method: 'POST', body: JSON.stringify(data) }),

  // AI Advisor
  getAdvice: (question: string, domain: string = 'Both', memoryMode: string = 'ON') =>
    fetchJson<AdviceResponse>('/api/agent/advice', {
      method: 'POST',
      body: JSON.stringify({ question, domain, memory_mode: memoryMode }),
    }),
  compareAdvice: (question: string, domain: string = 'Both') =>
    fetchJson<CompareAdviceResponse>('/api/agent/compare', {
      method: 'POST',
      body: JSON.stringify({ question, domain }),
    }),

  // Memory
  getMemoryEvents: (params?: { memory_type?: string; product_area?: string; technology?: string }) => {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return fetchJson<MemoryEvent[]>(`/api/memory/events${query ? `?${query}` : ''}`);
  },
  getMemoryInsights: () => fetchJson<any>('/api/memory/insights'),

  // Timeline
  getTimeline: () => fetchJson<TimelineEvent[]>('/api/timeline'),

  // Demo management
  loadDemoData: () => fetchJson<any>('/api/demo/load', { method: 'POST' }),
  resetDemoData: () => fetchJson<any>('/api/demo/reset', { method: 'POST' }),
  clearAllData: () => fetchJson<any>('/api/demo/clear', { method: 'POST' }),
};
