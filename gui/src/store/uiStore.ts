/* src/store/uiStore.ts */
// TODO: UI global state (theme, sidebar, etc.). Replace with Zustand/Context later.

export interface UIState {
  themeMode: 'light' | 'dark';
  sidebarOpen: boolean;
}

export const uiStore: UIState = {
  themeMode: 'light',
  sidebarOpen: true,
};

export function setThemeMode(_mode: UIState['themeMode']) {
  // TODO: implement with Zustand/Context
}

export function setSidebarOpen(_open: boolean) {
  // TODO: implement with Zustand/Context
}
