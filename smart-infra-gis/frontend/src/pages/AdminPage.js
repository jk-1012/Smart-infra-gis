import React, { useState, useEffect } from 'react';
import { Container, Box, Tabs, Tab, Button } from '@mui/material';
import Dashboard from '../components/Dashboard';
import MapView from '../components/MapView';
import ConflictReport from '../components/ConflictReport';
import axiosInstance from '../api/axiosConfig';

function AdminPage({ user }) {
  const [activeTab, setActiveTab] = useState(0);
  const [pipelines, setPipelines] = useState([]);
  const [projects, setProjects] = useState([]);
  const [conflicts, setConflicts] = useState([]);
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [pipelineRes, projectRes, conflictRes] = await Promise.all([
        axiosInstance.get('/gisdata/pipelines/'),
        axiosInstance.get('/projects/'),
        axiosInstance.get('/projects/conflicts/')
      ]);

      setPipelines(pipelineRes.data.features || pipelineRes.data);
      setProjects(projectRes.data.features || projectRes.data);
      setConflicts(conflictRes.data.results || conflictRes.data);

      // Calculate stats
      const pendingConflicts = conflictRes.data.filter(c => !c.resolved).length;
      setStats({
        totalProjects: projectRes.data.length,
        totalConflicts: conflictRes.data.length,
        pendingConflicts,
        resolvedConflicts: conflictRes.data.length - pendingConflicts,
        pipelinesCount: pipelineRes.data.length,
        costSavings: conflictRes.data.length * 50, // ₹50L per conflict avoided
        criticalConflicts: conflictRes.data.filter(c => c.severity === 'critical').length,
        highConflicts: conflictRes.data.filter(c => c.severity === 'high').length,
        mediumConflicts: conflictRes.data.filter(c => c.severity === 'medium').length,
        lowConflicts: conflictRes.data.filter(c => c.severity === 'low').length,
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleResolveConflict = async (conflictId) => {
    try {
      await axiosInstance.post(`/projects/conflicts/${conflictId}/resolve/`, {
        notes: 'Resolved by admin'
      });
      fetchData();
    } catch (error) {
      console.error('Error resolving conflict:', error);
    }
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 3 }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
          <Tab label="Dashboard" />
          <Tab label="Map View" />
          <Tab label="Conflicts" />
        </Tabs>
      </Box>

      {activeTab === 0 && <Dashboard stats={stats} />}

      {activeTab === 1 && (
        <Box sx={{ height: '70vh' }}>
          <MapView pipelines={pipelines} projects={projects} />
        </Box>
      )}

      {activeTab === 2 && (
        <ConflictReport
          conflicts={conflicts}
          onResolve={handleResolveConflict}
        />
      )}
    </Container>
  );
}

export default AdminPage;