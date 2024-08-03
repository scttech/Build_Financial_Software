
export function getMaxForYAxis(dataMax: number): number {
    if (dataMax === 0) return 0;

    const magnitude = Math.floor(Math.log10(dataMax));
    const divisor = Math.pow(10, magnitude);
    return Math.ceil(dataMax / divisor) * divisor;
}
export function determineScaleAndLabel (dataMax: number): { divisor: number, label: string } {
    if (dataMax > 1e12) {
        return { divisor: 1e12, label: "Trillions" };
    } else if (dataMax > 1e9) {
        return { divisor: 1e9, label: "Billions" };
    } else if (dataMax >= 1e6) {
        return { divisor: 1e6, label: "Millions" };
    } else if (dataMax >= 1e3) {
        return { divisor: 1e3, label: "Thousands" };
    } else if (dataMax >= 100){
        return { divisor: 10, label: "Hundreds" };
    } else if ( dataMax >= 10){
        return { divisor: 1, label: "Tens" };
    } else {
        return { divisor: 1, label: "Ones" };
    }
}