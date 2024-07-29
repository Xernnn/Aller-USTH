using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class FruitGameManager : MonoBehaviour
{
    int score;
    public Text scoreText;
    public bool gameIsOver;
    public GameObject gameOverPanel;
    public Text highscoreText;
    private int highscore;
    public Text GameOverPointText;

    void Start()
    {
        gameIsOver = false;
        score = 0;

        highscore = PlayerPrefs.GetInt("Highscore", 0);
        highscoreText.text = "Highscore: " + highscore;
    }

    public void UpdateTheScore(int scorePointsToAdd)
    {
        score += scorePointsToAdd;
        scoreText.text = "Score: " + score;
    }

    public void GameOver()
    {
        gameIsOver = true;
        GameOverPointText.text = "SCORE: " + Mathf.FloorToInt(score);

        if (Mathf.FloorToInt(score) > highscore)
        {
            highscore = Mathf.FloorToInt(score);
            PlayerPrefs.SetInt("Highscore", highscore);
            highscoreText.text = "Highscore: " + highscore;
        }
        
        gameOverPanel.SetActive(true);
    }
}
