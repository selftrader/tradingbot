import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './Layout';
import Dashboard from './pages/Dashboard';
import LiveUpdates from './pages/LiveUpdates';
import ConfigPage from './pages/ConfigPage';
import StockAnalysisPage from './pages/StockAnalysisPage';

function App() {
    const [user, setUser] = useState(null);

    // Load user info if already logged in (dummy implementation)
    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
    }, []);

    return (
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<Dashboard user={user} />} />
                    <Route path="/live-updates" element={<LiveUpdates user={user} />} />
                    <Route path="/config" element={<ConfigPage user={user} />} />
                    <Route path="/analysis" element={<StockAnalysisPage user={user} />} />
                </Routes>
            </Layout>
        </Router>
    );
}

export default App;
