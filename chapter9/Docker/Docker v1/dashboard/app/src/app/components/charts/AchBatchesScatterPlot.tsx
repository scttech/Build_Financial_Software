import * as React from 'react';
import {ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ResponsiveContainer, Legend} from 'recharts';
import Title from "@/app/components/Title";
import {AchBatchInfo, AchCompanyBatchInfo} from "@/app/fileDetails/[id]/page";
import {CurrencyTick} from "@/app/components/charts/CurrencyTick";
import {AchBatchesScatterTooltip} from "@/app/components/charts/AchBatchesScatterTooltip";
import {stringToColor} from "@/app/utils/ColorUtils";

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
                           tick={<CurrencyTick/>}
                           dataKey="totalCreditAndDebits" name="Total Amount" unit="" />
                    <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<AchBatchesScatterTooltip />} />
                        {plotData.map((entry, index) => (
                            <Scatter key={`${entry.companyName}`} name={`${entry.companyName}`} data={entry.companyBatches} fill={stringToColor(entry.companyName)}>
                                <Cell key={`cell-${entry.companyName}-${index}`} fill={stringToColor(entry.companyName)} />
                            </Scatter>
                        ))}
                </ScatterChart>
            </ResponsiveContainer>
        </>
    );
}