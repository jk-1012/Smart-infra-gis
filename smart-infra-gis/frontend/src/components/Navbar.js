import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function Navbar({ user, onLogout }) {
  const navigate = useNavigate();

  return (



          Smart Infra GIS



            {user.username} ({user.role})


            Logout




  );
}

export default Navbar;