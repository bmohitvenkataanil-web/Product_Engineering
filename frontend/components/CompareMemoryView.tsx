'use client';

import React from 'react';
import { CompareAdviceResponse } from '@/lib/types';
import { AlertTriangle, CheckCircle, BrainCircuit, CircleOff, ArrowRight } from 'lucide-react';

interface CompareMemoryViewProps {
  data: CompareAdviceResponse;
}

export default function CompareMemoryView({ data }: CompareMemoryViewProps) {
  const { without_memory, with_memory, what_changed_summary } = data;

  return (
    <div className="space-y-6">
      {/* What Changed Highlight Banner */}
      <div className="p-4 rounded-lg bg-primary-600/10 border border-primary-500/30 space-y-2">
        <div className="flex items-center gap-2">
          <BrainCircuit className="w-5 h-5 text-primary-500" />
          <h3 className="text-xs font-mono font-bold uppercase text-primary-500 tracking-wider">
            Memory Impact Evaluation: What Changed Because of Hindsight?
          </h3>
        </div>
        <p className="text-xs text-text-primary leading-relaxed font-sans">
          {what_changed_summary}
        </p>
      </div>

      {/* Side-by-side grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Column 1: Memory OFF */}
        <div className="bg-surface border border-border rounded-lg overflow-hidden flex flex-col">
          <div className="p-4 bg-background/60 border-b border-border flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-text-muted" />
              <h4 className="text-xs font-mono font-bold uppercase text-text-muted">
                Without Organizational Memory
              </h4>
            </div>
            <span className="badge-mono bg-border text-text-muted">Memory OFF</span>
          </div>

          <div className="p-4 space-y-4 flex-1">
            <div className="space-y-1">
              <span className="text-[11px] font-mono text-text-muted block">Recommendation</span>
              <div className="p-3 rounded bg-background border border-border/60 text-xs text-text-secondary leading-relaxed">
                {without_memory.recommendation}
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-[11px] font-mono text-text-muted block">Historical Context</span>
              <div className="p-3 rounded bg-background border border-border/60 text-xs text-text-muted italic">
                {without_memory.historical_context}
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-[11px] font-mono text-text-muted block">Previous Decisions Consulted</span>
              <div className="p-3 rounded bg-background border border-border/60 text-xs text-text-muted">
                None (Bypassed)
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-[11px] font-mono text-text-muted block">Observed Outcomes</span>
              <div className="p-3 rounded bg-background border border-border/60 text-xs text-text-muted">
                {without_memory.observed_outcomes}
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-[11px] font-mono text-text-muted block">Suggested Next Step</span>
              <div className="p-3 rounded bg-background border border-border/60 text-xs text-text-secondary">
                {without_memory.suggested_next_step}
              </div>
            </div>
          </div>
        </div>

        {/* Column 2: Hindsight Memory ON */}
        <div className="bg-surface border border-primary-500/40 rounded-lg overflow-hidden flex flex-col shadow-lg shadow-primary-500/5">
          <div className="p-4 bg-primary-600/15 border-b border-primary-500/30 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-success-500 animate-pulse" />
              <h4 className="text-xs font-mono font-bold uppercase text-primary-500 tracking-wider">
                With Hindsight Memory
              </h4>
            </div>
            <span className="badge-mono bg-success-500/10 text-success-500 border-success-500/30">
              Hindsight ON
            </span>
          </div>

          <div className="p-4 space-y-4 flex-1">
            <div className="space-y-1">
              <span className="text-[11px] font-mono text-primary-500 font-semibold block">Grounded Recommendation</span>
              <div className="p-3 rounded bg-background border border-primary-500/30 text-xs text-text-primary leading-relaxed font-medium">
                {with_memory.recommendation}
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-[11px] font-mono text-text-muted block">Original Organizational Context</span>
              <div className="p-3 rounded bg-background border border-border text-xs text-text-secondary leading-relaxed">
                {with_memory.historical_context}
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-[11px] font-mono text-text-muted block">Previous Decisions & Rejected Alternatives</span>
              <div className="p-3 rounded bg-background border border-border space-y-2">
                {with_memory.previous_decisions.length > 0 && (
                  <div>
                    <span className="text-[10px] font-mono text-text-muted uppercase block">Past Decisions:</span>
                    <ul className="list-disc list-inside text-xs text-text-primary">
                      {with_memory.previous_decisions.map((d, i) => (
                        <li key={i}>{d}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {with_memory.alternatives_rejected.length > 0 && (
                  <div className="pt-1">
                    <span className="text-[10px] font-mono text-danger-500 uppercase block">Rejected Options:</span>
                    <ul className="space-y-1 text-xs text-text-secondary">
                      {with_memory.alternatives_rejected.map((alt, i) => (
                        <li key={i} className="flex items-start gap-1">
                          <span className="font-semibold text-text-primary">{alt.option}:</span>
                          <span>{alt.reason || 'Not chosen'}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-[11px] font-mono text-success-500 font-semibold block">Actual Measured Outcome</span>
              <div className="p-3 rounded bg-background border border-success-500/30 text-xs text-text-primary">
                {with_memory.observed_outcomes}
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-[11px] font-mono text-text-muted block">Suggested Next Step</span>
              <div className="p-3 rounded bg-background border border-border text-xs text-text-primary font-medium flex items-center gap-2">
                <ArrowRight className="w-3.5 h-3.5 text-primary-500 flex-shrink-0" />
                <span>{with_memory.suggested_next_step}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
