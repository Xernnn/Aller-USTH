using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandTracking : MonoBehaviour
{
    public SocketClient socketClient;
    public GameObject[] landmarkPoints;

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
        string data = socketClient.Data;

        data = data.Replace("[", "").Replace("]", "");

        string[] points = data.Split(',');

        for (int i = 0; i < 9; i++)
        {
            float x = 2.5f + float.Parse(points[i * 2])/(-90);
            float y = 3.5f + -(float.Parse(points[i * 2 + 1]) / 100);

            landmarkPoints[i].transform.localPosition = new Vector3(x, y, 30);

            if (i == 1)
            {
                landmarkPoints[9].transform.localPosition = new Vector3(x, y - 0.7f, 30);
                landmarkPoints[10].transform.localPosition = new Vector3(x, y - 1.5f, 30);
            }

            if (i == 0)
            {
                landmarkPoints[11].transform.localPosition = new Vector3(x, y - 0.7f, 30);
                landmarkPoints[12].transform.localPosition = new Vector3(x, y - 1.5f, 30);
            }
        }
    }
}
