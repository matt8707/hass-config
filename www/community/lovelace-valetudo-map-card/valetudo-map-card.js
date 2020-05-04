class ValetudoMapCard extends HTMLElement {
  constructor() {
    super();
    this.drawingMap = false;
    this.drawingControls = false;
    this.lastUpdatedMap = "";
    this.lastDrawnTheme = null;
    this.lastUpdatedControls = "";
    this.attachShadow({ mode: 'open' });
    this.lastValidRobotPosition = [];

    this.cardContainer = document.createElement('ha-card');
    this.cardContainer.id = 'lovelaceValetudoHaCard';
    this.cardContainerStyle = document.createElement('style');
    this.shadowRoot.appendChild(this.cardContainer);
    this.shadowRoot.appendChild(this.cardContainerStyle);

    this.cardHeader = document.createElement('div');
    this.cardHeader.setAttribute('class', 'card-header');
    this.cardTitle = document.createElement('div');
    this.cardTitle.setAttribute('class', 'name');
    this.cardHeader.appendChild(this.cardTitle);
    this.cardContainer.appendChild(this.cardHeader);

    this.entityWarning1 = document.createElement('hui-warning');
    this.entityWarning1.id = 'lovelaceValetudoWarning1HaCard';
    this.cardContainer.appendChild(this.entityWarning1);

    this.entityWarning2 = document.createElement('hui-warning');
    this.entityWarning2.id = 'lovelaceValetudoWarning2HaCard';
    this.cardContainer.appendChild(this.entityWarning2);

    this.mapContainer = document.createElement('div');
    this.mapContainer.id = 'lovelaceValetudoMapCard';
    this.mapContainerStyle = document.createElement('style');
    this.cardContainer.appendChild(this.mapContainer);
    this.cardContainer.appendChild(this.mapContainerStyle);

    this.controlContainer = document.createElement('div');
    this.controlContainer.id = 'lovelaceValetudoControlCard';
    this.controlContainerStyle = document.createElement('style');
    this.cardContainer.appendChild(this.controlContainer);
    this.cardContainer.appendChild(this.controlContainerStyle);
  };

  shouldDrawMap(state, theme) {
    return !this.drawingMap && (this.lastUpdatedMap != state.last_updated || this.lastDrawnTheme != theme);
  };

  shouldDrawControls(state) {
    return !this.drawingControls && this.lastUpdatedControls != state.last_updated;
  };

  calculateColor(container, ...colors) {
    for (let color of colors) {
      if (!color) continue;
      if (color.startsWith('--')) {
        let possibleColor = getComputedStyle(container).getPropertyValue(color);
        if (!possibleColor) continue;
        return possibleColor;
      };
      return color;
    };
  };

  isOutsideBounds(x, y, drawnMapCanvas, config) {
    return (x < this._config.crop.left) || (x > drawnMapCanvas.width) || (y < config.crop.top) || (y > drawnMapCanvas.height);
  };

  drawMap(mapContainer, mapData, mapHeight, mapWidth, floorColor, obstacleWeakColor, obstacleStrongColor, noGoAreaColor, virtualWallColor, pathColor, chargerColor, vacuumColor) {
    // Points to pixels
    const widthScale = 50 / this._config.map_scale;
    const heightScale = 50 / this._config.map_scale;
    const leftOffset = mapData.attributes.image.position.left * this._config.map_scale;
    const topOffset = mapData.attributes.image.position.top * this._config.map_scale;

    // Create all objects
    const containerContainer = document.createElement('div');
    containerContainer.id = 'lovelaceValetudoCard';

    const drawnMapContainer = document.createElement('div');
    const drawnMapCanvas = document.createElement('canvas');
    drawnMapCanvas.width = mapWidth * this._config.map_scale;
    drawnMapCanvas.height = mapHeight * this._config.map_scale;
    drawnMapContainer.style.zIndex = 1;
    drawnMapContainer.appendChild(drawnMapCanvas);

    const chargerContainer = document.createElement('div');
    const chargerHTML = document.createElement('ha-icon');
    if (this._config.show_dock && mapData.attributes.charger) {
      chargerHTML.icon = this._config.dock_icon || 'mdi:flash';
      chargerHTML.style.left = `${Math.floor(mapData.attributes.charger[0] / widthScale) - leftOffset - (12 * this._config.icon_scale)}px`;
      chargerHTML.style.top = `${Math.floor(mapData.attributes.charger[1] / heightScale) - topOffset - (12 * this._config.icon_scale)}px`;
      chargerHTML.style.color = chargerColor;
      chargerHTML.style.transform = `scale(${this._config.icon_scale}, ${this._config.icon_scale})`;
    };
    chargerContainer.style.zIndex = 2;
    chargerContainer.appendChild(chargerHTML);

    const pathContainer = document.createElement('div');
    const pathCanvas = document.createElement('canvas');
    pathCanvas.width = mapWidth * this._config.map_scale;
    pathCanvas.height = mapHeight * this._config.map_scale;
    pathContainer.style.zIndex = 3;
    pathContainer.appendChild(pathCanvas);

    const vacuumContainer = document.createElement('div');
    const vacuumHTML = document.createElement('ha-icon');

    let robotPosition = mapData.attributes.robot;
    if(!robotPosition) {
      robotPosition = this.lastValidRobotPosition;
    }

    if (this._config.show_vacuum && robotPosition) {
      this.lastValidRobotPosition = robotPosition;
      vacuumHTML.icon = this._config.vacuum_icon || 'mdi:robot-vacuum';
      vacuumHTML.style.color = vacuumColor;
      vacuumHTML.style.left = `${Math.floor(robotPosition[0] / widthScale) - leftOffset - (12 * this._config.icon_scale)}px`;
      vacuumHTML.style.top = `${Math.floor(robotPosition[1] / heightScale) - topOffset - (12 * this._config.icon_scale)}px`;
      vacuumHTML.style.transform = `scale(${this._config.icon_scale}, ${this._config.icon_scale})`;
    }
    vacuumContainer.style.zIndex = 4;
    vacuumContainer.appendChild(vacuumHTML);

    // Put objects in container
    containerContainer.appendChild(drawnMapContainer);
    containerContainer.appendChild(chargerContainer);
    containerContainer.appendChild(pathContainer);
    containerContainer.appendChild(vacuumContainer);

    const mapCtx = drawnMapCanvas.getContext("2d");
    mapCtx.strokeStyle = floorColor;
    mapCtx.lineWidth = 1;
    mapCtx.fillStyle = floorColor;
    mapCtx.beginPath();
    if (mapData.attributes.image.pixels.floor) {
      for (let item of mapData.attributes.image.pixels.floor) {
        let x = item[0] * this._config.map_scale;
        let y = item[1] * this._config.map_scale;
        if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
        mapCtx.fillRect(x, y, this._config.map_scale, this._config.map_scale);
      };
    };

    mapCtx.strokeStyle = obstacleStrongColor;
    mapCtx.lineWidth = 1;
    mapCtx.fillStyle = obstacleWeakColor;
    mapCtx.beginPath();
    if (mapData.attributes.image.pixels.obstacle_weak) {
      for (let item of mapData.attributes.image.pixels.obstacle_weak) {
        let x = item[0] * this._config.map_scale;
        let y = item[1] * this._config.map_scale;
        if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
        mapCtx.fillRect(x, y, this._config.map_scale, this._config.map_scale);
      };
    };

    mapCtx.strokeStyle = obstacleStrongColor;
    mapCtx.lineWidth = 1;
    mapCtx.fillStyle = obstacleStrongColor;
    mapCtx.beginPath();
    if (mapData.attributes.image.pixels.obstacle_weak) {
      for (let item of mapData.attributes.image.pixels.obstacle_strong) {
        let x = item[0] * this._config.map_scale;
        let y = item[1] * this._config.map_scale;
        if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
        mapCtx.fillRect(x, y, this._config.map_scale, this._config.map_scale);
      };
    };

    if (mapData.attributes.no_go_areas) {
      mapCtx.strokeStyle = noGoAreaColor;
      mapCtx.lineWidth = 1;
      mapCtx.fillStyle = noGoAreaColor;
      for (let item of mapData.attributes.no_go_areas) {
        mapCtx.beginPath();
        for (let i = 0; i < item.length; i+=2) {
          let x = Math.floor(item[i] / widthScale) - leftOffset;
          let y = Math.floor(item[i + 1] / heightScale) - topOffset;
          if (i == 0) {
            mapCtx.moveTo(x, y);
          } else {
            mapCtx.lineTo(x, y);
          }
          if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
        };
        mapCtx.fill();
      };
    };

    if (mapData.attributes.virtual_walls) {
      mapCtx.strokeStyle = virtualWallColor;
      mapCtx.lineWidth = this._config.virtual_wall_width || 1;
      mapCtx.beginPath();
      for (let item of mapData.attributes.virtual_walls) {
        let fromX = Math.floor(item[0] / widthScale) - leftOffset;
        let fromY = Math.floor(item[1] / heightScale) - topOffset;
        let toX = Math.floor(item[2] / widthScale) - leftOffset;
        let toY = Math.floor(item[3] / heightScale) - topOffset;
        if (this.isOutsideBounds(fromX, fromY, drawnMapCanvas, this._config)) continue;
        if (this.isOutsideBounds(toX, toY, drawnMapCanvas, this._config)) continue;
        mapCtx.moveTo(fromX, fromY);
        mapCtx.lineTo(toX, toY);
        mapCtx.stroke();
      };
    };
    
    if (mapData.attributes.path && mapData.attributes.path.points) {
      const pathCtx = pathCanvas.getContext("2d");
      pathCtx.strokeStyle = pathColor;
      pathCtx.lineWidth = this._config.path_width || 1;

      let first = true;
      let prevX = 0;
      let prevY = 0;
      let x = 0;
      let y = 0;
      pathCtx.beginPath();
      for (let i = 0; i < mapData.attributes.path.points.length; i++) {
        let item = mapData.attributes.path.points[i];
        if (!first) {
          prevX = x;
          prevY = y;
        };
        x = Math.floor((item[0]) / widthScale) - leftOffset;
        y = Math.floor((item[1]) / heightScale) - topOffset;
        if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
        if (first) {
          pathCtx.moveTo(x, y);
          first = false;
        } else {
          pathCtx.lineTo(x, y);
        };

      };

      if (this._config.show_path) pathCtx.stroke();

      // Update vacuum angle
      if (!first) {
        vacuumHTML.style.transform = `scale(${this._config.icon_scale}, ${this._config.icon_scale}) rotate(${(Math.atan2(y - prevY, x - prevX) * 180 / Math.PI) + 90}deg)`;
      };
    };

    // Put our newly generated map in there
    while (mapContainer.firstChild) {
      mapContainer.firstChild.remove();
    };
    mapContainer.appendChild(containerContainer);
  };

  setConfig(config) {
    this._config = Object.assign({}, config);

    if (this._config.title === undefined) this._config.title = "Vacuum";
    if (this._config.show_dock === undefined) this._config.show_dock = true;
    if (this._config.show_vacuum === undefined) this._config.show_vacuum = true;
    if (this._config.show_path === undefined) this._config.show_path = true;
    if (this._config.map_scale === undefined) this._config.map_scale = 1;
    if (this._config.icon_scale === undefined) this._config.icon_scale = 1;
    if (this._config.rotate === undefined) this._config.rotate = 0;
    if (Number(this._config.rotate)) this._config.rotate = `${this._config.rotate}deg`;
    if (this._config.crop !== Object(this._config.crop)) this._config.crop = {};
    if (this._config.crop.top === undefined) this._config.crop.top = 0;
    if (this._config.crop.bottom === undefined) this._config.crop.bottom = 0;
    if (this._config.crop.left === undefined) this._config.crop.left = 0;
    if (this._config.crop.right === undefined) this._config.crop.right = 0;
    if (this._config.min_height === undefined) this._config.min_height = 0;

    // Set card title and hide the header completely if the title is set to an empty value
    if (!this._config.title) {
        this.cardHeader.style.display = 'none';
    } else {
        this.cardHeader.style.display = 'block';
    };
    this.cardTitle.textContent = this._config.title;
  };

  set hass(hass) {
    this._hass = hass;
    const config = this._config;
    let mapEntity = this._hass.states[this._config.entity];
    let infoEntity = this._hass.states[this._config.vacuum_entity]

    let canDrawMap = true;
    let canDrawControls = true;

    if (!mapEntity || mapEntity['state'] == 'unavailable' || !mapEntity.attributes || !mapEntity.attributes.image) {
      canDrawMap = false;
    }

    if (!infoEntity || infoEntity['state'] == 'unavailable' || !infoEntity.attributes) {
      canDrawControls = false;
      // Reset last-updated to redraw as soon as element becomes availables
      this.lastUpdatedControls = ""
    }

    if (!canDrawMap && this._config.entity) {
      // Remove the map
      this.mapContainer.style.display = 'none';

      // Show the warning
      this.entityWarning1.textContent = `Entity not available: ${this._config.entity}`;
      this.entityWarning1.style.display = 'block';
    } else {
      this.entityWarning1.style.display = 'none';
      this.mapContainer.style.display = 'block';
    };

    if (!canDrawControls && this._config.vacuum_entity) {
      // Remove the controls
      this.controlContainer.style.display = 'none';

      // Show the warning
      this.entityWarning2.textContent = `Entity not available: ${this._config.vacuum_entity}`;
      this.entityWarning2.style.display = 'block';
    } else {
      this.entityWarning2.style.display = 'none';
      this.controlContainer.style.display = 'block';
    };

    if (canDrawMap) {
      // Calculate map height and width
      const mapWidth = mapEntity.attributes.image.dimensions.width - this._config.crop.right;
      const mapHeight = mapEntity.attributes.image.dimensions.height - this._config.crop.bottom;

      // Calculate desired container height
      let containerHeight = (mapHeight * this._config.map_scale) - this._config.crop.top
      let minHeight = this._config.min_height;

      // Want height based on container width
      if (String(this._config.min_height).endsWith('w')) {
        minHeight = this._config.min_height.slice(0, -1) * this.mapContainer.offsetWidth;
      }

      let containerMinHeightPadding = minHeight > containerHeight ? (minHeight - containerHeight) / 2 : 0;

      // Set container CSS
      this.mapContainerStyle.textContent = `
        #lovelaceValetudoMapCard {
          height: ${containerHeight}px;
          padding-top: ${containerMinHeightPadding}px;
          padding-bottom: ${containerMinHeightPadding}px;
          overflow: hidden;
        }
        #lovelaceValetudoCard {
          position: relative;
          margin-left: auto;
          margin-right: auto;
          width: ${mapWidth * this._config.map_scale}px;
          height: ${mapHeight * this._config.map_scale}px;
          transform: rotate(${this._config.rotate});
          top: -${this._config.crop.top}px;
          left: -${this._config.crop.left}px;
        }
        #lovelaceValetudoCard div {
          position: absolute;
          background-color: transparent;
          width: 100%;
          height: 100%;
        }
      `
      // Calculate colours
      const homeAssistant = document.getElementsByTagName('home-assistant')[0];
      const floorColor = this.calculateColor(homeAssistant, this._config.floor_color, '--valetudo-map-floor-color', '--secondary-background-color');
      const obstacleWeakColor = this.calculateColor(homeAssistant, this._config.obstacle_weak_color, '--valetudo-map-obstacle-weak-color', '--divider-color');
      const obstacleStrongColor = this.calculateColor(homeAssistant, this._config.obstacle_strong_color, '--valetudo-map-obstacle-strong-color', '--accent-color');
      const noGoAreaColor = this.calculateColor(homeAssistant, this._config.no_go_area_color, '--valetudo-no-go-area-color', '--accent-color');
      const virtualWallColor = this.calculateColor(homeAssistant, this._config.virtual_wall_color, '--valetudo-virtual-wall-color', '--accent-color');
      const pathColor = this.calculateColor(homeAssistant, this._config.path_color, '--valetudo-map-path-color', '--primary-text-color');
      const chargerColor = this.calculateColor(homeAssistant, this._config.dock_color, 'green');
      const vacuumColor = this.calculateColor(homeAssistant, this._config.vacuum_color, '--primary-text-color');

      // Don't redraw unnecessarily often
      if (this.shouldDrawMap(mapEntity, hass.selectedTheme)) {
        // Start drawing map
        this.drawingMap = true;

        this.drawMap(this.mapContainer, mapEntity, mapHeight, mapWidth, floorColor, obstacleWeakColor, obstacleStrongColor, noGoAreaColor, virtualWallColor, pathColor, chargerColor, vacuumColor);

        // Done drawing map
        this.lastUpdatedMap = mapEntity.last_updated;
        this.lastDrawnTheme = hass.selectedTheme;
        this.drawingMap = false;
      };
    };

    // Draw status and controls
    if (canDrawControls) {
      // Set control container CSS
      this.controlContainerStyle.textContent = `
        .flex-box {
          display: flex;
          justify-content: space-evenly;
        }
        paper-button {
          cursor: pointer;
          position: relative;
          display: inline-flex;
          align-items: center;
          padding: 8px;
        }
        ha-icon {
          width: 24px;
          height: 24px;
        }
      `

      let infoEntity = this._hass.states[this._config.vacuum_entity]
      if (this.shouldDrawControls(infoEntity)) {
        // Start drawing controls
        this.drawingControls = true;

        this.infoBox = document.createElement('div');
        this.infoBox.classList.add('flex-box');

        // Default to MQTT status, fall back to Home Assistant Xiaomi status
        let status = null;
        if (infoEntity && infoEntity.attributes && infoEntity.attributes.valetudo_state && infoEntity.attributes.valetudo_state.name) {
          status = infoEntity.attributes.valetudo_state.name;
        } else if (infoEntity && infoEntity.attributes && infoEntity.attributes.status) {
          status = infoEntity.attributes.status;
        }

        if (status) {
          const statusInfo = document.createElement('p');
          statusInfo.innerHTML = status;
          this.infoBox.appendChild(statusInfo)
        };

        if (infoEntity && infoEntity.attributes && infoEntity.attributes.battery_icon && infoEntity.attributes.battery_level) {
          const batteryData = document.createElement('div');
          batteryData.style.display = "flex"
          batteryData.style.alignItems = "center"
          const batteryIcon = document.createElement('ha-icon');
          const batteryText = document.createElement('span');
          batteryIcon.icon = infoEntity.attributes.battery_icon
          batteryText.innerHTML = " " + infoEntity.attributes.battery_level + " %"
          batteryData.appendChild(batteryIcon);
          batteryData.appendChild(batteryText);
          this.infoBox.appendChild(batteryData);
        };

        this.controlFlexBox = document.createElement('div');
        this.controlFlexBox.classList.add('flex-box');

        // Create controls
        const startButton = document.createElement('paper-button');
        const startIcon = document.createElement('ha-icon');
        const startRipple = document.createElement('paper-ripple');
        startIcon.icon = 'mdi:play';
        startButton.appendChild(startIcon);
        startButton.appendChild(startRipple);
        startButton.addEventListener('click', (event) => {
          this._hass.callService('vacuum', 'start', { entity_id: this._config.vacuum_entity }).then();
        });
        this.controlFlexBox.appendChild(startButton);

        const pauseButton = document.createElement('paper-button');
        const pauseIcon = document.createElement('ha-icon');
        const pauseRipple = document.createElement('paper-ripple');
        pauseIcon.icon = 'mdi:pause';
        pauseButton.appendChild(pauseIcon);
        pauseButton.appendChild(pauseRipple);
        pauseButton.addEventListener('click', (event) => {
          this._hass.callService('vacuum', 'pause', { entity_id: this._config.vacuum_entity }).then();
        });
        this.controlFlexBox.appendChild(pauseButton);

        const stopButton = document.createElement('paper-button');
        const stopIcon = document.createElement('ha-icon');
        const stopRipple = document.createElement('paper-ripple');
        stopIcon.icon = 'mdi:stop';
        stopButton.appendChild(stopIcon);
        stopButton.appendChild(stopRipple);
        stopButton.addEventListener('click', (event) => {
          this._hass.callService('vacuum', 'stop', { entity_id: this._config.vacuum_entity }).then();
        });
        this.controlFlexBox.appendChild(stopButton);

        const homeButton = document.createElement('paper-button');
        const homeIcon = document.createElement('ha-icon');
        const homeRipple = document.createElement('paper-ripple');
        homeIcon.icon = 'hass:home-map-marker';
        homeButton.appendChild(homeIcon);
        homeButton.appendChild(homeRipple);
        homeButton.addEventListener('click', (event) => {
          this._hass.callService('vacuum', 'return_to_base', { entity_id: this._config.vacuum_entity }).then();
        });
        this.controlFlexBox.appendChild(homeButton);

        // Replace existing controls
        while (this.controlContainer.firstChild) {
          this.controlContainer.firstChild.remove();
        };
        this.controlContainer.append(this.infoBox);
        this.controlContainer.append(this.controlFlexBox);

        // Done drawing controls
        this.lastUpdatedControls = infoEntity.last_updated;
        this.drawingControls = false;
      };
    };
  };

  getCardSize() {
    return 1;
  };
}

customElements.define('valetudo-map-card', ValetudoMapCard);
