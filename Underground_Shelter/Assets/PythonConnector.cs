using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class PythonConnector : MonoBehaviour
{
    private TcpClient client;
    private NetworkStream stream;
    private Thread receiveThread;
    private bool isRunning = false;

    // 用来存最新的数据，给别的脚本读取
    public ServerData latestData;

    void Start()
    {
        ConnectToServer();
    }

    void ConnectToServer()
    {
        try
        {
            // 端口必须是 65500 (对应你修改后的 Python)
            client = new TcpClient("127.0.0.1", 65500);
            stream = client.GetStream();
            isRunning = true;

            // 开启一个子线程专门收数据，不卡主程序
            receiveThread = new Thread(ReceiveData);
            receiveThread.IsBackground = true;
            receiveThread.Start();

            Debug.Log("✅ 成功连接到 Python 后端！");
        }
        catch (Exception e)
        {
            Debug.LogError("❌ 连接失败 (请先运行 python server.py): " + e.Message);
        }
    }

    void ReceiveData()
    {
        while (isRunning)
        {
            try
            {
                byte[] buffer = new byte[4096];
                if (stream.CanRead)
                {
                    int bytesRead = stream.Read(buffer, 0, buffer.Length);
                    if (bytesRead > 0)
                    {
                        string jsonStr = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                        // 简单处理：按换行符切割，取最后一条有效数据
                        string[] lines = jsonStr.Split('\n');
                        foreach (var line in lines)
                        {
                            if (!string.IsNullOrEmpty(line))
                            {
                                // 解析 JSON
                                latestData = JsonUtility.FromJson<ServerData>(line);
                            }
                        }
                    }
                }
            }
            catch (Exception e)
            {
                Debug.LogWarning("数据断开: " + e.Message);
                isRunning = false;
            }
        }
    }

    void OnDestroy()
    {
        isRunning = false;
        if (client != null) client.Close();
        if (receiveThread != null) receiveThread.Abort();
    }
}