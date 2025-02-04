from app.db.neo4j.database_config import driver


def get_shared_targets(area_type: str):
    with driver.session() as session:
        query = f"""
        MATCH {get_area_type_full_path(area_type)} (city:City)<-[:HAPPENED_IN]-(event:Event)-[:COMMITTED_BY]->(group:Group_Name)
        MATCH (event)-[:TARGETED]->(target:Target_Type)
        WITH {area_type}, target, city.lat AS lat, city.lon AS lon, COLLECT(DISTINCT group.name) AS groups
        WHERE SIZE(groups) >= 2
        WITH {area_type}, target, SIZE(groups) AS GroupCount, groups, lat, lon
        ORDER BY {area_type}.name, GroupCount DESC
        WITH {area_type}, """
        query += """
        COLLECT({target: target.name, groupCount: GroupCount, groups: groups, lat: lat, lon: lon}) AS targets
        """
        query += f"""
        RETURN {area_type}.name AS {area_type}, 
               targets[0].target AS Target, 
               targets[0].groupCount AS GroupCount, 
               targets[0].groups AS Groups,
               targets[0].lat AS Latitude, 
               targets[0].lon AS Longitude
            """
        res = session.run(query).data()
        return res


def get_cooperating_groups():
    with driver.session() as session:
        query = """
        MATCH (event:Event) - [:COMMITTED_BY] -> (group1:Group_Name), (event) - [:COMMITTED_BY] -> (group2:Group_Name)
        WHERE group1.name < group2.name
        RETURN DISTINCT group1.name AS Group1, group2.name AS Group2
        ORDER BY Group1, Group2
        """
        res = session.run(query).data()
        return res


def get_shared_attack_types(area_type: str):
    with driver.session() as session:
        query = f"""
        MATCH {get_area_type_full_path(area_type)} (city:City)<-[:HAPPENED_IN]-(event:Event)-[:COMMITTED_BY]->(group:Group_Name)
        MATCH (event)-[:HAS_ATTACK_TYPE]->(attack_type:Attack_Type)
        WITH {area_type}, city.lat AS Latitude, city.lon AS Longitude, attack_type.name AS AttackType, 
             COLLECT(DISTINCT group.name) AS Groups
        WHERE SIZE(Groups) > 1
        WITH {area_type}, Latitude, Longitude, AttackType, Groups, SIZE(Groups) AS GroupCount
        ORDER BY {area_type}.name, GroupCount DESC
        WITH {area_type}, Latitude, Longitude,
        """
        query += """
        COLLECT({AttackType: AttackType, Groups: Groups, GroupCount: GroupCount}) AS AttackTypes        
        """
        query += f"""
        RETURN {area_type}.name AS {area_type}, 
               Latitude, Longitude, 
               AttackTypes[0].AttackType AS MostCommonAttackType, 
               AttackTypes[0].Groups AS Groups
        """
        res = session.run(query).data()
        return res


def top_group_city_by_area(area_type: str):
    with driver.session() as session:
        query = f"""
        MATCH {get_area_type_full_path(area_type)} (city:City)<-[:HAPPENED_IN]-(event:Event)-[:COMMITTED_BY]->(
        group:Group_Name) WITH {area_type}, city, COLLECT(DISTINCT group.name) AS groups, 
        COUNT(DISTINCT group.name) AS group_count ORDER BY {area_type}, group_count DESC
        WITH {area_type},
        """
        query += """COLLECT({city: city.name, lat: city.lat, lon: city.lon, count: group_count, groups: groups})[0] AS top_city"""
        query += f"""
        RETURN {area_type}.name AS {area_type}, 
        top_city.city AS city_name, 
        top_city.lat AS lat, 
        top_city.lon AS lon, 
        top_city.count AS group_count, 
        top_city.groups AS groups 
        ORDER BY {area_type};
        """
        res = session.run(query).data()
        return res


def get_groups_attacked_same_target_same_year():
    with driver.session() as session:
        query = """
        MATCH (group1:Group_Name) <- [:COMMITTED_BY] - (event1:Event)-[:TARGETED]->(targetType:Target_Type),
          (group2:Group_Name) <- [:COMMITTED_BY]- (event2:Event) -[:TARGETED]->(targetType)
        WHERE group1 <> group2 AND event1.date.year = event2.date.year
        WITH DISTINCT event1.date.year AS year, targetType.name AS target_type, 
                      COLLECT(DISTINCT group1.name) + COLLECT(DISTINCT group2.name) AS groups
        RETURN year, target_type, REDUCE(s = [], g IN groups | CASE WHEN NOT g IN s THEN s + g ELSE s END) AS unique_groups
        ORDER BY year, target_type;
        """
        res = session.run(query).data()
        return res


def get_area_type_full_path(area_type):
    if area_type == 'city':
        return ''
    elif area_type == 'state':
        return "(state:State)-[:CONTAINS]->"
    elif area_type == 'country':
        return "(country:Country)-[:CONTAINS]->(state:State)-[:CONTAINS]->"
    elif area_type == 'region':
        return "(region:Region) - [:CONTAINS] -> (country:Country)-[:CONTAINS]->(state:State)-[:CONTAINS]->"
