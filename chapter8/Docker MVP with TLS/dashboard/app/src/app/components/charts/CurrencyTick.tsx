import * as React from "react";

interface CurrencyTickProps {
    x: number;
    y: number;
    payload: {
        value: string;
    };
    angle: number;
    divisor: number;
}

export function CurrencyTick({ x, y, payload, angle, divisor }: Readonly<Partial<CurrencyTickProps>>): React.JSX.Element {
    const value = payload?.value ?? '0.0';
    const scaledValue = Number.parseFloat( value ) / (divisor ?? 1);
    const formattedValue = `${scaledValue.toFixed(0)}`;
    const rotation: string = `rotate(${angle ?? 0})`;
    return (
        <g transform={`translate(${x},${y})`}>
            <text x={0} y={0} dy={4} textAnchor="end" fill="#666" transform={rotation}>
                {formattedValue}
            </text>
        </g>
    );
}