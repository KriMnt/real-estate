from app.database import get_db
from sqlalchemy import inspect, text

def check_database_tables():
    try:
        db = next(get_db())
        inspector = inspect(db.bind)
        
        # List all tables
        tables = inspector.get_table_names()
        print(f"Tables in database: {tables}")
        
        # For each table, show some columns
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"\nTable '{table}' columns:")
            for i, column in enumerate(columns):
                if i < 5:  # Just show first 5 columns to keep output manageable
                    print(f"  - {column['name']} ({column['type']})")
            
            # Count rows
            count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()
            print(f"  Row count: {count[0]}")
        
        return True
    except Exception as e:
        print(f"Error checking tables: {e}")
        return False

if __name__ == "__main__":
    check_database_tables()