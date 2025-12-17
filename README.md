# PanditAI 🕉️

A Neuro-Symbolic Vedic Astrology application that combines ancient astrological wisdom with modern AI.

## What It Is

PanditAI generates personalized Vedic horoscope readings by:

1. Calculating precise planetary positions using Swiss Ephemeris
2. Applying classical Vedic astrology rules from a knowledge graph
3. Synthesizing insights using AI (Groq/Ollama)

## Tech Stack

### Backend

- **FastAPI** - REST API server
- **Python** - Core logic
- **Swiss Ephemeris** - Astronomical calculations
- **Neo4j** - Knowledge graph for astrological rules
- **Groq API** - AI inference (with Ollama fallback)

### Frontend

- **Next.js** - React framework
- **Tailwind CSS** - Styling
- **TypeScript** - Type safety

## Features

- ✨ Precise astronomical calculations (Planets, Houses, Ascendant)
- 📊 Advanced techniques (Navamsa D9, Jaimini Karakas, Arudha Padas)
- 🧠 AI-powered natural language readings
- 🎨 Modern, responsive UI with dark theme
- 🔮 Multiple Ayanamsa systems (Lahiri, Raman, KP)

## How It Works

```
User Input (Birth Details)
    ↓
Backend API (/calculate)
    ↓
├─ Astronomy Engine → Planetary Positions
├─ Knowledge Graph → Astrological Rules
└─ AI Model → Natural Language Reading
    ↓
JSON Response → Frontend Display
```

## Folder Structure

```
PanditAI/
├── backend/              # Python FastAPI server
│   ├── src/
│   │   ├── api/         # API endpoints
│   │   ├── astronomy/   # Calculation engine
│   │   ├── knowledge_graph/  # Neo4j queries
│   │   └── model/       # AI inference
│   ├── data/            # Ephemeris files
│   └── requirements.txt
│
├── frontend/            # Next.js application
│   ├── src/
│   │   ├── app/        # Pages & routes
│   │   └── components/ # UI components
│   └── package.json
│
└── docker-compose.yml   # Neo4j database
```

## Quick Start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python setup_data.py  # Download ephemeris files
python -m uvicorn src.api.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`

## Environment Variables

Create `backend/.env`:

```
GROQ_API_KEY=your_groq_api_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

## Future Upgrades

- [ ] Custom fine-tuned AI model for astrology
- [ ] Geocoding API integration for city → coordinates
- [ ] User authentication & saved profiles
- [ ] Transit predictions & compatibility analysis
- [ ] Mobile app (React Native)
- [ ] Multi-language support

## License

MIT
