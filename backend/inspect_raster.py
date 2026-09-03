from pathlib import Path

import numpy as np
import rasterio


RASTER_PATH = (
    Path(__file__).parent
    / "data"
    / "raw"
    / "habitat_suitability_maxent.tif"
)


with rasterio.open(RASTER_PATH) as src:
    print(f"File: {RASTER_PATH}")
    print(f"CRS: {src.crs}")
    print(f"Size: {src.width} x {src.height}")
    print(f"Band count: {src.count}")
    print(f"Data type: {src.dtypes}")
    print(f"NoData: {src.nodata}")
    print(f"Bounds: {src.bounds}")
    print(f"Transform: {src.transform}")
    print(f"Band descriptions: {src.descriptions}")

    preview_width = min(src.width, 2000)
    preview_height = min(src.height, 2000)

    sample = src.read(
        1,
        out_shape=(preview_height, preview_width),
        masked=True
    )

    values = sample.compressed()
    values = values[np.isfinite(values)]

    print(f"Sampled valid pixels: {values.size}")

    if values.size:
        print(f"Sample minimum: {values.min()}")
        print(f"Sample maximum: {values.max()}")
        print(f"Sample mean: {values.mean()}")

        for percentile in (50, 90, 95, 97.5, 99):
            value = np.percentile(values, percentile)
            print(f"{percentile}th percentile: {value}")