<template>
  <div class="insights-card">

    <h2>Night Parrot Insights</h2>

    <hr />

    <div class="insight-item">
      <div class="insight-label">
        RECENT SIGHTING
      </div>

      <p>
        Acoustic detection confirmed
        <strong>14 days ago</strong>
        (Pilbara Region)
      </p>
    </div>


    <div class="insight-item">
      <div class="insight-header">
        <span class="insight-label">
          HABITAT CONDITION
        </span>

        <span class="score">
          0.85
        </span>
      </div>

      <div class="condition-bar">
        <div class="condition-value"></div>
      </div>

      <div class="condition-text">
        Favorable (Intactness Score)
      </div>
    </div>


    <div class="insight-item">
      <div class="insight-label">
        PREDICTED SHIFT
      </div>

      <p>
        15 km South-West
        <br />
        Due to arid climate changes
      </p>
    </div>


    <div class="insight-item">
      <div class="insight-label">
        ELEVATION RANGE
      </div>

      <p>
        <strong>300m – 500m</strong>
        Above sea level
      </p>
    </div>

  </div>
</template>

<style scoped>
.insights-card {
  padding: 20px;

  background-color: #ffffff;

  border: 1px solid #e3e3e3;
  border-radius: 10px;
}

.insights-card h2 {
  margin: 0;

  color: #1f1f1f;

  font-size: 21px;
  font-weight: 600;
}

.insights-card hr {
  margin: 14px 0 18px;

  border: none;
  border-top: 1px solid #e3e3e3;
}

.insight-item {
  margin-bottom: 22px;
}

.insight-item:last-child {
  margin-bottom: 0;
}

.insight-label {
  display: block;

  margin-bottom: 5px;

  color: #555555;

  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.insight-item p {
  margin: 0;

  color: #333333;

  font-size: 13px;
  line-height: 1.4;
}

.insight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.score {
  color: #146c4a;

  font-size: 11px;
  font-weight: 600;
}

.condition-bar {
  width: 100%;
  height: 5px;

  margin: 5px 0 8px;

  overflow: hidden;

  background-color: #eeeeee;

  border-radius: 10px;
}

.condition-value {
  width: 85%;
  height: 100%;

  background-color: #146c4a;
}

.condition-text {
  color: #146c4a;

  font-size: 9px;
  font-weight: 600;
}
</style>