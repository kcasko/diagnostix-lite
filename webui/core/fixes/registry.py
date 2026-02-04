"""
DiagnOStiX 3.0 - Fix Registry

Singleton registry for managing all fix instances with:
- Category-based filtering
- Risk level filtering
- Platform compatibility filtering
"""

from typing import Dict, List, Type, Optional
from core.fixes.base import Fix, FixCategory, RiskLevel
import logging

logger = logging.getLogger(__name__)


class FixRegistry:
    """
    Singleton registry for all DiagnOStiX fixes.
    
    Provides:
    - Fix registration and retrieval
    - Category-based filtering
    - Risk level filtering
    - Platform compatibility filtering
    """
    _instance = None
    _fixes: Dict[str, Fix] = {}
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FixRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _ensure_loaded(cls) -> None:
        """Ensure fix implementations are imported and registered."""
        if cls._initialized and cls._fixes:
            return
        try:
            import core.fixes.implementations  # noqa: F401
        except Exception as e:
            logger.error(f"Failed to load fix implementations: {e}", exc_info=True)
        cls._initialized = True

    @classmethod
    def register(cls, fix_cls: Type[Fix]):
        """Register a new fix class."""
        try:
            fix_instance = fix_cls()
            if fix_instance.id in cls._fixes:
                logger.warning(f"Fix with ID {fix_instance.id} already registered. Overwriting.")
            cls._fixes[fix_instance.id] = fix_instance
            logger.info(f"Registered fix: {fix_instance.name} ({fix_instance.id}) "
                       f"[{fix_instance.category.value}] [{fix_instance.risk_level.value}]")
            cls._initialized = True
        except Exception as e:
            logger.error(f"Failed to register fix {fix_cls}: {e}")

    @classmethod
    def get_fix(cls, fix_id: str) -> Optional[Fix]:
        """Retrieve a fix instance by ID."""
        cls._ensure_loaded()
        return cls._fixes.get(fix_id)

    @classmethod
    def get_all_fixes(cls) -> List[Fix]:
        """Retrieve all registered fixes."""
        cls._ensure_loaded()
        return list(cls._fixes.values())

    @classmethod
    def get_fixes_by_category(cls, category: FixCategory) -> List[Fix]:
        """Retrieve all fixes in a specific category."""
        cls._ensure_loaded()
        return [fix for fix in cls._fixes.values() if fix.category == category]

    @classmethod
    def get_fixes_by_risk(cls, risk_level: RiskLevel) -> List[Fix]:
        """Retrieve all fixes with a specific risk level."""
        cls._ensure_loaded()
        return [fix for fix in cls._fixes.values() if fix.risk_level == risk_level]

    @classmethod
    def get_safe_fixes(cls) -> List[Fix]:
        """Retrieve all fixes that are safe to run."""
        cls._ensure_loaded()
        return [fix for fix in cls._fixes.values() if fix.risk_level == RiskLevel.SAFE]

    @classmethod
    def get_compatible_fixes(cls) -> List[Fix]:
        """Retrieve all fixes compatible with the current platform."""
        cls._ensure_loaded()
        return [fix for fix in cls._fixes.values() if fix.check_platform_compatibility()]

    @classmethod
    def get_fixes_requiring_admin(cls) -> List[Fix]:
        """Retrieve all fixes that require admin privileges."""
        cls._ensure_loaded()
        return [fix for fix in cls._fixes.values() if fix.requires_admin]

    @classmethod
    def get_categories(cls) -> List[Dict]:
        """Get all categories with their fix counts."""
        cls._ensure_loaded()
        categories = {}
        for fix in cls._fixes.values():
            cat = fix.category
            if cat not in categories:
                categories[cat] = {
                    "id": cat.value,
                    "label": cat.label,
                    "icon": cat.icon,
                    "count": 0,
                    "safe_count": 0
                }
            categories[cat]["count"] += 1
            if fix.risk_level == RiskLevel.SAFE:
                categories[cat]["safe_count"] += 1
        return list(categories.values())

    @classmethod
    def search_fixes(cls, query: str) -> List[Fix]:
        """Search fixes by name, description, or tags."""
        cls._ensure_loaded()
        query = query.lower()
        results = []
        for fix in cls._fixes.values():
            if (query in fix.name.lower() or 
                query in fix.description.lower() or
                any(query in tag.lower() for tag in fix.tags)):
                results.append(fix)
        return results

    @classmethod
    def get_fix_count(cls) -> int:
        """Get total number of registered fixes."""
        cls._ensure_loaded()
        return len(cls._fixes)

    @classmethod
    def clear(cls):
        """Clear all registered fixes (useful for testing)."""
        cls._fixes.clear()
        cls._initialized = False
