import DayOverview from "../components/Day";

export default function DayOverviewPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh]">
      <div className="w-full max-w-2xl bg-white/90 rounded-3xl shadow-xl p-0 md:p-8 border border-blue-100 relative">
        <div className="absolute -top-6 left-1/2 -translate-x-1/2 flex items-center gap-2">
          <span className="bg-gradient-to-r from-pink-400 to-red-400 text-white px-4 py-1 rounded-full text-xs font-semibold shadow">Today&apos;s Cycle Overview</span>
        </div>
        <DayOverview />
      </div>
    </div>
  );
}