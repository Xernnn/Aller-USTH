using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CursorManager : MonoBehaviour
{
    public SocketClient socketClient;
    public GameObject landmarkPoint;

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

            float x = 20 + float.Parse(points[18])/(-10);
            float y = 10 + -(float.Parse(points[19]) / 10);

            landmarkPoint.transform.localPosition = new Vector3(x, y, 0);
        }
        else
        {
            Debug.LogWarning("SocketClient is null");
        }
    }
}
