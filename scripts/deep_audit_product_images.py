import os
import re

# Gather all text from src, scripts, and root
all_code_text = ""
for folder in ["src", "scripts"]:
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", errors="ignore") as fl:
                        all_code_text += fl.read() + "\n"
                except:
                    pass

prod_dir = "public/images/products"
all_prod_files = [f for f in os.listdir(prod_dir) if os.path.isfile(os.path.join(prod_dir, f))]

definitely_used = []
uncertain_or_unused = []

for f in all_prod_files:
    fp = os.path.join(prod_dir, f)
    sz = os.path.getsize(fp)
    # Check if exact filename appears in code
    if f in all_code_text:
        definitely_used.append((f, sz, "Direct text match in codebase"))
        continue
    
    # Check if stem appears
    stem = os.path.splitext(f)[0]
    if len(stem) > 8 and stem in all_code_text:
        definitely_used.append((f, sz, f"Stem '{stem}' found in codebase"))
        continue
        
    uncertain_or_unused.append((f, sz))

print(f"Total product files: {len(all_prod_files)}")
print(f"Definitely used: {len(definitely_used)} ({sum(s for _, s, _ in definitely_used) / 1024 / 1024:.2f} MB)")
print(f"Uncertain / unreferenced in code: {len(uncertain_or_unused)} ({sum(s for _, s in uncertain_or_unused) / 1024 / 1024:.2f} MB)")

