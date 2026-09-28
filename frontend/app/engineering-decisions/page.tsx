'use client';

import React, { useEffect, useState } from 'react';
import Header from '@/components/Header';
import { api } from '@/lib/api';
import { EngineeringDecision } from '@/lib/types';
import EngineeringDecisionForm from '@/components/EngineeringDecisionForm';
import { Cpu, Plus, XCircle, Bot, ArrowRight, ShieldAlert, CheckCircle } from 'lucide-react';
import Link from 'next/link';

export default function EngineeringDecisionsPage() {
  const [decisions, setDecisions] = useState<EngineeringDecision[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedTech, setSelectedTech] = useState<string>('ALL');

  const fetchDecisions = async () => {
    try {
      const data = await api.getEngineeringDecisions();
      setDecisions(data);
    } catch (err) {
      console.error('Failed to load engineering decisions', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDecisions();
  }, []);

  const filtered = selectedTech === 'ALL'
    ? decisions
    : decisions.filter(d => d.technology === selectedTech);

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Engineering Architecture Decision Records (ADRs)" subtitle="Technical decisions, rejected options, constraints & consequences." />

      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-text-primary">Engineering & Architecture Memory</h3>
            <p className="text-xs text-text-muted">Structured ADRs retained in Hindsight to prevent repeating technical mistakes.</p>
          </div>

          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-2 px-3 py-1.5 rounded bg-primary-600 hover:bg-primary-700 text-white text-xs font-medium transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>Create New ADR</span>
          </button>
        </div>

        {/* Tech Filter */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
          {['ALL', 'PostgreSQL', 'Redis', 'Background Workers', 'FastAPI', 'React / Next.js'].map((tech) => (
            <button
              key={tech}
              onClick={() => setSelectedTech(tech)}
              className={`px-3 py-1.5 rounded-full font-mono text-xs border transition-colors whitespace-nowrap ${
                selectedTech === tech
                  ? 'bg-primary-600/20 text-primary-500 border-primary-500/40 font-semibold'
                  : 'bg-surface text-text-muted border-border hover:text-text-primary'
              }`}
            >
              {tech}
            </button>
          ))}
        </div>

        {/* ADR List */}
        {loading ? (
          <div className="p-12 text-center text-xs font-mono text-text-muted">Loading engineering decision records...</div>
        ) : filtered.length === 0 ? (
          <div className="p-12 text-center text-xs font-mono text-text-muted border border-dashed border-border rounded-lg">
            No engineering decision records found for this technology.
          </div>
        ) : (
          <div className="space-y-6">
            {filtered.map((ed) => (
              <div key={ed.id} className="bg-surface border border-border rounded-lg overflow-hidden shadow-md space-y-4 p-5 hover:border-border/80 transition-colors">
                {/* Header */}
                <div className="flex items-start justify-between border-b border-border pb-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs text-primary-500 font-bold">{ed.id}</span>
                      <h4 className="text-sm font-semibold text-text-primary">{ed.title}</h4>
                    </div>
                    <div className="flex items-center gap-3 text-xs font-mono text-text-muted mt-1">
                      <span>Tech: <strong className="text-text-primary">{ed.technology}</strong></span>
                      <span>Area: <strong>{ed.architecture_area}</strong></span>
                      <span>Date: <strong>{ed.date}</strong></span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="badge-mono bg-success-500/10 text-success-500 border-success-500/30">
                      {ed.status}
                    </span>
                    <Link
                      href={`/advisor?q=${encodeURIComponent(`Why are we using ${ed.technology} for ${ed.title}?`)}`}
                      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-background hover:bg-surface-hover border border-border text-xs text-text-secondary hover:text-text-primary font-mono transition-colors"
                    >
                      <Bot className="w-3.5 h-3.5 text-primary-500" />
                      <span>Ask Memory About This</span>
                    </Link>
                  </div>
                </div>

                {/* Main Problem & Decision Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div className="p-3.5 rounded bg-background border border-border space-y-1">
                    <span className="font-mono text-[10px] uppercase text-text-muted font-bold block">Problem & Context</span>
                    <p className="text-text-primary leading-relaxed">{ed.problem}</p>
                    {ed.context && <p className="text-text-muted text-[11px] pt-1 leading-normal">{ed.context}</p>}
                  </div>

                  <div className="p-3.5 rounded bg-background border border-primary-500/30 space-y-1">
                    <span className="font-mono text-[10px] uppercase text-primary-500 font-bold block">Engineering Decision Made</span>
                    <p className="text-text-primary font-medium leading-relaxed">{ed.decision}</p>
                  </div>
                </div>

                {/* Rejected Alternatives Section (Critical Spec Requirement) */}
                <div className="p-3.5 rounded bg-background border border-danger-500/20 space-y-2 text-xs">
                  <div className="flex items-center gap-1.5 text-danger-500 font-mono text-[11px] font-bold uppercase">
                    <XCircle className="w-3.5 h-3.5" />
                    <span>Rejected Alternatives & Historical Reasons</span>
                  </div>

                  {ed.rejected_alternatives && ed.rejected_alternatives.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {ed.rejected_alternatives.map((alt, idx) => (
                        <div key={idx} className="p-2 rounded bg-surface border border-border">
                          <span className="font-semibold text-text-primary">{alt.name}: </span>
                          <span className="text-text-muted text-[11px]">{alt.reason_rejected || 'Not selected'}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-text-muted text-[11px]">No explicit alternatives rejected.</p>
                  )}
                </div>

                {/* Constraints, Trade-offs & Consequences */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs pt-1">
                  {ed.constraints && (
                    <div className="p-2.5 rounded bg-background border border-border">
                      <span className="font-mono text-[10px] uppercase text-text-muted block font-semibold">Constraints</span>
                      <p className="text-text-secondary text-[11px] pt-0.5">{ed.constraints}</p>
                    </div>
                  )}

                  {ed.trade_offs && (
                    <div className="p-2.5 rounded bg-background border border-border">
                      <span className="font-mono text-[10px] uppercase text-warning-500 block font-semibold">Trade-offs</span>
                      <p className="text-text-secondary text-[11px] pt-0.5">{ed.trade_offs}</p>
                    </div>
                  )}

                  {ed.actual_consequences && (
                    <div className="p-2.5 rounded bg-success-500/5 border border-success-500/20">
                      <span className="font-mono text-[10px] uppercase text-success-500 block font-semibold">Actual Outcome</span>
                      <p className="text-text-primary text-[11px] pt-0.5 font-medium">{ed.actual_consequences}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <EngineeringDecisionForm
          onClose={() => setShowModal(false)}
          onSuccess={fetchDecisions}
        />
      )}
    </div>
  );
}
