import React, { useState, useEffect } from 'react';
import { Container, Box, Tabs, Tab, Button, Fab } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import MapView from '../components/MapView';
import ProjectForm from '../components/ProjectForm';
import ConflictReport from '../components/ConflictReport';
import axiosInstance from '../api/axiosConfig';

function EngineerPage({ user }) {
  const [activeTab, setActiveTab] = useState(0);
  const [pipelines, setPipelines] = useState([]);
  const [projects, setProjects] = useState([]);
  const [conflicts, setConflicts] = useState([]);
  const [projectFormOpen, setProjectFormOpen] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [pipelineRes, projectRes, conflictRes] = await Promise.all([
        axiosInstance.get(`/gisdata/pipelines/?city=${user.city}`),
        axiosInstance.get(`/projects/?city=${user.city}`),
        axiosInstance.get('/projects/conflicts/')
      ]);

      setPipelines(pipelineRes.data.features || pipelineRes.data);
      setProjects(projectRes.data.features || projectRes.data);
      setConflicts(conflictRes.data.results || conflictRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleCreateProject = async (projectData) => {
    try {
      await axiosInstance.post('/projects/', projectData);
      setProjectFormOpen(false);
      fetchData();
    } catch (error) {
      console.error('Error creating project:', error);
    }
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 3 }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
          <Tab label="Map View" />
          <Tab label="My Projects" />
          <Tab label="Conflicts" />
        </Tabs>
      </Box>

      {activeTab === 0 && (
        <Box sx={{ height: '70vh' }}>
          <MapView pipelines={pipelines} projects={projects} />
        </Box>
      )}

      {activeTab === 1 && (
        <Box>
          <ConflictReport
            conflicts={conflicts.filter(c =>
              projects.some(p => p.id === c.project)
            )}
            onResolve={() => {}}
          />
        </Box>
      )}

      {activeTab === 2 && (
        <ConflictReport conflicts={conflicts} onResolve={() => {}} />
      )}

      <Fab
        color="primary"
        aria-label="add"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={() => setProjectFormOpen(true)}
      >
        <AddIcon />
      </Fab>

      <ProjectForm
        open={projectFormOpen}
        onClose={() => setProjectFormOpen(false)}
        onSubmit={handleCreateProject}
        cities={[user.city]}
      />
    </Container>
  );
}

export default EngineerPage;