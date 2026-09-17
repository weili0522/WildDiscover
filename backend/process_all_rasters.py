"""Convert multiple species suitability rasters into classified GeoJSON."""

from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.features import shapes, sieve
from rasterio.transform import Affine
from shapely.geometry import shape

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

MINIMUM_SUITABILITY = 0.50
CLASS_BREAKS = np.array([0.50, 0.60, 0.70, 0.80, 0.90], dtype="float32")
CLASS_VALUES = {
    1: 0.55,
    2: 0.65,
    3: 0.75,
    4: 0.85,
    5: 0.95,
}

DOWNSAMPLE_FACTOR = 30
MIN_REGION_PIXELS = 12
SIMPLIFY_TOLERANCE_METRES = 1500

SPECIES_MAP = {
    "amytornis_purnelli": {"id": "dusky-grasswren", "name": "Dusky Grasswren"},
    "atrichornis_rufescens": {"id": "rufous-scrub-bird", "name": "Rufous Scrub-bird"},
    "leipoa_ocellata": {"id": "malleefowl", "name": "Malleefowl"},
    "pedionomus_torquatus": {"id": "plains-wanderer", "name": "Plains-wanderer"},
    "pezoporus_occidentalis": {"id": "night-parrot", "name": "Night Parrot"},
    "polytelis_alexandrae": {"id": "princess-parrot", "name": "Princess Parrot"}
}

def vectorize_raster(input_raster, output_geojson, species_id, species_name):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing {input_raster.name}...")

    with rasterio.open(input_raster) as src:
        output_height = src.height // DOWNSAMPLE_FACTOR
        output_width = src.width // DOWNSAMPLE_FACTOR

        suitability = src.read(
            1,
            out_shape=(output_height, output_width),
            masked=True,
            resampling=Resampling.bilinear,
        )

        scaled_transform = src.transform * Affine.scale(
            src.width / output_width,
            src.height / output_height,
        )

        raster_values = suitability.filled(np.nan)

        valid_pixels = (
            ~np.ma.getmaskarray(suitability)
            & np.isfinite(raster_values)
        )

        selected_pixels = (
            valid_pixels
            & (raster_values >= MINIMUM_SUITABILITY)
        )

        classified = np.zeros(raster_values.shape, dtype="uint8")

        classified[selected_pixels] = np.digitize(
            raster_values[selected_pixels],
            CLASS_BREAKS,
            right=False,
        )

        classified = sieve(
            classified,
            size=MIN_REGION_PIXELS,
            mask=selected_pixels,
            connectivity=8,
        )

        polygon_records = []

        for geometry, class_id in shapes(
            classified,
            mask=classified > 0,
            transform=scaled_transform,
            connectivity=8,
        ):
            class_id = int(class_id)
            if class_id not in CLASS_VALUES:
                continue

            polygon_records.append(
                {
                    "geometry": shape(geometry),
                    "species_id": species_id,
                    "species_name": species_name,
                    "suitability": CLASS_VALUES[class_id],
                }
            )

        if not polygon_records:
            print(f"No habitat polygons produced for {species_id}.")
            return

        habitat = gpd.GeoDataFrame(
            polygon_records,
            geometry="geometry",
            crs=src.crs,
        )

    habitat["geometry"] = habitat.geometry.simplify(
        SIMPLIFY_TOLERANCE_METRES,
        preserve_topology=True,
    )

    habitat = habitat[
        habitat.geometry.notna()
        & ~habitat.geometry.is_empty
        & (habitat.geometry.geom_type == "Polygon")
    ].copy()

    habitat = habitat.to_crs("EPSG:4326")

    habitat.to_file(output_geojson, driver="GeoJSON")

    print(f"Saved {species_id} to {output_geojson.name}")


def main():
    for prefix, info in SPECIES_MAP.items():
        input_raster = RAW_DIR / f"{prefix}_suitability.tif"
        output_geojson = PROCESSED_DIR / f"{info['id']}.geojson"
        
        if input_raster.exists():
            vectorize_raster(input_raster, output_geojson, info["id"], info["name"])
        else:
            print(f"File not found: {input_raster}")

if __name__ == "__main__":
    main()
