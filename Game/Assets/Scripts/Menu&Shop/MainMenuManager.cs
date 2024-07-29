using UnityEngine;

public class MainMenuManager : MonoBehaviour
{
    public GameObject mainCanvas;
    public GameObject modeCanvas;
    public CursorController cursorController; // Add reference to CursorController

    void Start()
    {
        mainCanvas.SetActive(true);
        modeCanvas.SetActive(false);
        cursorController.SetCursorCanvas(mainCanvas.GetComponent<Canvas>()); // Notify CursorController
    }

    public void ShowModeCanvas()
    {
        mainCanvas.SetActive(false);
        modeCanvas.SetActive(true);
        cursorController.SetCursorCanvas(modeCanvas.GetComponent<Canvas>()); // Notify CursorController
    }

    public void ShowMainCanvas()
    {
        mainCanvas.SetActive(true);
        modeCanvas.SetActive(false);
        cursorController.SetCursorCanvas(mainCanvas.GetComponent<Canvas>()); // Notify CursorController
    }
}
