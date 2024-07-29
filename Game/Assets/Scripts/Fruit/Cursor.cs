using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cursor : MonoBehaviour
{
    private Rigidbody rb;
    private SphereCollider sc;
    private TrailRenderer tr;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        sc = GetComponent<SphereCollider>();
        tr = GetComponent<TrailRenderer>();
        InitializeCursor();
    }

    void Update()
    {
        tr.enabled = true;
        sc.enabled = true;
    }

    public void InitializeCursor()
    {
        rb.velocity = Vector3.zero;
        rb.angularVelocity = Vector3.zero;
        tr.Clear();
    }
}