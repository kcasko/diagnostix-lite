from core.fixes.registry import FixRegistry
from core.fixes.base import Fix, FixCategory, RiskLevel


class SafeFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "test_safe"
        self.name = "Safe Fix"
        self.category = FixCategory.MAINTENANCE
        self.risk_level = RiskLevel.SAFE

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return "Preview"

    def run(self):
        return {"ok": True}

    def verify(self) -> bool:
        return True


class ModerateFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "test_mod"
        self.name = "Moderate Fix"
        self.category = FixCategory.PERFORMANCE
        self.risk_level = RiskLevel.MODERATE

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return "Preview"

    def run(self):
        return {"ok": True}

    def verify(self) -> bool:
        return True


def test_registry_filters():
    original = dict(FixRegistry._fixes)
    try:
        FixRegistry.clear()
        FixRegistry.register(SafeFix)
        FixRegistry.register(ModerateFix)

        assert FixRegistry.get_fix_count() == 2
        assert len(FixRegistry.get_safe_fixes()) == 1
        assert FixRegistry.get_safe_fixes()[0].id == "test_safe"

        perf = FixRegistry.get_fixes_by_category(FixCategory.PERFORMANCE)
        assert len(perf) == 1
        assert perf[0].id == "test_mod"
    finally:
        FixRegistry.clear()
        FixRegistry._fixes = original
