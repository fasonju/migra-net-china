library(dplyr)
library(sf)
library(lwgeom)

# Check if data exists in environment
if (!exists("df") || !exists("df_geo")) {
  stop("Please make sure 'df' and 'df_geo' are loaded in your R environment.")
}

message("1. Processing Geography (Calculating Centroids)...")

# --- Step A: Prepare Geo Data ---
# 1. Clean up names and handle geometries
df_geo_clean <- df_geo %>%
  mutate(Name_Perfecture = ifelse(is.na(Name_Perfecture), 
                                  Name_Province, 
                                  Name_Perfecture)) %>%
  st_make_valid() %>%
  mutate(
    # Create the text key used for Current Place matching
    pc_key = paste0(Name_Province, "_", Name_Perfecture, "_", Name_County),
    # Ensure code is character for matching
    Code_County_char = as.character(Code_County)
  )

# 2. Calculate Centroids (Lat/Lon)
# We convert polygons to points to get X (Longitude) and Y (Latitude)
df_centroids <- df_geo_clean %>%
  mutate(centroid = st_centroid(geometry)) %>%
  mutate(
    geo_lon = st_coordinates(centroid)[, 1], # X
    geo_lat = st_coordinates(centroid)[, 2]  # Y
  ) %>%
  st_drop_geometry() # Remove heavy polygon shapes, keep only data + points

# 3. Create Lookup Tables
# Lookup for Codes (Hometown & First Flow)
lookup_by_code <- df_centroids %>%
  select(Code_County_char, geo_lon, geo_lat) %>%
  distinct()

# Lookup for Names (Current Place)
lookup_by_name <- df_centroids %>%
  select(pc_key, geo_lon, geo_lat) %>%
  distinct()


message("2. Merging Coordinates into Migration Data...")

# --- Step B: Process Migration Data ---
df_export <- df %>%
  mutate(
    # Ensure keys match the lookup tables
    hometown_code_char = as.character(hometown_code),
    first_flow_code_char = as.character(first_flow_code),
    pc_key = paste0(current_province, "_", current_city, "_", current_county)
  ) %>%
  
  # 1. Attach Hometown Coordinates
  left_join(lookup_by_code, by = c("hometown_code_char" = "Code_County_char")) %>%
  rename(hometown_lon = geo_lon, hometown_lat = geo_lat) %>%
  
  # 2. Attach First Flow Coordinates
  left_join(lookup_by_code, by = c("first_flow_code_char" = "Code_County_char")) %>%
  rename(first_lon = geo_lon, first_lat = geo_lat) %>%
  
  # 3. Attach Current Place Coordinates
  left_join(lookup_by_name, by = "pc_key") %>%
  rename(current_lon = geo_lon, current_lat = geo_lat)


message("3. Saving to CSV...")

# Write to CSV
write.csv(df_export, "full_migration_data_with_coords.csv", row.names = FALSE)

message("Done! Saved as 'full_migration_data_with_coords.csv'")