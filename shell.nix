{ pins ? import ./nixos/npins
, pkgs ? import pins.nixpkgs { }
, lib ? pkgs.lib
, git-hooks ? import pins."git-hooks.nix"
}:
let
  emulatorScript = pkgs.writeShellScriptBin "emulator" ''
    ${lib.getExe pkgs.socat} -dd pty,link=/tmp/emu,cr exec:'${lib.getExe pkgs.uv} run mmp-emulator',pty,stderr,sane,cr
  '';
in
pkgs.mkShellNoCC {
  shellHook = ''
    ${(git-hooks.run {
      src = ./.;
      hooks = {
        editorconfig-checker.enable = true;
        nixpkgs-fmt.enable = true;
        ruff.enable = true;
        ruff-format.enable = true;
        isort.enable = true;
      };
    }).shellHook}
  '';
  buildInputs = with pkgs; [
    emulatorScript
    uv
    ruff
    socat
    isort
  ];
}
