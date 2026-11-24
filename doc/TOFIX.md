# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `src/pyscrapers/core/ffprobe.py:18` - the guard is inverted: it raises `TypeError` when the path *is* a `str`, so every `width`/`height`/`duration` call with a normal path fails (e.g. `ext_requests.py:91`); change to `if not isinstance(vid_file_path, str)`.
- `src/pyscrapers/workers/drumeo.py:233` - `session.download_url(course.resources, path, session)` passes 3 arguments to `download_url(source, target)` (`core/ext_requests.py:66`), and line 235 passes `session` as an extra first positional to `download_video_if_wider(source, target, width)`, which gives `width` twice; both raise `TypeError`, so the `drumeo` command cannot download anything. Drop the extra `session` arguments.
- `src/pyscrapers/workers/vk.py:56` - unpacks `for base, json_obj in yield_json_objs_and_base(r)`, but the generator yields `(json_obj, base)` (line 37), so `get_urls` indexes `json_obj["temp"]` on a string and fails; swap the order.
- `src/pyscrapers/workers/facebook.py:28` - `url_set.append(elements_img)` appends the whole list of `<img>` elements as one "url" (unhashable list -> `TypeError` in `UrlSet.append`); append each element's `src`.

## Medium

- `src/pyscrapers/workers/facebook.py:22` - the URL `https://www.facebook.com/{user_id}/workers` (and mamba's `/albums/workers/` and `album["workers"]` at `src/pyscrapers/workers/mamba_ru.py:14`, `:35`) are artifacts of the 2020 `photos -> workers` package rename (commit 6d19694, which changed `.../photos` to `.../workers`); restore `photos`.
- `src/pyscrapers/workers/youtube_dl_handlers.py:48` - the stray `"restrict"` followed by a comment and `"fixup": "never"` is implicit string concatenation, producing the key `"restrictfixup"`, so `fixup` is never set; remove `"restrict"` (or finish it as `"restrictfilenames": True,`).
- `pyproject.toml:45` - depends on `youtube-dl`, whose last PyPI release is from 2021 and no longer works with current sites; migrate `youtube_dl_handlers.py` to `yt-dlp` (API-compatible `YoutubeDL`).
- `src/pyscrapers/core/url_set.py:83` - `if filename is None` can never be true: `get_filename` raises `ValueError` for any suffix other than `.jpg/.mp4/.webp` (line 59), so one unknown URL aborts the whole download instead of being skipped; return `None` for unknown suffixes or catch the error.
- `src/pyscrapers/core/ext_requests.py:28` - `save_text`/`save_binary` (line 35) swallow `OSError` after `os.unlink`, which itself raises `FileNotFoundError` if `open` failed, and on success-path errors the caller still logs "written"; re-raise after cleanup. `download_url` (line 76) also uses `save_text`, which UTF-8-decodes binary downloads such as `resources.zip`; use `save_binary`.
- `src/pyscrapers/core/ext_requests.py:91` - `download_video_if_wider` compares the file's `height` against the requested `width`; call `ffprobe.width`.
- `src/pyscrapers/core/url_set.py:89` - `session.get(url, stream=True)` has no timeout, so the `--connect-timeout/--read-timeout` options (`configs.py:124`) are ignored for the actual downloads; pass `timeout=(ConfigRequests.connect_timeout, ConfigRequests.read_timeout)`.

## Low

- `src/pyscrapers/workers/getpocket.py:22` - Pocket was shut down by Mozilla in 2025, so the `getpocket` command can only fail; remove the worker and endpoint (`main.py:116`).
- `src/pyscrapers/workers/netflix.py:8` - `netflix_list` is registered as a command (`main.py:148`) but its body is only a comment; remove it or implement it.
- `src/pyscrapers/core/ext_requests.py:28` - debug output goes to fixed, predictable `/tmp` paths (`/tmp/temp` here, `/tmp/single.html` and `/tmp/page{N}.html` in `workers/audible.py:24`, `:91`), which can be symlink-hijacked on a shared host; use `tempfile`.
- `src/pyscrapers/core/ext_requests.py:7` - `import urllib` then uses `urllib.parse.urljoin` (line 61), which only works if something else imported `urllib.parse`; import `urllib.parse`.
- `src/pyscrapers/configs.py:20` - `WARNING` is listed twice in the log-level choices; drop the duplicate.
- `rsconstruct.toml:53` - sphinx `dep_inputs = ["src/pyscrapers/*.py"]` misses the `core/` and `workers/` subpackages that the sphinx docs autodoc; include them.
- `pyproject.toml:92` - `mypy_path = "src:python:scripts"` names `python` and `scripts` directories that do not exist; reduce to `src`.
- `src/pyscrapers/main.py:106` - typos in user-visible help: "youtuble_dl", and "stroies" at line 164.
