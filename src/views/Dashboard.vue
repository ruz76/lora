<template>
  <div>
    <div>
      <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      </base-header>
    </div>
    <div class="container-fluid">
      <!--Tables-->
      <div class="row">
        <div class="col-xl-6 mb-5 mb-xl-0">
          <div class="container-fluid mt--7">
          <Map :sensor="activeSensor"/>
          <div>
            <p>&nbsp;</p>
            <p>Time {{currentDate}}</p>
            <base-slider
                ref="dateSlider"
                v-model="dateSlider"
                :range="dateSliderRangeComputed"
                :step="1"
                :onchange="changeDate()"
            />
          </div>
          </div>
        </div>
        <div class="col-xl-6 mb-5 mb-xl-0">
          <!--Charts-->
          <div class="container-fluid mt--7">
            <div class="row">
              <div class="col-xl-12 mb-12 mb-xl-0">
                <card type="default" header-classes="bg-transparent">
                  <div slot="header" class="row align-items-center">
                    <div class="col">
                      <h6 class="text-light text-uppercase ls-1 mb-1">Location</h6>
                      <h5 class="h3 text-white mb-0">Location error in time</h5>
                    </div>
                  </div>
                  <line-chart
                      :height="350"
                      ref="distancesErrorChart"
                      :chart-data="distancesErrorChart.chartData"
                      :extra-options="distancesErrorChart.extraOptions"
                  >
                  </line-chart>

                </card>
              </div>

            </div>
            <div class="row">
              <div class="col-xl-12 mb-12 mb-xl-0">
                <p>&nbsp;</p>
              </div>
            </div>
            <div class="row">
              <div class="col-xl-12 mb-12 mb-xl-0">
                <card type="default" header-classes="bg-transparent">
                  <div slot="header" class="row align-items-center">
                    <div class="col">
                      <h6 class="text-light text-uppercase ls-1 mb-1">Measured</h6>
                      <h5 class="h3 text-white mb-0">Values in time</h5>
                    </div>
                  </div>
                  <line-chart
                      :height="350"
                      ref="measuredChart"
                      :chart-data="measuredChart.chartData"
                      :extra-options="measuredChart.extraOptions"
                  >
                  </line-chart>

                </card>
              </div>

            </div>
            <!-- End charts-->
          </div>
        </div>
        <!--End tables-->

      </div>

    </div>
  </div>
</template>
<script>
  // Charts
  import axios from "axios";
  import * as chartConfigs from '@/components/Charts/config';
  import LineChart from '@/components/Charts/LineChart';
  import BarChart from '@/components/Charts/BarChart';

  // Tables
  import SocialTrafficTable from './Dashboard/SocialTrafficTable';
  import PageVisitsTable from './Dashboard/PageVisitsTable';
  import Map from './Map.vue';

  export default {
    components: {
      LineChart,
      BarChart,
      PageVisitsTable,
      SocialTrafficTable,
      Map,
    },
    data() {
      return {
        sensors: [],
        activeSensorId: 0,
        activeSensor: {title: "", info: ""},
        statType: 'avg',
        dateSliderBefore: 31,
        dateSlider: 31,
        distancesErrorChart: {
          chartData: {
            datasets: [],
            labels: [],
          },
          extraOptions: chartConfigs.blueChartOptions,
        },
        measuredChart: {
          chartData: {
            datasets: [],
            labels: [],
          },
          extraOptions: chartConfigs.blueChartOptions,
        }
      };
    },
    computed: {
      // a computed getter
      dateSliderRangeComputed: function () {
        // `this` points to the vm instance
        return {min: 1, max: 31};
      },
      currentDate: function () {
        return "2020-01-" + Math.round(this.dateSlider);
      }
    },
    methods: {
      initDistancesErrorChart() {
        let cdata = this.activeSensor.avg_distance_error;
        switch (this.statType) {
          case 'avg':
            cdata = this.activeSensor.avg_distance_error;
            break;
          case 'min':
            cdata = this.activeSensor.min_distance_error;
            break;
          case 'max':
            cdata = this.activeSensor.max_distance_error;
            break;
          default:
            cdata = this.activeSensor.avg_distance_error;
        }
        let chartData = {
          datasets: [
            {
              label: 'Distance error',
              data: cdata
            }
          ],
          labels: this.activeSensor.times,
        };
        this.distancesErrorChart.chartData = chartData;
      },
      initMeasuredChart() {
        let chartData = {
          datasets: [
            {
              label: 'Temperature',
              data: this.activeSensor.measured
            }
          ],
          labels: this.activeSensor.times,
        };
        this.measuredChart.chartData = chartData;
      },
      changeDate() {
        //console.log(this.dateSlider);
        if (this.dateSlider !== this.dateSliderBefore) {
          this.dateSliderBefore = this.dateSlider;
          console.log(this.currentDate);
          this.getSensors(this.currentDate);
        }
      },
      getSensors(date) {
        var current_component = this;
        axios
        .get(
            "http://localhost/lora/get.php?end=" + date
        )
        .then(function (response) {
          console.log(response);
          if (response.status == "200") {
            current_component.sensors = response.data.sensors;
            current_component.activeSensor = current_component.sensors[current_component.activeSensorId];
            current_component.$root.$emit(
                "sensorChanged",
                current_component.activeSensor
            );
            current_component.$root.$emit("sensorsListChanged", current_component.sensors);
            current_component.initDistancesErrorChart();
            current_component.initMeasuredChart();
          } else {
            alert(response.data.error);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      switchToSensor(index) {
        this.activeSensorId = index;
        this.activeSensor = this.sensors[index];
        this.initDistancesErrorChart();
        this.initMeasuredChart();
        console.log("STS", this.activeSensor);
      }
    },
    mounted() {
      this.getSensors(this.currentDate);
      this.$root.$on("switchToSensor", (si) => {
        this.switchToSensor(si);
      });
      this.$root.$on("statChanged", (type) => {
        this.statType = type;
        this.initDistancesErrorChart();
      });
    }
  };
</script>
<style></style>
