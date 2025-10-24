import React from 'react';
import {
  Paper, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Chip, Button, Typography, Box
} from '@mui/material';
import WarningIcon from '@mui/icons-material/Warning';

function ConflictReport({ conflicts, onResolve }) {
  const getSeverityColor = (severity) => {
    const colors = {
      critical: 'error',
      high: 'warning',
      medium: 'info',
      low: 'success'
    };
    return colors[severity] || 'default';
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <WarningIcon color="error" sx={{ mr: 1 }} />
        <Typography variant="h6">
          Conflict Report ({conflicts.length} conflicts)
        </Typography>
      </Box>

      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Project</TableCell>
              <TableCell>Pipeline</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Severity</TableCell>
              <TableCell>Distance (m)</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {conflicts.map((conflict) => (
              <TableRow key={conflict.id}>
                <TableCell>{conflict.project_name}</TableCell>
                <TableCell>{conflict.pipeline_name}</TableCell>
                <TableCell>{conflict.conflict_type}</TableCell>
                <TableCell>
                  <Chip
                    label={conflict.severity}
                    color={getSeverityColor(conflict.severity)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {conflict.distance ? conflict.distance.toFixed(2) : 'N/A'}
                </TableCell>
                <TableCell>
                  {conflict.resolved ? (
                    <Chip label="Resolved" color="success" size="small" />
                  ) : (
                    <Chip label="Pending" color="warning" size="small" />
                  )}
                </TableCell>
                <TableCell>
                  {!conflict.resolved && (
                    <Button
                      size="small"
                      onClick={() => onResolve(conflict.id)}
                    >
                      Resolve
                    </Button>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}

export default ConflictReport;