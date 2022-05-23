<template>
  <section class="content">
    <div class="row">
      <div class="col-xl-6">
        <canvas id="myChart"></canvas>
      </div>
      <div class="col-xl-6">
        <div class="row">
          <div class="col total-col">
            <div class="total">
              <div class="total-header">
                Total
              </div>
              <div class="total-content">
                <div class="total-result">
                  {{ total }}
                </div>
              </div>

            </div>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <table class="table">
              <tr>
                <th>№</th>
                <th>заказ №</th>
                <th>стоимость, $</th>
                <th>срок поставки</th>
              </tr>
              <tr v-for="bid in listBids" :key="bid.id">
                <td>{{ bid.number }}</td>
                <td>{{ bid.bid_id }}</td>
                <td>{{ bid.price_usd }}</td>
                <td>{{ bid.delivery_time }}</td>
              </tr>
            </table>
          </div>
        </div>

      </div>

    </div>

  </section>
  <Pagination :total="totalPages" @pageChange="loadListBids"/>
</template>

<script>
import Pagination from '@/components/Pagination.vue'

export default {
  name: 'Home',
  data() {
    return {
      listBids: [],
      page: 1,
      totalPages: 0,
      total: 0
    }
  },
  components: {
    Pagination
  },
  created() {
    this.loadListBids(this.page)
  },
  methods: {
    async loadListBids(pageNumber) {
      this.listBids = await fetch(
          `${this.$store.getters.getServerUrl}?page=${pageNumber}`
      ).then(response => response.json()
      ).then(response => {
        this.totalPages = response.count_pages
        this.total = response.total
        return response.results
      })
      await this.getChat()
    },
    async getChat() {
      let chartStatus = Chart.getChart("myChart")
      if (!!chartStatus) {
        chartStatus.destroy();
      }
      const DATA_COUNT = this.listBids.length;
      const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

      const labels = []
      const dataSet = []

      this.listBids.forEach(function (el) {
        labels.push(el.delivery_time)
        dataSet.push(el.price_usd)
      })

      const data = {
        labels: labels,
        datasets: [
          {
            label: 'Стоимость заявки, $',
            data: dataSet,
            borderColor: 'blue',
            backgroundColor: 'blue',
          }
        ]
      };

      const ctx = document.getElementById('myChart').getContext('2d');
      const myChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });

    }
  }
}


</script>


<style>
.header {
  margin: 10px 0;
  min-height: 100px;
  background-color: #96f0a0;
  display: flex;
  align-items: center;
}

.logo {
  padding-left: 10px;
}

</style>
