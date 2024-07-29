using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Fruits : MonoBehaviour
{
    private FruitGameManager gm;
    public GameObject slicedFruit;
    public GameObject fruitJuice;

    private float rotationForce = 200;
    private Rigidbody rb;
    public int scorePoints;

    void Awake()
    {
        string currentSceneName = SceneManager.GetActiveScene().name;
        if (currentSceneName != "FruitOnly")
        {
            this.enabled = false;
        }
    }
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        gm = FindObjectOfType<FruitGameManager>();
    }

    void Update()
    {
        transform.Rotate(Vector2.right * Time.deltaTime * rotationForce);
    }

    private void InstantiateSlicedFruit()
    {
        GameObject instantiatedFruit = Instantiate(slicedFruit, transform.position, transform.rotation);
        GameObject instantiatedJuice = Instantiate(fruitJuice, new Vector3(transform.position.x, transform.position.y, 0), fruitJuice.transform.rotation);
    
        Rigidbody[] slicedRb = instantiatedFruit.transform.GetComponentsInChildren<Rigidbody>();

        foreach (Rigidbody srb in slicedRb)
        {
            srb.AddExplosionForce(130f, transform.position, 10);
            srb.velocity = rb.velocity * 1.2f;
        }

        Destroy(instantiatedFruit, 4);
        Destroy(instantiatedJuice, 4);
    }

    private void OnTriggerEnter(Collider other)
    {
        string currentSceneName = SceneManager.GetActiveScene().name;
        if (currentSceneName == "FruitOnly")
        {
            if (other.tag == "Blade")
            {
                gm.UpdateTheScore(scorePoints);
                Destroy(gameObject);
                InstantiateSlicedFruit();
            }
        }
    }
}
