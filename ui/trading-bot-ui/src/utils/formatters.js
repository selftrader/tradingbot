/**
 * Format a number with specified decimal places and optional Indian formatting
 * @param {number} value - Number to format
 * @param {number} decimals - Number of decimal places
 * @param {boolean} useIndianFormat - Whether to use Indian number formatting
 * @returns {string} Formatted number
 */
export const formatNumber = (value, decimals = 2, useIndianFormat = true) => {
    if (value === null || value === undefined || isNaN(value)) {
        return '-';
    }

    // Round to specified decimal places
    const roundedValue = Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
    
    if (useIndianFormat) {
        // Convert to Indian format (e.g., 1,00,000.00)
        const parts = roundedValue.toString().split('.');
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        return parts.join('.');
    } else {
        // Use standard international format
        return roundedValue.toLocaleString(undefined, {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }
};

/**
 * Format a percentage value
 * @param {number} value - Value to format as percentage
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted percentage
 */
export const formatPercentage = (value, decimals = 2) => {
    if (value === null || value === undefined || isNaN(value)) {
        return '-';
    }
    return `${formatNumber(value, decimals)}%`;
};

/**
 * Format currency value in INR
 * @param {number} value - Value to format as currency
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted currency
 */
export const formatCurrency = (value, decimals = 2) => {
    if (value === null || value === undefined || isNaN(value)) {
        return '-';
    }
    return `₹${formatNumber(value, decimals)}`;
};
