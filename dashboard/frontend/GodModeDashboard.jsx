import React, { useState, useEffect } from 'react';
import { Activity, ShieldAlert, Globe, Zap, DollarSign, Terminal } from 'lucide-react';

const GodModeDashboard = () => {
  const [stats, setStats] = useState({
    activeSworms: 0,
    criticalFindings: 0,
    targetsProcessed: 0,
    preventedLoss: 0
  });

  // Mock data for ROI visualization - integrates with analytics/roi_calculator.py
  const [liveAlerts, setLiveAlerts] = useState([]);

  return (
    <div className="min-h-screen bg-black text-white p-8 font-mono">
      {/* Header: CyberDudeBivash Authority Branding */}
      <div className="flex justify-between items-center border-b border-red-900 pb-6 mb-8">
        <div>
          <h1 className="text-4xl font-black text-red-600 tracking-tighter uppercase">
            CyberDudeBivash <span className="text-white">Bug Hunter</span>
          </h1>
          <p className="text-gray-500 text-sm tracking-widest uppercase mt-1">
            God-Mode Command Center // Global Threat Intelligence
          </p>
        </div>
        <div className="flex items-center space-x-4 bg-red-950/20 p-3 rounded-lg border border-red-900">
          <Activity className="text-green-500 animate-pulse" />
          <span className="text-sm font-bold text-green-500">SWARM STATUS: OPTIMAL</span>
        </div>
      </div>

      {/* High-Level ROI & Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <MetricCard title="Active Swarms" value="24" icon={<Globe className="text-blue-500" />} />
        <MetricCard title="Critical Findings" value="142" icon={<ShieldAlert className="text-red-500" />} />
        <MetricCard title="Potential ROI" value="$4.2M" icon={<DollarSign className="text-green-500" />} />
        <MetricCard title="Throughput" value="12k/hr" icon={<Zap className="text-yellow-500" />} />
      </div>

      {/* Central Terminal and Live Intel Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Real-Time Attack Path Visualization (Reasoning Orchestrator Output) */}
        <div className="lg:col-span-2 bg-zinc-900/50 rounded-xl border border-zinc-800 p-6">
          <h2 className="text-xl font-bold mb-4 flex items-center">
            <Terminal className="mr-2 text-red-600" /> Autonomous Reasoning Logs
          </h2>
          <div className="h-96 bg-black rounded-lg p-4 font-mono text-xs overflow-y-auto space-y-2 border border-zinc-800">
            <LogEntry time="01:09:01" msg="[GOD-MODE] New Finding: S3 Bucket 'tesla-dev-assets' exposed." />
            <LogEntry time="01:09:05" msg="[REASONING] Analyzing lateral movement potential..." />
            <LogEntry time="01:09:08" msg="[PIVOT] High Priority: Targeting linked cloud credentials." />
            <LogEntry time="01:09:12" msg="[SWARM] Sharding 12 new tasks to worker node 04." />
          </div>
        </div>

        {/* Live Finding Ticker */}
        <div className="bg-zinc-900/50 rounded-xl border border-zinc-800 p-6">
          <h2 className="text-xl font-bold mb-4">Critical Vulnerabilities</h2>
          <div className="space-y-4">
            <FindingRow domain="paypal.com" type="BOLA" severity="9.8" />
            <FindingRow domain="netflix.com" type="Cloud Leak" severity="8.5" />
            <FindingRow domain="google.com" type="API Exposure" severity="7.2" />
          </div>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ title, value, icon }) => (
  <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-xl hover:border-red-600 transition-colors">
    <div className="flex justify-between items-center mb-2">
      <p className="text-gray-400 text-xs font-bold uppercase">{title}</p>
      {icon}
    </div>
    <p className="text-3xl font-black">{value}</p>
  </div>
);

const LogEntry = ({ time, msg }) => (
  <p><span className="text-red-600">[{time}]</span> <span className="text-green-500">{msg}</span></p>
);

const FindingRow = ({ domain, type, severity }) => (
  <div className="flex justify-between items-center p-3 bg-black rounded border border-zinc-800">
    <div>
      <p className="text-sm font-bold text-white">{domain}</p>
      <p className="text-[10px] text-gray-500 uppercase">{type}</p>
    </div>
    <span className="text-red-600 font-black px-2 py-1 bg-red-950/20 rounded border border-red-900">
      {severity}
    </span>
  </div>
);

export default GodModeDashboard;