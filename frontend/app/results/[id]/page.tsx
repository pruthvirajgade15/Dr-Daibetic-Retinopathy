"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { screeningApi } from "../../../lib/api";
import { HistoryItem } from "../../../types/screening";
import Link from "next/link";
import { ArrowLeft, Activity, ShieldCheck, Clock, ExternalLink } from "lucide-react";
import { getGradeColor } from "../../../lib/utils";
import { ScreeningReport } from "../../../components/ScreeningReport";

export default function ResultDetailPage() {
  const params = useParams();
  const id = params?.id as string;
  const [record, setRecord] = useState<HistoryItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      screeningApi.getHistoryDetail(id)
        .then((data) => setRecord(data))
        .catch((err) => console.error(err))
        .finally(() => setLoading(false));
    }
  }, [id]);

  if (loading) {
    return <div className="text-center py-12 text-slate-400 text-sm">Loading screening details...</div>;
  }

  if (!record) {
    return (
      <div className="text-center py-12 space-y-4">
        <p className="text-slate-400 text-sm">Screening record not found.</p>
        <Link href="/history" className="text-cyan-400 text-xs hover:underline">
          ← Back to History
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <Link href="/history" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white">
        <ArrowLeft className="w-4 h-4" /> Back to History
      </Link>

      <ScreeningReport
        reportUrl={record.report_url}
        patientId={record.patient_id}
        eye={record.eye}
      />

      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-xl font-bold text-white">Screening Record: {record.patient_id}</h1>
            <p className="text-xs text-slate-400">Eye: {record.eye} | Date: {new Date(record.created_at).toLocaleString()}</p>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getGradeColor(record.predicted_grade)}`}>
            Grade {record.predicted_grade}: {record.predicted_stage}
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
            <span className="text-slate-400">Confidence</span>
            <p className="text-lg font-bold text-cyan-400 mt-1">{record.confidence}%</p>
          </div>
          <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
            <span className="text-slate-400">Image Quality</span>
            <p className="text-lg font-bold text-emerald-400 mt-1">{record.quality_score}%</p>
          </div>
          <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
            <span className="text-slate-400">Referral Status</span>
            <p className="text-lg font-bold text-amber-400 mt-1">
              {record.is_referable ? "Referral Required" : "Routine"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
