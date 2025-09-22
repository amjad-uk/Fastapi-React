export type User = { id:number; guid:string; firstname:string; lastname:string; date_of_birth:string; created_at:string; updated_at:string; age:number };
import {http} from './http';
export const listUsers = ()=> http<User[]>('/users');
export const createUser = (u: {firstname:string; lastname:string; date_of_birth:string})=> http<User>('/users/create', { method:'POST', body: JSON.stringify(u) });
export const updateUser = (id:number, patch: Partial<Omit<User,'id'|'guid'|'created_at'|'updated_at'|'age'>>)=> http<User>(`/user/${id}`, { method:'PUT', body: JSON.stringify(patch) });
export const deleteUser = (id:number)=> http<void>(`/user?id=${id}`, { method:'DELETE' });
