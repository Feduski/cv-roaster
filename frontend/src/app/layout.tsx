import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Resume Roaster',
  description: 'Your CV got roasted. Time to change it!',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className={inter.className}>
        <div className="fixed inset-0 bg-black">          
          {/* Background */}
          <div className="absolute inset-0 bg-black/50" style={{
            backgroundImage: `
              linear-gradient(rgba(255,69,0,0.15) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255, 68, 0, 0.20) 1px, transparent 1px)
            `,
            backgroundSize: '50px 50px'
          }}></div>
        </div>

        {/* NavBar */}  
        <div className="relative z-10 min-h-screen">
          <nav className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
            <div className="bg-black/80 backdrop-blur-xl border border-red-900 rounded-full px-8 py-3 shadow-2xl">
              <div className="flex items-center justify-center space-x-8">
                <Link href="/" className="text-red-500 font-bold text-xl hover:text-orange-500/80 transition-colors">
                  🔥 Resume Roaster
                </Link>
              </div>
            </div>
          </nav>

          {/* Contenido principal */}
          <main className="pt-32 px-4 pb-8">
            <div className="container mx-auto">
              {children}
            </div>
          </main>
        </div>
      </body>
    </html>
  )
}