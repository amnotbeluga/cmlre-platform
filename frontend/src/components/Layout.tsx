import { ReactNode, FC } from 'react';
import { Link, useLocation } from 'react-router-dom';

interface LayoutProps {
  children: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: '📊' },
    { name: 'Oceanographic', path: '/oceanographic', icon: '🌊' },
    { name: 'Fisheries', path: '/fisheries', icon: '🐟' },
    { name: 'Taxonomy', path: '/taxonomy', icon: '🦑' },
    { name: 'Molecular / eDNA', path: '/molecular', icon: '🧬' },
    { name: 'Analytics', path: '/analytics', icon: '📈' },
  ];

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>

      <aside 
        className="glass-panel" 
        style={{ 
          width: 'var(--sidebar-width)', 
          margin: '16px', 
          display: 'flex', 
          flexDirection: 'column',
          position: 'fixed',
          top: 0,
          bottom: 0,
          left: 0,
          zIndex: 10
        }}
      >
        <div style={{ padding: '32px 24px', borderBottom: '1px solid var(--glass-border)' }}>
          <h1 style={{ fontSize: '1.2rem', fontWeight: 800, background: 'linear-gradient(90deg, var(--accent-primary), var(--text-accent))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            CMLRE Platform
          </h1>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>Marine Data Unified</p>
        </div>

        <nav style={{ padding: '24px 12px', display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.name}
                to={item.path}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  padding: '12px 16px',
                  borderRadius: '12px',
                  color: isActive ? '#fff' : 'var(--text-secondary)',
                  background: isActive ? 'var(--accent-glow)' : 'transparent',
                  fontWeight: isActive ? 600 : 400,
                  transition: 'all 0.2s',
                  border: isActive ? '1px solid rgba(14, 165, 233, 0.3)' : '1px solid transparent'
                }}
              >
                <span style={{ fontSize: '1.2rem' }}>{item.icon}</span>
                {item.name}
              </Link>
            );
          })}
        </nav>
        
        <div style={{ padding: '24px', borderTop: '1px solid var(--glass-border)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
              A
            </div>
            <div>
              <div style={{ fontSize: '0.9rem', fontWeight: 600 }}>Admin User</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>admin@cmlre.gov.in</div>
            </div>
          </div>
        </div>
      </aside>


      <main style={{ flex: 1, marginLeft: 'calc(var(--sidebar-width) + 32px)', padding: '32px' }}>
        <div className="animate-fade-in" style={{ maxWidth: '1400px', margin: '0 auto' }}>
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
