import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Typography } from '@mui/material';

const TransactionHistory: React.FC = () => {
  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'date', headerName: 'Date', width: 150 },
    { field: 'type', headerName: 'Type', width: 150 },
    { field: 'amount', headerName: 'Amount', width: 150 },
    { field: 'status', headerName: 'Status', width: 150 },
  ];

  const rows = [
    { id: 1, date: '2023-01-01', type: 'Deposit', amount: 5000, status: 'Approved' },
    { id: 2, date: '2023-01-15', type: 'Withdrawal', amount: 2000, status: 'Pending' },
    { id: 3, date: '2023-02-01', type: 'Deposit', amount: 3000, status: 'Rejected' },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Transaction History
      </Typography>
      <div style={{ height: 400, width: '100%' }}>
        <DataGrid rows={rows} columns={columns} pageSize={5} rowsPerPageOptions={[5]} />
      </div>
    </Box>
  );
};

export default TransactionHistory;
