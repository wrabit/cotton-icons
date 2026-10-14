import os
import re
import shutil
import subprocess

RELEASE_TAG = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


def latest_release_tag(repo):
    """Return the highest semver tag of ``owner/name`` via git, no API needed.

    Only plain ``1.2.3`` / ``v1.2.3`` tags count, which skips prereleases and
    sub-package tags such as ``@lucide/lab@0.2.0``.
    """
    out = subprocess.run(
        ["git", "ls-remote", "--tags", "--refs", f"https://github.com/{repo}.git"],
        check=True, capture_output=True, text=True,
    ).stdout
    tags = [line.split("refs/tags/", 1)[1] for line in out.splitlines() if "refs/tags/" in line]
    releases = [(tuple(int(n) for n in m.groups()), t) for t in tags if (m := RELEASE_TAG.match(t))]
    if not releases:
        raise RuntimeError(f"No release tags found for {repo}")
    return max(releases)[1]


def clone_release(repo, dest):
    """Clone the latest release tag of ``repo`` into ``dest`` and return the tag.

    Cloning the tag rather than the default branch keeps the SVGs and the
    reported version from the same commit. Cloning main could pick up icons
    merged after the latest release and miss others from the same release.
    """
    tag = latest_release_tag(repo)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    subprocess.run(
        ["git", "-c", "advice.detachedHead=false", "clone", "--depth", "1", "--branch", tag,
         f"https://github.com/{repo}.git", dest],
        check=True,
    )
    return tag


def reset_output_dir(path):
    """Empty the output directory so icons removed upstream do not linger."""
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
