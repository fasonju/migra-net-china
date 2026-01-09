import networkx as nx
import pandas as pd
from typing import Literal


df_location = "df_migration_steps.csv"
df_geo_prefectures_location = "df_geo_prefectures.csv"
df_geo_provinces_location = "df_geo_provinces.csv"

def create_directed_graph(granularity: Literal["county", "prefecture", "province"]) -> nx.DiGraph:
    """Simple Graph,

    Args:
        granularity (str): granularity level county, prefecture, province

    Returns:
        nx.DiGraph: directed graph object weighted by nummber of flows
    """
    if granularity not in ["county", "prefecture", "province"]:
        raise ValueError("granularity must be one of county, prefecture, province")

    df = pd.read_csv(df_location)
    df_geo_prefectures = pd.read_csv(df_geo_prefectures_location, index_col='code')
    df_geo_provinces = pd.read_csv(df_geo_provinces_location, index_col='code')
    # keep only the first 4 digits for prefecture level, first 2 digits for province level
    if granularity == "prefecture":
        df["from_code"] = df["from_code"].astype(str).str[:4]
        df["to_code"] = df["to_code"].astype(str).str[:4]
    elif granularity == "province":
        df["from_code"] = df["from_code"].astype(str).str[:2]
        df["to_code"] = df["to_code"].astype(str).str[:2]

    G = nx.DiGraph()
    # dual index using from and to
    for _, row in df.iterrows():
        from_code = row["from_code"]
        to_code = row["to_code"]
        print(from_code, to_code)

        if from_code == to_code:
            continue

        if granularity == "prefecture":
            from_lon = df_geo_prefectures.loc[int(from_code), "lon"]
            from_lat = df_geo_prefectures.loc[int(from_code), "lat"]
            to_lon = df_geo_prefectures.loc[int(to_code), "lon"]
            to_lat = df_geo_prefectures.loc[int(to_code), "lat"]
        elif granularity == "province":
            from_lon = df_geo_provinces.loc[int(from_code), "lon"]
            from_lat = df_geo_provinces.loc[int(from_code), "lat"]
            to_lon = df_geo_provinces.loc[int(to_code), "lon"]
            to_lat = df_geo_provinces.loc[int(to_code), "lat"]
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
    
def create_undirected_graph(granularity: Literal["county", "prefecture", "province"]) -> nx.Graph:
    """Simple Graph,

    Args:
        granularity (str): granularity level county, prefecture, province

    Returns:
        nx.DiGraph: directed graph object weighted by nummber of flows
    """
    if granularity not in ["county", "prefecture", "province"]:
        raise ValueError("granularity must be one of county, prefecture, province")

    df = pd.read_csv(df_location)
    df_geo_prefectures = pd.read_csv(df_geo_prefectures_location, index_col='code')
    df_geo_provinces = pd.read_csv(df_geo_provinces_location, index_col='code')

    G = nx.Graph()
    # dual index using from and to
    for _, row in df.iterrows():
        if granularity == "prefecture":
            from_code = row["from_code"][:4]
            to_code = row["to_code"][:4]

            if from_code == to_code:
                continue

            from_lon = df_geo_prefectures.loc[int(from_code), "lon"]
            from_lat = df_geo_prefectures.loc[int(from_code), "lat"]
            to_lon = df_geo_prefectures.loc[int(to_code), "lon"]
            to_lat = df_geo_prefectures.loc[int(to_code), "lat"]
        elif granularity == "province":
            from_code = row["from_code"][:2]
            to_code = row["to_code"][:2]
            from_lon = df_geo_provinces.loc[int(from_code), "lon"]
            from_lat = df_geo_provinces.loc[int(from_code), "lat"]
            to_lon = df_geo_provinces.loc[int(to_code), "lon"]
            to_lat = df_geo_provinces.loc[int(to_code), "lat"]
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
        else:
            G.add_edge(from_code, to_code, weight=1)
            G.add_edge(to_code, from_code, weight=1)
    return G
