import * as React from "react";
import {formatCurrency} from "@/app/utils/CurrencyUtils";

interface CurrencyTickProps {
    x: number;
    y: number;
    payload: {
        value: string;
    };
}

export function CurrencyTick({ x, y, payload }: Readonly<Partial<CurrencyTickProps>>): React.JSX.Element {
    const value = payload?.value ?? '0.0';
    return (
        <g transform={`translate(${x},${y})`}>
            <text x={0} y={0} dy={16} textAnchor="end" fill="#666" transform="rotate(-35)">
                {formatCurrency(Number.parseFloat(value))}
            </text>
        </g>
    );
}