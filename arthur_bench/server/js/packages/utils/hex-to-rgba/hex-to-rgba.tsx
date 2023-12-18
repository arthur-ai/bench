const hexToRgba = (hex: string, alpha: number | undefined = 1): string => {
    hex = hex.toUpperCase();

    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);

    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
};

export default hexToRgba;
