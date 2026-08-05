// Pyodide Web Worker：在浏览器里跑真实 Python。
// 学习者代码运行在访问者自己的浏览器里——不经过任何服务器，反而最安全。
// 多 CDN 自动回退：jsdelivr 不可用时切 fastly / unpkg（对国内访问更稳）。
const CDN_BASES = [
  "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/",
  "https://fastly.jsdelivr.net/pyodide/v0.26.4/full/",
  "https://unpkg.com/pyodide@v0.26.4/full/",
];

let pyodide = null;
let PYODIDE_BASE = null;

(function loadPyodideScript() {
  for (const base of CDN_BASES) {
    try {
      importScripts(base + "pyodide.js");
      PYODIDE_BASE = base;
      return;
    } catch (e) {
      // 该 CDN 不可达，试下一个
    }
  }
  throw new Error("Pyodide 的所有 CDN 都不可达，请检查网络。");
})();

function capture() {
  let buf = "";
  pyodide.setStdout({ batched: (s) => { buf += s; } });
  pyodide.setStderr({ batched: () => {} }); // 出错走 exception，不需要 stderr 流
  return () => buf;
}

self.onmessage = async (e) => {
  const { id, type } = e.data;
  try {
    if (type === "init") {
      pyodide = await loadPyodide({ indexURL: PYODIDE_BASE });
      self.postMessage({ id, type: "ready" });
      return;
    }
    if (!pyodide) {
      self.postMessage({ id, type: "result", ok: false, stderr: "魔法引擎还没准备好。" });
      return;
    }

    if (type === "run") {
      const readBuf = capture();
      try {
        pyodide.runPython(e.data.code);
        self.postMessage({ id, type: "result", ok: true, stdout: readBuf() });
      } catch (err) {
        self.postMessage({ id, type: "result", ok: false, stdout: readBuf(), stderr: String(err.message || err) });
      }
      return;
    }

    if (type === "judge") {
      const readBuf = capture();
      pyodide.FS.writeFile("solution.py", e.data.code);
      pyodide.FS.writeFile("tests.py", e.data.tests);
      try {
        // 关键：Pyodide 长驻进程会缓存已导入的模块。
        // 先踢掉旧的 solution，保证 from solution import ... 拿到的是本次新写的代码。
        pyodide.runPython(
          "import sys; sys.modules.pop('solution', None); "
          + "import runpy; runpy.run_path('tests.py', run_name='__main__')"
        );
        self.postMessage({ id, type: "result", ok: true, stdout: readBuf() });
      } catch (err) {
        self.postMessage({ id, type: "result", ok: false, stdout: readBuf(), stderr: String(err.message || err) });
      }
      return;
    }
  } catch (err) {
    self.postMessage({ id, type: "result", ok: false, stderr: String(err.message || err) });
  }
};
