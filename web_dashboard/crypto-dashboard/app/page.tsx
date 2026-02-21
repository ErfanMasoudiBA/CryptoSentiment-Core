import { Suspense } from "react";
import DashboardContent from "./components/DashboardContent";

export default function Dashboard() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white items-center justify-center p-4">
          <div className="text-center max-w-sm w-full">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-slate-600 border-t-blue-500 mb-4"></div>
            <p className="text-slate-400">Loading dashboard...</p>
          </div>
        </div>
      }
    >
      <DashboardContent />
    </Suspense>
  );
}
