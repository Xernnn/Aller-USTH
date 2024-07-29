using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class FruitRunGameManager : MonoBehaviour
{
    int score;
    public Text scoreText;
    public bool gameIsOver;
    public Cursor cursor;
    public CursorManager cursorManager; 

    void Start()
    {
        gameIsOver = false;
        score = PlayerPrefs.GetInt("point", 0);
        InitializeGame();
    }

    void InitializeGame()
    {
        Debug.Log("Initializing Game");
        if (cursor != null)
        {
            cursor.InitializeCursor();
        }

        if (SocketClient.Instance == null)
        {
            Debug.LogError("SocketClient is not assigned and not found in the scene.");
            return;
        }
    }

    public void UpdateTheScore(int scorePointsToAdd)
    {
        score += scorePointsToAdd; 
        scoreText.text = "Score: " + score;
    }

    public void GameOver()
    {
        gameIsOver = true;
        PlayerPrefs.SetInt("point", score);
        SceneManager.LoadScene("Run"); 
    }
}
