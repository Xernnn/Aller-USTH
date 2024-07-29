using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RunManager : MonoBehaviour
{
    public SocketClient socketClient;
    public static int move;

    private int previousMove = -1;
    private float lastChangeTime = 0.0f;
    private const float delay = 0.3f; // 0.5 seconds delay

    void Start()
    {
        if (socketClient == null)
        {
            socketClient = FindObjectOfType<SocketClient>();
            if (socketClient == null)
            {
                Debug.LogError("SocketClient is not assigned and not found in the scene.");
                return;
            }
        }
    }

    void Update()
    {
        if (socketClient != null)
        {
            string data = socketClient.Data;
            if (string.IsNullOrEmpty(data))
            {
                Debug.LogWarning("Received empty or null data from SocketClient.");
                return;
            }

            Debug.Log("Received Data: " + data);

            data = data.Replace("[", "").Replace("]", "");
            data = data.Replace("(", "").Replace(")", "");

            string[] points = data.Split(',');

            if (points.Length > 22)
            {
                if (int.TryParse(points[22], out int result))
                {
                    float currentTime = Time.time;
                    if (result == previousMove)
                    {
                        if (currentTime - lastChangeTime < delay)
                        {
                            move = 0;
                        }
                        else
                        {
                            move = result;
                        }
                    }
                    else
                    {
                        move = result;
                        previousMove = result;
                        lastChangeTime = currentTime;
                    }
                }
                else
                {
                    Debug.LogWarning("Unable to parse move value.");
                }
            }
            else
            {
                Debug.LogWarning("Data does not contain enough points.");
            }
        }
        else
        {
            Debug.LogWarning("SocketClient is null");
        }
    }
}
