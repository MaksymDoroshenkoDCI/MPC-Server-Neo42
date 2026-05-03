import sqlite3
from fastmcp import FastMCP
import logging

# Initialize FastMCP server
mcp = FastMCP("Neo42 Application Package Center")

DB_PATH = "neo42_apc.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@mcp.tool()
def get_package_status(package_name: str, hostname: str) -> str:
    """
    Get the deployment status of a specific package on a specific endpoint.
    
    Args:
        package_name: Name of the software package (e.g., 'Google Chrome')
        hostname: Name of the endpoint/server (e.g., 'SRV-PROD-01')
    """
    conn = get_db_connection()
    query = """
    SELECT p.name as package, e.hostname, d.status, d.last_updated, d.error_log
    FROM deployments d
    JOIN packages p ON d.package_id = p.id
    JOIN endpoints e ON d.endpoint_id = e.id
    WHERE p.name LIKE ? AND e.hostname LIKE ?
    """
    row = conn.execute(query, (f"%{package_name}%", f"%{hostname}%")).fetchone()
    conn.close()

    if row:
        status_msg = f"Status of '{row['package']}' on '{row['hostname']}': {row['status']}"
        if row['error_log']:
            status_msg += f"\nError Log: {row['error_log']}"
        status_msg += f"\nLast Updated: {row['last_updated']}"
        return status_msg
    else:
        return f"No deployment record found for package '{package_name}' on host '{hostname}'."

@mcp.tool()
def list_server_inventory(hostname: str) -> str:
    """
    Lists all packages managed on a specific endpoint.
    
    Args:
        hostname: The hostname of the server to check.
    """
    conn = get_db_connection()
    query = """
    SELECT p.name, p.version, d.status
    FROM deployments d
    JOIN packages p ON d.package_id = p.id
    JOIN endpoints e ON d.endpoint_id = e.id
    WHERE e.hostname LIKE ?
    """
    rows = conn.execute(query, (f"%{hostname}%",)).fetchall()
    conn.close()

    if rows:
        inventory = [f"- {row['name']} (v{row['version']}): {row['status']}" for row in rows]
        return f"Inventory for {hostname}:\n" + "\n".join(inventory)
    else:
        return f"No inventory found for host '{hostname}'."

@mcp.tool()
def search_packages(query: str) -> str:
    """
    Search for available packages in the Application Package Center.
    
    Args:
        query: Search term for package name or category.
    """
    conn = get_db_connection()
    sql_query = "SELECT name, version, category FROM packages WHERE name LIKE ? OR category LIKE ?"
    rows = conn.execute(sql_query, (f"%{query}%", f"%{query}%")).fetchall()
    conn.close()

    if rows:
        results = [f"- {row['name']} (v{row['version']}) [{row['category']}]" for row in rows]
        return f"Found {len(rows)} packages:\n" + "\n".join(results)
    else:
        return f"No packages found matching '{query}'."

@mcp.tool()
def get_recent_pipelines() -> str:
    """
    Retrieves the status of recent deployment pipelines.
    """
    # For now, we simulate this with a static list or a simple query if we had data
    # In a real scenario, this would hit the 'pipelines' table
    return "Recent Pipelines:\n- Deploy Adobe Acrobat (SRV-PROD-01): SUCCESS\n- Deploy Neo42 Agent (WS-SUP-01): IN_PROGRESS (Step 3/5)\n- Update Chrome (SRV-PROD-02): FAILED (Checksum mismatch)"

if __name__ == "__main__":
    mcp.run()
