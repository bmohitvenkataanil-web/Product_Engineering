'use client';

import React, { useEffect, useState } from 'react';
import Header from '@/components/Header';
import FeedbackTable from '@/components/FeedbackTable';
import { api } from '@/lib/api';
import { Feedback } from '@/lib/types';
import { Plus } from 'lucide-react';

export default function FeedbackPage() {
  const [feedbacks, setFeedbacks] = useState<Feedback[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchFeedbacks = async () => {
    try {
      const data = await api.getFeedbacks();
      setFeedbacks(data);
    } catch (err) {
      console.error('Failed to load feedbacks', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeedbacks();
  }, []);

  return (
    <div className="flex-1 flex flex-col">
      <Header title="Customer Feedback Repository" subtitle="Connect customer feedback to historical product & engineering decisions." />

      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-text-primary">Incoming Customer Voice</h3>
            <p className="text-xs text-text-muted">Analyze feedback against retained organizational experience to prevent repeated mistakes.</p>
          </div>
        </div>

        {loading ? (
          <div className="p-12 text-center text-xs font-mono text-text-muted">Loading customer feedback repository...</div>
        ) : (
          <FeedbackTable feedbacks={feedbacks} onRefresh={fetchFeedbacks} />
        )}
      </div>
    </div>
  );
}
