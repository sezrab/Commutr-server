cycling = {
    'motorway': 10000,
    'motorway_link': 10000,
    'motorway_junction': 10000,

    'busway': 10000,
    'bus_guideway': 10000,
    
    'escape': 10000,
    'raceway': 10000,
    
    'trunk': 20,
    'trunk_link':20,
    
    'primary': 10,
    'primary_link': 10,
    
    'secondary': 3,
    'secondary_link': 3,
    
    'living_street': 3,
    'residential': 2,
    
    'tertiary': 2,
    'tertiary_link': 2,
    
    'service': 2,
    
    'pedestrian': 10,
    
    'track': 10,
    'footway': 10,
    'bridleway': 10,
    'steps': 10,
    'path': 10,
    'cycleway': 0.5,

    'construction': 10,
    'corridor': 3,    
    'road': 3,
    'unclassified': 2,

    None: 10,
}

mtb = {
    'motorway': 10000,
    'motorway_link': 10000,
    'motorway_junction': 10000,

    'busway': 10000,
    'bus_guideway': 10000,
    
    'escape': 10000,
    'raceway': 10000,
    
    'trunk': 50,
    'trunk_link':50,
    
    'primary': 10,
    'primary_link': 10,
    
    'secondary': 6,
    'secondary_link': 6,
    
    'living_street': 4,
    'residential': 4,
    
    'tertiary': 4,
    'tertiary_link': 4,
    
    'service': 2,
    
    'pedestrian': 3,
    
    'track': 0.5,
    'footway': 3,
    'bridleway': 0.5,
    'steps': 3,
    'path': 0.5,
    'cycleway': 0.5,

    'construction': 10,
    'corridor': 3,    
    'road': 3,
    'unclassified': 2,

    None: 10,
}

car = {
    'motorway': 1,
    'motorway_link': 1,
    'motorway_junction': 1,

    'busway': 10000,
    'bus_guideway': 10000,
    
    'escape': 10000,
    'raceway': 10000,
    
    'trunk': 2,
    'trunk_link':2,
    
    'primary': 3,
    'primary_link': 3,
    
    'secondary': 4,
    'secondary_link': 4,
    
    'living_street': 15,
    'residential': 15,
    
    'tertiary': 4,
    'tertiary_link': 4,
    
    'service': 5,
    
    'pedestrian': 10000,
    
    'track': 10000,
    'footway': 10000,
    'bridleway': 10000,
    'steps': 10000,
    'path': 10000,
    'cycleway': 10000,

    'construction': 10000,
    'corridor': 10000,
    'road': 5,
    'unclassified': 6,

    None: 100,
}


costMaps = {
    'mtb':mtb,
    'cycling':cycling,
    'car':car,
}