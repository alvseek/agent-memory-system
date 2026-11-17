### § generate-uuid

Generate a unique identifier:
- **Windows**: `powershell -c "[guid]::NewGuid().ToString()"`
- **Linux/macOS**: `uuidgen` or `cat /proc/sys/kernel/random/uuid`

