import networkx as nx
import pandas as pd
from typing import Literal


df_location = "df_migration_steps.csv"
df_geo_cities_location = "df_geo_cities.csv"
df_geo_prefectures_location = "df_geo_prefectures.csv"

def create_directed_graph(granularity: Literal["county", "city", "prefecture"]) -> nx.DiGraph:
    """Simple Graph,

    Args:
        granularity (str): granularity level county, city, prefecture

    Returns:
        nx.DiGraph: directed graph object weighted by nummber of flows
    """
    if granularity not in ["county", "city", "prefecture"]:
        raise ValueError("granularity must be one of county, city, prefecture")

    df = pd.read_csv(df_location)
    df_geo_cities = pd.read_csv(df_geo_cities_location, index_col='code')
    df_geo_prefectures = pd.read_csv(df_geo_prefectures_location, index_col='code')
    if granularity == "city":
        df["from_code"] = df["from_code"][:4]
        df["to_code"] = df["to_code"][:4]
    elif granularity == "prefecture":
        df["from_code"] = df["from_code"][:2]
        df["to_code"] = df["to_code"][:2]

    G = nx.DiGraph()
    # dual index using from and to
    for _, row in df.iterrows():
        from_code = row["from_code"]
        to_code = row["to_code"]

        if from_code == to_code:
            continue

        if granularity == "city":
            from_lon = df_geo_cities.loc[int(from_code), "lon"]
            from_lat = df_geo_cities.loc[int(from_code), "lat"]
            to_lon = df_geo_cities.loc[int(to_code), "lon"]
            to_lat = df_geo_cities.loc[int(to_code), "lat"]
        elif granularity == "prefecture":
            from_lon = df_geo_prefectures.loc[int(from_code), "lon"]
            from_lat = df_geo_prefectures.loc[int(from_code), "lat"]
            to_lon = df_geo_prefectures.loc[int(to_code), "lon"]
            to_lat = df_geo_prefectures.loc[int(to_code), "lat"]
        else:
            from_lon = row["from_lon"]
            from_lat = row["from_lat"]
            to_lon = row["to_lon"]
            to_lat = row["to_lat"]
        
        
        
        if G.has_node(from_code) is False:
            G.add_node(from_code, lon=from_lon, lat=from_lat)
        if G.has_node(to_code) is False:
            G.add_node(to_code, lon=to_lon, lat=to_lat)
        if G.has_edge(from_code, to_code):
            G[from_code][to_code]["weight"] += 1
        else:
            G.add_edge(from_code, to_code, weight=1)

        
    return G
    
def create_undirected_graph(granularity: Literal["county", "city", "prefecture"]) -> nx.DiGraph:
    """Simple Graph,

    Args:
        granularity (str): granularity level county, city, prefecture

    Returns:
        nx.DiGraph: directed graph object weighted by nummber of flows
    """
    if granularity not in ["county", "city", "prefecture"]:
        raise ValueError("granularity must be one of county, city, prefecture")

    df = pd.read_csv(df_location)
    df_geo_cities = pd.read_csv(df_geo_cities_location, index_col='code')
    df_geo_prefectures = pd.read_csv(df_geo_prefectures_location, index_col='code')

    G = nx.DiGraph()
    # dual index using from and to
    for _, row in df.iterrows():
        if granularity == "city":
            from_code = row["from_code"][:4]
            to_code = row["to_code"][:4]

            if from_code == to_code:
                continue

            from_lon = df_geo_cities.loc[int(from_code), "lon"]
            from_lat = df_geo_cities.loc[int(from_code), "lat"]
            to_lon = df_geo_cities.loc[int(to_code), "lon"]
            to_lat = df_geo_cities.loc[int(to_code), "lat"]
        elif granularity == "prefecture":
            from_code = row["from_code"][:2]
            to_code = row["to_code"][:2]
            from_lon = df_geo_prefectures.loc[int(from_code), "lon"]
            from_lat = df_geo_prefectures.loc[int(from_code), "lat"]
            to_lon = df_geo_prefectures.loc[int(to_code), "lon"]
            to_lat = df_geo_prefectures.loc[int(to_code), "lat"]
        else:
            from_code = row["from_code"]
            to_code = row["to_code"]
            from_lon = row["from_lon"]
            from_lat = row["from_lat"]
            to_lon = row["to_lon"]
            to_lat = row["to_lat"]
        

        
        if G.has_node(from_code) is False:
            G.add_node(from_code, lon=from_lon, lat=from_lat)
        if G.has_node(to_code) is False:
            G.add_node(to_code, lon=to_lon, lat=to_lat)
        if G.has_edge(from_code, to_code):
            G[from_code][to_code]["weight"] += 1
            G[to_code][from_code]["weight"] += 1
        else:
            G.add_edge(from_code, to_code, weight=1)
            G.add_edge(to_code, from_code, weight=1)
    return G
