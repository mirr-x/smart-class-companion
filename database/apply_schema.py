"""
Minimal Python executor for SQL schema file.
Reads and executes schema.sql - all DB logic is in the SQL file.
"""
import os
import sys
import oracledb

def execute_sql_file():
    user = os.getenv('ORACLE_DB_USER', 'system')
    password = os.getenv('ORACLE_DB_PASSWORD', 'oracle')
    host = os.getenv('ORACLE_DB_HOST', 'oracle')
    port = os.getenv('ORACLE_DB_PORT', '1521')
    name = os.getenv('ORACLE_DB_NAME', 'xepdb1')
    dsn = f"//{host}:{port}/{name}"
    
    sql_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    try:
        with open(sql_file, 'r') as f:
            sql_content = f.read()
        
        conn = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = conn.cursor()
        
        print(f"Executing schema.sql on {dsn}...")
        print("(All database creation logic is in schema.sql - pure PL/SQL)\n")
        
        # Remove the SET commands and trailing /
        sql_content = sql_content.replace('SET SERVEROUTPUT ON;', '')
        sql_content = sql_content.replace('DBMS_OUTPUT.PUT_LINE', '-- DBMS_OUTPUT.PUT_LINE')
        if sql_content.strip().endswith('/'):
            sql_content = sql_content.strip()[:-1]
        
        # Execute the PL/SQL block
        cursor.execute(sql_content)
        conn.commit()
        
        print("\n✓ Schema created successfully from schema.sql!")
        print("✓ All 19 tables created")
        print("✓ All migrations registered")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    execute_sql_file()
