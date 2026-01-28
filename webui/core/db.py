import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

DB_NAME = "diagnostix.db"

class Database:
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            # Default to storing in the parent directory of this file (core/../) -> base/diagnostix.db
            # Or better, alongside the main.py or in a dedicated data dir.
            # Let's put it in the webui root for now.
            base_path = Path(__file__).resolve().parent.parent
            self.db_path = base_path / DB_NAME
        else:
            self.db_path = db_path
            
        self.conn = None

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(
                self.db_path, 
                check_same_thread=False  # Needed for FastAPI threading
            )
            self.conn.row_factory = sqlite3.Row
            logger.info(f"Connected to database at {self.db_path}")
            self.init_db()
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def init_db(self):
        """Initialize the database schema."""
        create_audit_log_table = """
        CREATE TABLE IF NOT EXISTS fix_audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            hostname TEXT NOT NULL,
            os TEXT NOT NULL,
            fix_id TEXT NOT NULL,
            condition_id TEXT,
            before_state TEXT,
            after_state TEXT,
            result TEXT NOT NULL,
            error_message TEXT
        );
        """
        try:
            with self.conn:
                self.conn.execute(create_audit_log_table)
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def log_execution(self, 
                      fix_id: str, 
                      hostname: str, 
                      os_name: str, 
                      result: str, 
                      before_state: Any = None, 
                      after_state: Any = None, 
                      condition_id: str = "manual",
                      error_message: Optional[str] = None):
        """Log a fix execution to the audit table."""
        try:
            query = """
            INSERT INTO fix_audit_log (
                timestamp, hostname, os, fix_id, condition_id, 
                before_state, after_state, result, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Serialize states if they are dicts/lists
            before_json = json.dumps(before_state) if isinstance(before_state, (dict, list)) else str(before_state)
            after_json = json.dumps(after_state) if isinstance(after_state, (dict, list)) else str(after_state)
            
            with self.conn:
                self.conn.execute(query, (
                    datetime.now().isoformat(),
                    hostname,
                    os_name,
                    fix_id,
                    condition_id,
                    before_json,
                    after_json,
                    result,
                    error_message
                ))
        except sqlite3.Error as e:
            logger.error(f"Failed to write to audit log: {e}")

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve execution history."""
        try:
            cursor = self.conn.execute(
                "SELECT * FROM fix_audit_log ORDER BY timestamp DESC LIMIT ?", 
                (limit,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Failed to retrieve history: {e}")
            return []

# Singleton instance
db_instance = Database()
