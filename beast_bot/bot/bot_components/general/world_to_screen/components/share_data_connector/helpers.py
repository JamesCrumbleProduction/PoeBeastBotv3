def parse_str_vector_to_dict(value: str) -> dict[str, str]:
    parsed_data = dict()

    for raw_data in value.split():
        axis, coordinate = raw_data.split(':')
        parsed_data[axis.lower()] = coordinate.replace(',', '.')

    return parsed_data
