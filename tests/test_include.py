import yaml

from conda_devenv.devenv import handle_includes, render_jinja


def obtain_yaml_dicts(root_yaml_filename):
    contents = open(root_yaml_filename, "r").read()
    contents = render_jinja(contents, filename=root_yaml_filename)
    root_yaml = yaml.load(contents)
    dicts = handle_includes(root_yaml).values()
    dicts = list(dicts)

    # The list order does not matter, so we can"t use indices to fetch each item
    dicts = {d["name"]: d for d in dicts}
    return dicts


def test_include(datadir):
    datadir["a.yml"]
    datadir["b.yml"]
    datadir["c.yml"]

    dicts = obtain_yaml_dicts(datadir["c.yml"])
    assert len(dicts) == 3

    assert dicts["a"] == {
        "name": "a",
        "dependencies": [
            "a_dependency",
        ],
        "environment": {
            "PATH": [
                "a_path"
            ]
        }
    }

    assert dicts["b"] == {
        "name": "b",
        "dependencies": [
            "b_dependency",
        ],
        "environment": {
            "PATH": [
                "b_path"
            ]
        },
        "channels": [
            "b_channel",
        ],
    }

    assert dicts["c"] == {
        "name": "c",
        "channels": [
            "c_channel",
        ],
    }


def test_include_non_dag(datadir):
    datadir["a_non_dag.yml"]
    datadir["b_non_dag.yml"]

    dicts = obtain_yaml_dicts(datadir["b_non_dag.yml"])

    assert dicts["a"] == {
        "name": "a",
        "dependencies": [
            "a_dependency",
        ],
    }

    assert dicts["b"] == {
        "name": "b",
        "dependencies": [
            "b_dependency",
        ],
    }