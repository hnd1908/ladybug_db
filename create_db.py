import json
import real_ladybug as ladybug
from generate_data import collect_data

class LadybugDB:
    def __init__(self) -> None:
        self.db = ladybug.Database()
        self.conn = ladybug.Connection(self.db)
    
    def create_schema(self) -> None:
        self.conn.execute("""
            CREATE NODE TABLE Table_node (
                id STRING PRIMARY KEY,
                physical_name STRING,
                mask_name STRING,
                priv_name STRING
            )
        """)
        self.conn.execute("""
            CREATE NODE TABLE Column_node (
                id STRING PRIMARY KEY,
                physical_name STRING,
                mask_name STRING,
                priv_name STRING
            )
        """)
        self.conn.execute("""
            CREATE REL TABLE Table_lineage (FROM Table_node TO Table_node, type STRING)
        """)
        self.conn.execute("""
            CREATE REL TABLE Column_lineage (FROM Column_node TO Column_node, type STRING)
        """)
        self.conn.execute("""
            CREATE REL TABLE Belong_to (FROM Column_node TO Table_node)
        """)
    
    def load_data(self, json_file) -> None:
        with open(json_file) as f:
            data = __import__('json').load(f)
        
        for table in data['nodes']['tables']:
            self.conn.execute(f"CREATE (t:Table_node {{id: '{table['id']}', physical_name: '{table['physical_name']}', mask_name: '{table['mask_name']}', priv_name: '{table['priv_name']}'}})")
        
        for col in data['nodes']['columns']:
            self.conn.execute(f"CREATE (c:Column_node {{id: '{col['id']}', physical_name: '{col['physical_name']}', mask_name: '{col['mask_name']}', priv_name: '{col['priv_name']}'}})")
        
        for rel in data['relational']:
            self.conn.execute(f"MATCH (c:Column_node {{id: '{rel['column_id']}'}}), (t:Table_node {{id: '{rel['table_id']}'}}) CREATE (c)-[:Belong_to]->(t)")
        
        for edge in data['edges']['table_to_table']:
            self.conn.execute(f"MATCH (t1:Table_node {{id: '{edge['from']}'}}), (t2:Table_node {{id: '{edge['to']}'}}) CREATE (t1)-[:Table_lineage {{type: '{edge['type']}'}}]->(t2)")
        
        for edge in data['edges']['column_to_column']:
            self.conn.execute(f"MATCH (c1:Column_node {{id: '{edge['from']}'}}), (c2:Column_node {{id: '{edge['to']}'}}) CREATE (c1)-[:Column_lineage {{type: '{edge['type']}'}}]->(c2)")


    def create_db(self, json_file) -> ladybug.Connection:
        self.create_schema()
        self.load_data(json_file)

        return self.conn
if __name__ == "__main__":
    print("Do you want to generate new data? (y/n)")
    user_input = input().strip().lower()
    if user_input == 'y':
        print("Generating new data...")
        data = collect_data()
        with open('data/lineage_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Generated {len(data['nodes']['tables'])} tables, {len(data['nodes']['columns'])} columns")
    print("Creating database...")
    db = LadybugDB()
    db.create_db("data/lineage_data.json")
    print("Database created successfully.")