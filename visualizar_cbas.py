import matplotlib.pyplot as plt
import re
import os

def parse_coordinate(coord_str):
    """Parse coordinates in format: DDMMSS.SS[N/S]DDDMMSS.SS[E/W]"""
    # Remove any comments in square brackets
    coord_str = coord_str.split('[')[0].strip()
    
    # Parse latitude and longitude parts
    lat_pattern = r"(\d{2})(\d{2})(\d{2}\.\d{2})([NS])"
    lon_pattern = r"(\d{3})(\d{2})(\d{2}\.\d{2})([EW])"
    
    lat_match = re.search(lat_pattern, coord_str)
    lon_match = re.search(lon_pattern, coord_str)
    
    if lat_match and lon_match:
        lat_deg, lat_min, lat_sec, lat_dir = lat_match.groups()
        lon_deg, lon_min, lon_sec, lon_dir = lon_match.groups()
        
        lat = float(lat_deg) + float(lat_min)/60 + float(lat_sec)/3600
        if lat_dir == 'S':
            lat = -lat
            
        lon = float(lon_deg) + float(lon_min)/60 + float(lon_sec)/3600
        if lon_dir == 'W':
            lon = -lon
            
        return lon, lat  # Note: x=longitude, y=latitude for plotting
    return None

def read_map_file(file_path):
    """Read coordinates from a MAP file and return them as a list of (lon, lat) tuples"""
    coordinates = []
    polygon_active = False
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('//') or (line.startswith('/*') and not polygon_active):
                continue
            
            # End of comment block
            if line.endswith('*/') and not polygon_active:
                continue
                
            # Detect start of polygon
            if line.startswith('Polygon'):
                polygon_active = True
                continue
                
            # If we're in a polygon section, try to parse coordinates
            if polygon_active:
                # Check if the line looks like a coordinate (vs. a property setting)
                if re.search(r'\d{6}\.\d{2}[NS]\d{7}\.\d{2}[EW]', line):
                    coord = parse_coordinate(line)
                    if coord:
                        coordinates.append(coord)
    
    return coordinates

def plot_polygon(coordinates, title="FIR Boundary Polygon"):
    """Plot the polygon defined by the given coordinates"""
    if not coordinates:
        print("Error: No valid coordinates found")
        return
    
    x, y = zip(*coordinates)
    
    plt.figure(figsize=(12, 10))
    plt.plot(x, y, 'b-', linewidth=1.5)
    plt.fill(x, y, 'b', alpha=0.2)
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.axis('equal')
    
    # Add some key coordinates as points with labels
    for i in range(0, len(coordinates), max(1, len(coordinates) // 20)):  # Show ~20 points
        plt.plot(coordinates[i][0], coordinates[i][1], 'ro', markersize=5)
        plt.text(coordinates[i][0], coordinates[i][1], f'  Point {i+1}', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('cbas_polygon_visualization.png', dpi=300)
    plt.show()

def main():
    # File path to your MAP file
    file_path = r"e:\repositorios\eana\indra-map\figuras\CBAS.map"
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return
    
    print(f"Reading coordinates from {file_path}...")
    coordinates = read_map_file(file_path)
    
    if not coordinates:
        print("No valid coordinates found in the file.")
        return
    
    print(f"Found {len(coordinates)} valid coordinates.")
    plot_polygon(coordinates, title=f"CBAS FIR Boundary Polygon ({len(coordinates)} points)")
    print(f"Visualization saved as 'cbas_polygon_visualization.png'")

if __name__ == "__main__":
    main()
