using UnityEngine;

public class Wall : MonoBehaviour
{
    private float speed;
    private Vector3 targetPosition = new Vector3(0, 0, -10);

    public void SetSpeed(float newSpeed)
    {
        speed = newSpeed;
    }

    void Update()
    {
        transform.position = Vector3.MoveTowards(transform.position, targetPosition, speed * Time.deltaTime);

        if (transform.position == targetPosition)
        {
            Destroy(gameObject);
        }
    }
}
