from __future__ import annotations
import re
from typing import Tuple
from dataclasses import dataclass


class Map:
    def __init__(self):
        self._beacons = []


class Sensor:
    def __init__(self, coords: Tuple[int, int], closest_beacon: Beacon):
        self._coords = coords
        self._closest_beacon = closest_beacon
        self._dist_to_beacon = None

    def get_dist_to_beacon(self):
        if self._dist_to_beacon is None:
            self._dist_to_beacon = self._compute_dist_to_beacon()
        return self._dist_to_beacon

    def _compute_dist_to_beacon(self):
        dist_x = abs(self._coords[1] - self._closest_beacon.coords[1])
        dist_y = abs(self._coords[0] - self._closest_beacon.coords[0])
        return dist_x + dist_y

    def compute_min_dist_to_row(self, row_no):
        return abs(self._coords[1] - row_no)

    def compute_positions_covered_in_row(self, row_no):
        dist_to_row = self.compute_min_dist_to_row(row_no)
        dist_to_beacon = self.get_dist_to_beacon()
        # print(f"{dist_to_row=}")
        # print(f"{dist_to_beacon=}")
        if dist_to_beacon < dist_to_row:
            # print()
            return []
        x_range = (
            self._coords[0] - (self.get_dist_to_beacon() - dist_to_row),
            self._coords[0] + (self.get_dist_to_beacon() - dist_to_row),
        )
        positions_covered = list(range(*sorted(x_range)))
        # print(positions_covered)
        # print()
        return positions_covered

    def get_closest_beacon(self) -> Beacon:
        return self._closest_beacon


@dataclass
class Beacon:
    coords: Tuple[int, int]


def parse_row(row):
    matches = re.findall(r"[x|y]=-?\d+", row)
    coords = [int(coord.split("=")[1]) for coord in matches]
    sensor_coords = tuple(coords[:2])
    beacon_coords = tuple(coords[-2:])
    return sensor_coords, beacon_coords


def part1():
    sensors = []
    positions_without_distress_beacon = set()
    with open("input.txt") as f:
        for row in f:
            row = row.strip()
            sensor_coords, beacon_coords = parse_row(row)
            beacon = Beacon(beacon_coords)
            sensor = Sensor(coords=sensor_coords, closest_beacon=beacon)
            sensors.append(sensor)
            positions_without_distress_beacon.update(
                sensor.compute_positions_covered_in_row(2_000_000)
            )
    return len(positions_without_distress_beacon)


def part2():
    ...


if __name__ == "__main__":
    print(part1())
    print(part2())
