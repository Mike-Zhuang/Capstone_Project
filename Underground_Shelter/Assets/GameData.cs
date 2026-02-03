using System;

[Serializable]
public class SensorData
{
    public float radiation;
    public float toxic_gas;
    public float co2;
    public float oxygen;
}

[Serializable]
public class ServerData
{
    public string mode;  // Current mode from Python: n/r/g/o
    public SensorData sensor;
    public string alert_message;
    public string action_plan;
    public float prediction_water;
}