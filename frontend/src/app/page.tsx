export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col relative overflow-hidden">
      {/* Decorative Gold Glows */}
      <div className="absolute top-[-20%] left-[-10%] w-[500px] h-[500px] bg-[#ff8c42]/20 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[500px] h-[500px] bg-[#ffd700]/30 rounded-full blur-[100px] pointer-events-none" />

      {/* Navbar */}

      <main className="flex-1 flex flex-col lg:flex-row items-center justify-center p-6 lg:p-24 gap-12 z-10">
        {/* Left: Hero Text */}
        <div className="flex-1 text-center lg:text-left space-y-6 max-w-2xl">
          <h2 className="text-5xl lg:text-7xl font-extrabold tracking-tight leading-tight">
            Welcome to <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#ff8c42] via-[#ffd700] to-[#ff8c42] animate-pulse">
              PanditAI
            </span>
          </h2>

          <div className="flex gap-4 justify-center lg:justify-start pt-4">
            <button className="bg-[#ff8c42] hover:bg-[#ff8c42]/90 text-white font-semibold px-8 py-3 text-lg rounded-full shadow-lg shadow-[#ff8c42]/20 transition-all hover:scale-105">
              Get Started
            </button>
          </div>
        </div>

        {/* Right: Simple Form */}
        <div className="flex-1 w-full max-w-md">
          <div className="bg-white/5 backdrop-blur-xl border border-[#ff8c42]/20 rounded-lg shadow-2xl shadow-[#ff8c42]/10 p-8">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold mb-2">Enter Birth Details</h3>
            </div>

            <div className="space-y-4">
              <div>
                <label htmlFor="dob" className="block text-sm font-medium mb-2">
                  Date of Birth
                </label>
                <input
                  type="date"
                  id="dob"
                  className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:border-[#ff8c42] focus:outline-none focus:ring-1 focus:ring-[#ff8c42]"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label
                    htmlFor="time"
                    className="block text-sm font-medium mb-2"
                  >
                    Time
                  </label>
                  <input
                    type="time"
                    id="time"
                    className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:border-[#ff8c42] focus:outline-none focus:ring-1 focus:ring-[#ff8c42]"
                  />
                </div>
                <div>
                  <label
                    htmlFor="city"
                    className="block text-sm font-medium mb-2"
                  >
                    City
                  </label>
                  <input
                    type="text"
                    id="city"
                    placeholder="New Delhi"
                    className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:border-[#ff8c42] focus:outline-none focus:ring-1 focus:ring-[#ff8c42]"
                  />
                </div>
              </div>

              <div>
                <label
                  htmlFor="ayanamsa"
                  className="block text-sm font-medium mb-2"
                >
                  Ayanamsa
                </label>
                <select
                  id="ayanamsa"
                  className="w-full px-4 py-2 bg-white/5 border border-white/20 rounded-lg focus:border-[#ff8c42] focus:outline-none focus:ring-1 focus:ring-[#ff8c42]"
                >
                  <option value="lahiri">Lahiri (Chitrapaksha)</option>
                  <option value="raman">Raman</option>
                  <option value="kp">KP</option>
                </select>
              </div>

              <button className="w-full bg-gradient-to-r from-[#ff8c42] to-[#ff6b1a] hover:from-[#ff6b1a] hover:to-[#ff8c42] text-white font-bold py-4 text-lg rounded-lg mt-6 transition-all duration-500 shadow-lg">
                Generate Horoscope
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
