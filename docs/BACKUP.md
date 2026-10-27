# Private backup in Google Drive

Decided 26 Oct 2026 (author's offer). GitHub keeps run bundles for 90 days and Zenodo keeps only
the publishable part of each final release, so without this the provisional runs, the dry runs
and all private data (VulnCheck until it agrees in writing) would be lost. Drive also holds a
monthly copy of the whole repository in case the GitHub account is ever lost or locked.

## What is kept
| Folder inside Internet-Security-Snapshot-2027 | What | When | Size |
|---|---|---|---|
| `runs/` | Full bundle of every quarterly pull (provisional, final, dry runs), with checksums | After each pull | about 200 MB a pull |
| `repository/` | `git bundle` of every branch (code, schedule, run logs) | The 3rd of each month | a few MB |

About 3 GB for 2027 (`docs/CAPACITY.md`). The folder stays private: nothing in it is
published, and it holds data the standing rules keep private. Victim names are never in it
(ransomware.live is reduced to counts at collection).

## Setup (the author, about 20 minutes; schedule item `drive-backup-setup`)
Done on your own computer. The token goes only into GitHub secrets, never into chat, email or a
file in the repository.

1. Install rclone from https://rclone.org/downloads/ .
2. Run `rclone config` and create a remote named exactly `gdrive`: type `drive`; leave client
   id and secret blank; scope `drive` (option 1, full access: the narrower `drive.file` cannot
   see a folder you created yourself); **root_folder_id `1vcBEDbuFu9-KeCDxOH8vrwWHDdjbawvc`** (the
   author's folder "Internet-Security-Snapshot-2027", created 27 Oct; rclone then works only
   inside it); no service account; no advanced config; let it open the browser and sign in
   with pagagne@gmail.com; not a shared drive.
3. Test the sign-in: `rclone lsd gdrive:` should finish without an error (the folder is empty
   at first).
4. Run `rclone config file` to find the configuration file; open it and copy the whole
   `[gdrive]` section.
5. In GitHub: Settings > Secrets and variables > Actions > New repository secret, name
   `RCLONE_CONF`, paste the section, save. Keep rclone installed if you want to look at the backup
   from your computer.
6. Tell Claude; it runs the Backup workflow once by hand (a connection-test file in `tests/`
   and a repository copy in `repository/`) and checks in Drive that they arrived.

## Restoring
- A run: download its folder from `runs/` and check it with `sha256sum -c SHA256SUMS`.
- The repository: `git clone internet-security-snapshot-YYYY-MM-DD.bundle`.

## Notes
- If the token stops working (password change, access removed), the workflow fails and the
  run log shows it; repeat steps 2, 4 and 5.
- Drive space: free Google accounts share 15 GB between Drive, Gmail and Photos.
