from core.fixes.engine import FixEngine
from core.fixes.registry import FixRegistry
from core.fixes.base import Fix, FixCategory, RiskLevel
import core.fixes.engine as engine_module


class GoodFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "good_fix"
        self.name = "Good Fix"
        self.category = FixCategory.MAINTENANCE
        self.risk_level = RiskLevel.SAFE

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return "Preview"

    def run(self):
        return {"result": "done"}

    def verify(self) -> bool:
        return True


class SkipFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "skip_fix"
        self.name = "Skip Fix"
        self.category = FixCategory.MAINTENANCE
        self.risk_level = RiskLevel.SAFE

    def detect(self) -> bool:
        return False

    def preview(self) -> str:
        return "Preview"

    def run(self):
        return {"result": "done"}

    def verify(self) -> bool:
        return True


class IncompatibleFix(GoodFix):
    def __init__(self):
        super().__init__()
        self.id = "incompatible_fix"
        self.supported_platforms = ["never"]


def test_fix_engine_success(monkeypatch):
    original = dict(FixRegistry._fixes)
    monkeypatch.setattr(engine_module.db_instance, "log_execution", lambda *args, **kwargs: None)
    try:
        FixRegistry.clear()
        FixRegistry.register(GoodFix)
        result = FixEngine.run_fix("good_fix")
        assert result["success"] is True
    finally:
        FixRegistry.clear()
        FixRegistry._fixes = original


def test_fix_engine_skipped(monkeypatch):
    original = dict(FixRegistry._fixes)
    monkeypatch.setattr(engine_module.db_instance, "log_execution", lambda *args, **kwargs: None)
    try:
        FixRegistry.clear()
        FixRegistry.register(SkipFix)
        result = FixEngine.run_fix("skip_fix")
        assert result.get("skipped") is True
    finally:
        FixRegistry.clear()
        FixRegistry._fixes = original


def test_fix_engine_incompatible(monkeypatch):
    original = dict(FixRegistry._fixes)
    monkeypatch.setattr(engine_module.db_instance, "log_execution", lambda *args, **kwargs: None)
    try:
        FixRegistry.clear()
        FixRegistry.register(IncompatibleFix)
        result = FixEngine.run_fix("incompatible_fix")
        assert result["success"] is False
        assert "platform" in result["message"].lower()
    finally:
        FixRegistry.clear()
        FixRegistry._fixes = original
