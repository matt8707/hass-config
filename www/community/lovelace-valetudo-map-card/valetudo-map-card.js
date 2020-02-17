class ValetudoMapCard extends HTMLElement {
  constructor() {
    super();
    this.drawing = false;
    this.lastUpdated = "";
    this.attachShadow({ mode: 'open' });
    this.lastValidRobotPosition = [];

    this.cardContainer = document.createElement('ha-card');
    this.cardContainerStyle = document.createElement('style');
    this.shadowRoot.appendChild(this.cardContainer);
    this.shadowRoot.appendChild(this.cardContainerStyle);
  };

  shouldDraw(state) {
    return !this.drawing && this.lastUpdated != state.last_updated;
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

  isOutsideBounds(x, y, mapCanvas, config) {
    return (x < this._config.crop.left) || (x > mapCanvas.width) || (y < config.crop.top) || (y > mapCanvas.height);
  };

  drawMap(cardContainer, mapData, mapHeight, mapWidth, floorColor, obstacleWeakColor, obstacleStrongColor, noGoAreaColor, virtualWallColor, pathColor, chargerColor, vacuumColor) {
    // We're drawing
    this.drawing = true;

    // Points to pixels
    const widthScale = 50 / this._config.map_scale;
    const heightScale = 50 / this._config.map_scale;
    const leftOffset = mapData.attributes.image.position.left * this._config.map_scale;
    const topOffset = mapData.attributes.image.position.top * this._config.map_scale;

    // Create all objects
    const containerContainer = document.createElement('div');
    containerContainer.id = 'lovelaceValetudoCard';

    const mapContainer = document.createElement('div');
    const mapCanvas = document.createElement('canvas');
    mapCanvas.width = mapWidth * this._config.map_scale;
    mapCanvas.height = mapHeight * this._config.map_scale;
    mapContainer.style.zIndex = 1;
    mapContainer.appendChild(mapCanvas);

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
    containerContainer.appendChild(mapContainer);
    containerContainer.appendChild(chargerContainer);
    containerContainer.appendChild(pathContainer);
    containerContainer.appendChild(vacuumContainer);

    const mapCtx = mapCanvas.getContext("2d");
    mapCtx.strokeStyle = floorColor;
    mapCtx.lineWidth = 1;
    mapCtx.fillStyle = floorColor;
    mapCtx.beginPath();
    if (mapData.attributes.image.pixels.floor) {
      for (let item of mapData.attributes.image.pixels.floor) {
        let x = item[0] * this._config.map_scale;
        let y = item[1] * this._config.map_scale;
        if (this.isOutsideBounds(x, y, mapCanvas, this._config)) continue;
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
        if (this.isOutsideBounds(x, y, mapCanvas, this._config)) continue;
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
        if (this.isOutsideBounds(x, y, mapCanvas, this._config)) continue;
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
          if (this.isOutsideBounds(x, y, mapCanvas, this._config)) continue;
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
        if (this.isOutsideBounds(fromX, fromY, mapCanvas, this._config)) continue;
        if (this.isOutsideBounds(toX, toY, mapCanvas, this._config)) continue;
        mapCtx.moveTo(fromX, fromY);
        mapCtx.lineTo(toX, toY);
        mapCtx.stroke();
      };
    };
    
    if (mapData.attributes.path.points) {
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
        if (this.isOutsideBounds(x, y, mapCanvas, this._config)) continue;
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
    while (cardContainer.firstChild) {
      cardContainer.firstChild.remove();
    };
    cardContainer.appendChild(containerContainer);

    // We're done drawing
    this.drawing = false;
  };

  setConfig(config) {
    if (config.show_dock === undefined) config.show_dock = true;
    if (config.show_vacuum === undefined) config.show_vacuum = true;
    if (config.show_path === undefined) config.show_path = true;
    if (config.map_scale === undefined) config.map_scale = 1;
    if (config.icon_scale === undefined) config.icon_scale = 1;
    if (config.rotate === undefined) config.rotate = 0;
    if (Number(config.rotate)) config.rotate = `${config.rotate}deg`;
    if (config.crop !== Object(config.crop)) config.crop = {};
    if (config.crop.top === undefined) config.crop.top = 0;
    if (config.crop.bottom === undefined) config.crop.bottom = 0;
    if (config.crop.left === undefined) config.crop.left = 0;
    if (config.crop.right === undefined) config.crop.right = 0;
    if (config.min_height === undefined) config.min_height = 0;

    this._config = config;
  };

  set hass(hass) {
    this._hass = hass;
    const config = this._config;
    let mapEntity = this._hass.states[this._config.entity];
    if (!mapEntity || mapEntity['state'] == 'unavailable' || !mapEntity.attributes || !mapEntity.attributes.image) {
      let warning = document.createElement('hui-warning');
      warning.textContent = `Entity not available: ${this._config.entity}`;
      while (this.shadowRoot.firstChild) {
        this.shadowRoot.firstChild.remove();
      };
      this.shadowRoot.appendChild(warning);
      return;
    };

    // Calculate map height and width
    const mapWidth = mapEntity.attributes.image.dimensions.width - this._config.crop.right;
    const mapHeight = mapEntity.attributes.image.dimensions.height - this._config.crop.bottom;

    // Calculate desired container height
    let containerHeight = (mapHeight * this._config.map_scale) - this._config.crop.top
    let minHeight = this._config.min_height;

    // Want height based on container width
    if (String(this._config.min_height).endsWith('w')) {
        minHeight = this._config.min_height.slice(0, -1) * this.cardContainer.offsetWidth;
    }

    let containerMinHeightPadding = minHeight > containerHeight ? (minHeight - containerHeight) / 2 : 0;

    // Set container CSS
    this.cardContainerStyle.textContent = `
      ha-card {
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
    // Don't draw unnecessarily often
    if (!this.shouldDraw(mapEntity)) return;

    this.lastUpdated = mapEntity.last_updated;

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

    this.drawMap(this.cardContainer, mapEntity, mapHeight, mapWidth, floorColor, obstacleWeakColor, obstacleStrongColor, noGoAreaColor, virtualWallColor, pathColor, chargerColor, vacuumColor);
  };

  getCardSize() {
    return 1;
  };
}

customElements.define('valetudo-map-card', ValetudoMapCard);
