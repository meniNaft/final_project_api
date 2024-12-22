import pandas as pd

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
    return [{
        area_type: row.name,
        "casualties": row.Casualties
    } for row in res]


def get_top_terror_groups_by_casualties():
    res = statistic_repo.get_top_terror_groups_by_casualties()
    return [{
        "group_name": row.name,
        "casualties": row.Casualties
    } for row in res]


def attack_percentage_change_by_year(area_type: str, area_id: int):
    res = statistic_repo.attack_percentage_change_by_year(area_type, area_id)
    if len(res) == 0:
        return {"message": "no data found for this key words"}

    data = {
        'area': res[0].name,
        "attack_count": [{
            'year': row.year,
            'attack_count': row.attack_count,
        } for row in res]
    }

    df = pd.DataFrame(data['attack_count']).sort_values(by=['year'])
    df['percentage_change'] = df['attack_count'].pct_change() * 100
    df['percentage_change'] = df['percentage_change'].fillna('')

    return [{
        'year': row['year'],
        'percentage_change': row['percentage_change'],
        'attack_count': row['attack_count'],
        'area': data['area']
    } for _, row in df.iterrows()]


def most_active_terror_group(area_type: str, area_id: int):
    res = statistic_repo.most_active_terror_group(area_type, area_id)
    return [{
        "name": row.name,
        "attack_count": row.attack_count
    } for row in res]
