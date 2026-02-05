import React, { createContext, useCallback, useContext, useMemo, useState } from "react";

const FlashContext = createContext(null);

export function FlashProvider({ children }) {
  const [messages, setMessages] = useState([]); // { id, type: 'success'|'error', text }

  const addFlash = useCallback((type, text) => {
    const id = crypto.randomUUID();
    setMessages((prev) => [...prev, { id, type, text }]);

    // Auto-dismiss after 4s
    window.setTimeout(() => {
      setMessages((prev) => prev.filter((m) => m.id !== id));
    }, 4000);
  }, []);

  const clearAll = useCallback(() => setMessages([]), []);

  const value = useMemo(() => ({ messages, addFlash, clearAll }), [messages, addFlash, clearAll]);

  return <FlashContext.Provider value={value}>{children}</FlashContext.Provider>;
}

export function useFlash() {
  const ctx = useContext(FlashContext);
  if (!ctx) throw new Error("useFlash must be used within FlashProvider");
  return ctx;
}
