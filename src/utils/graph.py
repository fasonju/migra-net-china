import pandas as pd
import networks

# Build network with geographic data
def build_geo_network(df: pd.DataFrame, start_year: int, end_year: int) -> networks.Digraph:
    G = networks.DiGraph()
    
    # Helper to get node ID and Coords
    def get_node_info(row, prefix):
        # Determine column names based on prefix
        name_col = 'current_city' if prefix == 'current' else f'{prefix}_Name_Prefecture'
        lon_col = f'{prefix}_lon'
        lat_col = f'{prefix}_lat'
        
        node_id = row[name_col]
        coords = (row[lon_col], row[lat_col])
        return node_id, coords

    for idx, row in df.iterrows():
        # Extract info
        u_name, u_pos = get_node_info(row, 'hometown')
        v1_name, v1_pos = get_node_info(row, 'first')
        v2_name, v2_pos = get_node_info(row, 'current')
        
        # Add Nodes with Position Data (Idempotent)
        G.add_node(u_name, pos=u_pos)
        G.add_node(v1_name, pos=v1_pos)
        G.add_node(v2_name, pos=v2_pos)

        # Logic: Hometown -> First
        if start_year <= row['year_first_flow'] <= end_year:
            is_intra = (u_name == v1_name)
            if G.has_edge(u_name, v1_name):
                G[u_name][v1_name]['weight'] += 1
            else:
                G.add_edge(u_name, v1_name, weight=1, type='within' if is_intra else 'inter')

        # Logic: First -> Current
        # Only add if locations differ (otherwise it's a "stay")
        if (start_year <= row['year_current_flow'] <= end_year) and (v1_name != v2_name):
            is_intra = (v1_name == v2_name)
            if G.has_edge(v1_name, v2_name):
                G[v1_name][v2_name]['weight'] += 1
            else:
                G.add_edge(v1_name, v2_name, weight=1, type='within' if is_intra else 'inter')
                
    return G
