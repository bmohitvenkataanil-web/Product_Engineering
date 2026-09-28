'use client';

import React, { useEffect, useState } from 'react';
import Header from '@/components/Header';
import { api } from '@/lib/api';
import { DashboardData } from '@/lib/types';
import {
  MessageSquareText, Lightbulb, Cpu, Layers, FlaskConical,
  BrainCircuit, CheckCircle2, AlertCircle, ArrowUpRight, TrendingUp
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, AreaChart, Area
} from 'recharts';

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getDashboardData()
      .then(setData)
      .catch((err) => console.error('Dashboard fetch error', err))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return (
      <div className="flex-1 flex flex-col">
        <Header title="Dashboard" subtitle="Organizational Decision Intelligence" />
        <div className="p-12 text-center text-xs font-mono text-text-muted flex-1 flex items-center justify-center">
          Loading organizational decision memory data...
        </div>
      </div>
    );
  }

  const { metrics, charts, recent_organizational_learning, recent_product_decisions, recent_engineering_decisions, recent_outcomes, recent_feedback } = data;

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#6366f1'];

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Organizational Decision Dashboard" subtitle="Remembering what was decided, why, and what happened afterward." />

      <div className="p-6 space-y-6">
        {/* Top Metric Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
          <div className="p-3 rounded-lg bg-surface border border-border">
            <span className="text-[10px] font-mono text-text-muted uppercase">Total Feedback</span>
            <p className="text-xl font-bold font-mono text-text-primary mt-1">{metrics.total_feedback}</p>
          </div>
          <div className="p-3 rounded-lg bg-surface border border-border">
            <span className="text-[10px] font-mono text-text-muted uppercase">Product Decisions</span>
            <p className="text-xl font-bold font-mono text-primary-500 mt-1">{metrics.product_decisions}</p>
          </div>
          <div className="p-3 rounded-lg bg-surface border border-border">
            <span className="text-[10px] font-mono text-text-muted uppercase">Eng Decisions</span>
            <p className="text-xl font-bold font-mono text-text-primary mt-1">{metrics.engineering_decisions}</p>
          </div>
          <div className="p-3 rounded-lg bg-surface border border-border">
            <span className="text-[10px] font-mono text-text-muted uppercase">Architecture ADRs</span>
            <p className="text-xl font-bold font-mono text-text-primary mt-1">{metrics.architecture_decisions}</p>
          </div>
          <div className="p-3 rounded-lg bg-surface border border-border">
            <span className="text-[10px] font-mono text-text-muted uppercase">Experiments</span>
            <p className="text-xl font-bold font-mono text-text-primary mt-1">{metrics.experiments}</p>
          </div>
          <div className="p-3 rounded-lg bg-surface border border-border">
            <span className="text-[10px] font-mono text-text-muted uppercase">Learned Memory</span>
            <p className="text-xl font-bold font-mono text-primary-500 mt-1">{metrics.learned_experiences}</p>
          </div>
          <div className="p-3 rounded-lg bg-surface border border-border">
            <span className="text-[10px] font-mono text-text-muted uppercase">Successful Outcomes</span>
            <p className="text-xl font-bold font-mono text-success-500 mt-1">{metrics.successful_outcomes}</p>
          </div>
          <div className="p-3 rounded-lg bg-surface border border-border">
            <span className="text-[10px] font-mono text-text-muted uppercase">Open Issues</span>
            <p className="text-xl font-bold font-mono text-warning-500 mt-1">{metrics.unresolved_issues}</p>
          </div>
        </div>

        {/* Recent Organizational Learning Section */}
        <div className="bg-surface border border-border rounded-lg p-4 space-y-3">
          <div className="flex items-center justify-between border-b border-border pb-3">
            <div className="flex items-center gap-2">
              <BrainCircuit className="w-4 h-4 text-primary-500" />
              <h3 className="text-xs font-mono font-bold text-text-primary uppercase tracking-wider">
                Recent Organizational Learning
              </h3>
            </div>
            <span className="text-[11px] font-mono text-text-muted">Synthesized from Hindsight Memory Bank</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {recent_organizational_learning.map((item, idx) => (
              <div key={idx} className="p-3 rounded bg-background border border-border space-y-1.5 hover:border-border/80 transition-colors">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-text-primary">{item.title}</span>
                  <span className="font-mono text-[11px] text-text-muted">{item.date}</span>
                </div>
                <p className="text-xs text-text-secondary leading-relaxed">{item.summary}</p>
                <div className="pt-1 text-[11px] font-mono text-success-500 flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" />
                  <span>Impact: {item.impact}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Chart 1: Feedback Trend */}
          <div className="bg-surface border border-border rounded-lg p-4 space-y-2">
            <h4 className="text-xs font-mono font-bold text-text-muted uppercase">Feedback Volume Trend</h4>
            <div className="h-44">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={charts.feedback_trend}>
                  <XAxis dataKey="date" stroke="#64748b" fontSize={10} tickLine={false} />
                  <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
                  <Tooltip contentStyle={{ background: '#111726', borderColor: '#1e293b', fontSize: '11px' }} />
                  <Area type="monotone" dataKey="count" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.15} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 2: Product & Eng Decisions */}
          <div className="bg-surface border border-border rounded-lg p-4 space-y-2">
            <h4 className="text-xs font-mono font-bold text-text-muted uppercase">Decisions Over Time</h4>
            <div className="h-44">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={charts.engineering_decisions_trend}>
                  <XAxis dataKey="date" stroke="#64748b" fontSize={10} tickLine={false} />
                  <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
                  <Tooltip contentStyle={{ background: '#111726', borderColor: '#1e293b', fontSize: '11px' }} />
                  <Bar dataKey="count" fill="#10b981" radius={[2, 2, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 3: Decisions by Product Area */}
          <div className="bg-surface border border-border rounded-lg p-4 space-y-2">
            <h4 className="text-xs font-mono font-bold text-text-muted uppercase">Decisions by Product Area</h4>
            <div className="h-44">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={charts.decisions_by_area} dataKey="count" nameKey="area" cx="50%" cy="50%" outerRadius={55}>
                    {charts.decisions_by_area.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ background: '#111726', borderColor: '#1e293b', fontSize: '11px' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Recent Decisions & Outcomes Lists */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Recent Engineering Decisions */}
          <div className="bg-surface border border-border rounded-lg p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-border pb-2">
              <h4 className="text-xs font-mono font-bold text-text-primary uppercase">Recent ADR Architecture Decisions</h4>
              <span className="text-[11px] font-mono text-text-muted">Engineering Memory</span>
            </div>
            <div className="space-y-2">
              {recent_engineering_decisions.map((ed) => (
                <div key={ed.id} className="p-2.5 rounded bg-background border border-border flex items-center justify-between text-xs">
                  <div>
                    <div className="font-semibold text-text-primary">{ed.title}</div>
                    <div className="text-[11px] font-mono text-text-muted">Tech: {ed.technology} | {ed.architecture_area}</div>
                  </div>
                  <span className="badge-mono bg-primary-600/15 text-primary-500 border-primary-500/30">
                    {ed.date}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Measured Outcomes */}
          <div className="bg-surface border border-border rounded-lg p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-border pb-2">
              <h4 className="text-xs font-mono font-bold text-text-primary uppercase">Recent Measured Outcomes</h4>
              <span className="text-[11px] font-mono text-text-muted">Post-Implementation Hindsight</span>
            </div>
            <div className="space-y-2">
              {recent_outcomes.map((out) => (
                <div key={out.id} className="p-2.5 rounded bg-background border border-border flex items-center justify-between text-xs">
                  <div>
                    <div className="font-semibold text-text-primary">{out.title}</div>
                    <div className="text-[11px] font-mono text-success-500">Metrics: {out.metrics_impact || 'Impact recorded'}</div>
                  </div>
                  <span className="badge-mono bg-success-500/10 text-success-500 border-success-500/30">
                    {out.date}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
