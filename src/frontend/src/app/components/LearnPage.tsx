"use client"
import RecommendedCard from "../components/RecommendedCard";
import { useState, ChangeEvent } from "react";
import TopicCard from "../components/TopicCard";

interface Topic {
  id: number;
  title: string;
  desc: string;
  category: string;
  img?: string;
  icon?: string;
}

const allTopics: Topic[] = [
  { id: 1, title: "Understanding Your Cycle", desc: "A comprehensive guide...", category: "Cycle Phases", icon: "🔄" },
  { id: 2, title: "The Menstrual Phase", desc: "What happens during menstruation.", category: "Cycle Phases", icon: "🩸" },
  { id: 3, title: "The Follicular Phase", desc: "The phase leading up to ovulation.", category: "Cycle Phases", icon: "🌸" },
  { id: 4, title: "The Ovulatory Phase", desc: "The peak fertility window.", category: "Cycle Phases", icon: "⭐" },
  { id: 5, title: "The Luteal Phase", desc: "The phase after ovulation.", category: "Cycle Phases", icon: "🌙" },
  { id: 6, title: "Hormonal Fluctuations", desc: "How hormones change throughout the cycle.", category: "Hormonal Changes", icon: "⚡" },
  { id: 7, title: "Estrogen's Role", desc: "The hormone that peaks before ovulation.", category: "Hormonal Changes", icon: "💪" },
  { id: 8, title: "Progesterone's Influence", desc: "The hormone that rises after ovulation.", category: "Hormonal Changes", icon: "😴" },
  { id: 9, title: "Self-Care Strategies", desc: "Practices to support well-being.", category: "Self-Care", icon: "💝" },
  { id: 10, title: "Stress Management", desc: "Techniques to reduce stress.", category: "Self-Care", icon: "🧘" },
  { id: 11, title: "Sleep Optimization", desc: "Tips for better sleep.", category: "Self-Care", icon: "😴" },
  { id: 12, title: "Nutrition for Cycle Support", desc: "Dietary recommendations for cycle health.", category: "Self-Care", icon: "🥗" },
];

const recommended: Topic[] = [
  { id: 1, title: "Mindfulness for Cycle Harmony", desc: "Discover mindfulness techniques...", img: "/mindfulness.png", category: "", icon: "🧘" },
  { id: 2, title: "Cycle-Syncing Workouts", desc: "Tailor your workouts to match your cycle...", img: "/workouts.png", category: "", icon: "💪" },
  { id: 3, title: "Nourishing Your Body Through Each Phase", desc: "Learn how to adjust your diet...", img: "/nourish.png", category: "", icon: "🥗" },
];

const categories = ["All", "Cycle Phases", "Hormonal Changes", "Self-Care"] as const;
type Category = typeof categories[number];

