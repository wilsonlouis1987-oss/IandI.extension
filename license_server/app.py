import os, secrets, sqlite3, hashlib
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field

DB=os.getenv('LICENSE_DB','licenses.db'); ADMIN_TOKEN=os.getenv('IANDI_ADMIN_TOKEN','')
app=FastAPI(title='I&I BIM Tools License API',version='1.0.0')
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
 c.execute('CREATE TABLE IF NOT EXISTS licenses(key_hash TEXT PRIMARY KEY, plan TEXT NOT NULL, expires_at TEXT, max_devices INTEGER NOT NULL DEFAULT 1, revoked INTEGER NOT NULL DEFAULT 0)')
 c.execute('CREATE TABLE IF NOT EXISTS activations(key_hash TEXT NOT NULL, device_id TEXT NOT NULL, activated_at TEXT NOT NULL, PRIMARY KEY(key_hash,device_id))'); return c
def digest(k): return hashlib.sha256(k.encode()).hexdigest()
def now(): return datetime.now(timezone.utc)
def admin(auth):
 if not ADMIN_TOKEN or not auth or not secrets.compare_digest(auth,ADMIN_TOKEN): raise HTTPException(401,'Admin authentication required')
class Activate(BaseModel): license_key:str=Field(min_length=8,max_length=128); device_id:str=Field(min_length=8,max_length=128)
class Validate(Activate): feature_id:str=Field(min_length=1,max_length=100)
class CreateLicense(BaseModel): plan:str='pro'; days:int|None=Field(default=365,ge=1,le=3650); max_devices:int=Field(default=1,ge=1,le=20)
@app.get('/health')
def health(): return {'ok':True,'service':'I&I BIM Tools License API'}
@app.post('/v1/license/activate')
def activate(b:Activate):
 h=digest(b.license_key); c=db(); r=c.execute('SELECT * FROM licenses WHERE key_hash=?',(h,)).fetchone()
 if not r or r['revoked']: c.close(); raise HTTPException(403,'License invalid or revoked')
 if r['expires_at'] and datetime.fromisoformat(r['expires_at'])<=now(): c.close(); raise HTTPException(403,'License expired')
 n=c.execute('SELECT COUNT(*) FROM activations WHERE key_hash=?',(h,)).fetchone()[0]; exists=c.execute('SELECT 1 FROM activations WHERE key_hash=? AND device_id=?',(h,b.device_id)).fetchone()
 if not exists and n>=r['max_devices']: c.close(); raise HTTPException(409,'Device activation limit reached')
 c.execute('INSERT OR IGNORE INTO activations VALUES(?,?,?)',(h,b.device_id,now().isoformat())); c.commit(); c.close(); return {'active':True,'plan':r['plan'],'expires_at':r['expires_at']}
@app.post('/v1/license/validate')
def validate(b:Validate):
 h=digest(b.license_key); c=db(); r=c.execute('SELECT * FROM licenses WHERE key_hash=?',(h,)).fetchone(); active=c.execute('SELECT 1 FROM activations WHERE key_hash=? AND device_id=?',(h,b.device_id)).fetchone(); c.close()
 if not r or r['revoked'] or not active: raise HTTPException(403,'License not active on this device')
 if r['expires_at'] and datetime.fromisoformat(r['expires_at'])<=now(): raise HTTPException(403,'License expired')
 if r['plan']!='pro': raise HTTPException(403,'Pro license required')
 return {'valid':True,'feature_id':b.feature_id,'expires_at':r['expires_at']}
@app.post('/v1/license/deactivate')
def deactivate(b:Activate):
 c=db(); c.execute('DELETE FROM activations WHERE key_hash=? AND device_id=?',(digest(b.license_key),b.device_id)); c.commit(); c.close(); return {'deactivated':True}
@app.post('/v1/admin/licenses')
def create_license(b:CreateLicense,authorization:str|None=Header(default=None)):
 admin(authorization); key='IIBIM-'+secrets.token_urlsafe(24); expiry=(now()+timedelta(days=b.days)).isoformat() if b.days else None
 c=db(); c.execute('INSERT INTO licenses(key_hash,plan,expires_at,max_devices) VALUES(?,?,?,?)',(digest(key),b.plan,expiry,b.max_devices)); c.commit(); c.close(); return {'license_key':key,'plan':b.plan,'expires_at':expiry,'max_devices':b.max_devices}
@app.post('/v1/admin/licenses/revoke')
def revoke(license_key:str,authorization:str|None=Header(default=None)):
 admin(authorization); c=db(); c.execute('UPDATE licenses SET revoked=1 WHERE key_hash=?',(digest(license_key),)); c.commit(); c.close(); return {'revoked':True}
