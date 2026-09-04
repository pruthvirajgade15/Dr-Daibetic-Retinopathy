"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { screeningApi } from "../../lib/api";
import { HistoryItem } from "../../types/screening";
import { History, Eye, ArrowRight, Activity } from "lucide-react";
import { getGradeColor } from "../../lib/utils";

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    screeningApi.getHistory()
      .then((data) => setHistory(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
          <History className="w-5 h-5" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white">Patient Screening Archives</h1>
          <p className="text-xs text-slate-400">Historical database of clinical examinations and AI diagnostics.</p>
        </div>
      </div>

      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
        {loading ? (
          <p className="text-xs text-slate-400 py-12 text-center">Loading examination records...</p>
        ) : history.length === 0 ? (
          <div className="text-center py-12 space-y-3">
            <p className="text-xs text-slate-400">No examination history found.</p>
            <Link
              href="/screening"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs"
            >
              Start First Screening <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Patient Identifier</th>
                  <th className="py-3 px-4">Eye</th>
                  <th className="py-3 px-4">Diagnosis & Stage</th>
                  <th className="py-3 px-4">Confidence</th>
                  <th className="py-3 px-4">IQA Index</th>
                  <th className="py-3 px-4">Referral Status</th>
                  <th className="py-3 px-4">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                {history.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-3.5 px-4 font-mono font-bold text-cyan-400">{item.patient_id}</td>
                    <td className="py-3.5 px-4 font-semibold">{item.eye}</td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2.5 py-1 rounded-full text-[11px] font-bold border ${getGradeColor(item.predicted_grade)}`}>
                        {item.predicted_stage}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-mono">{item.confidence}%</td>
                    <td className="py-3.5 px-4 font-mono">{item.quality_score}%</td>
                    <td className="py-3.5 px-4">
                      {item.is_referable ? (
                        <span className="text-amber-400 font-semibold">Ophthalmology Referral</span>
                      ) : (
                        <span className="text-emerald-400 font-semibold">Routine Check</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4">
                      <Link
                        href={`/results/${item.id}`}
                        className="inline-flex items-center gap-1 text-cyan-400 hover:text-cyan-300 font-semibold hover:underline"
                      >
                        Details <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
