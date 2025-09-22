import { createContext, useCallback, useContext, useMemo, useState } from 'react';

export type Toast = { id: string; kind?: 'info'|'success'|'warning'|'error'; message: string };
type Ctx = { push: (t: Omit<Toast,'id'>|string)=>void; success:(m:string)=>void; error:(m:string)=>void; warning:(m:string)=>void; info:(m:string)=>void };

const ToastCtx = createContext<Ctx | null>(null);
export function useToasts(){
  const ctx = useContext(ToastCtx);
  if(!ctx) throw new Error('useToasts must be used inside <Toaster />');
  return ctx;
}

export default function Toaster({children}:{children:React.ReactNode}){
  const [items, setItems] = useState<Toast[]>([]);

  const remove = useCallback((id:string)=> setItems(prev => prev.filter(t => t.id !== id)), []);
  const push = useCallback((t: Omit<Toast,'id'>|string)=> {
    const toast: Toast = typeof t === 'string' ? { id: crypto.randomUUID(), message: t } : { id: crypto.randomUUID(), ...t };
    setItems(prev => [...prev, toast]);
    setTimeout(()=> remove(toast.id), 3500);
  }, [remove]);

  const api = useMemo<Ctx>(() => ({
    push,
    success: (m:string)=> push({kind:'success', message:m}),
    error:   (m:string)=> push({kind:'error',   message:m}),
    warning: (m:string)=> push({kind:'warning', message:m}),
    info:    (m:string)=> push({kind:'info',    message:m})
  }), [push]);

  return (
    <ToastCtx.Provider value={api}>
      {children}
      <div className="toaster" aria-live="polite" aria-atomic="true">
        {items.map(t => (
          <div key={t.id} className={`toast ${t.kind||'info'}`} role="status">
            <span className="toast-icon">{icon(t.kind)}</span>
            <span>{t.message}</span>
            <button className="toast-close" onClick={()=>remove(t.id)} aria-label="Dismiss">×</button>
          </div>
        ))}
      </div>
    </ToastCtx.Provider>
  );
}

function icon(kind: Toast['kind']){
  switch(kind){
    case 'success': return '✔';
    case 'warning': return '⚠';
    case 'error':   return '✖';
    default:        return 'ℹ';
  }
}
