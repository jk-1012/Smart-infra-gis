import React, { useState } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, Button, MenuItem, Grid
} from '@mui/material';

function ProjectForm({ open, onClose, onSubmit, cities }) {
  const [formData, setFormData] = useState({
    name: '',
    project_type: 'road',
    description: '',
    department: '',
    city: '',
    start_date: '',
    end_date: '',
    estimated_cost: ''
  });

  const projectTypes = [
    { value: 'road', label: 'Road Construction' },
    { value: 'metro', label: 'Metro Line' },
    { value: 'pipeline', label: 'Pipeline Installation' },
    { value: 'drainage', label: 'Drainage System' },
    { value: 'building', label: 'Building Construction' },
    { value: 'other', label: 'Other' }
  ];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    onSubmit(formData);
    setFormData({
      name: '', project_type: 'road', description: '', department: '',
      city: '', start_date: '', end_date: '', estimated_cost: ''
    });
  };

  return (

      Create New Project








              {projectTypes.map((option) => (

                  {option.label}

              ))}





























        Cancel

          Create Project



  );
}

export default ProjectForm;