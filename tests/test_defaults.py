"""Validate the community defaults inherited by CraftedSignal repositories."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CommunityDefaultsTests(unittest.TestCase):
    def test_every_file_has_a_valid_default_owner(self):
        rules = [line.split() for line in (ROOT / "CODEOWNERS").read_text().splitlines()
                 if line.strip() and not line.lstrip().startswith("#")]
        defaults = [owners for pattern, *owners in rules if pattern == "*"]
        self.assertTrue(defaults, "a catch-all owner is needed for new files")
        for owners in defaults:
            self.assertTrue(owners, "CODEOWNERS rules must name an owner")
            for owner in owners:
                self.assertRegex(owner, r"^@[A-Za-z0-9][A-Za-z0-9-]*(/[A-Za-z0-9_.-]+)?$")

    def test_security_reports_have_a_private_contact(self):
        policy = (ROOT / "SECURITY.md").read_text()
        self.assertIn("security@craftedsignal.io", policy)
        self.assertIn("Report a vulnerability", policy)
        self.assertRegex(policy.lower(), r"do not open public issues")

    def test_local_document_links_resolve(self):
        for doc in ROOT.glob("*.md"):
            for target in re.findall(r"\[[^\]]*\]\(([^ )]+)(?: [^)]*)?\)", doc.read_text()):
                if ":" in target or target.startswith("#"):
                    continue
                with self.subTest(doc=doc.name, target=target):
                    self.assertTrue((doc.parent / target.split("#")[0]).is_file())


if __name__ == "__main__":
    unittest.main()
