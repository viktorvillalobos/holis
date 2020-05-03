<template>
  <div class="connect-reports">
    <div class="columns">
      <div class="column">
        <h2>Panel de inteligencia empresarial</h2>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <card outline>
          <hour-connection />
        </card>
      </div>
      <div class="column">
        <card outline>
          <WIP />
        </card>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <card outline>
          <WIP />
        </card>
      </div>
    </div>
  </div>
</template>
<script>
import WIP from "@/components/WIP";
import Card from "@/components/Card";

import HourConnection from "@/components/Graphs/HourConnection"
export default {
  name: "Reportes",
  components: {
    WIP,
    Card,
    HourConnection
  },
  data() {
    return {
      options: {
        chart: {
          id: "vuechart-example"
        },
        xaxis: {
          categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
        }
      },
      series: [
        {
          name: "series-1",
          data: [30, 40, 45, 50, 49, 60, 70, 91]
        }
      ]
    };
  }
};
</script>
<style lang="scss" scoped>
</style>