import os
import sqlite3
import tempfile
import unittest
from fastapi.testclient import TestClient

class LicenseApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        os.environ['LICENSE_DB']=os.path.join(self.tmp.name,'test.db')
        os.environ['IANDI_ADMIN_TOKEN']='ci-test-admin-secret'
        import app
        app.DB=os.environ['LICENSE_DB']; app.ADMIN_TOKEN=os.environ['IANDI_ADMIN_TOKEN']
        self.client=TestClient(app.app); self.headers={'Authorization':app.ADMIN_TOKEN}
    def tearDown(self): self.tmp.cleanup()
    def test_issue_activate_validate_revoke(self):
        r=self.client.post('/v1/admin/licenses',json={'plan':'pro','days':30,'max_devices':1},headers=self.headers)
        self.assertEqual(r.status_code,200,r.text); key=r.json()['license_key']
        payload={'license_key':key,'device_id':'ci-device-001-abcdef'}
        self.assertEqual(self.client.post('/v1/license/activate',json=payload).status_code,200)
        self.assertTrue(self.client.post('/v1/license/validate',json=dict(payload,feature_id='B03')).json()['valid'])
        self.assertTrue(self.client.post('/v1/admin/licenses/revoke',json={'license_key':key},headers=self.headers).json()['revoked'])
        self.assertEqual(self.client.post('/v1/license/validate',json=dict(payload,feature_id='B03')).status_code,403)
    def test_device_limit_and_deactivate(self):
        key=self.client.post('/v1/admin/licenses',json={'max_devices':1},headers=self.headers).json()['license_key']
        a={'license_key':key,'device_id':'ci-device-001-abcdef'}
        b={'license_key':key,'device_id':'ci-device-002-abcdef'}
        self.assertEqual(self.client.post('/v1/license/activate',json=a).status_code,200)
        self.assertEqual(self.client.post('/v1/license/activate',json=b).status_code,409)
        self.client.post('/v1/license/deactivate',json=a)
        self.assertEqual(self.client.post('/v1/license/activate',json=b).status_code,200)
    def test_migrate_prototype_schema(self):
        c=sqlite3.connect(os.environ['LICENSE_DB'])
        c.execute('CREATE TABLE licenses(key_hash TEXT PRIMARY KEY,plan TEXT NOT NULL,expires_at TEXT,max_devices INTEGER NOT NULL DEFAULT 1,revoked INTEGER NOT NULL DEFAULT 0)')
        c.execute('CREATE TABLE activations(key_hash TEXT NOT NULL,device_id TEXT NOT NULL,activated_at TEXT NOT NULL,PRIMARY KEY(key_hash,device_id))')
        c.commit(); c.close()
        r=self.client.post('/v1/admin/licenses',json={'plan':'pro'},headers=self.headers)
        self.assertEqual(r.status_code,200,r.text)
        c=sqlite3.connect(os.environ['LICENSE_DB']); cols=[x[1] for x in c.execute('PRAGMA table_info(licenses)')]; c.close()
        self.assertIn('created_at',cols)

if __name__=='__main__': unittest.main()
