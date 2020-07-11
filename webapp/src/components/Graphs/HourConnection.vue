<template>
  <div class="connect-hour-connection">
    <h3>Horarios de conexión</h3>
    <p>En promedio de las personas de la empresa</p>
    <ul class="connect-hour-connection-list">
      <li>
        <span class="number">1</span>
        <div class="content">
          <span>
            <span>9</span>am -
            <span>6</span>pm
          </span>
          <p>El favorito</p>
        </div>
        <img :src="`${publicPath}img/clock-star.svg`" class="icon-clock-star" />
      </li>
      <li>
        <span class="number">2</span>
        <div class="content">
          <span>
            <span>9</span>am -
            <span>6</span>pm
          </span>
          <p>El no tan querido</p>
        </div>
      </li>
      <li>
        <span class="number">3</span>
        <div class="content">
          <span>
            <span>9</span>am -
            <span>6</span>pm
          </span>
          <p>El tercero en discordia</p>
        </div>
      </li>
    </ul>
    <ul class="card-actions">
      <li>
        <Btn flat primary>Ver más</Btn>
      </li>
    </ul>
  </div>
</template>
<script>
import Btn from '@/components/Btn'
export default {
  name: 'HourConnection',
  components: {
    Btn
  },
  data () {
    return {
      publicPath: process.env.BASE_URL
    }
  }
}
</script>
<style lang="scss" scoped>
.connect-hour-connection {
  padding: 15px;

  > p {
    font-size: 12px;
    margin-bottom: 15px;
  }

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
        color: #56ccf2;
        font-size: 48px;
      }

      img {
        width: 47px;
      }

      .content {
        width: calc(100% - 52px);
        margin-bottom: 0;
        > span {
          line-height: 1;
          font-size: 24px;

          span {
            font-size: 48px;
          }
        }
      }

      &:first-child {
        background-color: #b4edff;

        .number {
          background: #56ccf2;
          color: $light-gray;
        }

        .content {
          width: calc(100% - (52px + 47px));
        }
      }

      &:nth-child(2) {
        .number {
          font-size: 35px;
        }

        .content {
          > span {
            font-size: 24px;

            span {
              font-size: 35px;
            }
          }
        }
      }

      &:nth-child(3) {
        .number {
          font-size: 25px;
        }

        .content {
          > span {
            font-size: 18px;

            span {
              font-size: 25px;
            }
          }
        }
      }
    }
  }
}
</style>
