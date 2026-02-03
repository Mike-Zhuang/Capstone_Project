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

    // Store latest data for other scripts to read
    public ServerData latestData;

    void Start()
    {
        ConnectToServer();
    }

    void ConnectToServer()
    {
        try
        {
            // Port must be 65500 (matching your Python server)
            client = new TcpClient("127.0.0.1", 65500);
            stream = client.GetStream();
            isRunning = true;

            // Start a background thread to receive data
            receiveThread = new Thread(ReceiveData);
            receiveThread.IsBackground = true;
            receiveThread.Start();

            Debug.Log("✅ Successfully connected to Python backend!");
        }
        catch (Exception e)
        {
            Debug.LogError("❌ Connection failed (please run python server.py first): " + e.Message);
        }
    }

    /// <summary>
    /// Send a command to the Python backend
    /// </summary>
    /// <param name="command">Command: "n", "r", "g", or "o"</param>
    public void SendCommand(string command)
    {
        if (stream != null && stream.CanWrite)
        {
            try
            {
                byte[] data = Encoding.UTF8.GetBytes(command + "\n");
                stream.Write(data, 0, data.Length);
                Debug.Log($"📤 Sent command to Python: {command}");
            }
            catch (Exception e)
            {
                Debug.LogWarning("Failed to send command: " + e.Message);
            }
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
                        // Simple processing: split by newline, take the last valid data
                        string[] lines = jsonStr.Split('\n');
                        foreach (var line in lines)
                        {
                            if (!string.IsNullOrEmpty(line))
                            {
                                // Parse JSON
                                latestData = JsonUtility.FromJson<ServerData>(line);
                            }
                        }
                    }
                }
            }
            catch (Exception e)
            {
                Debug.LogWarning("Data stream disconnected: " + e.Message);
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