export function ConnectionStatus({ connected }: { connected: boolean }) {
  return (
    <div className="flex items-center gap-2 text-sm">
      <span className={`h-2.5 w-2.5 rounded-full ${connected ? "bg-emerald-400 animate-pulse" : "bg-red-400"}`} />
      <span className={connected ? "text-emerald-400" : "text-red-400"}>
        {connected ? "Live" : "Disconnected"}
      </span>
    </div>
  );
}
