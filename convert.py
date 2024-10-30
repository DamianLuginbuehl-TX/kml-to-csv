import pandas as pd
import xml.etree.ElementTree as ET


def extract_coordinates_from_kml(file_path, output_csv):
    # Parse the KML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define namespaces to handle KML elements
    ns = {"kml": "http://www.opengis.net/kml/2.2"}

    # Prepare a list to store data
    data = []

    # Loop through each Placemark in the KML
    for placemark in root.findall(".//kml:Placemark", ns):
        # Extract the name of the location
        name = (
            placemark.find("kml:name", ns).text
            if placemark.find("kml:name", ns) is not None
            else ""
        )

        # Extract coordinates
        coordinates = placemark.find(".//kml:coordinates", ns)
        if coordinates is not None:
            lon, lat, *_ = coordinates.text.strip().split(",")
            data.append({"Name": name, "Latitude": lat, "Longitude": lon})

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Data extracted and saved to {output_csv}")


# Usage
file_path = "input.kml"  # Path to your KML file
output_csv = "output.csv"  # Path to save the CSV file
extract_coordinates_from_kml(file_path, output_csv)
