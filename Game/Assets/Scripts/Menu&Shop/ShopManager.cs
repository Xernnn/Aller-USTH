using UnityEngine;

public class ShopManager : MonoBehaviour
{
    public GameObject shopCanvas;
    public GameObject modelCanvas;
    public GameObject bladeCanvas;

    void Start()
    {
        // Start with only the ShopCanvas active
        shopCanvas.SetActive(true);
        modelCanvas.SetActive(false);
        bladeCanvas.SetActive(false);
    }

    public void ShowModelCanvas()
    {
        shopCanvas.SetActive(false);
        modelCanvas.SetActive(true);
        bladeCanvas.SetActive(false);
    }

    public void ShowBladeCanvas()
    {
        shopCanvas.SetActive(false);
        modelCanvas.SetActive(false);
        bladeCanvas.SetActive(true);
    }

    public void ShowShopCanvas()
    {
        shopCanvas.SetActive(true);
        modelCanvas.SetActive(false);
        bladeCanvas.SetActive(false);
    }
}
