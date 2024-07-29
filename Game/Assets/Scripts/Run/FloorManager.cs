using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FloorManager : MonoBehaviour
{
    public GameObject[] hallwayPrefabs;
    public GameObject[] shortFloorPrefabs;
    public GameObject[] longFloorPrefabs;
    public GameObject[] startPrefabs;
    
    private List<GameObject> activeFloors = new List<GameObject>();
    public float zSpawn = 0;
    public float hallwayLength = 74;
    public float shortFloorLength = 97;
    public float longFloorLength = 105;
    public int numberOfFloors = 5;
    public Transform playerTransform;

    private bool spawnHallways = false;
    private float lastSpawnLength;

    void Start()
    {
        // Spawn initial floors
        for (int i = 0; i < numberOfFloors; i++)
        {
            if (i == 0)
            {
                StartFloor(Random.Range(0, startPrefabs.Length));
            }
            else if (spawnHallways)
            {
                SpawnRandomHallways();
            }
            else
            {
                SpawnInitialFloor();
            }
        }
    }

    void Update()
    {
        // Check if player has moved enough to spawn new floors
        if (playerTransform.position.z - 65 > zSpawn - numberOfFloors * hallwayLength)
        {
            if (spawnHallways)
            {
                SpawnRandomHallways();
            }
            else
            {
                SpawnInitialFloor();
            }
            DeleteFloors();
        }
    }

    private void SpawnInitialFloor()
    {
        if (Random.value > 0.5f)
        {
            SpawnFloor(shortFloorPrefabs, shortFloorLength);
        }
        else
        {
            SpawnFloor(longFloorPrefabs, longFloorLength);
        }
        spawnHallways = true;
    }

    private void SpawnRandomHallways()
    {
        int hallwayCount = Random.Range(2, 6); // Random between 2 to 5 inclusive
        for (int i = 0; i < hallwayCount; i++)
        {
            SpawnFloor(hallwayPrefabs, hallwayLength);
        }
        spawnHallways = false;
    }

    private void SpawnFloor(GameObject[] floorPrefabs, float floorLength)
    {
        int floorIndex = Random.Range(0, floorPrefabs.Length);
        GameObject go = Instantiate(floorPrefabs[floorIndex], new Vector3(0, 0, zSpawn), transform.rotation);
        activeFloors.Add(go);
        zSpawn += floorLength;
        lastSpawnLength = floorLength;  // Track the last spawned floor length
    }

    private void StartFloor(int floorIndex)
    {
        GameObject go = Instantiate(startPrefabs[floorIndex], new Vector3(0, 0, zSpawn), transform.rotation);
        activeFloors.Add(go);
        if (IsShortFloor(go))
        {
            zSpawn += shortFloorLength - 15;
            lastSpawnLength = shortFloorLength;
        }
        else
        {
            zSpawn += longFloorLength - 15;
            lastSpawnLength = longFloorLength;
        }
    }

    private bool IsShortFloor(GameObject floor)
    {
        return new List<GameObject>(shortFloorPrefabs).Contains(floor);
    }

    private void DeleteFloors()
    {
        // Determine how many floors to delete based on the player's position
        float playerZ = playerTransform.position.z;
        int floorsToDelete = 0;

        for (int i = 0; i < activeFloors.Count; i++)
        {
            if (activeFloors[i].transform.position.z + hallwayLength < playerZ - 65)
            {
                floorsToDelete++;
            }
            else
            {
                break;
            }
        }

        // Delete the determined number of floors
        for (int i = 0; i < floorsToDelete; i++)
        {
            Destroy(activeFloors[0]);
            activeFloors.RemoveAt(0);
        }
    }
}
