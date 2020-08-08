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

  getLayers(attributes, type, maxCount) {
    let layers = [];
    for (let layer of attributes.layers) {
      if (layer.type == type) {
        layers.push(layer);
      };

      if (layers.length == maxCount) {
        break;
      };
    };

    return layers;
  };

  getEntities(attributes, type, maxCount) {
    let entities = [];
    for (let entity of attributes.entities) {
      if (entity.type == type) {
        entities.push(entity);
      };

      if (maxCount && entities.length == maxCount) {
        break;
      };
    };

    return entities;
  };

  getChargerInfo(attributes, legacyMode) {
    if (legacyMode) {
      if (!attributes.charger) {
        return null;
      };

      return [attributes.charger[0], attributes.charger[1]];
    } else {
      let layer = this.getEntities(attributes, 'charger_location', 1)[0];
      if (layer === undefined) {
        return null;
      };

      return [layer.points[0], layer.points[1]];
    };
  };

  getRobotInfo(attributes, legacyMode) {
    if (legacyMode) {
      // Rotation info not supported in legacy mode
      if (!attributes.robot) {
        return null;
      }

      return [attributes.robot[0], attributes.robot[1], 0];
    } else {
      let layer = this.getEntities(attributes, 'robot_position', 1)[0];
      if (layer === undefined) {
        return null;
      };

      return [layer.points[0], layer.points[1], layer.metaData.angle];
    };
  };

  getGoToInfo(attributes, legacyMode) {
    if (legacyMode) {
      return null; // not supported in legacy mode
    } else {
      let layer = this.getEntities(attributes, 'go_to_target', 1)[0];
      if (layer === undefined) {
        return null;
      };

      return [layer.points[0], layer.points[1]];
    };
  };

  getFloorPoints(attributes, legacyMode) {
    if (legacyMode) {
      if (!attributes.image.pixels.floor) {
        return null;
      };

      return attributes.image.pixels.floor.flat();
    } else {
      let layer = this.getLayers(attributes, 'floor', 1)[0];
      if (layer === undefined) {
        return null;
      };

      return layer.pixels;
    };
  };

  getSegments(attributes, legacyMode) {
    if (legacyMode) {
      return null;  // not supported in legacy mode
    } else {
      return this.getLayers(attributes, 'segment');
    };
  };

  getWallPoints(attributes, legacyMode) {
    if (legacyMode) {
      if (!attributes.image.pixels.obstacle_strong) {
        return null;
      };

      return attributes.image.pixels.obstacle_strong.flat();
    } else {
      let layer = this.getLayers(attributes, 'wall', 1)[0];
      if (layer === undefined) {
        return null;
      };

      return layer.pixels;
    };
  };

  getVirtualWallPoints(attributes, legacyMode) {
    if (legacyMode) {
      let virtual_walls = [];
      if (attributes.virtual_walls) {
        for (let item of attributes.virtual_walls) {
          virtual_walls.push({"points": item.flat()});
        };
      };

      return virtual_walls;
    } else {
      return this.getEntities(attributes, 'virtual_wall');
    };
  };

  getPathPoints(attributes, legacyMode) {
    if (legacyMode) {
      if (!attributes.path && !attributes.path.points) {
        return null;
      };

      return attributes.path.points.flat();
    } else {
      let layer = this.getEntities(attributes, 'path', 1)[0];
      if (layer === undefined) {
        return null;
      };

      return layer.points;
    };
  };

  getPredictedPathPoints(attributes, legacyMode) {
    if (legacyMode) {
      return null;  // not supported in legacyMode
    } else {
      let layer = this.getEntities(attributes, 'predicted_path', 1)[0];
      if (layer === undefined) {
        return null;
      };

      return layer.points;
    };
  };

  getNoGoAreas(attributes, legacyMode) {
    if (legacyMode) {
      let no_go_areas = [];
      if (attributes.no_go_areas) {
        for (let item of attributes.no_go_areas) {
          no_go_areas.push({"points": item.flat()});
        };
      };

      return no_go_areas;
    } else {
      return this.getEntities(attributes, 'no_go_area');
    };
  };

  drawMap(mapLegacyMode, mapContainer, mapData, mapHeight, mapWidth, floorColor, wallColor, currentlyCleanedZoneColor, noGoAreaColor, virtualWallColor, pathColor, chargerColor, vacuumColor, gotoTargetColor) {
    // Points to pixels
    let pixelSize = 50;
    if (!mapLegacyMode) {
      pixelSize = mapData.attributes.pixelSize;
    };

    const widthScale = pixelSize / this._config.map_scale;
    const heightScale = pixelSize / this._config.map_scale;

    let objectLeftOffset = 0;
    let objectTopOffset = 0;
    let mapLeftOffset = 0;
    let mapTopOffset = 0;
    if (mapLegacyMode) {
      objectLeftOffset = mapData.attributes.image.position.left * this._config.map_scale;
      objectTopOffset = mapData.attributes.image.position.top * this._config.map_scale;
    } else {
      let floorLayer = this.getLayers(mapData.attributes, 'floor', 1)[0];
      mapLeftOffset = (floorLayer.dimensions.x.min) - 1;
      mapTopOffset = (floorLayer.dimensions.y.min) - 1;
    };

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
    let chargerInfo = this.getChargerInfo(mapData.attributes, mapLegacyMode);
    if (this._config.show_dock && chargerInfo) {
      chargerHTML.style.position = 'absolute'; // Needed in Home Assistant 0.110.0 and up
      chargerHTML.icon = this._config.dock_icon || 'mdi:flash';
      chargerHTML.style.left = `${Math.floor(chargerInfo[0] / widthScale) - objectLeftOffset - mapLeftOffset - (12 * this._config.icon_scale)}px`;
      chargerHTML.style.top = `${Math.floor(chargerInfo[1] / heightScale) - objectTopOffset - mapTopOffset - (12 * this._config.icon_scale)}px`;
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

    let robotInfo = this.getRobotInfo(mapData.attributes, mapLegacyMode);
    if(!robotInfo) {
      robotInfo = this.lastValidRobotInfo;
    }

    if (this._config.show_vacuum && robotInfo) {
      this.lastValidRobotInfo = robotInfo;
      vacuumHTML.style.position = 'absolute'; // Needed in Home Assistant 0.110.0 and up
      vacuumHTML.icon = this._config.vacuum_icon || 'mdi:robot-vacuum';
      vacuumHTML.style.color = vacuumColor;
      vacuumHTML.style.left = `${Math.floor(robotInfo[0] / widthScale) - objectLeftOffset - mapLeftOffset - (12 * this._config.icon_scale)}px`;
      vacuumHTML.style.top = `${Math.floor(robotInfo[1] / heightScale) - objectTopOffset - mapTopOffset - (12 * this._config.icon_scale)}px`;
      vacuumHTML.style.transform = `scale(${this._config.icon_scale}, ${this._config.icon_scale})`;
    }
    vacuumContainer.style.zIndex = 4;
    vacuumContainer.appendChild(vacuumHTML);

    const goToTargetContainer = document.createElement('div');
    const goToTargetHTML = document.createElement('ha-icon');
    let goToInfo = this.getGoToInfo(mapData.attributes, mapLegacyMode);
    if (this._config.show_goto_target && goToInfo) {
      goToTargetHTML.style.position = 'absolute'; // Needed in Home Assistant 0.110.0 and up
      goToTargetHTML.icon = this._config.goto_target_icon || 'mdi:pin';
      goToTargetHTML.style.left = `${Math.floor(goToInfo[0] / widthScale) - objectLeftOffset - mapLeftOffset - (12 * this._config.icon_scale)}px`;
      goToTargetHTML.style.top = `${Math.floor(goToInfo[1] / heightScale) - objectTopOffset - mapTopOffset - (22 * this._config.icon_scale)}px`;
      goToTargetHTML.style.color = gotoTargetColor;
      goToTargetHTML.style.transform = `scale(${this._config.icon_scale}, ${this._config.icon_scale})`;
    };
    goToTargetContainer.style.zIndex = 5;
    goToTargetContainer.appendChild(goToTargetHTML);

    // Put objects in container
    containerContainer.appendChild(drawnMapContainer);
    containerContainer.appendChild(chargerContainer);
    containerContainer.appendChild(pathContainer);
    containerContainer.appendChild(vacuumContainer);
    containerContainer.appendChild(goToTargetContainer);

    const mapCtx = drawnMapCanvas.getContext("2d");
    if (this._config.show_floor) {
      mapCtx.globalAlpha = this._config.floor_opacity;

      mapCtx.strokeStyle = floorColor;
      mapCtx.lineWidth = 1;
      mapCtx.fillStyle = floorColor;
      mapCtx.beginPath();
      let floorPoints = this.getFloorPoints(mapData.attributes, mapLegacyMode);
      if (floorPoints) {
        for (let i = 0; i < floorPoints.length; i+=2) {
          let x = (floorPoints[i] * this._config.map_scale) - mapLeftOffset;
          let y = (floorPoints[i + 1] * this._config.map_scale) - mapTopOffset;
          if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
          mapCtx.fillRect(x, y, this._config.map_scale, this._config.map_scale);
        };
      };

      mapCtx.globalAlpha = 1;
    };

    let segmentAreas = this.getSegments(mapData.attributes, mapLegacyMode);
    if (segmentAreas && this._config.show_segments) {
      const colorFinder = new FourColorTheoremSolver(segmentAreas, 6);
      mapCtx.globalAlpha = this._config.segment_opacity;

      for (let item of segmentAreas) {
        mapCtx.strokeStyle = this._config.segment_colors[colorFinder.getColor(item.metaData.segmentId)];
        mapCtx.lineWidth = 1;
        mapCtx.fillStyle = this._config.segment_colors[colorFinder.getColor(item.metaData.segmentId)];
        mapCtx.beginPath();
        let segmentPoints = item['pixels'];
        if (segmentPoints) {
          for (let i = 0; i < segmentPoints.length; i+=2) {
            let x = (segmentPoints[i] * this._config.map_scale) - mapLeftOffset;
            let y = (segmentPoints[i + 1] * this._config.map_scale) - mapTopOffset;
            if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
            mapCtx.fillRect(x, y, this._config.map_scale, this._config.map_scale);
          };
        };
      };

      mapCtx.globalAlpha = 1;
    };

    if (this._config.show_walls) {
      mapCtx.globalAlpha = this._config.wall_opacity;

      mapCtx.strokeStyle = wallColor;
      mapCtx.lineWidth = 1;
      mapCtx.fillStyle = wallColor;
      mapCtx.beginPath();
      let wallPoints = this.getWallPoints(mapData.attributes, mapLegacyMode);
      if (wallPoints) {
        for (let i = 0; i < wallPoints.length; i+=2) {
          let x = (wallPoints[i] * this._config.map_scale) - mapLeftOffset;
          let y = (wallPoints[i + 1] * this._config.map_scale) - mapTopOffset;
          if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
          mapCtx.fillRect(x, y, this._config.map_scale, this._config.map_scale);
        };
      };

      mapCtx.globalAlpha = 1;
    };

    if (mapData.attributes.currently_cleaned_zones && this._config.show_currently_cleaned_zones) {
      mapCtx.globalAlpha = this._config.currently_cleaned_zone_opacity;

      mapCtx.strokeStyle = currentlyCleanedZoneColor;
      mapCtx.lineWidth = 1;
      mapCtx.fillStyle = currentlyCleanedZoneColor;
      mapCtx.beginPath();
      for (let item of mapData.attributes.currently_cleaned_zones) {
        let x1 = Math.floor(item[0] / widthScale) - objectLeftOffset - mapLeftOffset;
        let y1 = Math.floor(item[1] / heightScale) - objectTopOffset - mapTopOffset;
        let x2 = Math.floor(item[2] / widthScale) - objectLeftOffset - mapLeftOffset;
        let y2 = Math.floor(item[3] / heightScale) - objectTopOffset - mapTopOffset;
        if (this.isOutsideBounds(x1, y1, drawnMapCanvas, this._config)) continue;
        if (this.isOutsideBounds(x2, y2, drawnMapCanvas, this._config)) continue;
        mapCtx.fillRect(x1, y1, x2 - x1, y2 - y1);
      };

      mapCtx.globalAlpha = 1.0;
    };

    let noGoAreas = this.getNoGoAreas(mapData.attributes, mapLegacyMode);
    if (noGoAreas && this._config.show_no_go_areas) {

      mapCtx.strokeStyle = noGoAreaColor;
      mapCtx.lineWidth = 2;
      mapCtx.fillStyle = noGoAreaColor;
      for (let item of noGoAreas) {
        mapCtx.globalAlpha = this._config.no_go_area_opacity;
        mapCtx.beginPath();
        let points = item['points'];
        for (let i = 0; i < points.length; i+=2) {
          let x = Math.floor(points[i] / widthScale) - objectLeftOffset - mapLeftOffset;
          let y = Math.floor(points[i + 1] / heightScale) - objectTopOffset - mapTopOffset;
          if (i == 0) {
            mapCtx.moveTo(x, y);
          } else {
            mapCtx.lineTo(x, y);
          }
          if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
        };
        mapCtx.fill();

        if (this._config.show_no_go_area_border) {
          mapCtx.closePath();
          mapCtx.globalAlpha = 1.0;
          mapCtx.stroke();
        }
      };
      mapCtx.globalAlpha = 1.0;
    };

    let virtualWallPoints = this.getVirtualWallPoints(mapData.attributes, mapLegacyMode);
    if (virtualWallPoints && this._config.show_virtual_walls && this._config.virtual_wall_width > 0) {
      mapCtx.globalAlpha = this._config.virtual_wall_opacity;

      mapCtx.strokeStyle = virtualWallColor;
      mapCtx.lineWidth = this._config.virtual_wall_width;
      mapCtx.beginPath();
      for (let item of virtualWallPoints) {
        let fromX = Math.floor(item['points'][0] / widthScale) - objectLeftOffset - mapLeftOffset;
        let fromY = Math.floor(item['points'][1] / heightScale) - objectTopOffset - mapTopOffset;
        let toX = Math.floor(item['points'][2] / widthScale) - objectLeftOffset - mapLeftOffset;
        let toY = Math.floor(item['points'][3] / heightScale) - objectTopOffset - mapTopOffset;
        if (this.isOutsideBounds(fromX, fromY, drawnMapCanvas, this._config)) continue;
        if (this.isOutsideBounds(toX, toY, drawnMapCanvas, this._config)) continue;
        mapCtx.moveTo(fromX, fromY);
        mapCtx.lineTo(toX, toY);
        mapCtx.stroke();
      };

      mapCtx.globalAlpha = 1;
    };
    
    let pathPoints = this.getPathPoints(mapData.attributes, mapLegacyMode);
    if (pathPoints) {
      const pathCtx = pathCanvas.getContext("2d");
      pathCtx.globalAlpha = this._config.path_opacity;

      pathCtx.strokeStyle = pathColor;
      pathCtx.lineWidth = this._config.path_width;

      let x = 0;
      let y = 0;
      let first = true;
      pathCtx.beginPath();
      for (let i = 0; i < pathPoints.length; i+=2) {
        x = Math.floor((pathPoints[i]) / widthScale) - objectLeftOffset - mapLeftOffset;
        y = Math.floor((pathPoints[i + 1]) / heightScale) - objectTopOffset - mapTopOffset;
        if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
        if (first) {
          pathCtx.moveTo(x, y);
          first = false;
        } else {
          pathCtx.lineTo(x, y);
        };
      };

      if (this._config.show_path && this._config.path_width > 0) pathCtx.stroke();

      // Update vacuum angle
      vacuumHTML.style.transform = `scale(${this._config.icon_scale}, ${this._config.icon_scale}) rotate(${robotInfo[2]}deg)`;

      pathCtx.globalAlpha = 1;
    };

    let predictedPathPoints = this.getPredictedPathPoints(mapData.attributes, mapLegacyMode);
    if (predictedPathPoints) {
      const pathCtx = pathCanvas.getContext("2d");
      pathCtx.globalAlpha = this._config.path_opacity;

      pathCtx.setLineDash([5,3]);
      pathCtx.strokeStyle = pathColor;
      pathCtx.lineWidth = this._config.path_width;

      let x = 0;
      let y = 0;
      let first = true;
      pathCtx.beginPath();
      for (let i = 0; i < predictedPathPoints.length; i+=2) {
        x = Math.floor((predictedPathPoints[i]) / widthScale) - objectLeftOffset - mapLeftOffset;
        y = Math.floor((predictedPathPoints[i + 1]) / heightScale) - objectTopOffset - mapTopOffset;
        if (this.isOutsideBounds(x, y, drawnMapCanvas, this._config)) continue;
        if (first) {
          pathCtx.moveTo(x, y);
          first = false;
        } else {
          pathCtx.lineTo(x, y);
        };
      };

      if (this._config.show_path && this._config.path_width > 0 && this._config.show_predicted_path) pathCtx.stroke();

      pathCtx.globalAlpha = 1;
    };

    // Put our newly generated map in there
    while (mapContainer.firstChild) {
      mapContainer.firstChild.remove();
    };
    mapContainer.appendChild(containerContainer);
  };

  setConfig(config) {
    this._config = Object.assign({}, config);

    // Title settings
    if (this._config.title === undefined) this._config.title = "Vacuum";

    // Show settings
    if (this._config.show_floor === undefined) this._config.show_floor = true;
    if (this._config.show_dock === undefined) this._config.show_dock = true;
    if (this._config.show_vacuum === undefined) this._config.show_vacuum = true;
    if (this._config.show_walls === undefined) this._config.show_walls = true;
    if (this._config.show_currently_cleaned_zones === undefined) this._config.show_currently_cleaned_zones = true;
    if (this._config.show_no_go_areas === undefined) this._config.show_no_go_areas = true;
    if (this._config.show_virtual_walls === undefined) this._config.show_virtual_walls = true;
    if (this._config.show_path === undefined) this._config.show_path = true;
    if (this._config.show_no_go_area_border === undefined) this._config.show_no_go_area_border = true;
    if (this._config.show_predicted_path === undefined) this._config.show_predicted_path = true;
    if (this._config.show_goto_target === undefined) this._config.show_goto_target = true;
    if (this._config.show_segments === undefined) this._config.show_segments = true;
    if (this._config.show_status === undefined) this._config.show_status = true;
    if (this._config.show_battery_level === undefined) this._config.show_battery_level = true;

    // Show button settings
    if (this._config.show_start_button === undefined) this._config.show_start_button = true;
    if (this._config.show_pause_button === undefined) this._config.show_pause_button = true;
    if (this._config.show_stop_button === undefined) this._config.show_stop_button = true;
    if (this._config.show_home_button === undefined) this._config.show_home_button = true;

    // Width settings
    if (this._config.virtual_wall_width === undefined) this._config.virtual_wall_width = 1;
    if (this._config.path_width === undefined) this._config.path_width = 1;

    // Scale settings
    if (this._config.map_scale === undefined) this._config.map_scale = 1;
    if (this._config.icon_scale === undefined) this._config.icon_scale = 1;

    // Opacity settings
    if (this._config.floor_opacity === undefined) this._config.floor_opacity = 1;
    if (this._config.segment_opacity === undefined) this._config.segment_opacity = 0.75;
    if (this._config.wall_opacity === undefined) this._config.wall_opacity = 1;
    if (this._config.currently_cleaned_zone_opacity === undefined) this._config.currently_cleaned_zone_opacity = 0.5;
    if (this._config.no_go_area_opacity === undefined) this._config.no_go_area_opacity = 0.5;
    if (this._config.virtual_wall_opacity === undefined) this._config.virtual_wall_opacity = 1;
    if (this._config.path_opacity === undefined) this._config.path_opacity = 1;

    // Color segment settings
    if (this._config.segment_colors === undefined) this._config.segment_colors = [
      "#19A1A1",
      "#7AC037",
      "#DF5618",
      "#F7C841",
    ];

    // Rotation settings
    if (this._config.rotate === undefined) this._config.rotate = 0;
    if (Number(this._config.rotate)) this._config.rotate = `${this._config.rotate}deg`;

    // Crop settings
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

    // Set container card background color
    if (this._config.background_color) {
      this.cardContainer.style.background = this._config.background_color;
    } else {
      this.cardContainer.style.background = null;
    };

    if (!Array.isArray(this._config.custom_buttons)) {
      this._config.custom_buttons = [];
    };
  };

  set hass(hass) {
    // Home Assistant 0.110.0 may call this function with undefined sometimes if inside another card
    if (hass === undefined) return;

    this._hass = hass;
    const config = this._config;
    let mapEntity = this._hass.states[this._config.entity];
    let infoEntity = this._hass.states[this._config.vacuum_entity]

    let canDrawMap = false;
    let mapLegacyMode = false;
    let canDrawControls = true;

    if (mapEntity && mapEntity['state'] != 'unavailable' && mapEntity.attributes) {
        if (mapEntity.attributes.__class == 'ValetudoMap') {
            canDrawMap = true;
        } else if (mapEntity.attributes.image) {
            canDrawMap = true;
            mapLegacyMode = true;
        };
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
      let width;
      let height;
      if (mapLegacyMode) {
        width = mapEntity.attributes.image.dimensions.width;
        height = mapEntity.attributes.image.dimensions.height;
      } else {
        let floorLayer = this.getLayers(mapEntity.attributes, 'floor', 1)[0];
        width = (floorLayer.dimensions.x.max - floorLayer.dimensions.x.min) + 2;
        height = (floorLayer.dimensions.y.max - floorLayer.dimensions.y.min) + 2;
      };

      const mapWidth = width - this._config.crop.right;
      const mapHeight = height - this._config.crop.bottom;

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
      const wallColor = this.calculateColor(homeAssistant, this._config.wall_color, '--valetudo-map-wall-color', '--accent-color');
      const currentlyCleanedZoneColor = this.calculateColor(homeAssistant, this._config.currently_cleaned_zone_color, '--valetudo-currently_cleaned_zone_color', '--secondary-text-color');
      const noGoAreaColor = this.calculateColor(homeAssistant, this._config.no_go_area_color, '--valetudo-no-go-area-color', '--accent-color');
      const virtualWallColor = this.calculateColor(homeAssistant, this._config.virtual_wall_color, '--valetudo-virtual-wall-color', '--accent-color');
      const pathColor = this.calculateColor(homeAssistant, this._config.path_color, '--valetudo-map-path-color', '--primary-text-color');
      const chargerColor = this.calculateColor(homeAssistant, this._config.dock_color, 'green');
      const vacuumColor = this.calculateColor(homeAssistant, this._config.vacuum_color, '--primary-text-color');
      const gotoTargetColor = this.calculateColor(homeAssistant, this._config.goto_target_color, 'blue');

      // Don't redraw unnecessarily often
      if (this.shouldDrawMap(mapEntity, hass.selectedTheme)) {
        // Start drawing map
        this.drawingMap = true;

        this.drawMap(mapLegacyMode, this.mapContainer, mapEntity, mapHeight, mapWidth, floorColor, wallColor, currentlyCleanedZoneColor, noGoAreaColor, virtualWallColor, pathColor, chargerColor, vacuumColor, gotoTargetColor);

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
        if (mapLegacyMode) {
          if (infoEntity && infoEntity.attributes && infoEntity.attributes.valetudo_state && infoEntity.attributes.valetudo_state.name) {
            status = infoEntity.attributes.valetudo_state.name;
          } else if (infoEntity && infoEntity.attributes && infoEntity.attributes.status) {
            status = infoEntity.attributes.status;
          }
        } else {
          if (infoEntity && infoEntity.attributes && infoEntity.attributes.valetudo_state) {
            status = infoEntity.attributes.valetudo_state;
          } else if (infoEntity && infoEntity.attributes && infoEntity.attributes.status) {
            status = infoEntity.attributes.status;
          }
        }

        if (status && this._config.show_status) {
          const statusInfo = document.createElement('p');
          statusInfo.innerHTML = status;
          this.infoBox.appendChild(statusInfo)
        };

        if (infoEntity && infoEntity.attributes && infoEntity.attributes.battery_icon && infoEntity.attributes.battery_level && this._config.show_battery_level) {
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
        if (this._config.show_start_button) {
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
        }

        if (this._config.show_pause_button) {
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
        }

        if (this._config.show_stop_button) {
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
        }

        if (this._config.show_home_button) {
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
        }

        this.customControlFlexBox = document.createElement('div');
        this.customControlFlexBox.classList.add('flex-box');

        for (let i = 0; i < this._config.custom_buttons.length; i++) {
          let custom_button = this._config.custom_buttons[i];
          if (custom_button === Object(custom_button) && custom_button.service && custom_button.service.includes('.')) {
            const customButton = document.createElement('paper-button');
            const customButtonIcon = document.createElement('ha-icon');
            const customButtonRipple = document.createElement('paper-ripple');
            customButtonIcon.icon = custom_button["icon"] || 'mdi:radiobox-blank';
            customButton.appendChild(customButtonIcon);
            customButton.appendChild(customButtonRipple);
            customButton.addEventListener('click', (event) => {
              const args = custom_button["service"].split('.');
              if (custom_button.service_data) {
                this._hass.callService(args[0], args[1], custom_button.service_data).then();
              } else {
                this._hass.callService(args[0], args[1]).then();
              }
            });
            this.customControlFlexBox.appendChild(customButton);
          }
        }

        // Replace existing controls
        while (this.controlContainer.firstChild) {
          this.controlContainer.firstChild.remove();
        };
        this.controlContainer.append(this.infoBox);
        this.controlContainer.append(this.controlFlexBox);
        this.controlContainer.append(this.customControlFlexBox);

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

/**
 * This class (FourColorTheoremSolver) is taken from https://github.com/Hypfer/Valetudo/blob/890120c76930bb8941459a7e0d1baa0af8577d83/client/zone/js-modules/map-color-finder.js under the Apache 2 license.
 * See https://github.com/Hypfer/Valetudo/blob/890120c76930bb8941459a7e0d1baa0af8577d83/LICENSE for more information.
**/
class FourColorTheoremSolver {

  /**
   * This class determines how to color the different map segments contained in the given layers object.
   * The resulting color mapping will ensure that no two adjacent segments share the same color.
   * The map is evaluated row-by-row and column-by-column in order to find every pair of segments that are in "line of sight" of each other.
   * Each pair of segments is then represented as an edge in a graph where the vertices represent the segments themselves.
   * We then use a simple greedy algorithm to color all vertices so that none of its edges connect it to a vertex with the same color.
   * @param {Array<object>} layers - the data containing the map image (array of pixel offsets)
   * @param {number} resolution - Minimal resolution of the map scanner in pixels. Any number higher than one will lead to this many pixels being skipped when finding segment boundaries.
   * For example: If the robot measures 30cm in length/width, this should be set to 6, as no room can be smaller than 6 pixels. This of course implies that a pixel represents 5cm in the real world.
   */
  constructor(layers, resolution) {
      const prec = Math.floor(resolution);
      this.stepFunction = function (c) {
          return c + prec;
      };
      var preparedLayers = this.preprocessLayers(layers);
      if (preparedLayers !== undefined) {
          var mapData = this.createPixelToSegmentMapping(preparedLayers);
          this.areaGraph = this.buildGraph(mapData);
          this.areaGraph.colorAllVertices();
      }
  }

  /**
   * @param {number} segmentId - ID of the segment you want to get the color for.
   * The segment ID is extracted from the layer meta data in the first contructor parameter of this class.
   * @returns {number} The segment color, represented as an integer. Starts at 0 and goes up the minimal number of colors required to color the map without collisions.
   */
  getColor(segmentId) {
      if (this.areaGraph === undefined) {
          // Layer preprocessing seems to have failed. Just return a default value for any input.
          return 0;
      }

      var segmentFromGraph = this.areaGraph.getById(segmentId);
      if (segmentFromGraph) {
          return segmentFromGraph.color;
      } else {
          return 0;
      }
  }

  preprocessLayers(layers) {
      var internalSegments = [];
      var boundaries = {
          minX: Infinity,
          maxX: -Infinity,
          minY: Infinity,
          maxY: -Infinity
      };
      const filteredLayers = layers.filter(layer => layer.type === "segment");
      if (filteredLayers.length <= 0) {
          return undefined;
      }
      filteredLayers.forEach(layer => {
          var allPixels = [];
          for (let index = 0; index < layer.pixels.length - 1; index += 2) {
              var p = {
                  x: layer.pixels[index],
                  y: layer.pixels[index + 1]
              };
              this.setBoundaries(boundaries, p);
              allPixels.push(p);
          }
          internalSegments.push({
              segmentId: layer.metaData.segmentId,
              pixels: allPixels
          });
      });
      return {
          boundaries: boundaries,
          segments: internalSegments
      };
  }

  setBoundaries(res, pixel) {
      if (pixel.x < res.minX) {
          res.minX = pixel.x;
      }
      if (pixel.y < res.minY) {
          res.minY = pixel.y;
      }
      if (pixel.x > res.maxX) {
          res.maxX = pixel.x;
      }
      if (pixel.y > res.maxY) {
          res.maxY = pixel.y;
      }
  }

  createPixelToSegmentMapping(preparedLayers) {
      var pixelData = this.create2DArray(
          preparedLayers.boundaries.maxX + 1,
          preparedLayers.boundaries.maxY + 1
      );
      var segmentIds = [];
      preparedLayers.segments.forEach(seg => {
          segmentIds.push(seg.segmentId);
          seg.pixels.forEach(p => {
              pixelData[p.x][p.y] = seg.segmentId;
          });
      });
      return {
          map: pixelData,
          segmentIds: segmentIds,
          boundaries: preparedLayers.boundaries
      };
  }

  buildGraph(mapData) {
      var vertices = mapData.segmentIds.map(i => new MapAreaVertex(i));
      var graph = new MapAreaGraph(vertices);
      this.traverseMap(mapData.boundaries, mapData.map, (x, y, currentSegmentId, pixelData) => {
          var newSegmentId = pixelData[x][y];
          graph.connectVertices(currentSegmentId, newSegmentId);
          return newSegmentId !== undefined ? newSegmentId : currentSegmentId;
      });
      return graph;
  }

  traverseMap(boundaries, pixelData, func) {
      // row-first traversal
      for (let y = boundaries.minY; y <= boundaries.maxY; y = this.stepFunction(y)) {
          var rowFirstSegmentId = undefined;
          for (let x = boundaries.minX; x <= boundaries.maxX; x = this.stepFunction(x)) {
              rowFirstSegmentId = func(x, y, rowFirstSegmentId, pixelData);
          }
      }
      // column-first traversal
      for (let x = boundaries.minX; x <= boundaries.maxX; x = this.stepFunction(x)) {
          var colFirstSegmentId = undefined;
          for (let y = boundaries.minY; y <= boundaries.maxY; y = this.stepFunction(y)) {
              colFirstSegmentId = func(x, y, colFirstSegmentId, pixelData);
          }
      }
  }

  /**
   * Credit for this function goes to the authors of this StackOverflow answer: https://stackoverflow.com/a/966938
   */
  create2DArray(length) {
      var arr = new Array(length || 0),
          i = length;
      if (arguments.length > 1) {
          var args = Array.prototype.slice.call(arguments, 1);
          while (i--) {
              arr[length - 1 - i] = this.create2DArray.apply(this, args);
          }
      }
      return arr;
  }
}

/**
 * This class (MapAreaVertex) is taken from https://github.com/Hypfer/Valetudo/blob/890120c76930bb8941459a7e0d1baa0af8577d83/client/zone/js-modules/map-color-finder.js under the Apache 2 license.
 * See https://github.com/Hypfer/Valetudo/blob/890120c76930bb8941459a7e0d1baa0af8577d83/LICENSE for more information.
**/
class MapAreaVertex {
  constructor(id) {
      this.id = id;
      this.adjacentVertexIds = new Set();
      this.color = undefined;
  }

  appendVertex(vertexId) {
      if (vertexId !== undefined) {
          this.adjacentVertexIds.add(vertexId);
      }
  }
}

/**
 * This class (MapAreaGraph) is taken from https://github.com/Hypfer/Valetudo/blob/890120c76930bb8941459a7e0d1baa0af8577d83/client/zone/js-modules/map-color-finder.js under the Apache 2 license.
 * See https://github.com/Hypfer/Valetudo/blob/890120c76930bb8941459a7e0d1baa0af8577d83/LICENSE for more information.
**/
class MapAreaGraph {
  constructor(vertices) {
      this.vertices = vertices;
      this.vertexLookup = new Map();
      this.vertices.forEach(v => {
          this.vertexLookup.set(v.id, v);
      });
  }

  connectVertices(id1, id2) {
      if (id1 !== undefined && id2 !== undefined && id1 !== id2) {
          if (this.vertexLookup.has(id1)) {
              this.vertexLookup.get(id1).appendVertex(id2);
          }
          if (this.vertexLookup.has(id2)) {
              this.vertexLookup.get(id2).appendVertex(id1);
          }
      }
  }

  /**
   * Color the graphs vertices using a greedy algorithm. Any vertices that have already been assigned a color will not be changed.
   * Color assignment will start with the vertex that is connected with the highest number of edges. In most cases, this will
   * naturally lead to a distribution where only four colors are required for the whole graph. This is relevant for maps with a high
   * number of segments, as the naive, greedy algorithm tends to require a fifth color when starting coloring in a segment far from the map's center.
   */
  colorAllVertices() {
      this.vertices.sort((l, r) => r.adjacentVertexIds.size - l.adjacentVertexIds.size)
          .forEach(v => {
              if (v.adjacentVertexIds.size <= 0) {
                  v.color = 0;
              } else {
                  var adjs = this.getAdjacentVertices(v);
                  var existingColors = adjs
                      .filter(vert => vert.color !== undefined)
                      .map(vert => vert.color);
                  v.color = this.lowestColor(existingColors);
              }
          });
  }

  getAdjacentVertices(vertex) {
      return Array.from(vertex.adjacentVertexIds).map(id => this.getById(id));
  }

  getById(id) {
      return this.vertices.find(v => v.id === id);
  }

  lowestColor(colors) {
      if (colors.length <= 0) {
          return 0;
      }
      for (let index = 0; index < colors.length + 1; index++) {
          if (!colors.includes(index)) {
              return index;
          }
      }
  }
}
