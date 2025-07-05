{
  "type": "FeatureCollection",
  "name": "Deutsche Glasfaser Netzwerk - Schema Deutschland",
  "crs": {
    "type": "name",
    "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" }
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "POP Düsseldorf",
        "typ": "POP",
        "standort": "Digital Realty DUS1/DUS2",
        "peering": "MegaIX",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [6.8672, 51.1883] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "POP Frankfurt",
        "typ": "POP",
        "standort": "Digital Realty FRA16",
        "peering": "DE-CIX",
        "bundesland": "Hessen"
      },
      "geometry": { "type": "Point", "coordinates": [8.7387, 50.1204] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "POP Amsterdam",
        "typ": "POP",
        "standort": "Science Park 120",
        "peering": "AMS-IX",
        "bundesland": "International"
      },
      "geometry": { "type": "Point", "coordinates": [4.951, 52.356] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Ahaus",
        "typ": "Stadt/Gemeinde",
        "status": "Ausgebaut",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [7.0097, 52.0747] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Borken",
        "typ": "Stadt/Gemeinde",
        "status": "Ausgebaut",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [6.8592, 51.8436] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Coesfeld",
        "typ": "Stadt/Gemeinde",
        "status": "Ausgebaut",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [7.166, 51.9449] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Dülmen",
        "typ": "Stadt/Gemeinde",
        "status": "Ausgebaut",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [7.2796, 51.8315] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Heiden",
        "typ": "Stadt/Gemeinde",
        "status": "Ausgebaut",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [6.9358, 51.8318] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Isselburg",
        "typ": "Stadt/Gemeinde",
        "status": "Ausgebaut",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [6.4603, 51.8314] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Lüdinghausen",
        "typ": "Stadt/Gemeinde",
        "status": "Ausgebaut",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [7.4447, 51.7709] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Rees",
        "typ": "Stadt/Gemeinde",
        "status": "Ausgebaut",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [6.3967, 51.759] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Selfkant",
        "typ": "Stadt/Gemeinde",
        "status": "Im Ausbau",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [5.9167, 51.0167] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Vreden",
        "typ": "Stadt/Gemeinde",
        "status": "Ausgebaut",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [6.8286, 52.0322] }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Winterberg",
        "typ": "Stadt/Gemeinde",
        "status": "In Planung",
        "bundesland": "Nordrhein-Westfalen"
      },
      "geometry": { "type": "Point", "coordinates": [8.5303, 51.196] }
    },
    {
      "type": "Feature",
      "properties": {
        "source": "POP Düsseldorf",
        "target": "POP Frankfurt",
        "typ": "Backbone"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [6.8672, 51.1883],
          [8.7387, 50.1204]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "source": "POP Düsseldorf",
        "target": "POP Amsterdam",
        "typ": "Backbone"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [6.8672, 51.1883],
          [4.951, 52.356]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Ahaus", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [7.0097, 52.0747],
          [6.8672, 51.1883]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Borken", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [6.8592, 51.8436],
          [6.8672, 51.1883]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Coesfeld", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [7.166, 51.9449],
          [6.8672, 51.1883]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Dülmen", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [7.2796, 51.8315],
          [6.8672, 51.1883]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Heiden", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [6.9358, 51.8318],
          [6.8672, 51.1883]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Isselburg", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [6.4603, 51.8314],
          [6.8672, 51.1883]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Lüdinghausen", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [7.4447, 51.7709],
          [6.8672, 51.1883]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Rees", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [6.3967, 51.759],
          [6.8672, 51.1883]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Selfkant", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [5.9167, 51.0167],
          [6.8672, 51.1883]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Vreden", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [6.8286, 52.0322],
          [6.8672, 51.1883]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": { "source": "Winterberg", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [8.5303, 51.196],
          [6.8672, 51.1883]
        ]
      }
    }
  ]
}

