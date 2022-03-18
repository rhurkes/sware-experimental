def get_padded_bounds(risk, padding_degrees):
    lats = [x[1] for x in risk]
    lons = [x[0] for x in risk]

    return {
        'max_lat': max(lats) + padding_degrees,
        'min_lat': min(lats) - padding_degrees,
        'max_lon': max(lons) + padding_degrees,
        'min_lon': min(lons) - padding_degrees,
    }
