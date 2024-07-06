import React from 'react';
import {Paper, Typography} from '@mui/material';
import Grid from '@mui/material/Unstable_Grid2';


const ResponsiveCards = () => {
    return (
        <Grid container spacing={2} sx={{pl: 1, pr: 1}}>
            {[1,2,3,4,5,6,7,8,9].map((value) => (
                <Grid xs={12} sm={6} md={4} lg={2} xl={1} key={value} >
                    <Paper elevation={3} sx={{ padding: 2 }}>
                        <Typography variant="h5" component="h3">
                            Card {value}
                        </Typography>
                        <Typography component="p">
                            This is some content inside card number {value}.
                        </Typography>
                    </Paper>
                </Grid>
            ))}
        </Grid>
    );
};

export default ResponsiveCards;