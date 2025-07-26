
import LearnPage from "../components/LearnPage";

export default function Learn() {
  return (
    <div className="flex flex-col items-center min-h-[70vh]">
      <div className="w-full max-w-4xl bg-white/90 rounded-3xl shadow-xl p-0 md:p-8 border border-blue-100 relative">
        <div className="absolute -top-6 left-1/2 -translate-x-1/2 flex items-center gap-2">
          <span className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-4 py-1 rounded-full text-xs font-semibold shadow">Learn &amp; Explore</span>
        </div>
        <LearnPage />
      </div>
    </div>
  );
}
