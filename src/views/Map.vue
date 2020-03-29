<template xmlns:>
  <div id="mapapp" :class="[$options.name]">
    <!-- app map -->
    <vl-map v-if="mapVisible" class="map" ref="map" :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
            @click="clickCoordinate = $event.coordinate" @postcompose="onMapPostCompose"
            data-projection="EPSG:4326" @mounted="onMapMounted">
      <!-- map view aka ol.View -->
      <vl-view ref="view" :center.sync="center" :zoom.sync="zoom" :rotation.sync="rotation" v-on:update:center="sendExtent" v-on:update:zoom="sendExtent"></vl-view>

      <!-- base layers -->
      <vl-layer-tile v-for="layer in baseLayers" :key="layer.name" :id="layer.name" :visible="layer.visible">
        <component :is="'vl-source-' + layer.name" v-bind="layer"></component>
      </vl-layer-tile>
      <!--// base layers -->

      <!-- other layers from config -->
      <component v-for="layer in layers" :is="layer.cmp" v-if="layer.visible" :key="layer.id" v-bind="layer">
        <!-- add vl-source-* -->
        <component :is="layer.source.cmp" v-bind="layer.source">
          <!-- add static features to vl-source-vector if provided -->
          <vl-feature v-if="layer.source.staticFeatures && layer.source.staticFeatures.length"
                      v-for="feature in layer.source.staticFeatures" :key="feature.id"
                      :id="feature.id" :properties="feature.properties">
            <component :is="geometryTypeToCmpName(feature.geometry.type)" v-bind="feature.geometry"></component>
          </vl-feature>

          <!-- add inner source if provided (like vl-source-vector inside vl-source-cluster) -->
          <component v-if="layer.source.source" :is="layer.source.source.cmp" v-bind="layer.source.source">
            <!-- add static features to vl-source-vector if provided -->
            <vl-feature v-if="layer.source.source.staticFeatures && layer.source.source.staticFeatures.length"
                        v-for="feature in layer.source.source.staticFeatures" :key="feature.id"
                        :id="feature.id" :properties="feature.properties">
              <component :is="geometryTypeToCmpName(feature.geometry.type)" v-bind="feature.geometry"></component>
            </vl-feature>
          </component>
        </component>
        <!--// vl-source-* -->

        <!-- add style components if provided -->
        <!-- create vl-style-box or vl-style-func -->
        <component v-if="layer.style" v-for="(style, i) in layer.style" :key="i" :is="style.cmp" v-bind="style">
          <!-- create inner style components: vl-style-circle, vl-style-icon, vl-style-fill, vl-style-stroke & etc -->
          <component v-if="style.styles" v-for="(st, cmp) in style.styles" :key="cmp" :is="cmp" v-bind="st">
            <!-- vl-style-fill, vl-style-stroke if provided -->
            <vl-style-fill v-if="st.fill" v-bind="st.fill"></vl-style-fill>
            <vl-style-stroke v-if="st.stroke" v-bind="st.stroke"></vl-style-stroke>
          </component>
        </component>
        <!--// style -->
      </component>
      <!--// other layers -->

    </vl-map>

  </div>
</template>

