import { useId } from 'react';

export default function Tooltip({text}:{text:string}){
  const id = useId();
  return (
    <span className="tip" aria-describedby={id} role="img" aria-label="Help">
      ⓘ
      <span id={id} role="tooltip" className="tip-bubble">{text}</span>
    </span>
  );
}
