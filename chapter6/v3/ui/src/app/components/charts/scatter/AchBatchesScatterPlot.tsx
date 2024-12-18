import * as React from 'react';
import {CartesianGrid, Cell, Legend, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis} from 'recharts';
import Title from "@/app/components/Title";
import {AchBatchInfo} from "@/app/fileDetails/[fileId]/page";
import {CurrencyTick} from "@/app/components/charts/CurrencyTick";
import {AchBatchesScatterTooltip} from "@/app/components/charts/scatter/AchBatchesScatterTooltip";
import {stringToColor} from "@/app/utils/ColorUtils";
import {determineScaleAndLabel} from "@/app/utils/ChartUtils";

interface AchBatchesScatterPlotProps {
    batches: AchBatchInfo[];
}

export default function AchBatchesScatterPlot({batches}: Readonly<AchBatchesScatterPlotProps>) {

    const plotData = batches.map(batch => {
        const updatedCompanyBatches = batch.companyBatches.map((companyBatch) => {
            return {
                ...companyBatch,
                totalCreditAndDebits: companyBatch.totalCreditAmount + companyBatch.totalDebitAmount
            };
        });
        return {
            ...batch,
            companyBatches: updatedCompanyBatches
        };
    });

    const maxValue = Math.max(...plotData.map(item =>
        Math.max(...item.companyBatches.map((companyBatch: any) => companyBatch.totalCreditAndDebits))
    ));
    //const { divisor, label } = determineScaleAndLabel(maxValue);

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
         }}>
      <Legend />
      <CartesianGrid />
      <XAxis type="number" dataKey="recordCount" name="Count" unit="" />
      <YAxis type="number"
             tick={<CurrencyTick/>}
             dataKey="totalCreditAndDebits" name="Total Amount" unit="" />
      <Tooltip cursor={{ strokeDasharray: '3 3' }}
         content={<AchBatchesScatterTooltip />} />
         {plotData.map((entry, index) => (
            <Scatter key={`${entry.companyName}`}
                     name={`${entry.companyName}`}
                     data={entry.companyBatches}
                     fill={stringToColor(entry.companyName)}>
               <Cell
                  key={`cell-${entry.companyName}-${index}`}
                            fill={stringToColor(entry.companyName)} />
                      </Scatter>
                   ))}
      </ScatterChart>
   </ResponsiveContainer>
</>);
}