import json
import logging
import math
import sys
import time
from os import PathLike
from pathlib import Path
from typing import Any, Self

import serial
from prometheus_client import Gauge, start_http_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Outlet:
    def __init__(
        self,
        name,
        true_rms_current,
        peak_rms_current,
        true_rms_voltage,
        average_power,
        voltamps,
        outlet_state,
    ) -> None:
        self.name: str = name
        self.true_rms_current: float = true_rms_current
        self.peak_rms_current: float = peak_rms_current
        self.true_rms_voltage: float = true_rms_voltage
        self.average_power: int = average_power
        self.voltamps: int = voltamps
        self.outlet_state: bool = outlet_state

    def __repr__(self) -> str:
        repr = "|"
        keys = self.__dict__.keys()
        for k in keys:
            repr += f" {getattr(self, k)} |"
        return repr


class Config:
    def __init__(self, port, baud_rate, serial_path) -> None:
        self.port: int = port
        self.baud_rate: int = baud_rate
        self.serial_path: PathLike = serial_path

    @classmethod
    def parse_json(cls, config_file: PathLike) -> Self:
        # TODO: maybe add some config validation + type checking
        with open(config_file, "r") as cfg:
            raw_config = json.loads(cfg.read())

        return cls(
            port=raw_config["port"],
            baud_rate=raw_config["baudRate"],
            serial_path=raw_config["serialPath"],
        )


def exec_cmd(device: PathLike, baudRate: int, cmd: str) -> str:
    with serial.Serial(str(device), baudRate) as serial_connection:
        # execute our actual command
        serial_connection.write(cmd.encode() + b"\r")

        # wait for execution response
        time.sleep(5)

        out = serial_connection.read_all()
        if out:
            return out.decode("utf-8")
        else:
            # broke pipe might not be the most fitting error, but it indicates errors
            # reading or writing to files/devices, so it seemed appropriate enough
            raise BrokenPipeError


def mmp_parser(ostatus: str) -> list[Outlet]:
    outlets: list[Outlet] = []
    # throw away every line that doesn't contain data columns
    raw_rows = ostatus.splitlines()
    rows: list[list[str]] = []
    for row in raw_rows:
        # we throw away the first and last column, since they are just buffer
        rows.append(row.split("|")[1:-1])

    start = math.inf
    finish = None
    for idx in range(len(rows) - 1, 0, -1):
        if not finish and len(rows[idx]) == 7:
            finish = idx
            continue
        if len(rows[idx]) == 7:
            start = min(start, idx)
            continue

        # break if we don't have a continues block of input
        if finish:
            break

    if not finish or start == math.inf:
        logger.exception(f"unparsable ostatus input: \n```\n{ostatus}\n```")
        raise ValueError

    for raw_columns in rows[start : finish + 1]:
        # typing here is kinda ugly
        columns: Any = list(map(lambda x: x.strip(), raw_columns))

        for idx in range(1, 6):
            columns[idx] = columns[idx].split(" ")[0]

        # True RMS Current, Peak RMS Current, True RMS Voltage
        columns[1] = float(columns[1])
        columns[2] = float(columns[2])
        columns[3] = float(columns[3])

        # Average Power, Volt-Amps
        columns[4] = int(columns[4])
        columns[5] = int(columns[5])

        # outlet_state
        columns[6] = columns[6] == "On"
        outlets.append(Outlet(*columns))
    return outlets


def main() -> None:
    # gate against oob access
    if len(sys.argv) >= 2 and sys.argv[-2] == "--config":
        config_path = Path(sys.argv[-1])
        if not config_path.is_file():
            raise FileExistsError
        config = Config.parse_json(config_path)
        logger.info(f"read config from {config_path}")
    else:
        logger.warning("missing --config arg, using default config")
        config = Config(port=29001, baud_rate=9600, serial_path="/tmp/emu")

    metrics: dict[str, str] = {
        "true_rms_current": "True RMS Current (A)",
        "peak_rms_current": "Peak RMS Current (A)",
        "true_rms_voltage": "True RMS Voltage (V)",
        "average_power": "Average Power (W)",
        "voltamps": "Volt-Amps (VA)",
        "outlet_state": "Outlet State (Bool)",
    }
    gauges: dict[str, Gauge] = {
        name: Gauge(name, description, ["name"])
        for name, description in metrics.items()
    }

    server, thread = start_http_server(config.port)
    logger.info("prometheus exporter http-server started")

    while True:
        raw_serial_output = exec_cmd(config.serial_path, config.baud_rate, "ostatus")
        outlets = mmp_parser(raw_serial_output)
        logger.info(f"parsed {len(outlets)} outlets")

        for outlet in outlets:
            for metric in metrics:
                value = getattr(outlet, metric)
                gauges[metric].labels(outlet.name).set(value)

        time.sleep(1)


if __name__ == "__main__":
    main()
