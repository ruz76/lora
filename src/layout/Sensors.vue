<template>
    <div>
        <vue-tree-list
          @click="onClick"
          :model="data"
          v-bind:default-expanded="true">
        </vue-tree-list>
    </div>
</template>
<script>
  import { VueTreeList, Tree, TreeNode } from 'vue-tree-list'
  export default {
    components: {
      VueTreeList
    },
    data () {
      return {
        data: new Tree([])
      }
    },
    methods: {

      onClick (params) {
        this.$root.$emit("switchToSensor", params.id);
      }
    },

    mounted() {
      this.$root.$on("sensorsListChanged", sensors => {
        let sensorsCount = sensors.length;
        let currentData = new Tree([]);
        for (let i = 0; i < sensorsCount; i++) {
          let sensor = {
            name: sensors[i].title,
            id: i,
            pid: 0,
            dragDisabled: true,
            addTreeNodeDisabled: true,
            addLeafNodeDisabled: true,
            editNodeDisabled: true,
            delNodeDisabled: true,
            children: [],
          }
          let sensorNode = new TreeNode(sensor);
          if (!currentData.children) currentData.children = [];
          currentData.addChildren(sensorNode);
        }
        this.data = currentData;
      });
    },

  }
</script>
<style lang="less" rel="stylesheet/less">
  .vtl {
    .vtl-drag-disabled {
      /*background-color: #d0cfcf;
      &:hover {
        background-color: #d0cfcf;
      }*/
    }
    .vtl-disabled {
      //background-color: #d0cfcf;
    }
  }
</style>

<style lang="less" rel="stylesheet/less" scoped>
  .icon {
    &:hover {
      cursor: pointer;
    }
  }
</style>
