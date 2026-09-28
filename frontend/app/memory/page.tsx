'use client';

import React, { useEffect, useState } from 'react';
import Header from '@/components/Header';
import { api } from '@/lib/api';
import { MemoryEvent } from '@/lib/types';
import { BrainCircuit, Search, Database, Layers, X } from 'lucide-react';

export default function MemoryPage() {
  const [events, setEvents] = useState<MemoryEvent[]>([]);
  const [insights, setInsights] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedType, setSelectedType] = useState<string>('ALL');
  const [selectedEvent, setSelectedEvent] = useState<MemoryEvent | null>(null);

  useEffect(() => {
    Promise.all([
      api.getMemoryEvents(),
      api.getMemoryInsights()
    ]).then(([evs, ins]) => {
      setEvents(evs);
      setInsights(ins);
    }).catch(err => console.error('Memory fetch error', err))
    .finally(() => setLoading(false));
  }, []);

  const filtered = selectedType === 'ALL'
    ? events
    : events.filter(e => e.memory_type === selectedType);

  const getMemoryBadge = (type: string) => {
    switch (type) {
      case 'FEEDBACK':
        return 'bg-warning-500/10 text-warning-500 border-warning-500/30';
      case 'PRODUCT_DECISION':
        return 'bg-primary-500/10 text-primary-500 border-primary-500/30';
      case 'ENGINEERING_DECISION':
      case 'ARCHITECTURE_DECISION':
        return 'bg-primary-600/20 text-primary-500 border-primary-500/40';
      case 'ALTERNATIVE_REJECTED':
        return 'bg-danger-500/10 text-danger-500 border-danger-500/30';
      case 'OUTCOME':
      case 'LESSON':
        return 'bg-success-500/10 text-success-500 border-success-500/30';
      default:
        return 'bg-border text-text-muted border-border';
    }
  };

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Hindsight Organizational Memory Explorer" subtitle="Direct visibility into retained facts, entity graphs, and lessons." />

      <div className="p-6 space-y-6">
        {/* Stats Row */}
        {insights && (
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
            <div className="p-3 rounded-lg bg-surface border border-border">
              <span className="text-[10px] font-mono text-text-muted uppercase">Total Retained</span>
              <p className="text-lg font-bold font-mono text-primary-500 mt-0.5">{insights.total_memories}</p>
            </div>
            <div className="p-3 rounded-lg bg-surface border border-border">
              <span className="text-[10px] font-mono text-text-muted uppercase">Feedback</span>
              <p className="text-lg font-bold font-mono text-text-primary mt-0.5">{insights.counts_by_type?.FEEDBACK || 0}</p>
            </div>
            <div className="p-3 rounded-lg bg-surface border border-border">
              <span className="text-[10px] font-mono text-text-muted uppercase">Product Dec.</span>
              <p className="text-lg font-bold font-mono text-text-primary mt-0.5">{insights.counts_by_type?.PRODUCT_DECISION || 0}</p>
            </div>
            <div className="p-3 rounded-lg bg-surface border border-border">
              <span className="text-[10px] font-mono text-text-muted uppercase">Eng ADRs</span>
              <p className="text-lg font-bold font-mono text-text-primary mt-0.5">{insights.counts_by_type?.ENGINEERING_DECISION || 0}</p>
            </div>
            <div className="p-3 rounded-lg bg-surface border border-border">
              <span className="text-[10px] font-mono text-text-muted uppercase">Rejected Options</span>
              <p className="text-lg font-bold font-mono text-danger-500 mt-0.5">{insights.counts_by_type?.ALTERNATIVE_REJECTED || 0}</p>
            </div>
            <div className="p-3 rounded-lg bg-surface border border-border">
              <span className="text-[10px] font-mono text-text-muted uppercase">Outcomes</span>
              <p className="text-lg font-bold font-mono text-success-500 mt-0.5">{insights.counts_by_type?.OUTCOME || 0}</p>
            </div>
            <div className="p-3 rounded-lg bg-surface border border-border">
              <span className="text-[10px] font-mono text-text-muted uppercase">Lessons</span>
              <p className="text-lg font-bold font-mono text-success-500 mt-0.5">{insights.counts_by_type?.LESSON || 0}</p>
            </div>
          </div>
        )}

        {/* Category Filters */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
          {['ALL', 'FEEDBACK', 'PRODUCT_DECISION', 'ENGINEERING_DECISION', 'ALTERNATIVE_REJECTED', 'OUTCOME', 'LESSON'].map((t) => (
            <button
              key={t}
              onClick={() => setSelectedType(t)}
              className={`px-3 py-1.5 rounded-full font-mono text-xs border transition-colors whitespace-nowrap ${
                selectedType === t
                  ? 'bg-primary-600/20 text-primary-500 border-primary-500/40 font-semibold'
                  : 'bg-surface text-text-muted border-border hover:text-text-primary'
              }`}
            >
              {t.replace('_', ' ')}
            </button>
          ))}
        </div>

        {/* Memory Event Cards */}
        {loading ? (
          <div className="p-12 text-center text-xs font-mono text-text-muted">Loading Hindsight memory index...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map((mem) => (
              <div
                key={mem.id}
                onClick={() => setSelectedEvent(mem)}
                className="bg-surface border border-border rounded-lg p-4 space-y-3 hover:border-primary-500/40 cursor-pointer transition-colors"
              >
                <div className="flex items-center justify-between">
                  <span className={`badge-mono ${getMemoryBadge(mem.memory_type)}`}>
                    {mem.memory_type.replace('_', ' ')}
                  </span>
                  <span className="font-mono text-[11px] text-text-muted">{mem.date}</span>
                </div>

                <div>
                  <h4 className="text-xs font-semibold text-text-primary line-clamp-2">{mem.summary}</h4>
                  <p className="text-[11px] text-text-secondary line-clamp-3 mt-1">{mem.content}</p>
                </div>

                <div className="pt-2 border-t border-border flex items-center justify-between text-[10px] font-mono text-text-muted">
                  <span>Area: {mem.product_area || mem.technology || 'General'}</span>
                  <span className="text-primary-500">ID: {mem.id}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Complete Memory Modal */}
      {selectedEvent && (
        <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4">
          <div className="bg-surface border border-border rounded-lg w-full max-w-2xl p-6 space-y-4 text-xs">
            <div className="flex items-center justify-between border-b border-border pb-3">
              <div className="flex items-center gap-2">
                <BrainCircuit className="w-5 h-5 text-primary-500" />
                <h3 className="font-mono font-bold text-text-primary uppercase">Memory Detail [{selectedEvent.id}]</h3>
              </div>
              <button onClick={() => setSelectedEvent(null)} className="text-text-muted hover:text-text-primary">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between font-mono">
                <span className={`badge-mono ${getMemoryBadge(selectedEvent.memory_type)}`}>
                  {selectedEvent.memory_type}
                </span>
                <span className="text-text-muted">Recorded Date: {selectedEvent.date}</span>
              </div>

              <div className="p-3 rounded bg-background border border-border space-y-1">
                <span className="font-mono text-[10px] uppercase text-text-muted">Summary Title</span>
                <p className="font-semibold text-text-primary">{selectedEvent.summary}</p>
              </div>

              <div className="p-3 rounded bg-background border border-border space-y-1">
                <span className="font-mono text-[10px] uppercase text-text-muted">Durable Content Payload</span>
                <p className="text-text-secondary leading-relaxed whitespace-pre-wrap">{selectedEvent.content}</p>
              </div>

              <div className="p-3 rounded bg-background border border-border flex items-center justify-between font-mono text-[11px]">
                <span>Hindsight Bank ID: <strong>product-engineering-memory</strong></span>
                <span>External Hindsight ID: <strong>{selectedEvent.hindsight_memory_id || 'retained'}</strong></span>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button onClick={() => setSelectedEvent(null)} className="px-4 py-1.5 rounded bg-primary-600 text-white font-medium">
                Close Memory View
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
