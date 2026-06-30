"""Manifest of the 33 chapters + front matter pages of the UN Handbook.

Each entry: (chapter_id, slug.html, section, human title).
chapter_id is the slug without extension and is used as the citation key.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    chapter_id: str
    filename: str
    section: str
    title: str
    is_chapter: bool  # True for the 33 numbered chapters, False for front matter


PAGES: list[Page] = [
    # ---- Front matter ----
    Page("index", "index.html", "Front matter", "Welcome", False),
    Page("introduction", "introduction.html", "Front matter", "Introduction", False),
    Page("about", "about.html", "Front matter", "About the Authors", False),
    Page("howto", "howto.html", "Front matter", "How to Use the Handbook", False),
    # ---- Foundations (Ch 1-11) ----
    Page("th_remote_sensing", "th_remote_sensing.html", "Foundations", "Remote Sensing Satellites Overview", True),
    Page("th_data_sources", "th_data_sources.html", "Foundations", "Big Earth Observation Data Cloud Services", True),
    Page("th_data_cubes", "th_data_cubes.html", "Foundations", "Earth Observation Data Cubes", True),
    Page("th_lucc", "th_lucc.html", "Foundations", "Land Cover and Crop Classification Schemas", True),
    Page("th_quality_control", "th_quality_control.html", "Foundations", "Quality Control of Training Data", True),
    Page("th_machine_learning", "th_machine_learning.html", "Foundations", "Machine Learning Algorithms", True),
    Page("th_uncertainty", "th_uncertainty.html", "Foundations", "Spatial Map Uncertainty Estimation", True),
    Page("th_validation", "th_validation.html", "Foundations", "Map Validation and Area Estimation", True),
    Page("th_design_frames", "th_design_frames.html", "Foundations", "Sampling Frames Design", True),
    Page("th_alignment", "th_alignment.html", "Foundations", "Field Data Collection Alignment", True),
    Page("th_parcel_extraction", "th_parcel_extraction.html", "Foundations", "Semantic Segmentation for Field Boundaries", True),
    # ---- Crop Type Mapping (Ch 12-17) ----
    Page("ct_poland", "ct_poland.html", "Crop Type Mapping", "Poland Monitoring Case Study", True),
    Page("ct_mexico", "ct_mexico.html", "Crop Type Mapping", "Mexico Classification", True),
    Page("ct_zimbabwe", "ct_zimbabwe.html", "Crop Type Mapping", "Zimbabwe Classification", True),
    Page("ct_china", "ct_china.html", "Crop Type Mapping", "Paddy Rice Classification", True),
    Page("ct_chile", "ct_chile.html", "Crop Type Mapping", "Chile Land Use Mapping", True),
    Page("ct_digital_earth_africa", "ct_digital_earth_africa.html", "Crop Type Mapping", "Digital Earth Africa Program", True),
    # ---- Crop Yield Estimation (Ch 18-22) ----
    Page("cy_finland", "cy_finland.html", "Crop Yield Estimation", "Early-Season Yield Mapping", True),
    Page("cy_indonesia", "cy_indonesia.html", "Crop Yield Estimation", "Crop Phenology Mapping", True),
    Page("cy_colombia", "cy_colombia.html", "Crop Yield Estimation", "Rice Phenology Mapping", True),
    Page("cy_poland", "cy_poland.html", "Crop Yield Estimation", "Yield Forecasting", True),
    Page("cy_china", "cy_china.html", "Crop Yield Estimation", "Soybean Yield Simulation", True),
    # ---- Crop Statistics Extraction (Ch 23-26) ----
    Page("crop_statistics_area", "crop_statistics_area.html", "Crop Statistics Extraction", "Weighted Area Estimators", True),
    Page("crop_statistics_regression", "crop_statistics_regression.html", "Crop Statistics Extraction", "Survey-Calibrated Mapping", True),
    Page("crop_statistics_calibration", "crop_statistics_calibration.html", "Crop Statistics Extraction", "List Frame Data Estimation", True),
    Page("crop_statistics_ppi", "crop_statistics_ppi.html", "Crop Statistics Extraction", "Prediction-Powered Inference", True),
    # ---- UAV Applications (Ch 27-30) ----
    Page("uav_field_parcels", "uav_field_parcels.html", "UAV Applications", "Field Parcel Identification", True),
    Page("uav_wheat_growth", "uav_wheat_growth.html", "UAV Applications", "Wheat Growth Monitoring", True),
    Page("uav_crop_growth", "uav_crop_growth.html", "UAV Applications", "Crop Growth Index Automation", True),
    Page("uav_agriculture_cook_islands", "uav_agriculture_cook_islands.html", "UAV Applications", "Cook Islands Integration", True),
    # ---- Agricultural Disaster Response (Ch 31) ----
    Page("dis_china_floods", "dis_china_floods.html", "Agricultural Disaster Response", "Automated Flood Detection", True),
    # ---- Additional Topics (Ch 32-33) ----
    Page("ad_world_cereal", "ad_world_cereal.html", "Additional Topics", "WorldCereal Global Initiative", True),
    Page("ad_learning", "ad_learning.html", "Additional Topics", "Training Resources", True),
]

assert sum(1 for p in PAGES if p.is_chapter) == 33, "expected 33 chapters"
