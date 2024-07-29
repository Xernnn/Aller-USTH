using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class SocketClient : MonoBehaviour
{
    private TcpClient socketConnection;
    private NetworkStream networkStream;
    public int Port = 5052;
    public bool StartReceiving = true;
    public bool PrintToConsole = false;
    public string Data;

    private UdpClient udpClient;
    public int UdpPort = 5053;

    public static SocketClient Instance { get; private set; }

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        if (StartReceiving)
        {
            ConnectToServer();
        }
        udpClient = new UdpClient();
    }

    void ConnectToServer()
    {
        try
        {
            socketConnection = new TcpClient("127.0.0.1", Port);
            networkStream = socketConnection.GetStream();
            Debug.Log("Connected to the server.");
        }
        catch (Exception e)
        {
            Debug.LogError("Socket error: " + e);
        }
    }

    void Update()
    {
        if (networkStream != null && networkStream.DataAvailable)
        {
            byte[] bytes = new byte[socketConnection.ReceiveBufferSize];
            networkStream.Read(bytes, 0, bytes.Length);
            string data = Encoding.ASCII.GetString(bytes).Trim('\0');
            Data = data;
            if (PrintToConsole)
            {
                Debug.Log(data);
            }
        }
    }

    public void SendUdpMessage(string message)
    {
        byte[] data = Encoding.UTF8.GetBytes(message);
        udpClient.Send(data, data.Length, "127.0.0.1", UdpPort);
    }

    void OnApplicationQuit()
    {
        if (networkStream != null)
            networkStream.Close();
        if (socketConnection != null)
            socketConnection.Close();
        if (udpClient != null)
            udpClient.Close();
    }
}