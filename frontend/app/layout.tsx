import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "../components/Navbar";

export const metadata: Metadata = {
  title: "DR-Screening-AI | Explainable Retinal Screening Platform",
  description: "Enterprise clinical deep learning and Explainable AI platform for automated Diabetic Retinopathy screening.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100 min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="border-t border-slate-900 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
          <p>
            DR-Screening-AI Clinical Decision Support Platform • For Clinical Screening & Research Use Only.
          </p>
        </footer>
      </body>
    </html>
  );
}
