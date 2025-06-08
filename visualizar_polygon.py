import matplotlib.pyplot as plt
import re

def parse_coordinate(coord_str):
    # Parse coordinates in format: DDMMSS.SS[N/S]DDDMMSS.SS[E/W]
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
    coordinates = []
    polygon_active = False
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('//') or line.startswith('/*'):
                continue
                
            # Detect start of polygon
            if line.startswith('Polygon'):
                polygon_active = True
                continue
                
            # If we're in a polygon section, try to parse coordinates
            if polygon_active:
                # Check if the line looks like a coordinate (vs. a property setting)
                if re.search(r'\d{6}\.\d{2}[NS]\d{7}\.\d{2}[EW]', line):
                    # Extract just the coordinate part (without comments)
                    coord_part = line.split('[')[0].strip()
                    coord = parse_coordinate(coord_part)
                    if coord:
                        coordinates.append(coord)
    
    return coordinates

def plot_polygon(coordinates):
    x, y = zip(*coordinates)
    
    plt.figure(figsize=(12, 10))
    plt.plot(x, y, 'b-', linewidth=2)
    plt.fill(x, y, alpha=0.2, color='lightblue')
    plt.title('CBAS FIR Boundary Polygon')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    
    # Add North arrow and scale
    plt.annotate('N', xy=(0.95, 0.95), xycoords='axes fraction',
                 fontsize=12, ha='center', va='center',
                 bbox=dict(boxstyle='circle', fc='white', ec='black'))
    plt.annotate('↑', xy=(0.95, 0.92), xycoords='axes fraction',
                 fontsize=16, ha='center', va='center')
    
    plt.savefig('cbas_polygon_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()

# Map file path
file_path = r"e:\repositorios\eana\indra-map\figuras\CBAS.map"
coordinates = read_map_file(file_path)
plot_polygon(coordinates)
print(f"Successfully visualized {len(coordinates)} coordinate points from CBAS.map")
print("Visualization saved as 'cbas_polygon_visualization.png'")
