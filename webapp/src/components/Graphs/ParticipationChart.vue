<template>
  <div class="connect-participation-chart">
    <h3>Top de participación</h3>
    <p>Esas personas que siempre puedes ver en la cartelera o en los chats abiertos</p>
    <div class="columns">
      <div class="column is-narrow">
        <div class="connect-participation-chart-winner">
          <Avatar />
          <img src="@/assets/Achievement.svg" />
        </div>
      </div>
      <div class="column">
        <apexchart type="bar" height="210" :options="chartOptions" :series="series" />
      </div>
    </div>
    <ul class="card-actions">
      <li>
        <Btn flat primary>¡Anuncialo!</Btn>
      </li>
      <li>
        <Btn dropdown primary>Exportar
            <template slot="options">
                <ul>
                    <li><a href="#">Excel</a></li>
                    <li><a href="#">CSV</a></li>
                </ul>
            </template>
        </Btn>
      </li>
    </ul>
  </div>
</template>
<script>
import Btn from "@/components/Btn";
import Avatar from "@/components/Avatar";
export default {
  name: "PaticipationChart",
  components: {
    Avatar,
    Btn
  },
  data() {
    return {
      series: [
        {
          data: [400, 430, 448, 470, 540]
        }
      ],
      chartOptions: {
        chart: {
          type: "bar",
          height: 350
        },
        plotOptions: {
          bar: {
            horizontal: true
          }
        },
        dataLabels: {
          enabled: false
        },
        xaxis: {
          categories: [
            "Pablo el Feliz",
            "Carla Honrada",
            "Pedro el Escamoso",
            "Mateo el Perezoso",
            "Benito el Divertido"
          ]
        }
      }
    };
  }
};
</script>
<style lang="scss" scoped>
.connect-participation-chart {
  padding: 15px;
  > p {
    font-size: 12px;
  }
  &-winner {
    padding: 10px;
    width: 125px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;

    img {
      margin-top: 10px;
    }
  }
}
</style>