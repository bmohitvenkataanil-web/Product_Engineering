'use client';

import React, { useEffect, useState } from 'react';
import Header from '@/components/Header';
import { api } from '@/lib/api';
import { TimelineEvent } from '@/lib/types';
import { GitCommit, AlertTriangle, Lightbulb, Cpu, FlaskConical, TrendingUp, ArrowDown } from 'lucide-react';

export default function TimelinePage() {
  const [events, setEvents] = useState<TimelineEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState<string>('ALL');

  useEffect(() => {
    api.getTimeline()
      .then(setEvents)
      .catch((err) => console.error('Timeline fetch error', err))
      .finally(() => setLoading(false));
  }, []);

  const filtered = filterType === 'ALL'
    ? events
    : events.filter(e => e.type === filterType);

  const getEventBadge = (type: string) => {
    switch (type) {
      case 'Problem':
        return { color: 'bg-danger-500/10 text-danger-500 border-danger-500/30', icon: AlertTriangle };
      case 'Product Decision':
        return { color: 'bg-primary-500/10 text-primary-500 border-primary-500/30', icon: Lightbulb };
      case 'Engineering Decision':
        return { color: 'bg-primary-600/15 text-primary-500 border-primary-500/40', icon: Cpu };
      case 'Experiment':
        return { color: 'bg-warning-500/10 text-warning-500 border-warning-500/30', icon: FlaskConical };
      case 'Outcome':
        return { color: 'bg-success-500/10 text-success-500 border-success-500/30', icon: TrendingUp };
      default:
        return { color: 'bg-border text-text-muted border-border', icon: GitCommit };
    }
  };

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Unified Organizational Timeline" subtitle="Chronological flow: Problem → Decision → Implementation → Outcome → New Decision." />

      <div className="p-6 space-y-6">
        {/* Timeline Header & Filter Bar */}
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-text-primary">Chronological Experience Stream</h3>
            <p className="text-xs text-text-muted">Visualizing how past choices directly led to observed organizational outcomes.</p>
          </div>

          <div className="flex items-center gap-1.5 overflow-x-auto text-xs font-mono">
            {['ALL', 'Problem', 'Product Decision', 'Engineering Decision', 'Experiment', 'Outcome'].map((t) => (
              <button
                key={t}
                onClick={() => setFilterType(t)}
                className={`px-2.5 py-1 rounded text-xs border transition-colors ${
                  filterType === t
                    ? 'bg-primary-600/20 text-primary-500 border-primary-500/40 font-semibold'
                    : 'bg-surface text-text-muted border-border hover:text-text-primary'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* Timeline Stream */}
        {loading ? (
          <div className="p-12 text-center text-xs font-mono text-text-muted">Building organizational timeline stream...</div>
        ) : (
          <div className="relative pl-6 border-l-2 border-border space-y-6">
            {filtered.map((ev, idx) => {
              const badge = getEventBadge(ev.type);
              const Icon = badge.icon;
              return (
                <div key={ev.id} className="relative group">
                  {/* Timeline dot */}
                  <div className="absolute -left-[31px] top-1.5 w-4 h-4 rounded-full bg-background border-2 border-primary-500 flex items-center justify-center">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary-500" />
                  </div>

                  {/* Card Content */}
                  <div className="bg-surface border border-border rounded-lg p-4 space-y-2 hover:border-border/80 transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className={`badge-mono ${badge.color}`}>
                          <Icon className="w-3 h-3 mr-1" />
                          {ev.type}
                        </span>
                        <span className="font-mono text-xs text-text-muted">{ev.date}</span>
                      </div>
                      {ev.product_area && (
                        <span className="font-mono text-[11px] text-primary-500">{ev.product_area}</span>
                      )}
                    </div>

                    <h4 className="text-sm font-semibold text-text-primary">{ev.title}</h4>
                    <p className="text-xs text-text-secondary leading-relaxed">{ev.description}</p>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
