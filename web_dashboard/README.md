# Web Dashboard (Next.js)

Cryptocurrency sentiment analysis web dashboard built with Next.js, TypeScript, and Tailwind CSS.

## Features

- **Dark Theme UI**: Modern dark-themed interface with slate color scheme
- **Sentiment Visualization**: Interactive pie chart showing sentiment distribution (positive, negative, neutral)
- **News Feed**: Real-time display of cryptocurrency news with sentiment indicators
- **Sidebar Navigation**: Easy navigation between Dashboard, Market, and Settings pages
- **Responsive Design**: Works on desktop and tablet devices

## Tech Stack

- **Next.js 16** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **Recharts** - For sentiment pie chart visualization
- **Axios** - For API calls to the FastAPI backend
- **Lucide React** - For icons

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- FastAPI backend running on `http://127.0.0.1:8000`

### Installation

1. Navigate to the dashboard directory:
```bash
cd web_dashboard/crypto-dashboard
```

2. Install dependencies (if not already installed):
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
crypto-dashboard/
├── app/
│   ├── components/
│   │   ├── Sidebar.tsx          # Navigation sidebar
│   │   ├── SentimentChart.tsx   # Pie chart component
│   │   └── NewsList.tsx         # News feed component
│   ├── page.tsx                 # Main dashboard page
│   ├── layout.tsx               # Root layout
│   └── globals.css              # Global styles
├── public/                      # Static assets
└── package.json
```

## API Integration

The dashboard connects to the FastAPI backend at `http://127.0.0.1:8000`:

- `GET /api/stats` - Fetches sentiment statistics
- `GET /api/news?limit=20` - Fetches latest news articles

Make sure the backend server is running before starting the dashboard.

## Features in Detail

### Sentiment Chart
- Displays sentiment distribution as a pie chart
- Shows counts and percentages for each sentiment category
- Color-coded: Green (positive), Red (negative), Gray (neutral)

### News List
- Displays latest 20 news articles
- Color-coded borders based on sentiment
- Shows source, date, and sentiment score
- Clickable external links to full articles

### Sidebar
- Navigation menu with icons
- Active route highlighting
- Ready for future pages (Market, Settings)
