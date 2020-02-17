# NoProcessLasso
Patches ProcessLasso to remove "nag" screen / splash screen

Place `patch.py` alongside `ProcessLasso.exe` or vice versa. After running `patch.py`, `ProcessLasso_patched.exe` will be generated, unless you pass `inline` as an option in which case `ProcessLasso.exe` will be renamed to `ProcessLasso_original.exe` and a patched version will be dropped to disk as `ProcessLasso.exe`.