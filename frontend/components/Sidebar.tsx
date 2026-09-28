'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  MessageSquareText,
  Lightbulb,
  Cpu,
  FlaskConical,
  GitCommit,
  BrainCircuit,
  Bot,
  RefreshCw,
  Database,
  Trash2,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { api } from '@/lib/api';
import { HindsightStatus } from '@/lib/types';

export default function Sidebar() {
  const pathname = usePathname();
  const [status, setStatus] = useState<HindsightStatus | null>(null);
  const [loadingDemo, setLoadingDemo] = useState(false);
  const [demoMessage, setDemoMessage] = useState('');

  const navItems = [
    { href: '/', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/feedback', label: 'Feedback', icon: MessageSquareText },
    { href: '/product-decisions', label: 'Product Decisions', icon: Lightbulb },
    { href: '/engineering-decisions', label: 'Engineering Decisions', icon: Cpu },
    { href: '/experiments', label: 'Experiments', icon: FlaskConical },
    { href: '/timeline', label: 'Timeline', icon: GitCommit },
    { href: '/memory', label: 'Memory Explorer', icon: BrainCircuit },
    { href: '/advisor', label: 'AI Advisor', icon: Bot },
  ];

  const fetchStatus = async () => {
    try {
      const data = await api.getHindsightStatus();
      setStatus(data);
    } catch (err) {
      console.error('Failed to load Hindsight status', err);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const handleLoadDemo = async () => {
    setLoadingDemo(true);
    setDemoMessage('Seeding demo data...');
    try {
      await api.loadDemoData();
      setDemoMessage('Demo data loaded!');
      await fetchStatus();
      window.location.reload();
    } catch (err) {
      setDemoMessage('Error loading demo data');
    } finally {
      setLoadingDemo(false);
      setTimeout(() => setDemoMessage(''), 3000);
    }
  };

  const handleResetDemo = async () => {
    if (!confirm('Reset all demo data to baseline state?')) return;
    setLoadingDemo(true);
    setDemoMessage('Resetting demo...');
    try {
      await api.resetDemoData();
      setDemoMessage('Demo reset complete!');
      await fetchStatus();
      window.location.reload();
    } catch (err) {
      setDemoMessage('Error resetting demo');
    } finally {
      setLoadingDemo(false);
      setTimeout(() => setDemoMessage(''), 3000);
    }
  };

  const handleClearAllData = async () => {
    if (!confirm('Wipe all mock data to start fresh with real company data?')) return;
    setLoadingDemo(true);
    setDemoMessage('Clearing mock data...');
    try {
      await api.clearAllData();
      setDemoMessage('Database cleared!');
      await fetchStatus();
      window.location.reload();
    } catch (err) {
      setDemoMessage('Error clearing data');
    } finally {
      setLoadingDemo(false);
      setTimeout(() => setDemoMessage(''), 3000);
    }
  };

  return (
    <aside className="w-64 bg-surface border-r border-border flex flex-col h-screen sticky top-0 select-none z-30">
      {/* Brand Header */}
      <div className="p-4 border-b border-border flex items-center gap-3">
        <div className="w-8 h-8 rounded bg-primary-600 flex items-center justify-center font-bold text-white tracking-wider">
          DM
        </div>
        <div>
          <h1 className="font-semibold text-text-primary text-sm tracking-tight leading-none">Decision Memory</h1>
          <p className="text-[11px] text-text-muted mt-1 leading-tight font-mono">Vectorize Hindsight</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
        <div className="px-3 mb-2 text-[10px] font-mono uppercase text-text-muted tracking-wider">Navigation</div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-2.5 px-3 py-2 rounded-md text-xs font-medium transition-colors ${
                isActive
                  ? 'bg-primary-600/15 text-primary-500 font-semibold border border-primary-500/30'
                  : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-primary-500' : 'text-text-muted'}`} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Bottom Hindsight Status & Actions */}
      <div className="p-3 border-t border-border bg-background/50 space-y-3 text-xs">
        {/* Status card */}
        <div className="p-2.5 rounded bg-surface border border-border space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono text-text-muted uppercase tracking-wider">Memory Engine</span>
            <div className="flex items-center gap-1.5">
              <span className={`w-2 h-2 rounded-full ${status?.connected ? 'bg-success-500 animate-pulse' : 'bg-warning-500'}`} />
              <span className="text-[11px] font-mono text-text-primary font-medium">
                {status?.connected ? 'Active' : 'Offline'}
              </span>
            </div>
          </div>

          <div className="text-[11px] text-text-secondary truncate">
            Bank: <span className="font-mono text-text-primary">{status?.bank_id || 'product-engineering-memory'}</span>
          </div>

          <div className="text-[10px] text-text-muted flex items-center justify-between">
            <span>Retained Memories:</span>
            <span className="font-mono text-primary-500 font-semibold">{status?.total_memories_retained ?? 0}</span>
          </div>
        </div>

        {/* Demo Data Buttons */}
        <div className="space-y-1.5">
          <button
            onClick={handleLoadDemo}
            disabled={loadingDemo}
            className="w-full flex items-center justify-center gap-2 px-3 py-1.5 rounded bg-surface hover:bg-surface-hover border border-border text-text-secondary hover:text-text-primary text-xs font-medium transition-colors"
          >
            <Database className="w-3.5 h-3.5 text-text-muted" />
            <span>Load Demo Data</span>
          </button>

          <button
            onClick={handleResetDemo}
            disabled={loadingDemo}
            className="w-full flex items-center justify-center gap-2 px-3 py-1.5 rounded bg-surface hover:bg-surface-hover border border-border text-text-muted hover:text-text-primary text-xs font-medium transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-text-muted ${loadingDemo ? 'animate-spin' : ''}`} />
            <span>Reset Demo Data</span>
          </button>

          <button
            onClick={handleClearAllData}
            disabled={loadingDemo}
            className="w-full flex items-center justify-center gap-2 px-3 py-1 rounded bg-danger-500/10 hover:bg-danger-500/20 border border-danger-500/30 text-danger-500 text-[11px] font-mono font-medium transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5 text-danger-500" />
            <span>Clear Data (Start Fresh)</span>
          </button>
          {demoMessage && (
            <p className="text-[10px] font-mono text-center text-primary-500 mt-1">{demoMessage}</p>
          )}
        </div>
      </div>
    </aside>
  );
}
