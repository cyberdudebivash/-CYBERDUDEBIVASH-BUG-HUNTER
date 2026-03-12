import React, { useState, useEffect } from 'react';
import { Share2, Database, ShieldCheck, Globe, Cpu } from 'lucide-react';

const SentinelApexView = () => {
  const [syncStatus, setSyncStatus] = useState('SYNCHRONIZED');
  const [uplinkStats, setUplinkStats] = useState({
    totalSyncs: 1450,
    deduplicated: 342,
    avgSyncTime: '84ms'
  });

  return (
    <div className="p-8 bg-zinc-950 rounded-2xl border border-zinc-800 shadow-2xl">
      {/* Platform Header */}
      <div className="flex justify-between items-center mb-10">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-red-600 rounded-lg">
            <Share2 className="text-white w-8 h-8" />
          </div>
          <div>
            <h2 className="text-3xl font-black text-white tracking-tighter">SENTINEL <span className="text-red-600">APEX</span></h2>
            <p className="text-xs text-zinc-500 font-bold uppercase tracking-widest">Global Intelligence Uplink // God-Mode Active</p>
          </div>
        </div>
        <div className="text-right">
          <span className="px-4 py-1 bg-green-950/30 text-green-500 border border-green-900 rounded-full text-xs font-bold animate-pulse">
            ● {syncStatus}
          </span>
        </div>
      </div>

      {/* Sync Telemetry Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <SyncMetric title="Total Ingested" value={uplinkStats.totalSyncs} icon={<Database className="text-blue-500" />} />
        <SyncMetric title="Unique Threats" value={uplinkStats.deduplicated} icon={<ShieldCheck className="text-red-500" />} />
        <SyncMetric title="Latency (Avg)" value={uplinkStats.avgSyncTime} icon={<Cpu className="text-purple-500" />} />
      </div>

      {/* Live Sync Stream */}
      <div className="bg-black border border-zinc-900 rounded-xl overflow-hidden">
        <div className="p-4 bg-zinc-900/50 border-b border-zinc-800 flex justify-between items-center">
          <h3 className="text-sm font-bold text-zinc-300 flex items-center">
            <Globe className="w-4 h-4 mr-2 text-red-600" /> Live Data Synchronization Feed
          </h3>
          <span className="text-[10px] text-zinc-500">UPLINK: v3.0.0</span>
        </div>
        <div className="p-4 h-64 overflow-y-auto space-y-3 font-mono text-[11px]">
          <SyncLog target="corp-prod.internal" type="BOLA" status="SYNCED" color="text-red-500" />
          <SyncLog target="dev-bucket-01" type="S3_EXPOSURE" status="DEDUPLICATED" color="text-yellow-500" />
          <SyncLog target="api.main-gateway" type="JWT_WEAKNESS" status="SYNCED" color="text-red-500" />
          <SyncLog target="staging-auth" type="INFO_LEAK" status="SYNCED" color="text-blue-500" />
        </div>
      </div>
    </div>
  );
};

const SyncMetric = ({ title, value, icon }) => (
  <div className="p-6 bg-zinc-900/40 border border-zinc-800 rounded-xl">
    <div className="flex items-center space-x-3 mb-2">
      {icon}
      <span className="text-[10px] font-bold text-zinc-500 uppercase">{title}</span>
    </div>
    <div className="text-2xl font-black text-white">{value}</div>
  </div>
);

const SyncLog = ({ target, type, status, color }) => (
  <div className="flex justify-between items-center border-b border-zinc-900 pb-2">
    <div className="flex space-x-4">
      <span className="text-zinc-600">[{new Date().toLocaleTimeString()}]</span>
      <span className="text-white font-bold">{target}</span>
      <span className={`${color} font-bold`}>{type}</span>
    </div>
    <span className="text-zinc-500 font-bold">{status}</span>
  </div>
);

export default SentinelApexView;