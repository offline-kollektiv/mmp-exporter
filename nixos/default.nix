{ pins ? import ./npins
, pkgs ? import pins.nixpkgs {
    overlays = [
      (import ./overlay.nix)
    ];
  }
, lib ? pkgs.lib
}: {
  inherit (pkgs) mmp-exporter;
  vmTest = import ./vm_test.nix { inherit pkgs lib; };
}
