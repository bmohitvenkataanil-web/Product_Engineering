'use client';

import React, { useEffect, useState } from 'react';
import Header from '@/components/Header';
import { api } from '@/lib/api';
import { ProductDecision } from '@/lib/types';
import ProductDecisionForm from '@/components/ProductDecisionForm';
import { Lightbulb, Plus, Search, CheckCircle, ArrowRight } from 'lucide-react';

export default function ProductDecisionsPage() {
  const [decisions, setDecisions] = useState<ProductDecision[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedArea, setSelectedArea] = useState<string>('ALL');

  const fetchDecisions = async () => {
    try {
      const data = await api.getProductDecisions();
      setDecisions(data);
    } catch (err) {
      console.error('Failed to load product decisions', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDecisions();
  }, []);

  const filtered = selectedArea === 'ALL'
    ? decisions
    : decisions.filter(d => d.product_area === selectedArea);

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Product Decision Repository" subtitle="Product choices retained in organizational memory with reasoning & outcomes." />

      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-text-primary">Product Decisions</h3>
            <p className="text-xs text-text-muted">Document why product approaches were chosen and what actual outcomes resulted.</p>
          </div>

          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-2 px-3 py-1.5 rounded bg-primary-600 hover:bg-primary-700 text-white text-xs font-medium transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>Record Product Decision</span>
          </button>
        </div>

        {/* Filter Bar */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
          {['ALL', 'Search & Relevance', 'User Onboarding', 'Notifications', 'Billing & Payments', 'Data Export', 'Analytics Dashboard'].map((area) => (
            <button
              key={area}
              onClick={() => setSelectedArea(area)}
              className={`px-3 py-1.5 rounded-full font-mono text-xs border transition-colors whitespace-nowrap ${
                selectedArea === area
                  ? 'bg-primary-600/20 text-primary-500 border-primary-500/40 font-semibold'
                  : 'bg-surface text-text-muted border-border hover:text-text-primary'
              }`}
            >
              {area}
            </button>
          ))}
        </div>

        {/* Decision Cards List */}
        {loading ? (
          <div className="p-12 text-center text-xs font-mono text-text-muted">Loading product decision memory...</div>
        ) : filtered.length === 0 ? (
          <div className="p-12 text-center text-xs font-mono text-text-muted border border-dashed border-border rounded-lg">
            No product decisions recorded for this filter.
          </div>
        ) : (
          <div className="space-y-4">
            {filtered.map((pd) => (
              <div key={pd.id} className="bg-surface border border-border rounded-lg p-5 space-y-4 hover:border-border/80 transition-colors">
                <div className="flex items-start justify-between border-b border-border pb-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs text-primary-500 font-bold">{pd.id}</span>
                      <h4 className="text-sm font-semibold text-text-primary">{pd.title}</h4>
                    </div>
                    <p className="text-xs text-text-muted mt-0.5">Product Area: <strong className="text-text-secondary">{pd.product_area}</strong> | Date: {pd.date}</p>
                  </div>
                  <span className="badge-mono bg-success-500/10 text-success-500 border-success-500/30">
                    {pd.status}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div className="p-3 rounded bg-background border border-border space-y-1">
                    <span className="font-mono text-[10px] uppercase text-text-muted block">Problem & Context</span>
                    <p className="text-text-primary leading-relaxed">{pd.problem}</p>
                    {pd.context && <p className="text-text-muted text-[11px] pt-1">{pd.context}</p>}
                  </div>

                  <div className="p-3 rounded bg-background border border-border space-y-1">
                    <span className="font-mono text-[10px] uppercase text-primary-500 font-semibold block">Chosen Approach & Reason</span>
                    <p className="font-semibold text-text-primary">{pd.chosen_approach}</p>
                    <p className="text-text-secondary pt-1">{pd.reason}</p>
                  </div>
                </div>

                {/* Options & Outcomes */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs pt-1">
                  <div>
                    <span className="font-mono text-[10px] uppercase text-text-muted block mb-1">Options Evaluated</span>
                    <div className="flex flex-wrap gap-1.5">
                      {pd.options_considered.map((opt, i) => (
                        <span key={i} className="px-2 py-0.5 rounded bg-background border border-border font-mono text-[11px] text-text-secondary">
                          {opt}
                        </span>
                      ))}
                    </div>
                  </div>

                  {pd.actual_outcome && (
                    <div className="p-2.5 rounded bg-success-500/5 border border-success-500/20">
                      <span className="font-mono text-[10px] uppercase text-success-500 font-bold block">Measured Outcome</span>
                      <p className="text-text-primary text-xs pt-0.5 font-medium">{pd.actual_outcome}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <ProductDecisionForm
          onClose={() => setShowModal(false)}
          onSuccess={fetchDecisions}
        />
      )}
    </div>
  );
}
