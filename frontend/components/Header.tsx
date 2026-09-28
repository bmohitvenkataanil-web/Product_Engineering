'use client';

import React from 'react';
import Link from 'next/link';
import { Bot, Layers, ArrowRight } from 'lucide-react';

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export default function Header({ title, subtitle }: HeaderProps) {
  return (
    <header className="h-14 bg-surface border-b border-border px-6 flex items-center justify-between sticky top-0 z-20">
      <div>
        <h2 className="text-sm font-semibold text-text-primary tracking-tight">{title}</h2>
        {subtitle && <p className="text-xs text-text-muted">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded bg-background border border-border text-xs text-text-muted">
          <Layers className="w-3.5 h-3.5 text-primary-500" />
          <span className="font-mono text-[11px]">Domain: Product & Engineering</span>
        </div>

        <Link
          href="/advisor"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-primary-600 hover:bg-primary-700 text-white text-xs font-medium transition-colors shadow-sm"
        >
          <Bot className="w-3.5 h-3.5" />
          <span>Ask AI Advisor</span>
          <ArrowRight className="w-3 h-3 opacity-70" />
        </Link>
      </div>
    </header>
  );
}
