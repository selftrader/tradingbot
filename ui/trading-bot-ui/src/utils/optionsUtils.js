export const calculateStrikePrice = (spotPrice, strikeType = 'ATM') => {
    const roundedPrice = Math.round(spotPrice / 50) * 50;
    
    switch (strikeType) {
        case 'ITM':
            return roundedPrice - 50;
        case 'OTM':
            return roundedPrice + 50;
        default:
            return roundedPrice; // ATM
    }
};

export const getExpiryDates = (weekly = true) => {
    const dates = [];
    let current = new Date();
    
    // Add weekly expiries (Thursday)
    if (weekly) {
        while (dates.length < 4) {
            if (current.getDay() === 4) { // Thursday
                dates.push(current.toISOString().split('T')[0]);
            }
            current.setDate(current.getDate() + 1);
        }
    }
    
    // Add monthly expiry
    const lastThursday = new Date(current.getFullYear(), current.getMonth() + 1, 0);
    while (lastThursday.getDay() !== 4) {
        lastThursday.setDate(lastThursday.getDate() - 1);
    }
    dates.push(lastThursday.toISOString().split('T')[0]);
    
    return dates;
};