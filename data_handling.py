import os
import rasterio

def inspect_raster_metadata(file_path, display_name):
    """Reads basic raster attributes and estimates RAM usage."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found. Please check the file path.\n")
        return

    with rasterio.open(file_path) as src:
        # Basic raster attributes
        width = src.width
        height = src.height
        total_pixels = width * height
        num_bands = src.count
        dtype = src.dtypes[0]
        nodata = src.nodata
        crs = src.crs
        bounds = src.bounds
        res_x, res_y = src.res

        # Calculate uncompressed memory footprint in RAM
        # Reads only a single 1x1 pixel window to determine the data type's byte size
        itemsize = src.read(1, window=rasterio.windows.Window(0, 0, 1, 1)).itemsize
        estimated_ram_gb = (total_pixels * num_bands * itemsize) / (1024 ** 3)
        file_size_gb = os.path.getsize(file_path) / (1024 ** 3)

        # Print formatted summary
        print("=" * 60)
        print(f"{display_name} RASTER METADATA SUMMARY")
        print("=" * 60)
        print(f"File Name:             {os.path.basename(file_path)}")
        print(f"Coordinate System:     {crs}")
        print(f"Raster Dimensions:     {width:,} (W) x {height:,} (H)")
        print(f"Total Pixel Count:     {total_pixels:,} pixels")
        print(f"Number of Bands:       {num_bands}")
        print(f"Data Type:             {dtype}")
        print(f"NoData Value:          {nodata}")
        print(f"Spatial Resolution:    {res_x:.2f} m x {abs(res_y):.2f} m")
        print("-" * 60)
        print("SPATIAL EXTENT (BOUNDS)")
        print(f"  Left (Min X):        {bounds.left:,.2f}")
        print(f"  Bottom (Min Y):      {bounds.bottom:,.2f}")
        print(f"  Right (Max X):       {bounds.right:,.2f}")
        print(f"  Top (Max Y):         {bounds.top:,.2f}")
        print("-" * 60)
        print(f"Compressed File Size:  {file_size_gb:.2f} GB")
        print(f"Uncompressed RAM Need: ~{estimated_ram_gb:.2f} GB")
        print("=" * 60)
        print("\n")

# Define the datasets for Iteration 1 and Iteration 2
datasets = [
    {
        "path": "2026-01-22_Liu_Ning_66355v1/data/90m_EPSG3577/Relief_dems_3s_mosaic1.tif",
        "name": "ITERATION 1: CSIRO 90m ELEVATION"
    },
    {
        "path": "2026-08-18_Valavi_Roozbeh_65549v9/data/1.HABITAT_CONDITION/3yr/HCAS33_AHC_2022_2024.tif",
        "name": "ITERATION 2: CSIRO HCAS v3.3 CONDITION"
    }
]

# Run the inspection loop
for dataset in datasets:
    inspect_raster_metadata(dataset["path"], dataset["name"])