using UnityEngine;
using System.Collections;

public class WallSpawner : MonoBehaviour
{
    public GameObject[] wallPrefabs; // Array of wall prefabs
    public float initialSpeed = 5f; // Initial speed of the walls
    public float speedIncreaseRate = 0.5f; // Rate at which the speed increases
    public float maxSpeed = 15f; // Maximum speed of the walls
    public float initialSpawnInterval = 20f; // Initial time between wall spawns
    public float spawnIntervalDecreaseRate = 0.5f; // Rate at which the spawn interval decreases
    public float minSpawnInterval = 10f; // Minimum time between wall spawns

    private float currentSpeed;
    private float currentSpawnInterval;

    void Start()
    {
        currentSpeed = initialSpeed;
        currentSpawnInterval = initialSpawnInterval;
        StartCoroutine(SpawnWalls());
    }

    IEnumerator SpawnWalls()
    {
        while (true)
        {
            SpawnWall();
            yield return new WaitForSeconds(currentSpawnInterval);
            currentSpeed = Mathf.Min(maxSpeed, currentSpeed + speedIncreaseRate);
            currentSpawnInterval = Mathf.Max(minSpawnInterval, currentSpawnInterval - spawnIntervalDecreaseRate);
        }
    }

    void SpawnWall()
    {
        int randomIndex = Random.Range(0, wallPrefabs.Length);
        GameObject wall = Instantiate(wallPrefabs[randomIndex], new Vector3(0, 0, 70), Quaternion.identity);
        wall.GetComponent<Wall>().SetSpeed(currentSpeed);
    }
}
