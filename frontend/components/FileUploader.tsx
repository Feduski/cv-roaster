'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function FileUploader() {
  const [file, setFile] = useState<File | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const router = useRouter()

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile && isValidFile(droppedFile)) {
      setFile(droppedFile)
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile && isValidFile(selectedFile)) {
      setFile(selectedFile)
    }
  }

  const isValidFile = (file: File) => {
    const validTypes = [
      'application/pdf', 
      'application/msword', 
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
    const maxSize = 5 * 1024 * 1024 // 5MB
    
    if (!validTypes.includes(file.type)) {
      alert('Please upload a PDF or DOC file')
      return false
    }
    
    if (file.size > maxSize) {
      alert('File is too large. Maximum 5MB')
      return false
    }
    
    return true
  }

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      //Por ahora en localhost. 
      const response = await fetch('http://localhost:8000/api/v1/upload-cv', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const data = await response.json();
      if (data && data.roast_id) {
        router.push(`/roast/${data.roast_id}`);
      } else {
        throw new Error('No roast_id returned');
      }
    } catch (error: any) {
      console.error('Error uploading file:', error);
      alert('Error uploading file. ' + (error.message || 'Please try again.'));
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <div className="space-y-8">
      {/* Zona de drag & drop */}
        <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-input')?.click()}
        className={`
            relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-500 transform cursor-pointer
            ${isDragging 
            ? 'border-red-500 bg-red-500/20 scale-105 shadow-2xl shadow-red-500/25' 
            : 'border-red-500/30 hover:border-red-500/60 bg-black/20 hover:bg-red-500/10 hover:scale-102'
            }
        `}
        >
        {/* Fondo animado */}
        <div className="absolute inset-0 rounded-2xl overflow-hidden">
            <div className={`absolute inset-0 bg-gradient-to-r from-red-500/5 via-orange-500/5 to-red-600/5 ${isDragging ? 'animate-pulse' : ''}`}></div>
        </div>

        {/* Texto (sin bloquear clics) */}
        <div className="relative z-10 text-white pointer-events-none">
            <div className={`text-6xl mb-6 transition-transform duration-300 ${isDragging ? 'scale-110' : ''}`}>
            {isDragging ? '🔥' : '📄'}
            </div>
            <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-red-400 to-orange-500 bg-clip-text text-transparent">
            {isDragging ? 'Drop it like it\'s hot!' : 'Drag your resume here'}
            </h3>
            <p className="text-white/60 text-lg mb-8">
            or click to select from your computer
            </p>
            <div className="text-sm text-white/40 space-y-1">
            <p>📋 Accepted: PDF, DOC, DOCX</p>
            <p>📏 Max size: 5MB</p>
            </div>
        </div>

        <input
            type="file"
            onChange={handleFileInput}
            accept=".pdf,.doc,.docx"
            className="hidden"
            id="file-input"
        />
        </div>

      {/* Archivo seleccionado */}
      {file && (
        <div className="bg-black/60 backdrop-blur-xl border border-red-500/30 rounded-xl p-6 transform animate-slideIn">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-red-500/20 rounded-xl flex items-center justify-center">
                <span className="text-2xl">📎</span>
              </div>
              <div>
                <p className="text-white font-semibold text-lg">{file.name}</p>
                <div className="flex items-center space-x-4 text-white/60 text-sm">
                  <span>{(file.size / 1024 / 1024).toFixed(2)} MB</span>
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  <span>Ready to roast</span>
                </div>
              </div>
            </div>
            {/* Botón para sacar el archivo*/}
            <button
              onClick={() => setFile(null)}
              className="text-white/60 hover:text-red-500 transition-colors p-2 hover:bg-red-500/10 rounded-lg"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Botón de upload */}
      {file && (
        <div className="space-y-4">
          <button
            onClick={handleUpload}
            disabled={isUploading}
            className={`
              relative w-full py-6 rounded-2xl font-bold text-xl transition-all duration-300 overflow-hidden
              ${isUploading
                ? 'bg-gray-800 cursor-not-allowed'
                : 'bg-gradient-to-r from-red-600 via-red-500 to-orange-500 hover:from-red-700 hover:via-red-600 hover:to-orange-600 transform hover:scale-105 hover:shadow-2xl hover:shadow-red-500/25'
              }
              text-white
            `}
          >
            {/* Animated background for loading */}
            {isUploading && (
              <div className="absolute inset-0 bg-gradient-to-r from-red-900 via-orange-900 to-red-900 animate-pulse"></div>
            )}
            
            <div className="relative z-10 flex items-center justify-center space-x-3">
              {isUploading ? (
                <>
                  <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Preparing the destruction...</span>
                </>
              ) : (
                <>
                  <span className="text-2xl">🔥</span>
                  <span>ROAST MY CV!</span>
                </>
              )}
            </div>
          </button>
          
          <p className="text-center text-white/40 text-sm">
            ⚠️ Warning: This process may hurt your feelings 
          </p>
        </div>
      )}
    </div>
  )
}