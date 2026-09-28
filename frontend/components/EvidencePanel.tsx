'use client';

import React from 'react';
import { ShieldCheck, History, XCircle, TrendingUp, AlertCircle, FileText } from 'lucide-react';
import { HistoricalEvidenceItem } from '@/lib/types';

interface EvidencePanelProps {
  evidence: HistoricalEvidenceItem[];
  confidence: string;
  historicalContext?: string;
  tradeOffs?: string;
  observedOutcomes?: string;
}

export default function EvidencePanel({
  evidence,
  confidence,
  historicalContext,
  tradeOffs,
  observedOutcomes
}: EvidencePanelProps) {
  const getBadgeColor = (conf: string) => {
    switch (conf.toLowerCase()) {
      case 'strong':
        return 'bg-success-500/10 text-success-500 border-success-500/30';
      case 'moderate':
        return 'bg-primary-500/10 text-primary-500 border-primary-500/30';
      case 'limited':
        return 'bg-warning-500/10 text-warning-500 border-warning-500/30';
      default:
        return 'bg-border text-text-muted border-border';
    }
  };

  const getEventIcon = (type: string) => {
    const t = type.toLowerCase();
    if (t.includes('engineering') || t.includes('decision')) return <FileText className="w-3.5 h-3.5 text-primary-500" />;
    if (t.includes('rejected') || t.includes('alternative')) return <XCircle className="w-3.5 h-3.5 text-danger-500" />;
    if (t.includes('outcome')) return <TrendingUp className="w-3.5 h-3.5 text-success-500" />;
    return <History className="w-3.5 h-3.5 text-warning-500" />;
  };

  return (
    <div className="bg-surface border border-border rounded-lg overflow-hidden">
      {/* Evidence Header */}
      <div className="p-4 border-b border-border bg-background/40 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-primary-500" />
          <h3 className="text-xs font-semibold text-text-primary uppercase font-mono tracking-wider">
            Retrieved Historical Evidence
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[11px] text-text-muted font-mono">Memory Confidence:</span>
          <span className={`badge-mono ${getBadgeColor(confidence)}`}>
            {confidence}
          </span>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* Narrative Historical Summary */}
        {historicalContext && (
          <div className="p-3 rounded bg-background border border-border/80">
            <h4 className="text-xs font-mono font-medium text-text-muted mb-1 flex items-center gap-1.5">
              <History className="w-3.5 h-3.5 text-primary-500" />
              Organizational History Summary
            </h4>
            <p className="text-xs text-text-primary leading-relaxed">{historicalContext}</p>
          </div>
        )}

        {/* Evidence List */}
        {evidence.length === 0 ? (
          <div className="p-4 text-center text-xs text-text-muted font-mono border border-dashed border-border rounded">
            No specific historical evidence retrieved.
          </div>
        ) : (
          <div className="space-y-2.5">
            <h4 className="text-xs font-mono font-medium text-text-muted uppercase tracking-wider">
              Evidence Items ({evidence.length})
            </h4>
            {evidence.map((item, idx) => (
              <div key={idx} className="p-3 rounded bg-background border border-border hover:border-border/80 transition-colors space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    {getEventIcon(item.type)}
                    <span className="font-medium text-text-primary">{item.type}</span>
                  </div>
                  <span className="font-mono text-[11px] text-text-muted">{item.date}</span>
                </div>
                <p className="text-xs text-text-primary font-medium">{item.title}</p>
                <p className="text-xs text-text-secondary leading-normal">{item.summary}</p>
                {item.relevance_reason && (
                  <div className="pt-1 text-[11px] text-text-muted font-mono italic">
                    Relevance: {item.relevance_reason}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Observed Outcomes & Trade-offs */}
        {(observedOutcomes || tradeOffs) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 border-t border-border">
            {observedOutcomes && (
              <div className="p-3 rounded bg-background border border-border">
                <span className="text-[11px] font-mono text-success-500 font-semibold block mb-1">Observed Outcome</span>
                <p className="text-xs text-text-secondary leading-normal">{observedOutcomes}</p>
              </div>
            )}
            {tradeOffs && (
              <div className="p-3 rounded bg-background border border-border">
                <span className="text-[11px] font-mono text-warning-500 font-semibold block mb-1">Evaluated Trade-Offs</span>
                <p className="text-xs text-text-secondary leading-normal">{tradeOffs}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
