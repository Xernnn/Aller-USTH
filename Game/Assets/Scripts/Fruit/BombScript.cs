using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class BombScript : MonoBehaviour
{
    private float rotationForce = 200;
    public ParticleSystem explosionParticle;
    
    void Awake()
    {
        string currentSceneName = SceneManager.GetActiveScene().name;
    }

    void Start()
    {
        transform.rotation = Random.rotation;
    }

    void Update()
    {
        transform.Rotate(Vector2.right * Time.deltaTime * rotationForce);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Blade")
        {
            string currentSceneName = SceneManager.GetActiveScene().name;
            Destroy(gameObject);
            Instantiate(explosionParticle, transform.position, explosionParticle.transform.rotation);
            if (currentSceneName == "Fruit")
            {
                FindObjectOfType<FruitRunGameManager>().GameOver();
            }
            else
            {
                FindObjectOfType<FruitGameManager>().GameOver();
            }
        }
    }
}
