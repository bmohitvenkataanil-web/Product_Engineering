'use client';

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Header from '@/components/Header';
import { api } from '@/lib/api';
import { AdviceResponse, CompareAdviceResponse } from '@/lib/types';
import EvidencePanel from '@/components/EvidencePanel';
import CompareMemoryView from '@/components/CompareMemoryView';
import { Bot, BrainCircuit, Search, ArrowRight, ShieldCheck, RefreshCw, XCircle, Layers } from 'lucide-react';

function AdvisorContent() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams ? searchParams.get('q') || '' : '';

  const [question, setQuestion] = useState(initialQuery);
  const [domain, setDomain] = useState<'Product' | 'Engineering' | 'Both'>('Both');
  const [memoryMode, setMemoryMode] = useState<'ON' | 'OFF'>('ON');
  const [isCompare, setIsCompare] = useState(false);

  const [loading, setLoading] = useState(false);
  const [adviceResult, setAdviceResult] = useState<AdviceResponse | null>(null);
  const [compareResult, setCompareResult] = useState<CompareAdviceResponse | null>(null);

  const exampleQuestions = {
    product: [
      "Customers are still complaining about onboarding verification. What should we change?",
      "Have we tried solving this onboarding friction before?",
      "Why did we simplify billing UI instead of rewriting the engine?"
    ],
    engineering: [
      "Should we migrate search to Elasticsearch?",
      "Why are we using PostgreSQL for search?",
      "What architecture trade-offs did we make for notifications?",
      "What happened the last time we changed notification frequency?",
      "Can we return large data exports synchronously?"
    ],
    combined: [
      "What product and engineering decisions were made around search, and what did we learn?",
      "What happened after we reduced notification frequency?"
    ]
  };

  const runQuery = async (qText?: string, mode?: 'ON' | 'OFF', compare?: boolean) => {
    const targetQ = qText !== undefined ? qText : question;
    const targetMode = mode !== undefined ? mode : memoryMode;
    const targetCompare = compare !== undefined ? compare : isCompare;

    if (!targetQ.trim()) return;

    setLoading(true);
    setAdviceResult(null);
    setCompareResult(null);

    try {
      if (targetCompare) {
        const res = await api.compareAdvice(targetQ, domain);
        setCompareResult(res);
      } else {
        const res = await api.getAdvice(targetQ, domain, targetMode);
        setAdviceResult(res);
      }
    } catch (err) {
      console.error('Advisor query error', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialQuery) {
      runQuery(initialQuery);
    }
  }, [initialQuery]);

  return (
    <div className="p-6 space-y-6">
      {/* Workspace Console Header */}
      <div className="bg-surface border border-border rounded-lg p-5 space-y-4 shadow-sm">
        <div>
          <h3 className="text-sm font-semibold text-text-primary">Decision Intelligence Workspace</h3>
          <p className="text-xs text-text-muted mt-0.5">
            Query durable organizational experience (past decisions, rejected alternatives, constraints, and outcomes) to make grounded choices.
          </p>
        </div>

        {/* Example Prompts */}
        <div className="space-y-2 pt-2 border-t border-border">
          <span className="text-[10px] font-mono uppercase text-text-muted">Example Organizational Queries:</span>
          <div className="flex flex-wrap gap-2">
            {exampleQuestions.engineering.slice(0, 3).map((q, i) => (
              <button
                key={`eng-${i}`}
                onClick={() => { setQuestion(q); runQuery(q); }}
                className="px-2.5 py-1 rounded bg-background hover:bg-surface-hover border border-border text-xs text-text-secondary hover:text-text-primary text-left transition-colors font-mono"
              >
                Eng: &quot;{q}&quot;
              </button>
            ))}
            {exampleQuestions.product.slice(0, 2).map((q, i) => (
              <button
                key={`prod-${i}`}
                onClick={() => { setQuestion(q); runQuery(q); }}
                className="px-2.5 py-1 rounded bg-background hover:bg-surface-hover border border-border text-xs text-primary-500 hover:text-primary-400 text-left transition-colors font-mono"
              >
                Prod: &quot;{q}&quot;
              </button>
            ))}
          </div>
        </div>

        {/* Input & Controls Console */}
        <form onSubmit={(e) => { e.preventDefault(); runQuery(); }} className="space-y-3 pt-2">
          <div className="relative">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask e.g. 'Should we migrate search from PostgreSQL to Elasticsearch?'"
              className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-primary-500 pr-28 shadow-inner"
            />
            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="absolute right-2 top-2 px-4 py-1.5 rounded bg-primary-600 hover:bg-primary-700 text-white text-xs font-medium transition-colors disabled:opacity-50 flex items-center gap-1.5"
            >
              {loading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Bot className="w-3.5 h-3.5" />}
              <span>Evaluate</span>
            </button>
          </div>

          {/* Mode Controls */}
          <div className="flex items-center justify-between text-xs font-mono">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <span className="text-text-muted">Memory Engine:</span>
                <button
                  type="button"
                  onClick={() => { setMemoryMode('ON'); setIsCompare(false); }}
                  className={`px-3 py-1 rounded text-xs border transition-colors ${
                    memoryMode === 'ON' && !isCompare
                      ? 'bg-primary-600/20 text-primary-500 border-primary-500/40 font-bold'
                      : 'bg-background text-text-muted border-border'
                  }`}
                >
                  Hindsight Memory ON
                </button>
                <button
                  type="button"
                  onClick={() => { setMemoryMode('OFF'); setIsCompare(false); }}
                  className={`px-3 py-1 rounded text-xs border transition-colors ${
                    memoryMode === 'OFF' && !isCompare
                      ? 'bg-border text-text-primary border-border-subtle font-bold'
                      : 'bg-background text-text-muted border-border'
                  }`}
                >
                  Memory OFF (Generic)
                </button>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-text-muted">Domain Scope:</span>
                {(['Both', 'Product', 'Engineering'] as const).map((d) => (
                  <button
                    key={d}
                    type="button"
                    onClick={() => setDomain(d)}
                    className={`px-2 py-0.5 rounded border text-[11px] ${
                      domain === d ? 'bg-surface-hover text-text-primary border-border-subtle' : 'text-text-muted border-border'
                    }`}
                  >
                    {d}
                  </button>
                ))}
              </div>
            </div>

            {/* Side-by-Side Compare Toggle */}
            <button
              type="button"
              onClick={() => { setIsCompare(true); runQuery(question, 'ON', true); }}
              className={`px-3 py-1 rounded text-xs border transition-colors flex items-center gap-1.5 ${
                isCompare
                  ? 'bg-success-500/20 text-success-500 border-success-500/40 font-bold'
                  : 'bg-background text-text-secondary border-border hover:text-text-primary'
              }`}
            >
              <BrainCircuit className="w-3.5 h-3.5 text-success-500" />
              <span>Side-by-Side Impact Compare</span>
            </button>
          </div>
        </form>
      </div>

      {/* Loading Spinner */}
      {loading && (
        <div className="bg-surface border border-border rounded-lg p-12 text-center space-y-3">
          <BrainCircuit className="w-8 h-8 text-primary-500 animate-spin mx-auto" />
          <p className="text-xs font-mono text-text-muted">
            Querying Hindsight Memory Bank, retrieving historical decisions, and constructing grounded advice...
          </p>
        </div>
      )}

      {/* Side-by-Side Compare View */}
      {compareResult && !loading && (
        <CompareMemoryView data={compareResult} />
      )}

      {/* Single Advice Result View */}
      {adviceResult && !compareResult && !loading && (
        <div className="space-y-6">
          {/* Grounded Recommendation Header */}
          <div className="bg-surface border border-primary-500/40 rounded-lg p-5 space-y-4 shadow-lg shadow-primary-500/5">
            <div className="flex items-center justify-between border-b border-border pb-3">
              <div className="flex items-center gap-2">
                <Bot className="w-5 h-5 text-primary-500" />
                <h3 className="text-xs font-mono font-bold uppercase text-text-primary tracking-wider">
                  Grounded Recommendation [{adviceResult.memory_mode} Mode]
                </h3>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-mono text-text-muted">Confidence:</span>
                <span className="badge-mono bg-success-500/10 text-success-500 border-success-500/30">
                  {adviceResult.memory_confidence}
                </span>
              </div>
            </div>

            <p className="text-sm font-semibold text-text-primary leading-relaxed">
              {adviceResult.recommendation}
            </p>

            {/* Actionable Next Step */}
            {adviceResult.suggested_next_step && (
              <div className="p-3 rounded bg-background border border-border flex items-center gap-2 text-xs">
                <ArrowRight className="w-4 h-4 text-primary-500 flex-shrink-0" />
                <div>
                  <span className="font-mono text-[10px] uppercase text-text-muted block">Suggested Action</span>
                  <span className="font-medium text-text-primary">{adviceResult.suggested_next_step}</span>
                </div>
              </div>
            )}
          </div>

          {/* Historical Facts & Rejected Alternatives Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {/* Previous Decisions */}
            <div className="bg-surface border border-border rounded-lg p-4 space-y-2">
              <span className="font-mono text-[10px] uppercase text-text-muted font-bold block">Previous Decisions Recalled</span>
              {adviceResult.previous_decisions.length === 0 ? (
                <p className="text-text-muted text-[11px]">No previous decisions recorded.</p>
              ) : (
                <ul className="space-y-1.5 text-text-primary">
                  {adviceResult.previous_decisions.map((d, i) => (
                    <li key={i} className="p-2 rounded bg-background border border-border font-mono text-[11px]">
                      {d}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/* Alternatives Rejected */}
            <div className="bg-surface border border-border rounded-lg p-4 space-y-2">
              <span className="font-mono text-[10px] uppercase text-danger-500 font-bold block">Alternatives Rejected & Reasons</span>
              {adviceResult.alternatives_rejected.length === 0 ? (
                <p className="text-text-muted text-[11px]">No rejected alternatives recorded.</p>
              ) : (
                <ul className="space-y-1.5">
                  {adviceResult.alternatives_rejected.map((alt, i) => (
                    <li key={i} className="p-2 rounded bg-background border border-border text-[11px]">
                      <span className="font-bold text-text-primary">{typeof alt === 'object' ? alt.option : alt}: </span>
                      <span className="text-text-muted">{typeof alt === 'object' ? alt.reason : 'Not selected'}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>

          {/* Evidence Drawer Panel */}
          <EvidencePanel
            evidence={adviceResult.relevant_memories}
            confidence={adviceResult.memory_confidence}
            historicalContext={adviceResult.historical_context}
            tradeOffs={adviceResult.trade_offs}
            observedOutcomes={adviceResult.observed_outcomes}
          />
        </div>
      )}
    </div>
  );
}

export default function AdvisorPage() {
  return (
    <div className="flex-1 flex flex-col">
      <Header title="Decision Intelligence Advisor" subtitle="Ask what your organization learned before making a new product or engineering decision." />
      <Suspense fallback={<div className="p-12 text-center text-xs font-mono text-text-muted">Loading Decision Advisor...</div>}>
        <AdvisorContent />
      </Suspense>
    </div>
  );
}