<script>

  import {kebabCase, range, random, camelCase} from 'lodash'
  import {createStyle} from 'vuelayers/lib/ol-ext'
  import ScaleLine from 'ol/control/ScaleLine'
  import FullScreen from 'ol/control/FullScreen'
  import ZoomSlider from 'ol/control/ZoomSlider'

  import VueLayers from 'vuelayers'

  const methods = {
    camelCase,
    sendExtent(any) {
      this.$root.$emit('setMapExtent', this.$refs.view.$view.calculateExtent());
    },
    geometryTypeToCmpName(type) {
      return 'vl-geom-' + kebabCase(type)
    },
    selectFilter(feature) {
      return ['position-feature'].indexOf(feature.getId()) === -1
    },
    onUpdatePosition(coordinate) {
      this.deviceCoordinate = coordinate
    },
    onMapPostCompose({vectorContext, frameState}) {
      if (!this.$refs.marker || !this.$refs.marker.$feature) {
        return
      }

      const feature = this.$refs.marker.$feature
      if (!feature.getGeometry() || !feature.getStyle()) {
        return
      }

      const flashGeom = feature.getGeometry().clone()
      const duration = feature.get('duration')
      const elapsed = frameState.time - feature.get('start')
      const elapsedRatio = elapsed / duration
      const radius = easeInOut(elapsedRatio) * 35 + 5
      const opacity = easeInOut(1 - elapsedRatio)
      const fillOpacity = easeInOut(0.5 - elapsedRatio)

      vectorContext.setStyle(createStyle({
        imageRadius: radius,
        fillColor: [119, 170, 203, fillOpacity],
        strokeColor: [119, 170, 203, opacity],
        strokeWidth: 2 + opacity,
      }))

      vectorContext.drawGeometry(flashGeom)
      vectorContext.setStyle(feature.getStyle()(feature)[0])
      vectorContext.drawGeometry(feature.getGeometry())

      if (elapsed > duration) {
        feature.set('start', Date.now())
      }

      this.$refs.map.render()
    },
    onMapMounted() {
      // now ol.Map instance is ready and we can work with it directly
      this.$refs.map.$map.getControls().extend([
        new ScaleLine(),
        new FullScreen(),
        new ZoomSlider(),
      ])
    },
    // base layers
    showBaseLayer(name) {
      let layer = this.baseLayers.find(layer => layer.visible)
      if (layer != null) {
        layer.visible = false
      }

      layer = this.baseLayers.find(layer => layer.name === name)
      if (layer != null) {
        layer.visible = true
      }
    },
    updateMap: function () {
      if (this.sensor.coordinates != null) {
        let last = this.sensor.lon.length - 1;
        if (this.maptype === "realtime") {
          this.drawCircles(this.sensor.lon, this.sensor.lat, this.sensor.avg_distance_error);
          this.drawCircle(this.sensor.lon[0], this.sensor.lat[0], this.sensor.avg_distance_error[0]);
          if (this.$store.state.mapmove) {
            this.center = [this.sensor.lon[0], this.sensor.lat[0]];
            this.zoom = 15;
          }
        }
        if (this.maptype === "history") {
          switch (this.statType) {
            case 'avg':
              this.drawCircles(this.sensor.lon, this.sensor.lat, this.sensor.avg_distance_error);
              this.drawCircle(this.sensor.lon[last], this.sensor.lat[last], this.sensor.avg_distance_error[last]);
              break;
            case 'min':
              this.drawCircles(this.sensor.lon, this.sensor.lat, this.sensor.min_distance_error);
              this.drawCircle(this.sensor.lon[last], this.sensor.lat[last], this.sensor.min_distance_error[last]);
              break;
            case 'max':
              this.drawCircles(this.sensor.lon, this.sensor.lat, this.sensor.max_distance_error);
              this.drawCircle(this.sensor.lon[last], this.sensor.lat[last], this.sensor.max_distance_error[last]);
              break;
            default:
              this.drawCircles(this.sensor.lon, this.sensor.lat, this.sensor.avg_distance_error);
              this.drawCircle(this.sensor.lon[last], this.sensor.lat[last], this.sensor.avg_distance_error[last]);
          }
          if (this.$store.state.mapmove) {
            this.center = [this.sensor.lon[last], this.sensor.lat[last]];
            this.zoom = 15;
          }
        }
      }
    },
    getStat() {
      switch (this.statType) {
        case 'avg':
          return this.sensor.avg_distance_error.reduce(function (p, c, i, a) {
            return p + (c / a.length)
          }, 0);
        case 'min':
          return Math.min(...this.sensor.min_distance_error);
        case 'max':
          return Math.max(...this.sensor.max_distance_error);
        default:
          return this.sensor.avg_distance_error.reduce(function (p, c, i, a) {
            return p + (c / a.length)
          }, 0);
      }
    },
    drawCircle(lon, lat, radius) {
      let source = {
        cmp: 'vl-source-vector',
        staticFeatures: [{
          type: 'Feature',
          id: 'sensor-error-last',
          geometry: {
            type: 'Circle',
            coordinates: [lon, lat],
            radius: radius,
          }
        }]
      }
      this.layers[1].source = source;
      this.layers[1].visible = true;
    },
    drawCircles(lon, lat, radius) {
      let features = [];
      for (let i = 0; i < radius.length; i++) {
        let feature = {
          type: 'Feature',
          id: 'sensor-error-' + i,
          geometry: {
            type: 'Circle',
            coordinates: [lon[i], lat[i]],
            radius: radius[i],
          }
        }
        features.push(feature);
      }
      let source = {
        cmp: 'vl-source-vector',
        staticFeatures: features
      }
      this.layers[0].source = source;
      this.layers[0].visible = true;
    }
  }
  export default {
    name: 'vld-demo-app',
    props: {
      sensor: {
        type: Object,
        default: null,
        description: "Data about current sensor."
      },
      maptype: {
        type: String,
        default: "history",
        description: "Type of the map."
      }
    },
    methods,
    mounted: function () {
      this.updateMap();
      this.$root.$on("updateMap", (type) => {
        this.statType = type;
        this.updateMap();
      });
    },
    watch: {
      sensor: function (newVal) {
        this.sensor = newVal;
        this.updateMap();
      }
    },
    data() {
      return {
        statType: 'avg',
        name: '',
        nameState: null,
        submittedNames: [],
        center: [0, 0],
        zoom: 2,
        rotation: 0,
        clickCoordinate: undefined,
        selectedFeatures: [],
        deviceCoordinate: undefined,
        mapPanel: {
          tab: 'draw',
        },
        panelOpen: true,
        mapVisible: true,
        drawControls: [
          {
            type: 'polygon',
            label: 'Draw',
            icon: 'square-o',
          },
          {
            type: undefined,
            label: 'Finish',
            icon: 'times',
          },
        ],
        drawType: undefined,
        drawnFeatures: [],
        // base layers
        baseLayers: [
          {
            name: 'osm',
            title: 'OpenStreetMap',
            visible: true,
          }
        ],
        // layers config
        layers: [
          // Circles
          {
            id: 'circles',
            title: 'Circles',
            cmp: 'vl-layer-vector',
            visible: false,
            source: {
              cmp: 'vl-source-vector',
              staticFeatures: [],
            },
            style: [
              {
                cmp: 'vl-style-box',
                styles: {
                  'vl-style-fill': {
                    color: [255, 0, 0, 0],
                  },
                  'vl-style-stroke': {
                    color: '#219e46',
                    width: 2,
                  },
                },
              },
            ],
          },
          {
            id: 'circle-last',
            title: 'Circle-last',
            cmp: 'vl-layer-vector',
            renderMode: "image",
            visible: false,
            source: {
              cmp: 'vl-source-vector',
              staticFeatures: [],
            },
            style: [
              {
                cmp: 'vl-style-box',
                styles: {
                  'vl-style-fill': {
                    color: [255, 0, 0, 0],
                  },
                  'vl-style-stroke': {
                    color: '#ff0000',
                    width: 4,
                  },
                },
              },
            ],
          },
        ],
      }
    },
  }
