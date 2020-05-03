<template>
  <div class="connect-hour-connection">
    <h3>Horarios de conexión</h3>
    <p>En promedio de las personas de la empresa</p>
    <ul class="connect-hour-connection-list">
      <li>
        <span class="number">1</span>
        <div class="content">
          <strong>
            <span>9</span>am -
            <span>6</span>pm
          </strong>
          <p>El favorito</p>
        </div>
        <img :src="`${publicPath}img/clock-star.svg`" class="icon" />
      </li>
      <li>
        <span class="number">2</span>
        <div class="content">
          <strong>
            <span>9</span>am -
            <span>6</span>pm
          </strong>
          <p>El no tan querido</p>
        </div>
      </li>
      <li>
        <span class="number">3</span>
        <div class="content">
          <strong>
            <span>9</span>am -
            <span>6</span>pm
          </strong>
          <p>El tercero en discordia</p>
        </div>
      </li>
    </ul>
    <ul class="card-actions">
        <li><Btn flat primary>Ver más</Btn></li>
    </ul>
  </div>
</template>
<script>
import Btn from "@/components/Btn";
export default {
  name: "HourConnection",
  components: {
    Btn
  },
  data() {
    return {
      publicPath: process.env.BASE_URL
    };
  }
};
</script>
<style lang="scss" scoped>
.connect-hour-connection {
  padding: 15px;

  &-list {
    width: 100%;
    li {
      display: inline-flex;
      width: 100%;
      justify-content: space-between;
      align-items: center;
      padding: 8px 15px;
      border-radius: 8px;

      .number {
        display: inline-flex;
        min-width: 0;
        width: 52px;
        height: 52px;
        background: #56ccf2;
        color: $light-gray;
        font-size: 48px;
      }

      img {
        width: 47px;
      }

      .content {
        width: calc(100% - 52px);
        margin-bottom: 0;
        strong {
          line-height: 1;
          font-size: 24px;

          span {
            font-size: 48px;
          }
        }
      }

      &:first-child {
        background-color: #b4edff;

        .content {
          width: calc(100% - (52px + 47px));
        }
      }
    }
  }
}
</style>