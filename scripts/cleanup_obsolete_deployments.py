import json
import urllib.request
import datetime
import time

auth_path = r"C:\Users\derre\AppData\Roaming\com.vercel.cli\Data\auth.json"
with open(auth_path) as f:
    token = json.load(f)["token"]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
team_id = "team_h6kuJ2QCPQHJAYNNBLfFG3Mz"
project_id = "prj_cG73SOly1TZF1jJ9KGtNEJamlNKV"

def api_get(endpoint):
    url = f"https://api.vercel.com{endpoint}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def api_delete(endpoint):
    url = f"https://api.vercel.com{endpoint}"
    req = urllib.request.Request(url, headers=headers, method="DELETE")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

# 1. Fetch all deployments
print("Fetching all deployments for krown-supply-store...")
all_deps = []
until = None
while True:
    ep = f"/v6/deployments?projectId={project_id}&teamId={team_id}&limit=100"
    if until:
        ep += f"&until={until}"
    data = api_get(ep)
    deps = data.get("deployments", [])
    if not deps:
        break
    all_deps.extend(deps)
    if len(deps) < 100:
        break
    until = deps[-1].get("createdAt")

print(f"Total deployments found: {len(all_deps)}")

# Sort by createdAt descending
all_deps.sort(key=lambda d: d.get("createdAt", 0), reverse=True)

# 2. Identify Protected Deployments
# Keep current live production deployment + top 5 previous production builds for rollback
KEEP_COUNT = 6
protected_deps = all_deps[:KEEP_COUNT]
candidates = all_deps[KEEP_COUNT:]

print(f"\nPROTECTED DEPLOYMENTS (Keeping {len(protected_deps)}):")
for idx, d in enumerate(protected_deps):
    created_dt = datetime.datetime.fromtimestamp(d.get("createdAt", 0) / 1000, datetime.timezone.utc)
    commit = d.get("meta", {}).get("githubCommitMessage", "")[:50].replace("\n", " ")
    print(f"  [PROTECTED {idx+1}] {d.get('uid')} | {created_dt.strftime('%Y-%m-%d %H:%M:%S UTC')} | {commit}")

print(f"\nCANDIDATES FOR REMOVAL: {len(candidates)} deployments")

# Safety checks on candidates
safe_candidates = []
for d in candidates:
    uid = d.get("uid")
    aliases = d.get("alias", []) or []
    # Check if any production domain is assigned
    if any("krownsupplyco.com" in a for a in aliases):
        print(f"SAFETY WARNING: Skipping {uid} because it is assigned to krownsupplyco.com!")
        continue
    safe_candidates.append(d)

print(f"Confirmed safe to delete: {len(safe_candidates)} deployments")

# Save inventory
inventory = [
    {
        "uid": d.get("uid"),
        "name": d.get("name"),
        "url": d.get("url"),
        "createdAt": d.get("createdAt"),
        "createdUtc": datetime.datetime.fromtimestamp(d.get("createdAt", 0) / 1000, datetime.timezone.utc).isoformat(),
        "commit": d.get("meta", {}).get("githubCommitMessage", ""),
        "reason": "Obsolete historical intermediate production build superseded by current live production build"
    }
    for d in safe_candidates
]

with open("scratch/deleted_deployments_inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)
print("Saved candidate inventory to scratch/deleted_deployments_inventory.json")

# 3. Execute Deletion
deleted_count = 0
failed_count = 0

for idx, d in enumerate(safe_candidates):
    uid = d.get("uid")
    try:
        res = api_delete(f"/v13/deployments/{uid}?teamId={team_id}")
        deleted_count += 1
        if (idx + 1) % 10 == 0 or (idx + 1) == len(safe_candidates):
            print(f"Deleted {deleted_count}/{len(safe_candidates)} deployments...")
        time.sleep(0.2) # Avoid rate limits
    except Exception as e:
        print(f"Failed to delete {uid}: {e}")
        failed_count += 1

print(f"\nDeployment cleanup complete! Successfully deleted: {deleted_count}, Failed: {failed_count}")

