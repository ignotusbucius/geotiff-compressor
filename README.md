# GeoTIFF Compressor

A Python application for compressing GeoTIFF files using optimal GDAL compression techniques.

## ✨ Features

- **Smart Compression**: Uses Cloud Optimized GeoTIFF (COG) format with JPEG compression
- **User-Friendly Interface**: Windows Explorer integration for easy file selection
- **Batch Processing**: Compress multiple files simultaneously
- **Optimal Settings**: JPEG compression with YCBCR color space for maximum efficiency
- **Preserves Geospatial Data**: Maintains all projection and coordinate information
- **Safe Operation**: Never modifies original files

## 🎯 Use Cases

Perfect for:
- Aerial and satellite imagery
- Orthophotos from QGIS georeferencing
- Large visual datasets requiring storage optimization
- Web mapping applications requiring fast loading

⚠️ **Not suitable for**: Elevation data, scientific measurements, or any data requiring lossless compression.

## 📋 Requirements

- **Python 3.x** with tkinter (usually included)
- **GDAL library** with command-line tools
- **Windows OS** (for Explorer integration)

## 🔧 Installation

### 1. Install GDAL

**Option A: Official GDAL**
- Download from [gdal.org](https://gdal.org/download.html)
- Add GDAL tools to your system PATH

**Option B: OSGeo4W (Recommended)**
- Download [OSGeo4W installer](https://trac.osgeo.org/osgeo4w/)
- Install with GDAL package

### 2. Verify Installation

Open command prompt and verify GDAL is working:
```bash
gdal_translate --version
```

You should see version information displayed.

## 🚀 Usage

### Quick Start
1. **Double-click** `run.bat`, or
2. **Command line**: `python geotiff_compressor.py`

### Workflow
1. 📁 **File Selection**: Windows Explorer opens automatically
2. ✅ **Confirmation**: Review selected GeoTIFF files
3. 📂 **Output Location**: Choose same directory (recommended) or new location
4. ⚡ **Processing**: Files compressed with `compressed-` prefix
5. ✨ **Complete**: Compressed files ready for use

## ⚙️ Compression Specifications

| Setting | Value |
|---------|--------|
| **Format** | Cloud Optimized GeoTIFF (COG) |
| **Compression** | JPEG |
| **Quality** | 75% |
| **Color Space** | YCBCR |
| **Tiling** | Internal |
| **Fallback** | Traditional GeoTIFF + JPEG |

### Expected Results
- **Size Reduction**: 70-95% smaller files
- **Quality**: Excellent for visual imagery
- **Compatibility**: Works with all GIS software
- **Performance**: Faster loading in web applications

## 📁 File Structure

```
geotiff-compressor/
├── geotiff_compressor.py    # Main application
├── run.bat                  # Windows launcher
├── README.md               # This file
└── sample.tif              # Test file
```

## 🔍 Technical Details

### Primary Compression Command
```bash
gdal_translate -of COG -co COMPRESS=JPEG -co QUALITY=75 input.tif compressed-input.tif
```

### Fallback Command (Legacy GDAL)
```bash
gdal_translate -b 1 -b 2 -b 3 -co COMPRESS=JPEG -co JPEG_QUALITY=75 -co PHOTOMETRIC=YCBCR -co TILED=YES input.tif compressed-input.tif
```

## 📝 Notes

- Original files are **never modified**
- All geospatial information is **preserved**
- Processing time varies with file size
- Best results on RGB imagery
- Requires sufficient disk space for output files

## 🤝 Contributing

This project uses GDAL's proven compression techniques optimized for GIS workflows. For issues or suggestions, please open a GitHub issue.

## 📄 License

Open source - feel free to use and modify for your GIS projects.