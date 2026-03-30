{ pkgs, lib, ... }:
let
  nixos-lib = import (pkgs.path + "/nixos/lib") { };
  serialPath = "/tmp/emu";
  port = 8000;
in
(nixos-lib.runTest {
  hostPkgs = pkgs;
  defaults.documentation.enable = lib.mkDefault false;
  imports = [
    {
      name = "mmp-parser-integration";
      nodes.node = {
        imports = [ ./module.nix ];
        nixpkgs.overlays = [ (import ./overlay.nix) ];
        environment.systemPackages = with pkgs; [ curl ];
        services.mmp.exporters."pdu01" = {
          enable = true;
          settings = {
            inherit port serialPath;
            baudRate = 9600;
          };
          emulator.enable = true;
        };
      };
      testScript = ''
        start_all()
        node.wait_for_unit("mmp-emulator-pdu01")
        node.wait_for_unit("mmp-exporter-pdu01")
        node.wait_for_open_port(${builtins.toString port})
        node.wait_until_succeeds("[[ $(curl http://localhost:${builtins.toString port}/ | grep 'MOD 1 Outlet 1' | wc -l) -eq 6 ]]")
        node.wait_until_succeeds("[[ $(curl http://localhost:${builtins.toString port}/ | grep 'MOD 4 Outlet 5' | wc -l) -eq 6 ]]")
      '';
    }
  ];
}).config.result