{
  "type": "FeatureCollection",
  "name": "Deutsche Glasfaser Netzwerk - Hessen",
  "features": [
    {
      "type": "Feature",
      "properties": { "name": "Limburg-Weilburg", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Hessen" },
      "geometry": { "type": "Point", "coordinates": [8.15, 50.4] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Fulda (Landkreis)", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Hessen" },
      "geometry": { "type": "Point", "coordinates": [9.6833, 50.55] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Schwalm-Eder-Kreis", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Hessen" },
      "geometry": { "type": "Point", "coordinates": [9.35, 51.0167] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Groß-Gerau (Landkreis)", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Hessen" },
      "geometry": { "type": "Point", "coordinates": [8.4833, 49.9167] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Limburg-Weilburg", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [8.15, 50.4], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Fulda (Landkreis)", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [9.6833, 50.55], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Schwalm-Eder-Kreis", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [9.35, 51.0167], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Groß-Gerau (Landkreis)", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [8.4833, 49.9167], [8.7387, 50.1204] ] }
    }
  ]
}

{
  "type": "FeatureCollection",
  "name": "Deutsche Glasfaser Netzwerk - Rheinland-Pfalz & Saarland",
  "features": [
    {
      "type": "Feature",
      "properties": { "name": "Polch", "typ": "Stadt/Gemeinde", "status": "Ausgebaut", "bundesland": "Rheinland-Pfalz" },
      "geometry": { "type": "Point", "coordinates": [7.3167, 50.3] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Bitburger Land", "typ": "Verbandsgemeinde", "status": "Im Ausbau", "bundesland": "Rheinland-Pfalz" },
      "geometry": { "type": "Point", "coordinates": [6.525, 49.9725] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Bad Kreuznach (Landkreis)", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Rheinland-Pfalz" },
      "geometry": { "type": "Point", "coordinates": [7.7, 49.8333] }
    },
    {
      "type": "Feature",
      "properties": { "name": "St. Wendel", "typ": "Stadt/Gemeinde", "status": "Im Ausbau", "bundesland": "Saarland" },
      "geometry": { "type": "Point", "coordinates": [7.1667, 49.4667] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Marpingen", "typ": "Stadt/Gemeinde", "status": "Im Ausbau", "bundesland": "Saarland" },
      "geometry": { "type": "Point", "coordinates": [7.05, 49.45] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Polch", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [7.3167, 50.3], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Bitburger Land", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [6.525, 49.9725], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Bad Kreuznach (Landkreis)", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [7.7, 49.8333], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "St. Wendel", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [7.1667, 49.4667], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Marpingen", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [7.05, 49.45], [8.7387, 50.1204] ] }
    }
  ]
}

{
  "type": "FeatureCollection",
  "name": "Deutsche Glasfaser Netzwerk - Baden-Württemberg",
  "features": [
    {
      "type": "Feature",
      "properties": { "name": "Sinsheim", "typ": "Stadt/Gemeinde", "status": "Im Ausbau", "bundesland": "Baden-Württemberg" },
      "geometry": { "type": "Point", "coordinates": [8.8797, 49.2547] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Bretten", "typ": "Stadt/Gemeinde", "status": "Im Ausbau", "bundesland": "Baden-Württemberg" },
      "geometry": { "type": "Point", "coordinates": [8.705, 49.0361] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Eppingen", "typ": "Stadt/Gemeinde", "status": "Im Ausbau", "bundesland": "Baden-Württemberg" },
      "geometry": { "type": "Point", "coordinates": [8.9092, 49.1369] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Buchen (Odenwald)", "typ": "Stadt/Gemeinde", "status": "Im Ausbau", "bundesland": "Baden-Württemberg" },
      "geometry": { "type": "Point", "coordinates": [9.3219, 49.5222] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Sinsheim", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [8.8797, 49.2547], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Bretten", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [8.705, 49.0361], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Eppingen", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [8.9092, 49.1369], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Buchen (Odenwald)", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [9.3219, 49.5222], [8.7387, 50.1204] ] }
    }
  ]
}

{
  "type": "FeatureCollection",
  "name": "Deutsche Glasfaser Netzwerk - Bayern",
  "features": [
    {
      "type": "Feature",
      "properties": { "name": "Aichach-Friedberg", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Bayern" },
      "geometry": { "type": "Point", "coordinates": [11.1, 48.4333] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Deggendorf (Landkreis)", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Bayern" },
      "geometry": { "type": "Point", "coordinates": [12.9, 48.8167] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Dingolfing-Landau", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Bayern" },
      "geometry": { "type": "Point", "coordinates": [12.5833, 48.6333] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Aschaffenburg (Landkreis)", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Bayern" },
      "geometry": { "type": "Point", "coordinates": [9.15, 50.0167] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Aichach-Friedberg", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [11.1, 48.4333], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Deggendorf (Landkreis)", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [12.9, 48.8167], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Dingolfing-Landau", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [12.5833, 48.6333], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Aschaffenburg (Landkreis)", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [9.15, 50.0167], [8.7387, 50.1204] ] }
    }
  ]
}

{
  "type": "FeatureCollection",
  "name": "Deutsche Glasfaser Netzwerk - Niedersachsen",
  "features": [
    {
      "type": "Feature",
      "properties": { "name": "Gifhorn (Landkreis)", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Niedersachsen" },
      "geometry": { "type": "Point", "coordinates": [10.55, 52.6] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Helmstedt (Landkreis)", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Niedersachsen" },
      "geometry": { "type": "Point", "coordinates": [11, 52.25] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Lüneburg (Landkreis)", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Niedersachsen" },
      "geometry": { "type": "Point", "coordinates": [10.45, 53.2] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Uelzen (Landkreis)", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Niedersachsen" },
      "geometry": { "type": "Point", "coordinates": [10.5667, 52.9667] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Gifhorn (Landkreis)", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [10.55, 52.6], [6.8672, 51.1883] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Helmstedt (Landkreis)", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [11, 52.25], [6.8672, 51.1883] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Lüneburg (Landkreis)", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [10.45, 53.2], [6.8672, 51.1883] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Uelzen (Landkreis)", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [10.5667, 52.9667], [6.8672, 51.1883] ] }
    }
  ]
}

{
  "type": "FeatureCollection",
  "name": "Deutsche Glasfaser Netzwerk - Schleswig-Holstein",
  "features": [
    {
      "type": "Feature",
      "properties": { "name": "Rendsburg-Eckernförde", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Schleswig-Holstein" },
      "geometry": { "type": "Point", "coordinates": [9.6667, 54.3] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Segeberg", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Schleswig-Holstein" },
      "geometry": { "type": "Point", "coordinates": [10.3, 53.9] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Steinburg", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Schleswig-Holstein" },
      "geometry": { "type": "Point", "coordinates": [9.45, 53.9167] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Rendsburg-Eckernförde", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [9.6667, 54.3], [6.8672, 51.1883] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Segeberg", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [10.3, 53.9], [6.8672, 51.1883] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Steinburg", "target": "POP Düsseldorf", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [9.45, 53.9167], [6.8672, 51.1883] ] }
    }
  ]
}

{
  "type": "FeatureCollection",
  "name": "Deutsche Glasfaser Netzwerk - Ostdeutschland",
  "features": [
    {
      "type": "Feature",
      "properties": { "name": "Landkreis Leipzig", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Sachsen" },
      "geometry": { "type": "Point", "coordinates": [12.6, 51.25] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Börde", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Sachsen-Anhalt" },
      "geometry": { "type": "Point", "coordinates": [11.3, 52.2] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Gotha (Landkreis)", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Thüringen" },
      "geometry": { "type": "Point", "coordinates": [10.7, 50.95] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Havelland", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Brandenburg" },
      "geometry": { "type": "Point", "coordinates": [12.6667, 52.6667] }
    },
    {
      "type": "Feature",
      "properties": { "name": "Ludwigslust-Parchim", "typ": "Landkreis", "status": "Im Ausbau", "bundesland": "Mecklenburg-Vorpommern" },
      "geometry": { "type": "Point", "coordinates": [11.75, 53.4167] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Landkreis Leipzig", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [12.6, 51.25], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Börde", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [11.3, 52.2], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Gotha (Landkreis)", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [10.7, 50.95], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Havelland", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [12.6667, 52.6667], [8.7387, 50.1204] ] }
    },
    {
      "type": "Feature",
      "properties": { "source": "Ludwigslust-Parchim", "target": "POP Frankfurt", "typ": "Regional" },
      "geometry": { "type": "LineString", "coordinates": [ [11.75, 53.4167], [8.7387, 50.1204] ] }
    }
  ]
}