"use client";
import Image from "next/image";
import { useState, useEffect } from "react";
import SymptomTracker from "./SymptomTracker";

interface CycleData {
  phase: string;
  days_since: number;
  symptoms?: string;
  moods?: string;
}

const DayOverview = () => {
  const [cycleData, setCycleData] = useState<CycleData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [lastTip, setLastTip] = useState<string | null>(null);

  useEffect(() => {
    fetchCycleData();
  }, []);

  const fetchCycleData = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await fetch('http://localhost:8000/api/phase', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      if (response.ok) {
        const data = await response.json();
        setCycleData(data);
      } else {
        // Fallback to demo data if not authenticated
        setCycleData({
          phase: "menstrual",
          days_since: 1,
          symptoms: "cramps, fatigue",
          moods: "tired, moody"
        });
      }
    } catch (err) {
      setError('Unable to load cycle data');
      // Fallback to demo data
      setCycleData({
        phase: "menstrual",
        days_since: 1,
        symptoms: "cramps, fatigue",
        moods: "tired, moody"
      });
    } finally {
      setLoading(false);
    }
  };

  const getPersonalizedTip = (phase: string, symptoms: string, moods: string) => {
    // Simple rules for demo: you can expand this for more depth
    if (symptoms.includes('cramps')) return 'Try a warm compress and gentle stretching for cramps.';
    if (symptoms.includes('bloating')) return 'Reduce salt and stay hydrated to help with bloating.';
    if (moods.includes('stressed')) return 'Take a few deep breaths and give yourself a break—you deserve it!';
    if (moods.includes('tired')) return 'Prioritize rest and hydration today.';
    if (phase === 'ovulatory') return 'You may feel most social and confident now. Celebrate yourself!';
    if (phase === 'follicular') return 'Great time for new projects! Your energy is rising—enjoy it.';
    if (phase === 'luteal') return 'Mood swings are normal. Prioritize self-care and listen to your body.';
    return 'Stay hydrated and rest. Gentle movement and warmth can help with cramps.';
  };

  const handleSymptomLogged = (symptoms: string, moods: string) => {
    setCycleData(prev => prev ? {
      ...prev,
      symptoms,
      moods
    } : null);
    setSuccessMsg('Symptoms and moods logged!');
    setLastTip(getPersonalizedTip(currentPhase, symptoms, moods));
    setTimeout(() => setSuccessMsg(null), 2000);
  };

  const getPhase = (phase: string) => {
    if (phase === "menstrual") return 1;
    if (phase === "follicular") return 2;
    if (phase === "ovulatory") return 3;
    if (phase === "luteal") return 4;
    return 1;
  };

  const getPhaseInfo = (phase: string) => {
    const phaseInfo = {
      menstrual: {
        name: "Menstruation",
        days: "Day 1-5",
        color: "bg-pink-500",
        description: "Today is the first day of your period. You may experience cramps, fatigue, and mood swings. Remember to be kind to yourself and prioritize rest."
      },
      follicular: {
        name: "Follicular Phase",
        days: "Day 6-14",
        color: "bg-blue-400",
        description: "You are in the follicular phase. Your body is preparing for ovulation, and you may feel more energetic and optimistic."
      },
      ovulatory: {
        name: "Ovulatory Phase",
        days: "Day 15-17",
        color: "bg-green-400",
        description: "You are in the ovulatory phase. This is your peak fertility window. You may feel confident and social."
      },
      luteal: {
        name: "Luteal Phase",
        days: "Day 18-28",
        color: "bg-purple-500",
        description: "You are in the luteal phase. Hormonal changes may lead to PMS symptoms like bloating and mood swings. Stay hydrated and maintain a balanced diet."
      }
    };
    return phaseInfo[phase as keyof typeof phaseInfo] || phaseInfo.menstrual;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error && !cycleData) {
    return (
      <div className="text-center text-red-500 p-4">
        {error}
      </div>
    );
  }

  const currentPhase = cycleData?.phase || "menstrual";
  const daysSince = cycleData?.days_since || 1;
  const phase = getPhase(currentPhase);
  const phaseInfo = getPhaseInfo(currentPhase);

  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh]">
      <div className="w-full max-w-2xl bg-white/90 rounded-3xl shadow-xl p-0 md:p-8 border border-blue-100 relative">
        {successMsg && (
          <div className="absolute top-4 left-1/2 -translate-x-1/2 z-20">
            <span className="bg-green-500 text-white px-4 py-2 rounded-full shadow font-semibold animate-fade-in">{successMsg}</span>
          </div>
        )}
        <div className="absolute -top-6 left-1/2 -translate-x-1/2 flex items-center gap-2">
          <span className="bg-gradient-to-r from-pink-400 to-purple-500 text-white px-4 py-1 rounded-full text-xs font-semibold shadow">Demo Mode</span>
        </div>
        <div className="flex flex-col items-center gap-2 mb-4">
          <div className="text-md text-[#59808C] mt-2">Today / <span className="text-black font-medium">Day {daysSince}</span></div>
          <h1 className="text-3xl pt-2 font-bold mb-2">Day {daysSince}</h1>
          <div className="flex items-center gap-2 mb-2">
            <span className={`px-3 py-1 rounded-full text-white text-sm font-semibold shadow ${phaseInfo.color}`}>{phaseInfo.name}</span>
            <span className="text-xs text-gray-400">{phaseInfo.days}</span>
          </div>
        </div>
        <div className="mb-4 text-center text-lg text-gray-700 font-medium">{phaseInfo.description}</div>
        <div className="mb-6 flex flex-col md:flex-row gap-6 items-center justify-center">
          <div className="flex flex-col items-center gap-2">
            <div className="text-sm text-gray-500">Mood</div>
            <div className="text-xl font-semibold text-gray-700">
              {cycleData?.moods ? cycleData.moods.split(',')[0].trim() : 'Neutral'}
            </div>
          </div>
          <div className="flex flex-col items-center gap-2">
            <div className="text-sm text-gray-500">Symptoms</div>
            <div className="text-xl font-semibold text-gray-700">
              {cycleData?.symptoms ? cycleData.symptoms.split(',')[0].trim() : 'None tracked'}
            </div>
          </div>
          <div className="flex flex-col items-center gap-2">
            <div className="text-sm text-gray-500">Estimated Next Period</div>
            <div className="text-xl font-semibold text-gray-700">
              {currentPhase === "luteal" ? `In ${28 - daysSince} days` : "Not in luteal phase"}
            </div>
          </div>
        </div>
        <div className="mb-6">
          <div className="font-semibold mb-2 text-center">AI-Powered Insights</div>
          <div className={`rounded-2xl shadow-lg p-6 flex flex-col items-center justify-center bg-gradient-to-r from-blue-50 via-purple-50 to-pink-100 border border-blue-100 mb-6`}>
            <div className="mb-2">
              {phase === 1 && (
                <span className="text-3xl">💧</span>
              )}
              {phase === 2 && (
                <span className="text-3xl">🌱</span>
              )}
              {phase === 3 && (
                <span className="text-3xl">✨</span>
              )}
              {phase === 4 && (
                <span className="text-3xl">🌙</span>
              )}
            </div>
            <div className="text-lg text-gray-700 text-center font-medium">
              {lastTip
                ? lastTip
                : (phase === 1 && "Stay hydrated and rest. Gentle movement and warmth can help with cramps.")
                || (phase === 2 && "Great time for new projects! Your energy is rising—enjoy it.")
                || (phase === 3 && "You may feel most social and confident now. Celebrate yourself!")
                || (phase === 4 && "Mood swings are normal. Prioritize self-care and listen to your body.")
              }
            </div>
          </div>
        </div>
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-700 mb-4 text-center">Track Today&apos;s Symptoms & Moods</h3>
          <SymptomTracker onSymptomLogged={handleSymptomLogged} />
        </div>
        <div className="flex gap-4 mt-4">
          <button 
            onClick={() => window.location.href = '/Chat'}
            className="flex-1 bg-gradient-to-r from-blue-500 to-purple-500 text-white py-3 px-4 rounded-full shadow hover:scale-105 transition-colors font-semibold text-lg"
          >
            Chat with AI
          </button>
          <button 
            onClick={() => window.location.href = '/Learn'}
            className="flex-1 bg-gradient-to-r from-pink-500 to-purple-500 text-white py-3 px-4 rounded-full shadow hover:scale-105 transition-colors font-semibold text-lg"
          >
            Learn More
          </button>
        </div>
        <div className="mt-8 text-center text-gray-500 italic text-sm">“Take care of your body. It’s the only place you have to live.”</div>
      </div>
    </div>
  );
};

export default DayOverview;
