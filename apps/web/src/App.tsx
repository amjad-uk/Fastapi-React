import {useEffect, useState} from 'react';
import {listUsers, createUser, updateUser, deleteUser, User} from './api/users';
import Modal from './components/Modal';
import UserForm, { Values } from './components/UserForm';
import Toaster, { useToasts } from './components/Toaster';

function AppInner(){
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string|null>(null);
  const [showAdd, setShowAdd] = useState(false);
  const [editUser, setEditUser] = useState<User|null>(null);
  const { error, success } = useToasts();

  async function refresh(){
    try{ setLoading(true); setUsers(await listUsers()); setErr(null); }
    catch(e:any){ setErr(e?.message || 'Failed to load'); error(e?.message || 'Failed to load'); }
    finally{ setLoading(false); }
  }
  useEffect(()=>{ refresh() },[]);

  function emitServerValidation(body:any){
    const details = body?.detail;
    if(Array.isArray(details)){
      for(const d of details){
        const loc = (d?.loc || []).slice(-1)[0];
        const field = typeof loc === 'string' ? loc : 'field';
        const msg = d?.msg || 'validation error';
        error(`${field}: ${msg}`);
      }
      return true;
    }
    return false;
  }

  async function onAdd(v:Values){
    try{
      await createUser({ firstname: v.firstname, lastname: v.lastname, date_of_birth: v.date_of_birth });
      setShowAdd(false);
      await refresh();
      success('Created');
    }catch(e:any){
      if(!emitServerValidation(e?.body)) error(e?.message || 'Create failed');
      throw e;
    }
  }
  async function onEdit(v:Values){
    if(!editUser) return;
    try{
      await updateUser(editUser.id, { firstname: v.firstname, lastname: v.lastname, date_of_birth: v.date_of_birth });
      setEditUser(null);
      await refresh();
      success('Updated');
    }catch(e:any){
      if(!emitServerValidation(e?.body)) error(e?.message || 'Update failed');
      throw e;
    }
  }
  async function onDelete(id:number){
    if(!confirm('Delete this user?')) return;
    try{
      await deleteUser(id);
      success('Deleted');
      await refresh();
    }catch(e:any){
      error(e?.message || 'Delete failed');
    }
  }

  return (
    <div className="container">
      <header className="header">
        <div>
          <div className="title">Users</div>
          <div className="muted">Add, edit, and delete records</div>
        </div>
        <button className="btn" onClick={()=>setShowAdd(true)}>+ Add user</button>
      </header>

      {loading && <p className="muted">Loading...</p>}
      {err && <p className="error" role="alert">{err}</p>}

      {!loading && users.length===0 && <p className="muted">No users yet. Click “Add user”.</p>}

      {!loading && users.length>0 && (
        <table className="table" aria-label="Users table">
          <thead>
            <tr>
              <th>UserId</th>
              <th>Name</th>
              <th>Date of Birth</th>
              <th>Age</th>
              <th className="sr-only">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id}>
                <td className="td"><code style={{fontSize:12}}>{u.guid}</code></td>
                <td className="td">{u.firstname} {u.lastname}</td>
                <td className="td">{u.date_of_birth}</td>
                <td className="td"><span className="chip">{u.age} yrs</span></td>
                <td className="td">
                  <div className="row" style={{gap:8}}>
                    <button className="btn secondary" onClick={()=>setEditUser(u)}>Edit</button>
                    <button className="btn danger" onClick={()=>onDelete(u.id)}>Delete</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {showAdd && (
        <Modal open={showAdd} onClose={()=>setShowAdd(false)} title="Add user">
          <UserForm onSubmit={onAdd} submitLabel="Create" />
        </Modal>
      )}

      {editUser && (
        <Modal open={!!editUser} onClose={()=>setEditUser(null)} title={`Edit #${editUser.id}`}>
          <UserForm
            key={editUser.id}
            initial={{firstname:editUser.firstname, lastname:editUser.lastname, date_of_birth:editUser.date_of_birth}}
            onSubmit={onEdit}
            submitLabel="Save changes"
          />
        </Modal>
      )}
    </div>
  );
}

export default function App(){
  return (
    <Toaster>
      <AppInner />
    </Toaster>
  );
}
