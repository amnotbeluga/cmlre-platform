import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';
import { api } from '../api/client';

const recentLogs = [
  { id: 'LOG-001', vessel: 'FV Deep Blue', zone: 'Zone A', species: 'Yellowfin Tuna', weight: '240 kg', date: '2023-10-12' },
  { id: 'LOG-002', vessel: 'FV Sea Hawk', zone: 'Zone C', species: 'Mackerel', weight: '1,200 kg', date: '2023-10-12' },
  { id: 'LOG-003', vessel: 'FV Aqua Star', zone: 'Zone B', species: 'Sardines', weight: '3,400 kg', date: '2023-10-11' },
  { id: 'LOG-004', vessel: 'FV Deep Blue', zone: 'Zone D', species: 'Skipjack Tuna', weight: '450 kg', date: '2023-10-11' },
  { id: 'LOG-005', vessel: 'FV Marlin', zone: 'Zone F', species: 'Sardines', weight: '2,100 kg', date: '2023-10-10' },
];

const Fisheries = () => {
  const [cpueData, setCpueData] = useState<any[]>([]);

  useEffect(() => {
    const fetchCPUE = async () => {
      try {
        const response = await api.getCPUE({});
        setCpueData(response.data);
      } catch (err) {
        console.error("Failed to fetch CPUE", err);
      }
    };
    fetchCPUE();
  }, []);

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      <header>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '8px' }}>Fisheries & CPUE</h1>
        <p style={{ color: 'var(--text-secondary)' }}>Track Catch Per Unit Effort and vessel logs across distinct economic zones.</p>
      </header>


      <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
        <div className="glass-panel" style={{ padding: '24px', flex: 1, minWidth: '200px' }}>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Total Catch (This Week)</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent-primary)' }}>34.2 Tons</div>
        </div>
        <div className="glass-panel" style={{ padding: '24px', flex: 1, minWidth: '200px' }}>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Active Vessels</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent-secondary)' }}>142</div>
        </div>
        <div className="glass-panel" style={{ padding: '24px', flex: 1, minWidth: '200px' }}>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Highest Yield Zone</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: '#10b981' }}>Zone C</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        

        <div className="glass-panel" style={{ padding: '24px' }}>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '24px' }}>Catch Distribution by Zone</h2>
          <div style={{ height: '350px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={cpueData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="zone" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <YAxis stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <Tooltip 
                  cursor={{fill: 'rgba(255,255,255,0.05)'}}
                  contentStyle={{ backgroundColor: 'var(--bg-secondary)', borderColor: 'var(--glass-border)', borderRadius: '8px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend />
                <Bar dataKey="Sardines" stackId="a" fill="var(--accent-primary)" radius={[0,0,4,4]} />
                <Bar dataKey="Mackerel" stackId="a" fill="var(--accent-secondary)" />
                <Bar dataKey="Tuna" stackId="a" fill="#38bdf8" radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>


        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '24px' }}>Recent Vessel Logs</h2>
          
          <div style={{ flex: 1, overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--glass-border)', color: 'var(--text-secondary)' }}>
                  <th style={{ padding: '12px 8px', fontWeight: 500 }}>Log ID</th>
                  <th style={{ padding: '12px 8px', fontWeight: 500 }}>Vessel</th>
                  <th style={{ padding: '12px 8px', fontWeight: 500 }}>Zone</th>
                  <th style={{ padding: '12px 8px', fontWeight: 500 }}>Primary Catch</th>
                  <th style={{ padding: '12px 8px', fontWeight: 500 }}>Weight</th>
                </tr>
              </thead>
              <tbody>
                {recentLogs.map((log, i) => (
                  <tr key={log.id} style={{ 
                    borderBottom: i === recentLogs.length - 1 ? 'none' : '1px solid rgba(255,255,255,0.05)',
                    transition: 'background 0.2s'
                  }}>
                    <td style={{ padding: '16px 8px', color: 'var(--text-accent)' }}>{log.id}</td>
                    <td style={{ padding: '16px 8px', fontWeight: 500 }}>{log.vessel}</td>
                    <td style={{ padding: '16px 8px' }}>
                      <span style={{ background: 'rgba(255,255,255,0.05)', padding: '4px 8px', borderRadius: '4px', fontSize: '0.85rem' }}>
                        {log.zone}
                      </span>
                    </td>
                    <td style={{ padding: '16px 8px' }}>{log.species}</td>
                    <td style={{ padding: '16px 8px', fontWeight: 600 }}>{log.weight}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <button style={{ 
            marginTop: '16px',
            padding: '10px',
            background: 'transparent',
            color: 'var(--text-accent)',
            border: '1px solid var(--glass-border)',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.2s',
            textAlign: 'center'
          }}
          onMouseOver={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
          onMouseOut={(e) => e.currentTarget.style.background = 'transparent'}
          >
            View All Logs →
          </button>
        </div>

      </div>
    </div>
  );
};

export default Fisheries;
