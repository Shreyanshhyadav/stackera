import { useApi } from "../hooks/useApi";

interface ServerMetrics {
  uptime_seconds: number;
  total_messages_received: number;
  total_messages_sent: number;
  current_clients: number;
  errors_count: number;
  messages_per_second: number;
  last_binance_update: string | null;
}

function formatUptime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `${h}h ${m}m ${s}s`;
}

export function MetricsPanel() {
  const { data, loading } = useApi<ServerMetrics>("/metrics", 5000);

  if (loading || !data) {
    return (
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 text-gray-500 text-sm">
        Loading metrics...
      </div>
    );
  }

  const items = [
    { label: "Uptime", value: formatUptime(data.uptime_seconds) },
    { label: "Connected Clients", value: data.current_clients },
    { label: "Messages In", value: data.total_messages_received.toLocaleString() },
    { label: "Messages Out", value: data.total_messages_sent.toLocaleString() },
    { label: "Msg/sec", value: data.messages_per_second.toFixed(1) },
    { label: "Errors", value: data.errors_count },
  ];

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
      <h3 className="text-gray-400 text-sm mb-4 font-medium">Server Metrics</h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
        {items.map((item) => (
          <div key={item.label}>
            <p className="text-xs text-gray-500">{item.label}</p>
            <p className="text-lg font-semibold text-white">{item.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
