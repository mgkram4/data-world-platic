import numpy as np
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

def get_overpass_data(lat, lon, radius):
    """
    Fetch detailed land use data from Overpass API.
    """
    overpass_query = f"""
    [out:json];
    (
        way["landuse"](around:{radius},{lat},{lon});
        way["leisure"](around:{radius},{lat},{lon});
        way["natural"](around:{radius},{lat},{lon});
        way["building"](around:{radius},{lat},{lon});
        way["amenity"](around:{radius},{lat},{lon});
    );
    out body geom;
    """
    
    response = requests.get(
        "https://overpass-api.de/api/interpreter",
        params={'data': overpass_query},
        timeout=30
    )
    response.raise_for_status()
    return response.json()

def get_marine_plastic_data(lat, lon, radius, coastal_distance):
    """
    Enhanced marine plastic data retrieval with realistic concentration ranges based on location.
    """
    # Base concentrations (particles/m³) for different regions
    developed_high = {'base': 15, 'std': 2}  # High-activity ports in developed countries
    developed_low = {'base': 8, 'std': 1.5}  # Less active areas in developed countries
    developing_high = {'base': 25, 'std': 3}  # High-activity ports in developing countries
    developing_low = {'base': 12, 'std': 2}  # Less active areas in developing countries

    # Define regions for different concentration patterns
    developed_regions = {
        # North America
        'san_francisco': {'lat': 37.7749, 'lon': -122.4194, 'profile': developed_high},
        'vancouver': {'lat': 49.2827, 'lon': -123.1207, 'profile': developed_low},
        'miami': {'lat': 25.7617, 'lon': -80.1918, 'profile': developed_high},
        
        # Europe
        'rotterdam': {'lat': 51.9225, 'lon': 4.4792, 'profile': developed_high},
        'barcelona': {'lat': 41.3851, 'lon': 2.1734, 'profile': developed_high},
        'marseille': {'lat': 43.2965, 'lon': 5.3698, 'profile': developed_high},
        
        # Asia-Pacific
        'tokyo': {'lat': 35.6762, 'lon': 139.6503, 'profile': developed_high},
        'singapore': {'lat': 1.3521, 'lon': 103.8198, 'profile': developed_high},
        'sydney': {'lat': -33.8688, 'lon': 151.2093, 'profile': developed_low}
    }

    developing_regions = {
        # Asia
        'mumbai': {'lat': 19.0760, 'lon': 72.8777, 'profile': developing_high},
        'manila': {'lat': 14.5995, 'lon': 120.9842, 'profile': developing_high},
        'jakarta': {'lat': -6.2088, 'lon': 106.8456, 'profile': developing_high},
        
        # Africa
        'lagos': {'lat': 6.5244, 'lon': 3.3792, 'profile': developing_high},
        'alexandria': {'lat': 31.2001, 'lon': 29.9187, 'profile': developing_high},
        'casablanca': {'lat': 33.5731, 'lon': -7.5898, 'profile': developing_low},
        
        # South America
        'rio': {'lat': -22.9068, 'lon': -43.1729, 'profile': developing_high},
        'lima': {'lat': -12.0464, 'lon': -77.0428, 'profile': developing_high}
    }

    # Find nearest region and its profile
    def find_nearest_profile(lat, lon, regions):
        min_dist = float('inf')
        nearest_profile = None
        
        for region in regions.values():
            dist = ((region['lat'] - lat) ** 2 + (region['lon'] - lon) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                nearest_profile = region['profile']
        
        return nearest_profile

    # Get the appropriate concentration profile
    profile = find_nearest_profile(lat, lon, developed_regions)
    if not profile:
        profile = find_nearest_profile(lat, lon, developing_regions)
    if not profile:
        profile = developed_low  # Default to developed_low if no match

    # Adjust concentration based on coastal distance (6-7km range)
    distance_factor = 1.0
    if 6000 <= coastal_distance <= 7000:
        distance_factor = 1.2  # Increase concentration for target range
    elif coastal_distance > 7000:
        distance_factor = 0.8  # Decrease for further distances
    
    base_value = profile['base'] * distance_factor
    
    # Generate historical data with appropriate distribution
    historical_data = [
        max(0, base_value + np.random.normal(0, profile['std']))
        for _ in range(50)
    ]

    # Determine concentration level
    def get_concentration_level(value):
        if value < 10:
            return 'Low'
        elif value < 20:
            return 'Medium'
        else:
            return 'High'

    current_concentration = get_concentration_level(base_value)
    
    return {
        'concentration': current_concentration,
        'regional_average': {
            'concentration': base_value,
            'trend': 'Stable',
            'historical': historical_data
        },
        'impact_assessment': {
            'level': current_concentration,
            'trend': 'Stable',
            'projected_change': -5 if base_value > 15 else 0
        },
        'raw_stats': {
            'sample_count': len(historical_data),
            'mean': np.mean(historical_data),
            'median': np.median(historical_data),
            'std': np.std(historical_data),
            'variance': np.var(historical_data),
            'min': np.min(historical_data),
            'max': np.max(historical_data),
            'percentile_90': np.percentile(historical_data, 90)
        }
    }

def analyze_land_use(land_use_data):
    """
    Detailed analysis of land use patterns and their environmental impact.
    """
    land_categories = {
        'residential': ['residential', 'apartments', 'house'],
        'commercial': ['retail', 'commercial', 'shop', 'marketplace'],
        'industrial': ['industrial', 'factory', 'warehouse', 'construction'],
        'recreational': ['park', 'playground', 'sports_centre', 'garden'],
        'natural': ['grass', 'forest', 'beach', 'water', 'wetland'],
        'agricultural': ['farmland', 'orchard', 'vineyard', 'greenhouse'],
        'infrastructure': ['parking', 'railway', 'highway', 'transportation']
    }
    
    analysis = {
        'land_features': {cat: 0 for cat in land_categories},
        'detailed_breakdown': {},
        'environmental_metrics': {
            'green_space_ratio': 0,
            'urban_density': 0,
            'natural_buffer_zones': 0
        }
    }
    
    total_elements = 0
    
    # Analyze each element
    for element in land_use_data.get('elements', []):
        tags = element.get('tags', {})
        
        # Track specific land use types
        for tag_key in ['landuse', 'leisure', 'natural', 'building', 'amenity']:
            if tag_key in tags:
                land_type = tags[tag_key]
                
                # Add to detailed breakdown
                if land_type not in analysis['detailed_breakdown']:
                    analysis['detailed_breakdown'][land_type] = 0
                analysis['detailed_breakdown'][land_type] += 1
                
                # Categorize into main categories
                for category, types in land_categories.items():
                    if land_type in types:
                        analysis['land_features'][category] += 1
                        break
                
                total_elements += 1
    
    # Calculate percentages
    if total_elements > 0:
        for category in analysis['land_features']:
            analysis['land_features'][category] = round(
                (analysis['land_features'][category] / total_elements) * 100, 2
            )
        
        # Calculate environmental metrics
        green_space = (analysis['land_features']['natural'] + 
                      analysis['land_features']['recreational'])
        urban_space = (analysis['land_features']['residential'] + 
                      analysis['land_features']['commercial'] + 
                      analysis['land_features']['industrial'])
        
        analysis['environmental_metrics'] = {
            'green_space_ratio': round(green_space, 2),
            'urban_density': round(urban_space, 2),
            'natural_buffer_zones': round(analysis['land_features']['natural'], 2)
        }
    
    return analysis

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        lat = request.form.get('lat')
        lon = request.form.get('lon')
        radius = request.form.get('radius')
        
        try:
            land_use_data = get_overpass_data(float(lat), float(lon), int(radius))
            plastic_data = get_marine_plastic_data(float(lat), float(lon), int(radius), 0)
            analysis = analyze_land_use(land_use_data)
            
            # Pass the analysis data with proper variable names
            return render_template('results.html', 
                data=land_use_data, 
                analysis=analysis,
                residential=analysis['land_features']['residential'],
                commercial=analysis['land_features']['commercial'],
                industrial=analysis['land_features']['industrial']
            )
            
        except requests.RequestException as e:
            return render_template('error.html', error=str(e))
        except ValueError as e:
            return render_template('error.html', error="Invalid input parameters")
    
    return render_template('query.html')

@app.route('/api/query', methods=['GET'])
def api_query():
    """
    Enhanced API endpoint for land use queries with detailed analysis.
    """
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        radius = request.args.get('radius', type=int, default=1000)
        coastal_distance = request.args.get('coastalDistance', type=int, default=5)
        
        if lat is None or lon is None:
            return jsonify({"error": "Parameters 'lat' and 'lon' are required."}), 400

        # Get land use data
        land_use_data = get_overpass_data(lat, lon, radius)
        
        # Get detailed land use analysis
        land_analysis = analyze_land_use(land_use_data)
        
        # Calculate environmental impact score
        impact_weights = {
            'residential': 2,
            'commercial': 3,
            'industrial': 5,
            'recreational': -1,
            'natural': -2,
            'agricultural': 1,
            'infrastructure': 4
        }
        
        impact_score = sum(
            land_analysis['land_features'][cat] * weight 
            for cat, weight in impact_weights.items()
        )
        
        # Get marine plastic data
        plastic_data = get_marine_plastic_data(lat, lon, radius, coastal_distance)
        
        # Prepare comprehensive analysis response
        analysis = {
            'impact_score': round(abs(impact_score), 2),
            'score_trend': 'High Impact' if impact_score > 50 else 'Moderate Impact' if impact_score > 0 else 'Low Impact',
            'land_features': land_analysis['land_features'],
            'detailed_breakdown': land_analysis['detailed_breakdown'],
            'environmental_metrics': land_analysis['environmental_metrics'],
            'coastal_metrics': {
                'beach_quality': 'Good' if land_analysis['land_features']['natural'] > 30 else 'Fair',
                'water_quality': 'Good' if impact_score < 0 else 'Fair' if impact_score < 50 else 'Poor',
                'erosion_risk': 'Low' if land_analysis['land_features']['natural'] > 40 else 'Medium'
            },
            'regional_averages': {
                **land_analysis['land_features'],
                'plastic_concentration': plastic_data['regional_average']['concentration']
            },
            'marine_health_index': round(100 - abs(impact_score)/2, 2),
            'coastal_vulnerability': 'Low' if impact_score < 0 else 'Medium' if impact_score < 50 else 'High',
            'marine_biodiversity': 'High' if impact_score < 0 else 'Medium' if impact_score < 50 else 'Low',
            'plastic_concentration': plastic_data['concentration'],
            'plastic_trend': plastic_data['regional_average']['trend'],
            'plastic_impact': plastic_data['impact_assessment']['level'],
            'plastic_historical': plastic_data['regional_average']['historical'],
            'raw_stats': plastic_data['raw_stats']
        }
        
        return jsonify({
            'land_use': land_use_data,
            'analysis': analysis
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 503
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)