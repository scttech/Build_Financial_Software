import * as React from 'react';
import {CartesianGrid, Cell, Legend, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis} from 'recharts';
import Title from "@/app/components/Title";
import {AchBatchInfo, AchCompanyBatchInfo} from "@/app/fileDetails/[fileId]/page";
import {CurrencyTick} from "@/app/components/charts/CurrencyTick";
import {AchBatchesScatterTooltip} from "@/app/components/charts/scatter/AchBatchesScatterTooltip";
import {stringToColor} from "@/app/utils/ColorUtils";
import {determineScaleAndLabel} from "@/app/utils/ChartUtils";

interface AchBatchesScatterPlotProps {
    batches: AchCompanyBatchInfo[];
}

export default function AchBatchesScatterPlot({batches}: Readonly<AchBatchesScatterPlotProps>) {

    const plotData = batches.map(batch => {
        const updatedCompanyBatches = batch.companyBatches.map((companyBatch: AchBatchInfo) => {
            return {
                ...companyBatch,
                totalCreditAndDebits: companyBatch.creditTotal.add(companyBatch.debitTotal)
            };
        });
        return {
            ...batch,
            companyBatches: updatedCompanyBatches
        };
    });

    const maxValue = Math.max(...plotData.map(item =>
        Math.max(...item.companyBatches.map((companyBatch: any) => companyBatch.totalCreditAndDebits.toNumber()))
    ));
    const { divisor, label } = determineScaleAndLabel(maxValue);

    console.log(plotData);

    return (
        <>
            <Title>ACH Batches</Title>
            <ResponsiveContainer>
                <ScatterChart
                    width={400}
                    height={400}
                    margin={{
                        top: 20,
                        right: 20,
                        bottom: 20,
                        left: 20,
                    }}
                >
                    <Legend />
                    <CartesianGrid />
                    <XAxis type="number" dataKey="recordCount" name="Count" unit="" />
                    <YAxis type="number"
                           tick={<CurrencyTick divisor={divisor} angle={0}/>}
                           label={{ value: `$ (in ${label})`, position: 'insideLeft', angle: -90, style: { textAnchor: 'middle' } }}
                           dataKey="totalCreditAndDebits" name="Total Amount" unit="" />
                    <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<AchBatchesScatterTooltip />} />
                        {plotData.map((entry, index) => (
                            <Scatter key={`${entry.companyId}`} name={`${entry.companyId}`} data={entry.companyBatches} fill={stringToColor(entry.companyId)}>
                                <Cell key={`cell-${entry.companyId}-${index}`} fill={stringToColor(entry.companyId)} />
                            </Scatter>
                        ))}
                </ScatterChart>
            </ResponsiveContainer>
        </>
    );
}