import { useState, useEffect } from 'react';
import { api } from '../api/client';

const Taxonomy = () => {
  const [taxonomyData, setTaxonomyData] = useState<any[]>([]);

  useEffect(() => {
    const fetchSpecies = async () => {
      try {
        const response = await api.getSpecies();
        if (Array.isArray(response.data)) {
          setTaxonomyData(response.data);
        } else {
          console.error("Backend error:", response.data);
          setTaxonomyData([]);
        }
      } catch (err) {
        console.error("Failed to fetch species", err);
        setTaxonomyData([]);
      }
    };
    fetchSpecies();
  }, []);

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      <header>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '8px' }}>Biological Taxonomy & Specimens</h1>
        <p style={{ color: 'var(--text-secondary)' }}>High-resolution reference imagery and verified taxonomic classifications.</p>
      </header>

      <div style={{ display: 'flex', gap: '16px', marginBottom: '8px' }}>
        <button style={{ padding: '8px 16px', background: 'var(--accent-primary)', color: '#fff', border: 'none', borderRadius: '20px', fontWeight: 600 }}>All Specimens</button>
        <button style={{ padding: '8px 16px', background: 'transparent', color: 'var(--text-secondary)', border: '1px solid var(--glass-border)', borderRadius: '20px' }}>Cnidaria</button>
        <button style={{ padding: '8px 16px', background: 'transparent', color: 'var(--text-secondary)', border: '1px solid var(--glass-border)', borderRadius: '20px' }}>Phytoplankton</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px' }}>
        
        {taxonomyData.map(item => (
          <div key={item.id} className="glass-panel" style={{ overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
            <div style={{ height: '240px', width: '100%', position: 'relative' }}>
              <img 
                src={item.imageUrl} 
                alt={item.commonName} 
                style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
              />
              <div style={{ position: 'absolute', top: '12px', right: '12px', background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)', padding: '4px 10px', borderRadius: '12px', fontSize: '0.8rem', fontWeight: 600, color: item.status === 'Endangered' ? '#ef4444' : '#10b981' }}>
                {item.status}
              </div>
            </div>
            
            <div style={{ padding: '20px', flex: 1, display: 'flex', flexDirection: 'column' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', letterSpacing: '1px', textTransform: 'uppercase', marginBottom: '4px' }}>
                {item.phylum} &gt; {item.class}
              </div>
              <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '2px', color: 'var(--text-primary)' }}>{item.commonName}</h2>
              <div style={{ fontSize: '1rem', fontStyle: 'italic', color: 'var(--accent-primary)', marginBottom: '16px' }}>{item.species}</div>
              
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '24px' }}>
                {item.description}
              </p>

              <div style={{ marginTop: 'auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>ID: {item.id}</span>
                <button style={{ background: 'transparent', border: 'none', color: 'var(--text-accent)', fontWeight: 600, cursor: 'pointer' }}>View Details →</button>
              </div>
            </div>
          </div>
        ))}

      </div>
    </div>
  );
};

export default Taxonomy;
