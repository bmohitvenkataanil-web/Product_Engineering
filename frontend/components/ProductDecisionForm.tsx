'use client';

import React, { useState } from 'react';
import { ProductDecisionCreate } from '@/lib/types';
import { api } from '@/lib/api';
import { X, Plus, Trash2 } from 'lucide-react';

interface ProductDecisionFormProps {
  onClose: () => void;
  onSuccess: () => void;
}

export default function ProductDecisionForm({ onClose, onSuccess }: ProductDecisionFormProps) {
  const [formData, setFormData] = useState<ProductDecisionCreate>({
    title: '',
    problem: '',
    context: '',
    options_considered: ['Option A', 'Option B'],
    chosen_approach: '',
    reason: '',
    expected_outcome: '',
    actual_outcome: '',
    date: new Date().toISOString().split('T')[0],
    status: 'Accepted',
    product_area: 'Search & Relevance',
  });
  const [submitting, setSubmitting] = useState(false);

  const handleOptionChange = (idx: number, val: string) => {
    const updated = [...formData.options_considered];
    updated[idx] = val;
    setFormData({ ...formData, options_considered: updated });
  };

  const addOption = () => {
    setFormData({ ...formData, options_considered: [...formData.options_considered, ''] });
  };

  const removeOption = (idx: number) => {
    setFormData({
      ...formData,
      options_considered: formData.options_considered.filter((_, i) => i !== idx),
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.createProductDecision(formData);
      onSuccess();
      onClose();
    } catch (err) {
      console.error('Failed to create product decision', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4">
      <div className="bg-surface border border-border rounded-lg w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
        <div className="p-4 border-b border-border bg-background flex items-center justify-between">
          <h3 className="text-xs font-mono font-bold text-text-primary uppercase tracking-wider">
            Record New Product Decision
          </h3>
          <button onClick={onClose} className="p-1 text-text-muted hover:text-text-primary">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4 overflow-y-auto flex-1 text-xs">
          <div className="space-y-1">
            <label className="font-mono text-text-muted">Decision Title *</label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g. Simplify Onboarding Flow Architecture"
              className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="font-mono text-text-muted">Product Area *</label>
              <select
                value={formData.product_area}
                onChange={(e) => setFormData({ ...formData, product_area: e.target.value })}
                className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
              >
                <option value="Search & Relevance">Search & Relevance</option>
                <option value="User Onboarding">User Onboarding</option>
                <option value="Notifications">Notifications</option>
                <option value="Billing & Payments">Billing & Payments</option>
                <option value="Data Export">Data Export</option>
                <option value="Analytics Dashboard">Analytics Dashboard</option>
                <option value="Security & Access">Security & Access</option>
              </select>
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
            <label className="font-mono text-text-muted">Problem Statement *</label>
            <textarea
              required
              rows={2}
              value={formData.problem}
              onChange={(e) => setFormData({ ...formData, problem: e.target.value })}
              placeholder="What customer problem or friction triggered this decision?"
              className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
            />
          </div>

          <div className="space-y-1">
            <label className="font-mono text-text-muted">Options Considered</label>
            {formData.options_considered.map((opt, idx) => (
              <div key={idx} className="flex items-center gap-2">
                <input
                  type="text"
                  value={opt}
                  onChange={(e) => handleOptionChange(idx, e.target.value)}
                  placeholder={`Option ${idx + 1}`}
                  className="flex-1 bg-background border border-border rounded px-3 py-1.5 text-text-primary focus:outline-none focus:border-primary-500"
                />
                <button type="button" onClick={() => removeOption(idx)} className="text-text-muted hover:text-danger-500">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
            <button
              type="button"
              onClick={addOption}
              className="mt-1 flex items-center gap-1 text-primary-500 hover:underline font-mono text-[11px]"
            >
              <Plus className="w-3.5 h-3.5" /> Add Option
            </button>
          </div>

          <div className="space-y-1">
            <label className="font-mono text-text-muted">Chosen Approach *</label>
            <input
              type="text"
              required
              value={formData.chosen_approach}
              onChange={(e) => setFormData({ ...formData, chosen_approach: e.target.value })}
              placeholder="Which option was selected?"
              className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
            />
          </div>

          <div className="space-y-1">
            <label className="font-mono text-text-muted">Reasoning *</label>
            <textarea
              required
              rows={2}
              value={formData.reason}
              onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
              placeholder="Why was this option chosen over others? What constraints existed?"
              className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="font-mono text-text-muted">Expected Outcome</label>
              <input
                type="text"
                value={formData.expected_outcome || ''}
                onChange={(e) => setFormData({ ...formData, expected_outcome: e.target.value })}
                placeholder="Target metrics impact"
                className="w-full bg-background border border-border rounded px-3 py-2 text-text-primary focus:outline-none focus:border-primary-500"
              />
            </div>
            <div className="space-y-1">
              <label className="font-mono text-text-muted">Actual Outcome (if known)</label>
              <input
                type="text"
                value={formData.actual_outcome || ''}
                onChange={(e) => setFormData({ ...formData, actual_outcome: e.target.value })}
                placeholder="Observed result after release"
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
              {submitting ? 'Retaining in Hindsight...' : 'Save & Retain Experience'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
