from sched import Event

from sqlalchemy import func, desc
from sqlalchemy.orm import aliased

from app.db.postgres.database_config import session_maker
from app.db.postgres.models import AttackType, Event, City, Country, State, Region, TerrorGroup


def get_deadliest_attack_types(only_top5: bool):
    with (session_maker() as session):
        query = (
            session.query(
                AttackType.id,
                AttackType.type,
                get_casualties_expression()
            )
            .join(AttackType.events)
            .group_by(AttackType.id)
            .order_by(desc('Casualties'))
        )

        if only_top5:
            query = query.limit(5)

        return query.all()


def get_avg_casualties_per_area(only_top5: bool, area_type: str):
    with session_maker() as session:
        country = aliased(Country)
        city = aliased(City)
        state = aliased(State)
        event = aliased(Event)

        query = session.query(
            func.round(
                (func.sum(event.civilian_killed_count) * 2 + func.sum(event.civilian_injured_count)) / func.count(
                    event.id), 2
            ).label('Casualties')
        )

        if area_type == 'city':
            selected_area = aliased(City)
            query = (query
                     .add_columns(selected_area.name)
                     .join(selected_area, selected_area.id == event.city_id)
                     .group_by(selected_area.id)
                     .order_by(desc('Casualties')))

        elif area_type == 'state':
            selected_area = aliased(State)
            query = (query
                     .add_columns(selected_area.name)
                     .join(city, city.id == event.city_id)
                     .join(selected_area, selected_area.id == city.state_id)
                     .group_by(selected_area.id)
                     .order_by(desc('Casualties')))

        elif area_type == 'country':
            selected_area = aliased(Country)
            query = (query
                     .add_columns(selected_area.name)
                     .join(city, city.id == event.city_id)
                     .join(state, state.id == city.state_id)
                     .join(selected_area, selected_area.id == state.country_id)
                     .group_by(selected_area.id)
                     .order_by(desc('Casualties')))

        else:
            selected_area = aliased(Region)
            query = (query
                     .add_columns(selected_area.name)
                     .join(city, city.id == event.city_id)
                     .join(state, state.id == city.state_id)
                     .join(country, country.id == state.country_id)
                     .join(selected_area, selected_area.id == country.region_id)
                     .group_by(selected_area.id)
                     .order_by(desc('Casualties')))

        if only_top5:
            query = query.limit(5)

        return query.all()


def get_top_terror_groups_by_casualties():
    with session_maker() as session:
        return (
            session.query(
                TerrorGroup.name,
                get_casualties_expression()
            )
            .join(TerrorGroup.events)
            .group_by(TerrorGroup.id)
            .order_by(desc('Casualties'))
            .limit(5)
            .all()
        )


def get_casualties_expression():
    return (func.sum(Event.civilian_killed_count) * 2 + func.sum(Event.civilian_injured_count)).label('Casualties')


def attack_percentage_change_by_year(area_type, area_id):
    with session_maker() as session:
        country = aliased(Country)
        city = aliased(City)
        state = aliased(State)
        event = aliased(Event)

        query = session.query(
            func.extract('year', event.date).label('year'),  # Extracting year from event date
            func.count(event.id).label('attack_count')  # Counting the number of events (attacks)
        )

        if area_type == 'city':
            selected_area = aliased(City)
            query = query.add_columns(selected_area.name) \
                .join(selected_area, selected_area.id == event.city_id) \
                .filter(selected_area.id == area_id) \
                .group_by(selected_area.id, func.extract('year', event.date)) \
                .order_by(func.extract('year', event.date))

        elif area_type == 'state':
            selected_area = aliased(State)
            query = query.add_columns(selected_area.name) \
                .join(city, city.id == event.city_id) \
                .join(selected_area, selected_area.id == city.state_id) \
                .filter(selected_area.id == area_id) \
                .group_by(selected_area.id, func.extract('year', event.date)) \
                .order_by(func.extract('year', event.date))

        elif area_type == 'country':
            selected_area = aliased(Country)
            query = query.add_columns(selected_area.name) \
                .join(city, city.id == event.city_id) \
                .join(state, state.id == city.state_id) \
                .join(selected_area, selected_area.id == state.country_id) \
                .filter(selected_area.id == area_id) \
                .group_by(selected_area.id, func.extract('year', event.date)) \
                .order_by(func.extract('year', event.date))

        elif area_type == 'region':
            selected_area = aliased(Region)
            query = query.add_columns(selected_area.name) \
                .join(city, city.id == event.city_id) \
                .join(state, state.id == city.state_id) \
                .join(country, country.id == state.country_id) \
                .join(selected_area, selected_area.id == country.region_id) \
                .filter(selected_area.id == area_id) \
                .group_by(selected_area.id, func.extract('year', event.date)) \
                .order_by(func.extract('year', event.date))

        return query.all()


def most_active_terror_group(area_type, area_id):
    with session_maker() as session:
        query = (
            session.query(
                TerrorGroup.name,
                func.count(Event.id).label('attack_count')
            )
            .join(Event.terror_groups))

        if area_type == 'city':
            query = (query.join(City, City.id == Event.city_id)
                     .filter(City.id == area_id))
        elif area_type == 'state':
            query = (query.join(City, City.id == Event.city_id)
                     .join(State, State.id == City.state_id)
                     .filter(State.id == area_id))
        elif area_type == 'country':
            query = (query.join(City, City.id == Event.city_id)
                     .join(State, State.id == City.state_id)
                     .join(Country, Country.id == State.country_id)
                     .filter(Country.id == area_id))
        elif area_type == 'region':
            query = (query.join(City, City.id == Event.city_id)
                     .join(State, State.id == City.state_id)
                     .join(Country, Country.id == State.country_id)
                     .join(Region, Region.id == Country.region_id)
                     .filter(Region.id == area_id))

        return (query
                .group_by(TerrorGroup.id)
                .order_by(desc('attack_count'))
                .limit(5)
                .all())
