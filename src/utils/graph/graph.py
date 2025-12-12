from enum import Enum

class Gender(Enum):
    FEMALE = 1
    MALE = 2

class EducationLevel(Enum):
    PRIMARY_SCHOOL = 1
    MIDDLE_SCHOOL = 2
    HIGH_SCHOOL = 3
    JUNIOR_COLLEGE = 4
    BACHELOR = 5
    MASTER = 6
    DOCTORATE = 7

class NodeAttributes():
    location_code: str
    province_code: str
    city_code: str
    county_code: str
    longitude: float
    latitude: float

    def __init__(self, location_code: str, province_code: str, city_code: str,
                 county_code: str, longitude: float, latitude: float):
        self.location_code = location_code
        self.province_code = province_code
        self.city_code = city_code
        self.county_code = county_code
        self.longitude = longitude
        self.latitude = latitude

class EdgeAttributes():
    from_node: str
    to_node: str
    year: int
    month: int
    gender: Gender
    education_level: EducationLevel
    average_family_cost_per_month: float
    average_family_income_per_month: float
    total_flows: int
    stay_at_destination: bool
    changed_household: bool
    stay_duration_months: int
    flow_index: int

    from_node_attrs: NodeAttributes
    to_node_attrs: NodeAttributes

    def __init__(self, from_node: str, to_node: str, year: int, month: int, gender: Gender,
                 education_level: EducationLevel, average_family_cost_per_month: float,
                 average_family_income_per_month: float, total_flows: int,
                 stay_at_destination: bool,  changed_household: bool, stay_duration_months: int, flow_index: int,
                 from_node_attrs: NodeAttributes,
                 to_node_attrs: NodeAttributes):
        self.from_node = from_node
        self.to_node = to_node
        self.year = year
        self.month = month
        self.gender = gender
        self.education_level = education_level
        self.average_family_cost_per_month = average_family_cost_per_month
        self.average_family_income_per_month = average_family_income_per_month
        self.total_flows = total_flows
        self.stay_at_destination = stay_at_destination
        self.changed_household = changed_household
        self.stay_duration_months = stay_duration_months
        self.flow_index = flow_index
        self.from_node_attrs = from_node_attrs
        self.to_node_attrs = to_node_attrs
    

"""
Index(['hometown_code', 'hometown_province_code', 'hometown_city_code',
       'hometown_county_code', 'hometown_lon', 'hometown_lat',
       'first_flow_code', 'first_flow_province_code', 'first_flow_city_code',
       'first_flow_county_code', 'first_lon', 'first_lat', 'year_first_flow',
       'month_first_flow', 'current_code', 'current_province_code',
       'current_city_code', 'current_county_code', 'current_lon',
       'current_lat', 'year_current_flow', 'month_current_flow', 'gender',
       'edu_level', 'average_family_cost_per_month',
       'average_family_income_per_month', 'num_flows_total', 'if_stay',
       'if_change_household_local', 'how_long_to_stay'],
"""