</script>

<style lang="sass">
  @import ~bulma/sass/utilities/_all

  #mapapp
    width: 100%
    height: 600px
    margin: 0
    padding: 10

  #modal-save-area
    position: relative
    top: 10px

  .vld-demo-app
    position: relative

    .map
      height: 100%
      width: 100%

    .map-panel
      padding: 0
      position: absolute
      left: 20%
      transform: translateX(-20%)

      .panel-heading
        box-shadow: 0 .25em .5em transparentize($dark, 0.8)

      .panel-content
        background: $white
        box-shadow: 0 .25em .5em transparentize($dark, 0.8)

      .panel-block
        &.draw-panel
          .buttons
            .button
              display: block
              flex: 1 1 100%

      +tablet()
        position: absolute
        top: 5px
        right: 40px
        max-height: 500px
        width: 32em

    .base-layers-panel
      position: absolute
      left: 50%
      bottom: 20px
      transform: translateX(-50%)

    .feature-popup
      position: absolute
      left: -50px
      bottom: 12px
      width: 20em
      max-width: none

      &:after, &:before
        top: 100%
        border: solid transparent
        content: ' '
        height: 0
        width: 0
        position: absolute
        pointer-events: none
      &:after
        border-top-color: white
        border-width: 10px
        left: 48px
        margin-left: -10px
      &:before
        border-top-color: #cccccc
        border-width: 11px
        left: 48px
        margin-left: -11px

      .card-content
        max-height: 20em
        overflow: auto

      .content
        word-break: break-all
</style>