const topicDetails: Record<string, { longDesc: string; tip: string }> = {
  "Understanding Your Cycle": {
    longDesc: "Your menstrual cycle is a natural, healthy process. It has four main phases: menstrual, follicular, ovulatory, and luteal. Each phase brings unique hormonal changes and experiences.",
    tip: "Tracking your cycle helps you understand your body and plan self-care."
  },
  "The Menstrual Phase": {
    longDesc: "This is when bleeding occurs. Hormone levels are low, and you may feel tired or moody. It's a good time to rest and be gentle with yourself.",
    tip: "Use heat therapy and stay hydrated to ease cramps."
  },
  "The Follicular Phase": {
    longDesc: "After your period, your body prepares for ovulation. Estrogen rises, and you may feel more energetic and optimistic.",
    tip: "Try new activities or start projects during this phase!"
  },
  "The Ovulatory Phase": {
    longDesc: "Ovulation is when an egg is released. You may feel most confident and social. Some people notice a slight rise in body temperature.",
    tip: "This is your peak fertility window."
  },
  "The Luteal Phase": {
    longDesc: "After ovulation, progesterone rises. PMS symptoms like bloating or mood swings can appear. Self-care is especially important now.",
    tip: "Prioritize rest and gentle movement."
  },
  "Hormonal Fluctuations": {
    longDesc: "Hormones like estrogen and progesterone change throughout your cycle, affecting mood, energy, and even skin.",
    tip: "It's normal for your feelings and energy to shift!"
  },
  "Estrogen's Role": {
    longDesc: "Estrogen peaks before ovulation, boosting mood and energy. It also supports bone and heart health.",
    tip: "Eat leafy greens and seeds to support estrogen balance."
  },
  "Progesterone's Influence": {
    longDesc: "Progesterone rises after ovulation, helping prepare the body for a possible pregnancy. It can make you feel calm or sleepy.",
    tip: "Notice if you need more rest during this phase."
  },
  "Self-Care Strategies": {
    longDesc: "Self-care includes rest, nutrition, movement, and emotional support. Your needs may change with each phase.",
    tip: "Listen to your body and honor what it needs."
  },
  "Stress Management": {
    longDesc: "Stress can affect your cycle. Mindfulness, gentle exercise, and talking to someone you trust can help.",
    tip: "Try deep breathing or a short walk to reset."
  },
  "Sleep Optimization": {
    longDesc: "Good sleep supports hormone balance and mood. Aim for 7-9 hours and keep a regular sleep schedule.",
    tip: "Wind down with a calming routine before bed."
  },
  "Nutrition for Cycle Support": {
    longDesc: "Eating a variety of whole foods, including iron-rich and anti-inflammatory foods, can support your cycle.",
    tip: "Stay hydrated and eat regular meals for steady energy."
  },
  // Recommended topics
  "Mindfulness for Cycle Harmony": {
    longDesc: "Mindfulness can help you tune into your body and emotions throughout your cycle. Try meditation, journaling, or gentle yoga.",
    tip: "A few minutes of mindful breathing can make a big difference."
  },
  "Cycle-Syncing Workouts": {
    longDesc: "Adjusting your workouts to your cycle can boost energy and reduce discomfort. Try gentle movement during your period and more intense exercise during the follicular and ovulatory phases.",
    tip: "Listen to your body and rest when needed."
  },
  "Nourishing Your Body Through Each Phase": {
    longDesc: "Your nutritional needs change throughout your cycle. Focus on iron-rich foods during your period and complex carbs in the luteal phase.",
    tip: "Meal prep can help you stay nourished and energized."
  },
};

