import "./globals.css";
import { ReactNode } from "react";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-100 font-sans text-gray-800">
        <header className="sticky top-0 z-30 w-full bg-white/80 backdrop-blur shadow-sm border-b border-blue-100">
          <nav className="max-w-7xl mx-auto flex items-center justify-between px-6 py-3">
            <div className="flex items-center gap-3">
              <img src="/Logo.png" alt="CycleWise Logo" className="h-10 w-10 rounded-full shadow" />
              <span className="text-2xl font-bold tracking-tight text-blue-700">CycleWise</span>
            </div>
            <div className="flex gap-8 items-center text-lg font-medium">
              <a href="/DayOverview" className="hover:text-blue-600 transition">Today</a>
              <a href="/Learn" className="hover:text-blue-600 transition">Learn</a>
              <a href="/Chat" className="hover:text-blue-600 transition">Chat</a>
              <a href="/PartnerTip" className="hover:text-blue-600 transition">Health</a>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-9 h-9 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full flex items-center justify-center border-2 border-blue-200 shadow">
                <span role="img" aria-label="User" className="text-xl">👩‍🦰</span>
              </div>
            </div>
          </nav>
        </header>
        <main className="min-h-[calc(100vh-64px)] pt-6 pb-12 px-2 md:px-0">
          {children}
        </main>
      </body>
    </html>
  );
}
