using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HoleFloorManager : MonoBehaviour
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
    public int numberOfHallways = 5;

    void Start()
    {
        // Spawn start floor
        SpawnStartFloor();
        
        // Spawn fixed number of hallways
        for (int i = 0; i < numberOfHallways; i++)
        {
            SpawnFloor(hallwayPrefabs, hallwayLength);
        }
    }

    private void SpawnStartFloor()
    {
        int floorIndex = Random.Range(0, startPrefabs.Length);
        GameObject go = Instantiate(startPrefabs[floorIndex], new Vector3(0, 0, zSpawn), transform.rotation);
        activeFloors.Add(go);
        zSpawn += IsShortFloor(go) ? shortFloorLength : longFloorLength;
    }

    private void SpawnFloor(GameObject[] floorPrefabs, float floorLength)
    {
        int floorIndex = Random.Range(0, floorPrefabs.Length);
        GameObject go = Instantiate(floorPrefabs[floorIndex], new Vector3(0, 0, zSpawn), transform.rotation);
        activeFloors.Add(go);
        zSpawn += floorLength;
    }

    private bool IsShortFloor(GameObject floor)
    {
        return new List<GameObject>(shortFloorPrefabs).Contains(floor);
    }
}