export default function Learn() {
  const [selectedCategory, setSelectedCategory] = useState<Category>("All");
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState<{ title: string; longDesc: string; tip: string } | null>(null);

  const filteredTopics = allTopics.filter(topic =>
    (selectedCategory === "All" || topic.category === selectedCategory) &&
    (topic.title.toLowerCase().includes(search.toLowerCase()) || topic.desc.toLowerCase().includes(search.toLowerCase()))
  );

  function handleSearchChange(e: ChangeEvent<HTMLInputElement>) {
    setSearch(e.target.value);
  }

  function handleRecommendedClick(title: string) {
    const details = topicDetails[title] || { longDesc: "No details available.", tip: "" };
    setModal({ title, ...details });
  }

  function handleTopicClick(title: string) {
    const details = topicDetails[title] || { longDesc: "No details available.", tip: "" };
    setModal({ title, ...details });
  }

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-pink-50 via-blue-50 to-purple-50 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-10 w-72 h-72 bg-gradient-to-r from-pink-200 to-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-gradient-to-r from-blue-200 to-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-gradient-to-r from-purple-200 to-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 container mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-pink-400 to-purple-500 rounded-full mb-6 shadow-lg">
            <span className="text-3xl">📚</span>
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-600 via-purple-600 to-blue-600 bg-clip-text text-transparent mb-4">
            Learn & Explore
          </h1>
          <p className="text-xl text-gray-700 max-w-2xl mx-auto leading-relaxed font-medium">
            Empower yourself with knowledge about your cycle, hormones, and self-care. 
            Explore bite-sized, evidence-based topics and tips.
          </p>
        </div>

        {/* Search Bar */}
        <div className="max-w-2xl mx-auto mb-16">
          <div className="relative">
            <input
              type="text"
              placeholder="Search topics..."
              value={search}
              onChange={handleSearchChange}
              className="w-full p-4 pl-12 rounded-2xl border-2 border-pink-200 focus:outline-none focus:ring-4 focus:ring-pink-200 focus:border-pink-400 shadow-lg bg-white/80 backdrop-blur-sm text-lg"
            />
            <div className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400">
              🔍
            </div>
          </div>
        </div>

        {/* Recommended Section */}
        <div className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-2">Recommended for You</h2>
            <p className="text-gray-600">Curated topics based on your cycle phase</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {recommended.map((rec, index) => (
              <button 
                key={rec.id} 
                onClick={() => handleRecommendedClick(rec.title)} 
                className="group relative overflow-hidden rounded-2xl bg-white shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 focus:outline-none"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-pink-50 to-purple-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div className="relative p-6">
                  <div className="text-4xl mb-4">{rec.icon}</div>
                  <h3 className="text-xl font-bold text-gray-800 mb-2 group-hover:text-pink-600 transition-colors">{rec.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{rec.desc}</p>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Categories */}
        <div className="mb-12">
          <div className="flex justify-center gap-4 flex-wrap">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 shadow-lg border-2 transform hover:scale-105 focus:outline-none
                  ${selectedCategory === cat 
                    ? "bg-gradient-to-r from-pink-500 to-purple-500 text-white border-transparent shadow-pink-200" 
                    : "bg-white text-gray-700 border-gray-200 hover:bg-pink-50 hover:border-pink-200"}`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Topics Grid */}
        <div>
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-2">All Topics</h2>
            <p className="text-gray-600">Explore our comprehensive library</p>
          </div>
          
          {filteredTopics.length === 0 ? (
            <div className="text-center py-16">
              <div className="text-6xl mb-4">🔍</div>
              <h3 className="text-2xl font-semibold text-gray-700 mb-2">No topics found</h3>
              <p className="text-gray-500">Try a different search or category!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
              {filteredTopics.map((topic, index) => (
                <button 
                  key={topic.id} 
                  onClick={() => handleTopicClick(topic.title)} 
                  className="group text-left bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 focus:outline-none overflow-hidden"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <div className="text-3xl mr-3">{topic.icon}</div>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        topic.category === "Cycle Phases" ? "bg-pink-100 text-pink-700" :
                        topic.category === "Hormonal Changes" ? "bg-purple-100 text-purple-700" :
                        "bg-blue-100 text-blue-700"
                      }`}>
                        {topic.category}
                      </span>
                    </div>
                    <h3 className="text-xl font-bold text-gray-800 mb-3 group-hover:text-pink-600 transition-colors">{topic.title}</h3>
                    <p className="text-gray-600 leading-relaxed">{topic.desc}</p>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      {modal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full mx-4 p-8 relative animate-fade-in">
            <button 
              onClick={() => setModal(null)} 
              className="absolute top-4 right-4 w-8 h-8 flex items-center justify-center text-gray-400 hover:text-pink-500 hover:bg-pink-50 rounded-full transition-all duration-200"
            >
              ✕
            </button>
            <h2 className="text-3xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent mb-4">{modal.title}</h2>
            <p className="text-gray-700 mb-6 text-lg leading-relaxed">{modal.longDesc}</p>
            <div className="bg-gradient-to-r from-pink-100 via-purple-100 to-blue-100 rounded-2xl p-6 text-center">
              <div className="text-2xl mb-2">💡</div>
              <p className="text-pink-700 font-semibold text-lg">{modal.tip}</p>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes blob {
          0% { transform: translate(0px, 0px) scale(1); }
          33% { transform: translate(30px, -50px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
          100% { transform: translate(0px, 0px) scale(1); }
        }
        .animate-blob {
          animation: blob 7s infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
        .animate-fade-in {
          animation: fadeIn 0.3s ease-out;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: scale(0.9); }
          to { opacity: 1; transform: scale(1); }
        }
      `}</style>
    </div>
  );
}
