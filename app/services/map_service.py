import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
import tempfile

geolocator = Nominatim(user_agent="geoapi")


def get_map(area_data: list, area_type: str, zoom_level: str, callback):
    location = [20, 0] if zoom_level == "region" else [area_data[0]['lat'], area_data[0]['lon']]
    m = folium.Map(location=location, zoom_start=get_zoom_level(zoom_level))
    marker_cluster = MarkerCluster().add_to(m)

    callback(marker_cluster, area_data, area_type)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.html', delete=False) as f:
        f.write(m._repr_html_())
    return m._repr_html_()


def add_area_terror_group_markers_to_map(map, data, area_type):
    for event in data:
        try:
            area_name = event[area_type]
            lat = event["Latitude"]
            lon = event["Longitude"]
            groups = event["Groups"]
            popup_content = (f"<b>{area_type}:</b><br>{area_name}<br><br><b>Terror Groups:</b><br>"
                             f"<ul style='min-width: 200px; max-height: 200px; overflow-y: scroll;'>")
            for group in groups:
                popup_content += f"<li>{group}</li>"
            popup_content += "</ul>"

            folium.Marker(
                [lat, lon],
                popup=popup_content,
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(map)
        except Exception as e:
            print(f"Error processing event {event}: {e}")
            continue


def add_attack_type_terror_group_markers_to_map(map, data, area_type):
    for event in data:
        try:
            attack_type = event["MostCommonAttackType"]
            lat = event["Latitude"]
            lon = event["Longitude"]
            groups = event["Groups"]
            area_name = event[area_type]

            popup_content = (f"<b>{area_type}:</b><br>{area_name}<br><br><b>Attack Type:</b><br>{attack_type}<br><br"
                             f"><b>Terror Groups:</b><br>"
                             f"<ul style='min-width: 200px; max-height: 200px; overflow-y: scroll;'>")
            for group in groups:
                popup_content += f"<li>{group}</li>"
            popup_content += "</ul>"

            folium.Marker(
                [lat, lon],
                popup=popup_content,
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(map)
        except Exception as e:
            print(f"Error processing event {event}: {e}")
            continue


def add_top_group_city_by_area_markers_to_map(map, data, area_type):
    for event in data:
        try:
            lat = event["lat"]
            lon = event["lon"]
            groups = event["groups"]
            groups_count = event["group_count"]
            city = event['city_name']
            area_name = event[area_type]

            popup_content = (f"<b>{area_type}:</b><br>{area_name}<br><br>"
                             f"<b>city:</b><br>{city}<br><br>"
                             f"<b>group count:</b><br>{groups_count}<br><br"
                             f"><b>Terror Groups:</b><br>"
                             f"<ul style='min-width: 200px; max-height: 200px; overflow-y: scroll;'>")
            for group in groups:
                popup_content += f"<li>{group}</li>"
            popup_content += "</ul>"

            folium.Marker(
                [lat, lon],
                popup=popup_content,
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(map)
        except Exception as e:
            print(f"Error processing event {event}: {e}")
            continue


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
