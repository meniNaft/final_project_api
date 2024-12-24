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


def get_area_type_full_path(area_type):
    if area_type == 'city':
        return ''
    elif area_type == 'state':
        return "(state:State)-[:CONTAINS]->"
    elif area_type == 'country':
        return "(country:Country)-[:CONTAINS]->(state:State)-[:CONTAINS]->"
    elif area_type == 'region':
        return "(region:Region) - [:CONTAINS] -> (country:Country)-[:CONTAINS]->(state:State)-[:CONTAINS]->"
