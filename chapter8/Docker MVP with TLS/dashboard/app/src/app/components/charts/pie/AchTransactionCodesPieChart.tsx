import * as React from 'react';
import {
    ScatterChart,
    Scatter,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Cell,
    ResponsiveContainer,
    Legend,
    BarChart, Bar, Sector, PieChart, Pie
} from 'recharts';
import Title from "@/app/components/Title";
import {AchBatchInfo, AchCompanyBatchInfo} from "@/app/fileDetails/[fileId]/page";
import {CurrencyTick} from "@/app/components/charts/CurrencyTick";
import {AchBatchesScatterTooltip} from "@/app/components/charts/scatter/AchBatchesScatterTooltip";
import {stringToColor} from "@/app/utils/ColorUtils";
import {AchFiles} from "@/app/interfaces/AchFiles";
import {AchFilesBarChartToolTip} from "@/app/components/charts/bar/AchFilesBarChartTooltip";
import {AchBatchEntriesResponse} from "@/app/fileDetails/[fileId]/batchDetails/[batchId]/page";
import {useState} from "react";

interface AchTransactionCodesPieChartProps {
    entries: AchBatchEntriesResponse[];
}

export default function AchTransactionCodesPieChart({entries}: Readonly<AchTransactionCodesPieChartProps>) {

    const [activeIndex, setActiveIndex] = useState(0);

    const COLORS:string[] = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#FF8042', '#FF8042', '#FF8042', '#FF8042', '#FF8042', '#FF8042'];

    const tranCodes: Record<number, number> = {};
    entries.forEach((entry: AchBatchEntriesResponse) => {
        tranCodes[entry.transaction_code] = (tranCodes[entry.transaction_code] || 0) + 1;
    });

    const plotData: { key: number; value: number }[] = Object.entries(tranCodes).map(([key, value]) => ({
        key: Number(key),
        value: value,
    }));

    console.log(plotData);

    const renderActiveShape = (props: any) => {
        const RADIAN = Math.PI / 180;
        const { cx, cy, midAngle, innerRadius, outerRadius, startAngle, endAngle, fill, payload, percent, value } = props;
        const sin = Math.sin(-RADIAN * midAngle);
        const cos = Math.cos(-RADIAN * midAngle);
        const sx = cx + (outerRadius + 10) * cos;
        const sy = cy + (outerRadius + 10) * sin;
        const mx = cx + (outerRadius + 30) * cos;
        const my = cy + (outerRadius + 30) * sin;
        const ex = mx + (cos >= 0 ? 1 : -1) * 22;
        const ey = my;
        const textAnchor = cos >= 0 ? 'start' : 'end';

        return (
            <g>
                <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>
                    {payload.name}
                </text>
                <Sector
                    cx={cx}
                    cy={cy}
                    innerRadius={innerRadius}
                    outerRadius={outerRadius}
                    startAngle={startAngle}
                    endAngle={endAngle}
                    fill={fill}
                />
                <Sector
                    cx={cx}
                    cy={cy}
                    startAngle={startAngle}
                    endAngle={endAngle}
                    innerRadius={outerRadius + 6}
                    outerRadius={outerRadius + 10}
                    fill={fill}
                />
                <path d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`} stroke={fill} fill="none" />
                <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
                <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} textAnchor={textAnchor} fill="#333">{`Tran Code ${payload.key}`}</text>
                <text x={ex + (cos >= 0 ? 1 : -1) * 12} y={ey} dy={18} textAnchor={textAnchor} fill="#999">
                    {`(Rate ${(percent * 100).toFixed(2)}%)`}
                </text>
            </g>
        );
    };

    const onPieEnter = (_: any, index: number) => {
        setActiveIndex(index);
    };

    return (
        <>
            <Title>Transaction Codes</Title>
            <ResponsiveContainer>
                <PieChart width={400} height={400}>
                    <Pie
                        activeIndex={activeIndex}
                        activeShape={renderActiveShape}
                        data={plotData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        dataKey="value"
                        onMouseEnter={onPieEnter}
                    >
                    {plotData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length] } />
                    ))}
                        </Pie>
                </PieChart>
            </ResponsiveContainer>
        </>
    );
}