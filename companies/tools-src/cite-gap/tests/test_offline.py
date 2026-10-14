"""外部通信をしないことの検証。

1) ソースを AST で解析し、ネットワーク系 import が無いこと。
2) ネットワーク呼び出しをパッチして失敗させた状態で、既存の全テスト
   （このファイル自身を除く）が通ること。
   注意: test_cli.py が起こす別プロセス（python -m cite_gap）にはパッチは届かない。
   その部分は 1) の静的検査で担保する。
"""
import ast
import contextlib
import os
import unittest

from . import offline_guard

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src", "cite_gap")
BANNED = {"socket", "urllib", "http", "requests", "ssl", "ftplib", "smtplib"}


def _imported_roots(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                yield node.lineno, a.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.lineno, node.module.split(".")[0]
        elif isinstance(node, ast.Call):
            # __import__("socket") / importlib.import_module("socket") も拾う
            f = node.func
            name = getattr(f, "id", None) or getattr(f, "attr", None)
            if name in ("__import__", "import_module") and node.args:
                a0 = node.args[0]
                if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                    yield node.lineno, a0.value.split(".")[0]


class AstNoNetworkImports(unittest.TestCase):
    def test_sources_exist(self):
        self.assertTrue([n for n in os.listdir(SRC) if n.endswith(".py")])

    def test_no_network_imports(self):
        for name in sorted(os.listdir(SRC)):
            if not name.endswith(".py"):
                continue
            with open(os.path.join(SRC, name), encoding="utf-8") as f:
                tree = ast.parse(f.read(), name)
            for lineno, root in _imported_roots(tree):
                self.assertNotIn(root, BANNED, f"{name}:{lineno} が {root} を import している")


class GuardWorks(unittest.TestCase):
    def test_guard_blocks(self):
        import socket
        import urllib.request
        with contextlib.ExitStack() as st:
            for p in offline_guard.patches():
                st.enter_context(p)
            with self.assertRaises(offline_guard.NetworkAttempt):
                socket.getaddrinfo("example.invalid", 80)
            with self.assertRaises(offline_guard.NetworkAttempt):
                urllib.request.urlopen("http://example.invalid/")
            with socket.socket() as sk:
                with self.assertRaises(offline_guard.NetworkAttempt):
                    sk.connect(("127.0.0.1", 9))


class ExistingSuiteUnderGuard(unittest.TestCase):
    def test_all_existing_tests_pass_offline(self):
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        for mod in ("test_core", "test_cli"):
            suite.addTests(loader.loadTestsFromName(f"tests.{mod}"))
        n = suite.countTestCases()
        self.assertGreater(n, 0)
        with contextlib.ExitStack() as st:
            for p in offline_guard.patches():
                st.enter_context(p)
            res = unittest.TextTestRunner(verbosity=0).run(suite)
        self.assertTrue(res.wasSuccessful(), f"{len(res.failures)} failures, {len(res.errors)} errors")
        self.assertEqual(res.testsRun, n)


if __name__ == "__main__":
    unittest.main()
