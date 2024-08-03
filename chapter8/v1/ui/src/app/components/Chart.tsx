import * as React from 'react';
import {useTheme} from '@mui/material/styles';
import {Label, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from 'recharts';
import Title from './Title';

// Generate Sales Data
function createData(time: string, creditAmount?: number, debitAmount?: number) {
    return { time, creditAmount, debitAmount };
}

const transactionData = [
    createData('00:00', 0, 500),
    createData('03:00', 300, 750),
    createData('06:00', 600, 1000),
    createData('09:00', 800, 1250),
    createData('12:00', 1500, 2000),
    createData('15:00', 2000, 2100),
    createData('18:00', 2400, 2200),
    createData('21:00', 2400, 2400),
    createData('24:00', undefined, undefined),
];



export default function Chart() {
    const theme = useTheme();

    return (
        <React.Fragment>
            <Title>Today</Title>
            <ResponsiveContainer>
                <LineChart
                    data={transactionData}
                    margin={{
                        top: 16,
                        right: 16,
                        bottom: 0,
                        left: 24,
                    }}
                >
                    <XAxis
                        dataKey="time"
                        stroke={theme.palette.text.secondary}
                        style={theme.typography.body2}
                    />
                    <YAxis
                        stroke={theme.palette.text.secondary}
                        style={theme.typography.body2}
                    >
                        <Label
                            angle={270}
                            position="left"
                            style={{
                                textAnchor: 'middle',
                                fill: theme.palette.text.primary,
                                ...theme.typography.body1,
                            }}
                        >
                            Transactions ($)
                        </Label>
                    </YAxis>
                    <Tooltip />
                    <Legend />
                    <Line
                        name='Credit Total'
                        isAnimationActive={false}
                        type="monotone"
                        dataKey="creditAmount"
                        stroke={theme.palette.primary.main}
                        activeDot={{ r: 8 }}
                    />
                    <Line
                        name='Debit Total'
                        isAnimationActive={false}
                        type="monotone"
                        dataKey="debitAmount"
                        stroke={theme.palette.secondary.main}
                        activeDot={{ r: 8 }}
                    />
                </LineChart>
            </ResponsiveContainer>
        </React.Fragment>
    );
}