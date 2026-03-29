import type { PriceUpdate } from "../hooks/useWebSocket";

const ICONS: Record<string, string> = {
  BTCUSDT: "₿",
  ETHUSDT: "Ξ",
  BNBUSDT: "◆",
};

export function PriceCard({ data }: { data: PriceUpdate }) {
  const isUp = data.change_24h >= 0;
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 flex flex-col gap-2 min-w-[220px]">
      <div className="flex items-center gap-2 text-gray-400 text-sm">
        <span className="text-2xl">{ICONS[data.symbol] ?? "●"}</span>
        <span className="font-medium">{data.symbol.replace("USDT", " / USDT")}</span>
      </div>
      <span className="text-3xl font-bold text-white tracking-tight">
        ${data.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
      </span>
      <span className={`text-sm font-semibold ${isUp ? "text-emerald-400" : "text-red-400"}`}>
        {isUp ? "▲" : "▼"} {Math.abs(data.change_24h).toFixed(2)}%
      </span>
      <span className="text-xs text-gray-600">
        {new Date(data.timestamp).toLocaleTimeString()}
      </span>
    </div>
  );
}
