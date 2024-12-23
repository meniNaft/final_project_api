import pandas as pd
import app.services.map_service as map_service
import app.db.postgres.repositories.statistic_repository as statistic_repo


def get_deadliest_attack_types(only_top5: bool = False):
    res = statistic_repo.get_deadliest_attack_types(only_top5)
    return [{
        "id": row.id,
        "type": row.type,
        "casualties": row.Casualties
    } for row in res]


def get_avg_casualties_per_area(only_top5: bool, area_type: str):
    res = statistic_repo.get_avg_casualties_per_area(only_top5, area_type)
    res = [{
        area_type: row.name,
        "lat": row.lat,
        "lon": row.lon,
        "casualties": row.Casualties
    } for row in res]
    return map_service.get_map(
        area_data=res,
        area_type=area_type,
        zoom_level="region",
        callback=map_service.add_avg_casualties_marker_to_map)


def get_top_terror_groups_by_casualties():
    res = statistic_repo.get_top_terror_groups_by_casualties()
    return [{
        "group_name": row.name,
        "casualties": row.Casualties
    } for row in res]


def attack_percentage_change_by_year(area_type: str, area_id: int):
    res = statistic_repo.attack_percentage_change_by_year(area_type, area_id)
    if len(res) == 0:
        return {"message": "No data found for this keyword"}

    data = {
        area_type: res[0].name,
        'lat': res[0].lat,
        'lon': res[0].lon,
        "attack_count": [{
            'year': row.year,
            'attack_count': row.attack_count,
        } for row in res]
    }

    df = pd.DataFrame(data['attack_count']).sort_values(by=['year'])
    df['percentage_change'] = (df['attack_count'].pct_change() * 100).round(2)
    df['percentage_change'] = df['percentage_change'].fillna('').round(2)

    result = {
        area_type: data[area_type],
        'lat': data['lat'],
        'lon': data['lon'],
        "percentage_per_year": [{
            'year': row['year'],
            'percentage_change': row['percentage_change'],
            'attack_count': row['attack_count']
        } for _, row in df.iterrows()]
    }

    return map_service.get_map(
        area_data=[result],
        area_type=area_type,
        zoom_level=area_type,
        callback=map_service.add_attack_percentage_marker_to_map
    )


def most_active_terror_group_map(area_type: str, area_id: int):
    data = statistic_repo.most_active_terror_group(area_type, area_id)
    if len(data) == 0:
        return {"message": "No data found for this keyword"}

    result = {
        area_type: data[0].area_name,
        'lat': data[0].lat,
        'lon': data[0].lon,
        'terror_groups': [{
            'group_name': row.name,
            'attack_count': row.attack_count
        } for row in data]
    }

    return map_service.get_map(
        area_data=[result],
        area_type=area_type,
        zoom_level=area_type,
        callback=map_service.add_terror_group_marker_to_map
    )
