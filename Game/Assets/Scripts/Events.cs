using System.Collections;
using System.Collections.Generic;
using UnityEngine.SceneManagement;
using UnityEngine;

public class Events : MonoBehaviour
{
    public void Play()
    {
        SceneManager.LoadScene("Run");
    }

    public void Shop()
    {
        SceneManager.LoadScene("Shop");
    }

    public void Fruit()
    {
        SceneManager.LoadScene("Fruit");
    }
    public void FruitOnly()
    {
        SceneManager.LoadScene("FruitOnly");
    }
    public void Hole()
    {
        SceneManager.LoadScene("Hole");
    }

    public void MainMenu()
    {
        SceneManager.LoadScene("Menu");
    }

    public void Quit()
    {
        Application.Quit();
    }
}
