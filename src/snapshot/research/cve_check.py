"""Research task wrapper: the CVE-existence check (snapshot.cvecheck), run on GitHub."""
from ..cvecheck import main

if __name__ == "__main__":
    raise SystemExit(main())
