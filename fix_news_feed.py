import re

with open('frontend/src/components/NewsFeed.vue', 'r') as f:
    content = f.read()

# Update script setup
script_pattern = r'<script setup>.*?</script>'
new_script = """<script setup>
import { computed, ref } from 'vue'
import newsData from '../mocks/mockNewsData.json'

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
</script>"""
content = re.sub(script_pattern, new_script, content, flags=re.DOTALL)

# Update the template to use absolute image URL
# It was using getArticleImage(article.image)
content = content.replace(':src="getArticleImage(article.image)"', ':src="article.image"')

# Add target="_blank" and href="article.externalUrl" if not present
content = content.replace('<a href="#" class="read-more">', '<a :href="article.externalUrl" target="_blank" rel="noopener noreferrer" class="read-more">')

with open('frontend/src/components/NewsFeed.vue', 'w') as f:
    f.write(content)
