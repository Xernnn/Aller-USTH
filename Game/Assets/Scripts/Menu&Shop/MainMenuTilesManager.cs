using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainMenuTileManager : MonoBehaviour
{
    public GameObject tilePrefab;
    private List<GameObject> activeTiles = new List<GameObject>();
    public float zSpawn = 15;
    public float tileLength = 35;
    public int numberOfTiles = 5;
    public Transform playerTransform;

    void Start()
    {
        for (int i = 0; i < numberOfTiles; i++)
        {
            SpawnTile();
        }
    }

    void Update()
    {
        if (playerTransform.position.z - 65 > zSpawn - (numberOfTiles * tileLength))
        {
            SpawnTile();
            DeleteTile();
        }
    }

    public void SpawnTile()
    {
        GameObject go = Instantiate(tilePrefab, transform.forward * zSpawn, transform.rotation);
        activeTiles.Add(go);
        zSpawn += tileLength;
    }

    private void DeleteTile()
    {
        Destroy(activeTiles[0]);
        activeTiles.RemoveAt(0);
    }
}