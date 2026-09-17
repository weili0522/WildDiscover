export const targetSpecies = [
  {
    id: 'night-parrot',
    commonName: 'Night Parrot',
    scientificName: 'Pezoporus occidentalis',
    habitat: 'Pilbara & Diamantina',
    featured: true
  },
  {
    id: 'princess-parrot',
    commonName: 'Princess Parrot',
    scientificName: 'Polytelis alexandrae',
    habitat: 'Great Sandy Desert',
    featured: true
  },
  {
    id: 'plains-wanderer',
    commonName: 'Plains-wanderer',
    scientificName: 'Pedionomus torquatus',
    habitat: 'Riverina Grasslands',
    featured: true
  },
  {
    id: 'rufous-scrub-bird',
    commonName: 'Rufous Scrub-bird',
    scientificName: 'Atrichornis rufescens',
    habitat: 'Ancient Rainforests',
    featured: true
  },
  {
    id: 'malleefowl',
    commonName: 'Malleefowl',
    scientificName: 'Leipoa ocellata',
    habitat: 'Mallee Woodlands',
    featured: false
  },
  {
    id: 'dusky-grasswren',
    commonName: 'Dusky Grasswren',
    scientificName: 'Amytornis purnelli',
    habitat: 'Central Australian Ranges',
    featured: false
  }
]

export const australianRegions = [
  { code: 'ALL', name: 'All Australia' },
  { code: 'WA', name: 'Western Australia' },
  { code: 'QLD', name: 'Queensland' },
  { code: 'NT', name: 'Northern Territory' },
  { code: 'SA', name: 'South Australia' },
  { code: 'NSW', name: 'New South Wales' },
  { code: 'VIC', name: 'Victoria' }
]

export const climateHorizons = [
  {
    id: 'current',
    label: '2000–2025'
  },
  {
    id: '2030',
    label: '2030 Model'
  },
  {
    id: '2050',
    label: '2050 Projection'
  }
]

export const environmentalLayers = [
  {
    id: 'vegetation',
    label: 'Vegetation Intactness',
    selected: true
  },
  {
    id: 'elevation',
    label: 'Elevation & Escarpments',
    selected: true
  },
  {
    id: 'spinifex',
    label: 'Spinifex Density (Triodia)',
    selected: true
  }
]

export const habitatPotentialPoints = [
  {
    id: 'high',
    level: 'High Potential',
    probability: 88,
    location: 'Fortescue Basin Swale',
    latitude: -22.35,
    longitude: 118.89
  },
  {
    id: 'medium',
    level: 'Medium Potential',
    probability: 65,
    location: 'Hamersley Foothills',
    latitude: -22.52,
    longitude: 118.55
  },
  {
    id: 'low',
    level: 'Low Potential',
    probability: 28,
    location: 'Marginal Habitat',
    latitude: -22.75,
    longitude: 118.2
  }
]

export const defaultMapFilters = {
  selectedSpecies: ['night-parrot'],
  region: 'WA',
  climateHorizon: 'current',
  probability: 0,
  selectedLayers: [
    'vegetation',
    'elevation',
    'spinifex'
  ]
}