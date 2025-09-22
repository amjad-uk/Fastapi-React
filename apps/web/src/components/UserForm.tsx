import {useMemo, useState} from 'react';
import {validateUser, calcAge, MIN_DOB} from '../lib/validate';
import Tooltip from './Tooltip';
import { useToasts } from './Toaster';

export type Values = {firstname:string;lastname:string;date_of_birth:string};
const LABELS: Record<keyof Values, string> = { firstname:'First name', lastname:'Last name', date_of_birth:'Date of Birth' };

export default function UserForm({initial,onSubmit,submitLabel='Save'}:{initial?:Partial<Values>;onSubmit:(v:Values)=>Promise<void>;submitLabel?:string}){
  const [v,setV] = useState<Values>({
    firstname: initial?.firstname || '',
    lastname: initial?.lastname || '',
    date_of_birth: initial?.date_of_birth || '',
  });
  const [errs,setErrs] = useState<Record<string,string>>({});
  const [busy,setBusy] = useState(false);
  const { error, success } = useToasts();
  const computedAge = useMemo(()=> v.date_of_birth ? calcAge(v.date_of_birth) : '', [v.date_of_birth]);

  function onChange<K extends keyof Values>(k:K){
    return (e:any)=>{
      const next = {...v, [k]: e.target.value};
      setV(next);
      const ve = validateUser(next);
      setErrs(ve);
    };
  }

  async function submit(e:React.FormEvent){
    e.preventDefault();
    const ve = validateUser(v);
    setErrs(ve);
    const keys = Object.keys(ve);
    if(keys.length>0){
      keys.forEach(k => error(`${LABELS[k as keyof Values]}: ${ve[k]}`));
      return;
    }
    setBusy(true);
    try{
      await onSubmit(v);
      success('Saved');
    }catch(err:any){
      error(err?.message || 'Request failed');
    }finally{
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="grid" aria-busy={busy}>
      <div className="row">
        <label className="field" style={{flex:'1 1 220px'}}>
          <span>First name <Tooltip text="2–20 letters, A–Z only" /></span>
          <input className={"input"+(errs.firstname?' invalid':'')} value={v.firstname} onChange={onChange('firstname')} required placeholder="Alan" />
        </label>
        <label className="field" style={{flex:'1 1 220px'}}>
          <span>Last name <Tooltip text="2–20 letters, A–Z only" /></span>
          <input className={"input"+(errs.lastname?' invalid':'')} value={v.lastname} onChange={onChange('lastname')} required placeholder="Turing" />
        </label>
      </div>
      <div className="row">
        <label className="field" style={{flex:'1 1 220px'}}>
          <span>Date of Birth <Tooltip text={`On/after ${MIN_DOB}, not in the future`} /></span>
          <input className={"input"+(errs.date_of_birth?' invalid':'')} type="date" min={MIN_DOB} value={v.date_of_birth} onChange={onChange('date_of_birth')} required />
        </label>
        <div className="field" style={{flex:'1 1 220px'}}>
          <span>Age <Tooltip text="Auto-computed from DOB" /></span>
          <div className="input" aria-readonly>
            {computedAge !== '' ? `${computedAge} yrs` : '—'}
          </div>
        </div>
      </div>
      <div className="modal-footer" style={{padding:0, borderTop:'none'}}>
        <button className="btn" type="submit" disabled={busy}>{submitLabel}</button>
      </div>
    </form>
  );
}
