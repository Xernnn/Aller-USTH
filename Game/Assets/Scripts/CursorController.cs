using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using System.Collections.Generic;

public class CursorController : MonoBehaviour
{
    public SocketClient socketClient;
    public RectTransform cursorTransform;
    public float hoverDuration = 2f;
    private float hoverTimer = 0f;
    private Button hoveredButton = null;
    private Canvas currentCanvas;

    void Start()
    {
        InitializeSocketClient();
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

            float x = 400 + float.Parse(points[18]) * -2;
            float y = 250 + -(float.Parse(points[19]) * 2);

            cursorTransform.localPosition = new Vector3(x, y, 0);

            CheckForHoverAndClick();
        }
    }

    void CheckForHoverAndClick()
    {
        PointerEventData pointerData = new PointerEventData(EventSystem.current)
        {
            position = cursorTransform.position
        };

        List<RaycastResult> results = new List<RaycastResult>();
        EventSystem.current.RaycastAll(pointerData, results);

        foreach (RaycastResult result in results)
        {
            Button button = result.gameObject.GetComponent<Button>();
            if (button != null)
            {
                Debug.Log("Hovered over button: " + button.name);
                if (hoveredButton == button)
                {
                    hoverTimer += Time.deltaTime;
                    if (hoverTimer >= hoverDuration)
                    {
                        button.onClick.Invoke();
                        Debug.Log("Button clicked: " + button.name);
                        hoverTimer = 0f;
                    }
                }
                else
                {
                    hoveredButton = button;
                    hoverTimer = 0f;
                }
                return;
            }
        }

        // Reset if no button is hovered
        hoveredButton = null;
        hoverTimer = 0f;
    }

    public void SetCursorCanvas(Canvas canvas)
    {
        currentCanvas = canvas;
        cursorTransform.SetParent(currentCanvas.transform, false);
    }

    private void InitializeSocketClient()
    {
        if (socketClient == null)
        {
            socketClient = FindObjectOfType<SocketClient>();
            if (socketClient == null)
            {
                Debug.LogError("SocketClient is not assigned and not found in the scene.");
            }
        }
    }
}
