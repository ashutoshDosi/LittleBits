'use client';

import React, { useState, useEffect } from 'react';

interface HealthData {
  hydration: {
    percentage: number;
    water_intake_ml: number;
    recommended_ml: number;
    status: string;
  };
  exercise: {
    steps_today: number;
    calories_burned: number;
    active_minutes: number;
    status: string;
  };
  sleep: {
    hours_last_night: number;
    quality_score: number;
    recommended_hours: number;
    status: string;
  };
}

interface CalendarData {
  description: string;
  stress_level: string;
  meeting_count: number;
  total_hours: number;
  next_meeting: string;
  free_time: string;
}

interface WeatherData {
  temperature: number;
  description: string;
  humidity: number;
  pressure: number;
  impact_on_symptoms: string;
}

export default function HealthTracker() {
  const [healthData, setHealthData] = useState<HealthData | null>(null);
  const [calendarData, setCalendarData] = useState<CalendarData | null>(null);
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'calendar' | 'health' | 'weather'>('overview');

  useEffect(() => {
    fetchHealthData();
  }, []);

  const fetchHealthData = async () => {
    try {
      // Get demo token if needed
      let token = localStorage.getItem('authToken');
      if (!token) {
        const resp = await fetch('http://localhost:8000/demo/auth', { 
          method: 'POST', 
          headers: { 'Content-Type': 'application/json' } 
        });
        const data = await resp.json();
        token = data.access_token;
        if (token) localStorage.setItem('authToken', token);
      }

      const headers: Record<string, string> = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      // Fetch all data in parallel (use demo endpoints for demo mode)
      const [healthResponse, calendarResponse, weatherResponse] = await Promise.all([
        fetch('http://localhost:8000/demo/health', { headers }),
        fetch('http://localhost:8000/demo/calendar', { headers }),
        fetch('http://localhost:8000/demo/weather', { headers })
      ]);

      const healthResult = await healthResponse.json();
      const calendarResult = await calendarResponse.json();
      const weatherResult = await weatherResponse.json();

      // Set data (use fallback if API fails)
      setHealthData(healthResult.data || {
        hydration: {
          percentage: 75,
          water_intake_ml: 1500,
          recommended_ml: 2000,
          status: "needs_improvement"
        },
        exercise: {
          steps_today: 6500,
          calories_burned: 320,
          active_minutes: 45,
          status: "moderate"
        },
        sleep: {
          hours_last_night: 7.5,
          quality_score: 8,
          recommended_hours: 8,
          status: "good"
        }
      });

      setCalendarData(calendarResult.data || {
        description: "3 meetings today, 2 hours total",
        stress_level: "moderate",
        meeting_count: 3,
        total_hours: 2.0,
        next_meeting: "2:00 PM",
        free_time: "1:00 PM - 2:00 PM"
      });

      setWeatherData(weatherResult.data || {
        temperature: 72,
        description: "Partly cloudy",
        humidity: 65,
        pressure: 1013,
        impact_on_symptoms: "Moderate humidity may affect bloating and discomfort. Consider staying hydrated and avoiding salty foods."
      });

      setLoading(false);
    } catch (error) {
      console.error('Error fetching health data:', error);
      
      // Fallback to demo data
      setHealthData({
        hydration: {
          percentage: 75,
          water_intake_ml: 1500,
          recommended_ml: 2000,
          status: "needs_improvement"
        },
        exercise: {
          steps_today: 6500,
          calories_burned: 320,
          active_minutes: 45,
          status: "moderate"
        },
        sleep: {
          hours_last_night: 7.5,
          quality_score: 8,
          recommended_hours: 8,
          status: "good"
        }
      });

      setCalendarData({
        description: "3 meetings today, 2 hours total",
        stress_level: "moderate",
        meeting_count: 3,
        total_hours: 2.0,
        next_meeting: "2:00 PM",
        free_time: "1:00 PM - 2:00 PM"
      });

      setWeatherData({
        temperature: 72,
        description: "Partly cloudy",
        humidity: 65,
        pressure: 1013,
        impact_on_symptoms: "Moderate humidity may affect bloating and discomfort. Consider staying hydrated and avoiding salty foods."
      });

      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'good': return 'text-green-600 bg-green-100';
      case 'moderate': return 'text-yellow-600 bg-yellow-100';
      case 'needs_improvement': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStressColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-green-600 bg-green-100';
      case 'moderate': return 'text-yellow-600 bg-yellow-100';
      case 'high': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your health data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-100">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-pink-200">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-pink-400 to-purple-500 rounded-full mb-4 shadow-lg">
              <span className="text-2xl">💪</span>
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-pink-600 via-purple-600 to-blue-600 bg-clip-text text-transparent mb-2">
              Health & Wellness Dashboard
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Track your health metrics, calendar stress, and environmental factors that impact your cycle
            </p>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="flex justify-center space-x-2 mb-8">
          {[
            { id: 'overview', label: 'Overview', icon: '📊' },
            { id: 'calendar', label: 'Calendar', icon: '📅' },
            { id: 'health', label: 'Health', icon: '💪' },
            { id: 'weather', label: 'Weather', icon: '🌤️' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center space-x-2 px-6 py-3 rounded-full font-semibold transition-all duration-300 ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-lg scale-105'
                  : 'bg-white text-gray-700 hover:bg-pink-50 border border-gray-200'
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl p-8">
          {activeTab === 'overview' && (
            <div className="space-y-8">
              <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">Today's Health Overview</h2>
              
              {/* Health Metrics Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {/* Hydration */}
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border border-blue-200">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-3xl">💧</span>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(healthData?.hydration.status || '')}`}>
                      {healthData?.hydration.status.replace('_', ' ')}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-800 mb-2">Hydration</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Intake:</span>
                      <span className="font-semibold">{healthData?.hydration.water_intake_ml}ml / {healthData?.hydration.recommended_ml}ml</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${healthData?.hydration.percentage || 0}%` }}
                      ></div>
                    </div>
                    <p className="text-sm text-gray-600">{healthData?.hydration.percentage}% of daily goal</p>
                  </div>
                </div>

                {/* Exercise */}
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 border border-green-200">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-3xl">🚶</span>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(healthData?.exercise.status || '')}`}>
                      {healthData?.exercise.status}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-800 mb-2">Activity</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Steps:</span>
                      <span className="font-semibold">{healthData?.exercise.steps_today.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Active:</span>
                      <span className="font-semibold">{healthData?.exercise.active_minutes} min</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Calories:</span>
                      <span className="font-semibold">{healthData?.exercise.calories_burned}</span>
                    </div>
                  </div>
                </div>

                {/* Sleep */}
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6 border border-purple-200">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-3xl">😴</span>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(healthData?.sleep.status || '')}`}>
                      {healthData?.sleep.status}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold text-gray-800 mb-2">Sleep</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Hours:</span>
                      <span className="font-semibold">{healthData?.sleep.hours_last_night}h / {healthData?.sleep.recommended_hours}h</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Quality:</span>
                      <span className="font-semibold">{healthData?.sleep.quality_score}/10</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Calendar & Weather Summary */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-2xl p-6 border border-orange-200">
                  <div className="flex items-center mb-4">
                    <span className="text-3xl mr-3">📅</span>
                    <div>
                      <h3 className="text-xl font-bold text-gray-800">Today's Schedule</h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStressColor(calendarData?.stress_level || '')}`}>
                        {calendarData?.stress_level} stress
                      </span>
                    </div>
                  </div>
                  <p className="text-gray-700 mb-2">{calendarData?.description}</p>
                  <p className="text-sm text-gray-600">Next meeting: {calendarData?.next_meeting}</p>
                </div>

                <div className="bg-gradient-to-br from-cyan-50 to-cyan-100 rounded-2xl p-6 border border-cyan-200">
                  <div className="flex items-center mb-4">
                    <span className="text-3xl mr-3">🌤️</span>
                    <div>
                      <h3 className="text-xl font-bold text-gray-800">Weather Impact</h3>
                      <span className="text-sm text-gray-600">{weatherData?.temperature}°F, {weatherData?.description}</span>
                    </div>
                  </div>
                  <p className="text-gray-700 text-sm">{weatherData?.impact_on_symptoms}</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'calendar' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">Calendar & Stress Analysis</h2>
              
              <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-2xl p-8 border border-orange-200">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-800 mb-4">Today's Schedule</h3>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-4 bg-white/50 rounded-xl">
                        <div>
                          <p className="font-semibold text-gray-800">Meetings</p>
                          <p className="text-gray-600">{calendarData?.meeting_count} scheduled</p>
                        </div>
                        <span className="text-2xl">📋</span>
                      </div>
                      <div className="flex items-center justify-between p-4 bg-white/50 rounded-xl">
                        <div>
                          <p className="font-semibold text-gray-800">Total Hours</p>
                          <p className="text-gray-600">{calendarData?.total_hours} hours</p>
                        </div>
                        <span className="text-2xl">⏰</span>
                      </div>
                      <div className="flex items-center justify-between p-4 bg-white/50 rounded-xl">
                        <div>
                          <p className="font-semibold text-gray-800">Next Meeting</p>
                          <p className="text-gray-600">{calendarData?.next_meeting}</p>
                        </div>
                        <span className="text-2xl">🕐</span>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-2xl font-bold text-gray-800 mb-4">Stress Analysis</h3>
                    <div className="space-y-4">
                      <div className="p-4 bg-white/50 rounded-xl">
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-semibold text-gray-800">Stress Level</span>
                          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStressColor(calendarData?.stress_level || '')}`}>
                            {calendarData?.stress_level}
                          </span>
                        </div>
                        <p className="text-gray-600 text-sm">
                          Based on meeting count, duration, and timing
                        </p>
                      </div>
                      
                      <div className="p-4 bg-white/50 rounded-xl">
                        <h4 className="font-semibold text-gray-800 mb-2">Free Time</h4>
                        <p className="text-gray-600">{calendarData?.free_time}</p>
                        <p className="text-sm text-gray-500 mt-2">Perfect for self-care activities</p>
                      </div>
                      
                      <div className="p-4 bg-white/50 rounded-xl">
                        <h4 className="font-semibold text-gray-800 mb-2">Recommendations</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          <li>• Take breaks between meetings</li>
                          <li>• Use free time for gentle exercise</li>
                          <li>• Stay hydrated throughout the day</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'health' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">Detailed Health Metrics</h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Hydration Details */}
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border border-blue-200">
                  <div className="flex items-center mb-6">
                    <span className="text-4xl mr-4">💧</span>
                    <div>
                      <h3 className="text-2xl font-bold text-gray-800">Hydration Tracking</h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(healthData?.hydration.status || '')}`}>
                        {healthData?.hydration.status.replace('_', ' ')}
                      </span>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-white/50 rounded-xl p-4">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-semibold text-gray-800">Daily Progress</span>
                        <span className="text-2xl font-bold text-blue-600">{healthData?.hydration.percentage}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className="bg-blue-500 h-3 rounded-full transition-all duration-500"
                          style={{ width: `${healthData?.hydration.percentage || 0}%` }}
                        ></div>
                      </div>
                      <div className="flex justify-between text-sm text-gray-600 mt-2">
                        <span>{healthData?.hydration.water_intake_ml}ml</span>
                        <span>{healthData?.hydration.recommended_ml}ml goal</span>
                      </div>
                    </div>
                    
                    <div className="bg-white/50 rounded-xl p-4">
                      <h4 className="font-semibold text-gray-800 mb-2">Hydration Tips</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        <li>• Drink water before each meal</li>
                        <li>• Keep a water bottle nearby</li>
                        <li>• Add lemon or cucumber for flavor</li>
                        <li>• Monitor urine color (should be light yellow)</li>
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Exercise Details */}
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 border border-green-200">
                  <div className="flex items-center mb-6">
                    <span className="text-4xl mr-4">🚶</span>
                    <div>
                      <h3 className="text-2xl font-bold text-gray-800">Activity Tracking</h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(healthData?.exercise.status || '')}`}>
                        {healthData?.exercise.status}
                      </span>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="grid grid-cols-3 gap-4">
                      <div className="bg-white/50 rounded-xl p-4 text-center">
                        <div className="text-2xl font-bold text-green-600">{healthData?.exercise.steps_today.toLocaleString()}</div>
                        <div className="text-sm text-gray-600">Steps</div>
                      </div>
                      <div className="bg-white/50 rounded-xl p-4 text-center">
                        <div className="text-2xl font-bold text-green-600">{healthData?.exercise.active_minutes}</div>
                        <div className="text-sm text-gray-600">Active Min</div>
                      </div>
                      <div className="bg-white/50 rounded-xl p-4 text-center">
                        <div className="text-2xl font-bold text-green-600">{healthData?.exercise.calories_burned}</div>
                        <div className="text-sm text-gray-600">Calories</div>
                      </div>
                    </div>
                    
                    <div className="bg-white/50 rounded-xl p-4">
                      <h4 className="font-semibold text-gray-800 mb-2">Activity Recommendations</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        <li>• Aim for 10,000 steps daily</li>
                        <li>• Include 30 minutes of moderate activity</li>
                        <li>• Take walking breaks during work</li>
                        <li>• Try gentle yoga or stretching</li>
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Sleep Details */}
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6 border border-purple-200">
                  <div className="flex items-center mb-6">
                    <span className="text-4xl mr-4">😴</span>
                    <div>
                      <h3 className="text-2xl font-bold text-gray-800">Sleep Quality</h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(healthData?.sleep.status || '')}`}>
                        {healthData?.sleep.status}
                      </span>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-white/50 rounded-xl p-4 text-center">
                        <div className="text-2xl font-bold text-purple-600">{healthData?.sleep.hours_last_night}h</div>
                        <div className="text-sm text-gray-600">Hours Slept</div>
                      </div>
                      <div className="bg-white/50 rounded-xl p-4 text-center">
                        <div className="text-2xl font-bold text-purple-600">{healthData?.sleep.quality_score}/10</div>
                        <div className="text-sm text-gray-600">Quality Score</div>
                      </div>
                    </div>
                    
                    <div className="bg-white/50 rounded-xl p-4">
                      <h4 className="font-semibold text-gray-800 mb-2">Sleep Tips</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        <li>• Maintain consistent sleep schedule</li>
                        <li>• Create a relaxing bedtime routine</li>
                        <li>• Keep bedroom cool and dark</li>
                        <li>• Avoid screens 1 hour before bed</li>
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Health Insights */}
                <div className="bg-gradient-to-br from-pink-50 to-pink-100 rounded-2xl p-6 border border-pink-200">
                  <div className="flex items-center mb-6">
                    <span className="text-4xl mr-4">💡</span>
                    <div>
                      <h3 className="text-2xl font-bold text-gray-800">Health Insights</h3>
                      <span className="text-sm text-gray-600">AI-powered recommendations</span>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-white/50 rounded-xl p-4">
                      <h4 className="font-semibold text-gray-800 mb-2">Today's Focus</h4>
                      <p className="text-gray-700 mb-3">
                        Based on your current cycle phase and health metrics, focus on:
                      </p>
                      <ul className="text-sm text-gray-600 space-y-2">
                        <li className="flex items-start">
                          <span className="text-pink-500 mr-2">•</span>
                          Increase water intake by 500ml
                        </li>
                        <li className="flex items-start">
                          <span className="text-pink-500 mr-2">•</span>
                          Take a 15-minute walk during your free time
                        </li>
                        <li className="flex items-start">
                          <span className="text-pink-500 mr-2">•</span>
                          Practice stress management between meetings
                        </li>
                      </ul>
                    </div>
                    
                    <div className="bg-white/50 rounded-xl p-4">
                      <h4 className="font-semibold text-gray-800 mb-2">Cycle Correlation</h4>
                      <p className="text-sm text-gray-600">
                        Your current health metrics suggest you're in the luteal phase. 
                        This is normal to feel slightly more tired and need extra hydration.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'weather' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">Weather & Environmental Impact</h2>
              
              <div className="bg-gradient-to-br from-cyan-50 to-cyan-100 rounded-2xl p-8 border border-cyan-200">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-800 mb-6">Current Weather</h3>
                    <div className="space-y-4">
                      <div className="bg-white/50 rounded-xl p-6 text-center">
                        <div className="text-6xl mb-4">🌤️</div>
                        <div className="text-4xl font-bold text-gray-800 mb-2">{weatherData?.temperature}°F</div>
                        <div className="text-xl text-gray-600 mb-4">{weatherData?.description}</div>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <span className="text-gray-600">Humidity:</span>
                            <div className="font-semibold">{weatherData?.humidity}%</div>
                          </div>
                          <div>
                            <span className="text-gray-600">Pressure:</span>
                            <div className="font-semibold">{weatherData?.pressure} hPa</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-2xl font-bold text-gray-800 mb-6">Impact on Your Cycle</h3>
                    <div className="space-y-4">
                      <div className="bg-white/50 rounded-xl p-6">
                        <h4 className="font-semibold text-gray-800 mb-3">Today's Impact</h4>
                        <p className="text-gray-700 mb-4">{weatherData?.impact_on_symptoms}</p>
                        
                        <h4 className="font-semibold text-gray-800 mb-3">Recommendations</h4>
                        <ul className="text-sm text-gray-600 space-y-2">
                          <li className="flex items-start">
                            <span className="text-cyan-500 mr-2">•</span>
                            Stay hydrated to combat humidity effects
                          </li>
                          <li className="flex items-start">
                            <span className="text-cyan-500 mr-2">•</span>
                            Avoid salty foods that can worsen bloating
                          </li>
                          <li className="flex items-start">
                            <span className="text-cyan-500 mr-2">•</span>
                            Consider indoor activities if weather affects mood
                          </li>
                          <li className="flex items-start">
                            <span className="text-cyan-500 mr-2">•</span>
                            Monitor how weather changes affect your symptoms
                          </li>
                        </ul>
                      </div>
                      
                      <div className="bg-white/50 rounded-xl p-6">
                        <h4 className="font-semibold text-gray-800 mb-3">Weather Tracking</h4>
                        <p className="text-sm text-gray-600 mb-4">
                          Track how different weather conditions affect your cycle symptoms over time.
                        </p>
                        <div className="grid grid-cols-3 gap-4 text-center">
                          <div>
                            <div className="text-2xl">🌧️</div>
                            <div className="text-xs text-gray-600">Rainy Days</div>
                          </div>
                          <div>
                            <div className="text-2xl">☀️</div>
                            <div className="text-xs text-gray-600">Sunny Days</div>
                          </div>
                          <div>
                            <div className="text-2xl">❄️</div>
                            <div className="text-xs text-gray-600">Cold Days</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 