import { useState } from "react";
import { useWebSocket } from "./hooks/useWebSocket";
import { PriceCard } from "./components/PriceCard";
import { PriceChart } from "./components/PriceChart";
import { MetricsPanel } from "./components/MetricsPanel";
import { ConnectionStatus } from "./components/ConnectionStatus";

const WS_URL = `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/ws`;

const SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"];

export default function App() {
  const { prices, connected } = useWebSocket(WS_URL);
  const [selectedSymbol, setSelectedSymbol] = useState(SYMBOLS[0]);

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-xl font-bold tracking-tight">⚡ Stackera</span>
          <span className="text-xs text-gray-500 hidden sm:inline">Real-time Crypto Prices</span>
        </div>
        <ConnectionStatus connected={connected} />
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8 flex flex-col gap-8">
        {/* Price Cards */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {SYMBOLS.map((sym) => {
            const data = prices[sym];
            return data ? (
              <button
                key={sym}
                onClick={() => setSelectedSymbol(sym)}
                className={`text-left cursor-pointer transition-all ${selectedSymbol === sym ? "ring-2 ring-emerald-500/50 rounded-2xl" : ""}`}
              >
                <PriceCard data={data} />
              </button>
            ) : (
              <div
                key={sym}
                className="bg-gray-900 border border-gray-800 rounded-2xl p-6 text-gray-600 text-sm animate-pulse"
              >
                Waiting for {sym}...
              </div>
            );
          })}
        </section>

        {/* Chart */}
        <PriceChart symbol={selectedSymbol} />

        {/* Metrics */}
        <MetricsPanel />
      </main>
    </div>
  );
}
