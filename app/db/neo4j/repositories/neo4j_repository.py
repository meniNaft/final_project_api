from app.db.neo4j.database_config import driver


def get_shared_targets():
    with driver.session() as session:
        query = """
            MATCH (g1:Group_Name)-[:COMMITTED_BY]->(e:Event)-[:TARGETED]->(t:Target_Type)
            MATCH (g2:Group_Name)-[:COMMITTED_BY]->(e)-[:TARGETED]->(t)
            WHERE g1 <> g2
            WITH country AS Country, region AS Region, city AS City, t.name AS Target, 
                 COLLECT(DISTINCT g1.name) + COLLECT(DISTINCT g2.name) AS Groups
            WITH CASE 
                     WHEN e.region IS NOT NULL THEN e.region
                     WHEN e.country IS NOT NULL THEN e.country
                     ELSE e.city
                 END AS Area, 
                 Target, 
                 Groups, 
                 SIZE(Groups) AS GroupCount
            ORDER BY Area, GroupCount DESC
            WITH Area, COLLECT({Target: Target, Groups: Groups, GroupCount: GroupCount}) AS TargetGroups
            RETURN Area, TargetGroups[0] AS MostAttackedTarget

            """
        res = session.run(query).data()
        print(res)

    # return [
    #     {"location": get_point_by_region(x.get("Region")), "groups": x.get("MostAttackedTarget", {}).get("Groups", [])}
    #     for x in res]