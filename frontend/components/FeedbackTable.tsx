'use client';

import React, { useState } from 'react';
import { Feedback, FeedbackAnalyzeResponse } from '@/lib/types';
import { api } from '@/lib/api';
import EvidencePanel from './EvidencePanel';
import { BrainCircuit, Search, CheckCircle, AlertTriangle, ArrowRight, X } from 'lucide-react';

interface FeedbackTableProps {
  feedbacks: Feedback[];
  onRefresh?: () => void;
}

export default function FeedbackTable({ feedbacks, onRefresh }: FeedbackTableProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFeedback, setSelectedFeedback] = useState<Feedback | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<FeedbackAnalyzeResponse | null>(null);
  const [memoryMode, setMemoryMode] = useState<'ON' | 'OFF'>('ON');

  const filtered = feedbacks.filter((fb) =>
    fb.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
    fb.customer_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    fb.product_area.toLowerCase().includes(searchTerm.toLowerCase()) ||
    fb.id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleAnalyze = async (fb: Feedback) => {
    setSelectedFeedback(fb);
    setAnalyzing(true);
    setAnalysisResult(null);
    try {
      const res = await api.analyzeFeedback(fb.id, memoryMode);
      setAnalysisResult(res);
    } catch (err) {
      console.error('Failed to analyze feedback', err);
    } finally {
      setAnalyzing(false);
    }
  };

  const getPriorityBadge = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical':
      case 'high':
        return 'bg-danger-500/10 text-danger-500 border-danger-500/30';
      case 'medium':
        return 'bg-warning-500/10 text-warning-500 border-warning-500/30';
      default:
        return 'bg-border text-text-muted border-border';
    }
  };

  return (
    <div className="space-y-4">
      {/* Table Filters */}
      <div className="flex items-center justify-between gap-4 bg-surface p-3 border border-border rounded-lg">
        <div className="relative flex-1 max-w-sm">
          <Search className="w-4 h-4 text-text-muted absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Filter feedback by customer, area, keyword..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-background border border-border rounded px-3 py-1.5 pl-9 text-xs text-text-primary placeholder:text-text-muted focus:outline-none focus:border-primary-500"
          />
        </div>

        <div className="flex items-center gap-2 text-xs">
          <span className="text-text-muted font-mono">Memory Mode:</span>
          <button
            onClick={() => setMemoryMode('ON')}
            className={`px-2.5 py-1 rounded text-xs font-mono font-medium border transition-colors ${
              memoryMode === 'ON'
                ? 'bg-primary-600/20 text-primary-500 border-primary-500/40'
                : 'bg-background text-text-muted border-border'
            }`}
          >
            Hindsight ON
          </button>
          <button
            onClick={() => setMemoryMode('OFF')}
            className={`px-2.5 py-1 rounded text-xs font-mono font-medium border transition-colors ${
              memoryMode === 'OFF'
                ? 'bg-border text-text-primary border-border-subtle'
                : 'bg-background text-text-muted border-border'
            }`}
          >
            Memory OFF
          </button>
        </div>
      </div>

      {/* Main Table */}
      <div className="bg-surface border border-border rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-background/80 border-b border-border">
                <th className="table-header">ID</th>
                <th className="table-header">Customer</th>
                <th className="table-header">Feedback Content</th>
                <th className="table-header">Product Area</th>
                <th className="table-header">Priority</th>
                <th className="table-header">Date</th>
                <th className="table-header">Status</th>
                <th className="table-header text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/40">
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-xs text-text-muted font-mono">
                    No matching customer feedback records found.
                  </td>
                </tr>
              ) : (
                filtered.map((fb) => (
                  <tr key={fb.id} className="hover:bg-surface-hover/60 transition-colors">
                    <td className="table-cell font-mono text-xs text-text-muted">{fb.id}</td>
                    <td className="table-cell font-medium text-text-primary">{fb.customer_name}</td>
                    <td className="table-cell max-w-xs truncate text-text-secondary" title={fb.content}>
                      {fb.content}
                    </td>
                    <td className="table-cell font-mono text-xs text-primary-500">{fb.product_area}</td>
                    <td className="table-cell">
                      <span className={`badge-mono ${getPriorityBadge(fb.priority)}`}>
                        {fb.priority}
                      </span>
                    </td>
                    <td className="table-cell font-mono text-xs text-text-muted">{fb.date}</td>
                    <td className="table-cell">
                      <span className="badge-mono bg-border/60 text-text-secondary border-border">
                        {fb.status}
                      </span>
                    </td>
                    <td className="table-cell text-right">
                      <button
                        onClick={() => handleAnalyze(fb)}
                        className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-primary-600/15 hover:bg-primary-600/30 text-primary-500 border border-primary-500/30 text-xs font-medium transition-colors"
                      >
                        <BrainCircuit className="w-3.5 h-3.5" />
                        <span>Analyze with Memory</span>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Detail / Memory Analysis Modal */}
      {selectedFeedback && (
        <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4">
          <div className="bg-surface border border-border rounded-lg w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            {/* Modal Header */}
            <div className="p-4 border-b border-border bg-background flex items-center justify-between">
              <div className="flex items-center gap-2">
                <BrainCircuit className="w-5 h-5 text-primary-500" />
                <div>
                  <h3 className="text-xs font-mono font-bold text-text-primary uppercase tracking-wider">
                    Feedback Memory Analysis [{selectedFeedback.id}]
                  </h3>
                  <p className="text-xs text-text-muted">Customer: {selectedFeedback.customer_name}</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedFeedback(null)}
                className="p-1 text-text-muted hover:text-text-primary rounded hover:bg-surface-hover"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6 space-y-6 overflow-y-auto flex-1">
              {/* Original Feedback Details */}
              <div className="p-4 rounded bg-background border border-border space-y-2">
                <span className="text-[10px] font-mono uppercase text-text-muted">Original Feedback Content</span>
                <p className="text-sm font-medium text-text-primary">{selectedFeedback.content}</p>
                <div className="flex items-center gap-4 text-xs font-mono text-text-muted pt-1">
                  <span>Area: <strong className="text-primary-500">{selectedFeedback.product_area}</strong></span>
                  <span>Priority: <strong>{selectedFeedback.priority}</strong></span>
                  <span>Date: <strong>{selectedFeedback.date}</strong></span>
                </div>
              </div>

              {analyzing ? (
                <div className="p-12 text-center space-y-3">
                  <BrainCircuit className="w-8 h-8 text-primary-500 animate-spin mx-auto" />
                  <p className="text-xs font-mono text-text-muted">
                    Recalling historical organizational experiences from Hindsight Memory Bank...
                  </p>
                </div>
              ) : analysisResult ? (
                <div className="space-y-6">
                  {/* Grounded Recommendation */}
                  <div className="p-4 rounded-lg bg-primary-600/10 border border-primary-500/30 space-y-2">
                    <span className="text-[10px] font-mono uppercase text-primary-500 font-bold block">
                      Grounded Recommendation (Memory {analysisResult.memory_mode_used})
                    </span>
                    <p className="text-sm font-semibold text-text-primary leading-relaxed">
                      {analysisResult.recommendation}
                    </p>
                  </div>

                  {/* Evidence Drawer */}
                  <EvidencePanel
                    evidence={(analysisResult.historical_evidence || []).map((e: any) => ({
                      type: e.type || 'Evidence',
                      date: e.date || '',
                      title: e.title || '',
                      summary: e.content || e.summary || '',
                      relevance_reason: e.relevance_reason || 'Retrieved from Hindsight memory bank'
                    }))}
                    confidence={analysisResult.memory_confidence}
                    observedOutcomes={analysisResult.observed_outcome}
                    tradeOffs={analysisResult.trade_offs}
                  />

                  {/* Next Step Action */}
                  <div className="p-4 rounded bg-background border border-border flex items-center justify-between">
                    <div>
                      <span className="text-[10px] font-mono uppercase text-text-muted block">Suggested Next Step</span>
                      <p className="text-xs font-medium text-text-primary">{analysisResult.next_step}</p>
                    </div>
                    <button
                      onClick={() => setSelectedFeedback(null)}
                      className="px-4 py-2 rounded bg-primary-600 hover:bg-primary-700 text-white text-xs font-medium transition-colors"
                    >
                      Acknowledge & Save
                    </button>
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
