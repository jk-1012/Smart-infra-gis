import React, { useState, useRef, useCallback } from 'react';
import Map, { Source, Layer, NavigationControl } from 'react-map-gl';
import { Box, Paper, ToggleButton, ToggleButtonGroup } from '@mui/material';

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN || 'your-mapbox-token';

function MapView({ pipelines, projects, onMapClick, drawMode = false }) {
  const [viewState, setViewState] = useState({
    longitude: 72.5714,
    latitude: 23.0225,
    zoom: 12
  });

  const [visibleLayers, setVisibleLayers] = useState(['water', 'drainage', 'sewage']);
  const mapRef = useRef();

  const handleLayerToggle = (event, newLayers) => {
    setVisibleLayers(newLayers);
  };

  const pipelineLayer = {
    id: 'pipelines',
    type: 'line',
    paint: {
      'line-color': ['get', 'color'],
      'line-width': 3,
      'line-opacity': 0.8
    }
  };

  const projectLayer = {
    id: 'projects',
    type: 'line',
    paint: {
      'line-color': '#ff6b6b',
      'line-width': 4,
      'line-dasharray': [2, 2]
    }
  };

  const pipelineGeoJSON = {
    type: 'FeatureCollection',
    features: pipelines
      .filter(p => visibleLayers.includes(p.properties.utility_type_name?.toLowerCase()))
      .map(p => ({
        ...p,
        properties: {
          ...p.properties,
          color: getUtilityColor(p.properties.utility_type_name)
        }
      }))
  };

  const projectGeoJSON = {
    type: 'FeatureCollection',
    features: projects
  };

  function getUtilityColor(type) {
    const colors = {
      water: '#2196f3',
      drainage: '#4caf50',
      sewage: '#9c27b0',
      gas: '#ff9800',
      electricity: '#f44336',
      telecom: '#00bcd4'
    };
    return colors[type?.toLowerCase()] || '#757575';
  }

  return (

      <Map
        ref={mapRef}
        {...viewState}
        onMove={evt => setViewState(evt.viewState)}
        mapboxAccessToken={MAPBOX_TOKEN}
        style={{ width: '100%', height: '100%' }}
        mapStyle="mapbox://styles/mapbox/streets-v12"
        onClick={onMapClick}
      >













          Water
          Drainage
          Sewage
          Gas
          Electricity
          Telecom



  );
}

export default MapView;