import * as React from 'react';
import {Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from 'recharts';
import Title from "@/app/components/Title";
import {CurrencyTick} from "@/app/components/charts/CurrencyTick";
import {AchFiles} from "@/app/interfaces/AchFiles";
import {AchFilesBarChartToolTip} from "@/app/components/charts/bar/AchFilesBarChartTooltip";
import {determineScaleAndLabel, getMaxForYAxis} from "@/app/utils/ChartUtils";

interface AchFilesBarChartProps {
    files: AchFiles[];
}

export default function AchFilesBarChart({files}: Readonly<AchFilesBarChartProps>) {

    const plotData = files.map(file => {
        return {
            ...file,
            "Credit Total": file.creditTotal.toNumber(),
            "Debit Total": file.debitTotal.toNumber()
        };
    });

    const getLabel = (key: string) => {
        const item = plotData.find((item) => item.id === key);
        return item ? item.filename : '';
    }

    const maxValue = Math.max(...plotData.map(item => item["Credit Total"] + item["Debit Total"]));
    const { divisor, label } = determineScaleAndLabel(maxValue);


    console.log(plotData);

    return (
        <>
            <Title>Top 10 Files Today</Title>
            <ResponsiveContainer>
                <BarChart
                    width={500}
                    height={300}
                    data={plotData}
                    margin={{
                        top: 30,
                        right: 20,
                        bottom: 20,
                        left: 20,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="id" tickFormatter={getLabel} />
                    <YAxis tick={<CurrencyTick divisor={divisor} angle={0}/>}
                        domain={[0, (dataMax: number) => getMaxForYAxis(dataMax)]}
                           label={{ value: `$ (in ${label})`, position: 'insideLeft', angle: -90, style: { textAnchor: 'middle' } }}
                    />
                    <Tooltip content={<AchFilesBarChartToolTip />} />
                    <Legend />
                    <Bar dataKey="Credit Total" stackId="a" fill="#8884d8" />
                    <Bar dataKey="Debit Total" stackId="a" fill="#82ca9d" />
                </BarChart>
            </ResponsiveContainer>
        </>
    );
}