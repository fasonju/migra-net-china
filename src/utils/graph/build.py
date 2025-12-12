import pandas as pd
import networkx as nx

from utils.graph.graph import EdgeAttributes, EducationLevel, Gender, NodeAttributes


def build_granular_graph(df: pd.DataFrame) -> nx.Graph:
    """
    Build a detailed migration graph from the DataFrame.
    Most granular version so for each flow there is an edge with full attributes.
    """
    def fill_missing_nodes(G: nx.Graph, row: pd.Series):
        # hometown to first flow
        hometown_code = row['hometown_code']
        first_flow_code = row['first_flow_code']
        current_code = row['current_code']

        if not G.has_node(hometown_code):
            hometown_province_code = row['hometown_province_code']
            hometown_city_code = row['hometown_city_code']
            hometown_county_code = row['hometown_county_code']
            hometown_longitude = row['hometown_lon']
            hometown_latitude = row['hometown_lat']
            hometown_node_attributes = NodeAttributes(
                location_code=hometown_code,
                province_code=hometown_province_code,
                city_code=hometown_city_code,
                county_code=hometown_county_code,
                longitude=hometown_longitude,
                latitude=hometown_latitude
            )

            G.add_node(hometown_code, attributes=hometown_node_attributes)

        if not G.has_node(first_flow_code):
            first_flow_province_code = row['first_flow_province_code']
            first_flow_city_code = row['first_flow_city_code']
            first_flow_county_code = row['first_flow_county_code']
            first_flow_longitude = row['first_lon']
            first_flow_latitude = row['first_lat']
            first_flow_node_attributes = NodeAttributes(
                location_code=first_flow_code,
                province_code=first_flow_province_code,
                city_code=first_flow_city_code,
                county_code=first_flow_county_code,
                longitude=first_flow_longitude,
                latitude=first_flow_latitude
            )

            G.add_node(first_flow_code, attributes=first_flow_node_attributes)

        if not G.has_node(current_code):
            current_province_code = row['current_province_code']
            current_city_code = row['current_city_code']
            current_county_code = row['current_county_code']
            current_longitude = row['current_lon']
            current_latitude = row['current_lat']
            current_node_attributes = NodeAttributes(
                location_code=current_code,
                province_code=current_province_code,
                city_code=current_city_code,
                county_code=current_county_code,
                longitude=current_longitude,
                latitude=current_latitude
            )

            G.add_node(current_code, attributes=current_node_attributes)

            
    G = nx.MultiDiGraph()

    for index , row in df.iterrows():
        hometown_code = row['hometown_code']
        first_flow_code = row['first_flow_code']
        current_code = row['current_code']
        fill_missing_nodes(G, row)

        year_first_flow = row['year_first_flow']
        month_first_flow = row['month_first_flow']
        year_current_flow = row['year_current_flow']
        month_current_flow = row['month_current_flow']
        education_level = EducationLevel(row['edu_level'])
        gender = Gender(row['gender'])
        average_family_cost_per_month = row['average_family_cost_per_month']
        average_family_income_per_month = row['average_family_income_per_month']
        num_flows_total = row['num_flows_total']
        if_stay = row['if_stay']
        changed_household = row['if_change_household_local']
        stay_duration_months = row['how_long_to_stay']


        # add edges
        edge_attributes_1 = EdgeAttributes(
            from_node=hometown_code,
            to_node=first_flow_code,
            year = year_first_flow,
            month = month_first_flow,
            education_level=education_level,
            gender=gender,
            average_family_cost_per_month=average_family_cost_per_month,
            average_family_income_per_month=average_family_income_per_month,
            total_flows=num_flows_total,
            stay_at_destination=if_stay,
            changed_household=changed_household,
            stay_duration_months=stay_duration_months,
            flow_index=index,
            from_node_attrs=G.nodes[hometown_code]['attributes'],
            to_node_attrs=G.nodes[first_flow_code]['attributes']
        )

        G.add_edge(hometown_code, first_flow_code, attributes=edge_attributes_1)

        edge_attributes_2 = EdgeAttributes(
            from_node=first_flow_code,
            to_node=current_code,
            year = year_current_flow,
            month = month_current_flow,
            education_level=education_level,
            gender=gender,
            average_family_cost_per_month=average_family_cost_per_month,
            average_family_income_per_month=average_family_income_per_month,
            total_flows=num_flows_total,
            stay_at_destination=if_stay,
            changed_household=changed_household,
            stay_duration_months=stay_duration_months,
            flow_index=index,
            from_node_attrs=G.nodes[first_flow_code]['attributes'],
            to_node_attrs=G.nodes[current_code]['attributes']
        )

        G.add_edge(first_flow_code, current_code, attributes=edge_attributes_2)
    return G


# Build network with geographic data full data from all datapoints. Only used for plotting
def build_geo_network(df: pd.DataFrame, start_year: int, end_year: int) -> nx.DiGraph:
    G = nx.DiGraph()
    
    # Helper to get node ID and Coords
    def get_node_info(row, prefix) -> tuple[str, tuple[float, float]]:
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

def build_migration_network_for_year(df: pd.DataFrame, year: int) -> nx.DiGraph:
    """
    Build directed migration network for a specific year.
    
    Parameters:
    -----------
    df : DataFrame
        Migration data
    year : int
        Year to analyze
        either year_first_flow or year_current_flow matches this year.
    
    Returns:
    --------
    G : nx.DiGraph
        Network with nodes (cities) and edges (migration flows)
    """
    G = nx.DiGraph()
    
    # Filter data for the year
    year_data = df[
        ((df['year_first_flow'] == year) | (df['year_current_flow'] == year))
    ]

    
    for _, row in year_data.iterrows():
        # Extract city names and coordinates
        hometown = row['hometown_Name_Prefecture']
        first_city = row['first_Name_Prefecture']
        current_city = row['current_city']
        
        hometown_pos = (row['hometown_lon'], row['hometown_lat'])
        first_pos = (row['first_lon'], row['first_lat'])
        current_pos = (row['current_lon'], row['current_lat'])
        
        # Add nodes with positions
        G.add_node(hometown, pos=hometown_pos, 
                  lon=row['hometown_lon'], lat=row['hometown_lat'])
        G.add_node(first_city, pos=first_pos,
                  lon=row['first_lon'], lat=row['first_lat'])
        G.add_node(current_city, pos=current_pos,
                  lon=row['current_lon'], lat=row['current_lat'])
        
        # Add edges for flows in this year
        if row['year_first_flow'] == year and hometown != first_city:
            if G.has_edge(hometown, first_city):
                G[hometown][first_city]['weight'] += 1
            else:
                G.add_edge(hometown, first_city, weight=1)
        
        if row['year_current_flow'] == year and first_city != current_city:
            if G.has_edge(first_city, current_city):
                G[first_city][current_city]['weight'] += 1
            else:
                G.add_edge(first_city, current_city, weight=1)
    
    # Remove isolated nodes
    G.remove_nodes_from(list(nx.isolates(G)))
    
    return G
