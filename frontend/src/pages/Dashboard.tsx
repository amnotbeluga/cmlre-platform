import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const mockData = [
  { name: 'Jan', temp: 24.2, salinity: 35.1 },
  { name: 'Feb', temp: 24.5, salinity: 35.2 },
  { name: 'Mar', temp: 25.1, salinity: 35.4 },
  { name: 'Apr', temp: 26.8, salinity: 35.6 },
  { name: 'May', temp: 28.2, salinity: 35.8 },
  { name: 'Jun', temp: 29.5, salinity: 35.5 },
  { name: 'Jul', temp: 28.9, salinity: 34.2 },
];

const StatCard = ({ title, value, change, isPositive }: { title: string, value: string, change: string, isPositive: boolean }) => (
  <div className="glass-panel" style={{ padding: '24px', flex: 1 }}>
    <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontWeight: 500, marginBottom: '8px' }}>{title}</h3>
    <div style={{ display: 'flex', alignItems: 'flex-end', gap: '12px' }}>
      <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--text-primary)' }}>{value}</div>
      <div style={{ fontSize: '0.9rem', fontWeight: 600, color: isPositive ? '#10b981' : '#ef4444', marginBottom: '6px' }}>
        {isPositive ? '↑' : '↓'} {change}
      </div>
    </div>
  </div>
);

const Dashboard = () => {
  return (
    <div>
      <header style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '8px' }}>Platform Overview</h1>
        <p style={{ color: 'var(--text-secondary)' }}>Live telemetry and analytics from the Arabian Sea and Bay of Bengal.</p>
      </header>


      <div style={{ display: 'flex', gap: '24px', marginBottom: '32px', flexWrap: 'wrap' }}>
        <StatCard title="Active Sensors" value="1,284" change="12 today" isPositive={true} />
        <StatCard title="Data Points Ingested" value="24.5M" change="1.2M/hr" isPositive={true} />
        <StatCard title="Avg Sea Surface Temp" value="28.2°C" change="0.4°C" isPositive={true} />
        <StatCard title="Anomaly Alerts" value="3" change="2 less than yesterday" isPositive={false} />
      </div>


      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        

        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>SST & Salinity Trends (Arabian Sea)</h2>
            <select style={{ background: 'var(--bg-tertiary)', color: 'var(--text-primary)', border: '1px solid var(--glass-border)', padding: '6px 12px', borderRadius: '8px', outline: 'none' }}>
              <option>Last 6 Months</option>
              <option>Last Year</option>
            </select>
          </div>
          
          <div style={{ height: '300px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="name" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <YAxis stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--bg-secondary)', borderColor: 'var(--glass-border)', borderRadius: '8px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="temp" stroke="var(--accent-primary)" strokeWidth={3} fillOpacity={1} fill="url(#colorTemp)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>


        <div className="glass-panel" style={{ padding: '24px' }}>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '24px' }}>System Health</h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {[
              { name: 'Ingestion Pipeline', status: 'Healthy', color: '#10b981' },
              { name: 'TimescaleDB Cluster', status: 'Healthy', color: '#10b981' },
              { name: 'AI Models (GPU)', status: 'Heavy Load', color: '#f59e0b' },
              { name: 'Kafka Brokers', status: 'Healthy', color: '#10b981' },
            ].map(sys => (
              <div key={sys.name} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px', background: 'rgba(255,255,255,0.02)', borderRadius: '8px' }}>
                <span style={{ fontWeight: 500 }}>{sys.name}</span>
                <span style={{ fontSize: '0.85rem', color: sys.color, background: `${sys.color}22`, padding: '4px 10px', borderRadius: '12px', fontWeight: 600 }}>
                  {sys.status}
                </span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};

export default Dashboard;
