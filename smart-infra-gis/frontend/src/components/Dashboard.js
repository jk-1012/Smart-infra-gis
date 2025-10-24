import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell } from 'recharts';

function Dashboard({ stats }) {
  const conflictData = [
    { name: 'Resolved', value: stats.resolvedConflicts || 0 },
    { name: 'Pending', value: stats.pendingConflicts || 0 },
  ];

  const severityData = [
    { name: 'Critical', count: stats.criticalConflicts || 0 },
    { name: 'High', count: stats.highConflicts || 0 },
    { name: 'Medium', count: stats.mediumConflicts || 0 },
    { name: 'Low', count: stats.lowConflicts || 0 },
  ];

  const COLORS = ['#4caf50', '#ff9800', '#f44336', '#2196f3'];

  return (





              {stats.totalProjects || 0}

            Total Projects






              {stats.totalConflicts || 0}

            Conflicts Detected






              ₹{(stats.costSavings || 0).toLocaleString()}

            Cost Savings (Lakhs)






              {stats.pipelinesCount || 0}

            Pipelines Mapped





            Conflict Status


                {conflictData.map((entry, index) => (

                ))}








            Conflicts by Severity











  );
}

export default Dashboard;