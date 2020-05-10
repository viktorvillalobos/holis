<template>
  <div class="connect-happiness-chart">
    <h3>Análisis de sentimientos</h3>
    <p>Luego de muchos análisis, ahora puedes saber cómo se sienten las personas en tu empresa</p>
    <div class="columns">
      <div class="column">
        <div id="chart">
          <apexchart type="area" height="350" :options="chartOptions" :series="series"></apexchart>
        </div>
      </div>
      <div class="column is-narrow">
        <div class="connect-emotion-card">
          <img src="@/assets/happy.svg" alt="Happy person" />
          <div class="content">
            <span class="number">100</span>
            <div class="text">
              <p class="title">persona(s) felices</p>
              <p class="legend">en los últimos 7 días</p>
            </div>
          </div>
        </div>
        <div class="connect-emotion-card">
          <img src="@/assets/neutral.svg" alt="Neutral person" />
          <div class="content">
            <span class="number">3</span>
            <div class="text">
              <p class="title">persona(s) neutrales</p>
              <p class="legend">en los últimos 7 días</p>
            </div>
          </div>
        </div>
        <div class="connect-emotion-card">
          <img src="@/assets/unhappy.svg" alt="Unhappy person" />
          <div class="content">
            <span class="number">50</span>
            <div class="text">
              <p class="title">persona(s) infelices</p>
              <p class="legend">en los últimos 7 días</p>
            </div>
          </div>
        </div>
        <a href="#">¿Qué significa esto?</a>
      </div>
    </div>
    <ul class="card-actions">
      <li>
        <Btn dropdown primary>
          Exportar
          <template slot="options">
            <ul>
              <li>
                <a href="#">Excel</a>
              </li>
              <li>
                <a href="#">CSV</a>
              </li>
            </ul>
          </template>
        </Btn>
      </li>
    </ul>
  </div>
</template>
<script>
import Btn from "@/components/Btn";
export default {
  name: "HappinessChart",
  components: {
    Btn
  },
  data() {
    return {
      series: [
        {
          name: "felices",
          data: [31, 40, 28, 51, 42, 109, 100]
        },
        {
          name: "neutrales",
          data: [0, 5, 3, 8, 10, 1, 3]
        },
        {
          name: "infelices",
          data: [13, 24, 10, 8, 6, 35, 50]
        }
      ],
      chartOptions: {
        chart: {
          height: 350,
          type: "area"
        },
        dataLabels: {
          enabled: false
        },
        colors: ['#4cf25d', '#e0e0e0', '#ffa439'],
        stroke: {
          curve: "smooth"
        },
        xaxis: {
          type: "datetime",
          categories: [
            "2018-09-19T00:00:00.000Z",
            "2018-09-19T01:30:00.000Z",
            "2018-09-19T02:30:00.000Z",
            "2018-09-19T03:30:00.000Z",
            "2018-09-19T04:30:00.000Z",
            "2018-09-19T05:30:00.000Z",
            "2018-09-19T06:30:00.000Z"
          ]
        },
        tooltip: {
          x: {
            format: "dd/MM/yy HH:mm"
          }
        }
      }
    };
  }
};
</script>
<style lang="scss" scoped>
.connect-happiness-chart {
  padding: 15px;
  > p {
    font-size: 12px;
  }
}
.connect-emotion-card {
  margin-bottom: 11px;
  padding: 15px;
  width: 335px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 20px;
  border-radius: 8px;

  .title {
    font-weight: 400;
  }

  .content {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    .number {
      background: transparent;
      min-width: 0;
      width: auto;
      height: auto;
      line-height: 0.8;
      margin: 0;
      font-size: 28px;
    }

    .text {
      text-align: right;
    }

    .title {
      font-size: 15px;
    }

    .legend {
      font-size: 11px;
    }

    p {
      margin: 0;
    }
  }

  &:nth-child(1) {
    background-color: rgba(76, 242, 93, 0.8);
    .content {
      .number {
        font-size: 48px;
      }

      .title {
        font-size: 16px;
      }
    }
  }

  &:nth-child(2) {
    background-color: rgba(224, 224, 224, 0.6);
  }

  &:nth-child(3) {
    background-color: rgba(255, 164, 57, 0.6);
    margin-bottom: 0;
  }
}
</style>