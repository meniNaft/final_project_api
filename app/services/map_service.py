import folium
from geopy.geocoders import Nominatim
import tempfile

geolocator = Nominatim(user_agent="geoapi")


def get_map(area_data: list, area_type: str, zoom_level: str, callback):
    location =[20, 0] if zoom_level == "region" else [area_data[0]['lat'], area_data[0]['lon']]
    m = folium.Map(location=location, zoom_start=get_zoom_level(zoom_level))
    callback(m, area_data, area_type)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.html', delete=False) as f:
        f.write(m._repr_html_())
    return m._repr_html_()


def add_text_search_markers_to_map(map, data, area_type):
    for event in data:
        try:
            title = event["title"]
            lat = event["lat"]
            lon = event["lon"]
            body = event["body"]
            category = event["category"]
            date = event["date"]

            popup_content = (f"<b>Title</b><br>{title}<br><br><b>Category:</b> {category}<br><b>Date:</b> {date}<br><br><b"
                             f">Details:</b><br>")
            popup_content += f'<div style="min-width: 200px; max-height: 200px; overflow-y: scroll;">{body}</div>'

            folium.Marker(
                [lat, lon],
                popup=popup_content,
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(map)

        except Exception as e:
            print(f"Error processing event {event}: {e}")
            continue


def add_avg_casualties_marker_to_map(map, area_data, area_type):
    def get_color(average):
        if average < 5:
            return 'green'
        elif average < 10:
            return 'orange'
        return 'red'

    for area in area_data:
        try:
            area_name = area[area_type]
            casualties = area["casualties"]

            folium.Marker(
                [area['lat'], area['lon']],
                popup=f"<b>{area_name}</b><br><br>Casualties: {casualties}",
                icon=folium.Icon(color=get_color(area["casualties"]), icon="info-sign")
            ).add_to(map)
        except:
            continue


def add_attack_percentage_marker_to_map(map, area_data, area_type):
    for area in area_data:
        try:
            area_name = area[area_type]
            lat = area['lat']
            lon = area['lon']
            percentage_per_year = area["percentage_per_year"]
            popup_content = f"<b>{area_name}</b><br>Latitude: {lat}<br>Longitude: {lon}<br><br><b>Yearly Attack Percentage Change:</b><br>"
            popup_content += '<div style="max-height: 200px; overflow-y: scroll;">'
            for record in percentage_per_year:
                year = record['year']
                attack_count = record['attack_count']
                percentage_change = record['percentage_change']
                popup_content += f"""
                    <br>
                    <div style="min-width: 200px;>
                        <b>Year:</b> {year}<br>
                        <b>Attacks:</b> {attack_count}<br>
                        <b>Change:</b> {percentage_change}%<br>
                    </div>
                    """
            # End the scrollable section
            popup_content += '</div>'

            folium.Marker(
                [lat, lon],
                popup=popup_content,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(map)

        except Exception as e:
            print(f"Error processing area {area}: {e}")
            continue


def add_terror_group_marker_to_map(map, area_data, area_type):
    for area in area_data:
        try:
            area_name = area[area_type]
            lat = area['lat']
            lon = area['lon']
            terror_groups = area["terror_groups"]
            popup_content = f"<b>{area_name}</b><br>Latitude: {lat}<br>Longitude: {lon}<br><br><b>Terror Groups:</b><br>"
            popup_content += '<div style="max-height: 200px; overflow-y: scroll;">'

            for group in terror_groups:
                group_name = group['group_name']
                attack_count = group['attack_count']

                popup_content += f"""
                    <br>
                    <div style="min-width: 200px;">
                        <b>Group Name:</b> {group_name}<br>
                        <b>Attacks:</b> {attack_count}<br>
                    </div>
                    """
            popup_content += '</div>'

            folium.Marker(
                [lat, lon],
                popup=popup_content,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(map)

        except Exception as e:
            print(f"Error processing area {area}: {e}")
            continue


def get_zoom_level(area_type: str) -> int:
    if area_type.lower() == "region":
        return 2
    elif area_type.lower() == "state":
        return 8
    elif area_type.lower() == "city":
        return 12
    else:
        return 10
