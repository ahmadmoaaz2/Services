import React, {useEffect, useState} from 'react';
import { Button, Navbar, Nav, Form, FormControl, FormLabel } from 'react-bootstrap';

const service_url = "http://services-based-kafka.westus.cloudapp.azure.com"


function App() {
    let [active, setActive] = useState("home")
    let [interval, setInterval] = useState(2)
    let [intervalUnit, setIntervalUnit] = useState("s")
    let [lastUpdated, setLastUpdated] = useState(new Date().toLocaleString())
    let [loading, setLoading] = useState(true)
    let [stats, setStats] = useState({})
    let [foodAndWaterReq, setFoodAndWaterReq] = useState({})
    let [cageReq, setCageReq] = useState({})

    async function updateDashboard(){
        setLoading(true)
        await Promise.all([
            fetch(service_url + ":8100/stats").then(response => {
                if (!response.ok && response.status !== 200)
                    return Promise.reject("Error in request")
                response.json()
            }).then(json => {
                setStats(json)
            }).catch(e => {
                console.error(e)
                setStats({})
            }),
            fetch(service_url + ":8110/foodAndWater?index=1").then(response => response.json()).then(json => {
                setFoodAndWaterReq(json)
            }).catch(e => {
                console.error(e)
                setFoodAndWaterReq({})
            }),
            fetch(service_url + ":8110/cageReadings?index=1").then(response => response.json()).then(json => {
                setCageReq(json)
            }).catch(e => {
                console.error(e)
                setCageReq({})
            }),
        ])
        setLastUpdated(new Date().toLocaleString())
        setLoading(false)
    }

    useEffect(() => {
        let totalInterval = 1000 * interval
        switch (intervalUnit){
            case "m":
                totalInterval *= 60
                break;
            case "h":
                totalInterval *= 60 * 60
                break;
            default:
                break;
        }
        setTimeout(updateDashboard, totalInterval)
    }, [interval, intervalUnit, lastUpdated])

    function changeInterval(formData) {
        console.log(formData.target[0])
    }
    return (
        <>
            <Navbar bg="dark" variant="dark">
                <Navbar.Brand className={"lead"} href="/">Aviary Monitor API</Navbar.Brand>
                <Nav className="mr-auto">
                    <Nav.Link href="/" active={active === "home"}>Dashboard</Nav.Link>
                </Nav>
                <Form inline onSubmit={changeInterval}>
                    <FormLabel className={"text-white mr-1 lead"}>Refresh Interval: </FormLabel>
                    <FormControl type="text" placeholder="2" className="mr-sm-2"
                                 onChange={event => setInterval(parseInt(event.target.value))}/>
                    <Form.Control as="select" className={"mr-1"}  onChange={event => setIntervalUnit(event.target.value)}>
                        <option value={"s"}>Seconds</option>
                        <option value={"m"}>Minutes</option>
                        <option value={"h"}>Hours</option>
                    </Form.Control>
                    <Button variant="outline-info" type={"submit"}>Confirm</Button>
                </Form>
            </Navbar>
            <Button onClick={updateDashboard}>Click</Button>
        </>
    );
}

export default App;
