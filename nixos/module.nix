{ lib
, config
, pkgs
, ...
}:
let
  cfg = config.services.mmp;
  inherit (lib) mkOption mkEnableOption mkPackageOption mapAttrs' filterAttrs optional;
  inherit (lib.types) submodule attrsOf path int;
  emulatorUnitName = name: "mmp-emulator-${name}";
  mkEmulatorUnit = name: conf: {
    name = emulatorUnitName name;
    value = {
      description = "MMP Emulator Service";
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {
        # We have to use cr to convert \r to \n, since the MMP devices expect carriage return, but python input doesn't have an option to handle that.
        # This makes the test a bit more flaky, but hey that only emulates the actual thing even further, and *shouldn't* be a problem due to the retry limits :)
        ExecStart = "${lib.getExe conf.emulator.socatPackage} -dd pty,link=${conf.settings.serialPath},cr exec:'${conf.package}/bin/mmp-emulator',pty,stderr,sane,cr";
        Restart = "on-failure";
        RestartSec = 15;
        StartLimitIntervalSec = 45;
      };
    };
  };
  mkExporterUnit = name: conf: {
    name = "mmp-exporter-${name}";
    value = {
      description = "MMP Exporter Service";
      wantedBy = [ "multi-user.target" ];
      wants = [ "network.target" ];
      after = [ "network.target" ] ++ optional conf.emulator.enable ((emulatorUnitName name) + ".service");
      serviceConfig = {
        ExecStart = "${lib.getExe conf.package} --config ${pkgs.writeText "config.json" (builtins.toJSON conf.settings)}";
        Restart = "on-failure";
        RestartSec = 15;
        StartLimitIntervalSec = 600;
      };
    };
  };
in
{
  options.services.mmp = {
    exporters = mkOption {
      default = { };
      type = attrsOf (submodule ({ name, ... }: {
        options = {
          enable = mkEnableOption "mmp-exporter";
          package = mkPackageOption pkgs "mmp-exporter" { };
          settings = {
            port = mkOption {
              type = int;
              default = 8000;
            };
            baudRate = mkOption {
              type = int;
              default = 9600;
            };
            serialPath = mkOption {
              type = path;
              default = "/tmp/emu-mmp-${name}";
            };
          };
          emulator = mkOption {
            default = { };
            type = submodule ({ name, ... }: {
              options = {
                enable = mkEnableOption "mmp-emulator";
                socatPackage = mkPackageOption pkgs "socat" { };
              };
            });
          };
        };
      }));
    };
  };
  config =
    let
      exporters = mapAttrs' mkExporterUnit (filterAttrs (_: conf: conf.enable) cfg.exporters);
      emulators = mapAttrs' mkEmulatorUnit (filterAttrs (_: conf: conf.enable && conf.emulator.enable) cfg.exporters);
    in
    {
      systemd.services = emulators // exporters;
    };
}
