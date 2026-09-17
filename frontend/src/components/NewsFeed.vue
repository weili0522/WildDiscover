<script setup>
import { computed, ref } from 'vue'
import newsData from '../mocks/mockNewsData.json'

import nightParrotImage from '../assets/night-parrot.jpg'
import princessParrotImage from '../assets/princess-parrot.jpg'
import plainsWandererImage from '../assets/plains-wanderer.jpg'
import rufousScrubBirdImage from '../assets/rufous-scrub-bird.jpg'
import heroImage from '../assets/hero.jpg'
import sightingQueenslandImage from '../assets/sighting-queensland.jpg'
import sightingPilbaraImage from '../assets/sighting-pilbara.jpg'

const imageMap = {
  'night-parrot': nightParrotImage,
  'princess-parrot': princessParrotImage,
  'plains-wanderer': plainsWandererImage,
  'rufous-scrub-bird': rufousScrubBirdImage,
  'spinifex': heroImage,
  'sighting-queensland': sightingQueenslandImage,
  'sighting-pilbara': sightingPilbaraImage
}

const categories = [
  'All News',
  'Rediscoveries & Sightings',
  'Ecosystem Science',
  'Habitat Protection',
  'Policy Updates'
]

const selectedCategory = ref('All News')

const filteredNews = computed(() => {
  if (selectedCategory.value === 'All News') {
    return newsData
  }

  return newsData.filter(
    article => article.category === selectedCategory.value
  )
})

function getArticleImage(imageName) {
  return imageMap[imageName] || heroImage
}
</script>

<template>
  <section class="news-feed">
    <div class="category-tabs" aria-label="News categories">
      <button
        v-for="category in categories"
        :key="category"
        type="button"
        class="category-button"
        :class="{ active: selectedCategory === category }"
        @click="selectedCategory = category"
      >
        {{ category }}
      </button>
    </div>

    

    <div v-if="filteredNews.length" class="news-grid">
      <article
        v-for="article in filteredNews"
        :key="article.id"
        class="news-card"
      >
        <div class="news-content">
          <div class="article-meta">
            <span class="source">{{ article.source }}</span>
            <span>·</span>
            <span>{{ article.publishedAt }}</span>
            <span class="category-badge">{{ article.category }}</span>
          </div>

          <h2>{{ article.title }}</h2>

          <p>{{ article.summary }}</p>

          <a
            :href="article.externalUrl"
            class="read-link"
            target="_blank"
            rel="noopener noreferrer"
          >
            Read Full Story ↗
          </a>
        </div>

        <img
          :src="getArticleImage(article.image)"
          :alt="`${article.title} thumbnail`"
          class="news-thumbnail"
        />
      </article>
    </div>

    <div v-else class="empty-state">
      No news is available in this category.
    </div>
  </section>
</template>

<style scoped>
.news-feed {
  min-width: 0;
}

.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px;
  border: 1px solid #e3e9e5;
  border-radius: 12px;
  background: #ffffff;
}

.category-button {
  padding: 9px 14px;
  border: 0;
  border-radius: 20px;
  background: transparent;
  color: #5e6c65;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.category-button:hover {
  background: #edf6f1;
  color: #176b48;
}

.category-button.active {
  background: #176b48;
  color: #ffffff;
}

.update-status {
  display: flex;
  align-items: center;
  gap: 7px;
  margin: 10px 4px 16px;
  color: #6e7e75;
  font-size: 14px;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #50bd8a;
}

.news-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}

.news-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 132px;
  gap: 20px;
  align-items: center;
  min-height: 155px;
  padding: 20px;
  border: 1px solid #e2e8e4;
  border-radius: 13px;
  background: #ffffff;
  box-shadow: 0 5px 18px rgb(30 78 57 / 4%);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.news-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 9px 24px rgb(30 78 57 / 8%);
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 7px;
  margin-bottom: 10px;
  color: #7a8881;
  font-size: 14px;
}

.source {
  color: #2c7254;
  font-weight: 800;
}

.category-badge {
  padding: 5px 9px;
  border-radius: 16px;
  background: #e5f7ed;
  color: #27805a;
  font-weight: 700;
}

.news-content h2 {
  margin: 0 0 8px;
  color: #203f31;
  font-size: 20px;
  line-height: 1.35;
}

.news-content p {
  margin: 0 0 12px;
  color: #68766f;
  font-size: 16px;
  line-height: 1.55;
}

.read-link {
  color: #1d704e;
  font-size: 15px;
  font-weight: 800;
  text-decoration: none;
}

.read-link:hover {
  text-decoration: underline;
}

.news-thumbnail {
  width: 132px;
  height: 104px;
  border-radius: 10px;
  object-fit: cover;
}

.empty-state {
  padding: 48px 20px;
  border: 1px dashed #cad7d0;
  border-radius: 12px;
  background: white;
  color: #68766f;
  text-align: center;
}

@media (max-width: 700px) {
  .news-card {
    grid-template-columns: 1fr;
  }

  .news-thumbnail {
    grid-row: 1;
    width: 100%;
    height: 190px;
  }

  .category-tabs {
    overflow-x: auto;
    flex-wrap: nowrap;
  }

  .category-button {
    flex-shrink: 0;
  }
}
</style>