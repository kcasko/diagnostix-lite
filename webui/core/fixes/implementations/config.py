"""
DiagnOStiX 3.0 - Configuration Fixes (Pure Python)
"""

import winreg
from typing import Dict, Any

from core.fixes.base import Fix, FixCategory, RiskLevel
from core.fixes.registry import FixRegistry


def set_registry_value(key_path: str, value_name: str, value_data, value_type=winreg.REG_DWORD, hive=winreg.HKEY_CURRENT_USER):
    """Helper to set a registry value, creating the key if needed."""
    try:
        key = winreg.CreateKeyEx(hive, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, value_type, value_data)
        winreg.CloseKey(key)
        return True
    except PermissionError:
        raise PermissionError(f"Admin required to modify {key_path}")
    except Exception as e:
        raise Exception(f"Registry error: {e}")


def get_registry_value(key_path: str, value_name: str, hive=winreg.HKEY_CURRENT_USER, default=None):
    """Helper to read a registry value."""
    try:
        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return value
    except FileNotFoundError:
        return default
    except Exception:
        return default


class RestoreContextMenuFix(Fix):
    """Restore Windows 11 classic context menu using winreg."""

    REG_PATH = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"

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
        # Check if the key already exists (fix already applied)
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_PATH, 0, winreg.KEY_READ)
            winreg.CloseKey(key)
            return False  # Already fixed
        except FileNotFoundError:
            return True  # Fix needed

    def preview(self) -> str:
        return (
            "Will modify registry to restore classic context menu:\n"
            "- Creates key: HKCU\\Software\\Classes\\CLSID\\{86ca1aa0-...}\\InprocServer32\n"
            "- Sets default value to empty string\n\n"
            "Requires Explorer restart or reboot to take effect."
        )

    def run(self) -> Dict[str, Any]:
        try:
            key = winreg.CreateKeyEx(
                winreg.HKEY_CURRENT_USER,
                self.REG_PATH,
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "")
            winreg.CloseKey(key)
            return {"output": "Classic context menu restored. Restart Explorer or reboot.", "requires_reboot": True}
        except Exception as e:
            raise Exception(f"Failed to modify registry: {e}")

    def verify(self) -> bool:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_PATH, 0, winreg.KEY_READ)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False


class DisableBingSearchFix(Fix):
    """Disable Bing search in Windows Start menu using winreg."""

    REG_PATH = r"Software\Policies\Microsoft\Windows\Explorer"

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
        # Check if DisableSearchBoxSuggestions is already set
        value = get_registry_value(self.REG_PATH, "DisableSearchBoxSuggestions")
        return value != 1  # Fix needed if not already 1

    def preview(self) -> str:
        return (
            "Will disable Bing search integration:\n"
            "- DisableSearchBoxSuggestions = 1\n\n"
            "Start menu search will only show local results."
        )

    def run(self) -> Dict[str, Any]:
        set_registry_value(self.REG_PATH, "DisableSearchBoxSuggestions", 1, winreg.REG_DWORD)
        return {"output": "Bing search disabled. Changes take effect immediately or after restart."}

    def verify(self) -> bool:
        value = get_registry_value(self.REG_PATH, "DisableSearchBoxSuggestions")
        return value == 1


class EnableLongPathsFix(Fix):
    """Enable Windows long path support using winreg (requires admin)."""

    REG_PATH = r"SYSTEM\CurrentControlSet\Control\FileSystem"

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
        # Check if already enabled
        value = get_registry_value(self.REG_PATH, "LongPathsEnabled", hive=winreg.HKEY_LOCAL_MACHINE)
        return value != 1

    def preview(self) -> str:
        return (
            "Will enable long path support:\n"
            "- LongPathsEnabled = 1 (in HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem)\n\n"
            "Required for modern development tools (Git, Node.js, etc.).\n"
            "NOTE: Requires administrator privileges."
        )

    def run(self) -> Dict[str, Any]:
        try:
            set_registry_value(
                self.REG_PATH, 
                "LongPathsEnabled", 
                1, 
                winreg.REG_DWORD, 
                hive=winreg.HKEY_LOCAL_MACHINE
            )
            return {"output": "Long paths enabled. Changes take effect for new processes."}
        except PermissionError:
            raise PermissionError("Administrator privileges required to enable long paths.")

    def verify(self) -> bool:
        value = get_registry_value(self.REG_PATH, "LongPathsEnabled", hive=winreg.HKEY_LOCAL_MACHINE)
        return value == 1


FixRegistry.register(RestoreContextMenuFix)
FixRegistry.register(DisableBingSearchFix)
FixRegistry.register(EnableLongPathsFix)
