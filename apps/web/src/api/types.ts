export class ApiError extends Error{status:number;body?:unknown;constructor(m:string,s:number,b?:unknown){super(m);this.status=s;this.body=b}}
