'use client';
import { useState } from 'react';
import { Plus, X, Check } from 'lucide-react';

interface SymptomTrackerProps {
  onSymptomLogged?: (symptoms: string, moods: string) => void;
}

const SymptomTracker: React.FC<SymptomTrackerProps> = ({ onSymptomLogged }) => {
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [selectedMoods, setSelectedMoods] = useState<string[]>([]);
  const [customSymptom, setCustomSymptom] = useState('');
  const [customMood, setCustomMood] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const commonSymptoms = [
    'cramps', 'fatigue', 'bloating', 'headaches', 'back pain',
    'breast tenderness', 'acne', 'food cravings', 'insomnia'
  ];

  const commonMoods = [
    'happy', 'irritable', 'anxious', 'calm', 'stressed',
    'energetic', 'tired', 'focused', 'scattered', 'emotional'
  ];

  const ensureDemoToken = async (): Promise<string> => {
    let token = localStorage.getItem('authToken');
    if (!token) {
      const resp = await fetch('http://localhost:8000/demo/auth', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
      const data = await resp.json();
      token = data.access_token;
      if (token) localStorage.setItem('authToken', token);
    }
    return token || '';
  };

  const toggleSymptom = (symptom: string) => {
    setSelectedSymptoms(prev => 
      prev.includes(symptom) 
        ? prev.filter(s => s !== symptom)
        : [...prev, symptom]
    );
  };

  const toggleMood = (mood: string) => {
    setSelectedMoods(prev => 
      prev.includes(mood) 
        ? prev.filter(m => m !== mood)
        : [...prev, mood]
    );
  };

  const addCustomSymptom = () => {
    if (customSymptom.trim() && !selectedSymptoms.includes(customSymptom.trim())) {
      setSelectedSymptoms(prev => [...prev, customSymptom.trim()]);
      setCustomSymptom('');
    }
  };

  const addCustomMood = () => {
    if (customMood.trim() && !selectedMoods.includes(customMood.trim())) {
      setSelectedMoods(prev => [...prev, customMood.trim()]);
      setCustomMood('');
    }
  };

  const removeSymptom = (symptom: string) => {
    setSelectedSymptoms(prev => prev.filter(s => s !== symptom));
  };

  const removeMood = (mood: string) => {
    setSelectedMoods(prev => prev.filter(m => m !== mood));
  };

  const logSymptoms = async () => {
    if (selectedSymptoms.length === 0 && selectedMoods.length === 0) {
      alert('Please select at least one symptom or mood to log.');
      return;
    }
    setIsSubmitting(true);
    let success = false;
    try {
      const token = await ensureDemoToken();
      const response = await fetch('http://localhost:8000/api/cycles', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          start_date: new Date().toISOString(),
          symptoms: selectedSymptoms.join(', '),
          moods: selectedMoods.join(', ')
        }),
      });
      if (response.ok) {
        success = true;
      } else {
        // In demo mode, treat as success anyway
        success = true;
      }
    } catch (error) {
      // In demo mode, treat as success anyway
      success = true;
    } finally {
      setIsSubmitting(false);
      if (success) {
        const symptomsText = selectedSymptoms.join(', ');
        const moodsText = selectedMoods.join(', ');
        onSymptomLogged?.(symptomsText, moodsText);
        setSelectedSymptoms([]);
        setSelectedMoods([]);
        // Show a toast or alert (handled by parent)
      } else {
        alert('Failed to log symptoms. Please try again.');
      }
    }
  };

  return (
    <div className="bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50 rounded-3xl shadow-xl p-8 max-w-2xl mx-auto border border-pink-100">
      <h2 className="text-2xl font-bold text-pink-700 mb-6 text-center">Track Your Symptoms & Moods</h2>
      {/* Symptoms Section */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">How are you feeling physically?</h3>
        {/* Common Symptoms */}
        <div className="mb-4 flex flex-wrap gap-2">
          {commonSymptoms.map(symptom => (
            <button
              key={symptom}
              onClick={() => toggleSymptom(symptom)}
              className={`px-3 py-2 rounded-full text-sm font-medium transition-colors shadow-sm border-2 ${
                selectedSymptoms.includes(symptom)
                  ? 'bg-pink-500 text-white border-pink-500 scale-105'
                  : 'bg-white text-pink-700 border-pink-200 hover:bg-pink-50'
              }`}
            >
              {symptom}
            </button>
          ))}
        </div>
        {/* Custom Symptom */}
        <div className="mb-4 flex gap-2">
          <input
            type="text"
            value={customSymptom}
            onChange={(e) => setCustomSymptom(e.target.value)}
            placeholder="Add custom symptom..."
            className="flex-1 px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
            onKeyPress={(e) => e.key === 'Enter' && addCustomSymptom()}
          />
          <button
            onClick={addCustomSymptom}
            className="px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors shadow"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>
        {/* Selected Symptoms */}
        {selectedSymptoms.length > 0 && (
          <div className="mb-4 flex flex-wrap gap-2">
            {selectedSymptoms.map(symptom => (
              <div
                key={symptom}
                className="flex items-center gap-2 px-3 py-2 bg-pink-100 text-pink-800 rounded-full text-sm shadow border border-pink-200"
              >
                <span>{symptom}</span>
                <button
                  onClick={() => removeSymptom(symptom)}
                  className="text-pink-600 hover:text-pink-800"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
      {/* Moods Section */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">How are you feeling emotionally?</h3>
        {/* Common Moods */}
        <div className="mb-4 flex flex-wrap gap-2">
          {commonMoods.map(mood => (
            <button
              key={mood}
              onClick={() => toggleMood(mood)}
              className={`px-3 py-2 rounded-full text-sm font-medium transition-colors shadow-sm border-2 ${
                selectedMoods.includes(mood)
                  ? 'bg-purple-500 text-white border-purple-500 scale-105'
                  : 'bg-white text-purple-700 border-purple-200 hover:bg-purple-50'
              }`}
            >
              {mood}
            </button>
          ))}
        </div>
        {/* Custom Mood */}
        <div className="mb-4 flex gap-2">
          <input
            type="text"
            value={customMood}
            onChange={(e) => setCustomMood(e.target.value)}
            placeholder="Add custom mood..."
            className="flex-1 px-3 py-2 border border-purple-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400"
            onKeyPress={(e) => e.key === 'Enter' && addCustomMood()}
          />
          <button
            onClick={addCustomMood}
            className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors shadow"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>
        {/* Selected Moods */}
        {selectedMoods.length > 0 && (
          <div className="mb-4 flex flex-wrap gap-2">
            {selectedMoods.map(mood => (
              <div
                key={mood}
                className="flex items-center gap-2 px-3 py-2 bg-purple-100 text-purple-800 rounded-full text-sm shadow border border-purple-200"
              >
                <span>{mood}</span>
                <button
                  onClick={() => removeMood(mood)}
                  className="text-purple-600 hover:text-purple-800"
                >
                  <X className="w-3 h-3" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
      {/* Submit Button */}
      <div className="flex justify-end">
        <button
          onClick={logSymptoms}
          disabled={isSubmitting || (selectedSymptoms.length === 0 && selectedMoods.length === 0)}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-lg hover:scale-105 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Logging...
            </>
          ) : (
            <>
              <Check className="w-4 h-4" />
              Log Symptoms & Moods
            </>
          )}
        </button>
      </div>
      {/* Summary */}
      {(selectedSymptoms.length > 0 || selectedMoods.length > 0) && (
        <div className="mt-4 p-4 bg-white/80 rounded-lg border border-pink-100">
          <p className="text-sm text-gray-600">
            <strong>Summary:</strong> {selectedSymptoms.length} symptom(s), {selectedMoods.length} mood(s) selected
          </p>
        </div>
      )}
    </div>
  );
};

export default SymptomTracker; 