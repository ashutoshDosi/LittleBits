'use client';
import { useState } from 'react';

export default function TestPage() {
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testAuth = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/demo/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      setResult(`Auth Success: ${JSON.stringify(data, null, 2)}`);
    } catch (error) {
      setResult(`Auth Error: ${error}`);
    }
    setLoading(false);
  };

  const testChat = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/demo/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: 'Hello, test message' }),
      });
      const data = await response.json();
      setResult(`Chat Success: ${JSON.stringify(data, null, 2)}`);
    } catch (error) {
      setResult(`Chat Error: ${error}`);
    }
    setLoading(false);
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">API Connection Test</h1>
      
      <div className="space-y-4 mb-6">
        <button
          onClick={testAuth}
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          Test Authentication
        </button>
        
        <button
          onClick={testChat}
          disabled={loading}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50 ml-4"
        >
          Test Chat
        </button>
      </div>

      {loading && <div className="text-blue-600">Loading...</div>}
      
      {result && (
        <div className="bg-gray-100 p-4 rounded">
          <h3 className="font-bold mb-2">Result:</h3>
          <pre className="whitespace-pre-wrap text-sm">{result}</pre>
        </div>
      )}
    </div>
  );
} 