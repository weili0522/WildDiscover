import json

new_data = [
  {
    "id": 1,
    "source": "UWA News",
    "publishedAt": "September 2024",
    "category": "Rediscoveries & Sightings",
    "title": "Largest known population of Night Parrots discovered in WA",
    "summary": "Indigenous rangers and researchers have discovered potentially the largest population of Night Parrots in the Ngururrpa Indigenous Protected Area, detecting the birds at 17 of 31 survey sites.",
    "image": "https://www.uwa.edu.au/news/-/media/Project/UWA/UWA/News/Article/2024/09/Night-Parrot-Ngururrpa.jpg",
    "externalUrl": "https://www.uwa.edu.au/news/Article/2024/September/Discovery-of-largest-known-population-of-night-parrots"
  },
  {
    "id": 2,
    "source": "CSIRO",
    "publishedAt": "February 2024",
    "category": "Ecosystem Science",
    "title": "World-first genome sequencing of the elusive Night Parrot",
    "summary": "Scientists have published the first fully annotated genome for the Night Parrot, providing a crucial tool to understand its biology and improve conservation efforts.",
    "image": "https://www.csiro.au/-/media/News-releases/2024/Night-Parrot-Genome/Night-Parrot-supplied-by-Nick-Leseberg.jpg",
    "externalUrl": "https://www.csiro.au/en/news/All/News/2024/February/Scientists-sequence-genome-of-elusive-Night-Parrot"
  },
  {
    "id": 3,
    "source": "Conservation Partners",
    "publishedAt": "August 2024",
    "category": "Rediscoveries & Sightings",
    "title": "Night Parrots detected 150km away from known populations in QLD",
    "summary": "Supported by government funding, conservation groups have successfully recorded Night Parrot calls, significantly expanding the known range of the critically endangered bird.",
    "image": "https://www.bushheritage.org.au/getmedia/12345678/Night-Parrot-Nick-Leseberg.jpg",
    "externalUrl": "https://conservationpartners.org.au/news/"
  },
  {
    "id": 4,
    "source": "Bush Heritage",
    "publishedAt": "July 2024",
    "category": "Habitat Protection",
    "title": "Protecting Pullen Pullen Reserve from feral predators",
    "summary": "Ongoing management at the Pullen Pullen Reserve continues to safeguard Night Parrot populations through intensive feral cat and fox management.",
    "image": "https://www.bushheritage.org.au/getmedia/abcdef12/Pullen-Pullen-landscape.jpg",
    "externalUrl": "https://www.bushheritage.org.au/places-we-protect/queensland/pullen-pullen"
  },
  {
    "id": 5,
    "source": "WWF Australia",
    "publishedAt": "October 2024",
    "category": "Policy Updates",
    "title": "New acoustic monitoring arrays deployed in the Great Sandy Desert",
    "summary": "Indigenous Desert Alliance and WWF have partnered to deploy massive acoustic sensor networks to identify new spinifex habitats for endangered species.",
    "image": "https://www.wwf.org.au/images/content/night-parrot-acoustic.jpg",
    "externalUrl": "https://wwf.org.au/news/"
  }
]

with open('frontend/src/mocks/mockNewsData.json', 'w') as f:
    json.dump(new_data, f, indent=2)
