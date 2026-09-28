export interface Feedback {
  id: string;
  customer_id?: string;
  customer_name: string;
  content: string;
  product_area: string;
  sentiment: string;
  priority: string;
  date: string;
  status: string;
  created_at: string;
}

export interface FeedbackCreate {
  customer_id?: string;
  customer_name: string;
  content: string;
  product_area: string;
  sentiment?: string;
  priority?: string;
  date: string;
  status?: string;
}

export interface FeedbackAnalyzeResponse {
  feedback_id: string;
  problem: string;
  historical_evidence: Array<{
    type: string;
    date: string;
    title: string;
    content: string;
  }>;
  previous_attempts: string[];
  observed_outcome: string;
  recommendation: string;
  trade_offs: string;
  next_step: string;
  memory_confidence: string;
  memory_mode_used: string;
}

export interface ProductDecision {
  id: string;
  title: string;
  problem: string;
  context?: string;
  options_considered: string[];
  chosen_approach: string;
  reason: string;
  expected_outcome?: string;
  actual_outcome?: string;
  date: string;
  status: string;
  product_area: string;
  related_feedback_id?: string;
  created_at: string;
}

export interface ProductDecisionCreate {
  title: string;
  problem: string;
  context?: string;
  options_considered: string[];
  chosen_approach: string;
  reason: string;
  expected_outcome?: string;
  actual_outcome?: string;
  date: string;
  status?: string;
  product_area: string;
  related_feedback_id?: string;
}

export interface AlternativeOption {
  name: string;
  reason_rejected?: string;
}

export interface EngineeringDecision {
  id: string;
  title: string;
  problem: string;
  context?: string;
  decision: string;
  alternatives_considered: string[];
  rejected_alternatives: AlternativeOption[];
  constraints?: string;
  trade_offs?: string;
  expected_consequences?: string;
  actual_consequences?: string;
  technology: string;
  architecture_area: string;
  date: string;
  status: string;
  related_product_decision_id?: string;
  related_feedback_id?: string;
  created_at: string;
}

export interface EngineeringDecisionCreate {
  title: string;
  problem: string;
  context?: string;
  decision: string;
  alternatives_considered: string[];
  rejected_alternatives: AlternativeOption[];
  constraints?: string;
  trade_offs?: string;
  expected_consequences?: string;
  actual_consequences?: string;
  technology: string;
  architecture_area: string;
  date: string;
  status?: string;
  related_product_decision_id?: string;
  related_feedback_id?: string;
}

export interface ArchitectureDecision {
  id: string;
  title: string;
  status: string;
  date: string;
  technology: string;
  problem: string;
  context?: string;
  constraints?: string;
  options: string[];
  decision: string;
  trade_offs?: string;
  consequences?: string;
  related_decisions: string[];
  created_at: string;
}

export interface ArchitectureDecisionCreate {
  title: string;
  status?: string;
  date: string;
  technology: string;
  problem: string;
  context?: string;
  constraints?: string;
  options: string[];
  decision: string;
  trade_offs?: string;
  consequences?: string;
  related_decisions?: string[];
}

export interface Experiment {
  id: string;
  name: string;
  product_area: string;
  hypothesis: string;
  variant_a: string;
  variant_b: string;
  start_date: string;
  end_date?: string;
  result?: string;
  conclusion?: string;
  status: string;
  created_at: string;
}

export interface ExperimentCreate {
  name: string;
  product_area: string;
  hypothesis: string;
  variant_a: string;
  variant_b: string;
  start_date: string;
  end_date?: string;
  result?: string;
  conclusion?: string;
  status?: string;
}

export interface Outcome {
  id: string;
  title: string;
  description: string;
  category: string;
  metrics_impact?: string;
  date: string;
  related_decision_type?: string;
  related_decision_id?: string;
  created_at: string;
}

export interface OutcomeCreate {
  title: string;
  description: string;
  category?: string;
  metrics_impact?: string;
  date: string;
  related_decision_type?: string;
  related_decision_id?: string;
}

export interface HistoricalEvidenceItem {
  type: string;
  date: string;
  title: string;
  summary: string;
  relevance_reason: string;
}

export interface AdviceResponse {
  question: string;
  domain: string;
  memory_mode: string;
  recommendation: string;
  historical_context?: string;
  previous_decisions: string[];
  alternatives_rejected: Array<{ option: string; reason?: string } | any>;
  trade_offs?: string;
  observed_outcomes?: string;
  what_changed?: string;
  suggested_next_step?: string;
  relevant_memories: HistoricalEvidenceItem[];
  memory_confidence: string;
  memory_status: string;
}

export interface CompareAdviceResponse {
  question: string;
  without_memory: AdviceResponse;
  with_memory: AdviceResponse;
  what_changed_summary: string;
}

export interface MemoryEvent {
  id: string;
  memory_type: string;
  summary: string;
  content: string;
  product_area?: string;
  technology?: string;
  hindsight_memory_id?: string;
  date: string;
  related_decision_id?: string;
  related_outcome_id?: string;
  created_at: string;
}

export interface TimelineEvent {
  id: string;
  date: string;
  type: string;
  title: string;
  description: string;
  product_area?: string;
  technology?: string;
  status?: string;
  related_id?: string;
}

export interface HindsightStatus {
  connected: boolean;
  mode: string;
  bank_id: string;
  base_url: string;
  total_memories_retained: number;
  message: string;
}

export interface DashboardData {
  metrics: {
    total_feedback: number;
    product_decisions: number;
    engineering_decisions: number;
    architecture_decisions: number;
    experiments: number;
    learned_experiences: number;
    successful_outcomes: number;
    unresolved_issues: number;
  };
  charts: {
    feedback_trend: Array<{ date: string; count: number }>;
    product_decisions_trend: Array<{ date: string; count: number }>;
    engineering_decisions_trend: Array<{ date: string; count: number }>;
    decisions_by_area: Array<{ area: string; count: number }>;
    decisions_by_tech: Array<{ technology: string; count: number }>;
    outcome_distribution: Array<{ category: string; count: number }>;
  };
  recent_organizational_learning: Array<{
    title: string;
    summary: string;
    date: string;
    impact: string;
  }>;
  recent_product_decisions: Array<{
    id: string;
    title: string;
    product_area: string;
    date: string;
    status: string;
    chosen_approach: string;
  }>;
  recent_engineering_decisions: Array<{
    id: string;
    title: string;
    technology: string;
    architecture_area: string;
    date: string;
    status: string;
    decision: string;
  }>;
  recent_outcomes: Array<{
    id: string;
    title: string;
    category: string;
    metrics_impact: string;
    date: string;
  }>;
  recent_feedback: Array<{
    id: string;
    customer_name: string;
    content: string;
    product_area: string;
    priority: string;
    date: string;
    status: string;
  }>;
}
