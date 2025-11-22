# Python module

- モジュール、パッケージ、ライブラリについて
    https://zenn.dev/delacroix/articles/e3f62ca001deb0
- このディレクトリ構造で
    ```
    uv run main.py # はできるけど
    uv run a/child1.py # はできない
    ```
    たぶん実行ファイルのある位置からpython pathを探索するため
- 正確にはpythonは`sys.path`に入っているもののみ探索する, `sys.path` に入っているのは以下
    - 実行ファイルのあるディレクトリ
        - `python a.py` で実行した場合のみ
    - カレントワーキングディレクトリ
        - `python -m a` で実行した場合のみ
    - 標準ライブラリのあるディレクトリ
    - `site-packages` のあるディレクトリ(インストールしたライブラリ)
    - `PYTHONPATH` に指定されたディレクトリ
- すなわち構造的にはこうなるべき
    - `src/my-pacakge` 以下に共有で使うものを置く
    - `src/main.py`, `src/main2.py`, ... に実行ファイルを置く