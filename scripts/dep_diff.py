"""Dep diff helper: compares pyproject.toml deps between two releases."""

import json
import re
import sys
import urllib.request


def parse_deps(url):
    try:
        resp = urllib.request.urlopen(url, timeout=15)
        text = resp.read().decode()
        m = re.search(r"dependencies\s*=\s*\[(.*?)\]", text, re.DOTALL)
        if not m:
            return set()
        return set(re.findall(r'"([^"]+)"', m.group(1)))
    except Exception:
        return set()


def main():
    pkg, d, cur, latest, entries = sys.argv[1:6]
    url_old, url_new = sys.argv[6], sys.argv[7]

    old_deps = parse_deps(url_old)
    new_deps = parse_deps(url_new)
    added = sorted(new_deps - old_deps)
    removed = sorted(old_deps - new_deps)

    entry = {"pkg": pkg, "dir": d, "current": cur, "latest": latest}
    if added:
        entry["deps_added"] = "\n".join(added)
    if removed:
        entry["deps_removed"] = "\n".join(removed)

    u = json.loads(entries)
    u.append(entry)
    print(json.dumps(u))


if __name__ == "__main__":
    main()
