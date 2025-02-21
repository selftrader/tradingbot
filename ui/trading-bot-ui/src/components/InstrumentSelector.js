import React, { useState } from "react";
import { Button, Select, MenuItem } from "@mui/material";

const InstrumentSelector = ({ onSelectInstrument }) => {
    const [instrument, setInstrument] = useState("index");

    return (
        <div>
            <Select value={instrument} onChange={(e) => setInstrument(e.target.value)}>
                <MenuItem value="index">Index (NIFTY/BANKNIFTY)</MenuItem>
                <MenuItem value="options">Options (F&O)</MenuItem>
                <MenuItem value="stocks">Stocks</MenuItem>
                <MenuItem value="sectoral">Sectoral Indices</MenuItem>
            </Select>
            <Button onClick={() => onSelectInstrument(instrument)}>Start Trading</Button>
        </div>
    );
};

export default InstrumentSelector;
