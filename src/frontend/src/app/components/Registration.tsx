"use client"
import { useState, ChangeEvent, FormEvent } from "react";


export default function Registration() {
  const [dob, setDob] = useState("");
  const [lastCycle, setLastCycle] = useState("");
  const [periodLength, setPeriodLength] = useState("");

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    // TODO: Add your signup logic here
    alert(`Submitted:\nDOB: ${dob}\nLast Cycle: ${lastCycle}\nPeriod Length: ${periodLength}`);
  }

  return (
    <div
      className="relative flex min-h-screen flex-col bg-[#f9fbfb] overflow-x-hidden"
      style={{ fontFamily: `"Spline Sans", "Noto Sans", sans-serif` }}
    >
      <div className="flex h-full flex-col grow">
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#e9eff1] px-10 py-3">
          <div className="flex items-center gap-4 text-[#101719]">
            <div className="w-10 h-10">
              <svg
                viewBox="0 0 48 48"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="w-full h-full"
              >
                <path d="M44 4H30.6666V17.3334H17.3334V30.6666H4V44H44V4Z" fill="currentColor" />
              </svg>
            </div>
            <h2 className="text-[#101719] text-lg font-bold leading-tight tracking-[-0.015em]">
              CycleWise
            </h2>
          </div>
        </header>

        <main className="flex justify-center flex-1 py-5 px-10">
          <div className="flex flex-col w-full max-w-[512px] py-5">
            <h2 className="text-center text-[28px] font-bold leading-tight tracking-light text-[#101719] pb-3 pt-5 px-4">
              Fill your Details
            </h2>

            <form className="flex flex-wrap items-end gap-4 px-4 py-3 max-w-[480px]" onSubmit={handleSubmit} noValidate>
              {/* Date of Birth */}
              <label className="flex flex-col flex-1 min-w-[10rem]">
                <input
                  type="date"
                  placeholder="Date of Birth (MM/DD/YYYY)"
                  value={dob}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => setDob(e.target.value)}
                  className="form-input w-full rounded-xl bg-[#e9eff1] p-4 text-[#101719] text-base font-normal leading-normal placeholder:text-[#57818e] h-14 border-none focus:outline-none focus:ring-0 focus:border-none resize-none"
                  required
                />
              </label>

              {/* Last Cycle Date */}
              <label className="flex flex-col flex-1 min-w-[10rem]">
                <input
                  type="text"
                  placeholder="Last Cycle Date (MM/DD)"
                  value={lastCycle}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => setLastCycle(e.target.value)}
                  className="form-input w-full rounded-xl bg-[#e9eff1] p-4 text-[#101719] text-base font-normal leading-normal placeholder:text-[#57818e] h-14 border-none focus:outline-none focus:ring-0 focus:border-none resize-none"
                  pattern="^(0[1-9]|1[0-2])\/([0-2][0-9]|3[01])$"
                  title="Format: MM/DD"
                  required
                />
              </label>

              {/* Period Length */}
              <label className="flex flex-col flex-1 min-w-[10rem]">
                <input
                  type="number"
                  placeholder="Period Length (days)"
                  value={periodLength}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => setPeriodLength(e.target.value)}
                  className="form-input w-full rounded-xl bg-[#e9eff1] p-4 text-[#101719] text-base font-normal leading-normal placeholder:text-[#57818e] h-14 border-none focus:outline-none focus:ring-0 focus:border-none resize-none"
                  min={1}
                  max={14}
                  required
                />
              </label>

              <p className="text-[#57818e] text-sm font-normal leading-normal w-full px-4 pt-1 pb-3">
                By signing up, you agree to our Terms of Service and Privacy Policy.
              </p>

              <div className="w-full px-4 py-3">
                <button
                  type="submit"
                  className="flex items-center justify-center w-full min-w-[84px] max-w-[480px] h-10 px-4 rounded-full bg-[#addbea] text-[#101719] text-sm font-bold leading-normal tracking-[0.015em] cursor-pointer"
                >
                  <span className="truncate">Sign Up</span>
                </button>
              </div>
            </form>
          </div>
        </main>
      </div>
    </div>
  );
}
