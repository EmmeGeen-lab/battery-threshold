import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "src" / "battery_threshold.py"
SPEC = importlib.util.spec_from_file_location("battery_threshold", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class DetectionTests(unittest.TestCase):
    def test_detects_bat1_threshold(self):
        with tempfile.TemporaryDirectory() as temp:
            node = Path(temp) / "BAT1" / "charge_control_end_threshold"
            node.parent.mkdir()
            node.write_text("70\n", encoding="utf-8")
            old = os.environ.get("BATTERY_THRESHOLD_SYSFS_ROOT")
            os.environ["BATTERY_THRESHOLD_SYSFS_ROOT"] = temp
            try:
                value, detail = MODULE.read_threshold()
            finally:
                if old is None:
                    os.environ.pop("BATTERY_THRESHOLD_SYSFS_ROOT", None)
                else:
                    os.environ["BATTERY_THRESHOLD_SYSFS_ROOT"] = old
            self.assertEqual(value, 70)
            self.assertIn("BAT1", detail)

    def test_missing_node_is_unsupported(self):
        with tempfile.TemporaryDirectory() as temp:
            old = os.environ.get("BATTERY_THRESHOLD_SYSFS_ROOT")
            os.environ["BATTERY_THRESHOLD_SYSFS_ROOT"] = temp
            try:
                value, _ = MODULE.read_threshold()
            finally:
                if old is None:
                    os.environ.pop("BATTERY_THRESHOLD_SYSFS_ROOT", None)
                else:
                    os.environ["BATTERY_THRESHOLD_SYSFS_ROOT"] = old
            self.assertIsNone(value)


if __name__ == "__main__":
    unittest.main()
