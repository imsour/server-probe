import React, {useEffect, useState} from 'react';
import '../styles/App.css';
import Chart from "./Chart";
import Switch from '@mui/material/Switch';
import axios from "axios";
import {api} from "../consts";

function App() {
    const FETCH_INTERVAL = 1000
    const [series, setSeries] = useState([{data: []}])
    const [probeStatus, setProbeStatus] = useState(false)
    const [connectionError, setConnectionError] = useState(false)

    function fetchProbeStatus() {
        fetch(api.PROBE_STATUS)
            .then((r) => r.json())
            .then((probe: { running: boolean }) => {
                setProbeStatus(probe.running);
                setConnectionError(false);
            })
            .catch(() => {
                setConnectionError(true);
            });
    }

    function fetchSeries() {
        fetch(api.PROBE_DATA)
            .then((r) => r.json())
            .then((data: any) => {
                setSeries(data);
                setConnectionError(false);
            })
            .catch(() => {
                setConnectionError(true);
                setProbeStatus(false);
            });
    }

    function postProbeStatus() {
        axios.post(probeStatus ? api.PROBE_STOP : api.PROBE_START)
            .then((r) => {
                if (r.status === 200) {
                    setProbeStatus(!probeStatus);
                    setConnectionError(false);
                }
            })
            .catch(function (error) {
                setConnectionError(true);
            });
    }

    useEffect(() => {
        fetchProbeStatus();
        fetchSeries();
    },[])

    useEffect(()=>{
        //Clear fetch interval when component is unmounted.
        const interval = setInterval(() => {
            if (probeStatus)
                fetchSeries();
        }, FETCH_INTERVAL);
        return () => clearInterval(interval);
    },[probeStatus])

    return (
        <div className="App">
            <p className="Header">
                Server Endpoint Probe - Timing the internet since '98
            </p>
            <div className="Subtext">
                <Switch
                    checked={probeStatus}
                    onChange={postProbeStatus}/>
                {connectionError ? 'Connection To Probe Service Failed, Please Try Again.'
                    : probeStatus ? `Probing every ${FETCH_INTERVAL}ms` : "Probing Is OFF"}
            </div>
            <div className="Chart">
                <Chart
                    series={series}
                    range={20000}
                />
            </div>
        </div>
    );
}

export default App;
