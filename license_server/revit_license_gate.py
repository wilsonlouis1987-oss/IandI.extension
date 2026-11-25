# I&I BIM Tools — Pro access helper
# Python 3 / pyRevit integration module. Not yet wired into the Dynamo .dyn graphs.
import hashlib
import json
import os
import platform
import urllib.request
import urllib.error

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "tool_access.json")
API_BASE = os.environ.get("IANDI_LICENSE_API", "").rstrip("/")
LICENSE_FILE = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "IandI BIM Tools", "license.json")

def _config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def is_free(tool_id):
    return tool_id in set(_config().get("free_tool_ids", []))

def device_id():
    # Stable app-scoped identifier; never use a user's email or Windows account name.
    raw = platform.node() + "|" + platform.machine() + "|" + os.environ.get("PROCESSOR_IDENTIFIER", "")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]

def stored_key():
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("license_key", "")
    except Exception:
        return ""

def check_pro(tool_id, license_key=None):
    """Return (allowed, message). Free tools always pass. Pro requires online validation."""
    if is_free(tool_id):
        return True, "Free tool"
    key = license_key or stored_key()
    if not key:
        return False, "This is a Pro tool. Activate your I&I BIM Tools Pro license."
    if not API_BASE.startswith("https://"):
        return False, "License service is not configured. Please try again later."
    payload = json.dumps({
        "license_key": key,
        "device_id": device_id(),
        "feature_id": tool_id
    }).encode("utf-8")
    req = urllib.request.Request(
        API_BASE + "/v1/license/validate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
        return bool(data.get("valid")), "Pro license verified" if data.get("valid") else "Pro license invalid"
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return False, "Pro license invalid, expired, or not activated on this device."
        return False, "License check failed. Internet connection required."
    except Exception:
        return False, "Could not reach the license server. Internet connection required."
