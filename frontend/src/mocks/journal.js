export const journalSummary = {
  activeInvestigations: 3,
  savedZones: 5,
  evidenceSubmitted: 8
}

export const investigations = [
  {
    id: 'night-parrot-investigation',
    number: '01',
    speciesId: 'night-parrot',
    commonName: 'Night Parrot',
    scientificName: 'Pezoporus occidentalis',
    category: 'Critically Elusive',
    type: 'Priority Investigation',
    status: 'Completed',
    latestExploration: '7 Sep 2026',
    zonesExplored: 4,
    evidenceSubmitted: 3,
    savedBoundary: '14.2 km²',
    savedArea: 'Pilbara Sector 4',
    probability: 82,
    probabilityLevel: 'High Potential',
    image: 'night-parrot.jpg',
    actionLabel: 'View Exploration Summary'
  },
  {
    id: 'princess-parrot-investigation',
    number: '02',
    speciesId: 'princess-parrot',
    commonName: 'Princess Parrot',
    scientificName: 'Polytelis alexandrae',
    category: 'Nomadic Desert Explorer',
    type: 'Arid Corridor Study',
    status: 'In Progress',
    latestExploration: '14 Aug 2026',
    zonesExplored: 2,
    evidenceSubmitted: 1,
    savedBoundary: '28.5 km²',
    savedArea: 'Great Victoria Desert Dunes',
    probability: 64,
    probabilityLevel: 'Medium Potential',
    image: 'princess-parrot.jpg',
    actionLabel: 'Continue Exploration'
  },
  {
    id: 'plains-wanderer-investigation',
    number: '03',
    speciesId: 'plains-wanderer',
    commonName: 'Plains-wanderer',
    scientificName: 'Pedionomus torquatus',
    category: 'Critically Endangered',
    type: 'Grassland Structural Survey',
    status: 'Not Started',
    latestExploration: 'No session logged',
    zonesExplored: 5,
    evidenceSubmitted: 4,
    savedBoundary: '9.8 km²',
    savedArea: 'Riverina Grasslands Sector 2',
    probability: 76,
    probabilityLevel: 'High Potential',
    image: 'plains-wanderer.jpg',
    actionLabel: 'Start Exploration'
  }
]

export const journalStatuses = [
  'All Statuses',
  'Completed',
  'In Progress',
  'Not Started'
]

export const explorationDetail = {
  investigationId: 'princess-parrot-investigation',
  title: 'Princess Parrot Exploration',
  sessionStatus: 'Exploration in Progress',
  sector: 'Great Victoria Desert Dunes',
  location: 'Great Victoria Desert',
  coordinates: '28°05′12″S 125°46′30″E',
  area: '28.5 km²',
  probability: 64,
  probabilityLevel: 'Medium Potential',
  observationsLogged: 1,
  fieldTime: '28 mins in field',
  species: {
    commonName: 'Princess Parrot',
    scientificName: 'Polytelis alexandrae',
    conservationStatus: 'Nomadic Desert Explorer',
    image: 'princess-parrot.jpg'
  },
  observations: [
    {
      id: 'observation-sighting',
      type: 'audio',
      title: 'Princess Parrot Call Recorded',
      time: '18:42',
      description: 'Soft chattering call recorded near desert oak habitat',
      attachment: 'princess_call_01.wav'
    }
  ],
  noticeOptions: [
    {
      id: 'heard-call',
      label: 'Heard call',
      description: 'Audio / vocal'
    },
    {
      id: 'saw-bird',
      label: 'Saw a bird',
      description: 'Direct sighting'
    },
    {
      id: 'found-signs',
      label: 'Found signs',
      description: 'Nest / droppings'
    },
    {
      id: 'other',
      label: 'Other',
      description: 'Flora / habitat'
    }
  ]
}

export const completedExplorationSummary = {
  investigationId: 'night-parrot-investigation',
  title: 'Night Parrot Exploration',
  status: 'Exploration Completed',
  fieldSummaryId: '#0294',
  completedAt: '10 September 2026 · 19:20',
  contributionPoints: 20,
  readOnly: true,
  sector: 'Pilbara Sector 4',
  location: 'Fortescue Basin Swale',
  sessionDate: '19:20 AEST',
  area: '14.2 km²',
  probability: 82,
  probabilityLevel: 'High Potential',
  explorationTime: '42 minutes',
  observationsRecorded: 2,
  species: {
    commonName: 'Night Parrot',
    scientificName: 'Pezoporus occidentalis',
    conservationStatus: 'Critically Endangered',
    image: 'night-parrot.jpg'
  },
  findings: [
    {
      id: 'bird-call',
      type: 'audio',
      title: 'Bird Call Heard',
      time: '19:08',
      description: 'Two-note rising whistle',
      attachment: 'acoustic_log_04.wav',
      duration: '2m 40s'
    },
    {
      id: 'roost-signs',
      type: 'signs',
      title: 'Roost Signs Found',
      time: '18:45',
      description: 'Possible tunnel in mature spinifex',
      attachment: '2 photos attached'
    }
  ],
  fieldNotes:
    'Arrived at 18:20 near the western hummock line. At 19:08, recorded two distinct low acoustic whistles matching known Night Parrot frequency. Triodia hummocks were unburnt and dense with low mammalian predator presence.',
  environmentalRecord:
    'Dusk (22 Lux) • 23.4°C • SE Calm Wind (4 km/h) • Triodia hummocks unburnt >35 yrs',
  privacyProtection:
    'ALA Obfuscation Applied (10 km buffer)'
}