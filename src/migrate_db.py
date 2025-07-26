"""
migrate_db.py
Database migration script to add new columns to existing tables.
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """
    Add new columns to the users table for age, cycle_start_date, and period_duration.
    """
    db_path = "cyclewise.db"
    
    if not os.path.exists(db_path):
        print("Database file not found. Please run init_db.py first.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add new columns if they don't exist
        if 'age' not in columns:
            print("Adding 'age' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")
        
        if 'cycle_start_date' not in columns:
            print("Adding 'cycle_start_date' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN cycle_start_date DATETIME")
        
        if 'period_duration' not in columns:
            print("Adding 'period_duration' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN period_duration INTEGER")
        
        conn.commit()
        print("✅ Database migration completed successfully!")
        
        # Show updated table structure
        cursor.execute("PRAGMA table_info(users)")
        print("\nUpdated users table structure:")
        for column in cursor.fetchall():
            print(f"  {column[1]} ({column[2]})")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    migrate_database() 