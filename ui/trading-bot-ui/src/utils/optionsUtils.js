const getOptions = () => {
    return [
      { label: "NIFTY 50", value: "nifty_50" },
      { label: "BANKNIFTY", value: "bank_nifty" },
      { label: "Reliance", value: "reliance" },
    ];
  };
  
  export default getOptions;  // ✅ Fixed missing export
  