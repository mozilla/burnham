# Development

## Custom Glean SDK distribution

When working on a bug fix for the Python bindings for the Glean SDK, you may
wish to replace the glean-sdk wheel installed in the burnham Docker image
with a custom distribution.

Bump the glean-sdk version identifier before you build a wheel distribution
for the glean-sdk and optionally every dependency of glean-sdk that you added
or upgraded. Be sure to check the `requirements.txt` file for the pinned
dependencies. 📦

Then update the [Dockerfile][dockerfile] to copy the local wheels into the
Docker image:

```text
COPY --from=wheels /wheels/*.whl /tmp/wheels/

# Copy custom distribution to temporary wheels directory in image
COPY glean_sdk-31.2.1-cp36-abi3-manylinux1_x86_64.whl /tmp/wheels/
```

Then make sure that the version requirement for the Python bindings for the
Glean SDK and its dependencies in the [burnham setup.py][setup.py] matches
your custom distributions.

```text
install_requires=["click>=7.0", "glean-sdk==31.2.1", "wrapt", "typing_extensions"]
```

When you build the burnham Docker image you should now see a message that pip
has installed your custom wheels in the log.

## Run burnham missions locally

You can run the `fake-data-platform` and the burnham missions locally using
`docker-compose`. Run the following command from the top-level directory:

```text
docker-compose up --build
```

This will launch the platform and run 3 additional containers running
`burnham`. It will print logs from all containers to stdout, the log of
`platform` should show the received pings. The `burnham` containers will exit
automatically, you can stop the platform with Ctrl-C.

[dockerfile]: ../Dockerfile
