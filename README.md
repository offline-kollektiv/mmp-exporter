# MMP - Modular Metered Power - prometheus exporter and emulator

If you are using nixos, you can add the `overlay.nix` and `module.nix` from the `./nixos` directory.
Otherwise feel free to build the package using `uv` and deploy it however you see fit.

example-config.json:
```json
{
  "port": 8000,
  "baudRate": 9600,
  "serialPath": "/dev/USBtty01"
}
```

```bash
uv run mmp-exporter --config example-config.json
```
