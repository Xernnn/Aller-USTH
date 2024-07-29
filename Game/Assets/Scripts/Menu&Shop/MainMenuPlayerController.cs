using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainMenuPlayerController : MonoBehaviour
{
    private CharacterController controller;
    private Vector3 direction;
    public float forwardSpeed;

    public float Gravity = -20;
    public Animator animator;

    void Start()
    {
        controller = GetComponent<CharacterController>();

        if (controller == null)
        {
            Debug.LogError("CharacterController component not found on the GameObject. Please add a CharacterController component.");
            enabled = false; // Disable the script if CharacterController is not found
            return;
        }

        Time.timeScale = 1.2f;
    }

    private void FixedUpdate()
    {
        if (controller == null)
        {
            return;
        }

        controller.Move(direction * Time.fixedDeltaTime);
    }

    void Update()
    {
        if (controller == null)
        {
            return;
        }

        animator.SetBool("isGameStarted", true);
        animator.SetBool("isGrounded", true);

        direction.z = forwardSpeed;

        if (controller.isGrounded)
        {
            direction.y = 0;
        }
        else
        {
            direction.y += Gravity * Time.deltaTime;
        }
    }
}