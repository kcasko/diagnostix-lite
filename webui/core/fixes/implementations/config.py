"""
DiagnOStiX 3.0 - Configuration Fixes
"""

import asyncio
from typing import Dict, Any

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry
from core.script_runner import script_runner


class RestoreContextMenuFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "restore_context_menu"
        self.name = "Restore Classic Context Menu"
        self.description = "Restore Windows 11 full right-click context menu (removes simplified menu)."
        self.simple_description = "Get back the old right-click menu with all options visible."
        self.category = FixCategory.CONFIG
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows"]
        self.requires_admin = False
        self.requires_reboot = True
        self.estimated_time = 5
        self.tags = ["context", "menu", "right-click", "windows11", "ui"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return (
            "Will modify registry to restore classic context menu:
"
            "- Disables Windows 11 simplified right-click menu
"
            "- Shows all options directly without 'Show more options'

"
            "Requires Explorer restart or reboot to take effect."
        )

    def run(self) -> Dict[str, Any]:
        result = asyncio.get_event_loop().run_until_complete(
            script_runner.apply_registry("03-Config-Tweaks/ContextMenu_old.reg")
        )
        return {"output": result.stdout, "requires_reboot": True}

    def verify(self) -> bool:
        return True


class DisableBingSearchFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "disable_bing_search"
        self.name = "Disable Bing Search"
        self.description = "Remove Bing web results from Windows Start menu search."
        self.simple_description = "Stop seeing web results when you search in the Start menu."
        self.category = FixCategory.CONFIG
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows"]
        self.requires_admin = False
        self.estimated_time = 5
        self.tags = ["bing", "search", "privacy", "start", "menu"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return (
            "Will disable Bing search integration:
"
            "- BingSearchEnabled = 0
"
            "- SearchboxTaskbarMode = 0

"
            "Start menu search will only show local results."
        )

    def run(self) -> Dict[str, Any]:
        result = asyncio.get_event_loop().run_until_complete(
            script_runner.apply_registry("03-Config-Tweaks/Disable_Bing_Search.reg")
        )
        return {"output": result.stdout}

    def verify(self) -> bool:
        return True


class EnableLongPathsFix(Fix):
    def __init__(self):
        super().__init__()
        self.id = "enable_long_paths"
        self.name = "Enable Long File Paths"
        self.description = "Enable Windows support for file paths longer than 260 characters."
        self.simple_description = "Allow longer file and folder names (needed for some programs)."
        self.category = FixCategory.CONFIG
        self.risk_level = RiskLevel.SAFE
        self.supported_platforms = ["windows"]
        self.requires_admin = True
        self.estimated_time = 5
        self.tags = ["path", "long", "260", "developer", "git"]

    def detect(self) -> bool:
        return True

    def preview(self) -> str:
        return (
            "Will enable long path support:
"
            "- LongPathsEnabled = 1 (in HKLM)

"
            "Required for modern development tools (Git, Node.js, etc.)."
        )

    def run(self) -> Dict[str, Any]:
        result = asyncio.get_event_loop().run_until_complete(
            script_runner.apply_registry("03-Config-Tweaks/Enable_LongPaths.reg")
        )
        return {"output": result.stdout}

    def verify(self) -> bool:
        return True


FixRegistry.register(RestoreContextMenuFix)
FixRegistry.register(DisableBingSearchFix)
FixRegistry.register(EnableLongPathsFix)
