'use client';
import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function GeminiChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [authToken, setAuthToken] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Authentication check on component mount
  useEffect(() => {
    console.log('Chat component mounted');
    const token = localStorage.getItem('authToken');
    console.log('Stored token:', token ? 'exists' : 'none');
    if (token) {
      setAuthToken(token);
      setIsAuthenticated(true);
      console.log('Using stored token');
    } else {
      console.log('No stored token, trying demo auth');
      // Use demo authentication for testing
      handleDemoAuth();
    }
  }, []);

  // Demo authentication function
  const handleDemoAuth = async () => {
    console.log('Starting demo auth...');
    try {
      const response = await fetch('http://localhost:8000/demo/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const data = await response.json();
      console.log('Demo auth response:', data);
      if (data.access_token) {
        setAuthToken(data.access_token);
        setIsAuthenticated(true);
        localStorage.setItem('authToken', data.access_token);
        console.log('Demo auth successful');
      }
    } catch (error) {
      console.error('Demo auth failed:', error);
      // Continue without auth - will use demo endpoint
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Send message called with input:', input);
    console.log('Loading state:', loading);
    console.log('Is authenticated:', isAuthenticated);
    
    if (!input.trim() || loading) {
      console.log('Message send blocked - input empty or loading');
      return;
    }

    // Determine endpoint and headers based on authentication
    // const endpoint = isAuthenticated ? '/chat' : '/demo/chat';
    const endpoint = '/demo/chat';
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // No need to set Authorization header for demo

    console.log('Using endpoint:', endpoint);
    console.log('Headers:', headers);

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    console.log('Set loading to true');

    try {
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ 
          message: input,
        }),
      });

      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);

      if (response.ok) {
        const assistantMessage: Message = {
          role: 'assistant',
          content: data.response,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, assistantMessage]);
        console.log('Message sent successfully');
      } else {
        // Handle different error formats from your API
        const errorMessage = data.detail || data.error || 'Failed to get response';
        console.error('API error:', errorMessage);
        throw new Error(errorMessage);
      }
    } catch (error) {
      console.error('Error:', error);
      
      // Handle authentication errors specifically
      if (error instanceof Error && error.message.includes('401')) {
        console.log('Authentication error, trying to re-authenticate');
        // Try to re-authenticate
        await handleDemoAuth();
      }
      
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      console.log('Set loading to false');
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="flex flex-col h-[70vh] max-w-2xl mx-auto bg-gradient-to-br from-blue-50 via-purple-50 to-pink-100 rounded-3xl shadow-inner overflow-hidden">
      {/* Header */}
      <div className="bg-white/80 shadow-sm border-b px-6 py-4 rounded-t-3xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-semibold text-gray-800">CycleWise Chat</h1>
              <p className="text-sm text-gray-500">Your AI Health Companion</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${isAuthenticated ? 'bg-green-500' : 'bg-yellow-500'}`}></div>
            <span className="text-xs text-gray-500">
              {isAuthenticated ? 'Authenticated' : 'Demo Mode'}
            </span>
            <div className="text-xs text-gray-400 ml-2">
              Loading: {loading ? 'Yes' : 'No'}
            </div>
          </div>
        </div>
      </div>

      {/* Chat Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-100">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mb-4">
              <Bot className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-medium text-gray-700 mb-2">Welcome to CycleWise!</h3>
            <p className="text-gray-500 max-w-md">
              I&apos;m your AI health assistant powered by Google Gemini. I can help you with cycle tracking, health insights, and personalized recommendations.
            </p>
            {!isAuthenticated && (
              <p className="text-yellow-600 text-sm mt-2">
                Running in demo mode - some features may be limited.
              </p>
            )}
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex max-w-[80%] ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  {/* Avatar */}
                  <div className={`flex-shrink-0 ${message.role === 'user' ? 'ml-3' : 'mr-3'}`}>
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shadow-lg ${
                      message.role === 'user' 
                        ? 'bg-gradient-to-r from-pink-400 to-red-400' 
                        : 'bg-gradient-to-r from-blue-500 to-purple-600'
                    }`}>
                      {message.role === 'user' ? (
                        <User className="w-4 h-4 text-white" />
                      ) : (
                        <Bot className="w-4 h-4 text-white" />
                      )}
                    </div>
                  </div>

                  {/* Message Bubble */}
                  <div className={`rounded-2xl px-5 py-3 shadow-md transition-all duration-200 ${
                    message.role === 'user'
                      ? 'bg-gradient-to-r from-pink-400 to-red-400 text-white'
                      : 'bg-white text-gray-800 border border-gray-200'
                  }`}>
                    <p className="text-base whitespace-pre-wrap leading-relaxed">{message.content}</p>
                    <p className={`text-xs mt-1 ${
                      message.role === 'user' ? 'text-pink-100' : 'text-gray-400'
                    }`}>
                      {formatTime(message.timestamp)}
                    </p>
                  </div>
                </div>
              </div>
            ))}

            {/* Loading indicator */}
            {loading && (
              <div className="flex justify-start">
                <div className="flex">
                  <div className="mr-3">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                  </div>
                  <div className="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-200">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Form */}
      <div className="bg-white/90 border-t p-4 rounded-b-3xl shadow-inner">
        <form onSubmit={sendMessage} className="flex space-x-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me about your health, cycle tracking, or wellness tips..."
              disabled={loading}
              className="w-full px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed pr-12 bg-white/80 shadow"
            />
          </div>
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white p-3 rounded-full disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  );
}
