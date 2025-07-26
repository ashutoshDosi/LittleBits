import Image from "next/image";
import LoginPage from "./components/Login";

export default function Home() {
  return (
    <div className="relative min-h-[80vh] flex flex-col items-center justify-center overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 z-0 animate-gradient bg-gradient-to-br from-pink-100 via-blue-100 to-purple-100 opacity-80" />
      {/* Hero Card */}
      <div className="relative z-10 w-full max-w-xl bg-white/70 backdrop-blur-lg rounded-3xl shadow-2xl p-8 border border-blue-100 flex flex-col items-center">
        {/* Emoji illustration */}
        <div className="flex items-center justify-center mb-4">
          <span className="text-5xl mr-2">🩸</span>
          <span className="text-5xl mr-2">🤗</span>
          <span className="text-5xl">🌸</span>
        </div>
        <h1 className="text-4xl font-extrabold text-blue-700 mb-2 text-center drop-shadow-sm">Welcome to CycleWise</h1>
        <p className="text-lg text-gray-700 mb-4 text-center max-w-md font-medium">
          <span className="bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent font-bold">Empathetic AI for Menstrual Health</span>
        </p>
        <p className="text-base text-gray-600 mb-6 text-center max-w-md">
          Track your cycle, chat about symptoms, and get personalized support—all in one beautiful, inclusive app. No stigma. No shame. Just care.
        </p>
        <button
          disabled
          className="w-full flex items-center justify-center gap-3 px-6 py-3 bg-gray-200 text-gray-400 rounded-full font-semibold text-lg shadow mb-2 cursor-not-allowed"
        >
          <svg data-prefix="fab" data-icon="google" className="svg-inline--fa fa-google" role="img" viewBox="0 0 512 512" width="24" height="24" fill="currentColor"><path d="M500 261.8C500 403.3 403.1 504 260 504 122.8 504 12 393.2 12 256S122.8 8 260 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9c-88.3-85.2-252.5-21.2-252.5 118.2 0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9l-140.8 0 0-85.3 236.1 0c2.3 12.7 3.9 24.9 3.9 41.4z"></path></svg>
          Sign in with Google
        </button>
        <div className="mt-2 text-center">
          <span className="inline-block bg-gradient-to-r from-blue-500 to-purple-500 text-white px-4 py-1 rounded-full text-xs font-bold shadow animate-pulse">Demo Mode</span>
        </div>
        <div className="mt-8 w-full flex flex-col gap-3 items-center">
          <a href="/DayOverview" className="w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-full font-semibold text-lg shadow hover:scale-105 transition text-center">Try the App</a>
        </div>
      </div>
    </div>
  );
}
