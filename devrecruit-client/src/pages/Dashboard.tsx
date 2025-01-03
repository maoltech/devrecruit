import * as React from 'react';
import { Box, Typography, Grid, Card, CardContent } from '@mui/material';
import { Line, Pie, Bar } from 'react-chartjs-2';

const Dashboard: React.FC = () => {
  const lineData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    datasets: [
      {
        label: 'Investment Growth',
        data: [1000, 2000, 3000, 4000, 5000],
        borderColor: 'rgba(75,192,192,1)',
        fill: false,
      },
    ],
  };

  const pieData = {
    labels: ['Stocks', 'Bonds', 'Real Estate'],
    datasets: [
      {
        data: [50, 30, 20],
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
      },
    ],
  };

  const barData = {
    labels: ['Deposits', 'Withdrawals'],
    datasets: [
      {
        label: 'Transactions',
        data: [10000, 4000],
        backgroundColor: ['#36A2EB', '#FF6384'],
      },
    ],
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Investment Dashboard
      </Typography>
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Investment Growth</Typography>
              <Line data={lineData} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6">Portfolio Allocation</Typography>
              <Pie data={pieData} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6">Transaction Summary</Typography>
              <Bar data={barData} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;