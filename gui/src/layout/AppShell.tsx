import type { FC, PropsWithChildren } from 'react';
import TopBar from './TopBar';
import SideNav from './SideNav';
import Breadcrumbs from './Breadcrumbs';

// TODO: Basic app layout with top bar, side nav, and content area
const AppShell: FC<PropsWithChildren> = ({ children }) => {
  return (
    <div className="app-shell">
      <TopBar />
      <div className="app-shell-body" style={{ display: 'flex' }}>
        <SideNav />
        <main className="app-shell-content" style={{ flex: 1 }}>
          <Breadcrumbs />
          {children ?? <div>ContentOutlet</div>}
        </main>
      </div>
    </div>
  );
};

export default AppShell;
