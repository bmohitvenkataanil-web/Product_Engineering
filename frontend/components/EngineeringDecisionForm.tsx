'use client';

import React, { useState } from 'react';
import { EngineeringDecisionCreate, AlternativeOption } from '@/lib/types';
import { api } from '@/lib/api';
import { X, Plus, Trash2 } from 'lucide-react';

interface EngineeringDecisionFormProps {
  onClose: () => void;
  onSuccess: () => void;
}

export default function EngineeringDecisionForm({ onClose, onSuccess }: EngineeringDecisionFormProps) {
  const [formData, setFormData] = useState<EngineeringDecisionCreate>({
    title: '',
    problem: '',
    context: '',
    decision: '',
    alternatives_considered: ['Elasticsearch', 'OpenSearch'],
    rejected_alternatives: [
      { name: 'Elasticsearch', reason_rejected: 'Operational complexity not justified at current scale.' }
    ],
    constraints: '',
    trade_offs: '',
    expected_consequences: '',
    actual_consequences: '',
    technology: 'PostgreSQL',
    architecture_area: 'Search & Storage',
    date: new Date().toISOString().split('T')[0],
    status: 'Accepted',
  });
  const [submitting, setSubmitting] = useState(false);

  const handleRejectedChange = (idx: number, field: keyof AlternativeOption, val: string) => {
    const updated = [...formData.rejected_alternatives];
    updated[idx] = { ...updated[idx], [field]: val };
    setFormData({ ...formData, rejected_alternatives: updated });
  };

  const addRejectedAlt = () => {
    setFormData({
      ...formData,
      rejected_alternatives: [...formData.rejected_alternatives, { name: '', reason_rejected: '' }]
    });
  };

  const removeRejectedAlt = (idx: number) => {
    setFormData({
      ...formData,
      rejected_alternatives: formData.rejected_alternatives.filter((_, i) => i !== idx)
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.createEngineeringDecision(formData);
      onSuccess();
      onClose();
    } catch (err) {
      console.error('Failed to create engineering ADR', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4">
      <div className="bg-surface border border-border rounded-lg w-full max-w-3xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
        <div className="p-4 border-b border-border bg-background flex items-center justify-between">
          <h3 className="text-xs font-mono font-bold text-text-primary uppercase tracking-wider">
            Record Architecture Decision Record (ADR)
          </h3>
          <button onClick={onClose} className="p-1 text-text-muted hover:text-text-primary">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4 overflow-y-auto flex-1 text-xs">
          <div className="space-y-1">
            <label className="font-mono text-text-muted">ADR Title *</label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g. Use PostgreSQL for Search Optimization"
              className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
            />
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div className="space-y-1">
              <label className="font-mono text-text-muted">Technology *</label>
              <select
                value={formData.technology}
                onChange={(e) => setFormData({ ...formData, technology: e.target.value })}
                className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
              >
                <option value="PostgreSQL">PostgreSQL</option>
                <option value="Redis">Redis</option>
                <option value="Background Workers">Background Workers</option>
                <option value="FastAPI">FastAPI</option>
                <option value="React / Next.js">React / Next.js</option>
                <option value="Elasticsearch">Elasticsearch</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="font-mono text-text-muted">Architecture Area *</label>
              <input
                type="text"
                required
                value={formData.architecture_area}
                onChange={(e) => setFormData({ ...formData, architecture_area: e.target.value })}
                placeholder="e.g. Search & Storage"
                className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
              />
            </div>

            <div className="space-y-1">
              <label className="font-mono text-text-muted">Date *</label>
              <input
                type="date"
                required
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="font-mono text-text-muted">Problem & Context *</label>
            <textarea
              required
              rows={2}
              value={formData.problem}
              onChange={(e) => setFormData({ ...formData, problem: e.target.value })}
              placeholder="What technical problem, bottleneck, or constraint motivated this decision?"
              className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
            />
          </div>

          <div className="space-y-1">
            <label className="font-mono text-text-muted">Engineering Decision *</label>
            <textarea
              required
              rows={2}
              value={formData.decision}
              onChange={(e) => setFormData({ ...formData, decision: e.target.value })}
              placeholder="What exact engineering approach was selected?"
              className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
            />
          </div>

          {/* Rejected Alternatives Section */}
          <div className="space-y-2 pt-2 border-t border-border">
            <label className="font-mono text-text-muted font-semibold block">
              Rejected Alternatives & Reasons (Crucial for Hindsight Memory)
            </label>
            {formData.rejected_alternatives.map((alt, idx) => (
              <div key={idx} className="grid grid-cols-12 gap-2 items-center bg-background p-2 rounded border border-border">
                <input
                  type="text"
                  placeholder="Rejected Option (e.g. Elasticsearch)"
                  value={alt.name}
                  onChange={(e) => handleRejectedChange(idx, 'name', e.target.value)}
                  className="col-span-4 bg-surface border border-border rounded px-2.5 py-1 text-text-primary focus:outline-none focus:border-primary-500"
                />
                <input
                  type="text"
                  placeholder="Reason Rejected (e.g. Operational complexity)"
                  value={alt.reason_rejected || ''}
                  onChange={(e) => handleRejectedChange(idx, 'reason_rejected', e.target.value)}
                  className="col-span-7 bg-surface border border-border rounded px-2.5 py-1 text-text-primary focus:outline-none focus:border-primary-500"
                />
                <button
                  type="button"
                  onClick={() => removeRejectedAlt(idx)}
                  className="col-span-1 text-text-muted hover:text-danger-500 flex justify-center"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
            <button
              type="button"
              onClick={addRejectedAlt}
              className="flex items-center gap-1 text-primary-500 hover:underline font-mono text-[11px]"
            >
              <Plus className="w-3.5 h-3.5" /> Add Rejected Alternative
            </button>
          </div>

          <div className="grid grid-cols-2 gap-4 pt-2 border-t border-border">
            <div className="space-y-1">
              <label className="font-mono text-text-muted">Constraints</label>
              <input
                type="text"
                value={formData.constraints || ''}
                onChange={(e) => setFormData({ ...formData, constraints: e.target.value })}
                placeholder="e.g. Keep infrastructure simple, no extra cluster"
                className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
              />
            </div>
            <div className="space-y-1">
              <label className="font-mono text-text-muted">Trade-offs</label>
              <input
                type="text"
                value={formData.trade_offs || ''}
                onChange={(e) => setFormData({ ...formData, trade_offs: e.target.value })}
                placeholder="e.g. Lower operational cost vs less specialized search features"
                className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="font-mono text-text-muted">Expected Consequences</label>
              <input
                type="text"
                value={formData.expected_consequences || ''}
                onChange={(e) => setFormData({ ...formData, expected_consequences: e.target.value })}
                placeholder="e.g. Search latency <300ms without new dependencies"
                className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
              />
            </div>
            <div className="space-y-1">
              <label className="font-mono text-text-muted">Actual Consequences / Measured Outcome</label>
              <input
                type="text"
                value={formData.actual_consequences || ''}
                onChange={(e) => setFormData({ ...formData, actual_consequences: e.target.value })}
                placeholder="e.g. Search latency decreased 42%"
                className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
              />
            </div>
          </div>

          <div className="pt-4 border-t border-border flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded border border-border text-text-muted hover:text-text-primary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-4 py-2 rounded bg-primary-600 hover:bg-primary-700 text-white font-medium"
            >
              {submitting ? 'Retaining ADR in Hindsight...' : 'Save ADR & Retain Experience'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
