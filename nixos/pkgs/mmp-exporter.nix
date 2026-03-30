{ lib
, python3Packages
}: python3Packages.buildPythonApplication {
  pname = "mmp-exporter";
  version = "0.1.0";

  disabled = python3Packages.pythonOlder "3.13";

  pyproject = true;

  src = ../../.;
  build-system = with python3Packages; [ hatchling ];
  propagatedBuildInputs = with python3Packages; [
    pyserial
    prometheus-client
  ];
  meta = {
    mainProgram = "mmp-exporter";
  };
}
