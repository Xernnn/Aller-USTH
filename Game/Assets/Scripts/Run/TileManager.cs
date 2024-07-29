using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TileManager : MonoBehaviour
{
    public GameObject[] tilePrefabs;
    public GameObject[] startPrefabs;
    private List<GameObject> activeTiles = new List<GameObject>();
    public float zSpawn = 15;
    public float tileLength = 35;
    public int numberOfTiles = 5;
    public Transform playerTransform;
    void Start()
    {
        for (int i = 0; i < numberOfTiles; i++)
        {
            if (i == 0)
            {
                StartTile(Random.Range(0, startPrefabs.Length));
            } else
            {
                SpawnTile(Random.Range(0, tilePrefabs.Length));
            }
        }
    }

    void Update()
    {
        if (playerTransform.position.z - 65 > zSpawn - (numberOfTiles * tileLength))
        {
            SpawnTile(Random.Range(0, tilePrefabs.Length));
            DeleteTile();
        }
    }

    public void SpawnTile(int tileIndex)
    {
        GameObject go = Instantiate(tilePrefabs[tileIndex], transform.forward * zSpawn, transform.rotation);
        activeTiles.Add(go);
        zSpawn += tileLength;
    }
    public void StartTile(int tileIndex)
    {
        GameObject go = Instantiate(startPrefabs[tileIndex], transform.forward * zSpawn, transform.rotation);
        activeTiles.Add(go);
        zSpawn += tileLength;
    }

    private void DeleteTile()
    {
        Destroy(activeTiles[0]);
        activeTiles.RemoveAt(0);
    }
}
