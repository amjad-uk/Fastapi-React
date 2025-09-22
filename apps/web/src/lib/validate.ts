export const MIN_DOB = '1915-01-01';
export function calcAge(isoDate:string): number{
  const d = new Date(isoDate);
  const t = new Date();
  let years = t.getFullYear() - d.getFullYear();
  const m = t.getMonth() - d.getMonth();
  if (m < 0 || (m === 0 && t.getDate() < d.getDate())) years--;
  return years;
}
export function validateUser(u:{firstname:string;lastname:string;date_of_birth:string}){
  const errs:Record<string,string> = {};
  const nameRe = /^[A-Za-z]{2,20}$/;
  if(!nameRe.test(u.firstname||'')) errs.firstname='2–20 letters, A–Z only';
  if(!nameRe.test(u.lastname||'')) errs.lastname='2–20 letters, A–Z only';
  if(!u.date_of_birth) errs.date_of_birth='Required';
  else{
    if(u.date_of_birth < MIN_DOB) errs.date_of_birth = 'On/after 1915-01-01';
    const today = new Date(); today.setHours(0,0,0,0);
    if(new Date(u.date_of_birth) > today) errs.date_of_birth = 'Cannot be in the future';
  }
  return errs;
}
