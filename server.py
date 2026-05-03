import sqlite3
from fastmcp import FastMCP
import logging
import mongodb_mock

# Initialize MongoDB mock data
mongodb_mock.init_mongodb()

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
def check_rental_availability(asset_type: str = None) -> str:
    """
    Check the availability of rental assets (e.g., Notebooks, Projectors).
    
    Args:
        asset_type: Optional filter for a specific type of asset.
    """
    conn = get_db_connection()
    if asset_type:
        query = "SELECT asset_type, total_quantity, available_quantity FROM rentals WHERE asset_type LIKE ?"
        rows = conn.execute(query, (f"%{asset_type}%",)).fetchall()
    else:
        query = "SELECT asset_type, total_quantity, available_quantity FROM rentals"
        rows = conn.execute(query).fetchall()
    conn.close()

    if rows:
        lines = [f"- {row['asset_type']}: {row['available_quantity']} available (out of {row['total_quantity']})" for row in rows]
        return "Rental Asset Availability:\n" + "\n".join(lines)
    else:
        return f"No rental assets found matching '{asset_type or 'all'}'."

@mcp.tool()
def check_license_compliance(package_name: str) -> str:
    """
    Check if the number of deployments for a package exceeds purchased licenses.
    
    Args:
        package_name: The name of the package to check.
    """
    conn = get_db_connection()
    query = """
    SELECT p.name, l.purchased_count, COUNT(d.id) as deployed_count
    FROM packages p
    JOIN licenses l ON p.id = l.package_id
    LEFT JOIN deployments d ON p.id = d.package_id AND d.status = 'Success'
    WHERE p.name LIKE ?
    GROUP BY p.id
    """
    row = conn.execute(query, (f"%{package_name}%",)).fetchone()
    conn.close()

    if row:
        name, purchased, deployed = row['name'], row['purchased_count'], row['deployed_count']
        compliance = "COMPLIANT" if deployed <= purchased else "NON-COMPLIANT"
        status = f"License Status for '{name}': {compliance}\n"
        status += f"- Purchased: {purchased}\n"
        status += f"- Deployed: {deployed}\n"
        if deployed > purchased:
            status += f"WARNING: Over-licensed by {deployed - purchased} units!"
        return status
    else:
        return f"No license data found for package '{package_name}'."

@mcp.tool()
def get_server_telemetry(hostname: str) -> str:
    """
    Fetch real-time telemetry (CPU, Memory, Processes) from MongoDB for a specific server.
    
    Args:
        hostname: The hostname of the server.
    """
    telemetry = mongodb_mock.get_telemetry(hostname)
    if telemetry:
        return f"Real-time Telemetry for {hostname} (from MongoDB):\n{telemetry}"
    else:
        return f"No telemetry data available for {hostname} in MongoDB."

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
