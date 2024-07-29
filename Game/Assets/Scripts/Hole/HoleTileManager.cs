using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HoleTileManager : MonoBehaviour
{
    public GameObject[] tilePrefabs;
    public GameObject[] startPrefabs;
    private List<GameObject> activeTiles = new List<GameObject>();
    public float zSpawn = 15;
    public float tileLength = 35;
    public int numberOfTiles = 5;

    void Start()
    {
        // Spawn start tile
        SpawnStartTile();
        
        // Spawn fixed number of additional tiles
        for (int i = 0; i < numberOfTiles; i++)
        {
            SpawnTile(Random.Range(0, tilePrefabs.Length));
        }
    }

    public void SpawnTile(int tileIndex)
    {
        GameObject go = Instantiate(tilePrefabs[tileIndex], transform.forward * zSpawn, transform.rotation);
        activeTiles.Add(go);
        zSpawn += tileLength;
    }

    public void SpawnStartTile()
    {
        int tileIndex = Random.Range(0, startPrefabs.Length);
        GameObject go = Instantiate(startPrefabs[tileIndex], transform.forward * zSpawn, transform.rotation);
        activeTiles.Add(go);
        zSpawn += tileLength;
    }
}
