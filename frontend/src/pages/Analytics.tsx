import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter, ZAxis } from 'recharts';
import { api } from '../api/client';

const Analytics = () => {
  const [scatterData, setScatterData] = useState<any[]>([]);
  const [trendData, setTrendData] = useState<any[]>([]);
  const [correlationResult, setCorrelationResult] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [depthRes, sstRes] = await Promise.all([
          api.getDepthProfile(),
          api.getSSTAnomaly(),
        ]);

        if (Array.isArray(depthRes.data)) setScatterData(depthRes.data);
        if (Array.isArray(sstRes.data)) setTrendData(sstRes.data);
      } catch (err) {
        console.error('Failed to fetch analytics data', err);
      }
    };
    fetchData();
  }, []);

  const handleRunCorrelation = async () => {
    try {
      const res = await api.runCorrelation({ variableX: 'temperature', variableY: 'salinity' });
      setCorrelationResult(res.data);
    } catch (err) {
      console.error('Failed to run correlation', err);
    }
  };


  const displayScatter = scatterData.length > 0 ? scatterData : [
    { depth: 10, temp: 28.5, salinity: 35.1 },
    { depth: 50, temp: 26.2, salinity: 35.3 },
    { depth: 100, temp: 22.8, salinity: 35.5 },
    { depth: 200, temp: 18.1, salinity: 35.6 },
    { depth: 500, temp: 12.5, salinity: 35.8 },
    { depth: 1000, temp: 6.2, salinity: 35.9 },
    { depth: 2000, temp: 2.8, salinity: 36.1 },
  ];

  const displayTrend = trendData.length > 0 ? trendData : [
    { year: '2018', anomaly: 0.2 },
    { year: '2019', anomaly: 0.4 },
    { year: '2020', anomaly: 0.5 },
    { year: '2021', anomaly: 0.3 },
    { year: '2022', anomaly: 0.7 },
    { year: '2023', anomaly: 0.9 },
  ];

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      <header>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '8px' }}>Data Analytics & ML Models</h1>
        <p style={{ color: 'var(--text-secondary)' }}>Advanced exploratory data analysis and predictive modeling for marine trends.</p>
      </header>

      <div style={{ display: 'flex', gap: '16px', marginBottom: '8px' }}>
        <button style={{ padding: '8px 16px', background: 'var(--accent-primary)', color: '#fff', border: 'none', borderRadius: '20px', fontWeight: 600 }}>Climate Anomalies</button>
        <button style={{ padding: '8px 16px', background: 'transparent', color: 'var(--text-secondary)', border: '1px solid var(--glass-border)', borderRadius: '20px' }}>Predictive Yields</button>
        <button style={{ padding: '8px 16px', background: 'transparent', color: 'var(--text-secondary)', border: '1px solid var(--glass-border)', borderRadius: '20px' }}>Current Modeling</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        

        <div className="glass-panel" style={{ padding: '24px' }}>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '8px' }}>Depth Profile Correlation</h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '24px' }}>Temperature vs Depth (Colored by Salinity)</p>
          
          <div style={{ height: '300px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="temp" type="number" name="Temp" unit="°C" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <YAxis dataKey="depth" type="number" name="Depth" unit="m" reversed={true} stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <ZAxis dataKey="salinity" type="number" range={[50, 400]} name="Salinity" unit=" PSU" />
                <Tooltip 
                  cursor={{strokeDasharray: '3 3'}}
                  contentStyle={{ backgroundColor: 'var(--bg-secondary)', borderColor: 'var(--glass-border)', borderRadius: '8px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Scatter name="Sensor Data" data={displayScatter} fill="var(--accent-primary)" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>


        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>SST Anomaly Trends</h2>
            <div style={{ background: '#ef444422', color: '#ef4444', padding: '4px 10px', borderRadius: '12px', fontSize: '0.8rem', fontWeight: 600 }}>High Alert</div>
          </div>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '24px' }}>Historical progression of Sea Surface Temperature anomalies (°C).</p>
          
          <div style={{ height: '300px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={displayTrend} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="year" stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <YAxis stroke="var(--text-secondary)" tick={{fill: 'var(--text-secondary)'}} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--bg-secondary)', borderColor: 'var(--glass-border)', borderRadius: '8px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Line type="monotone" dataKey="anomaly" stroke="#ef4444" strokeWidth={3} dot={{ r: 6, fill: '#ef4444', strokeWidth: 2, stroke: 'var(--bg-primary)' }} activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>


      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '4px' }}>Run Correlation Analysis</h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>Compute Pearson correlation between oceanographic variables across depth gradients.</p>
            
            {correlationResult && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginTop: '8px' }}>
                <div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Correlation (r)</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#ef4444' }}>{correlationResult.correlationCoefficient}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>p-value</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#10b981' }}>{correlationResult.pValue}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>R²</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--accent-primary)' }}>{correlationResult.rSquared}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Method</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 700 }}>{correlationResult.method}</div>
                </div>
              </div>
            )}

            {correlationResult?.interpretation && (
              <p style={{ fontSize: '0.85rem', color: 'var(--text-accent)', marginTop: '12px', fontStyle: 'italic' }}>
                💡 {correlationResult.interpretation}
              </p>
            )}
          </div>
          <button 
            onClick={handleRunCorrelation}
            style={{ 
              padding: '12px 24px', 
              background: 'linear-gradient(90deg, var(--accent-secondary), var(--accent-primary))', 
              color: '#fff', 
              border: 'none', 
              borderRadius: '8px', 
              fontWeight: 600, 
              cursor: 'pointer',
              boxShadow: '0 4px 12px rgba(14, 165, 233, 0.3)',
              whiteSpace: 'nowrap',
            }}
          >
            Execute Analysis
          </button>
        </div>
      </div>

    </div>
  );
};

export default Analytics;
