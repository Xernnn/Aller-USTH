using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerController : MonoBehaviour
{
    private CharacterController controller;
    private Vector3 direction;
    public float forwardSpeed;
    public float maxSpeed;

    private int desiredLane = 1; // 0--1--2
    public float laneDistance = 3f;

    public float jumpForce;
    public float Gravity = -20;

    public Animator animator;
    private bool isSliding = false;

    void Start()
    {
        controller = GetComponent<CharacterController>();
        Time.timeScale = 1.2f;
    }

    private void FixedUpdate()
    {
        if (!PlayerManager.isGameStarted)
        {
            return;
        }
        controller.Move(direction * Time.fixedDeltaTime);
    }

    void Update()
    {
        if (!PlayerManager.isGameStarted)
        {
            return;
        }

        if (PlayerManager.gameOver)
        {
            forwardSpeed = 0;
        }

        animator.SetBool("isGameStarted", true);
        animator.SetBool("isGrounded", controller.isGrounded);

        if (forwardSpeed < maxSpeed)
        {
            forwardSpeed += 0.015f * Time.deltaTime;
        }

        direction.z = forwardSpeed;

        if (controller.isGrounded)
        {
            if (RunManager.move == 3) // Replace Input.GetKeyDown(KeyCode.W)
            {
                Jump();
            }
        }
        else
        {
            direction.y += Gravity * Time.deltaTime;
        }

        if (RunManager.move == 4 && !isSliding) // Replace Input.GetKeyDown(KeyCode.S)
        {
            StartCoroutine(Slide());
        }

        if (RunManager.move == 1) // Replace Input.GetKeyDown(KeyCode.D)
        {
            desiredLane++;
            if (desiredLane == 3)
                desiredLane = 2;
            else {
                StartCoroutine(Right());
            }
        }
        if (RunManager.move == 2) // Replace Input.GetKeyDown(KeyCode.A)
        {
            desiredLane--;
            if (desiredLane == -1)
                desiredLane = 0;
            else {
                StartCoroutine(Left());
            }
        }

        Vector3 targetPosition = transform.position.z * transform.forward + transform.position.y * transform.up;

        if (desiredLane == 0)
        {
            targetPosition += Vector3.left * laneDistance;
        }
        else if (desiredLane == 2)
        {
            targetPosition += Vector3.right * laneDistance;
        }

        if (transform.position == targetPosition)
        {
            return;
        }
        Vector3 diff = targetPosition - transform.position;
        Vector3 moveDir = diff.normalized * 25 * Time.deltaTime;
        if (moveDir.sqrMagnitude < diff.sqrMagnitude)
        {
            controller.Move(moveDir);
        }
        else
        {
            controller.Move(diff);
        }
    }

    private void Jump()
    {
        direction.y = jumpForce;
    }

    private void OnControllerColliderHit(ControllerColliderHit hit)
    {
        if (hit.transform.CompareTag("Obstacle"))
        {
            PlayerManager.gameOver = true;
            animator.SetBool("isGameOver", true);
        }
        else if (hit.transform.CompareTag("Table"))
        {
            Vector3 hitNormal = hit.normal;
            if (Vector3.Dot(hitNormal, Vector3.forward) < -0.7f)
            {
                PlayerManager.gameOver = true;
                animator.SetBool("isGameOver", true);
            }
        }
        else if (hit.transform.CompareTag("FruitPortal"))
        {
            int point = (int)PlayerManager.point;
            PlayerPrefs.SetInt("Score", point);
            SceneManager.LoadScene("Fruit");
        }
    }

    private IEnumerator Slide()
    {
        isSliding = true;
        Debug.Log("Slide");
        animator.SetBool("isSliding", true);
        controller.center = new Vector3(0, -0.5f, 0);
        controller.height = 0.2f;
        yield return new WaitForSeconds(1.3f);
        controller.center = new Vector3(0, 0, 0);
        controller.height = 2;
        Debug.Log("No Slide");
        animator.SetBool("isSliding", false);
        isSliding = false;
    }

    private IEnumerator Left()
    {
        Debug.Log("Left");
        animator.SetBool("isLeft", true);
        yield return new WaitForSeconds(1f);
        animator.SetBool("isLeft", false);
        Debug.Log("No Left");
    }

    private IEnumerator Right()
    {
        Debug.Log("Right");
        animator.SetBool("isRight", true);
        yield return new WaitForSeconds(1f);
        animator.SetBool("isRight", false);
        Debug.Log("No Right");
    }
}
