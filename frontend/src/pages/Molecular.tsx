import { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, ResponsiveContainer, Legend } from 'recharts';
import { api } from '../api/client';

const Molecular = () => {
  const [ednaComposition, setEdnaComposition] = useState<any[]>([]);
  const [sequence, setSequence] = useState<string[]>([]);
  const [gcContent, setGcContent] = useState<number>(0);
  const [samples, setSamples] = useState<any[]>([]);
  const [activeSample, setActiveSample] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [compRes, seqRes, samplesRes] = await Promise.all([
          api.getEDNAComposition(),
          api.getEDNASequence(),
          api.getEDNASamples(),
        ]);

        if (Array.isArray(compRes.data)) setEdnaComposition(compRes.data);
        if (seqRes.data?.sequence) {
          const seq = seqRes.data.sequence;
          setSequence(seq.match(/.{1,66}/g) || []);
          setGcContent(seqRes.data.gcContent || 0);
        }
        if (Array.isArray(samplesRes.data) && samplesRes.data.length > 0) {
          setSamples(samplesRes.data);
          setActiveSample(samplesRes.data[0]);
        }
      } catch (err) {
        console.error('Failed to fetch molecular data', err);
      }
    };
    fetchData();
  }, []);


  const displayComposition = ednaComposition.length > 0 ? ednaComposition : [
    { name: 'Teleostei (Bony Fish)', value: 45, color: '#0ea5e9' },
    { name: 'Crustacea', value: 20, color: '#8b5cf6' },
    { name: 'Cnidaria (Jellyfish)', value: 12, color: '#06b6d4' },
    { name: 'Mollusca', value: 10, color: '#10b981' },
    { name: 'Echinodermata', value: 8, color: '#f59e0b' },
    { name: 'Unclassified', value: 5, color: '#64748b' },
  ];

  const displaySequence = sequence.length > 0 ? sequence : 
    `ATGGCGTACCCGTAGCTACGTAGGCTTACGGTTTAAGCGCATTACGATCGCGTTAGCGCATATCGG
CCATAGCGCTAGCCTTAGCGTAGCATCGGCTAACGTAGCTACGTAGCTAGCATCGGCTAACGTAGC
TACGTAGCTAGCATCGGCTAACGTAGCTACGTAGCTAGCATCGGCTAACGTAGCTACGTAGCTAGC
ATCGGCTAACGTAGCTACGTAGCTAGCATCGGCTAACGTAGCTACGTAGCTAGCATCGGCTAACGT`.match(/.{1,66}/g) || [];

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      <header>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '8px' }}>Molecular & eDNA Sequencing</h1>
        <p style={{ color: 'var(--text-secondary)' }}>Environmental DNA (eDNA) analysis and genomic sequencing records from oceanic sampling sites.</p>
      </header>


      {samples.length > 0 && (
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {samples.map(s => (
            <button
              key={s.sampleId}
              onClick={() => setActiveSample(s)}
              style={{
                padding: '6px 14px',
                background: activeSample?.sampleId === s.sampleId ? 'var(--accent-primary)' : 'transparent',
                color: activeSample?.sampleId === s.sampleId ? '#fff' : 'var(--text-secondary)',
                border: '1px solid var(--glass-border)',
                borderRadius: '20px',
                cursor: 'pointer',
                fontSize: '0.85rem',
                fontWeight: 600,
                transition: 'all 0.2s ease',
              }}
            >
              {s.sampleId}
            </button>
          ))}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        

        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Active Sequence Viewer</h2>
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              {gcContent > 0 && (
                <div style={{ background: 'rgba(14, 165, 233, 0.1)', color: '#0ea5e9', padding: '4px 12px', borderRadius: '16px', fontSize: '0.85rem', fontWeight: 600 }}>
                  GC: {gcContent}%
                </div>
              )}
              <div style={{ background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', padding: '4px 12px', borderRadius: '16px', fontSize: '0.85rem', fontWeight: 600 }}>
                {activeSample ? activeSample.location : 'Sample: AS-012'}
              </div>
            </div>
          </div>

          <div style={{ 
            flex: 1, 
            background: 'var(--bg-primary)', 
            padding: '24px', 
            borderRadius: '12px',
            fontFamily: '"Fira Code", "Courier New", monospace',
            fontSize: '0.9rem',
            color: 'var(--text-secondary)',
            border: '1px solid var(--glass-border)',
            overflowX: 'auto',
            lineHeight: 1.8
          }}>
            {displaySequence.map((line, i) => (
              <div key={i} style={{ display: 'flex', gap: '16px' }}>
                <span style={{ color: '#475569', userSelect: 'none' }}>{(i * 66).toString().padStart(4, '0')}</span>
                <span>
                  {line.split('').map((char, j) => {
                    let color = 'var(--text-primary)';
                    if (char === 'A') color = '#ef4444'; // Red
                    if (char === 'T') color = '#3b82f6'; // Blue
                    if (char === 'C') color = '#10b981'; // Green
                    if (char === 'G') color = '#f59e0b'; // Yellow
                    return <span key={j} style={{ color, fontWeight: 600 }}>{char}</span>;
                  })}
                </span>
              </div>
            ))}
          </div>

          <div style={{ display: 'flex', gap: '12px', marginTop: '24px' }}>
            <button style={{ flex: 1, padding: '12px', background: 'var(--accent-primary)', color: '#fff', border: 'none', borderRadius: '8px', fontWeight: 600, cursor: 'pointer' }}>Run BLAST Alignment</button>
            <button style={{ flex: 1, padding: '12px', background: 'transparent', color: 'var(--text-primary)', border: '1px solid var(--glass-border)', borderRadius: '8px', fontWeight: 600, cursor: 'pointer' }}>Export FASTA</button>
          </div>
        </div>


        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '8px' }}>Sample Metadata</h2>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '16px' }}>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Collection Date</div>
                <div style={{ fontWeight: 500 }}>{activeSample?.collectionDate || '—'}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Depth</div>
                <div style={{ fontWeight: 500 }}>{activeSample?.depth || '—'}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Filter Type</div>
                <div style={{ fontWeight: 500 }}>{activeSample?.filterType || '—'}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Total Reads</div>
                <div style={{ fontWeight: 500 }}>{activeSample?.totalReads?.toLocaleString() || '—'}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Unique OTUs</div>
                <div style={{ fontWeight: 500 }}>{activeSample?.uniqueOTUs || '—'}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Shannon Index</div>
                <div style={{ fontWeight: 500 }}>{activeSample?.shannonIndex || '—'}</div>
              </div>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '24px', flex: 1, display: 'flex', flexDirection: 'column' }}>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 600, marginBottom: '16px' }}>Taxonomic Assignment</h2>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>
              Relative abundance of identified taxa within the eDNA sample matrix.
            </p>
            
            <div style={{ flex: 1, minHeight: '200px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={displayComposition}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {displayComposition.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: 'var(--bg-secondary)', borderColor: 'var(--glass-border)', borderRadius: '8px', color: '#fff' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <Legend verticalAlign="bottom" height={36} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Molecular;
