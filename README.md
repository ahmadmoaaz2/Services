# Aviary Monitor

This project is a demonstration of a microservice setup with deployment files and build scripts


Below are sample event objects that are passed in to get results.

```
POST /foodAndWater   
[
    {name: "bowl1", type: "water", waterPurity: "98%", waterLevel: "76%", waterTemperature: 19}, 
    {name: "bowl2", type: "food", foodWeight: 100}
]

POST /cageReadings  
{
    temperature: 21, 
    birdlocations: 
        ["top-center-left", bottom-left-frontCorner]
}

GET /settings  
{
    currentSettings: {}, 
    defaultSettings: {}
}  

POST /settings  
{
    temperatureUnit: "C", 
    wieghtUnit: "g", 
    bowlWieghts: 
        {one: "100"}
}

Peak Number of Events: 200 every day. around 1 every 5 minutes.

Users
The users of the system could be an app that monitors the state of an aviary and possibly even automatically maintains it
