import React, { useState, useEffect } from 'react';
import { Container, Box, Typography, Paper, Grid, Chip } from '@mui/material';
import MapView from '../components/MapView';
import axiosInstance from '../api/axiosConfig';

function CitizenPage({ user }) {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await axiosInstance.get(`/projects/?city=${user.city}&status=in_progress`);
      setProjects(response.data.features || response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  return (


        Ongoing Projects in {user.city}












              Project List

            {projects.map((project) => (


                  {project.name}


                  {project.description}





                {project.start_date && (

                    Start: {new Date(project.start_date).toLocaleDateString()}

                )}

            ))}




  );
}

export default CitizenPage;