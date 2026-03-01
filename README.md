# LadybugDB - Data Lineage Graph Database

## Data Structure

### Naming Patterns

Each table/column has 3 catalog names representing different access levels:

**Table Format:**
- Physical: `tcb_{zone}.{schema}.{table_name}_{id}`
- Mask: `{zone}_mask.{schema}.{table_name}_{id}`
- Priv: `{zone}_priv.{schema}.{table_name}_{id}`

**Column Format:**
- Physical: `tcb_{zone}.{schema}.{table_name}_{id}.{column_name}_{id}`
- Mask: `{zone}_mask.{schema}.{table_name}_{id}.{column_name}_{id}`
- Priv: `{zone}_priv.{schema}.{table_name}_{id}.{column_name}_{id}`

### Data Components

**Zones (3):**
- `standardize` - Raw data layer
- `curated` - Processed data layer
- `insights` - Analytics/reporting layer

**Schemas (8):**
- `rbg`, `sales`, `finance`, `hr`, `analytics`, `reporting`, `marketing`, `operations`

**Table Names (10):**
- `customer`, `order`, `product`, `transaction`, `employee`, `invoice`, `payment`, `shipment`, `inventory`, `campaign`

**Column Names (12):**
- `id`, `name`, `date`, `amount`, `status`, `type`, `code`, `value`, `count`, `total`, `avg`, `sum`

### Dataset Size
- **Tables:** 100 (t0-t99)
- **Columns:** 500-1000 (5-12 columns per table)
- **Table Lineage:** Chain structure with depth up to 11 hops
- **Column Lineage:** 300 relationships

## Example Data

```
Table: tcb_standardize.hr.customer_0
  - tcb_standardize.hr.customer_0.id_0
  - tcb_standardize.hr.customer_0.name_1
  - tcb_standardize.hr.customer_0.status_2

Table: curated_mask.sales.order_5
  - curated_mask.sales.order_5.amount_0
  - curated_mask.sales.order_5.date_1
```

## Query Examples

### 1. Search Table by Full Name
```python
query.search_table_by_full_name("tcb_standardize.hr.customer_0")
query.search_table_by_full_name("standardize_mask.hr.customer_0")
query.search_table_by_full_name("standardize_priv.hr.customer_0")
```

### 2. Get Columns of a Table
```python
query.get_columns_by_table("tcb_standardize.hr.customer_0")
```

### 3. Get Downstream Tables (with depth)
```python
# 1 hop downstream
query.get_downstream_tables("tcb_standardize.hr.customer_0", depth=1)

# 3 hops downstream
query.get_downstream_tables("tcb_standardize.hr.customer_0", depth=3)

# All downstream (up to 11 hops)
query.get_downstream_tables("tcb_standardize.hr.customer_0")
```

### 4. Get Upstream Tables
```python
query.get_upstream_tables("tcb_insights.reporting.customer_summary_99", depth=5)
```

### 5. Get Column Lineage
```python
query.get_column_lineage("tcb_standardize.hr.customer_0.id_0", depth=2)
```

### 6. Search Column by Full Name
```python
query.search_column_by_full_name("tcb_standardize.hr.customer_0.id_0")
```

## Setup & Run

### 1. Generate Data
```bash
python generate_data.py
```

### 2. Create Database
```bash
python create_db.py
```

### 3. Query Database
```bash
python query_db.py
```

## Query API

### LadybugQuery Methods

| Method | Parameters | Description |
|--------|------------|-------------|
| `get_table_by_id(table_id)` | table_id: str | Get table by ID (t0-t99) |
| `get_columns_by_table(table_full_name)` | table_full_name: str | Get all columns of a table |
| `get_table_lineage(table_full_name, depth)` | table_full_name: str, depth: int\|None | Get table lineage |
| `get_column_lineage(column_full_name, depth)` | column_full_name: str, depth: int\|None | Get column lineage |
| `search_table_by_full_name(full_name)` | full_name: str | Search table by exact name |
| `search_column_by_full_name(full_name)` | full_name: str | Search column by exact name |
| `get_upstream_tables(table_full_name, depth)` | table_full_name: str, depth: int\|None | Get upstream tables |
| `get_downstream_tables(table_full_name, depth)` | table_full_name: str, depth: int\|None | Get downstream tables |

### Depth Parameter
- `depth=1`: Direct connections only
- `depth=3`: Up to 3 hops
- `depth=11`: Maximum depth in dataset
- `depth=None`: All reachable nodes
