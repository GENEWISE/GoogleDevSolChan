import re

def parse_vcf(content):
    variants = []
    for line in content.split("\n"):
        if line.startswith("#") or not line.strip():
            continue  
        cols = line.split("\t")
        if len(cols) < 8:
            continue  
        variant = {
            "chromosome": cols[0],
            "position": int(cols[1]),
            "id": cols[2] if cols[2] != "." else None,
            "reference": cols[3],
            "alt": cols[4],
            "quality": float(cols[5]) if cols[5] != "." else None,
            "filter": cols[6],
            "info": cols[7],
        }
        variants.append(variant)

    return variants