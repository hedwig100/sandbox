# Play-Abseil

## Tips
- [This page](https://abseil.io/docs/cpp/quickstart.html)'s bazel version is so old that you sometimes fail to build. You can use newer version of bazel to avoid this.

## Bazel Tips
- You can use environmental variable `BAZEL_CXXOPTS` to configure c++ version in bazel.
    - e.g. `export BAZEL_CXXOPTS="-std=c++14"`