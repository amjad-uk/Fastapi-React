import { useEffect, useRef } from 'react';
export default function Modal({open,onClose,children,title}:{open:boolean;onClose:()=>void;children:React.ReactNode;title:string}){
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(()=>{
    const d = ref.current!;
    if(open && !d.open) d.showModal();
    if(!open && d.open) d.close();
  },[open]);
  return (
    <dialog ref={ref} className="modal" onClose={onClose}>
      <div className="modal-header">
        <strong>{title}</strong>
        <button className="btn secondary" onClick={onClose} aria-label="Close">Close</button>
      </div>
      <div className="modal-body">{children}</div>
    </dialog>
  );
}
