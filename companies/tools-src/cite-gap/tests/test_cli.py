import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV = dict(os.environ, PYTHONPATH=os.path.join(ROOT, "src"), PYTHONIOENCODING="utf-8")


def run(*args, stdin=None):
    return subprocess.run([sys.executable, "-m", "cite_gap", *args], input=stdin,
                          capture_output=True, text=True, encoding="utf-8", env=ENV)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, name, text):
        p = os.path.join(self.tmp.name, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        return p

    def test_exit_1_and_output_format(self):
        p = self.write("d.md", "# t\n\n国内の副業人口は2割に達した。\n")
        r = run(p)
        self.assertEqual(r.returncode, 1)
        self.assertIn(f"{p}:3  出典なし  「国内の副業人口は2割に達した。」  理由: 割合(2割)", r.stdout)

    def test_exit_0(self):
        p = self.write("ok.md", "売上は3倍になった（未確認）。\n")
        r = run(p)
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("出典なし  「", r.stdout)

    def test_json(self):
        p = self.write("d.md", "売上は3倍になった。\n")
        r = run("--json", p)
        self.assertEqual(r.returncode, 1)
        data = json.loads(r.stdout)
        self.assertEqual(data["summary"]["gaps"], 1)
        self.assertEqual(data["findings"][0]["line"], 1)
        self.assertEqual(data["findings"][0]["reasons"][0], {"kind": "倍率", "text": "3倍"})

    def test_strict_flag(self):
        p = self.write("d.md", "売上は50%増えた。\n出典: https://example.com/a\n")
        self.assertEqual(run(p).returncode, 0)
        self.assertEqual(run("--strict", p).returncode, 1)

    def test_stdin(self):
        r = run("-", stdin="必ず儲かる。\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("<stdin>:1", r.stdout)

    def test_missing_file_is_exit_2(self):
        r = run(os.path.join(self.tmp.name, "none.md"))
        self.assertEqual(r.returncode, 2)

    def test_help_and_version(self):
        r = run("--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("--strict", r.stdout)
        self.assertIn("0.1.0", run("--version").stdout)


class NoNetworkTests(unittest.TestCase):
    def test_no_network_modules_in_source(self):
        banned = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                  "ssl", "asyncio", "subprocess", "xmlrpc", "telnetlib")
        src = os.path.join(ROOT, "src", "cite_gap")
        for name in os.listdir(src):
            if not name.endswith(".py"):
                continue
            with open(os.path.join(src, name), encoding="utf-8") as f:
                for line in f:
                    s = line.strip()
                    if s.startswith(("import ", "from ")):
                        mod = s.split()[1].split(".")[0]
                        self.assertNotIn(mod, banned, f"{name}: {s}")


if __name__ == "__main__":
    unittest.main()
