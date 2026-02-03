using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class ShelterController : MonoBehaviour
{
    public PythonConnector connector;

    [Header("--- Drag Objects Here ---")]
    public Transform leadShield;        // Lead shield (Transform)
    public GameObject toxicGasOutside;  // Toxic gas particles (GameObject)
    public Transform ventilationFan;    // Ventilation fan Quad (Transform)
    public ParticleSystem oxygenBubbles;// Water tank particles (ParticleSystem)
    public Light alarmLight;            // Alarm light (Light)
    public TextMeshProUGUI dashboardText; // Dashboard text on wall

    [Header("--- Drag Buttons Here ---")]
    public Button btnRadiation;
    public Button btnGas;
    public Button btnOxygen;  // New: Oxygen button
    public Button btnReset;

    [Header("--- Animation Parameters ---")]
    public float shieldOpenY = 5.0f;
    public float shieldClosedY = 2.0f;
    public float animSpeed = 2.0f;

    // Internal state tracking
    private string currentMode = "n";  // n=normal, r=radiation, g=gas, o=oxygen
    private float targetShieldY;

    void Start()
    {
        targetShieldY = shieldOpenY;

        // Bind buttons with command sending
        if (btnRadiation) btnRadiation.onClick.AddListener(TriggerRadiation);
        if (btnGas) btnGas.onClick.AddListener(TriggerGas);
        if (btnOxygen) btnOxygen.onClick.AddListener(TriggerOxygen);
        if (btnReset) btnReset.onClick.AddListener(ResetSystem);
    }

    void Update()
    {
        // 1. Lead shield animation
        if (leadShield != null)
        {
            Vector3 pos = leadShield.position;
            float newY = Mathf.MoveTowards(pos.y, targetShieldY, animSpeed * Time.deltaTime);
            leadShield.position = new Vector3(pos.x, newY, pos.z);
        }

        // 2. Fan rotation (rotates when no gas, stops when gas)
        if (ventilationFan != null)
        {
            if (currentMode != "g") ventilationFan.Rotate(0, 0, -300 * Time.deltaTime);
        }

        // 3. Update dashboard display
        UpdateDashboard();

        // 4. Alarm light effects
        if (currentMode != "n")
        {
            alarmLight.color = Color.red;
            alarmLight.intensity = Mathf.PingPong(Time.time * 5, 3); // Flashing
        }
        else
        {
            alarmLight.color = Color.cyan;
            alarmLight.intensity = 1.5f;
        }

        // 5. Toxic gas visual effect
        if (toxicGasOutside != null) toxicGasOutside.SetActive(currentMode == "g");
        
        // 6. Oxygen bubbles effect
        if (oxygenBubbles != null)
        {
            if (currentMode == "o" && !oxygenBubbles.isPlaying)
                oxygenBubbles.Play();
            else if (currentMode != "o" && oxygenBubbles.isPlaying)
                oxygenBubbles.Stop();
        }
    }

    void TriggerRadiation()
    {
        currentMode = "r";
        targetShieldY = shieldClosedY; // Lower lead shield
        
        // Send command to Python backend!
        if (connector != null) connector.SendCommand("r");
    }

    void TriggerGas()
    {
        currentMode = "g";
        targetShieldY = shieldOpenY; // Raise lead shield
        
        // Send command to Python backend!
        if (connector != null) connector.SendCommand("g");
    }
    
    void TriggerOxygen()
    {
        currentMode = "o";
        targetShieldY = shieldOpenY;
        
        // Send command to Python backend!
        if (connector != null) connector.SendCommand("o");
    }

    void ResetSystem()
    {
        currentMode = "n";
        targetShieldY = shieldOpenY;
        
        // Send command to Python backend!
        if (connector != null) connector.SendCommand("n");
    }

    void UpdateDashboard()
    {
        if (dashboardText == null) return;

        // Get AI prediction from Python
        float waterUsage = 0;
        string pythonAlert = "SYSTEM NORMAL";
        string pythonAction = "MONITORING";
        
        if (connector != null && connector.latestData != null)
        {
            waterUsage = connector.latestData.prediction_water;
            pythonAlert = connector.latestData.alert_message;
            pythonAction = connector.latestData.action_plan;
        }

        string status = pythonAlert;
        string action = pythonAction;
        string colorTag = "green";

        if (currentMode == "r")
        {
            colorTag = "red";
        }
        else if (currentMode == "g")
        {
            colorTag = "orange";
        }
        else if (currentMode == "o")
        {
            colorTag = "yellow";
        }

        string txt = $"<size=120%>=== SHELTER OS ===</size>\n\n";
        txt += $"STATUS: <color={colorTag}>{status}</color>\n";
        txt += $"ACTION: {action}\n\n";
        txt += $"[AI PREDICTION]\n";
        txt += $"Water Usage (24h): {waterUsage} L";

        dashboardText.text = txt;
    }
}