import real_ladybug as ladybug

from create_db import LadybugDB

class LadybugQuery:
    def __init__(self, conn):
        self.conn = conn
    
    def get_response(self, result):
        return [row for row in result]

    def get_table_by_id(self, table_id):
        result = self.conn.execute(f"MATCH (t:Table_node {{id: '{table_id}'}}) RETURN t")
        return self.get_response(result)
    
    def get_columns_by_table(self, table_full_name):
        result = self.conn.execute(f"MATCH (c:Column_node)-[:Belong_to]->(t:Table_node) WHERE t.physical_name = '{table_full_name}' OR t.mask_name = '{table_full_name}' OR t.priv_name = '{table_full_name}' RETURN c")
        return self.get_response(result)
    
    def get_table_lineage(self, table_full_name, depth=None):
        depth_pattern = f"*1..{depth}" if depth else "*"
        result = self.conn.execute(f"MATCH (t1:Table_node)-[:Table_lineage{depth_pattern}]->(t2:Table_node) WHERE t1.physical_name = '{table_full_name}' OR t1.mask_name = '{table_full_name}' OR t1.priv_name = '{table_full_name}' RETURN t2")
        return self.get_response(result)
    
    def get_column_lineage(self, column_full_name, depth=None):
        depth_pattern = f"*1..{depth}" if depth else "*"
        result = self.conn.execute(f"MATCH (c1:Column_node)-[:Column_lineage{depth_pattern}]->(c2:Column_node) WHERE c1.physical_name = '{column_full_name}' OR c1.mask_name = '{column_full_name}' OR c1.priv_name = '{column_full_name}' RETURN c2")
        return self.get_response(result)
    
    def search_table_by_name(self, name_pattern):
        result = self.conn.execute(f"MATCH (t:Table_node) WHERE t.physical_name CONTAINS '{name_pattern}' RETURN t")
        return self.get_response(result)
    
    def search_table_by_full_name(self, full_name):
        result = self.conn.execute(f"MATCH (t:Table_node) WHERE t.physical_name = '{full_name}' OR t.mask_name = '{full_name}' OR t.priv_name = '{full_name}' RETURN t")
        return self.get_response(result)
    
    def search_column_by_full_name(self, full_name):
        result = self.conn.execute(f"MATCH (c:Column_node) WHERE c.physical_name = '{full_name}' OR c.mask_name = '{full_name}' OR c.priv_name = '{full_name}' RETURN c")
        return self.get_response(result)
    
    def get_upstream_tables(self, table_full_name, depth=None):
        depth_pattern = f"*1..{depth}" if depth else "*"
        result = self.conn.execute(f"MATCH (t1:Table_node)-[:Table_lineage{depth_pattern}]->(t2:Table_node) WHERE t2.physical_name = '{table_full_name}' OR t2.mask_name = '{table_full_name}' OR t2.priv_name = '{table_full_name}' RETURN t1")
        return self.get_response(result)
    
    def get_downstream_tables(self, table_full_name, depth=None):
        depth_pattern = f"*1..{depth}" if depth else "*"
        result = self.conn.execute(f"MATCH (t1:Table_node)-[:Table_lineage{depth_pattern}]->(t2:Table_node) WHERE t1.physical_name = '{table_full_name}' OR t1.mask_name = '{table_full_name}' OR t1.priv_name = '{table_full_name}' RETURN t2")
        return self.get_response(result)

if __name__ == "__main__":
    conn = LadybugDB().create_db("data/lineage_data.json")
    query = LadybugQuery(conn)
    
    # Example queries
    print("Table t0:")
    print(query.get_table_by_id("t0"))
    
    print("\nColumns of table t0:")
    print(query.get_columns_by_table("tcb_standardize.hr.customer_0"))
    
    print("\nDownstream tables (depth=1):")
    print(query.get_downstream_tables("tcb_standardize.hr.customer_0", depth=1))
    
    print("\nDownstream tables (depth=3):")
    print(query.get_downstream_tables("tcb_standardize.hr.customer_0", depth=3))
    
    print("\nSearch table by physical name:")
    print(query.search_table_by_full_name("tcb_standardize.hr.customer_0"))
    
    print("\nSearch table by mask name:")
    print(query.search_table_by_full_name("standardize_mask.hr.customer_0"))
    
    print("\nSearch column by full name:")
    print(query.search_column_by_full_name("tcb_standardize.hr.customer_0.id_0"))
