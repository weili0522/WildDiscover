"""Convert the Night Parrot suitability raster into classified GeoJSON."""

from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.features import shapes, sieve
from rasterio.transform import Affine
from shapely.geometry import shape


BASE_DIR = Path(__file__).parent

INPUT_RASTER = (
    BASE_DIR
    / "data"
    / "raw"
    / "habitat_suitability_maxent.tif"
)

OUTPUT_GEOJSON = (
    BASE_DIR
    / "data"
    / "processed"
    / "ghost_habitat_prediction.geojson"
)

# Minimum probability displayed on the map.
MINIMUM_SUITABILITY = 0.50

# Probability class boundaries.
CLASS_BREAKS = np.array(
    [0.50, 0.60, 0.70, 0.80, 0.90],
    dtype="float32",
)

# Representative value saved for each class.
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


def vectorize_raster():
    """Create classified habitat polygons from the probability raster."""

    OUTPUT_GEOJSON.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with rasterio.open(INPUT_RASTER) as src:
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

        classified = np.zeros(
            raster_values.shape,
            dtype="uint8",
        )

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
                    "species_id": "pilot-bird",
                    "species_name": "Night Parrot",
                    "suitability": CLASS_VALUES[class_id],
                }
            )

        if not polygon_records:
            raise RuntimeError(
                "No habitat polygons were produced."
            )

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

    habitat.to_file(
        OUTPUT_GEOJSON,
        driver="GeoJSON",
    )

    print(f"Polygon count: {len(habitat)}")
    print(f"Output CRS: {habitat.crs}")
    print(f"Saved to: {OUTPUT_GEOJSON}")
    print(
        "File size: "
        f"{OUTPUT_GEOJSON.stat().st_size / 1024 / 1024:.2f} MB"
    )

    print("\nFeatures by suitability class:")

    print(
        habitat["suitability"]
        .value_counts()
        .sort_index()
    )


if __name__ == "__main__":
    vectorize_raster()