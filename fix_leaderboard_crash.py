import re

with open('frontend/src/components/LeaderboardView.vue', 'r') as f:
    content = f.read()

# Remove the current-user-section completely
section_pattern = r'<section class="current-user-section">.*?</section>'
content = re.sub(section_pattern, '', content, flags=re.DOTALL)

with open('frontend/src/components/LeaderboardView.vue', 'w') as f:
    f.write(content)
