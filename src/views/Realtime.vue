<template>
  <div>
    <div>
      <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      </base-header>
    </div>
    <div class="container-fluid">
      <!--Tables-->
      <div class="row">
        <div class="col-xl-12 mb-5 mb-xl-0">
          <div class="mt--7">
            <p>The location error is refreshed every 5 second. Last refresh {{currentDate}}</p>
            <base-dropdown>
              <base-button slot="title" type="secondary" class="dropdown-toggle">Select history count</base-button>
              <a
                  class="dropdown-item"
                  v-for="(count, index) in recordscounts"
                  :key="`${index}`"
                  v-on:click="switchToRecordCount(`${index}`)"
              >{{count}}</a>
            </base-dropdown>
            <input type="checkbox" v-on:change="setMapMove()" checked>Move the map to the current position</input>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-xl-12 mb-5 mb-xl-0">
          <div class="mt++10">
            <Map :sensor="activeSensor" maptype="realtime"/>
          </div>
        </div>
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
      Map,
    },
    data() {
      return {
        sensors: [],
        activeSensorId: 0,
        activeSensor: {title: "", info: ""},
        statType: 'avg',
        currentDate: null,
        recordscounts: [1, 5, 10, 20],
        activeRecordsCount: 10,
        movemap: true
      };
    },
    beforeDestroy() {
      clearInterval(this.polling);
    },
    created() {
      this.pollData();
    },
    computed: {

    },
    methods: {
      switchToRecordCount(index) {
        this.activeRecordsCount = this.recordscounts[index];
        this.getSensors(this.currentDate);
      },
      setMapMove() {
        this.$store.commit('changeMapMove');
      },
      pollData() {
        var current_component = this;
        this.polling = setInterval(() => {
          current_component.getSensors(current_component.currentDate);
        }, 5000);
      },
      getSensors(date) {
        var current_component = this;
        this.currentDate = new Date();
        axios
        .get(
            this.$store.state.serviceUrl + "?level=realtime&end=" + date + "&recordscount=" + this.activeRecordsCount
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
      }
    },
    mounted() {
      this.getSensors(this.currentDate);
      this.$root.$on("switchToSensor", (si) => {
        this.switchToSensor(si);
      });
      this.$root.$on("statChanged", (type) => {
        this.statType = type;
      });
    }
  };
</script>
<style></style>
