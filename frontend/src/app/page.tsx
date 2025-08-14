'use client'

import FileUploader from '../../components/FileUploader'

export default function Home() {
  return (
    <div className="max-w-3xl mx-auto">
      <div className="text-center mb-16">
        <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-red-500 via-orange-500 to-red-600 bg-clip-text text-transparent">
          Ready for Destruction?
        </h1>
        <p className="text-white/80 text-xl leading-relaxed max-w-2xl mx-auto">
          Upload your resume and discover everything that's wrong with it. 
          <br />
          <span className="text-red-400 font-medium">Don't worry, we'll also tell you how to fix it.</span>
        </p>
      </div>
      
      {/* Upload Section and data section */}
      <div className="bg-gray-900/70 backdrop-blur-xl border border-red-500/20 rounded-2xl p-8 shadow-2xl">
        <FileUploader />
        
        {/* Info cards */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-center hover:bg-red-500/20 transition-colors">
            <div className="text-3xl mb-3">📄</div>
            <h3 className="text-white font-semibold mb-2">Supported Formats</h3>
            <p className="text-white/60 text-sm">PDF, DOC, DOCX</p>
          </div>
          
          <div className="bg-orange-500/10 border border-orange-500/20 rounded-xl p-6 text-center hover:bg-orange-500/20 transition-colors">
            <div className="text-3xl mb-3">🔒</div>
            <h3 className="text-white font-semibold mb-2">Secure Processing</h3>
            <p className="text-white/60 text-sm">Your CV is processed safely and <b>not stored</b></p>
          </div>
          
          <div className="bg-red-600/10 border border-red-600/20 rounded-xl p-6 text-center hover:bg-red-600/20 transition-colors">
            <div className="text-3xl mb-3">⚡</div>
            <h3 className="text-white font-semibold mb-2">Fast Results</h3>
            <p className="text-white/60 text-sm">Get roasted in seconds</p>
          </div>
        </div>
      </div>
    </div>
  )
}