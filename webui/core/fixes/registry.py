from typing import Dict, List, Type
from .base import Fix
import logging

logger = logging.getLogger(__name__)

class FixRegistry:
    _instance = None
    _fixes: Dict[str, Fix] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FixRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, fix_cls: Type[Fix]):
        """Register a new fix class."""
        try:
            fix_instance = fix_cls()
            if fix_instance.id in cls._fixes:
                logger.warning(f"Fix with ID {fix_instance.id} already registered. Overwriting.")
            cls._fixes[fix_instance.id] = fix_instance
            logger.info(f"Registered fix: {fix_instance.name} ({fix_instance.id})")
        except Exception as e:
            logger.error(f"Failed to register fix {fix_cls}: {e}")

    @classmethod
    def get_fix(cls, fix_id: str) -> Fix:
        """Retrieve a fix instance by ID."""
        return cls._fixes.get(fix_id)

    @classmethod
    def get_all_fixes(cls) -> List[Fix]:
        """Retrieve all registered fixes."""
        return list(cls._fixes.values())

    @classmethod
    def clear(cls):
        """Clear all registered fixes (useful for testing)."""
        cls._fixes.clear()
