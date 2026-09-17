export const gallerySpecies = [
  {
    id: 'night-parrot',
    name: 'Night Parrot',
    scientificName: 'Pezoporus occidentalis',
    status: 'Critically Endangered',
    statusClass: 'critical',
    habitat: 'Spinifex grasslands and arid regions',
    activeTime: 'Dusk and night (nocturnal)',
    location: 'Remote inland WA and QLD',
    whyItMatters:
      'One of Australia’s rarest birds and an important indicator of healthy spinifex ecosystems.',
    didYouKnow:
      'Night Parrots are exceptionally elusive and are more frequently detected using acoustic listening sensors than visual sightings.',
    description:
      'Cryptic nocturnal ground parrot inhabiting remote spinifex hummocks. One of Australia’s rarest birds.',
    image: 'night-parrot.jpg',
    audioDuration: '0:38',
    verified: true
  },
  {
    id: 'princess-parrot',
    name: 'Princess Parrot',
    scientificName: 'Polytelis alexandrae',
    status: 'Vulnerable',
    statusClass: 'vulnerable',
    habitat: 'Great Sandy Desert woodlands',
    activeTime: 'Daytime (diurnal)',
    location: 'Central and western Australia',
    whyItMatters:
      'Its movements provide valuable information about the condition of remote desert habitats.',
    didYouKnow:
      'Princess Parrots are highly nomadic and may disappear from an area for many years before returning after favourable rainfall.',
    description:
      'Delicate desert parrot with pastel pink throat and slender tail, nomadically roaming inland arid woodlands.',
    image: 'princess-parrot.jpg',
    audioDuration: '0:24',
    verified: true
  },
  {
    id: 'plains-wanderer',
    name: 'Plains-wanderer',
    scientificName: 'Pedionomus torquatus',
    status: 'Critically Endangered',
    statusClass: 'critical',
    habitat: 'Sparse native grasslands',
    activeTime: 'Mostly dusk and night',
    location: 'NSW and northern Victoria',
    whyItMatters:
      'It is the only surviving member of its taxonomic family and represents a unique evolutionary lineage.',
    didYouKnow:
      'Female Plains-wanderers are larger and more colourful, while males perform most incubation and chick-rearing duties.',
    description:
      'Small, ground-dwelling bird inhabiting sparse native grasslands, standing on tiptoes to peer over grass tussocks.',
    image: 'plains-wanderer.jpg',
    audioDuration: '0:31',
    verified: true
  },
  {
    id: 'rufous-scrub-bird',
    name: 'Rufous Scrub-bird',
    scientificName: 'Atrichornis rufescens',
    status: 'Endangered',
    statusClass: 'endangered',
    habitat: 'Wet subtropical rainforest',
    activeTime: 'Daytime (diurnal)',
    location: 'Eastern NSW and southern QLD',
    whyItMatters:
      'Protecting this species also preserves ancient rainforest habitat used by many other native animals.',
    didYouKnow:
      'The Rufous Scrub-bird is rarely seen, but its remarkably loud call can travel through dense rainforest vegetation.',
    description:
      'Extremely secretive ancient songbird of wet subtropical rainforests with an extraordinarily loud, ringing call.',
    image: 'rufous-scrub-bird.jpg',
    audioDuration: '0:14',
    verified: true
  },
  {
    id: 'malleefowl',
    name: 'Malleefowl',
    scientificName: 'Leipoa ocellata',
    status: 'Vulnerable',
    statusClass: 'vulnerable',
    habitat: 'Mallee woodland and shrubland',
    activeTime: 'Daytime (diurnal)',
    location: 'Southern and western Australia',
    whyItMatters:
      'Its nesting behaviour supports soil turnover and helps researchers monitor the health of mallee ecosystems.',
    didYouKnow:
      'Malleefowl regulate the temperature of their nesting mounds by repeatedly adding or removing soil and vegetation.',
    description:
      'Renowned mound-builder that regulates egg incubation temperatures using massive decomposing nest mounds.',
    image: 'malleefowl.jpg',
    audioDuration: '0:28',
    verified: true
  },
  {
    id: 'dusky-grasswren',
    name: 'Dusky Grasswren',
    scientificName: 'Amytornis purnelli',
    status: 'Least Concern',
    statusClass: 'least-concern',
    habitat: 'Rocky ranges and spinifex',
    activeTime: 'Daytime (diurnal)',
    location: 'Central Australia',
    whyItMatters:
      'Monitoring this species helps scientists understand how arid-zone birds respond to fire and habitat change.',
    didYouKnow:
      'Dusky Grasswrens usually run and hop between rocks rather than flying long distances.',
    description:
      'Highly agile terrestrial bird darting among fractured boulder ridges and spinifex clumps across arid ranges.',
    image: 'dusky-grasswren.jpg',
    audioDuration: '0:19',
    verified: true
  }
]

export const conservationFilters = [
  {
    id: 'all',
    label: 'All',
    count: 6
  },
  {
    id: 'critical',
    label: 'Critically Endangered',
    count: 2
  },
  {
    id: 'endangered',
    label: 'Endangered',
    count: 1
  },
  {
    id: 'vulnerable',
    label: 'Vulnerable',
    count: 2
  },
  {
    id: 'least-concern',
    label: 'Least Concern',
    count: 1
  }
]