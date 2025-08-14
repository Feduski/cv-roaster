'use client'

import { useParams } from 'next/navigation'
import Link from 'next/link'

export default function RoastPage() {
  const params = useParams()
  const roastId = params.id

  // Contenido simulado
  const mockRoast = "Here would be the roast part about ur cv"

  const mockFeedback = [
    "Point 1",
    "Point 2",
    "Point 3",  
    "Point 4",
  ]

  return (
    <div className="max-w-5xl mx-auto space-y-10">
      {/* Header animado */}
      <div className="text-center">
        <div className="inline-block animate-bounce mb-4">
          <span className="text-6xl">💀</span>
        </div>
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-red-500 via-orange-500 to-red-600 bg-clip-text text-transparent">
          Your CV Got Roasted
        </h1>
        <div className="bg-black/40 backdrop-blur-xl border border-red-500/20 rounded-full px-6 py-2 inline-block">
          <p className="text-white/80">Roast ID: <span className="text-red-400 font-mono">{roastId}</span></p>
        </div>
      </div>

      {/* Roast Section */}
      <div className="bg-black/60 backdrop-blur-xl border border-red-500/30 rounded-2xl p-8 shadow-2xl shadow-red-500/10">
        <div className="flex items-center mb-6">
          <div className="w-12 h-12 bg-red-500/20 rounded-xl flex items-center justify-center mr-4">
            <span className="text-2xl">🔥</span>
          </div>
          <h2 className="text-3xl font-bold text-white">
            The Truth... 
          </h2>
        </div>
        
        <div className="bg-black/80 rounded-xl p-8 border border-red-500/20 relative overflow-hidden">
          {/* Animated background */}
          <div className="absolute inset-0 bg-gradient-to-r from-red-500/5 via-orange-500/5 to-red-600/5 animate-pulse"></div>
          
          <div className="relative z-10">
            <div className="flex items-start space-x-4">
              <div className="w-8 h-8 bg-red-500/30 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                <span className="text-red-400 text-lg">💬</span>
              </div>
              <blockquote className="text-white text-xl leading-relaxed italic font-medium">
                "{mockRoast}"
              </blockquote>
            </div>
          </div>
        </div>
      </div>

      {/* Feedback Section */}
      <div className="bg-black/60 backdrop-blur-xl border border-orange-500/30 rounded-2xl p-8 shadow-2xl shadow-orange-500/10">
        <div className="flex items-center mb-6">
          <div className="w-12 h-12 bg-orange-500/20 rounded-xl flex items-center justify-center mr-4">
            <span className="text-2xl">💡</span>
          </div>
          <h2 className="text-3xl font-bold text-white">
            How to Fix This Mess
          </h2>
        </div>
        
        <div className="space-y-4">
          {mockFeedback.map((tip, index) => (
            <div 
              key={index} 
              className="bg-black/40 rounded-xl p-6 border border-orange-500/20 hover:bg-orange-500/10 transition-colors group"
            >
              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                  <span className="text-black font-bold text-sm">{index + 1}</span>
                </div>
                <p className="text-white text-lg leading-relaxed">{tip}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="bg-black/40 backdrop-blur-xl border border-red-500/20 rounded-2xl p-8">
        <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
          <Link 
            href="/"
            className="group relative px-8 py-4 bg-gradient-to-r from-red-600 to-orange-500 hover:from-red-700 hover:to-orange-600 text-white rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-2xl hover:shadow-red-500/25"
          >
            <div className="flex items-center space-x-3">
              <span className="text-xl group-hover:animate-spin">🔄</span>
              <span>Roast Another CV</span>
            </div>
          </Link>
          
          <button className="group px-8 py-4 bg-gradient-to-r from-gray-700 to-gray-600 hover:from-gray-600 hover:to-gray-500 text-white rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105">
            <div className="flex items-center space-x-3">
              <span className="text-xl group-hover:animate-pulse">📤</span>
              <span>Share Roast</span>
            </div>
          </button>
        </div>
      </div>

      {/* Fun stats, static 4 now*/}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-black/40 backdrop-blur-xl border border-red-500/20 rounded-xl p-6 text-center">
          <div className="text-3xl mb-2">🎯</div>
          <div className="text-2xl font-bold text-red-400 mb-1">87%</div>
          <div className="text-white/60 text-sm">Brutality Level</div>
        </div>
        
        <div className="bg-black/40 backdrop-blur-xl border border-orange-500/20 rounded-xl p-6 text-center">
          <div className="text-3xl mb-2">⚡</div>
          <div className="text-2xl font-bold text-orange-400 mb-1">2.3s</div>
          <div className="text-white/60 text-sm">Roast Time</div>
        </div>
    
      </div>
    </div>
  )
}