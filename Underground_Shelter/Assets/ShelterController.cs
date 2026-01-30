using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class ShelterController : MonoBehaviour
{
    public PythonConnector connector;

    [Header("--- 拖拽物体 ---")]
    public Transform leadShield;        // 铅板 (Transform)
    public GameObject toxicGasOutside;  // 毒气粒子 (GameObject)
    public Transform ventilationFan;    // 刚才做的 Quad 风扇 (Transform)
    public ParticleSystem oxygenBubbles;// 水箱里的粒子 (ParticleSystem)
    public Light alarmLight;            // 警报灯 (Light)
    public TextMeshProUGUI dashboardText; // 墙上的绿字

    [Header("--- 拖拽按钮 ---")]
    public Button btnRadiation;
    public Button btnGas;
    public Button btnReset;

    [Header("--- 动画参数 (不用改) ---")]
    public float shieldOpenY = 5.0f;
    public float shieldClosedY = 2.0f;
    public float animSpeed = 2.0f;

    // 内部变量
    private bool isRadiation = false;
    private bool isGas = false;
    private float targetShieldY;

    void Start()
    {
        targetShieldY = shieldOpenY;

        // 绑定按钮
        if (btnRadiation) btnRadiation.onClick.AddListener(TriggerRadiation);
        if (btnGas) btnGas.onClick.AddListener(TriggerGas);
        if (btnReset) btnReset.onClick.AddListener(ResetSystem);
    }

    void Update()
    {
        // 1. 铅板动画
        if (leadShield != null)
        {
            Vector3 pos = leadShield.position;
            float newY = Mathf.MoveTowards(pos.y, targetShieldY, animSpeed * Time.deltaTime);
            leadShield.position = new Vector3(pos.x, newY, pos.z);
        }

        // 2. 风扇旋转 (没毒气时转，有毒气停)
        if (ventilationFan != null)
        {
            if (!isGas) ventilationFan.Rotate(0, 0, -300 * Time.deltaTime);
        }

        // 3. 刷新屏幕
        UpdateDashboard();

        // 4. 灯光特效
        if (isRadiation || isGas)
        {
            alarmLight.color = Color.red;
            alarmLight.intensity = Mathf.PingPong(Time.time * 5, 3); // 闪烁
        }
        else
        {
            alarmLight.color = Color.cyan;
            alarmLight.intensity = 1.5f;
        }

        // 5. 毒气特效
        if (toxicGasOutside != null) toxicGasOutside.SetActive(isGas);
    }

    void TriggerRadiation()
    {
        isRadiation = true;
        isGas = false;
        targetShieldY = shieldClosedY; // 铅板落下
    }

    void TriggerGas()
    {
        isGas = true;
        isRadiation = false;
        targetShieldY = shieldOpenY; // 铅板升起
    }

    void ResetSystem()
    {
        isRadiation = false;
        isGas = false;
        targetShieldY = shieldOpenY;
    }

    void UpdateDashboard()
    {
        if (dashboardText == null) return;

        // 默认显示 Python 传来的预测值
        float waterUsage = 0;
        if (connector != null && connector.latestData != null)
            waterUsage = connector.latestData.prediction_water;

        string status = "SYSTEM NORMAL";
        string action = "MONITORING ACTIVE";
        string colorTag = "green";

        if (isRadiation)
        {
            status = "WARNING: HIGH RADIATION";
            action = "DEPLOYING SHIELD...";
            colorTag = "red";
        }
        else if (isGas)
        {
            status = "WARNING: TOXIC GAS";
            action = "SEALING VENTS...";
            colorTag = "red";
        }

        string txt = $"<size=120%>=== SHELTER OS ===</size>\n\n";
        txt += $"STATUS: <color={colorTag}>{status}</color>\n";
        txt += $"ACTION: {action}\n\n";
        txt += $"[AI PREDICTION]\n";
        txt += $"Water Usage (24h): {waterUsage} L";

        dashboardText.text = txt;
    }
}