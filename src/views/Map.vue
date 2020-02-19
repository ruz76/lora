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
        <!--// app map -->
        <div>
          <b-button @click="setStat('min')">Min</b-button>
          <b-button @click="setStat('max')">Max</b-button>
          <b-button @click="setStat('avg')">Avg</b-button>
            <b-button @click="testVuex()">Vuex</b-button>
        </div>
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
        getExtent(area) {
          let minx = Number.MAX_VALUE;
          let miny = Number.MAX_VALUE;
          let maxx = -Number.MAX_VALUE;
          let maxy = -Number.MAX_VALUE;
          let coordinates = area.features[0].geometry.coordinates[0];
          for(let i = 0; i < coordinates.length; i++){
            if (coordinates[i][0] < minx) {
              minx = coordinates[i][0];
            }
            if (coordinates[i][1] < miny) {
              miny = coordinates[i][1];
            }
            if (coordinates[i][0] > maxx) {
              maxx = coordinates[i][0];
            }
            if (coordinates[i][1] > maxy) {
              maxy = coordinates[i][1];
            }
          }
          return [minx, miny, maxx, maxy];
        },
        updateMap() {          
          if (this.sensor.coordinates != null) {
              console.log("UM", this.sensor, this.statType);
              this.drawCircle(this.sensor.coordinates, this.getStat());
              this.center = this.sensor.coordinates;
              this.zoom = 17;
          }
        },
        getStat() {
          switch (this.statType) {
            case 'avg':
              return this.sensor.avg_distance_error.reduce(function(p,c,i,a){return p + (c/a.length)},0);
            case 'min':
              return Math.min(...this.sensor.min_distance_error);
            case 'max':
              return Math.max(...this.sensor.max_distance_error);
            default:  
              return this.sensor.avg_distance_error.reduce(function(p,c,i,a){return p + (c/a.length)},0);
          }
        },
        setStat(type) {
          this.statType = type;
          this.updateMap();
          this.$root.$emit(
              "statChanged", type
          );
        },
        drawCircle(coordinates, radius) {
          let source = {
              cmp: 'vl-source-vector',
              staticFeatures: [{
                  type: 'Feature',
                  id: 'sensor-error',
                  geometry: {
                    type: 'Circle',
                    coordinates: coordinates,
                    radius: radius,
                  }
              }]
          }
          this.layers[0].source = source;
          this.layers[0].visible = true;
        },
        testVuex() {
          this.$store.commit('increment');
          this.$store.state.hovno = 5;
          console.log(this.$store.state.count);
          console.log(this.$store.state.hovno);
        }
    }
    export default {
        name: 'vld-demo-app',
        props: {
          sensor: {
            type: Object,
            default: null,
            description: "Data about current sensor."
          }
        },
        methods,
        mounted: function () {
            this.updateMap();
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
              staticFeatures: range(0, 100).map(i => {
                let coordinate = [
                  random(-50, 50),
                  random(-50, 50),
                ]

                return {
                  type: 'Feature',
                  id: 'random-cirlce-' + i,
                  geometry: {
                    type: 'Circle',
                    coordinates: coordinate,
                    radius: random(Math.pow(10, 5), Math.pow(10, 6)),
                  },
                }
              }),
            },
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
