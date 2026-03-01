import json
import random

def collect_data():
    zones = ["standardize", "curated", "insights"]
    schemas = ["rbg", "sales", "finance", "hr", "analytics", "reporting", "marketing", "operations"]
    table_names = ["customer", "order", "product", "transaction", "employee", "invoice", "payment", "shipment", "inventory", "campaign"]
    column_names = ["id", "name", "date", "amount", "status", "type", "code", "value", "count", "total", "avg", "sum"]

    tables = []
    columns = []
    relational = []
    table_edges = []
    column_edges = []

    col_id = 0
    for i in range(100):
        zone = zones[i % 3]
        schema = random.choice(schemas)
        table = f"{random.choice(table_names)}_{i}"
        
        tables.append({
            "id": f"t{i}",
            "physical_name": f"tcb_{zone}.{schema}.{table}",
            "mask_name": f"{zone}_mask.{schema}.{table}",
            "priv_name": f"{zone}_priv.{schema}.{table}"
        })
        
        num_cols = random.randint(5, 12)
        for j in range(num_cols):
            col_name = f"{random.choice(column_names)}_{j}"
            columns.append({
                "id": f"c{col_id}",
                "physical_name": f"tcb_{zone}.{schema}.{table}.{col_name}",
                "mask_name": f"{zone}_mask.{schema}.{table}.{col_name}",
                "priv_name": f"{zone}_priv.{schema}.{table}.{col_name}",
                "table_id": f"t{i}"
            })
            relational.append({"column_id": f"c{col_id}", "table_id": f"t{i}"})
            col_id += 1

    # Create chain-like structure for deep lineage (up to depth 11)
    for i in range(11):
        for j in range(8):
            src = i * 8 + j
            dst = (i + 1) * 8 + j
            if src < 100 and dst < 100:
                table_edges.append({"from": f"t{src}", "to": f"t{dst}", "type": "feeds"})
    
    # Add some random cross-connections
    for i in range(30):
        src = random.randint(0, 99)
        dst = random.randint(0, 99)
        if src != dst and abs(src - dst) > 5:
            table_edges.append({"from": f"t{src}", "to": f"t{dst}", "type": "feeds"})

    # Column lineage with depth
    for i in range(300):
        src = random.randint(0, len(columns)-1)
        dst = random.randint(0, len(columns)-1)
        if src != dst:
            column_edges.append({"from": f"c{src}", "to": f"c{dst}", "type": random.choice(["derived_from", "aggregated_to"])})

    return {
        "nodes": {"tables": tables, "columns": columns},
        "edges": {"table_to_table": table_edges, "column_to_column": column_edges},
        "relational": relational
    }

if __name__ == "__main__":
    print("Generating data...")
    data = collect_data()
    with open('data/lineage_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Generated {len(data['nodes']['tables'])} tables, {len(data['nodes']['columns'])} columns")
