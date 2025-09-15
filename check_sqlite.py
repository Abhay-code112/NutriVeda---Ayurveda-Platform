import sqlite3
import os

def check_sqlite_database():
    """Check SQLite database status and configuration"""
    
    db_path = 'nutriveda.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    print("📊 SQLite Database Status:")
    print(f"   📁 File: {os.path.abspath(db_path)}")
    print(f"   📏 Size: {os.path.getsize(db_path)} bytes")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n🗂️  Tables ({len(tables)}):")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   ✅ {table_name}: {count} records")
        
        # Check backend tables specifically
        backend_tables = [t[0] for t in tables if 'backend' in t[0]]
        if backend_tables:
            print(f"\n🎯 Backend Tables ({len(backend_tables)}):")
            for table in backend_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   📋 {table}: {count} records")
        
        conn.close()
        print("\n✅ SQLite database is working perfectly!")
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")

if __name__ == "__main__":
    check_sqlite_database()
