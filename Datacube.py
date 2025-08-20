# Helper script to analyze your datacube structure
# Run this separately to understand your .pkl file structure

import pickle
import numpy as np
import pandas as pd

def analyze_datacube_structure(pkl_file_path):
    """
    Analyze the structure of your datacube to understand the data format
    """
    print("Loading datacube...")
    with open(pkl_file_path, 'rb') as f:
        datacube = pickle.load(f)
    
    print(f"Datacube type: {type(datacube)}")
    print(f"Number of items: {len(datacube)}")
    
    if isinstance(datacube, dict):
        # Analyze first few samples
        sample_keys = list(datacube.keys())[:5]
        print(f"\nSample keys: {sample_keys}")
        
        for key in sample_keys[:2]:  # Look at first 2 samples
            print(f"\n--- Sample {key} ---")
            sample = datacube[key]
            print(f"Sample type: {type(sample)}")
            
            if isinstance(sample, dict):
                print("Keys in sample:")
                for k, v in sample.items():
                    if isinstance(v, np.ndarray):
                        print(f"  {k}: numpy array, shape: {v.shape}, dtype: {v.dtype}")
                    else:
                        print(f"  {k}: {type(v)}, value: {v}")
            else:
                print(f"Sample content: {sample}")
    
    elif isinstance(datacube, list):
        print(f"First item type: {type(datacube[0])}")
        if len(datacube) > 0:
            print(f"First item: {datacube[0]}")
    
    return datacube

def create_custom_extractor(datacube_sample):
    """
    Based on your datacube structure, create a custom metadata extractor
    """
    print("\n=== Custom Extractor Function ===")
    print("Based on your datacube structure, here's a custom extractor:")
    
    print("""
def extract_spatial_metadata_custom(datacube):
    metadata = []
    
    for key, data in datacube.items():
        try:
            # Adjust these field names based on your actual structure
            entry = {
                'sample_id': key,
                'pm25_value': data['your_pm25_field_name'],  # Replace with actual field
                'green_index': data['your_green_index_field'],  # Replace with actual field
                'urban_index': data['your_urban_index_field'],  # Replace with actual field
                'latitude': data.get('lat', data.get('latitude', np.nan)),
                'longitude': data.get('lon', data.get('longitude', np.nan)),
                'date': data.get('date', data.get('timestamp', None)),
                'image_shape': data['image'].shape if 'image' in data else None
            }
            metadata.append(entry)
        except Exception as e:
            print(f"Error processing {key}: {e}")
            continue
    
    return pd.DataFrame(metadata)
    """)

if __name__ == "__main__":
    # Usage
    pkl_file = "D:\Database\Transfer_Learning_Datacube.pkl"  # Replace with your file path
    
    try:
        datacube = analyze_datacube_structure(pkl_file)
        
        # Get a sample for analysis
        if isinstance(datacube, dict) and len(datacube) > 0:
            sample_key = list(datacube.keys())[0]
            sample = datacube[sample_key]
            create_custom_extractor(sample)
        
    except FileNotFoundError:
        print(f"File not found: {pkl_file}")
        print("Please update the file path to your actual .pkl file location")
    except Exception as e:
        print(f"Error analyzing datacube: {e}")