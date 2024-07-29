using UnityEngine;

public class RotateModel : MonoBehaviour
{
    public float rotationSpeed = 5f;

    void Update()
    {
        Debug.Log("RotateModel script is running");
        transform.Rotate(Vector3.up, rotationSpeed * Time.deltaTime);
    }
}
