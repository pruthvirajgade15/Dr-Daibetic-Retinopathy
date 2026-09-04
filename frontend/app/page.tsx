"use client";

import Link from "next/link";
import { Eye, ShieldCheck, Cpu, Layers, ArrowRight, Activity } from "lucide-react";

export default function HomePage() {
  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="text-center space-y-6 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
          <Activity className="w-3.5 h-3.5" /> Clinical Deep Learning & Explainable AI
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white">
          Automated Retinal Screening with{" "}
          <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-indigo-400 bg-clip-text text-transparent">
            Explainable AI
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-400 leading-relaxed">
          Screen Diabetic Retinopathy across the standard 5-Grade ICDR scale with sub-second neural inference, instant Image Quality Assessment (IQA), and anatomical Grad-CAM attention heatmaps.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            href="/screening"
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-sm shadow-lg shadow-cyan-500/25 transition-all hover:scale-105"
          >
            Launch Screening Studio <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-sm transition-all"
          >
            Clinical Dashboard
          </Link>
        </div>
      </section>

      {/* Feature Pillars */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl backdrop-blur-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-white">Automated IQA Verification</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Real-time evaluation of retinal focus, exposure, and illumination prevents ungradable scans from causing diagnostic error.
          </p>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl backdrop-blur-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
            <Cpu className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-white">5-Grade ICDR Staging</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Powered by PyTorch EfficientNet-B0 trained with Class-Balanced Focal Loss for accurate early microaneurysm detection.
          </p>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-2xl backdrop-blur-sm space-y-3">
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
            <Layers className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-white">Explainable AI (Grad-CAM)</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Visual heatmaps pinpoint microaneurysms, hemorrhages, and exudates with anatomical quadrant attention breakdown.
          </p>
        </div>
      </section>
    </div>
  );
}
