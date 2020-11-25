import React, {useEffect, useState} from 'react';
import {Button, Form, FormControl, FormLabel, Jumbotron, Nav, Navbar, Spinner} from 'react-bootstrap';

const service_url = "http://services-based-kafka.westus.cloudapp.azure.com"

let initialSeconds = 10
let initialized = false
let timeOutList = []


function App() {
    let [active, setActive] = useState("home")
    let [interval, setInterval] = useState(initialSeconds)
    let [intervalUnit, setIntervalUnit] = useState("s")
    let [lastUpdated, setLastUpdated] = useState(new Date().toLocaleString())
    let [loading, setLoading] = useState(true)
    let [stats, setStats] = useState({})
    let [foodAndWaterReq, setFoodAndWaterReq] = useState({})
    let [cageReq, setCageReq] = useState({})

    async function updateDashboard() {
        setLoading(true)
        await Promise.all([
            fetch(service_url + "/processing/stats").then(response => {
                if (!response.ok || response.status !== 200)
                    return Promise.reject("Error in request /stats")
                return response.json()
            }).then(json => {
                setStats(json)
            }).catch(e => {
                console.error(e)
                setStats({})
            }),
            fetch(service_url + "/audit_log/foodAndWater?index=1").then(response => {
                if (!response.ok || response.status !== 200)
                    return Promise.reject("Error in request /foodAndWater")
                return response.json()
            }).then(json => {
                setFoodAndWaterReq(json)
            }).catch(e => {
                console.error(e)
                setFoodAndWaterReq({})
            }),
            fetch(service_url + "/audit_log/cageReadings?index=1").then(response => {
                if (!response.ok || response.status !== 200)
                    return Promise.reject("Error in request /cageReadings")
                return response.json()
            }).then(json => {
                setCageReq(json)
            }).catch(e => {
                console.error(e)
                setCageReq({})
            }),
        ])
        setLastUpdated(new Date().toLocaleString())
        setLoading(false)
    }

    let totalIntervalInMS = 1000 * interval
    switch (intervalUnit) {
        case "m":
            totalIntervalInMS *= 60
            break;
        case "h":
            totalIntervalInMS *= 60 * 60
            break;
        default:
            break;
    }

    useEffect(() => {
        for (let timeout of timeOutList)
            clearTimeout(timeout)
        if (!initialized) {
            timeOutList.push(setTimeout(updateDashboard, initialSeconds * 1000))
            initialized = true
        } else
            timeOutList.push(setTimeout(updateDashboard, totalIntervalInMS))
    }, [interval, intervalUnit, lastUpdated])


    let nextUpdate = new Date(lastUpdated)
    nextUpdate.setSeconds(nextUpdate.getSeconds() + totalIntervalInMS / 1000)
    return (
        <>
            <Navbar bg="dark" variant="dark">
                <Navbar.Brand className={"lead"} href="/">Aviary Monitor API</Navbar.Brand>
                <Nav className="mr-auto">
                    <Nav.Link href="/" active={active === "home"}>Dashboard</Nav.Link>
                </Nav>
                <Form inline>
                    <FormLabel className={"text-white mr-1 lead"}>Refresh Interval: </FormLabel>
                    <FormControl value={interval} type="number" placeholder="2" className="mr-sm-2"
                                 onChange={event => setInterval(parseInt(event.target.value))} required={true}/>
                    <Form.Control defaultValue={intervalUnit} as="select" className={"mr-1"}
                                  onChange={event => setIntervalUnit(event.target.value)}>
                        <option value={"s"}>Seconds</option>
                        <option value={"m"}>Minutes</option>
                        <option value={"h"}>Hours</option>
                    </Form.Control>
                </Form>
            </Navbar>
            <Jumbotron className={'m-0 p-5 pb-6'}>
                <h1>Current Stats</h1>
                <div className="highlight">
                    <pre>
                        <code className="language-html" data-lang="html">
                            {JSON.stringify(stats) !== "{}" ? JSON.stringify(stats, undefined, 4) : "No Data"}
                        </code>
                    </pre>
                </div>
                <br/>
                <h1>/foodAndWater?index=1</h1>
                <div className="highlight">
                    <pre>
                        <code className="language-html" data-lang="html">
                            {JSON.stringify(foodAndWaterReq) !== "{}" ? JSON.stringify(foodAndWaterReq, undefined, 4) : "No Data"}
                        </code>
                    </pre>
                </div>
                <Form inline>
                    <FormLabel className={"text-black mr-1 lead"}>Index: </FormLabel>
                    <FormControl id={"cage"} value={interval} type="number" placeholder="2" className="mr-sm-2"
                                 onChange={event => setInterval(parseInt(event.target.value))} required={true}/>
                    <Button onClick={() => window.open(service_url+":8110/foodAndWater?index=" + document.getElementById("cage").value)}>Fetch</Button>
                </Form>
                <br/>
                <h1>/cageReadings?index=1</h1>
                <div className="highlight">
                    <pre>
                        <code className="language-html" data-lang="html">
                            {JSON.stringify(cageReq) !== "{}" ? JSON.stringify(cageReq, undefined, 4) : "No Data"}
                        </code>
                    </pre>
                </div>
                <Form inline>
                    <FormLabel className={"text-black mr-1 lead"}>Index: </FormLabel>
                    <FormControl id={"cage"} value={interval} type="number" placeholder="2" className="mr-sm-2"
                                 onChange={event => setInterval(parseInt(event.target.value))} required={true}/>
                    <Button onClick={() => window.open(service_url+":8110/cageReadings?index=" + document.getElementById("cage").value)}>Fetch</Button>
                </Form>
                <br/>
                <br/>
                <br/>
            </Jumbotron>
            <Navbar fixed={"bottom"} bg="dark" variant="dark">
                <div className={"navbar-left"} style={{marginRight: '5%'}}>
                    <p className={"text-white lead m-2"}> <span className={"strong"}>Last Updated:</span> {lastUpdated}</p>
                </div>
                <div className={"navbar-center"} style={{marginRight: '5%'}}>
                    <p className={"text-white lead m-2"}> Next Update: {nextUpdate.toLocaleString()}</p>
                </div>
                <Form inline className={"navbar-right"} style={{position: "absolute", right: "1%"}}>
                    <Button variant="outline-info m-1" onClick={updateDashboard} disabled={loading}>{loading ? (<>
                        <Spinner size={"sm"} animation="border"
                                 variant="primary"/> Updating... </>) : "Update Now"}</Button>
                </Form>
            </Navbar>
        </>
    );
}

export default App;
