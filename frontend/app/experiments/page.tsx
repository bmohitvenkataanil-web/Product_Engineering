'use client';

import React, { useEffect, useState } from 'react';
import Header from '@/components/Header';
import { api } from '@/lib/api';
import { Experiment } from '@/lib/types';
import { FlaskConical, CheckCircle2, AlertCircle, Plus, X } from 'lucide-react';

export default function ExperimentsPage() {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoading] = useState(true);
  const [completingExp, setCompletingExp] = useState<Experiment | null>(null);
  const [resultText, setResultText] = useState('');
  const [conclusionText, setConclusionText] = useState('');

  const fetchExperiments = async () => {
    try {
      const data = await api.getExperiments();
      setExperiments(data);
    } catch (err) {
      console.error('Failed to load experiments', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExperiments();
  }, []);

  const handleCompleteSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!completingExp) return;

    try {
      await api.completeExperiment(completingExp.id, {
        end_date: new Date().toISOString().split('T')[0],
        result: resultText,
        conclusion: conclusionText,
        status: 'Completed'
      });
      setCompletingExp(null);
      setResultText('');
      setConclusionText('');
      fetchExperiments();
    } catch (err) {
      console.error('Failed to complete experiment', err);
    }
  };

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Product & Engineering Experiments" subtitle="Hypothesis testing and recorded outcomes retained in Hindsight." />

      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-text-primary">Controlled Experiments</h3>
            <p className="text-xs text-text-muted">Completed experiment outcomes automatically become durable organizational experience.</p>
          </div>
        </div>

        {loading ? (
          <div className="p-12 text-center text-xs font-mono text-text-muted">Loading experiment records...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {experiments.map((exp) => (
              <div key={exp.id} className="bg-surface border border-border rounded-lg p-5 space-y-4 hover:border-border/80 transition-colors">
                <div className="flex items-start justify-between border-b border-border pb-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs text-primary-500 font-bold">{exp.id}</span>
                      <h4 className="text-sm font-semibold text-text-primary">{exp.name}</h4>
                    </div>
                    <p className="text-xs text-text-muted mt-0.5">Area: <strong>{exp.product_area}</strong> | Started: {exp.start_date}</p>
                  </div>
                  <span className={`badge-mono ${exp.status === 'Completed' ? 'bg-success-500/10 text-success-500 border-success-500/30' : 'bg-warning-500/10 text-warning-500 border-warning-500/30'}`}>
                    {exp.status}
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div className="p-2.5 rounded bg-background border border-border">
                    <span className="font-mono text-[10px] uppercase text-text-muted block">Hypothesis</span>
                    <p className="text-text-primary">{exp.hypothesis}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-[11px]">
                    <div className="p-2 rounded bg-background border border-border">
                      <span className="font-mono text-[10px] uppercase text-text-muted block">Variant A (Control)</span>
                      <p className="text-text-secondary">{exp.variant_a}</p>
                    </div>
                    <div className="p-2 rounded bg-background border border-border">
                      <span className="font-mono text-[10px] uppercase text-text-muted block">Variant B (Test)</span>
                      <p className="text-text-secondary">{exp.variant_b}</p>
                    </div>
                  </div>

                  {exp.result && (
                    <div className="p-2.5 rounded bg-background border border-border space-y-1">
                      <span className="font-mono text-[10px] uppercase text-primary-500 font-bold block">Measured Result</span>
                      <p className="text-text-primary">{exp.result}</p>
                    </div>
                  )}

                  {exp.conclusion && (
                    <div className="p-2.5 rounded bg-success-500/5 border border-success-500/20 space-y-1">
                      <span className="font-mono text-[10px] uppercase text-success-500 font-bold block">Retained Lesson Learned</span>
                      <p className="text-text-primary font-medium">{exp.conclusion}</p>
                    </div>
                  )}
                </div>

                {exp.status !== 'Completed' && (
                  <div className="pt-2 border-t border-border flex justify-end">
                    <button
                      onClick={() => setCompletingExp(exp)}
                      className="px-3 py-1.5 rounded bg-primary-600 hover:bg-primary-700 text-white text-xs font-medium transition-colors"
                    >
                      Complete & Retain Experiment
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Complete Modal */}
      {completingExp && (
        <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4">
          <div className="bg-surface border border-border rounded-lg w-full max-w-lg p-6 space-y-4 text-xs">
            <div className="flex items-center justify-between border-b border-border pb-3">
              <h3 className="font-mono font-bold text-text-primary uppercase">Complete Experiment [{completingExp.id}]</h3>
              <button onClick={() => setCompletingExp(null)} className="text-text-muted hover:text-text-primary">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCompleteSubmit} className="space-y-4">
              <div className="space-y-1">
                <label className="font-mono text-text-muted">Measured Result *</label>
                <textarea
                  required
                  rows={2}
                  value={resultText}
                  onChange={(e) => setResultText(e.target.value)}
                  placeholder="e.g. Opt-outs decreased by 48%, but daily engagement declined by 6%."
                  className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
                />
              </div>

              <div className="space-y-1">
                <label className="font-mono text-text-muted">Conclusion & Reusable Lesson *</label>
                <textarea
                  required
                  rows={3}
                  value={conclusionText}
                  onChange={(e) => setConclusionText(e.target.value)}
                  placeholder="e.g. Future notification changes should implement targeted frequency rules rather than global toggles."
                  className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button type="button" onClick={() => setCompletingExp(null)} className="px-3 py-1.5 rounded border border-border">
                  Cancel
                </button>
                <button type="submit" className="px-4 py-1.5 rounded bg-primary-600 hover:bg-primary-700 text-white font-medium">
                  Complete & Retain in Hindsight
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
